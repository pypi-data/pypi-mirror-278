from dataclasses import dataclass
from typing import Dict

from docker.models.containers import Container

from launchflow.models.flow_state import ResourceState


@dataclass
class CreateResourceDockerInputs:
    resource: ResourceState
    image: str
    env_vars: Dict[str, str]
    command: str
    ports: Dict[str, int]
    logs_dir: str


@dataclass
class CreateResourceDockerOutputs:
    container: Container
    ports: Dict[str, int]


@dataclass
class DestroyResourceDockerInputs:
    container_id: str
    logs_dir: str
