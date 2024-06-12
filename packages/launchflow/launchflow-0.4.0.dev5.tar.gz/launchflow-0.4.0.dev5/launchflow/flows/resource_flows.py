import asyncio
import dataclasses
import datetime
import io
import logging
import os
import sys
import time
from typing import Any, Dict, List, Literal, Optional, Tuple, cast

import beaupy
import deepdiff
import rich
import yaml
from docker.models.containers import Container
from rich.progress import Progress, SpinnerColumn, TextColumn

from launchflow import exceptions
from launchflow.cli.utils import import_from_string
from launchflow.clients.docker_client import DockerClient, docker_service_available
from launchflow.config import config
from launchflow.config.launchflow_yaml import LocalBackend
from launchflow.docker.resource import DockerResource
from launchflow.locks import Lock, LockInfo, LockOperation, OperationType, ReleaseReason
from launchflow.managers.environment_manager import EnvironmentManager
from launchflow.managers.resource_manager import ResourceManager
from launchflow.managers.service_manager import ServiceManager
from launchflow.models.enums import (
    EnvironmentType,
    ResourceProduct,
    ResourceStatus,
    ServiceProduct,
    ServiceStatus,
)
from launchflow.models.flow_state import (
    AWSEnvironmentConfig,
    EnvironmentState,
    GCPEnvironmentConfig,
    ResourceState,
    ServiceState,
)
from launchflow.models.launchflow_uri import LaunchFlowURI
from launchflow.node import Node
from launchflow.resource import Resource
from launchflow.service import Service
from launchflow.validation import validate_resource_name
from launchflow.workflows.apply_resource_tofu.create_tofu_resource import (
    create_tofu_resource,
)
from launchflow.workflows.apply_resource_tofu.schemas import ApplyResourceTofuInputs
from launchflow.workflows.destroy_resource_tofu.delete_tofu_resource import (
    delete_tofu_resource,
)
from launchflow.workflows.destroy_resource_tofu.schemas import DestroyResourceTofuInputs
from launchflow.workflows.destroy_service.destroy_service import (
    destroy_aws_ecs_fargate_service,
    destroy_gcp_cloud_run_service,
)
from launchflow.workflows.destroy_service.schemas import (
    DestroyAWSServiceInputs,
    DestroyGCPServiceInputs,
)
from launchflow.workflows.import_tofu_resource.import_tofu_resource import (
    import_tofu_resource,
)
from launchflow.workflows.import_tofu_resource.schemas import ImportResourceTofuInputs
from launchflow.workflows.manage_docker.manage_docker_resources import (
    create_docker_resource,
    destroy_docker_resource,
    replace_docker_resource,
)
from launchflow.workflows.manage_docker.schemas import (
    CreateResourceDockerInputs,
    DestroyResourceDockerInputs,
)


@dataclasses.dataclass
class ContainerResource:
    container: Container

    def __str__(self):
        return f'DockerContainer(name="{self.container.name}", image="{self.container.image.tags[0]}")'

    def __hash__(self) -> int:
        return hash(self.container.name)


@dataclasses.dataclass(frozen=True)
class DestroyServicePlan:
    service_name: str
    service_manager: ServiceManager
    existing_service: ServiceState

    @property
    def ref(self) -> str:
        return f"Service(name={self.service_name}, product={self.existing_service.product.value})"


@dataclasses.dataclass(frozen=True)
class DestroyGCPServicePlan(DestroyServicePlan):
    gcp_environment_config: GCPEnvironmentConfig


@dataclasses.dataclass(frozen=True)
class DestroyAWSServicePlan(DestroyServicePlan):
    aws_environment_config: AWSEnvironmentConfig


@dataclasses.dataclass(frozen=True)
class DestroyResourcePlan:
    resource_name: str
    resource: ResourceState
    resource_manager: ResourceManager

    @property
    def ref(self) -> str:
        return f"Resource(name={self.resource_name}, product={self.resource.product.value})"


def dump_resource_inputs(resource_inputs: Dict[str, Any]):
    return yaml.safe_dump(resource_inputs).replace("'", "")


@dataclasses.dataclass
class CreateResourcePlan:
    resource: Resource
    resource_manager: ResourceManager
    existing_resource: Optional[ResourceState]
    environment_type: EnvironmentType
    operation_type: Literal["create", "update", "replace", "noop"] = "create"

    def __post_init__(self):
        if self.existing_resource is None:
            self.operation_type = "create"
            return
        if self.existing_resource.status == ResourceStatus.CREATE_FAILED:
            self.operation_type = "create"
            return

        self.operation_type = "noop"
        new_resource_inputs = self.resource.inputs(self.environment_type).to_dict()
        existing_resource_inputs = self.existing_resource.inputs or {}
        diff = deepdiff.DeepDiff(
            existing_resource_inputs, new_resource_inputs, ignore_order=True
        )
        if diff.affected_root_keys:
            for key in diff.affected_root_keys:
                if key in self.resource.replacement_arguments:
                    self.operation_type = "replace"
                    return
                else:
                    self.operation_type = "update"

    def print_plan(self, console: rich.console.Console = rich.console.Console()):
        if self.existing_resource is None or (
            # This second case handles the case where the resource initially failed to create
            self.existing_resource.inputs is None
            and self.existing_resource.status == ResourceStatus.CREATE_FAILED
        ):
            resource_inputs = self.resource.inputs(self.environment_type).to_dict()
            if resource_inputs:
                resource_inputs_str = dump_resource_inputs(resource_inputs)
                console.print(
                    f"[blue]{self.resource.__class__.__name__}({self.resource.name})[/blue] will be [bold green]created[/bold green] with the following configuration:"
                )

                console.print("    " + "\n    ".join(resource_inputs_str.split("\n")))
            else:
                console.print(
                    f"[blue]{self.resource.__class__.__name__}({self.resource.name})[/blue] will be [bold green]created[/bold green] with the default configuration."
                )
                print()
        else:
            args_diff = compare_dicts(
                self.existing_resource.inputs,
                self.resource.inputs(self.environment_type).to_dict(),
            )
            if args_diff:
                op_msg = "updated"
                if self.operation_type == "replace":
                    op_msg = "replaced"
                console.print(
                    f"[blue]{self.resource.__class__.__name__}({self.resource.name})[/blue] will be [bold red]{op_msg}[/bold red] with the following updates:\n    {args_diff}"
                )
            print()

        if self.resource.depends_on:
            console.print("    [yellow]Depends on:[/yellow]")
            for dep in self.resource.depends_on:
                console.print(
                    f"        [blue]{dep.__class__.__name__}({dep.name})[/blue]"
                )
            print()

    def task_description(self):
        if self.operation_type == "create":
            return f"Creating [blue]{self.resource.__class__.__name__}({self.resource.name})[/blue]..."
        if self.operation_type == "update":
            return f"Updating [blue]{self.resource.__class__.__name__}({self.resource.name})[/blue]..."
        if self.operation_type == "replace":
            return f"Replacing [blue]{self.resource.__class__.__name__}({self.resource.name})[/blue]..."

    def success_message(self):
        if self.operation_type == "create":
            return f"[green]✓[/green] Successfully created [blue]{self.resource.__class__.__name__}({self.resource.name})[/blue]"
        if self.operation_type == "update":
            return f"[green]✓[/green] Successfully updated [blue]{self.resource.__class__.__name__}({self.resource.name})[/blue]"
        if self.operation_type == "replace":
            return f"[green]✓[/green] Successfully replaced [blue]{self.resource.__class__.__name__}({self.resource.name})[/blue]"

    def failure_message(self):
        return f"[red]✗[/red] Failed to {self.operation_type} [blue]{self.resource.__class__.__name__}({self.resource.name})[/blue]"


def compare_dicts(d1, d2):
    diff = deepdiff.DeepDiff(d1, d2, ignore_order=True)
    diff_keys = diff.affected_root_keys
    diff_strs = []
    for key in diff_keys:
        old_value = d1.get(key)
        new_value = d2.get(key)
        diff_strs.append(f"[cyan]{key}[/cyan]: {old_value} -> {new_value}")
    return "\n    ".join(diff_strs)


def deduplicate_resources(resources: Tuple[Resource]) -> List[Resource]:
    """
    Deduplicate resources based on matching name and product name.

    Args:
    - `resources`: The resources to deduplicate.

    Returns:
    - The deduplicated resources.
    """
    resource_dict = {}

    for resource in resources:
        if resource.name in resource_dict:
            existing_resource = resource_dict[resource.name]
            if existing_resource.product != resource.product:
                raise exceptions.DuplicateResourceProductMismatch(
                    resource_name=resource.name,
                    existing_product=existing_resource.product.name,
                    new_product=resource.product.name,
                )
        resource_dict[resource.name] = resource

    return list(resource_dict.values())


def import_resources(resource_import_strs: List[str]) -> List[Resource]:
    sys.path.insert(0, "")
    resources: List[Resource] = []
    for resource_str in resource_import_strs:
        imported_resource = import_from_string(resource_str)
        if not isinstance(imported_resource, Resource):
            continue
        resources.append(imported_resource)
    return resources


def is_local_resource(resource: Resource) -> bool:
    if isinstance(resource, DockerResource):
        return True

    return False


async def _confirm_plan(
    environment_manager: EnvironmentManager,
    resource_plans: List[CreateResourcePlan],
) -> List[CreateResourcePlan]:
    environment_ref = (
        f"{environment_manager.project_name}/{environment_manager.environment_name}"
    )
    if len(resource_plans) == 1:
        selected_plan = resource_plans[0]
        resource_ref = f"{selected_plan.resource.__class__.__name__}({selected_plan.resource.name})"
        selected_plan.print_plan()
        answer = beaupy.confirm(
            f"[bold]{selected_plan.operation_type.capitalize()}[/bold] [blue]{resource_ref}[/blue] in [bold yellow]`{environment_ref}`[/bold yellow]?"
        )
        if not answer:
            rich.print("User cancelled resource creation. Exiting.")
            return
        selected_plans = [selected_plan]
    else:
        for plan in resource_plans:
            plan.print_plan()
        rich.print(
            f"Select the resources you want to change in [bold yellow]`{environment_ref}`[/bold yellow]:"
        )
        selected_plans: List[CreateResourcePlan] = beaupy.select_multiple(
            options=resource_plans,
            preprocessor=lambda plan: f"[bold]{plan.operation_type.capitalize()}[/bold] {plan.resource.__class__.__name__}({plan.resource.name})",
        )
        for plan in selected_plans:
            rich.print(
                f"[[pink1]✓[/pink1]] [pink1]{plan.resource.__class__.__name__}({plan.resource.name})[/pink1]"
            )
        print()
    return selected_plans


async def plan_resources(
    environment_manager: EnvironmentManager,
    *resources: Resource,
) -> List[CreateResourcePlan]:
    resource_plans: List[CreateResourcePlan] = []

    # Stage 1: Load all resources and build our plan
    # NOTE: we lazy load the env type to avoid loading the environment for
    # local resources. This allows users to create local resources without
    # having any AWS / GCP credentials required to read the artifact bucket
    env_type = None
    for resource in resources:
        validate_resource_name(resource.name)
        if is_local_resource(resource):
            resource_manager = environment_manager.create_docker_resource_manager(
                resource.name
            )
        else:
            if env_type is None:
                environment = await environment_manager.load_environment()
                env_type = environment.environment_type
            resource_manager = environment_manager.create_resource_manager(
                resource.name
            )
        try:
            existing_resource = await resource_manager.load_resource()
        except exceptions.ResourceNotFound:
            existing_resource = None

        if (
            existing_resource is not None
            and existing_resource.product != resource.product
        ):
            raise exceptions.ResourceProductMismatch(
                existing_product=existing_resource.product.name,
                new_product=resource.product,
            )

        plan = CreateResourcePlan(
            resource=resource,
            resource_manager=resource_manager,
            existing_resource=existing_resource,
            environment_type=env_type,
        )
        if plan.operation_type == "noop":
            rich.print(
                f"[green][blue]{resource.__class__.__name__}({resource.name})[/blue] is up to date.[/green]"
            )
            print()
            continue

        resource_plans.append(plan)
    return resource_plans


async def _create_or_update_tofu_resource(
    new_resource_state: ResourceState,
    plan: CreateResourcePlan,
    environment: EnvironmentState,
    launchflow_uri: LaunchFlowURI,
    lock_info: LockInfo,
    logs_dir: str,
) -> ResourceState:
    inputs = ApplyResourceTofuInputs(
        launchflow_uri=launchflow_uri,
        backend=plan.resource_manager.backend,
        gcp_env_config=environment.gcp_config,
        aws_env_config=environment.aws_config,
        resource=new_resource_state,
        lock_id=lock_info.lock_id,
        logs_dir=logs_dir,
    )

    to_save = new_resource_state.model_copy()
    try:
        outputs = await create_tofu_resource(inputs)
        to_save.aws_arn = outputs.aws_arn
        to_save.gcp_id = outputs.gcp_id
        to_save.status = ResourceStatus.READY
    except Exception as e:
        # TODO: Log this to the logs_dir
        logging.error("Exception occurred: %s", e, exc_info=True)
        # Reset the create args to their original state
        if to_save.status == ResourceStatus.CREATING:
            to_save.inputs = None
            to_save.status = ResourceStatus.CREATE_FAILED
        else:
            to_save.inputs = plan.existing_resource.inputs
            to_save.status = ResourceStatus.UPDATE_FAILED

    return to_save


async def _create_or_update_docker_resource(
    plan: CreateResourcePlan,
    new_resource_state: ResourceState,
    operation_type: str,
    logs_dir: str,
) -> ResourceState:
    resource: DockerResource = plan.resource

    inputs = CreateResourceDockerInputs(
        resource=new_resource_state,
        image=resource.docker_image,
        env_vars=resource.env_vars,
        command=resource.command,
        ports=resource.ports,
        logs_dir=logs_dir,
    )

    to_save = new_resource_state.model_copy()
    if operation_type == "create":
        fn = create_docker_resource
    elif operation_type == "update":
        fn = replace_docker_resource
    else:
        raise NotImplementedError(f"Got an unexpected operator type {operation_type}.")
    try:
        outputs = await fn(inputs)

        # Store the connection info next to where the flow state will be stored
        # This  is not great but better than storing in the flow state
        launchflow_yaml_path = config.launchflow_yaml.config_path
        project_name = plan.resource_manager.project_name
        environment_name = plan.resource_manager.environment_name
        connection_info_path = os.path.join(
            os.path.dirname(launchflow_yaml_path),
            ".launchflow",
            "docker",
            project_name,
            environment_name,
            "resources",
            inputs.resource.name,
            "connection_info.yaml",
        )
        resource.ports.update(outputs.ports)
        resource.running_container_id = outputs.container.id

        # These steps must be done after the resource has been updated, otherwise incorrect data
        # will be stored to disk.
        to_save.inputs = dataclasses.asdict(resource.inputs())
        os.makedirs(os.path.dirname(connection_info_path), exist_ok=True)
        connection_info = resource.connection_info()
        if connection_info is None:
            raise ValueError(
                "Failed to generate connection info after creating docker resource."
            )
        with open(connection_info_path, "w") as file:
            file.write(yaml.dump(connection_info.to_dict()))

        to_save.status = ResourceStatus.READY
    except Exception as e:
        logging.error("Exception occurred: %s", e, exc_info=True)
        # Reset the create args to their original state
        if to_save.status == ResourceStatus.CREATING:
            to_save.inputs = None
            to_save.status = ResourceStatus.CREATE_FAILED
        else:
            to_save.inputs = plan.existing_resource.inputs
            to_save.status = ResourceStatus.UPDATE_FAILED

    return to_save


async def _execute_plan(
    plan_node: "_CreatePlanNode",
    environment: Optional[EnvironmentState],
    progress: Progress,
):
    lock = plan_node.lock
    plan = plan_node.plan
    env_type = None
    if environment is not None:
        env_type = environment.environment_type
    async with lock as lock_info:
        base_logging_dir = "/tmp/launchflow"
        os.makedirs(base_logging_dir, exist_ok=True)
        logs_dir = f"{base_logging_dir}/{plan.resource.name}-{int(time.time())}.log"
        task_description = plan.task_description()
        task_description += (
            f"\n  > View detailed logs with: [bold]tail -f {logs_dir}[/bold]"
        )
        task = progress.add_task(task_description)
        launchflow_uri = LaunchFlowURI(
            project_name=plan.resource_manager.project_name,
            environment_name=plan.resource_manager.environment_name,
            resource_name=plan.resource_manager.resource_name,
        )

        updated_time = datetime.datetime.now(datetime.timezone.utc)
        created_time = (
            plan.existing_resource.created_at
            if plan.existing_resource
            else updated_time
        )
        status = ResourceStatus.CREATING
        if (
            plan.existing_resource is not None
            and plan.existing_resource.status != ResourceStatus.CREATE_FAILED
        ):
            status = ResourceStatus.UPDATING

        new_resource_state = ResourceState(
            name=plan.resource.name,
            product=plan.resource.product,
            cloud_provider=plan.resource.product.cloud_provider(),
            created_at=created_time,
            updated_at=updated_time,
            status=status,
            inputs=plan.resource.inputs(env_type).to_dict(),
            depends_on=[r.name for r in plan.resource.depends_on],
        )

        if is_local_resource(plan.resource):
            to_save = await _create_or_update_docker_resource(
                plan, new_resource_state, plan.operation_type, logs_dir
            )
        elif isinstance(plan.resource, Resource):
            to_save = await _create_or_update_tofu_resource(
                new_resource_state,
                plan,
                environment,
                launchflow_uri,
                lock_info,
                logs_dir,
            )
        else:
            raise NotImplementedError("Got an unknown resource type.")

        await plan.resource_manager.save_resource(to_save, lock_info.lock_id)
        if to_save.status == ResourceStatus.READY:
            progress.console.print(plan.success_message())
            if plan.resource._success_message:
                progress.console.print(f"  > {plan.resource._success_message}")
        else:
            progress.console.print(plan.failure_message())
        progress.console.print(f"  > View detailed logs at: [bold]{logs_dir}[/bold]")
        progress.remove_task(task)
        return to_save.status == ResourceStatus.READY


@dataclasses.dataclass
class _CreatePlanNode:
    lock: Lock
    plan: CreateResourcePlan
    child_plans: Dict[str, "_CreatePlanNode"] = dataclasses.field(default_factory=dict)
    parent_plans: Dict[str, "_CreatePlanNode"] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class _DestroyPlanNode:
    lock: Lock
    plan: DestroyResourcePlan
    child_plans: Dict[str, "DestroyResourcePlan"] = dataclasses.field(
        default_factory=dict
    )
    parent_plans: Dict[str, "DestroyResourcePlan"] = dataclasses.field(
        default_factory=dict
    )


async def _organize_create_plans(
    locked_plans: List[Tuple[Lock, CreateResourcePlan]], em: EnvironmentManager
):
    # Resources keys by the resource name they are operating on
    keyed_plans = {}
    for lock, plan in locked_plans:
        keyed_plans[plan.resource_manager.resource_name] = _CreatePlanNode(lock, plan)

    # Nodes that are the root of the plan tree (i.e. they have no parents)
    root_plan_nodes = []
    for plan_node in keyed_plans.values():
        if plan_node.plan.resource.depends_on:
            child_plans = {}
            valid_root = True
            for dep in plan_node.plan.resource.depends_on:
                dep_node = keyed_plans.get(dep.name)
                if dep_node is not None:
                    child_plans[dep_node.plan.resource_manager.resource_name] = (
                        plan_node
                    )
                    plan_node.parent_plans[dep.name] = dep_node
                else:
                    try:
                        # Attempt to load the parent resource if it wasn't in the plan
                        # to ensure that exists in a ready state
                        await em.create_resource_manager(dep.name).load_resource()
                    except exceptions.ResourceNotFound:
                        # If this happens we do not attempt to create the resource sincie
                        # it's parents are not part of the plan
                        rich.print(
                            f"[red]✗[/red] Dependency `{dep.__class__.__name__}({dep.name})` not found for `{plan_node.plan.resource.__class__.__name__}({plan_node.plan.resource.name})`"
                        )
                        await lock.release(lock.lock_info.lock_id)
                        child_plans = {}
                        valid_root = False
                        break
            if child_plans:
                # Only add the child plan to it's parents once we know all parents exist
                for key, plan in child_plans.items():
                    keyed_plans[key].child_plans[
                        plan.plan.resource_manager.resource_name
                    ] = plan
            elif valid_root:
                root_plan_nodes.append(plan_node)
        else:
            root_plan_nodes.append(plan_node)

    return root_plan_nodes


async def _organize_destroy_plans(locked_plans: List[Tuple[Lock, DestroyResourcePlan]]):
    # Resources keys by the resource name they are operating on
    keyed_plans: Dict[str, _DestroyPlanNode] = {}
    root_plan_nodes: Dict[str, _DestroyPlanNode] = {}
    for lock, plan in locked_plans:
        plan_node = _DestroyPlanNode(lock, plan)
        keyed_plans[plan.resource_manager.resource_name] = plan_node
        root_plan_nodes[plan.resource_manager.resource_name] = plan_node

    # Nodes that are the root of the plan tree (i.e. they have no children)
    for plan_node in keyed_plans.values():
        if plan_node.plan.resource.depends_on:
            for resource_name in plan_node.plan.resource.depends_on:
                child_plan = root_plan_nodes.get(resource_name, None)
                if child_plan is not None:
                    del root_plan_nodes[resource_name]
                    plan_node.child_plans[resource_name] = child_plan
                    child_plan.parent_plans[
                        plan_node.plan.resource_manager.resource_name
                    ] = plan_node
    return list(root_plan_nodes.values())


async def _lock_plan(plan: CreateResourcePlan) -> Lock:
    op_type = OperationType.CREATE_RESOURCE
    if plan.operation_type == "update":
        op_type = OperationType.UPDATE_RESOURCE
    elif plan.operation_type == "replace":
        op_type = OperationType.REPLACE_RESOURCE
    plan_output = io.StringIO()
    console = rich.console.Console(no_color=True, file=plan_output)
    plan.print_plan(console)
    plan_output.seek(0)
    lock = await plan.resource_manager.lock_resource(
        operation=LockOperation(
            operation_type=op_type, metadata={"plan": plan_output.read()}
        ),
    )
    try:
        existing_resource = await plan.resource_manager.load_resource()
    except exceptions.ResourceNotFound:
        existing_resource = None
    if plan.existing_resource != existing_resource:
        # If the resource has changed since planning we release the lock
        # and will not attempt to execute the plan
        rich.print(
            f"[red]✗ Resource `{plan.resource.__class__.__name__}({plan.resource.name})` state has changed since planning[/red]"
        )
        await lock.release(lock.lock_info.lock_id, reason=ReleaseReason.ABANDONED)
    else:
        return lock


async def create(
    environment_name: str,
    *resources: Tuple[Resource],
    launchflow_api_key: Optional[str] = None,
    prompt: bool = True,
):
    """
    Create resources in an environment.

    Args:
    - `environment_name`: The name of the environment to create resources in.
    - `resources`: A tuple of resources to create.
    - `prompt`: Whether to prompt the user before creating resources.
    """
    resources: List[Resource] = deduplicate_resources(resources)

    if (
        any(is_local_resource(resource) for resource in resources)
        and not docker_service_available()
    ):
        raise exceptions.MissingDockerDependency(
            "Docker is required to create local resources."
        )

    environment_manager = EnvironmentManager(
        project_name=config.launchflow_yaml.project,
        environment_name=environment_name,
        backend=config.launchflow_yaml.backend,
    )

    if launchflow_api_key is not None:
        # NOTE: This will throw an error if LaunchFlowBackend is not used
        environment_manager.set_launchflow_api_key(launchflow_api_key)

    # Stage 1: Build our plan
    resource_plans = await plan_resources(environment_manager, *resources)
    if not resource_plans:
        rich.print("No resources to create.")
        return True
    # Stage 2: Confirm the plan
    if not prompt:
        selected_plans = resource_plans
    else:
        selected_plans = await _confirm_plan(environment_manager, resource_plans)

    if not selected_plans:
        rich.print("No resources selected.")
        return True

    local_plans = [plan for plan in selected_plans if is_local_resource(plan.resource)]
    remote_plans = [
        plan for plan in selected_plans if not is_local_resource(plan.resource)
    ]

    # Stage 3: Execute plans
    # First we lock the environment to prevent the environment from being
    # modified while we are creating resources
    locked_plans: List[Tuple[Lock, CreateResourcePlan]] = [
        (await _lock_plan(plan), plan) for plan in local_plans
    ]
    environment = None
    # NOTE: we handle remote seperately from local here to avoid locking the environment
    # for local resources
    if remote_plans:
        async with environment_manager.lock_environment(
            operation=LockOperation(operation_type=OperationType.LOCK_ENVIRONMENT)
        ):
            # Next we lock all resources to prevent them from being modified
            # And verify that the resources are still in the same state as when we
            # planned them
            environment = await environment_manager.load_environment()
            for plan in remote_plans:
                locked_plans.append((await _lock_plan(plan), plan))

    organized_plans = await _organize_create_plans(locked_plans, environment_manager)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        results = []
        pending = set()
        plans_to_start: List[_CreatePlanNode] = organized_plans
        completed_plans: Dict[str, _CreatePlanNode] = {}

        while pending or plans_to_start:
            while plans_to_start:
                plan_node = plans_to_start.pop(0)

                async def execute_plan_wrapper(node):
                    result = await _execute_plan(node, environment, progress)
                    completed_plans[node.plan.resource_manager.resource_name] = node
                    # If this is a child plan make sure all of the parent plans
                    # have been completed before starting this plan
                    for child_plan in node.child_plans.values():
                        if all(
                            parent in completed_plans
                            for parent in child_plan.parent_plans.keys()
                        ):
                            plans_to_start.append(child_plan)
                    results.append((node, result))

                pending.add(asyncio.create_task(execute_plan_wrapper(plan_node)))

            _, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )
        successful_create_count = 0
        failed_create_count = 0
        successful_update_count = 0
        failed_update_count = 0
        successful_replace_count = 0
        failed_replace_count = 0
        for plan_node, result in results:
            if plan_node.plan.operation_type == "create":
                if result:
                    successful_create_count += 1
                else:
                    failed_create_count += 1
            elif plan_node.plan.operation_type == "update":
                if result:
                    successful_update_count += 1
                else:
                    failed_update_count += 1
            elif plan_node.plan.operation_type == "replace":
                if result:
                    successful_replace_count += 1
                else:
                    failed_replace_count += 1

        print()
        if successful_create_count:
            progress.console.print(
                f"[green]Successfully created {successful_create_count} resources[/green] "
            )
        if failed_create_count:
            progress.console.print(
                f"[red]Failed to create {failed_create_count} resources[/red] "
            )
        if successful_update_count:
            progress.console.print(
                f"[green]Successfully updated {successful_update_count} resources[/green] "
            )
        if failed_update_count:
            progress.console.print(
                f"[red]Failed to update {failed_update_count} resources[/red] "
            )
        if successful_replace_count:
            progress.console.print(
                f"[green]Successfully replaced {successful_replace_count} resources[/green] "
            )
        if failed_replace_count:
            progress.console.print(
                f"[red]Failed to replace {failed_replace_count} resources[/red] "
            )

        # Returns true if the command succeeded
        return (
            not failed_create_count
            and not failed_update_count
            and not failed_replace_count
        )


async def _destroy_resource(
    lock: Lock,
    plan: DestroyResourcePlan,
    environment: Optional[EnvironmentState],
    progress: Progress,
):
    async with lock as lock_info:
        resource_ref = f"Resource(name={plan.resource_manager.resource_name}, product={plan.resource.product.value})"
        base_logging_dir = "/tmp/launchflow"
        os.makedirs(base_logging_dir, exist_ok=True)
        logs_dir = f"{base_logging_dir}/{plan.resource.name}-{int(time.time())}.log"
        task_description = f"Destroying [blue]{resource_ref}[/blue]..."
        task_description += (
            f"\n  > View detailed logs with: [bold]tail -f {logs_dir}[/bold]"
        )
        task = progress.add_task(task_description)

        if plan.resource.product == ResourceProduct.LOCAL_DOCKER:
            # Get the connection info path, this will contain the running container id so we know which one to delete
            # This is hacky, but better than adding it to the flow-state if we're removing these docker types anyways
            backend = cast(LocalBackend, plan.resource_manager.backend)
            base_resource_path = os.path.join(
                backend.path,
                plan.resource_manager.project_name,
                plan.resource_manager.environment_name,
                "resources",
                plan.resource_manager.resource_name,
            )
            connection_info_path = os.path.join(
                base_resource_path, "connection_info.yaml"
            )

            with open(connection_info_path, "r") as file:
                data = yaml.safe_load(file)
                container_id = data.get("container_id", None)

                if container_id is None:
                    logging.warning(
                        "Didn't find a container to delete, clearing up flow state."
                    )

                    async def trivial(_):
                        pass

                    fn = trivial

                inputs = DestroyResourceDockerInputs(
                    container_id=container_id, logs_dir=logs_dir
                )

                fn = destroy_docker_resource
        else:
            # EnvironmentState is not none since we load it when destroying local resources
            environment = cast(EnvironmentState, environment)

            launchflow_uri = LaunchFlowURI(
                project_name=plan.resource_manager.project_name,
                environment_name=plan.resource_manager.environment_name,
                resource_name=plan.resource_manager.resource_name,
            )
            inputs = DestroyResourceTofuInputs(
                launchflow_uri=launchflow_uri,
                backend=plan.resource_manager.backend,
                lock_id=lock_info.lock_id,
                gcp_env_config=environment.gcp_config,
                aws_env_config=environment.aws_config,
                resource=plan.resource,
                logs_dir=logs_dir,
            )

            fn = delete_tofu_resource

        plan.resource.status = ResourceStatus.DELETING
        try:
            await fn(inputs)
            await plan.resource_manager.delete_resource(lock_info.lock_id)
            progress.remove_task(task)
            progress.console.print(
                f"[green]✓[/green] [blue]{resource_ref}[/blue] successfully deleted"
            )
        except Exception as e:
            # TODO: Log this to the logs_dir
            logging.error("Exception occurred: %s", e, exc_info=True)
            plan.resource.status = ResourceStatus.DELETE_FAILED
            progress.remove_task(task)
            progress.console.print(
                f"[red]✗[/red] [blue]{resource_ref}[/blue] failed to delete"
            )
            await plan.resource_manager.save_resource(plan.resource, lock_info.lock_id)

        progress.console.print(f"  > View detailed logs at: [bold]{logs_dir}[/bold]")


async def _destroy_service(lock: Lock, plan: DestroyServicePlan, progress: Progress):
    async with lock as lock_info:
        base_logging_dir = "/tmp/launchflow"
        os.makedirs(base_logging_dir, exist_ok=True)
        logs_dir = f"{base_logging_dir}/{plan.service_name}-{int(time.time())}.log"
        task_description = f"Destroying [blue]{plan.ref}[/blue]..."
        task_description += (
            f"\n  > View detailed logs with: [bold]tail -f {logs_dir}[/bold]"
        )
        task = progress.add_task(task_description)
        launchflow_uri = LaunchFlowURI(
            project_name=plan.service_manager.project_name,
            environment_name=plan.service_manager.environment_name,
            service_name=plan.service_manager.service_name,
        )

        plan.existing_service.status = ServiceStatus.DELETING
        try:
            if isinstance(plan, DestroyGCPServicePlan):
                await destroy_gcp_cloud_run_service(
                    DestroyGCPServiceInputs(
                        launchflow_uri=launchflow_uri,
                        backend=plan.service_manager.backend,
                        lock_id=lock_info.lock_id,
                        logs_dir=logs_dir,
                        gcp_project_id=plan.gcp_environment_config.project_id,
                    )
                )
            elif isinstance(plan, DestroyAWSServicePlan):
                await destroy_aws_ecs_fargate_service(
                    DestroyAWSServiceInputs(
                        launchflow_uri=launchflow_uri,
                        backend=plan.service_manager.backend,
                        lock_id=lock_info.lock_id,
                        logs_dir=logs_dir,
                        aws_region=plan.aws_environment_config.region,
                    )
                )
            else:
                raise NotImplementedError(
                    f"Service product {plan.existing_service.product} is not supported"
                )

            await plan.service_manager.delete_service(lock_info.lock_id)
            progress.console.print(
                f"[green]✓[/green] [blue]{plan.ref}[/blue] successfully deleted"
            )
        except Exception as e:
            # TODO: Log this to the logs_dir
            logging.error("Exception occurred: %s", e, exc_info=True)
            plan.existing_service.status = ServiceStatus.DELETE_FAILED
            progress.console.print(
                f"[red]✗[/red] [blue]{plan.ref}[/blue] failed to delete"
            )
            await plan.service_manager.save_service(
                plan.existing_service, lock_info.lock_id
            )

        progress.remove_task(task)
        progress.console.print(f"  > View detailed logs at: [bold]{logs_dir}[/bold]")


# TODO: Update workflow logging to use FlowLogger
async def destroy(
    environment_name: str,
    *nodes: Tuple[Node],
    local_only: bool = False,
    prompt: bool = True,
):
    """
    Destroy resources in an environment.

    Args:
    - `environment_name`: The name of the environment to destroy.
    - `nodes`: A tuple of nodes to destroy. If none are provided, all nodes will be destroyed.
    - `local_only`: Whether to destroy only local resources.
    - `prompt`: Whether to prompt the user before destroying resources.
    """

    environment_manager = EnvironmentManager(
        project_name=config.launchflow_yaml.project,
        environment_name=environment_name,
        backend=config.launchflow_yaml.backend,
    )

    # Stage 1. List all resources and services
    environment = None
    resources = await environment_manager.list_docker_resources()
    services = {}

    if resources and not docker_service_available():
        raise exceptions.MissingDockerDependency(
            "Docker is required to destroy local resources."
        )

    if not local_only:
        environment = await environment_manager.load_environment()
        remote_resources = await environment_manager.list_resources()
        remote_services = await environment_manager.list_services()
        # TODO: handle the case where local and remote resources share the same name
        resources.update(remote_resources)
        services.update(remote_services)

    # If nodes are provided, filter for them. If none are provided, we destroy everything
    if nodes:
        filtered_resources = {}
        filtered_services = {}
        loaded_resource_names = resources.keys()
        loaded_service_names = services.keys()
        for node in nodes:
            if isinstance(node, Resource):
                if is_local_resource(node) and not docker_service_available():
                    raise exceptions.MissingDockerDependency(
                        "Docker is required to destroy local resources."
                    )

                if node.name not in loaded_resource_names:
                    raise exceptions.ResourceNotFound(resource_name=node.name)
                filtered_resources[node.name] = resources[node.name]
            elif isinstance(node, Service):
                if node.name not in loaded_service_names:
                    raise exceptions.ServiceNotFound(service_name=node.name)
                filtered_services[node.name] = services[node.name]
        resources = filtered_resources
        services = filtered_services

    destroy_plans: List[DestroyResourcePlan] = []
    for name, resource in resources.items():
        if resource.product == ResourceProduct.LOCAL_DOCKER:
            resource_manager = environment_manager.create_docker_resource_manager(name)
        else:
            resource_manager = environment_manager.create_resource_manager(name)
        destroy_plans.append(
            DestroyResourcePlan(
                resource_name=name, resource=resource, resource_manager=resource_manager
            )
        )
    for name, service in services.items():
        service_manager = environment_manager.create_service_manager(name)
        if service.product == ServiceProduct.GCP_CLOUD_RUN:
            if environment.gcp_config is None:
                raise exceptions.GCPConfigNotFound(environment_manager=environment_name)
            destroy_plans.append(
                DestroyGCPServicePlan(
                    service_name=name,
                    service_manager=service_manager,
                    existing_service=service,
                    gcp_environment_config=environment.gcp_config,
                )
            )
        elif service.product == ServiceProduct.AWS_ECS_FARGATE:
            if environment.aws_config is None:
                raise exceptions.AWSConfigNotFound()
            destroy_plans.append(
                DestroyAWSServicePlan(
                    service_name=name,
                    service_manager=service_manager,
                    existing_service=service,
                    aws_environment_config=environment.aws_config,
                )
            )
        else:
            raise NotImplementedError(
                f"Service product {service.product} is not supported"
            )

    if not destroy_plans:
        rich.print("Nothing to delete in the environment. Exiting.")
        return
    # Stage 2. Confirm the deletions
    if not prompt:
        selected_plans = destroy_plans
    else:
        rich.print(
            f"Select the resources / services you want to delete in [bold yellow]`{environment_name}`[/bold yellow]."
        )
        selected_plans = beaupy.select_multiple(
            options=destroy_plans,
            preprocessor=lambda plan: plan.ref,
        )
        for plan in selected_plans:
            rich.print(f"[[pink1]✓[/pink1]] [pink1]{plan.ref}[/pink1]")
        print()
    if not selected_plans:
        rich.print("No resources / services selected. Exiting.")
        return

    service_plans_to_execute = []
    resource_plans_to_execute = []
    selected_remote_plans = []

    for plan in selected_plans:
        # Lock local resources withouth the environment
        # this prevents the need for credentials to the artifact
        # bucket if you are only destroying local resources
        if (
            isinstance(plan, DestroyResourcePlan)
            and plan.resource.product == ResourceProduct.LOCAL_DOCKER
        ):
            lock = await plan.resource_manager.lock_resource(
                operation=LockOperation(operation_type=OperationType.DESTROY_RESOURCE)
            )
            resource_plans_to_execute.append((lock, plan))
        else:
            selected_remote_plans.append(plan)
    if selected_remote_plans:
        async with environment_manager.lock_environment(
            operation=LockOperation(operation_type=OperationType.LOCK_ENVIRONMENT)
        ):
            for plan in selected_remote_plans:
                if isinstance(plan, DestroyServicePlan):
                    lock = await plan.service_manager.lock_service(
                        operation=LockOperation(
                            operation_type=OperationType.DESTROY_SERVICE
                        )
                    )
                    service_plans_to_execute.append((lock, plan))
                else:
                    lock = await plan.resource_manager.lock_resource(
                        operation=LockOperation(
                            operation_type=OperationType.DESTROY_RESOURCE
                        )
                    )
                    resource_plans_to_execute.append((lock, plan))

    organize_plans = await _organize_destroy_plans(resource_plans_to_execute)
    # Stage 3. Destroy the resources
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        pending = set()
        plans_to_start: List[_DestroyPlanNode] = organize_plans
        completed_plans: Dict[str, _DestroyPlanNode] = {}

        for lock, plan in service_plans_to_execute:
            pending.add(asyncio.create_task(_destroy_service(lock, plan, progress)))

        while pending or plans_to_start:
            while plans_to_start:
                plan_node = plans_to_start.pop(0)

                async def execute_plan_wrapper(node):
                    await _destroy_resource(node.lock, node.plan, environment, progress)
                    completed_plans[node.plan.resource_manager.resource_name] = node
                    for child_plan in node.child_plans.values():
                        if all(
                            parent in completed_plans
                            for parent in child_plan.parent_plans.keys()
                        ):
                            plans_to_start.append(child_plan)

                pending.add(asyncio.create_task(execute_plan_wrapper(plan_node)))

            _, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )


async def stop_local_containers(
    container_ids: List[str],
    prompt: bool = True,
):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(
            "Loading local resources",
        )
        containers = []
        if docker_service_available():
            _client = DockerClient()
            containers = [
                ContainerResource(_client.get_container(container_id))
                for container_id in container_ids
            ]
        to_stop_options = [
            container
            for container in containers
            if container.container.status == "running"
        ]
        progress.remove_task(task)

    to_stop = set()
    if not to_stop_options:
        progress.console.print(
            "[green]✓[/green] No containers to stop. No action required."
        )
        return
    if prompt:
        rich.print(
            "The following running local containers were found. Select which you would like to [bold]stop[/bold]:"
        )
        options = [
            f"[bold]Stop[/bold]: [bold]{container}[/bold]"
            for container in to_stop_options
        ]
        answers = beaupy.select_multiple(options, return_indices=True)
        for answer in answers:
            rich.print(f"[pink1]>[/pink1] Stop: [blue]{to_stop_options[answer]}[/blue]")
            to_stop.add(to_stop_options[answer])
        if not to_stop:
            rich.print("[green]✓[/green] No containers selected. No action required.")
            return
    else:
        for container in to_stop_options:
            to_stop.add(container)

    docker_client = None
    stop_queue = set()
    for container in to_stop:
        task = progress.add_task(f"Stopping [blue]{container}[/blue]...", total=1)

        if docker_client is None:
            docker_client = DockerClient()
        docker_client.stop_container(container.container.name)

        stop_queue.add((container, task))

    successes = 0
    failures = 0
    while stop_queue:
        await asyncio.sleep(0.5)

        while stop_queue:
            container, task = stop_queue.pop()
            try:
                container.container.reload()
                if container.container.status == "exited":
                    progress.console.print(
                        f"[green]✓[/green] Stop successful for [blue]{container}[/blue]"
                    )
                    successes += 1
            except Exception as e:
                progress.remove_task(task)
                progress.console.print(f"[red]✗[/red] Failed to stop {container}")
                progress.console.print(f"    └── {e}")
                failures += 1
            finally:
                progress.remove_task(task)

    if successes:
        progress.console.print(
            f"[green]✓[/green] Successfully stopped {successes} containers"
        )
    if failures:
        progress.console.print(f"[red]✗[/red] Failed to stop {failures} containers")


@dataclasses.dataclass
class ImportResourcePlan:
    resource: Resource
    resource_manager: ResourceManager


async def _run_import_plans(
    environment: EnvironmentState,
    plan: ImportResourcePlan,
    progress: Progress,
):
    base_logging_dir = "/tmp/launchflow"
    os.makedirs(base_logging_dir, exist_ok=True)
    logs_dir = f"{base_logging_dir}/{plan.resource.name}-{int(time.time())}.log"
    task_description = f"Importing [blue]{plan.resource.__class__.__name__}({plan.resource.name})[/blue]..."
    task_description += (
        f"\n  > View detailed logs with: [bold]tail -f {logs_dir}[/bold]"
    )
    task = progress.add_task(task_description)
    launchflow_uri = LaunchFlowURI(
        project_name=plan.resource_manager.project_name,
        environment_name=plan.resource_manager.environment_name,
        resource_name=plan.resource_manager.resource_name,
    )
    updated_time = datetime.datetime.now(datetime.timezone.utc)
    created_time = updated_time
    status = ResourceStatus.CREATING
    new_resource_state = ResourceState(
        name=plan.resource.name,
        product=plan.resource.product,
        cloud_provider=plan.resource.product.cloud_provider(),
        created_at=created_time,
        updated_at=updated_time,
        status=status,
        inputs=plan.resource.inputs(environment.environment_type).to_dict(),
        depends_on=[r.name for r in plan.resource.depends_on],
    )
    to_save = None
    try:
        imports = plan.resource.import_resource(environment)

        inputs = ImportResourceTofuInputs(
            launchflow_uri=launchflow_uri,
            backend=plan.resource_manager.backend,
            gcp_env_config=environment.gcp_config,
            aws_env_config=environment.aws_config,
            resource=new_resource_state,
            imports=imports,
            lock_id=None,
            logs_dir=logs_dir,
        )
        to_save = new_resource_state.model_copy()
        outputs = await import_tofu_resource(inputs)
        to_save.aws_arn = outputs.aws_arn
        to_save.gcp_id = outputs.gcp_id
        to_save.status = ResourceStatus.READY
        message = f"[green]✓[/green] Successfully imported [blue]{plan.resource.__class__.__name__}({plan.resource.name})[/blue]"
        await plan.resource_manager.save_resource(to_save, "TODO")

    except Exception as e:
        # TODO: Log this to the logs_dir
        logging.error("Exception occurred: %s", e, exc_info=True)
        # This can be none if we failed to call `import_resource`
        if to_save is not None:
            # Reset the create args to their original state
            to_save.inputs = None
            to_save.status = ResourceStatus.CREATE_FAILED
        message = f"[red]✗[/red] Failed to import [blue]{plan.resource.__class__.__name__}({plan.resource.name})[/blue]"
        message += f"\n  > {e}"
        # We delete the resource here since it failed to import
        await plan.resource_manager.delete_resource("TODO")

    progress.remove_task(task)
    message += f"\n  > View detailed logs at: [bold]{logs_dir}[/bold]"
    progress.console.print(message)


# TODO: add locks here
async def import_existing_resources(environment_name: str, *resources: Tuple[Resource]):
    resources: List[Resource] = deduplicate_resources(resources)

    environment_manager = EnvironmentManager(
        project_name=config.launchflow_yaml.project,
        environment_name=environment_name,
        backend=config.launchflow_yaml.backend,
    )
    environment = await environment_manager.load_environment()

    plans = []
    for resource in resources:
        rm = environment_manager.create_resource_manager(resource.name)
        try:
            _ = await rm.load_resource()
        except exceptions.ResourceNotFound:
            plans.append(ImportResourcePlan(resource=resource, resource_manager=rm))

    environment_ref = (
        f"{environment_manager.project_name}/{environment_manager.environment_name}"
    )
    rich.print(
        f"Select the resources you want to imports in [bold yellow]`{environment_ref}`[/bold yellow]:"
    )
    selected_plans: List[CreateResourcePlan] = beaupy.select_multiple(
        options=plans,
        preprocessor=lambda plan: f"[bold]Import[/bold] {plan.resource.__class__.__name__}({plan.resource.name})",
    )
    for plan in selected_plans:
        rich.print(
            f"[[pink1]✓[/pink1]] [pink1]{plan.resource.__class__.__name__}({plan.resource.name})[/pink1]"
        )

    tasks = []
    print()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        for plan in selected_plans:
            tasks.append(
                asyncio.create_task(_run_import_plans(environment, plan, progress))
            )
        await asyncio.gather(*tasks)
