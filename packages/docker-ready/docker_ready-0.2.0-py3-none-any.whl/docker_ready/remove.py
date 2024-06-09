import shutil

from docker_ready.project import Project
from docker_ready.utils.constants import Labels
from docker_ready.utils.tools import docker


def remove_project(project: Project) -> None:
    _remove_config_dir(p=project)
    _remove_containers(p=project)


def _remove_config_dir(p: Project) -> None:
    if p.user_dir.exists():
        shutil.rmtree(path=p.user_dir)


def _remove_containers(p: Project) -> None:
    if containers := p.containers or docker.containers.list(
        filters={"label": f"{Labels.project}={p.compose.name}"}
    ):
        for container in containers:
            container.remove(force=True)


__all__ = ["remove_project"]
