import pathlib

import toml
from invoke import task, UnexpectedExit
from invoke.context import Context as InvokeContext

from exceptions import NonZeroExitException
from schemas import ProjectsTomlSchema, Repo, CommandResult, Script


@task(
    help={
        "pull_master": "Pull the master branch.",
        "pull_develop": "Pull the develop branch",
        "run_scripts": "Run scripts associated with repo."
    }
)
def upgrade(c, pull_master=True, pull_develop=True, run_scripts=True):
    results = upgrade_repos(c, pull_master, pull_develop, run_scripts)
    _print_console_output(results)


def upgrade_repos(c: InvokeContext, pull_master: bool = True, pull_develop: bool = True, run_scripts: bool = False):
    """
    Update your repos.
    pull_master: Should we pull down the latest master
    pull_develop: Should we pull down the latest develop(will skip if not defined in config)
    migrate: Should we run migrations(will skip if not defined in config)
    """
    results = []
    project = _get_project_config()
    directory = project.directory
    repos = project.repos
    for idx, repo in repos.items():
        try:
            if pull_master:
                pull_result = pull_branch(c, repo, directory, repo.main_repo)
                results.append(pull_result)
                if pull_result.exit_code > 0:
                    return results
                if run_scripts:
                    scripts_results = run_repo_scripts(c, repo)
                    results.extend(scripts_results)
        except NonZeroExitException as e:
            result = CommandResult(
                exit_code=e.exit_code,
                message=e.message
            )
            results.append(result)
    return results


def _get_project_config():
    """Import the projects toml file and return a dict."""
    path = pathlib.Path(__file__).parent.absolute()
    toml_file = f"{path}/projects.toml"
    projects = toml.load(toml_file)

    # validate via pydantic models
    project_schema = ProjectsTomlSchema.parse_obj(projects)
    return project_schema


def _generate_path(directory: str, project_folder: str):
    return f"{directory}{project_folder}"


def _generate_script(script: Script):
    executable = f"{script.executable} {script.path}"
    return executable.strip()


def _run_command(c: InvokeContext, cmd: str) -> CommandResult:
    """Command runner."""
    try:
        result = c.run(cmd)
        return CommandResult(
            exit_code=result.exited,
            message=result.stdout,
            command=cmd
        )
    except UnexpectedExit as e:
        raise NonZeroExitException(
            exit_code=e.result.exited,
            message=e.result.stderr,
            command=cmd
        )


def _print_console_output(results):
    """Generate console output."""
    reset_style = "\u001b[0m"
    print("########## OUTPUT ##########")

    for result in results:
        style = "\u001b[32m"
        if result.exit_code > 0:
            style = "\u001b[31m"

        print(f"{style} Command ran: {result.command} {reset_style}")
        print(f"  * Exit code: {result.exit_code}")
        print(f"  * Message: {result.message}")


def pull_branch(c: InvokeContext, repo: Repo, directory: str, branch_name: str) -> CommandResult:
    """Change to the repo directory and pull master."""
    project_path = _generate_path(directory, repo.folder_name)
    cmd = f"cd {project_path} && git checkout {branch_name} && git pull"
    return _run_command(c, cmd)


def run_repo_scripts(c: InvokeContext, repo: Repo):
    """Run the scripts defined on the repo."""
    results = []
    scripts = repo.scripts
    for script in scripts:
        executable = _generate_script(script)
        try:
            result = _run_command(c, executable)
            results.append(result)
        except NonZeroExitException as e:
            result = CommandResult(
                exit_code=e.exit_code,
                message=e.message,
                command=executable
            )
            results.append(result)
            return results
