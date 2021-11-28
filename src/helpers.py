from functools import lru_cache

import toml
import pathlib

from schemas import ProjectsTomlSchema

@lru_cache()
def generate_project_config(config: str):
    """
    Generate a project config file.
    :argument   config: Folder name for config to run
    """
    path = pathlib.Path(__file__).parent.parent.absolute()
    project_config_folder = f"{path}/configs/{config}"
    project_build_config = toml.load(f"{project_config_folder}/build.toml")
    project_config = ''

    main_file = f"{project_config_folder}/{project_build_config['main_file']}.toml"
    with open(main_file) as fp:
        project_config += fp.read()
        project_config += '\n'

    for repo_file in project_build_config['repo_build_order']:
        with open(f"{project_config_folder}/{repo_file}.toml") as fp:
            project_config += fp.read()
            project_config += '\n'

    # validate via pydantic models

    project = toml.loads(project_config)
    project_schema = ProjectsTomlSchema.parse_obj(project)
    return project_schema
