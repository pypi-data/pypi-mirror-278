from launchflow.workflows.apply_resource_tofu.schemas import (
    ApplyResourceTofuInputs,
    ApplyResourceTofuOutputs,
)
from launchflow.workflows.commands.tf_commands import TFApplyCommand
from launchflow.workflows.utils import run_tofu


async def create_tofu_resource(inputs: ApplyResourceTofuInputs):
    state_prefix = inputs.launchflow_uri.tf_state_prefix(
        inputs.lock_id, module=inputs.resource.product.value
    )

    tf_vars = {}
    if inputs.gcp_env_config:
        tf_vars.update(
            {
                "gcp_project_id": inputs.gcp_env_config.project_id,
                "gcp_region": inputs.gcp_env_config.default_region,
                "resource_name": inputs.launchflow_uri.resource_name,
                "artifact_bucket": inputs.gcp_env_config.artifact_bucket,
                "environment_service_account_email": inputs.gcp_env_config.service_account_email,
                **inputs.resource.inputs,
            }
        )
    else:
        tf_vars.update(
            {
                "aws_region": inputs.aws_env_config.region,
                "resource_name": inputs.launchflow_uri.resource_name,
                "artifact_bucket": inputs.aws_env_config.artifact_bucket,
                "env_role_name": inputs.aws_env_config.iam_role_arn.split("/")[-1],
                "vpc_id": inputs.aws_env_config.vpc_id,
                "launchflow_environment": inputs.launchflow_uri.environment_name,
                "launchflow_project": inputs.launchflow_uri.project_name,
                **inputs.resource.inputs,
            }
        )

    tf_apply_command = TFApplyCommand(
        tf_module_dir=f"workflows/tf/resources/{inputs.resource.product.value}",
        backend=inputs.backend,
        tf_state_prefix=state_prefix,
        tf_vars=tf_vars,
        logging_dir=inputs.logs_dir,
    )

    output = await run_tofu(tf_apply_command)

    return ApplyResourceTofuOutputs(
        gcp_id=output.get("gcp_id"), aws_arn=output.get("aws_arn")
    )
