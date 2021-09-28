from typing import Optional, Dict, List

from pydantic import BaseModel


class Script(BaseModel):
    """
    Script that needs run to setup or update a project.

    executable: is the program or executable to run the script. bash python php node etc

    path: is the path to the script and any arguments you need. Example if you were running and compiling a typescript
    project then your executable would be npm and the path would be: run tsc:build && npm run webpack:build.

    action: task action - upgrade/setup/all
    """
    executable: str
    path: str
    action: str


class Repo(BaseModel):
    folder_name: str
    active: bool
    main_repo: str
    develop_repo: Optional[str]
    scripts: Optional[List[Script]]


class ProjectsTomlSchema(BaseModel):
    title: str
    directory: str
    repos: Dict[str, Repo]


class CommandResult(BaseModel):
    exit_code: int
    message: str
    command: str

