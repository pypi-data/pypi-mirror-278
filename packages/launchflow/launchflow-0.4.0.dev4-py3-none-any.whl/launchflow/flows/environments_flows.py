import datetime
import logging
from typing import Optional, Tuple

import beaupy
import rich
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from launchflow import exceptions
from launchflow.clients.response_schemas import EnvironmentType
from launchflow.locks import LockOperation, OperationType
from launchflow.managers.environment_manager import EnvironmentManager
from launchflow.managers.project_manager import ProjectManager
from launchflow.models.enums import CloudProvider, EnvironmentStatus
from launchflow.models.flow_state import (
    AWSEnvironmentConfig,
    EnvironmentState,
    GCPEnvironmentConfig,
)
from launchflow.models.launchflow_uri import LaunchFlowURI
from launchflow.validation import validate_environment_name
from launchflow.workflows import (
    AWSEnvironmentCreationInputs,
    AWSEnvironmentDeletionInputs,
    GCPEnvironmentCreationInputs,
    GCPEnvironmentDeletionInputs,
    create_aws_environment,
    create_gcp_environment,
    delete_aws_environment,
    delete_gcp_environment,
)


async def get_environment(
    project_state_manager: ProjectManager,
    environment_name: Optional[str] = None,
    prompt_for_creation: bool = True,
) -> Tuple[str, EnvironmentState]:
    if environment_name is None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Fetching environments...", total=None)
            environments = await project_state_manager.list_environments()
            progress.remove_task(task)
        environment_names = [f"{name}" for name in environments.keys()]
        if prompt_for_creation:
            environment_names.append("[i yellow]Create new environment[/i yellow]")
        print("Select the environment to use:")
        selected_environment = beaupy.select(environment_names, strict=True)
        if selected_environment is None:
            rich.print("[red]No environment selected.")
            raise typer.Exit(1)
        if prompt_for_creation and selected_environment == environment_names[-1]:
            if environment_name is None:
                environment_name = beaupy.prompt("Enter the environment name:")
                rich.print(f"[pink1]>[/pink1] {environment_name}")
            validate_environment_name(environment_name)
            environment = await create_environment(
                environment_type=None,
                cloud_provider=None,
                manager=EnvironmentManager(
                    project_name=project_state_manager.project_name,
                    environment_name=environment_name,
                    backend=project_state_manager.backend,
                ),
            )
        else:
            rich.print(f"[pink1]>[/pink1] {selected_environment}")
            print()
            environment = environments[selected_environment]
            environment_name = selected_environment
        return environment_name, environment
    try:
        # Fetch the environment to ensure it exists
        env_manager = EnvironmentManager(
            project_name=project_state_manager.project_name,
            environment_name=environment_name,
            backend=project_state_manager.backend,
        )
        environment = await env_manager.load_environment()
    except exceptions.EnvironmentNotFound as e:
        if prompt_for_creation:
            answer = beaupy.confirm(
                f"Environment `{environment_name}` does not exist yet. Would you like to create it?"
            )
            if answer:
                environment = await create_environment(
                    environment_type=None,
                    cloud_provider=None,
                    manager=EnvironmentManager(
                        project_name=project_state_manager.project_name,
                        environment_name=environment_name,
                        backend=project_state_manager.backend,
                    ),
                )
            else:
                raise e
        else:
            raise e
    return environment_name, environment


async def delete_environment(
    manager: EnvironmentManager, detach: bool = False, prompt: bool = True
):
    if prompt:
        user_confirmation = beaupy.confirm(
            f"Would you like to delete the environment `{manager.environment_name}`?",
        )
        if not user_confirmation:
            rich.print("[red]✗[/red] Environment deletion cancelled.")
            return

    launchflow_uri = LaunchFlowURI(
        environment_name=manager.environment_name, project_name=manager.project_name
    )
    async with manager.lock_environment(
        operation=LockOperation(operation_type=OperationType.DELETE_ENVIRONMENT)
    ) as lock:
        existing_environment = await manager.load_environment()
        existing_resources = await manager.list_resources()
        existing_services = await manager.list_services()
        if existing_resources or existing_services:
            raise exceptions.EnvironmentNotEmpty(manager.environment_name)
        if not detach:
            try:
                if existing_environment.gcp_config is not None:
                    await delete_gcp_environment(
                        inputs=GCPEnvironmentDeletionInputs(
                            launchflow_uri=launchflow_uri,
                            environment=existing_environment,
                        )
                    )
                elif existing_environment.aws_config is not None:
                    await delete_aws_environment(
                        inputs=AWSEnvironmentDeletionInputs(
                            launchflow_uri=launchflow_uri,
                            aws_region=existing_environment.aws_config.region,
                            artifact_bucket=existing_environment.aws_config.artifact_bucket,
                            lock_id=lock.lock_id,
                        )
                    )
            except Exception as e:
                logging.debug("Exception occurred: %s", e, exc_info=True)
                existing_environment.status = EnvironmentStatus.DELETE_FAILED
                await manager.save_environment(existing_environment, lock.lock_id)
                raise e
        await manager.delete_environment(lock.lock_id)
        rich.print("[green]✓[/green] Environment deleted.")


async def lookup_organization(prompt: bool = True):
    try:
        from google.cloud import resourcemanager_v3
    except ImportError:
        raise exceptions.MissingGCPDependency()
    organization_client = resourcemanager_v3.OrganizationsAsyncClient()

    orgs = await organization_client.search_organizations()
    org: resourcemanager_v3.Organization = None
    # 1. look up organiztaion for the project
    # We do this first to ensure it won't fail before creating the project
    all_orgs = []
    async for o in orgs:
        all_orgs.append(o)
    if not all_orgs:
        raise exceptions.NoOrgs()
    if len(all_orgs) > 1:
        if not prompt:
            raise ValueError(
                "Multiple organizations found. Please provide one with the --gcp-org flag or run interactively."
            )
        print(
            "You have access to multiple organizations. Please select which one to use:"
        )
        org_options = [f"{o.display_name} ({o.name})" for o in all_orgs]
        org_idx = beaupy.select(org_options, return_index=True, strict=True)
        if org_idx is None:
            raise ValueError("No org selected")
        org = all_orgs[org_idx]
        rich.print(f"[pink1]>[/pink1] {org_options[org_idx]}")
        print()

    else:
        org = all_orgs[0]
    return org.name


async def create_environment(
    environment_type: Optional[EnvironmentType],
    cloud_provider: Optional[CloudProvider],
    manager: EnvironmentManager,
    # GCP cloud provider options, this are used if you are importing an existing setup
    gcp_project_id: Optional[str] = None,
    gcs_artifact_bucket: Optional[str] = None,
    gcp_organization_name: Optional[str] = None,
    environment_service_account_email: Optional[str] = None,
    prompt: bool = True,
) -> Optional[EnvironmentState]:
    """Create a new environment in a project."""
    async with manager.lock_environment(
        operation=LockOperation(operation_type=OperationType.CREATE_ENVIRONMENT)
    ) as lock:
        # TODO: maybe prompt the user if the environment already exists that this will update stuff
        try:
            existing_environment = await manager.load_environment()
        except exceptions.EnvironmentNotFound:
            existing_environment = None
        if existing_environment is not None:
            existing_environment_type = existing_environment.environment_type
            if (
                environment_type is not None
                and environment_type != existing_environment_type
            ):
                raise exceptions.ExistingEnvironmentDifferentEnvironmentType(
                    manager.environment_name, existing_environment_type
                )
            environment_type = existing_environment_type

            existing_cloud_provider = None
            if existing_environment.aws_config is not None:
                existing_cloud_provider = CloudProvider.AWS
            elif existing_environment.gcp_config is not None:
                existing_cloud_provider = CloudProvider.GCP
            else:
                raise ValueError("Environment has no cloud provider.")
            if cloud_provider is not None and cloud_provider != existing_cloud_provider:
                raise exceptions.ExistingEnvironmentDifferentCloudProvider(
                    manager.environment_name
                )

            cloud_provider = existing_cloud_provider

            # TODO: add tests for these exceptions being thrown
            if existing_environment.gcp_config is not None:
                if (
                    gcp_project_id is not None
                    and existing_environment.gcp_config.project_id is not None
                    and gcp_project_id != existing_environment.gcp_config.project_id
                ):
                    raise exceptions.ExistingEnvironmentDifferentGCPProject(
                        manager.environment_name,
                        existing_environment.gcp_config.project_id,
                    )
                gcp_project_id = (
                    existing_environment.gcp_config.project_id or gcp_project_id
                )
                if (
                    gcs_artifact_bucket is not None
                    and existing_environment.gcp_config.artifact_bucket is not None
                    and gcs_artifact_bucket
                    != existing_environment.gcp_config.artifact_bucket
                ):
                    raise exceptions.ExistingEnvironmentDifferentGCPBucket(
                        manager.environment_name,
                        existing_environment.gcp_config.artifact_bucket,
                    )
                gcs_artifact_bucket = (
                    existing_environment.gcp_config.artifact_bucket
                    or gcs_artifact_bucket
                )
                if (
                    environment_service_account_email is not None
                    and existing_environment.gcp_config.service_account_email
                    is not None
                    and environment_service_account_email
                    != existing_environment.gcp_config.service_account_email
                ):
                    raise exceptions.ExistingEnvironmentDifferentGCPServiceAccount(
                        manager.environment_name,
                        existing_environment.gcp_config.service_account_email,
                    )
                environment_service_account_email = (
                    existing_environment.gcp_config.service_account_email
                    or environment_service_account_email
                )

        if environment_type is None and prompt:
            print("Select the environment type:")
            selection = beaupy.select(
                ["development", "production"],
                strict=True,
            )
            rich.print(f"[pink1]>[/pink1] {selection}")
            environment_type = EnvironmentType(selection)
            print()

        # TODO: move this logic into an EnvironmentPlan step
        if cloud_provider is None and prompt:
            print("Select the cloud provider for the environment:")
            selection = beaupy.select(["GCP", "AWS"], strict=True)
            rich.print(f"[pink1]>[/pink1] {selection}")
            cloud_provider = CloudProvider[selection]
            print()

        if cloud_provider is None:
            raise ValueError("Cloud provider is required.")

        if environment_type is None:
            raise ValueError("Environment type is required.")

        launchflow_uri = LaunchFlowURI(
            environment_name=manager.environment_name,
            project_name=manager.project_name,
        )
        if cloud_provider == CloudProvider.GCP:
            org_name = gcp_organization_name
            if gcp_project_id is None and org_name is None:
                org_name = await lookup_organization(prompt)
            gcp_environment_info = await create_gcp_environment(
                inputs=GCPEnvironmentCreationInputs(
                    launchflow_uri=launchflow_uri,
                    gcp_project_id=gcp_project_id,
                    environment_service_account_email=environment_service_account_email,
                    artifact_bucket=gcs_artifact_bucket,
                    org_name=org_name,
                    lock_id=lock.lock_id,
                ),
            )
            create_time = datetime.datetime.now(datetime.timezone.utc)
            status = (
                EnvironmentStatus.READY
                if gcp_environment_info.success
                else EnvironmentStatus.CREATE_FAILED
            )
            env = EnvironmentState(
                created_at=create_time,
                updated_at=create_time,
                gcp_config=GCPEnvironmentConfig(
                    project_id=gcp_environment_info.gcp_project_id,
                    default_region="us-central1",
                    default_zone="us-central1-a",
                    service_account_email=gcp_environment_info.environment_service_account_email,
                    artifact_bucket=gcp_environment_info.artifact_bucket,
                ),
                environment_type=environment_type,
                status=status,
            )
        elif cloud_provider == CloudProvider.AWS:
            if existing_environment is not None:
                aws_account_id = existing_environment.aws_config.account_id
                region = existing_environment.aws_config.region
            else:
                try:
                    import boto3
                    import botocore
                except ImportError:
                    raise exceptions.MissingAWSDependency()
                sts = boto3.client("sts")
                try:
                    response = sts.get_caller_identity()
                    aws_account_id = response["Account"]
                except botocore.exceptions.NoCredentialsError as e:
                    raise exceptions.NoAWSCredentialsFound() from e

                if prompt:
                    # TODO: Explore the idea of an "EnvironmentPlan" and move this prompt into the plan step
                    answer = beaupy.confirm(
                        f"Based on your credentials this will create an environment in AWS account {aws_account_id}. Would you like to continue?"
                    )
                    if not answer:
                        typer.echo("AWS account ID rejected.")
                        typer.exit(1)

                # TODO: make this configurable
                region = "us-east-1"
            aws_environment_info = await create_aws_environment(
                inputs=AWSEnvironmentCreationInputs(
                    launchflow_uri=launchflow_uri,
                    region=region,
                    aws_account_id=aws_account_id,
                    environment_type=environment_type,
                    artifact_bucket=(
                        existing_environment.aws_config.artifact_bucket
                        if existing_environment
                        else None
                    ),
                    lock_id=lock.lock_id,
                )
            )
            create_time = datetime.datetime.now(datetime.timezone.utc)
            status = (
                EnvironmentStatus.READY
                if aws_environment_info.success
                else EnvironmentStatus.CREATE_FAILED
            )
            env = EnvironmentState(
                created_at=create_time,
                updated_at=create_time,
                aws_config=AWSEnvironmentConfig(
                    artifact_bucket=aws_environment_info.artifact_bucket,
                    vpc_id=aws_environment_info.vpc_id,
                    iam_role_arn=aws_environment_info.role_arn,
                    ecs_cluster_name=aws_environment_info.ecs_cluster_name,
                    region=region,
                    account_id=aws_account_id,
                ),
                environment_type=environment_type,
                status=status,
            )
        else:
            raise ValueError("Invalid cloud provider.")
        await manager.save_environment(env, lock.lock_id)

        if env.status == EnvironmentStatus.READY:
            rich.print("[green]Environment created successfully![/green]")
            return env
        else:
            rich.print("[red]✗ Failed to create environment.[/red]")
