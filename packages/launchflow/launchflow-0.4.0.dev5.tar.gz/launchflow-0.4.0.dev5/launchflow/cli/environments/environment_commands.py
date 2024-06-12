import logging
from typing import Optional

import beaupy
import rich
import typer

from launchflow import exceptions
from launchflow.cli.utils import print_response
from launchflow.cli.utyper import UTyper
from launchflow.config import config
from launchflow.flows.environments_flows import create_environment, delete_environment
from launchflow.managers.environment_manager import EnvironmentManager
from launchflow.managers.project_manager import ProjectManager
from launchflow.models.enums import CloudProvider, EnvironmentType
from launchflow.validation import validate_environment_name

app = UTyper(help="Interact with your LaunchFlow environments.")


@app.command()
async def create(
    name: str = typer.Argument(None, help="The environment name."),
    env_type: Optional[EnvironmentType] = typer.Option(
        None, help="The environment type (`development` or `production`)."
    ),
    cloud_provider: Optional[CloudProvider] = typer.Option(
        None, help="The cloud provider."
    ),
    # GCP cloud provider options, this are used if you are importing an existing setup
    gcp_project_id: Optional[str] = typer.Option(
        None, help="The GCP project ID to import."
    ),
    gcs_artifact_bucket: Optional[str] = typer.Option(
        None, help="The GCS bucket to import.", hidden=True
    ),
    gcp_organization_name: Optional[str] = typer.Option(
        None,
        help="The GCP organization name (organization/XXXXXX) to place newly create GCP projects in. If not provided you will be prompted to select an organization.",
    ),
    environment_service_account_email: Optional[str] = typer.Option(
        None, help="The GCP service account email to import for the environment."
    ),
    auto_approve: bool = typer.Option(
        False, "--auto-approve", "-y", help="Auto approve environment creation."
    ),
):
    """Create a new environment in a LaunchFlow project."""
    if (
        gcp_project_id or gcs_artifact_bucket or environment_service_account_email
    ) and (cloud_provider != CloudProvider.GCP):
        rich.print(
            "[red]Error: GCP options can only be used with the GCP cloud provider. Add the `--cloud-provider=gcp` flag and try again.[/red]"
        )
        raise typer.Exit(1)
    if name is None and not auto_approve:
        name = beaupy.prompt("Enter the environment name:")
        rich.print(f"[pink1]>[/pink1] {name}")
    if name is None:
        typer.echo("Environment name is required.")
        raise typer.Exit(1)
    validate_environment_name(name)
    environment_manager = EnvironmentManager(
        project_name=config.launchflow_yaml.project,
        environment_name=name,
        backend=config.launchflow_yaml.backend,
    )
    try:
        environment = await create_environment(
            env_type,
            cloud_provider=cloud_provider,
            manager=environment_manager,
            gcp_project_id=gcp_project_id,
            gcs_artifact_bucket=gcs_artifact_bucket,
            gcp_organization_name=gcp_organization_name,
            environment_service_account_email=environment_service_account_email,
            prompt=not auto_approve,
        )
    except Exception as e:
        logging.debug("Exception occurred: %s", e, exc_info=True)
        rich.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    if environment is not None:
        print_response(
            "Environment",
            environment.model_dump(
                mode="json", exclude_defaults=True, exclude_none=True
            ),
        )


@app.command()
async def list():
    """List all environments in a LaunchFlow project."""
    manager = ProjectManager(
        project_name=config.project,
        backend=config.launchflow_yaml.backend,
    )
    try:
        envs = await manager.list_environments()
    except Exception as e:
        logging.debug("Exception occurred: %s", e, exc_info=True)
        rich.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    print_response(
        "Environments",
        {
            name: env.model_dump(mode="json", exclude_defaults=True, exclude_none=True)
            for name, env in envs.items()
        },
    )


@app.command()
async def get(
    name: str = typer.Argument(..., help="The environment name."),
):
    """Get information about a specific environment."""
    environment_manager = EnvironmentManager(
        project_name=config.launchflow_yaml.project,
        environment_name=name,
        backend=config.launchflow_yaml.backend,
    )
    try:
        env = await environment_manager.load_environment()
    except Exception as e:
        logging.debug("Exception occurred: %s", e, exc_info=True)
        rich.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    print_response(
        "Environment",
        env.model_dump(mode="json", exclude_defaults=True, exclude_none=True),
    )


@app.command()
async def delete(
    name: str = typer.Argument(..., help="The environment name."),
    detach: bool = typer.Option(
        False,
        help="If true we will not clean up any of the cloud resources associated with the environment and will simply delete the record from LaunchFlow.",
    ),
    auto_approve: bool = typer.Option(
        False, "--auto-approve", "-y", help="Auto approve environment deletion."
    ),
):
    """Delete an environment."""
    if name is None:
        name = beaupy.prompt("Enter the environment name:")
        rich.print(f"[pink1]>[/pink1] {name}")
    environment_manager = EnvironmentManager(
        project_name=config.launchflow_yaml.project,
        environment_name=name,
        backend=config.launchflow_yaml.backend,
    )
    try:
        await environment_manager.load_environment()
    except exceptions.EnvironmentNotFound:
        rich.print(f"[red]Environment '{name}' not found.[/red]")
        raise typer.Exit(1)
    try:
        await delete_environment(
            manager=environment_manager, detach=detach, prompt=not auto_approve
        )
    except Exception as e:
        logging.exception("Exception occurred: %s", e)
        logging.debug("Exception occurred: %s", e, exc_info=True)
        rich.print(f"[red]{e}[/red]")
        raise typer.Exit(1)
