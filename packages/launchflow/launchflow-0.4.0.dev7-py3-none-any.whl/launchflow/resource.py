import dataclasses
import logging
import os
from typing import Dict, Generic, List, Optional, Set, TypeVar, get_args

import fsspec
import yaml

import launchflow
from launchflow import exceptions
from launchflow.cache import cache
from launchflow.config import config
from launchflow.managers.environment_manager import EnvironmentManager
from launchflow.models.enums import CloudProvider, EnvironmentType, ResourceProduct
from launchflow.models.flow_state import EnvironmentState
from launchflow.node import Inputs, Node, Outputs


@dataclasses.dataclass
class _ResourceURI:
    project_name: str
    environment_name: str
    product: ResourceProduct
    resource_name: str


# Step 1: Check if the outputs should be fetched from a mounted volume
def _load_outputs_from_mounted_volume(resource_uri: _ResourceURI):
    if config.env.outputs_path is not None:
        local_resource_path = os.path.join(
            config.env.outputs_path, resource_uri.resource_name, "latest"
        )
        if not os.path.exists(local_resource_path):
            logging.warning(f"Outputs for resource '{resource_uri}' not found on disk.")
            return None
        else:
            with open(local_resource_path) as f:
                return yaml.safe_load(f)


# Step 2: Check the cache for outputs, otherwise fetch from remote
def _load_outputs_from_cache(resource_uri: _ResourceURI):
    resource_outputs = cache.get_resource_outputs(
        resource_uri.project_name,
        resource_uri.environment_name,
        resource_uri.product.value,
        resource_uri.resource_name,
    )
    if resource_outputs is not None:
        logging.debug(f"Using cached resource outputs for {resource_uri}")
        return resource_outputs


# Step 3a: Load artifact bucket from environment variable
def _get_artifact_bucket_path_from_local(resource_uri: _ResourceURI):
    if config.env.artifact_bucket is not None:
        # If the bucket env var is set, we use it to build the outputs path
        resource_outputs_bucket_path = (
            f"{config.env.artifact_bucket}/resources/{resource_uri.resource_name}.yaml"
        )
        logging.debug(
            f"Using Resource outputs bucket path built from environment variable for {resource_uri}"
        )
    else:
        # If the bucket env var is not set, we check the cache or fetch from remote
        resource_outputs_bucket_path = cache.get_resource_outputs_bucket_path(
            resource_uri.project_name,
            resource_uri.environment_name,
            resource_uri.product.value,
            resource_uri.resource_name,
        )
    return resource_outputs_bucket_path


def _resource_path_from_env(resource_uri: _ResourceURI, env: EnvironmentState) -> str:
    if resource_uri.product.cloud_provider() == CloudProvider.GCP:
        if env.gcp_config is None:
            raise exceptions.GCPConfigNotFound(resource_uri.environment_name)
        bucket_url = f"gs://{env.gcp_config.artifact_bucket}"
    elif resource_uri.product.cloud_provider() == CloudProvider.AWS:
        if env.aws_config is None:
            raise exceptions.AWSConfigNotFound(resource_uri.environment_name)
        bucket_url = f"s3://{env.aws_config.artifact_bucket}"

    return f"{bucket_url}/resources/{resource_uri.resource_name}.yaml"


async def _get_artifact_bucket_from_remote_async(resource_uri: _ResourceURI):
    em = EnvironmentManager(
        project_name=resource_uri.project_name,
        environment_name=resource_uri.environment_name,
        backend=config.launchflow_yaml.backend,
    )
    env = await em.load_environment()
    return _resource_path_from_env(resource_uri, env)


def _get_artifact_bucket_from_remote_sync(resource_uri: _ResourceURI):
    em = EnvironmentManager(
        project_name=resource_uri.project_name,
        environment_name=resource_uri.environment_name,
        backend=config.launchflow_yaml.backend,
    )
    env = em.load_environment_sync()
    return _resource_path_from_env(resource_uri, env)


def _load_outputs_from_remote_bucket(
    resource_outputs_bucket_path: str, resource_name: str
):
    try:
        # TODO: Support async file reading (fsspec supports it)
        with fsspec.open(resource_outputs_bucket_path, mode="r") as file:
            resource_outputs = yaml.safe_load(file.read())
    except FileNotFoundError:
        raise exceptions.ResourceOutputsNotFound(resource_name)
    except PermissionError:
        raise exceptions.PermissionCannotReadOutputs(
            resource_name=resource_name, bucket_path=resource_outputs_bucket_path
        )
    except Exception as e:
        if resource_outputs_bucket_path.startswith("gs://"):
            bucket_name = resource_outputs_bucket_path.removeprefix("gs://").split("/")[
                0
            ]
            bucket_url = (
                f"https://console.cloud.google.com/storage/browser/{bucket_name}"
            )
        else:
            bucket_name = resource_outputs_bucket_path.removeprefix("s3://").split("/")[
                0
            ]
            bucket_url = f"https://s3.console.aws.amazon.com/s3/buckets/{bucket_name}"
        raise exceptions.ForbiddenOutputs(bucket_url) from e

    return resource_outputs


T = TypeVar("T", bound=Outputs)


class Resource(Node, Generic[T]):
    def __init__(
        self,
        name: str,
        product: ResourceProduct,
        replacement_arguments: Optional[Set[str]] = None,
        depends_on: Optional[List["Resource"]] = None,
        success_message: Optional[str] = None,
    ):
        self.name = name
        self.product = product

        if depends_on is None:
            depends_on = []
        self.depends_on = depends_on
        if replacement_arguments is None:
            replacement_arguments = set()
        self.replacement_arguments = replacement_arguments
        # This line extracts the type argument from the Generic base
        self._outputs_type: T = get_args(self.__class__.__orig_bases__[0])[0]
        self._success_message = success_message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def __eq__(self, value: "Resource") -> bool:
        return (
            isinstance(value, Resource)
            and value.name == self.name
            and value.product == self.product
            # TODO: Determine a better way to compare the inputs
            # Right now, we have to set the environment type to None which will
            # probably cause issues in the future
            and value.inputs(None) == self.inputs(None)
            and value._outputs_type == self._outputs_type
            and value._success_message == self._success_message
        )

    def inputs(self, environment_type: EnvironmentType) -> Inputs:
        raise NotImplementedError

    async def inputs_async(self, environment_type: EnvironmentType) -> Inputs:
        raise NotImplementedError

    def import_resource(self, environment: EnvironmentState) -> Dict[str, str]:
        """Returns a mapping from the resource name to the import string.

        TODO: this is very tofu specific right now, we should make it more generic
        """
        raise NotImplementedError(
            f"Importing is currently not support for resource type: {self.__class__.__name__}"
        )

    def outputs(self) -> T:
        """
        Synchronously connect to the resource by fetching its outputs.
        """
        project_name = launchflow.project
        environment_name = launchflow.environment
        resource_uri = _ResourceURI(
            project_name, environment_name, self.product, self.name
        )
        # Load outputs from mounted volume
        resource_outputs = _load_outputs_from_mounted_volume(resource_uri)
        if resource_outputs:
            return self._outputs_type(**resource_outputs)
        # Load outputs from cache
        resource_outputs = _load_outputs_from_cache(resource_uri)
        if resource_outputs:
            return self._outputs_type(**resource_outputs)

        # Load outputs from remote bucket
        artifact_bucket_path = _get_artifact_bucket_path_from_local(resource_uri)
        if artifact_bucket_path is None:
            artifact_bucket_path = _get_artifact_bucket_from_remote_sync(resource_uri)

        resource_outputs = _load_outputs_from_remote_bucket(
            artifact_bucket_path, resource_uri.resource_name
        )
        cache.set_resource_outputs(
            resource_uri.project_name,
            resource_uri.environment_name,
            resource_uri.product,
            resource_uri.resource_name,
            resource_outputs,
        )
        return self._outputs_type(**resource_outputs)

    async def outputs_async(self) -> T:
        """
        Asynchronously connect to the resource by fetching its outputs.
        """

        project_name = launchflow.project
        environment_name = launchflow.environment
        resource_uri = _ResourceURI(
            project_name, environment_name, self.product, self.name
        )
        # Load outputs from mounted volume
        resource_outputs = _load_outputs_from_mounted_volume(resource_uri)
        if resource_outputs:
            return self._outputs_type(**resource_outputs)

        # Load outputs from cache
        resource_outputs = _load_outputs_from_cache(resource_uri)
        if resource_outputs:
            logging.debug(f"Loaded outputs from cache for {resource_uri}")
            return self._outputs_type(**resource_outputs)
        logging.debug(f"No outputs found in cache for {resource_uri}")

        # Load outputs from remote bucket
        artifact_bucket_path = _get_artifact_bucket_path_from_local(resource_uri)
        if artifact_bucket_path is None:
            artifact_bucket_path = await _get_artifact_bucket_from_remote_async(
                resource_uri
            )

        resource_outputs = _load_outputs_from_remote_bucket(
            artifact_bucket_path, resource_uri.resource_name
        )
        cache.set_resource_outputs(
            resource_uri.project_name,
            resource_uri.environment_name,
            resource_uri.product.value,
            resource_uri.resource_name,
            resource_outputs,
        )
        return self._outputs_type(**resource_outputs)
