import pathlib
from typing import List

import toml
from invoke import task, UnexpectedExit
from invoke.context import Context as InvokeContext

from console_messages import success_message, error_message, info_message, generic_message
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


@task(
    help={
        "run_scripts": "Run scripts associated with repo."
    }
)
def setup(c, run_scripts=True):
    """
    Task to setup new repos and run the associated actions with them.
    :argument   run_scripts: bool should we run the scripts associated with the repo
    """
    results = setup_repos(c, run_scripts)
    _print_console_output(results)


def upgrade_repos(c: InvokeContext, pull_master: bool = True, pull_develop: bool = True, run_scripts: bool = False):
    """
    Update your repos.
    :argument   pull_master - Should we pull down the latest master
    :argument   pull_develop - Should we pull down the latest develop(will skip if not defined in config)
    :argument   run_scripts: Should we run defined upgrade scripts.
    """
    results = []
    project = _get_project_config()
    directory = project.directory
    repos = project.repos
    for idx, repo in repos.items():
        if not repo.active:
            return results
        try:
            if pull_master:
                info_message(f"PULLING {repo.main_repo}")
                pull_result = pull_branch(c, repo, directory, repo.main_repo)
                results.append(pull_result)
                if run_scripts:
                    scripts_results = run_repo_scripts(c, repo, 'upgrade')
                    results.extend(scripts_results)
            if pull_develop:
                info_message(f"PULLING {repo.develop_repo}")
                pull_result = pull_branch(c, repo, directory, repo.develop_repo)
                results.append(pull_result)
                if run_scripts:
                    scripts_results = run_repo_scripts(c, repo, 'upgrade')
                    if scripts_results:
                        results.extend(scripts_results)
        except NonZeroExitException as e:
            result = CommandResult(
                exit_code=e.exit_code,
                message=e.message
            )
            results.append(result)
    return results


def setup_repos(c: InvokeContext, run_scripts: bool = False):
    """
    Setup your repos.
    run_scripts: Should we run the defined setup scripts
    """
    results = []
    project = _get_project_config()
    directory = project.directory
    repos = project.repos
    for idx, repo in repos.items():
        if not repo.active:
            return results
        try:
            clone_result = clone_repo(c, repo, directory)
            results.append(clone_result)
            if run_scripts:
                scripts_results = run_repo_scripts(c, repo, 'setup')
                if scripts_results:
                    results.extend(scripts_results)
        except NonZeroExitException as e:
            result = CommandResult(
                exit_code=e.exit_code,
                message=e.message,
                command=e.command
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


def _run_scripts(c, scripts: List[Script], results: List):
    for script in scripts:
        executable = _generate_script(script)
        info_message(f"RUNNING {executable}")
        result = _run_command(c, executable)
        results.append(result)
    return results


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
    info_message("########## OUTPUT ##########")

    for result in results:
        message = f"Command ran: {result.command}"
        if result.exit_code == 0:
            success_message(message)
        if result.exit_code > 0:
            error_message(message)

        generic_message(f"  * Exit code: {result.exit_code}")
        generic_message(f"  * Message: {result.message}")


def pull_branch(c: InvokeContext, repo: Repo, directory: str, branch_name: str) -> CommandResult:
    """Change to the repo directory and pull master."""
    project_path = _generate_path(directory, repo.folder_name)
    cmd = f"cd {project_path} && git checkout {branch_name} && git pull"
    return _run_command(c, cmd)


def clone_repo(c: InvokeContext, repo: Repo, directory: str) -> CommandResult:
    """Change to the repo directory and pull master."""
    cmd = f"cd {directory} && git clone {repo.repo_url}"
    return _run_command(c, cmd)


def run_repo_scripts(c: InvokeContext, repo: Repo, action: str):
    """
    Run the scripts defined on the repo.
    repo: repo from the config file
    action: action defined array (upgrade / setup)
    """
    results = []
    scripts = repo.scripts

    if not scripts:
        return results

    setup_scripts = []
    upgrade_scripts = []
    all_scripts = []

    for script in scripts:
        if script.action == 'setup':
            setup_scripts.append(script)
        elif script.action == 'upgrade':
            upgrade_scripts.append(script)
        elif script.action == 'all':
            all_scripts.append(script)

    if action == 'setup':
        try:
            results = _run_scripts(c, setup_scripts, results)
        except NonZeroExitException as e:
            result = CommandResult(
                exit_code=e.exit_code,
                message=e.message
            )
            results.append(result)
            # return results since we had an error
            return results

    if action == 'upgrade':
        try:
            results = _run_scripts(c, upgrade_scripts, results)
        except NonZeroExitException as e:
            result = CommandResult(
                exit_code=e.exit_code,
                message=e.message,
                command=e.command
            )
            results.append(result)
            # return results since we had an error
            return results

    try:
        results = _run_scripts(c, all_scripts, results)
    except NonZeroExitException as e:
        result = CommandResult(
            exit_code=e.exit_code,
            message=e.message
        )
        results.append(result)
        # return results since we had an error
        return results
