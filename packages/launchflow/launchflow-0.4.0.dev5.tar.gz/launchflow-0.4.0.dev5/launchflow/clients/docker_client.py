import hashlib
import json
import logging
from copy import deepcopy
from typing import Any, Dict, List, Optional

import docker
from docker.errors import APIError, DockerException, ImageNotFound, NotFound
from docker.models.containers import Container
from docker.models.images import Image


class PortAlreadyAllocatedError(Exception):
    def __init__(self, message):
        super().__init__(message)


def hash_resource_inputs(resource_inputs: Dict[str, Any]) -> str:
    """
    Hash the create args and store it as a label on the container so we can tell when the create args
    have changed. This isn't free from false positives -- if two dictionaries have different key order
    then they will hash to different values even if the data is the same. This is fine though.

    Args:
    - `resource_inputs`: The dictionary of resource inputs.

    Returns:
    - The hash of the create args.
    """
    args_copy = deepcopy(resource_inputs)
    if "kwargs" in args_copy:
        args_copy.update(args_copy.pop("kwargs"))
    del args_copy["ports"]

    serialized_args = json.dumps(args_copy)
    return hashlib.sha256(serialized_args.encode()).hexdigest()


def docker_service_available():
    try:
        docker.from_env()
        return True
    # TODO: Link to LF docs when we're erroring out for this. Might be nice to have a check_docker_available that raises
    # instead to link from one place.
    except DockerException:
        return False


class DockerClient:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            logging.error(f"An error occurred when trying to connect to Docker: {e}")
            logging.error(
                "This error usually occurs when Docker is not running or installed.\n"
                "You can install Docker Engine from https://docs.docker.com/engine/install/\n"
            )

    def list_containers(self) -> List[Container]:
        """
        List all Docker containers with the launchflow_managed label.
        """
        try:
            # lists all containers with the launchflow_managed label
            containers = self.client.containers.list(
                filters={"label": "launchflow_managed"}
            )
            logging.info(f"Found {len(containers)} containers.")
            return containers
        except APIError as e:
            logging.error(f"Server returned error when trying to list containers: {e}")
            return []
        except Exception as e:
            logging.error(f"An error occurred when trying to list containers: {e}")
            return []

    def get_container(self, name_or_id: str) -> Optional[Container]:
        """
        Get a Docker container by name or id.
        """
        try:
            container = self.client.containers.get(name_or_id)
            logging.info(f"Container {name_or_id} found.")
            return container
        except NotFound:
            logging.warning(f"No container with name/id {name_or_id} found.")
            return None
        except APIError as e:
            logging.error(
                f"Server returned error when trying to get container {name_or_id}: {e}"
            )
            return None

    def start_container(
        self,
        name: str,
        image: str,
        env_vars=None,
        command=None,
        ports=None,
        volumes=None,
        **kwargs,
    ) -> Container:
        """
        Start a Docker container from an image with a given name, environment variables, ports, and volumes.
        """
        resource_inputs = locals()
        del resource_inputs["self"]

        try:
            logging.info(
                f"Attempting to start container '{name}' using image '{image}'."
            )
            container = self.client.containers.run(
                image,
                name=name,
                detach=True,
                environment=env_vars,
                command=command,
                ports=ports,
                volumes=volumes,
                labels={
                    "launchflow_managed": "true",
                    "resource_inputs_hash": hash_resource_inputs(resource_inputs),
                },
                **kwargs,
            )
            logging.info(f"Container '{name}' started successfully.")
            return container
        except ImageNotFound:
            logging.warning(f"Image '{image}' not found. Attempting to pull image.")
            self.pull_image(image)
            return self.start_container(name, image, env_vars, ports, volumes, **kwargs)
        except APIError as e:
            logging.error(
                f"Server returned error when trying to start container '{name}': {e}"
            )

            # If the port is already in use, raise a custom exception to trigger a retry
            if "port is already allocated" in (error_message := str(e.explanation)):
                raise PortAlreadyAllocatedError(message=error_message) from e
            return None

    def stop_container(self, name_or_id: str):
        """
        Stop a Docker container by name or id.
        """
        try:
            container = self.get_container(name_or_id)
            if container:
                logging.info(f"Stopping container '{name_or_id}'.")
                container.stop()
                logging.info(f"Container '{name_or_id}' stopped successfully.")
        except NotFound:
            logging.warning(f"No container with name '{name_or_id}' to stop.")
        except APIError as e:
            logging.error(
                f"Server returned error when trying to stop container '{name_or_id}': {e}"
            )

    def remove_container(self, name_or_id: str, force=False):
        """
        Remove a Docker container by name or id. Can be forced to remove running containers.
        """
        try:
            container = self.get_container(name_or_id)
            if container:
                logging.info(f"Removing container '{name_or_id}'.")
                container.remove(force=force)
                logging.info(f"Container '{name_or_id}' removed successfully.")
        except NotFound:
            logging.warning(f"No container with name '{name_or_id}' to remove.")
        except APIError as e:
            logging.error(
                f"Server returned error when trying to remove container '{name_or_id}': {e}"
            )

    def pull_image(self, image: str) -> Image:
        """
        Pull a Docker image by name.
        """
        try:
            pulled_image = self.client.images.pull(image)
            logging.info(f"Image '{image}' pulled successfully.")
            return pulled_image
        except APIError as e:
            logging.error(
                f"Server returned error when trying to pull image '{image}': {e}"
            )
            return None

    def build_and_push_image(self, config):
        """
        Build and push a Docker image according to the provided config.
        This function is not fully implemented as it requires additional config details.
        """
        logging.warning("The build_and_push_image method is not yet implemented.")
        pass


# Example usage of DockerClient
if __name__ == "__main__":
    docker_client = DockerClient()

    env_vars = {
        "POSTGRES_USER": "user",
        "POSTGRES_PASSWORD": "password",
        "POSTGRES_DB": "mydb",
    }
    port_bindings = {"5432/tcp": 5433}  # Port mapping from container to host
    volumes = {
        "/local/path/to/data": {"bind": "/var/lib/postgresql/data", "mode": "rw"}
    }

    # docker_client.stop_container("my_postgres_container")

    # docker_client.remove_container("my_postgres_container")

    container = docker_client.start_container(
        name="my_postgres_container",
        image="postgres",
        env_vars=env_vars,
        ports=port_bindings,
        volumes=volumes,
    )

    if container:
        print(f"Started Postgres container with ID: {container.id}")

    print(docker_client.list_containers())
