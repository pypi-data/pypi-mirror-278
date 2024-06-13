from launchflow.workflows.commands.tf_commands import TFDestroyCommand
from launchflow.workflows.destroy_resource_tofu.schemas import DestroyResourceTofuInputs
from launchflow.workflows.utils import run_tofu


async def delete_tofu_resource(inputs: DestroyResourceTofuInputs):
    state_prefix = inputs.launchflow_uri.tf_state_prefix(
        inputs.lock_id, module=inputs.resource.product.value
    )

    tf_vars = {}
    if inputs.gcp_env_config:
        tf_vars["gcp_project_id"] = inputs.gcp_env_config.project_id
        module_dir = "workflows/tf/empty/gcp_empty"
    else:
        tf_vars["aws_region"] = inputs.aws_env_config.region
        module_dir = "workflows/tf/empty/aws_empty"

    tf_apply_command = TFDestroyCommand(
        tf_module_dir=module_dir,
        backend=inputs.backend,
        tf_state_prefix=state_prefix,
        tf_vars=tf_vars,
        logging_dir=inputs.logs_dir,
    )

    await run_tofu(tf_apply_command)
    return
