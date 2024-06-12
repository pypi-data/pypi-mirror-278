import os
from typing import Dict, Optional

import yaml

import launchflow
from launchflow.config import config
from launchflow.models.enums import ResourceProduct
from launchflow.node import Inputs
from launchflow.resource import Resource, T
from launchflow.workflows.manage_docker.manage_docker_resources import find_open_port


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
        # TODO: After making connect work, these resources should at most cache the port, they
        # shouldn't generate a port every time they spin up (then we have to ignore it in lf create)
        self.ports = ports or {}
        self.running_container_id = running_container_id

    def connection_info(self) -> Optional[T]:
        """
        Docker resources must implement a connection_info method to return the connection info that
        should be stored on disk. If the resource is not running, this method should return None.
        """
        raise NotImplementedError

    def inputs(self, *args, **kwargs) -> Inputs:
        raise NotImplementedError

    async def inputs_async(self, *args, **kwargs) -> Inputs:
        raise NotImplementedError

    @property
    def resource_type(self):
        return self.__class__.__name__

    def refresh_ports(self) -> None:
        """
        Refresh the allocated ports with new ones.
        """
        for internal_port in self.ports:
            self.ports[internal_port] = find_open_port()

    def outputs(self) -> T:
        """
        Synchronously connect to the resource by fetching its outputs.
        """
        # TODO handle project_name / environment_name / launchflow_yaml_path being None
        project_name = launchflow.project
        environment_name = launchflow.environment
        launchflow_yaml_path = config.launchflow_yaml.config_path

        if (
            project_name is None
            or environment_name is None
            or launchflow_yaml_path is None
        ):
            raise NotImplementedError

        connection_info_path = os.path.join(
            os.path.dirname(launchflow_yaml_path),
            ".launchflow",
            "docker",
            project_name,
            environment_name,
            "resources",
            self.name,
            "connection_info.yaml",
        )

        with open(connection_info_path) as file:
            resource_connection_info = yaml.safe_load(file.read())
        return self._outputs_type(**resource_connection_info)

    async def outputs_async(self) -> T:
        """
        Asynchronously connect to the resource by fetching its outputs.
        """
        return self.outputs()
