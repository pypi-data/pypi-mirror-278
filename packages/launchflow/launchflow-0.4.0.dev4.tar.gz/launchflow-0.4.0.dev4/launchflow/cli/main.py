import asyncio
import logging
import os
from typing import List, Optional

import beaupy
import fsspec
import rich
import typer
import uvloop
from rich.progress import Progress, SpinnerColumn, TextColumn

import launchflow
from launchflow import exceptions
from launchflow.cache.launchflow_tmp import (
    build_cache_key,
    encode_resource_outputs_cache,
)
from launchflow.cli import project_gen
from launchflow.cli.accounts import account_commands
from launchflow.cli.ast_search import find_launchflow_resources
from launchflow.cli.config import config_commands
from launchflow.cli.constants import (
    API_KEY_HELP,
    ENVIRONMENT_HELP,
    SCAN_DIRECTORY_HELP,
    SERVICE_HELP,
)
from launchflow.cli.environments import environment_commands
from launchflow.cli.gen.templates.django.django_template import DjangoProjectGenerator
from launchflow.cli.gen.templates.fastapi.fastapi_template import (
    FastAPIProjectGenerator,
)
from launchflow.cli.gen.templates.flask.flask_template import FlaskProjectGenerator
from launchflow.cli.project import project_commands
from launchflow.cli.resources import resource_commands
from launchflow.cli.secrets import secret_commands
from launchflow.cli.service_utils import (
    import_services_from_config,
    import_services_from_directory,
)
from launchflow.cli.services import service_commands
from launchflow.cli.utils import print_response
from launchflow.cli.utyper import UTyper
from launchflow.clients import async_launchflow_client_ctx
from launchflow.config import config
from launchflow.dependencies.opentofu import install_opentofu, needs_opentofu
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.flows.account_id import get_account_id_from_config
from launchflow.flows.auth import login_flow, logout_flow
from launchflow.flows.cloud_provider import CloudProvider
from launchflow.flows.cloud_provider import connect as connect_provider
from launchflow.flows.environments_flows import get_environment
from launchflow.flows.resource_flows import create as create_resources
from launchflow.flows.resource_flows import destroy as destroy_resources
from launchflow.flows.resource_flows import (
    import_existing_resources,
    import_resources,
    is_local_resource,
)
from launchflow.flows.service_flows import deploy as deploy_services
from launchflow.flows.service_flows import promote as promote_services
from launchflow.managers.project_manager import ProjectManager

app = UTyper(help="LaunchFlow CLI.", no_args_is_help=True)
app.add_typer(account_commands.app, name="accounts")
app.add_typer(project_commands.app, name="projects")
app.add_typer(environment_commands.app, name="environments")
app.add_typer(resource_commands.app, name="resources")
app.add_typer(service_commands.app, name="services")
app.add_typer(config_commands.app, name="config")
app.add_typer(secret_commands.app, name="secrets")


@app.callback()
def cli_setup(log_level: Optional[str] = None):
    if log_level is not None:
        logging.basicConfig(level=log_level)
    if needs_opentofu():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Installing dependencies...", total=1)
            install_opentofu()
            rich.print("[green]✓[/green] Dependencies installed.")
            progress.remove_task(task)


def _set_global_project_and_environment(
    project: Optional[str], environment: Optional[str]
):
    if project is not None:
        launchflow.project = project
    else:
        launchflow.project = config.project
    if environment is not None:
        launchflow.environment = environment
    else:
        launchflow.environment = config.environment


@app.command()
async def init(
    directory: str = typer.Argument(None, help="Directory to initialize launchflow."),
    account_id: str = typer.Option(
        None,
        help="Account ID to use for this project. Defaults to the account ID set in the config.",
    ),
):
    """Initialize a new launchflow project."""
    async with async_launchflow_client_ctx() as client:
        try:
            project = await project_gen.project(client, account_id)

            if "aws" in project.configured_cloud_providers:
                cloud_provider = "aws"
            elif "gcp" in project.configured_cloud_providers:
                cloud_provider = "gcp"
            else:
                raise NotImplementedError(
                    f"Cloud provider {project.configured_cloud_providers} is not supported yet."
                )

            environment = await get_environment(
                client=client,
                project=project,
                environment_name=None,
                prompt_for_creation=True,
            )
        except Exception as e:
            typer.echo(e)
            raise typer.Exit(1)

        if not directory:
            relative_path = project.name
            full_directory_path = os.path.join(os.path.abspath("."), relative_path)
        else:
            relative_path = directory
            full_directory_path = os.path.abspath(relative_path)
        while os.path.exists(full_directory_path):
            typer.echo(f"Directory `{full_directory_path}` already exists.")
            directory_name = beaupy.prompt("Enter a directory name for your project:")
            full_directory_path = os.path.join(
                os.path.abspath(directory), directory_name
            )

        framework = project_gen.framework(cloud_provider)
        resources = project_gen.resources(cloud_provider)

        if framework == project_gen.Framework.FASTAPI:
            generator = FastAPIProjectGenerator(
                resources=resources,
                cloud_provider=cloud_provider,
                launchflow_project_name=project.name,
                launchflow_environment_name=environment.name,
            )
            generator.generate_project(full_directory_path)
        elif framework == project_gen.Framework.FLASK:
            generator = FlaskProjectGenerator(
                resources=resources,
                cloud_provider=cloud_provider,
                launchflow_project_name=project.name,
                launchflow_environment_name=environment.name,
            )
            generator.generate_project(full_directory_path)
        elif framework == project_gen.Framework.DJANGO:
            generator = DjangoProjectGenerator(
                resources=resources,
                cloud_provider=cloud_provider,
                launchflow_project_name=project.name,
                launchflow_environment_name=environment.name,
            )
            generator.generate_project(full_directory_path)
        else:
            raise NotImplementedError(f"Framework {framework} is not supported yet.")

        print()
        print("Done!")
        print()
        print("Navigate to your project directory:")
        rich.print(f"  $ [green]cd {relative_path}")
        print()
        print("To create your resources run:")
        rich.print("  $ [green]launchflow create")
        print()
        print("To build and deploy your app remotely run:")
        rich.print("  $ [green]launchflow deploy")


async def _create_resources(
    resource_ref: Optional[str],
    environment: Optional[str],
    launchflow_api_key: Optional[str],
    scan_directory: str,
    auto_approve: bool,
    local_only: bool,
    remote_only: bool,
):
    if local_only and remote_only:
        typer.echo("Internal error: local_only and remote_only cannot both be true.")
        raise typer.Exit(1)

    if resource_ref is None:
        resource_refs = find_launchflow_resources(scan_directory)
    else:
        resource_refs = [resource_ref]

    resources = import_resources(resource_refs)

    if local_only:
        resources = [resource for resource in resources if is_local_resource(resource)]
    elif remote_only:
        resources = [
            resource for resource in resources if not is_local_resource(resource)
        ]

    try:
        success = await create_resources(
            environment,
            *resources,
            launchflow_api_key=launchflow_api_key,
            prompt=not auto_approve,
        )
        if not success:
            raise typer.Exit(1)
        print()

    except LaunchFlowRequestFailure as e:
        logging.debug("Exception occurred: %s", e, exc_info=True)
        e.pretty_print()
        raise typer.Exit(1)


@app.command()
async def create(
    environment: Optional[str] = typer.Argument(None, help=ENVIRONMENT_HELP),
    resource: Optional[str] = typer.Option(
        None,
        help="Resource to create. If none we will scan the directory for available resources.",
    ),
    scan_directory: str = typer.Option(".", help=SCAN_DIRECTORY_HELP),
    auto_approve: bool = typer.Option(
        False, "--auto-approve", "-y", help="Auto approve resource creation."
    ),
    local_only: bool = typer.Option(
        False, "--local", help="Create only local resources."
    ),
    launchflow_api_key: Optional[str] = typer.Option(None, help=API_KEY_HELP),
):
    """Create any resources that are not already created."""
    if launchflow.config.launchflow_yaml is None:
        raise exceptions.LaunchFlowYamlNotFound()
    # NOTE: this needs to be before we import the resources
    if environment is None:
        environment, _ = await get_environment(
            project_state_manager=ProjectManager(
                backend=config.launchflow_yaml.backend,
                project_name=config.project,
            ),
            environment_name=environment,
            prompt_for_creation=True,
        )
    _set_global_project_and_environment(None, environment)

    await _create_resources(
        resource_ref=resource,
        environment=environment,
        launchflow_api_key=launchflow_api_key,
        scan_directory=scan_directory,
        auto_approve=auto_approve,
        local_only=local_only,
        remote_only=False,
    )


# TODO add resource filter
@app.command()
async def destroy(
    environment: Optional[str] = typer.Argument(None, help=ENVIRONMENT_HELP),
    local_only: bool = typer.Option(
        False, "--local", help="Only destroy local resources."
    ),
    auto_approve: bool = typer.Option(
        False, "--auto-approve", "-y", help="Auto approve resource destruction."
    ),
):
    """Destroy all resources in the project / environment."""
    if launchflow.config.launchflow_yaml is None:
        raise exceptions.LaunchFlowYamlNotFound()
    # NOTE: this needs to be before we import the resources
    if environment is None:
        environment, _ = await get_environment(
            project_state_manager=ProjectManager(
                backend=config.launchflow_yaml.backend,
                project_name=config.project,
            ),
            environment_name=environment,
            prompt_for_creation=False,
        )
    _set_global_project_and_environment(None, environment)

    try:
        await destroy_resources(
            environment, local_only=local_only, prompt=not auto_approve
        )
    except LaunchFlowRequestFailure as e:
        logging.debug("Exception occurred: %s", e, exc_info=True)
        e.pretty_print()
        raise typer.Exit(1)


@app.command(hidden=True)
async def deploy(
    environment: Optional[str] = typer.Argument(None, help=ENVIRONMENT_HELP),
    service: Optional[str] = typer.Option(None, help=SERVICE_HELP),
    auto_approve: bool = typer.Option(
        False, "--auto-approve", "-y", help="Auto approve the deployment."
    ),
    launchflow_api_key: Optional[str] = typer.Option(None, help=API_KEY_HELP),
    scan_directory: str = typer.Option(".", help=SCAN_DIRECTORY_HELP),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Verbose output. Will include all options provided to your service.",
    ),
    build_local: bool = typer.Option(
        False,
        "--build-local",
        help="Build the Docker image locally.",
    ),
    skip_create: bool = typer.Option(
        False,
        "--skip-create",
        help="Skip the Resource creation step.",
    ),
):
    """Deploy a service to a project / environment."""
    if environment is None:
        environment, _ = await get_environment(
            project_state_manager=ProjectManager(
                backend=config.launchflow_yaml.backend,
                project_name=config.project,
            ),
            environment_name=environment,
            prompt_for_creation=True,
        )
    _set_global_project_and_environment(None, environment)

    if not skip_create:
        await _create_resources(
            resource_ref=None,
            environment=environment,
            launchflow_api_key=launchflow_api_key,
            scan_directory=scan_directory,
            auto_approve=auto_approve,
            local_only=False,
            remote_only=True,
        )

    # Load services defined in launchflow.yaml
    services = import_services_from_config(service, environment)
    # Load services defined in code
    code_services = import_services_from_directory(scan_directory)

    # Merges and resolves any conflicts between the services defined in launchflow.yaml and the services defined in code
    service_names = set()
    for found_service in code_services:
        if found_service.name in service_names:
            typer.echo(
                f"Service `{found_service.name}` is configured in launchflow.yaml and your code. Services may only be specified in code or in launchflow.yaml, not both."
            )
            raise typer.Exit(1)
        if service is not None and found_service.name != service:
            continue
        services.append(found_service)

    if not services:
        typer.echo("No services found.")
        raise typer.Exit(1)

    await deploy_services(
        *services,
        environment=environment,
        launchflow_api_key=launchflow_api_key,
        prompt=not auto_approve,
        verbose=verbose,
        build_local=build_local,
    )


@app.command(hidden=True)
async def promote(
    from_environment: str = typer.Argument(
        ..., help="The environment to promote from."
    ),
    to_environment: str = typer.Argument(..., help="The environment to promote to"),
    service: Optional[str] = typer.Option(None, help=SERVICE_HELP),
    auto_approve: bool = typer.Option(
        False, "--auto-approve", "-y", help="Auto approve the deployment."
    ),
    launchflow_api_key: Optional[str] = typer.Option(None, help=API_KEY_HELP),
    scan_directory: str = typer.Option(".", help=SCAN_DIRECTORY_HELP),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Verbose output. Will include all options provided to your service.",
    ),
    # NOTE: these options are here to make it easier to test the github integration
    launch_service_address: Optional[str] = typer.Option(None, hidden=True),
    account_service_address: Optional[str] = typer.Option(None, hidden=True),
):
    """Promote a service. This will take the image that is running in `from_environment` and promote it to a service in `to_environment`."""
    if launch_service_address is not None:
        config.settings.launch_service_address = launch_service_address
        config.settings.account_service_address = account_service_address

    # Load services defined in launchflow.yaml
    services = import_services_from_config(service, to_environment)
    # Load services defined in code
    code_services = import_services_from_directory(scan_directory)

    # Merges and resolves any conflicts between the services defined in launchflow.yaml and the services defined in code
    service_names = set()
    for found_service in code_services:
        if found_service.name in service_names:
            typer.echo(
                f"Service `{found_service.name}` is configured in launchflow.yaml and your code. Services may only be specified in code or in launchflow.yaml, not both."
            )
            raise typer.Exit(1)
        if service is not None and found_service.name != service:
            continue
        services.append(found_service)

    if not services:
        typer.echo("No services found.")
        raise typer.Exit(1)

    await promote_services(
        *services,
        from_environment=from_environment,
        to_environment=to_environment,
        launchflow_api_key=launchflow_api_key,
        prompt=not auto_approve,
        verbose=verbose,
    )


@app.command()
async def login():
    """Login to LaunchFlow. If you haven't signup this will create a free account for you."""
    try:
        async with async_launchflow_client_ctx(None) as client:
            await login_flow(client)
    except Exception as e:
        typer.echo(f"Failed to login. {e}")
        typer.Exit(1)


@app.command()
def logout():
    """Logout of LaunchFlow."""
    try:
        logout_flow()
    except Exception as e:
        typer.echo(f"Failed to logout. {e}")
        typer.Exit(1)


@app.command()
async def connect(
    account_id: str = typer.Argument(
        None, help="The account ID to fetch. Of the format `acount_123`"
    ),
    provider: CloudProvider = typer.Option(
        None, help="The cloud provider to setup your account with."
    ),
    status: bool = typer.Option(
        False,
        "--status",
        "-s",
        help="Only print out connection status instead of instructions for connecting.",
    ),
):
    """Connect your LaunchFlow account to a cloud provider (AWS or GCP) or retrieve connection info with the `--status / -s` flag."""
    async with async_launchflow_client_ctx() as client:
        if status:
            account_id = await get_account_id_from_config(client, account_id)
            connection_status = await client.connect.status(account_id)
            to_print = connection_status.model_dump()
            del to_print["aws_connection_info"]["cloud_foundation_template_url"]
            print_response("Connection Status", to_print)
        else:
            try:
                await connect_provider(client, account_id, provider)
            except LaunchFlowRequestFailure as e:
                e.pretty_print()
                raise typer.Exit(1)
            except Exception as e:
                typer.echo(str(e))
                raise typer.Exit(1)


@app.command()
async def logs(
    operation_id: str = typer.Argument(
        None, help="The operation ID to fetch logs for."
    ),
):
    """Fetch the logs for a given operation."""
    async with async_launchflow_client_ctx() as client:
        try:
            operation = await client.operations.get(operation_id)
            if not operation.environment_name:
                typer.echo("Operation does not have an environment.")
                raise typer.Exit(1)
            environment = await client.environments.get(
                operation.project_name, operation.environment_name
            )
            if environment.aws_config:
                path = f"s3://{environment.aws_config.artifact_bucket}/logs/{operation_id}.log"
            elif environment.gcp_config:
                path = f"gs://{environment.gcp_config.artifact_bucket}/logs/{operation_id}.log"
            else:
                typer.echo("No artifact bucket found for environment.")
                raise typer.Exit(1)
            with fsspec.open(path) as f:
                print(f.read().decode("utf-8"))
        except LaunchFlowRequestFailure as e:
            e.pretty_print()
            raise typer.Exit(1)


@app.command(hidden=True, name="import")
async def import_resource_cmd(
    environment: Optional[str] = typer.Argument(None, help=ENVIRONMENT_HELP),
    resource: str = typer.Option(
        None,
        help="Resource to import. If none we will scan the directory for available resources.",
    ),
    scan_directory: str = typer.Option(".", help=SCAN_DIRECTORY_HELP),
):
    if launchflow.config.launchflow_yaml is None:
        raise exceptions.LaunchFlowYamlNotFound()
    if environment is None:
        environment, _ = await get_environment(
            project_state_manager=ProjectManager(
                backend=config.launchflow_yaml.backend,
                project_name=config.project,
            ),
            environment_name=environment,
            prompt_for_creation=True,
        )
    _set_global_project_and_environment(None, environment)
    if resource is None:
        resource_refs = find_launchflow_resources(scan_directory)
    else:
        resource_refs = [resource]
    resources = import_resources(resource_refs)

    success = await import_existing_resources(environment, *resources)
    if not success:
        raise typer.Exit(1)


# TODO: I think this is swallowing debug logs for the child processes
# TODO: Update this flow to use the FlowLogger
# TODO: Would be nice to have environment be optional, but typer makes it difficult/messy
@app.command()
async def run(
    environment: str = typer.Argument(..., help=ENVIRONMENT_HELP),
    scan_directory: str = typer.Option(".", help=SCAN_DIRECTORY_HELP),
    args: Optional[List[str]] = typer.Argument(None, help="Additional command to run"),
    disable_run_cache: bool = typer.Option(
        False,
        "--disable-run-cache",
        help="Disable the run cache, Resource outputs will always be fetched.",
    ),
):
    """Run a command against an environment.

    Sample commands:

        launchflow run dev -- ./run.sh
            - Runs ./run.sh against dev environment resources.
    """
    # Caution: environment _must_ be set before importing resources to ensure the correct
    # resource is set
    launchflow.environment = environment
    resources_refs = find_launchflow_resources(scan_directory)
    resources = import_resources(resources_refs)

    local_resources = [
        resource for resource in resources if is_local_resource(resource)
    ]
    remote_resources = [
        resource for resource in resources if not is_local_resource(resource)
    ]
    if local_resources or remote_resources:
        typer.echo("Creating resources...")
        await create_resources(environment, *resources, prompt=True)
        typer.echo("Created resources successfully.\n")

    if args is None:
        typer.echo("No command provided. Exiting")
        return

    command = " ".join(args)
    current_env = os.environ.copy()
    current_env["LAUNCHFLOW_ENVIRONMENT"] = environment

    if not disable_run_cache:
        rich.print("Building run cache...")
        # Connects to all remote resources, and encodes their outputs as an env variable
        resource_outputs = await launchflow.connect_all(*remote_resources)
        resource_outputs_dict = {
            build_cache_key(
                project=launchflow.project,
                environment=environment,
                product=resource.product.value,
                resource=resource.name,
            ): outputs.to_dict()
            for resource, outputs in zip(remote_resources, resource_outputs)
        }
        run_cache = encode_resource_outputs_cache(resource_outputs_dict)
        current_env["LAUNCHFLOW_RUN_CACHE"] = run_cache
        rich.print("Run cache built successfully.")

    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        env=current_env,
    )
    rich.print("───── Program Output ─────")
    rich.print()
    try:

        async def read_line():
            while True:
                line = await proc.stdout.readline()
                if not line:
                    break
                yield line.decode("utf-8")

        async for line in read_line():
            if line:
                rich.print(line, end="")

    except asyncio.CancelledError:
        # TODO: I don't like this sleep but for some reason it starts before the above process has finished printing
        await asyncio.sleep(1)
    finally:
        try:
            proc.kill()
        except ProcessLookupError:
            # Swallow exception if process has already been stopped
            pass
        rich.print("\n──────────────────────────")
        # typer.echo("\nStopping running local resources...")
        # TODO: Add back stopping local containers after removing flow state / connection info on disk
        # local_container_ids = [resource.running_container_id for resource in local_resources]
        # await stop_local_containers(local_container_ids, prompt=False)
        # typer.echo("\nStopped local resources successfully.")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app()
