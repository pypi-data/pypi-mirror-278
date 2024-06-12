import os
from enum import Enum
from typing import List, Optional, Type

import beaupy
import rich
import typer

from launchflow import Resource, exceptions
from launchflow.aws.elasticache import ElasticacheRedis
from launchflow.aws.rds import RDSPostgres
from launchflow.aws.s3 import S3Bucket
from launchflow.backend import BackendOptions, LaunchFlowBackend, LocalBackend
from launchflow.clients import async_launchflow_client_ctx
from launchflow.config import config
from launchflow.config.launchflow_yaml import LaunchFlowDotYaml
from launchflow.docker.postgres import DockerPostgres
from launchflow.docker.redis import DockerRedis
from launchflow.flows.auth import login_flow
from launchflow.flows.project_flows import get_project
from launchflow.gcp.cloudsql import CloudSQLPostgres
from launchflow.gcp.compute_engine import ComputeEngineRedis
from launchflow.gcp.gcs import GCSBucket
from launchflow.gcp.memorystore import MemorystoreRedis
from launchflow.validation import validate_project_name


class BackendType(Enum):
    LOCAL = "local"
    GCS = "gcs"
    LAUNCHFLOW = "lf"


class Framework(Enum):
    FASTAPI = "fastapi"
    FLASK = "flask"
    DJANGO = "django"


FRAMEWORK_CHOICES = [
    (
        Framework.FASTAPI,
        "FastAPI framework, high performance, easy to learn, fast to code, ready for production.",
    ),
    (
        Framework.FLASK,
        "The Python micro framework for building web applications.",
    ),
    (
        Framework.DJANGO,
        "The Web framework for perfectionists with deadlines.",
    ),
]


class InfrastructureProvider(Enum):
    GCP = "GCP"
    AWS = "AWS"
    Docker = "Docker"


INFRASTRUCTURE_PROVIDER_CHOICES = [
    (InfrastructureProvider.GCP, "Google Cloud Platform"),
    (InfrastructureProvider.AWS, "Amazon Web Services"),
    (InfrastructureProvider.Docker, "Docker Engine (localhost)"),
]


GCP_RESOURCE_CHOICES = [
    (
        GCSBucket,
        "Storage bucket. Powered by Google Cloud Storage (GCS).",
    ),
    (
        CloudSQLPostgres,
        "PostgreSQL database. Powered by Cloud SQL on GCP.",
    ),
    (
        ComputeEngineRedis,
        "Redis on a VM. Powered by Compute Engine on GCP.",
    ),
    (
        MemorystoreRedis,
        "Redis Cluster. Powered by Memorystore on GCP.",
    ),
]

AWS_RESOURCE_CHOICES = [
    (
        S3Bucket,
        "Storage bucket. Powered by Amazon S3.",
    ),
    (
        RDSPostgres,
        "PostgreSQL database. Powered by Amazon RDS.",
    ),
    (
        ElasticacheRedis,
        "Redis Cluster. Powered by Amazon ElastiCache.",
    ),
]

DOCKER_RESOURCE_CHOICES = [
    (
        DockerPostgres,
        "PostgreSQL database. Running locally on Docker.",
    ),
    (
        DockerRedis,
        "Redis instance. Running locally on Docker.",
    ),
]


def _select_backend() -> Optional[BackendType]:
    options = [
        "Local - State will be saved in your project directory",
        "LaunchFlow Cloud - State will be managed for you and shared with teammates",
    ]
    answer = beaupy.select(options=options, return_index=True)
    if answer is None:
        typer.echo("No backend selected. Exiting.")
        raise typer.Exit(1)
    if answer == 0:
        return BackendType.LOCAL
    return BackendType.LAUNCHFLOW


def maybe_append_file_to_gitignore(file_name: str, gitignore_path=".gitignore"):
    need_to_append = True

    if os.path.isfile(gitignore_path):
        with open(gitignore_path, "r") as gitignore_file:
            gitignore_contents = gitignore_file.readlines()

        for line in gitignore_contents:
            line = line.strip()
            if line == file_name or (line.endswith("/") and file_name.startswith(line)):
                need_to_append = False
                break

    if need_to_append:
        with open(gitignore_path, "a") as gitignore_file:
            gitignore_file.write(f"\n# LaunchFlow\n{file_name}\n")


async def generate_launchflow_yaml(
    default_backend_type: Optional[BackendType],
):
    cwd = os.getcwd()
    config_path = os.path.join(cwd, "launchflow.yaml")
    if os.path.exists(config_path):
        typer.echo("A launchflow.yaml file already exists in this directory.")
        overwrite = beaupy.confirm(
            "Would you like to reconfigure the existing launchflow.yaml?",
            default_is_yes=False,
        )
        if not overwrite:
            typer.echo("Reusing the existing launchflow.yaml. No changes will be made.")
            return
        typer.echo("This program will overwrite the existing launchflow.yaml.")

    backend_type = default_backend_type
    if backend_type is None:
        backend_type = _select_backend()

    if backend_type == BackendType.LAUNCHFLOW:
        login_or_signup = False
        try:
            config.get_access_token()
        except exceptions.LaunchFlowRequestFailure:
            rich.print("[red]Failed to refresh LaunchFlow credentials.[/red]")
            login_or_signup = beaupy.confirm(
                "Would you like to re-login to LaunchFlow?",
                default_is_yes=True,
            )
            if not login_or_signup:
                typer.echo("Exiting.")
                raise typer.Exit(1)
        except exceptions.NoLaunchFlowCredentials:
            rich.print("[red]No LaunchFlow credentials found.[/red]")
            login_or_signup = beaupy.confirm(
                "Would you like to login / sign up for LaunchFlow?",
                default_is_yes=True,
            )
            if not login_or_signup:
                typer.echo("Exiting.")
                raise typer.Exit(1)

        if login_or_signup:
            async with async_launchflow_client_ctx(None) as client:
                await login_flow(client)

        async with async_launchflow_client_ctx(None) as client:
            accounts = await client.accounts.list()
            if len(accounts) == 0:
                rich.print("[red]Failed to fetch LaunchFlow accounts.[/red]")
                rich.print(
                    "Please contact team@launchflow.com if the issue persists.\n"
                )
                raise typer.Exit(1)
            elif len(accounts) > 1:
                rich.print("Which LaunchFlow account would you like to use?")
                account_id = beaupy.select(
                    [account.id for account in accounts], strict=True
                )
                if account_id is None:
                    rich.print("No account selected. Exiting.")
                    raise typer.Exit(1)
                rich.print(f"[pink1]>[/pink1] {account_id}")
                account_id_for_config = account_id
            else:
                account_id = accounts[0].id
                account_id_for_config = "default"

        async with async_launchflow_client_ctx(
            launchflow_account_id=account_id
        ) as client:
            project = await get_project(
                client=client.projects,
                account_id=account_id,
                project_name=None,
                prompt_for_creation=True,
            )
            if project is None:
                typer.echo("Project creation cancelled.")
                raise typer.Exit(1)
            project_name = project.name

        backend = LaunchFlowBackend.parse_backend(f"lf://{account_id_for_config}")
    else:
        project_name = beaupy.prompt(
            "What would you like to name your LaunchFlow project?"
        )
        while True:
            valid, reason = validate_project_name(project_name, raise_on_error=False)
            if valid:
                break
            else:
                rich.print(f"[red]{reason}[/red]")
                project_name = beaupy.prompt("Please enter a new project name.")
        backend = LocalBackend.parse_backend("file://.launchflow")

    launchflow_yaml = LaunchFlowDotYaml(
        project=project_name,
        backend=backend,
        backend_options=BackendOptions(),
        default_environment=None,
        config_path=config_path,
    )
    launchflow_yaml.save()

    # Append to the gitignore (if .launchflow is not already in the gitignore)
    maybe_append_file_to_gitignore(
        file_name=".launchflow", gitignore_path=os.path.join(cwd, ".gitignore")
    )


def _select_framework() -> Framework:
    options = [f"{f[0].value} - {f[1]}" for f in FRAMEWORK_CHOICES]
    print()
    print("Select a framework for your API: (More coming soon)")
    answer = beaupy.select(options=options, return_index=True, strict=True)
    if answer is None:
        typer.echo("No framework selected. Exiting.")
        raise typer.Exit(1)
    rich.print(f"[pink1]>[/pink1] {options[answer]}")
    return FRAMEWORK_CHOICES[answer][0]


def _select_infra_provider() -> Optional[InfrastructureProvider]:
    answer = beaupy.confirm(
        "Would you like to add any infrastructure to your project?",
        default_is_yes=True,
    )
    if not answer:
        typer.echo("No infrastructure selected. Continuing without infrastructure.")
        return None

    options = [f"{f[0].value} - {f[1]}" for f in INFRASTRUCTURE_PROVIDER_CHOICES]
    print()
    print(
        "Select the infrastructure provider you'd like to use. You can always change providers later."
    )
    answer = beaupy.select(options=options, return_index=True, strict=True)
    if answer is None:
        typer.echo(
            "No infrastructure provider selected. Continuing without infrastructure."
        )
        return None
    return INFRASTRUCTURE_PROVIDER_CHOICES[answer][0]


def _select_resources(
    infra_provider: Optional[InfrastructureProvider],
) -> List[Type[Resource]]:
    if infra_provider is None:
        return []

    if infra_provider == InfrastructureProvider.GCP:
        resource_choices = GCP_RESOURCE_CHOICES
    elif infra_provider == InfrastructureProvider.AWS:
        resource_choices = AWS_RESOURCE_CHOICES
    elif infra_provider == InfrastructureProvider.Docker:
        resource_choices = DOCKER_RESOURCE_CHOICES
    else:
        raise NotImplementedError(
            f"Infrastructure provider {infra_provider} is not supported yet."
        )

    options = [f"{f[0].__name__} - {f[1]}" for f in resource_choices]
    rich.print()
    rich.print(
        "Select any Resources you'd like to include in your application. You can always add / remove Resources later."
    )
    answers = beaupy.select_multiple(options=options, return_indices=True)
    to_ret = []
    for answer in answers:
        rich.print(f"[pink1]>[/pink1] {options[answer]}")
        to_ret.append(resource_choices[answer][0])
    if not answers:
        rich.print(
            "[pink1]>[/pink1] No Resources selected. Continuing without Resources."
        )
    return to_ret


# TODO: Implement template project generation
async def generate_template_project(
    template_id: str,
    default_backend: Optional[BackendType] = None,
):
    raise NotImplementedError("The template project feature is not implemented yet.")


# TODO: Implement bootstrap project generation
async def generate_bootstrap_project(
    default_backend: Optional[BackendType] = None,
):
    raise NotImplementedError("The bootstrap project feature is not implemented yet.")
    # project_name = beaupy.prompt("What is the name of your project?")

    # # Prompt the user to select where to save the project and default to the cwd
    # cwd_path = os.getcwd()
    # potential_project_path = os.path.join(cwd_path, project_name)
    # project_path = beaupy.prompt(
    #     "Where would you like to save the project?",
    #     initial_value=potential_project_path,
    # )
    # print(f"User selected the following project path: {project_path}")

    # framework = _select_framework()
    # infra_provider = _select_infra_provider()
    # resources = _select_resources(infra_provider)

    # print(f"User selected the following framework: {framework}")
    # print(f"User selected the following infrastructure provider: {infra_provider}")
    # print(f"User selected the following resources: {resources}")

    # if framework == Framework.FASTAPI:
    #     generator = FastAPIProjectGenerator(
    #         resources=resources,
    #         cloud_provider=cloud_provider,
    #         launchflow_project_name=project.name,
    #         launchflow_environment_name=environment.name,
    #     )
    #     generator.generate_project(full_directory_path)
    # elif framework == Framework.FLASK:
    #     generator = FlaskProjectGenerator(
    #         resources=resources,
    #         cloud_provider=cloud_provider,
    #         launchflow_project_name=project.name,
    #         launchflow_environment_name=environment.name,
    #     )
    #     generator.generate_project(full_directory_path)
    # elif framework == Framework.DJANGO:
    #     generator = DjangoProjectGenerator(
    #         resources=resources,
    #         cloud_provider=cloud_provider,
    #         launchflow_project_name=project.name,
    #         launchflow_environment_name=environment.name,
    #     )
    #     generator.generate_project(full_directory_path)
    # else:
    #     raise NotImplementedError(f"Framework {framework} is not supported yet.")

    # print()
    # print("Done!")
    # print()
    # print("Navigate to your project directory:")
    # rich.print(f"  $ [green]cd {directory}")
    # print()
    # print("To create your resources run:")
    # rich.print("  $ [green]launchflow create")
    # print()
    # print("To build and deploy your app remotely run:")
    # rich.print("  $ [green]launchflow deploy")
