from typing import Dict, Optional

import launchflow
from launchflow import exceptions
from launchflow.clients.docker_client import DockerClient
from launchflow.managers.docker_resource_manager import (
    base64_to_dict,
    get_container_filter_labels,
)
from launchflow.models.enums import ResourceProduct
from launchflow.node import Inputs
from launchflow.resource import Resource, T


class DockerResource(Resource[T]):
    def __init__(
        self,
        name: str,
        docker_image: str,
        env_vars: Optional[Dict[str, str]] = None,
        command: Optional[str] = None,
        ports: Optional[Dict[str, int]] = None,
        running_container_id: Optional[str] = None,
    ):
        super().__init__(name, ResourceProduct.LOCAL_DOCKER, {})
        self.docker_image = docker_image
        self.env_vars = env_vars or {}
        self.command = command

        self.ports = ports or {}
        self.running_container_id = running_container_id

    def inputs(self, *args, **kwargs) -> Inputs:
        raise NotImplementedError

    async def inputs_async(self, *args, **kwargs) -> Inputs:
        raise NotImplementedError

    @property
    def resource_type(self):
        return self.__class__.__name__

    def outputs(self) -> T:
        """
        Synchronously connect to the resource by fetching its outputs.
        """
        docker_client = DockerClient()
        containers = docker_client.client.containers.list(
            filters={
                "label": get_container_filter_labels(resource_name=self.name, environment_name=launchflow.environment),
            },
            all=True
        )

        # If no containers match, it hasn't been created yet.
        # More than one matching should not happen by launchflow's doing.
        if len(containers) == 0:
            return self._outputs_type(password="password", ports={})
        if len(containers) != 1:
            raise ValueError(f"Expected 1 container, got {len(containers)}")

        if containers[0].status != "running":
            raise exceptions.ResourceStopped(self.name)

        # Get the inputs dict, which is the same as the outputs for containers
        encoded_inputs = containers[0].labels.get("inputs", None)

        inputs_dict = base64_to_dict(encoded_inputs)
        return self._outputs_type(**inputs_dict)

    async def outputs_async(self) -> T:
        """
        Asynchronously connect to the resource by fetching its outputs.
        """
        return self.outputs()
