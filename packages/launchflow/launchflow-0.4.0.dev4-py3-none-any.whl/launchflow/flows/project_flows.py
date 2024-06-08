from typing import Optional

import beaupy
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn

from launchflow.clients.projects_client import ProjectsAsyncClient
from launchflow.clients.response_schemas import ProjectResponse
from launchflow.exceptions import LaunchFlowRequestFailure


async def get_project(
    client: ProjectsAsyncClient,
    account_id: str,
    project_name: Optional[str],
    prompt_for_creation: bool = False,
    include_non_ready: bool = False,
) -> ProjectResponse:
    if project_name is None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Fetching projects...", total=None)
            projects = await client.projects.list(account_id)
            progress.remove_task(task)

        projects = [p for p in projects if p.status == "ready" or include_non_ready]
        project_names = [p.name for p in projects]
        if prompt_for_creation:
            project_names.append("[i yellow]Create new project[/i yellow]")
        print("Select the project to use:")
        selected_project = beaupy.select(project_names, return_index=True, strict=True)
        if prompt_for_creation and selected_project == len(project_names) - 1:
            if project_name is None:
                project_name = beaupy.prompt("Enter the project name:")
                rich.print(f"[pink1]>[/pink1] {project_name}")
            project = await create_project(client)
        else:
            project = projects[selected_project]
            rich.print(f"[pink1]>[/pink1] {project.name}")
        return project
    try:
        # Fetch the project to ensure it exists
        project = await client.get(project_name)
    except LaunchFlowRequestFailure as e:
        if e.status_code == 404 and prompt_for_creation:
            answer = beaupy.confirm(
                f"Project `{project_name}` does not exist yet. Would you like to create it?"
            )
            if answer:
                # TODO: this will just use their default account. Should maybe ask them.
                # But maybe that should be in the create project flow?
                project = await create_project(client, project_name)
            else:
                raise e
        else:
            raise e
    return project


async def create_project(
    client: ProjectsAsyncClient,
    project_name: str,
    account_id: str,
    prompt: bool = True,
):
    if prompt:
        user_confirmation = beaupy.confirm(
            f"Would you like to create a new project `{project_name}` in your LaunchFlow account `{account_id}`?",
            default_is_yes=True,
        )
        if not user_confirmation:
            rich.print("[red]✗[/red] Project creation cancelled.")
            return

    project = None
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Creating LaunchFlow Project...", total=None)
        try:
            project = await client.create(project_name)
        except Exception as e:
            progress.console.print("[red]✗[/red] Failed to create project.")
            progress.console.print(
                "    └── Run this command again to retry creating the project."
            )
            progress.console.print(f"    └── {str(e)}")
            raise e
        finally:
            progress.update(task, advance=1)
            progress.remove_task(task)
    progress.console.print("[green]✓[/green] Project created successfully.")
    return project
