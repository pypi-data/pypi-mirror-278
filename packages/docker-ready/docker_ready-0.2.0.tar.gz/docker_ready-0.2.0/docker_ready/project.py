from pathlib import Path
from typing import Annotated, Any

from docker.models.containers import Container
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import HttpUrl
from pydantic_yaml import parse_yaml_file_as

from docker_ready.utils.constants import Dirs


class Info(BaseModel):
    full_name: str
    description: str
    site_url: HttpUrl
    repo_url: HttpUrl
    container_registry_url: HttpUrl


class ProjectYaml(BaseModel):
    info: Info
    env_files: dict[str, dict[str, Any]]


class Network(BaseModel):
    name: str
    driver: str


class Service(BaseModel):
    image: str
    container_name: Annotated[str | None, Field(default=None)]
    env_file: list
    networks: Annotated[list[str] | None, Field(default=None)]
    ports: Annotated[list[str] | None, Field(default=None)]
    volumes: Annotated[list[str] | None, Field(default=None)]


class ComposeYaml(BaseModel):
    name: str
    networks: Annotated[dict[str, Network] | None, Field(default=None)]
    services: dict[str, Service]


class Project:
    def __init__(self, directory: Path, containers: list[Container] | None = None) -> None:
        self.root_dir = directory
        self.user_dir = Dirs.config.joinpath(directory.name)

        if self.user_dir.exists():
            directory = self.user_dir

        self._project(directory=directory)
        self._compose(directory=directory)
        self.containers = containers

    def _project(self, directory: Path) -> None:
        self.project_yaml_file = directory.joinpath("project.yaml")
        project = parse_yaml_file_as(ProjectYaml, self.project_yaml_file)
        self.info = project.info
        self.env_files = project.env_files

    def _compose(self, directory: Path) -> None:
        self.compose_yaml_file = directory.joinpath("compose.yaml")
        self.compose = parse_yaml_file_as(ComposeYaml, self.compose_yaml_file)


__all__ = ["Project"]
