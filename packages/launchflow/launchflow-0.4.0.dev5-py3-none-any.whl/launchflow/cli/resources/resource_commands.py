import typer

from launchflow.cli.constants import ENVIRONMENT_HELP
from launchflow.cli.utils import print_response
from launchflow.cli.utyper import UTyper
from launchflow.config import config
from launchflow.flows.environments_flows import get_environment
from launchflow.managers.project_manager import ProjectManager

app = UTyper(help="Commands for viewing resources managed by LaunchFlow")


@app.command()
async def list(environment: str = typer.Argument(None, help=ENVIRONMENT_HELP)):
    """List all resources in a project/environment."""
    ps_manager = ProjectManager(
        backend=config.launchflow_yaml.backend, project_name=config.project
    )
    name, env = await get_environment(
        ps_manager,
        environment_name=environment,
        prompt_for_creation=False,
    )
    environment_manager = ps_manager.create_environment_manager(name)
    resources = await environment_manager.list_resources()
    print_response(
        "Resources",
        {
            name: resource.model_dump(
                mode="json", exclude_defaults=True, exclude_none=True
            )
            for name, resource in resources.items()
        },
    )
