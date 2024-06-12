from launchflow.workflows.commands.tf_commands import TFDestroyCommand
from launchflow.workflows.destroy_service.schemas import (
    DestroyAWSServiceInputs,
    DestroyGCPServiceInputs,
)
from launchflow.workflows.utils import run_tofu


async def destroy_gcp_cloud_run_service(inputs: DestroyGCPServiceInputs):
    # Step 1 - Destroy the tf that defines the service
    cloud_run_state_prefix = inputs.launchflow_uri.tf_state_prefix(
        inputs.lock_id, module="cloud_run_service"
    )
    tf_destroy_service_command = TFDestroyCommand(
        tf_module_dir="workflows/tf/empty/gcp_empty",
        backend=inputs.backend,
        tf_state_prefix=cloud_run_state_prefix,
        tf_vars={
            "gcp_project_id": inputs.gcp_project_id,
        },
        logging_dir=inputs.logs_dir,
    )
    await run_tofu(tf_destroy_service_command)

    # Step 2 - Destroy the tf that defines the docker repo
    ar_state_prefix = inputs.launchflow_uri.tf_state_prefix(
        inputs.lock_id, module="docker_artifact_registry"
    )
    tf_destroy_docker_repo_command = TFDestroyCommand(
        tf_module_dir="workflows/tf/empty/gcp_empty",
        backend=inputs.backend,
        tf_state_prefix=ar_state_prefix,
        tf_vars={
            "gcp_project_id": inputs.gcp_project_id,
        },
        logging_dir=inputs.logs_dir,
    )
    await run_tofu(tf_destroy_docker_repo_command)
    return


async def destroy_aws_ecs_fargate_service(inputs: DestroyAWSServiceInputs):
    # Step 1 - Destroy the tf that defines the service
    fargate_state_prefix = inputs.launchflow_uri.tf_state_prefix(
        inputs.lock_id, module="ecs_fargate_service"
    )
    tf_destroy_service_command = TFDestroyCommand(
        tf_module_dir="workflows/tf/empty/aws_empty",
        backend=inputs.backend,
        tf_state_prefix=fargate_state_prefix,
        tf_vars={
            "aws_region": inputs.aws_region,
        },
        logging_dir=inputs.logs_dir,
    )
    await run_tofu(tf_destroy_service_command)

    # Step 2 - Destroy the tf that defines the docker repo
    repo_state_prefix = inputs.launchflow_uri.tf_state_prefix(
        inputs.lock_id, module="aws_codebuild_and_ecr"
    )
    tf_destroy_docker_repo_command = TFDestroyCommand(
        tf_module_dir="workflows/tf/empty/aws_empty",
        backend=inputs.backend,
        tf_state_prefix=repo_state_prefix,
        tf_vars={
            "aws_region": inputs.aws_region,
        },
        logging_dir=inputs.logs_dir,
    )
    await run_tofu(tf_destroy_docker_repo_command)
    return
