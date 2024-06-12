from pydantic import BaseModel
from typing import Union, List
from pathlib import Path
from typing import Optional
from collections import defaultdict

from .StorageConfig import LocalStorageConfig, S3StorageConfig


class ScriptConfig(BaseModel):
    name: str
    run_on_start: bool = True
    command: Optional[str] = None
    run_every: Optional[int] = None  # seconds (in cloud minutes)
    storage: Optional[str] = None  # folder to bind in cloud
    type: str = "script"
    wait_for: Optional[List[str]] = []

    # make sure that at least run_on_start or run_every is set
    def __init__(self, **data):
        super().__init__(**data)
        if not self.run_on_start and not self.run_every:
            raise ValueError(
                f"Script {self.name} must have either run_on_start or run_every set."
            )


class NotebookConfig(BaseModel):
    name: str
    command: Union[str, None] = None
    storage: Union[str, None] = None  # folder to bind in cloud
    port: int = 8888
    host: str = "0.0.0.0"
    type: str = "notebook"


class APIConfig(BaseModel):
    name: str
    command: Union[str, None] = None
    port: int = 8000
    host: str = "0.0.0.0"
    storage: Union[str, None] = None  # folder to bind in cloud
    type: str = "api"


class UIConfig(BaseModel):
    name: str
    command: str  # steamlit, javascript, ...
    port: int = 3000
    host: str = "0.0.0.0"
    env: dict = {}  # can accept the name of another service as a url placeholder
    type: str = "ui"


class Config(BaseModel):
    dir: Path
    project: str
    scripts: List[ScriptConfig] = []
    notebooks: List[NotebookConfig] = []
    apis: List[APIConfig] = []
    uis: List[UIConfig] = []
    storage: List[Union[LocalStorageConfig, S3StorageConfig]] = []

    def __init__(self, **data):
        super().__init__(**data)
        self.scripts = self.sort_scripts(self.scripts)

    # iterator for all the services
    def __iter__(self):
        # if self.storage:
        #     for storage in self.storage:
        #         yield storage
        if self.scripts:
            for script in self.scripts:
                yield script
        if self.notebooks:
            for notebook in self.notebooks:
                yield notebook
        if self.apis:
            for api in self.apis:
                yield api
        if self.uis:
            for ui in self.uis:
                yield ui
        if self.storage:
            for storage in self.storage:
                yield storage

    def type2folder(self, type):
        return type + "s"

    @staticmethod
    def sort_scripts(scripts):
        # cehcks
        object_names = {obj.name for obj in scripts}
        for obj in scripts:
            # check if all dependencies are in the scripts
            if not set(obj.wait_for).issubset(object_names):
                raise ValueError(
                    f"Dependency {set(obj.wait_for) - object_names} not found in scripts"
                )
            # check script is running on start
            if obj.wait_for and not obj.run_on_start:
                raise ValueError(
                    f"Script {obj.name} is not running on start, but has dependencies. This is not allowed."
                )
            # check all dependencies are running on start
            if obj.wait_for and not all(
                script.run_on_start for script in scripts if script.name in obj.wait_for
            ):
                raise ValueError(
                    f"Script {obj.name} has dependencies, but not all dependencies are running on start. This is not allowed."
                )
        # sort the scripts
        dependencies = {script.name: set(script.wait_for) for script in scripts}
        independent = {
            script.name for script in scripts if not dependencies[script.name]
        }
        sorted_scripts = []
        while independent:
            script = independent.pop()
            sorted_scripts.append(script)
            for name, deps in dependencies.items():
                deps.discard(script)
                if not deps and name not in sorted_scripts:
                    independent.add(name)
        if len(sorted_scripts) != len(scripts):
            raise ValueError("Dependency cycle detected in your scripts configuration.")
        return [
            next(script for script in scripts if script.name == name)
            for name in sorted_scripts
        ]
