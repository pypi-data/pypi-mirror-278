from pathlib import Path
from typing import NamedTuple


class Labels(NamedTuple):
    project = "docker-ready.project"


class Dirs(NamedTuple):
    config = Path("~").expanduser().joinpath(".config").joinpath("docker-ready")


__all__ = ["Labels", "Dirs"]
