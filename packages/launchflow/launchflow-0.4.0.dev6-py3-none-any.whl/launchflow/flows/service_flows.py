import asyncio
import datetime
import logging
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import beaupy
import rich
import yaml

from launchflow import exceptions
from launchflow.aws.service import AWSService
from launchflow.config import config
from launchflow.flows.flow_logger import FlowLogger, WorkflowProgress
from launchflow.flows.flow_utils import compare_dicts
from launchflow.gcp.service import GCPService
from launchflow.locks import Lock, LockInfo, LockOperation, OperationType, ReleaseReason
from launchflow.managers.environment_manager import EnvironmentManager
from launchflow.managers.service_manager import ServiceManager
from launchflow.models.enums import EnvironmentStatus, ServiceProduct, ServiceStatus
from launchflow.models.flow_state import (
    AWSEnvironmentConfig,
    GCPEnvironmentConfig,
    ServiceState,
)
from launchflow.models.launchflow_uri import LaunchFlowURI
from launchflow.service import Service
from launchflow.utils import generate_deployment_id
from launchflow.validation import validate_service_name
from launchflow.workflows.common_inputs import DockerBuildInputs
from launchflow.workflows.deploy_aws_service.deploy_aws_service import (
    deploy_aws_ecs_fargate_build_local,
    deploy_aws_ecs_fargate_build_remote,
    promote_aws_ecs_fargate,
)
from launchflow.workflows.deploy_aws_service.schemas import (
    AWSPromotionInputs,
    DeployECSFargateInputs,
    PromoteECSFargateInputs,
)
from launchflow.workflows.deploy_gcp_service.deploy_gcp_service import (
    deploy_gcp_cloud_run_build_local,
    deploy_gcp_cloud_run_build_remote,
    promote_gcp_cloud_run,
)
from launchflow.workflows.deploy_gcp_service.schemas import (
    DeployCloudRunInputs,
    GCPPromotionInputs,
    PromoteCloudRunInputs,
)


# TODO: move this to a common util
def dump_service_inputs(service_inputs: Dict[str, Any]):
    return yaml.safe_dump(service_inputs).replace("'", "")


@dataclass(frozen=True)
class DeployServicePlan:
    service: Service
    service_manager: ServiceManager
    existing_service: Optional[ServiceState]
    verbose: bool

    @property
    def service_ref(self) -> str:
        if self.verbose:
            return str(self.service)
        return f"{self.service.__class__.__name__}({self.service.name})"

    def print_plan(self):
        if (
            self.existing_service is None
            or self.existing_service.status == ServiceStatus.DEPLOY_FAILED
        ):
            input_args = self.service.inputs().to_dict()
            if input_args:
                service_inputs_str = dump_service_inputs(input_args)
                rich.print(
                    f"[blue]{self.service_ref}[/blue] will be [bold green]deployed[/bold green] with the following configuration:"
                )

                rich.print("    " + "\n    ".join(service_inputs_str.split("\n")))
            else:
                rich.print(
                    f"[blue]{self.service_ref}[/blue] will be [bold green]deployed[/bold green] with the default configuration."
                )
                print()
            return
        # TODO: look into case where arguments are None, it should always be set
        existing_args = self.existing_service.inputs or {}
        args_diff = compare_dicts(existing_args, self.service.inputs().to_dict())
        if args_diff:
            rich.print(
                f"[red]{self.service_ref} has changed arguments:[/red]\n{args_diff}"
            )
        else:
            rich.print(
                f"[green]{self.service_ref} matches the existing service configuration[/green]"
            )
        print()


@dataclass(frozen=True)
class DeployGCPServicePlan(DeployServicePlan):
    gcp_environment_config: GCPEnvironmentConfig


@dataclass(frozen=True)
class DeployAWSServicePlan(DeployServicePlan):
    aws_environment_config: AWSEnvironmentConfig


@dataclass(frozen=True)
class PromoteServicePlan:
    to_service: Service
    from_service_manager: ServiceManager
    to_service_manager: ServiceManager
    existing_from_service: ServiceState
    existing_to_service: Optional[ServiceState]
    verbose: bool

    @property
    def service_ref(self) -> str:
        if self.verbose:
            return str(self.to_service)
        return f"{self.to_service.__class__.__name__}({self.to_service.name})"

    def print_plan(self):
        input_args = self.to_service.inputs().to_dict()
        if input_args:
            service_inputs_str = dump_service_inputs(input_args)
            rich.print(
                f"[blue]{self.service_ref}[/blue] will be [bold green]promoted[/bold green] with the following configuration:"
            )

            rich.print("    " + "\n    ".join(service_inputs_str.split("\n")))
        else:
            rich.print(
                f"[blue]{self.service_ref}[/blue] will be [bold green]promoted[/bold green] with the default configuration."
            )
            print()


@dataclass(frozen=True)
class PromoteGCPServicePlan(PromoteServicePlan):
    from_gcp_environment_config: GCPEnvironmentConfig
    to_gcp_environment_config: GCPEnvironmentConfig


@dataclass(frozen=True)
class PromoteAWSServicePlan(PromoteServicePlan):
    from_aws_environment_config: AWSEnvironmentConfig
    to_aws_environment_config: AWSEnvironmentConfig


@dataclass(frozen=True)
class ServiceOutputs:
    aws_arn: Optional[str]
    gcp_id: Optional[str]
    service_url: Optional[str]
    docker_image: Optional[str]


async def _deploy_gcp_service(
    gcp_service_plan: DeployGCPServicePlan,
    lock_info: LockInfo,
    launchflow_uri: LaunchFlowURI,
    workflow_progress: WorkflowProgress,
    infrastructure_logs: str,
    build_logs: str,
    build_local: bool,
) -> ServiceOutputs:
    full_yaml_path = os.path.dirname(
        os.path.abspath(config.launchflow_yaml.config_path)
    )
    local_source_dir = os.path.join(
        full_yaml_path, gcp_service_plan.service._build_directory
    )

    if gcp_service_plan.service.product == ServiceProduct.GCP_CLOUD_RUN:
        inputs = DeployCloudRunInputs(
            gcp_service=gcp_service_plan.service,
            deployment_id=generate_deployment_id(),
            lock_id=lock_info.lock_id,
            launchflow_uri=launchflow_uri,
            gcp_environment_config=gcp_service_plan.gcp_environment_config,
            docker_build_inputs=DockerBuildInputs(
                source_tarball_bucket=gcp_service_plan.gcp_environment_config.artifact_bucket,
                source_tarball_path=f"builds/{gcp_service_plan.service_manager.project_name}/{gcp_service_plan.service_manager.environment_name}/services/{gcp_service_plan.service_manager.service_name}/source.tar.gz",
                dockerfile_path=gcp_service_plan.service._dockerfile,
                local_source_dir=local_source_dir,
            ),
            infrastructure_logs=infrastructure_logs,
            build_logs=build_logs,
        )
        # TODO: Determine if we should just branch the logic in the workflow. Feels a bit leaky here.
        if build_local:
            outputs = await deploy_gcp_cloud_run_build_local(
                inputs,
                workflow_progress=workflow_progress,
            )
        else:
            outputs = await deploy_gcp_cloud_run_build_remote(
                inputs,
                workflow_progress=workflow_progress,
            )
    else:
        raise NotImplementedError(
            f"Service product {gcp_service_plan.service.product} is not supported"
        )
    return ServiceOutputs(
        aws_arn=None,
        gcp_id=outputs.gcp_id,
        service_url=outputs.service_url,
        docker_image=outputs.docker_image,
    )


async def _deploy_aws_service(
    aws_service_plan: DeployAWSServicePlan,
    lock_info: LockInfo,
    launchflow_uri: LaunchFlowURI,
    workflow_progress: WorkflowProgress,
    logs_dir: str,
    build_logs: str,
    build_local: bool,
) -> ServiceOutputs:
    full_yaml_path = os.path.dirname(
        os.path.abspath(config.launchflow_yaml.config_path)
    )
    local_source_dir = os.path.join(
        full_yaml_path, aws_service_plan.service._build_directory
    )

    if aws_service_plan.service.product == ServiceProduct.AWS_ECS_FARGATE:
        inputs = DeployECSFargateInputs(
            aws_service=aws_service_plan.service,
            deployment_id=generate_deployment_id(),
            lock_id=lock_info.lock_id,
            launchflow_uri=launchflow_uri,
            aws_environment_config=aws_service_plan.aws_environment_config,
            docker_build_inputs=DockerBuildInputs(
                source_tarball_bucket=aws_service_plan.aws_environment_config.artifact_bucket,
                source_tarball_path=f"builds/{aws_service_plan.service_manager.project_name}/{aws_service_plan.service_manager.environment_name}/services/{aws_service_plan.service_manager.service_name}/source.tar.gz",
                dockerfile_path=aws_service_plan.service._dockerfile,
                local_source_dir=local_source_dir,
            ),
            infrastructure_logs=logs_dir,
            build_logs=build_logs,
        )
        # TODO: Determine if we should just branch the logic in the workflow. Feels a bit leaky here.
        if build_local:
            outputs = await deploy_aws_ecs_fargate_build_local(
                inputs,
                workflow_progress=workflow_progress,
            )
        else:
            outputs = await deploy_aws_ecs_fargate_build_remote(
                inputs,
                workflow_progress=workflow_progress,
            )
    else:
        raise NotImplementedError(
            f"Service product {aws_service_plan.service.product} is not supported"
        )
    return ServiceOutputs(
        gcp_id=None,
        aws_arn=outputs.aws_arn,
        service_url=outputs.service_url,
        docker_image=outputs.docker_image,
    )


async def _execute_deploy_plan(
    plan: DeployServicePlan, lock: Lock, logger: FlowLogger, build_local: bool
):
    async with lock as lock_info:
        base_logging_dir = "/tmp/launchflow"
        os.makedirs(base_logging_dir, exist_ok=True)
        build_logs = (
            f"{base_logging_dir}/{plan.service.name}-build-{int(time.time())}.log"
        )
        infrastructure_logs = (
            f"{base_logging_dir}/{plan.service.name}-{int(time.time())}.log"
        )

        # TODO: Dont pass service_ref here, too long when verbose is True
        # TODO: explore the idea of adding the service plan inside the deployment panel
        # TODO: Make the num_steps dynamic so we dont have to pass in ahead of time
        num_steps = 4
        if build_local:
            num_steps = 3
        with logger.start_workflow(
            plan.service_ref,
            num_steps=num_steps,
            infrastructure_logs=infrastructure_logs,
        ) as workflow_progress:
            workflow_progress.update(f"Deploying {plan.service_ref}")
            launchflow_uri = LaunchFlowURI(
                project_name=plan.service_manager.project_name,
                environment_name=plan.service_manager.environment_name,
                service_name=plan.service_manager.service_name,
            )

            updated_time = datetime.datetime.now(datetime.timezone.utc)
            created_time = (
                plan.existing_service.created_at
                if plan.existing_service
                else updated_time
            )
            status = ServiceStatus.DEPLOYING
            new_service_state = ServiceState(
                name=plan.service.name,
                product=plan.service.product,
                cloud_provider=plan.service.product.cloud_provider(),
                created_at=created_time,
                updated_at=updated_time,
                status=status,
                inputs=plan.service.inputs().to_dict(),
            )
            to_save = new_service_state.model_copy()

            try:
                if isinstance(plan, DeployGCPServicePlan):
                    outputs = await _deploy_gcp_service(
                        plan,
                        lock_info,
                        launchflow_uri,
                        workflow_progress,
                        infrastructure_logs,
                        build_logs,
                        build_local,
                    )
                elif isinstance(plan, DeployAWSServicePlan):
                    outputs = await _deploy_aws_service(
                        plan,
                        lock_info,
                        launchflow_uri,
                        workflow_progress,
                        infrastructure_logs,
                        build_logs,
                        build_local,
                    )
                else:
                    raise NotImplementedError(
                        f"Service type {type(plan.service)} is not supported"
                    )

                to_save.aws_arn = outputs.aws_arn
                to_save.gcp_id = outputs.gcp_id
                to_save.docker_image = outputs.docker_image
                to_save.service_url = outputs.service_url
                to_save.status = ServiceStatus.READY

            # TODO: Move all the expcetion logic in the workflow to this block
            except Exception as e:
                # TODO: Log this to the logs_dir
                logging.error("Exception occurred: %s", e, exc_info=True)
                # Reset the service info to its original state
                if plan.existing_service is not None:
                    to_save.inputs = plan.existing_service.inputs
                    to_save.docker_image = plan.existing_service.docker_image
                    to_save.service_url = plan.existing_service.service_url
                    to_save.gcp_id = plan.existing_service.gcp_id
                else:
                    to_save.inputs = None
                    to_save.docker_image = None
                    to_save.service_url = None
                    to_save.gcp_id = None
                to_save.status = ServiceStatus.DEPLOY_FAILED

            await plan.service_manager.save_service(to_save, lock_info.lock_id)
            if to_save.status == ServiceStatus.READY:
                workflow_progress.update(f"[green]✓ {plan.service_ref} deployed 🚀")
                # TODO: Add some color to the outputs
                complete_message = (
                    f"\nOutputs:\n"
                    f"  Docker image: [blue]{to_save.docker_image}[/blue]\n"
                    f"  Service URL: [blue]{to_save.service_url}[/blue]\n"
                )
            else:
                workflow_progress.update(
                    f"[red]✗ {plan.service_ref} failed to deploy[/red]"
                )
                complete_message = ""

            workflow_progress.complete(complete_message)
            return to_save.status == ServiceStatus.READY


async def _execute_deploy_plans(
    service_plans: List[DeployServicePlan],
    environment_manager: EnvironmentManager,
    build_local: bool,
):
    locked_plans: List[Tuple[Lock, DeployServicePlan]] = []
    async with environment_manager.lock_environment(
        operation=LockOperation(operation_type=OperationType.LOCK_ENVIRONMENT)
    ):
        # Next we lock all resources to prevent them from being modified
        # And verify that the resources are still in the same state as when we
        # planned them
        for plan in service_plans:
            lock = await plan.service_manager.lock_service(
                operation=LockOperation(operation_type=OperationType.DEPLOY_SERVICE)
            )
            try:
                existing_service = await plan.service_manager.load_service()
            except exceptions.ServiceNotFound:
                existing_service = None
            if plan.existing_service != existing_service:
                # If the resource has changed since planning we release the lock
                # and will not attempt to execute the plan
                rich.print(
                    f"[red]✗ Service `{plan.service_ref})` state has changed since planning[/red]"
                )
                await lock.release(
                    lock_id=lock.lock_info.lock_id, reason=ReleaseReason.ABANDONED
                )
            else:
                locked_plans.append((lock, plan))

    with FlowLogger(count=len(locked_plans)) as logger:
        tasks = []
        for lock, plan in locked_plans:
            tasks.append(_execute_deploy_plan(plan, lock, logger, build_local))
        results = await asyncio.gather(*tasks)
        success_count = 0
        failure_count = 0
        for result in results:
            if result:
                success_count += 1
            else:
                failure_count += 1

    print()
    if success_count:
        rich.print(f"[green]Successfully deployed {success_count} services[/green] ")
    if failure_count:
        rich.print(f"[red]Failed to deploy {failure_count} services[/red] ")
    print()


async def _promote_gcp_service(
    gcp_service_plan: PromoteGCPServicePlan,
    lock_info: LockInfo,
    launchflow_uri: LaunchFlowURI,
    workflow_progress: WorkflowProgress,
    logs_dir: str,
) -> ServiceOutputs:
    if gcp_service_plan.to_service.product == ServiceProduct.GCP_CLOUD_RUN:
        inputs = PromoteCloudRunInputs(
            gcp_service=gcp_service_plan.to_service,
            deployment_id=generate_deployment_id(),
            lock_id=lock_info.lock_id,
            launchflow_uri=launchflow_uri,
            gcp_environment_config=gcp_service_plan.to_gcp_environment_config,
            gcp_promote_inputs=GCPPromotionInputs(
                source_docker_image=gcp_service_plan.existing_from_service.docker_image,
                source_env_region=gcp_service_plan.from_gcp_environment_config.default_region,
            ),
            infrastructure_logs=logs_dir,
        )
        outputs = await promote_gcp_cloud_run(
            inputs,
            workflow_progress=workflow_progress,
        )
    else:
        raise NotImplementedError(
            f"Service product {gcp_service_plan.to_service.product} is not supported"
        )
    return ServiceOutputs(
        aws_arn=None,
        gcp_id=outputs.gcp_id,
        service_url=outputs.service_url,
        docker_image=outputs.docker_image,
    )


async def _promote_aws_service(
    aws_service_plan: PromoteAWSServicePlan,
    lock_info: LockInfo,
    launchflow_uri: LaunchFlowURI,
    workflow_progress: WorkflowProgress,
    logs_dir: str,
) -> ServiceOutputs:
    if aws_service_plan.to_service.product == ServiceProduct.AWS_ECS_FARGATE:
        inputs = PromoteECSFargateInputs(
            aws_service=aws_service_plan.to_service,
            deployment_id=generate_deployment_id(),
            lock_id=lock_info.lock_id,
            launchflow_uri=launchflow_uri,
            aws_environment_config=aws_service_plan.to_aws_environment_config,
            aws_promote_inputs=AWSPromotionInputs(
                source_docker_image=aws_service_plan.existing_from_service.docker_image,
                source_env_region=aws_service_plan.from_aws_environment_config.region,
                source_tarball_path=f"builds/{aws_service_plan.to_service_manager.project_name}/{aws_service_plan.to_service_manager.environment_name}/services/{aws_service_plan.to_service_manager.service_name}/source.tar.gz",
            ),
            infrastructure_logs=logs_dir,
        )
        outputs = await promote_aws_ecs_fargate(
            inputs,
            workflow_progress=workflow_progress,
        )
    else:
        raise NotImplementedError(
            f"Service product {aws_service_plan.to_service.product} is not supported"
        )
    return ServiceOutputs(
        gcp_id=None,
        aws_arn=outputs.aws_arn,
        service_url=outputs.service_url,
        docker_image=outputs.docker_image,
    )


async def _execute_promote_plan(
    plan: PromoteServicePlan, lock: Lock, logger: FlowLogger
):
    async with lock as lock_info:
        base_logging_dir = "/tmp/launchflow"
        os.makedirs(base_logging_dir, exist_ok=True)
        logs_dir = f"{base_logging_dir}/{plan.to_service.name}-{int(time.time())}.log"

        # TODO: Dont pass service_ref here, too long when verbose is True
        # TODO: explore the idea of adding the service plan inside the deployment panel
        # TODO: Make the num_steps dynamic so we dont have to pass in ahead of time
        num_steps = 3
        with logger.start_workflow(
            plan.service_ref, num_steps=num_steps, infrastructure_logs=logs_dir
        ) as workflow_progress:
            workflow_progress.update(f"Promoting {plan.service_ref}")
            launchflow_uri = LaunchFlowURI(
                project_name=plan.to_service_manager.project_name,
                environment_name=plan.to_service_manager.environment_name,
                service_name=plan.to_service_manager.service_name,
            )

            updated_time = datetime.datetime.now(datetime.timezone.utc)
            created_time = (
                plan.existing_to_service.created_at
                if plan.existing_to_service
                else updated_time
            )
            status = ServiceStatus.PROMOTING
            new_service_state = ServiceState(
                name=plan.to_service.name,
                product=plan.to_service.product,
                cloud_provider=plan.to_service.product.cloud_provider(),
                created_at=created_time,
                updated_at=updated_time,
                status=status,
                inputs=plan.to_service.inputs().to_dict(),
            )
            to_save = new_service_state.model_copy()

            try:
                if isinstance(plan, PromoteGCPServicePlan):
                    outputs = await _promote_gcp_service(
                        plan,
                        lock_info,
                        launchflow_uri,
                        workflow_progress,
                        logs_dir,
                    )
                elif isinstance(plan, PromoteAWSServicePlan):
                    outputs = await _promote_aws_service(
                        plan,
                        lock_info,
                        launchflow_uri,
                        workflow_progress,
                        logs_dir,
                    )
                else:
                    raise NotImplementedError(
                        f"Service type {type(plan.to_service)} is not supported"
                    )

                to_save.aws_arn = outputs.aws_arn
                to_save.gcp_id = outputs.gcp_id
                to_save.docker_image = outputs.docker_image
                to_save.service_url = outputs.service_url
                to_save.status = ServiceStatus.READY

            # TODO: Move all the expcetion logic in the workflow to this block
            except Exception as e:
                # TODO: Log this to the logs_dir
                logging.error("Exception occurred: %s", e, exc_info=True)
                # Reset the service info to its original state
                if plan.existing_to_service is not None:
                    to_save.inputs = plan.existing_to_service.inputs
                    to_save.docker_image = plan.existing_to_service.docker_image
                    to_save.service_url = plan.existing_to_service.service_url
                    to_save.gcp_id = plan.existing_to_service.gcp_id
                else:
                    to_save.inputs = None
                    to_save.docker_image = None
                    to_save.service_url = None
                    to_save.gcp_id = None
                to_save.status = ServiceStatus.PROMOTE_FAILED

            await plan.to_service_manager.save_service(to_save, lock_info.lock_id)
            if to_save.status == ServiceStatus.READY:
                workflow_progress.update(f"[green]✓ {plan.service_ref} promoted 🚀")
                # TODO: Add some color to the outputs
                workflow_progress.complete(
                    f"\nOutputs:\n"
                    f"  Docker image: [blue]{to_save.docker_image}[/blue]\n"
                    f"  Service URL: [blue]{to_save.service_url}[/blue]\n"
                    f"\nView deployment logs at: [blue]{logs_dir}[/blue]\n"
                )
            else:
                workflow_progress.update(
                    f"[red]✗ {plan.service_ref} failed to promote[/red]"
                )
                workflow_progress.complete(
                    f"\nView deployment logs at: [blue]{logs_dir}[/blue]\n"
                )

            return to_save.status == ServiceStatus.READY


async def _execute_promote_plans(
    service_plans: List[PromoteServicePlan],
    to_environment_manager: EnvironmentManager,
):
    locked_plans: List[Tuple[Lock, DeployServicePlan]] = []
    async with to_environment_manager.lock_environment(
        operation=LockOperation(operation_type=OperationType.LOCK_ENVIRONMENT)
    ):
        # Next we lock all resources to prevent them from being modified
        # And verify that the resources are still in the same state as when we
        # planned them
        for plan in service_plans:
            lock = await plan.to_service_manager.lock_service(
                operation=LockOperation(operation_type=OperationType.PROMOTE_SERVICE)
            )
            try:
                existing_service = await plan.to_service_manager.load_service()
            except exceptions.ServiceNotFound:
                existing_service = None
            if plan.existing_to_service != existing_service:
                # If the resource has changed since planning we release the lock
                # and will not attempt to execute the plan
                rich.print(
                    f"[red]✗ Service `{plan.service_ref})` state has changed since planning[/red]"
                )
                await lock.release(
                    lock_id=lock.lock_info.lock_id, reason=ReleaseReason.ABANDONED
                )
            else:
                locked_plans.append((lock, plan))

    with FlowLogger(count=len(locked_plans)) as logger:
        tasks = []
        for lock, plan in locked_plans:
            tasks.append(_execute_promote_plan(plan, lock, logger))
        results = await asyncio.gather(*tasks)
        success_count = 0
        failure_count = 0
        for result in results:
            if result:
                success_count += 1
            else:
                failure_count += 1

    print()
    if success_count:
        rich.print(f"[green]Successfully promoted {success_count} services[/green] ")
    if failure_count:
        rich.print(f"[red]Failed to promote {failure_count} services[/red] ")
    print()


async def plan_deploy_services(
    *services: Service,
    environment_manager: EnvironmentManager,
    verbose: bool,
) -> List[DeployServicePlan]:
    environment = await environment_manager.load_environment()
    # Should we lock here while reading the state below? We could unlock right before we prompt the user
    # TODO: determine if we should also hash / compare the environment state
    if environment.status != EnvironmentStatus.READY:
        raise exceptions.EnvironmentNotReady(environment_manager.environment_name)

    service_plans: List[DeployServicePlan] = []
    for service in services:
        validate_service_name(service.name)
        service_manager = environment_manager.create_service_manager(service.name)
        try:
            existing_service = await service_manager.load_service()
            if existing_service.product != service.product:
                raise exceptions.ServiceProductMismatch(
                    existing_service.product, service.name
                )
            if existing_service.status.is_pending():
                raise exceptions.ServiceIsPending(service.name)
        except exceptions.ServiceNotFound:
            existing_service = None

        if isinstance(service, GCPService):
            gcp_environment_config = environment.gcp_config
            if gcp_environment_config is None:
                raise exceptions.GCPConfigNotFound(environment_manager.environment_name)
            service_plans.append(
                DeployGCPServicePlan(
                    service=service,
                    service_manager=service_manager,
                    existing_service=existing_service,
                    verbose=verbose,
                    gcp_environment_config=gcp_environment_config,
                )
            )
        elif isinstance(service, AWSService):
            aws_environment_config = environment.aws_config
            if aws_environment_config is None:
                raise exceptions.AWSConfigNotFound(environment_manager.environment_name)
            service_plans.append(
                DeployAWSServicePlan(
                    service=service,
                    service_manager=service_manager,
                    existing_service=existing_service,
                    verbose=verbose,
                    aws_environment_config=aws_environment_config,
                )
            )

        else:
            raise NotImplementedError(f"Service type {type(service)} is not supported")

    return service_plans


async def plan_promote_services(
    *services: Service,
    from_environment_manager: EnvironmentManager,
    to_environment_manager: EnvironmentManager,
    verbose: bool,
) -> List[PromoteServicePlan]:
    from_environment = await from_environment_manager.load_environment()
    to_environment = await to_environment_manager.load_environment()
    # Should we lock here while reading the state below? We could unlock right before we prompt the user
    if from_environment.status != EnvironmentStatus.READY:
        raise exceptions.EnvironmentNotReady(from_environment_manager.environment_name)
    if to_environment.status != EnvironmentStatus.READY:
        raise exceptions.EnvironmentNotReady(to_environment_manager.environment_name)
    service_plans: List[PromoteServicePlan] = []
    for service in services:
        validate_service_name(service.name)
        from_service_manager = from_environment_manager.create_service_manager(
            service.name
        )
        to_service_manager = to_environment_manager.create_service_manager(service.name)
        from_service_state = await from_service_manager.load_service()
        if from_service_state.status != ServiceStatus.READY:
            raise exceptions.ServiceNotReady(from_service_manager.service_name)
        if from_service_state.product != service.product:
            raise exceptions.ServiceProductMismatch(
                from_service_state.product, service.name
            )

        try:
            to_service_state = await to_service_manager.load_service()
            if to_service_state.product != service.product:
                raise exceptions.ServiceProductMismatch(
                    to_service_state.product, service.name
                )
            if to_service_state.status.is_pending():
                raise exceptions.ServiceIsPending(service.name)
        except exceptions.ServiceNotFound:
            to_service_state = None

        if isinstance(service, GCPService):
            from_gcp_environment_config = from_environment.gcp_config
            if from_gcp_environment_config is None:
                raise exceptions.GCPConfigNotFound(
                    from_environment_manager.environment_name
                )
            to_gcp_environment_config = to_environment.gcp_config
            if to_gcp_environment_config is None:
                raise exceptions.GCPConfigNotFound(
                    to_environment_manager.environment_name
                )
            service_plans.append(
                PromoteGCPServicePlan(
                    to_service=service,
                    from_service_manager=from_service_manager,
                    to_service_manager=to_service_manager,
                    existing_from_service=from_service_state,
                    existing_to_service=to_service_state,
                    verbose=verbose,
                    from_gcp_environment_config=from_gcp_environment_config,
                    to_gcp_environment_config=to_gcp_environment_config,
                )
            )
        elif isinstance(service, AWSService):
            from_aws_environment_config = from_environment.aws_config
            if from_aws_environment_config is None:
                raise exceptions.AWSConfigNotFound(
                    from_environment_manager.environment_name
                )
            to_aws_environment_config = to_environment.aws_config
            if to_aws_environment_config is None:
                raise exceptions.AWSConfigNotFound(
                    to_environment_manager.environment_name
                )
            service_plans.append(
                PromoteAWSServicePlan(
                    to_service=service,
                    from_service_manager=from_service_manager,
                    to_service_manager=to_service_manager,
                    existing_from_service=from_service_state,
                    existing_to_service=to_service_state,
                    verbose=verbose,
                    from_aws_environment_config=from_aws_environment_config,
                    to_aws_environment_config=to_aws_environment_config,
                )
            )
        else:
            raise NotImplementedError(f"Service type {type(service)} is not supported")

    return service_plans


async def _confirm_deploy_plans(
    service_plans: List[DeployServicePlan],
    environment_manager: EnvironmentManager,
):
    environment_ref = (
        f"{environment_manager.project_name}/{environment_manager.environment_name}"
    )
    if len(service_plans) == 1:
        selected_plan = service_plans[0]
        selected_plan.print_plan()
        answer = beaupy.confirm(
            f"[bold]Deploy[/bold] [blue]{selected_plan.service_ref}[/blue] to [bold yellow]`{environment_ref}`[/bold yellow]?"
        )
        if not answer:
            return []
        return [selected_plan]
    else:
        for selected_plan in service_plans:
            selected_plan.print_plan()
        rich.print(
            f"Select the services you want to deploy to [bold yellow]`{environment_ref}`[/bold yellow]."
        )
        selected_plans: List[DeployServicePlan] = beaupy.select_multiple(
            options=service_plans,
            preprocessor=lambda plan: plan.service_ref,
        )
        for plan in selected_plans:
            rich.print(f"[pink1]>[/pink1] {plan.service_ref}")
        print()
        return selected_plans


async def _confirm_promote_plans(
    service_plans: List[PromoteServicePlan],
    from_environment_manager: EnvironmentManager,
    to_environment_manager: EnvironmentManager,
):
    from_environment_ref = f"{from_environment_manager.project_name}/{from_environment_manager.environment_name}"
    to_environment_ref = f"{to_environment_manager.project_name}/{to_environment_manager.environment_name}"
    if len(service_plans) == 1:
        selected_plan = service_plans[0]
        selected_plan.print_plan()
        answer = beaupy.confirm(
            f"[bold]Promote[/bold] [blue]{selected_plan.service_ref}[/blue] from [bold yellow]`{from_environment_ref}`[/bold yellow] to [bold yellow]`{to_environment_ref}`[/bold yellow]?"
        )
        if not answer:
            return []
        return [selected_plan]
    else:
        for selected_plan in service_plans:
            selected_plan.print_plan()
        rich.print(
            f"Select the services you want to promote from [bold yellow]`{from_environment_ref}`[/bold yellow] to [bold yellow]`{to_environment_ref}`[/bold yellow]."
        )
        selected_plans: List[DeployServicePlan] = beaupy.select_multiple(
            options=service_plans,
            preprocessor=lambda plan: plan.service_ref,
        )
        for plan in selected_plans:
            rich.print(f"[pink1]>[/pink1] {plan.service_ref}")
        print()
        return selected_plans


async def deploy(
    *services: Service,
    environment: str,
    launchflow_api_key: Optional[str] = None,
    prompt: bool = True,
    # TODO: only include tofu logs if verbose is set, otherwise dump to /tmp/launchflow
    verbose: bool = False,
    build_local: bool = False,
):
    environment_manager = EnvironmentManager(
        project_name=config.launchflow_yaml.project,
        environment_name=environment,
        backend=config.launchflow_yaml.backend,
    )
    if launchflow_api_key is not None:
        # NOTE: This will throw an error if LaunchFlowBackend is not used
        environment_manager.set_launchflow_api_key(launchflow_api_key)

    # Stage 1: Build the service plans using the existing environment state
    all_service_plans = await plan_deploy_services(
        *services, environment_manager=environment_manager, verbose=verbose
    )
    if not all_service_plans:
        rich.print("No services to deploy. Exiting.")
        return

    # Stage 2: Confirm the service plans with the user
    if not prompt:
        selected_service_plans: List[DeployServicePlan] = all_service_plans
    else:
        selected_service_plans = await _confirm_deploy_plans(
            all_service_plans, environment_manager
        )
    if not selected_service_plans:
        rich.print("No services selected. Exiting.")
        return

    # Validate plans for correctness
    for plan in selected_service_plans:
        yaml_base_path = os.path.dirname(
            os.path.abspath(config.launchflow_yaml.config_path)
        )
        service_build_dir = os.path.normpath(
            os.path.join(yaml_base_path, plan.service._build_directory)
        )
        if not os.path.exists(plan.service._build_directory):
            raise exceptions.ServiceBuildDirectoryNotFound(
                plan.service.name, service_build_dir
            )
        docker_path = os.path.join(service_build_dir, plan.service._dockerfile)
        if not os.path.exists(docker_path):
            raise exceptions.ServiceDockerfileNotFound(plan.service.name, docker_path)

    # Stage 3: Execute plans
    # First we lock the environment to prevent the environment from being
    # modified while we are deploying services
    await _execute_deploy_plans(
        selected_service_plans, environment_manager, build_local
    )


async def promote(
    *services: Service,
    from_environment: str,
    to_environment: str,
    launchflow_api_key: Optional[str] = None,
    prompt: bool = True,
    verbose: bool = False,
):
    from_environment_manager = EnvironmentManager(
        project_name=config.launchflow_yaml.project,
        environment_name=from_environment,
        backend=config.launchflow_yaml.backend,
    )
    to_environment_manager = EnvironmentManager(
        project_name=config.launchflow_yaml.project,
        environment_name=to_environment,
        backend=config.launchflow_yaml.backend,
    )
    if launchflow_api_key is not None:
        # NOTE: This will throw an error if LaunchFlowBackend is not used
        from_environment_manager.set_launchflow_api_key(launchflow_api_key)
        to_environment_manager.set_launchflow_api_key(launchflow_api_key)

    # Stage 1: Build the service plans using the existing environment state
    all_service_plans = await plan_promote_services(
        *services,
        from_environment_manager=from_environment_manager,
        to_environment_manager=to_environment_manager,
        verbose=verbose,
    )
    if not all_service_plans:
        rich.print("No services to promote. Exiting.")
        return

    # Stage 2: Confirm the service plans with the user
    if not prompt:
        selected_service_plans: List[PromoteServicePlan] = all_service_plans
    else:
        selected_service_plans = await _confirm_promote_plans(
            all_service_plans, from_environment_manager, to_environment_manager
        )
    if not selected_service_plans:
        rich.print("No services selected. Exiting.")
        return

    # # Stage 3: Execute plans
    # # First we lock the environment to prevent the environment from being
    # # modified while we are promoting services
    await _execute_promote_plans(selected_service_plans, to_environment_manager)
