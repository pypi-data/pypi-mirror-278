import shutil

from docker.models.networks import Network
from dotenv import dotenv_values

from docker_ready.project import ComposeYaml, Project, Service
from docker_ready.utils.constants import Labels
from docker_ready.utils.tools import docker


def run_project(project: Project) -> None:
    _setup_project_dir(project=project)
    networks = _create_networks(compose=project.compose)
    for name, service in project.compose.services.items():
        _run_service(name=name, project_networks=networks, service=service, project=project)


def _setup_project_dir(project: Project) -> None:
    _create_project_dir(project=project)
    _create_env_files(project=project)


def _create_project_dir(project: Project) -> None:
    if not project.user_dir.exists():
        project.user_dir.mkdir(parents=True)

        shutil.copyfile(
            project.project_yaml_file.absolute(),
            project.user_dir.joinpath(project.project_yaml_file.name),
        )
        shutil.copyfile(
            project.compose_yaml_file.absolute(),
            project.user_dir.joinpath(project.compose_yaml_file.name),
        )


def _create_env_files(project: Project) -> None:
    for file_name, envs in project.env_files.items():
        with open(project.user_dir.joinpath(f"{file_name}.env"), "w") as f:
            for env_name, env_value in envs.items():
                f.write(f"{env_name}={env_value}\n")


def _create_networks(compose: ComposeYaml) -> dict[str, Network] | None:
    if compose.networks:
        networks = {}
        for _, network in compose.networks.items():
            networks.update(
                {network.name: docker.networks.create(name=network.name, driver=network.driver)}
            )
        return networks


def _run_service(
    name: str, service: Service, project_networks: dict[str, Network] | None, project: Project
) -> None:
    container = docker.containers.run(
        image=service.image,
        environment=_environment(s=service, p=project),
        labels=_labels(p=project),
        name=_name(s=service, p=project),
        ports=_ports(s=service),
        volumes=service.volumes,
        detach=True,
    )
    if service.networks and project_networks:
        for service_network in service.networks:
            if network := project_networks.get(service_network):
                network.connect(container=container, aliases=[service.container_name, name])


def _environment(s: Service, p: Project) -> dict[str, str | None] | None:
    if s.env_file:
        return dotenv_values(p.user_dir.joinpath(s.env_file[0]))


def _labels(p: Project) -> dict[str, str]:
    return {Labels.project: p.compose.name}


def _name(s: Service, p: Project) -> str:
    if s.container_name:
        return s.container_name
    return f"{p.compose.name}-{s.container_name}"


def _ports(s: Service) -> dict[int | str, int | tuple | list[int] | None] | None:
    if s.ports:
        ports = {}
        for port in s.ports:
            host, container = port.split(":")
            ports.update({container: host})
        return ports


__all__ = ["run_project"]
