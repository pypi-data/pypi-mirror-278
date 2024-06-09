from pathlib import Path

from docker_ready.project import Project
from docker_ready.utils.constants import Labels
from docker_ready.utils.tools import docker

PROJECTS_DIR = Path(__file__).parent.joinpath("projects").absolute()


def get_all_projects() -> list[Project]:
    return [Project(directory=child) for child in PROJECTS_DIR.iterdir() if child.is_dir()]


def get_project_by_name(name: str) -> Project | None:
    for child in PROJECTS_DIR.iterdir():
        if child.name == name and child.is_dir():
            containers = (
                docker.containers.list(filters={"label": f"{Labels.project}={name}"}) or None
            )
            return Project(directory=child, containers=containers)


def get_running_projects() -> list[Project]:
    projects_containers = {}
    if containers := docker.containers.list(filters={"label": Labels.project}):
        for container in containers:
            project_name = container.labels[Labels.project]
            if projects_containers.get(project_name):
                projects_containers[project_name].append(container)
            else:
                projects_containers[project_name] = [container]

    return [
        Project(directory=PROJECTS_DIR.joinpath(name), containers=containers)
        for name, containers in projects_containers.items()
    ]


__all__ = ["get_all_projects", "get_project_by_name", "get_running_projects"]
