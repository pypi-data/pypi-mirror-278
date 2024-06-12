import asyncio
import os
import shutil
from typing import Dict, Optional, Union

import httpx
import yaml

from launchflow import exceptions
from launchflow.backend import GCSBackend, LaunchFlowBackend, LocalBackend
from launchflow.clients.environments_client import (
    EnvironmentsAsyncClient,
    EnvironmentsSyncClient,
)
from launchflow.clients.resources_client import ResourcesAsyncClient
from launchflow.clients.services_client import ServicesAsyncClient
from launchflow.config import config
from launchflow.gcp_clients import (
    get_storage_client,
    read_from_gcs,
    read_from_gcs_sync,
    write_to_gcs,
)
from launchflow.locks import GCSLock, LaunchFlowLock, LocalLock, Lock, LockOperation
from launchflow.managers.base import BaseManager
from launchflow.managers.resource_manager import ResourceManager
from launchflow.managers.service_manager import ServiceManager
from launchflow.models.flow_state import EnvironmentState, ResourceState, ServiceState


def _load_local_environment(path: str, project_name: str, environment_name: str):
    base_env_path = os.path.join(path, project_name, environment_name)
    env_path = os.path.join(base_env_path, "flow.state")
    try:
        with open(env_path, "r") as f:
            raw_env = yaml.safe_load(f)
            env = EnvironmentState.model_validate(raw_env)
    except FileNotFoundError:
        raise exceptions.EnvironmentNotFound(environment_name)
    return env


async def _load_gcs_environment(
    bucket: str, prefix: str, project_name: str, environment_name: str
):
    try:
        env_path = os.path.join(prefix, project_name, environment_name, "flow.state")
        raw_state = yaml.safe_load(await read_from_gcs(bucket, env_path))
        state = EnvironmentState.model_validate(raw_state)
        return state
    except exceptions.GCSObjectNotFound:
        raise exceptions.EnvironmentNotFound(environment_name)


def _load_gcs_environment_sync(
    bucket: str, prefix: str, project_name: str, environment_name: str
):
    try:
        env_path = os.path.join(prefix, project_name, environment_name, "flow.state")
        raw_state = yaml.safe_load(read_from_gcs_sync(bucket, env_path))
        state = EnvironmentState.model_validate(raw_state)
        return state
    except exceptions.GCSObjectNotFound:
        raise exceptions.EnvironmentNotFound(environment_name)


async def _load_launchflow_environment(
    project_name: str,
    environment_name: str,
    launch_url: str,
    launchflow_account_id: str,
    launch_api_key: Optional[str] = None,
):
    async with httpx.AsyncClient(timeout=60) as client:
        environments_client = EnvironmentsAsyncClient(
            client, launch_url, launchflow_account_id, launch_api_key
        )
        try:
            state = await environments_client.get(project_name, environment_name)
        except exceptions.LaunchFlowRequestFailure as e:
            if e.status_code == 404:
                raise exceptions.EnvironmentNotFound(environment_name)
            raise e

        return state


def _load_launchflow_environment_sync(
    project_name: str,
    environment_name: str,
    launch_url: str,
    launchflow_account_id: str,
    launch_api_key: Optional[str] = None,
):
    with httpx.Client(timeout=60) as client:
        environments_client = EnvironmentsSyncClient(
            client, launch_url, launchflow_account_id, launch_api_key
        )
        try:
            state = environments_client.get(project_name, environment_name)
        except exceptions.LaunchFlowRequestFailure as e:
            if e.status_code == 404:
                raise exceptions.EnvironmentNotFound(environment_name)
            raise e

        return state


def _save_local_environment(
    environment: EnvironmentState, path: str, project_name: str, environment_name: str
):
    env_path = os.path.join(path, project_name, environment_name)
    if not os.path.exists(env_path):
        os.makedirs(env_path)
    with open(os.path.join(env_path, "flow.state"), "w") as f:
        json_data = environment.to_dict()
        yaml.dump(json_data, f, sort_keys=False)


async def _save_gcs_environment(
    environment: EnvironmentState,
    bucket: str,
    prefix: str,
    project_name: str,
    environment_name: str,
):
    env_path = os.path.join(prefix, project_name, environment_name, "flow.state")
    await write_to_gcs(
        bucket,
        env_path,
        yaml.dump(environment.to_dict(), sort_keys=False),
    )


async def _save_launchflow_environment(
    environment: EnvironmentState,
    project_name: str,
    environment_name: str,
    lock_id: str,
    launch_url: str,
    launchflow_account_id: str,
    launch_api_key: Optional[str],
):
    async with httpx.AsyncClient() as client:
        env_client = EnvironmentsAsyncClient(
            client, launch_url, launchflow_account_id, launch_api_key
        )
        await env_client.create(
            project_name=project_name,
            env_name=environment_name,
            environment=environment,
            lock_id=lock_id,
        )


def _list_resources_from_local_backend(
    backend: LocalBackend, project_name: str, environment_name: str
) -> Dict[str, ResourceState]:
    resources = {}
    resources_path = os.path.join(
        backend.path,
        project_name,
        environment_name,
        "resources",
    )
    if os.path.exists(resources_path):
        for dir in os.scandir(resources_path):
            if dir.is_dir():
                if os.path.exists(os.path.join(dir.path, "flow.state")):
                    resource_name = os.path.basename(dir.path)
                    resource_path = os.path.join(dir.path, "flow.state")
                    with open(resource_path, "r") as f:
                        resource = ResourceState.model_validate(yaml.safe_load(f))
                        resources[resource_name] = resource
    return resources


class EnvironmentManager(BaseManager):
    def __init__(
        self,
        project_name: str,
        environment_name: str,
        backend: Union[LocalBackend, LaunchFlowBackend, GCSBackend],
    ) -> None:
        super().__init__(backend)
        self.project_name = project_name
        self.environment_name = environment_name

    async def load_environment(self) -> EnvironmentState:
        if isinstance(self.backend, LocalBackend):
            return _load_local_environment(
                self.backend.path, self.project_name, self.environment_name
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            return await _load_launchflow_environment(
                self.project_name,
                self.environment_name,
                self.backend.lf_cloud_url,
                config.get_account_id(),
                self.backend.launchflow_api_key,
            )
        elif isinstance(self.backend, GCSBackend):
            return await _load_gcs_environment(
                self.backend.bucket,
                self.backend.prefix,
                self.project_name,
                self.environment_name,
            )

    def load_environment_sync(self) -> EnvironmentState:
        if isinstance(self.backend, LocalBackend):
            return _load_local_environment(
                self.backend.path, self.project_name, self.environment_name
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            return _load_launchflow_environment_sync(
                self.project_name,
                self.environment_name,
                self.backend.lf_cloud_url,
                config.get_account_id(),
                self.backend.launchflow_api_key,
            )
        elif isinstance(self.backend, GCSBackend):
            return _load_gcs_environment_sync(
                self.backend.bucket,
                self.backend.prefix,
                self.project_name,
                self.environment_name,
            )

    async def save_environment(self, environment: EnvironmentState, lock_id: str):
        if isinstance(self.backend, LocalBackend):
            _save_local_environment(
                environment, self.backend.path, self.project_name, self.environment_name
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            await _save_launchflow_environment(
                environment,
                self.project_name,
                self.environment_name,
                lock_id,
                self.backend.lf_cloud_url,
                config.get_account_id(),
                self.backend.launchflow_api_key,
            )
        elif isinstance(self.backend, GCSBackend):
            await _save_gcs_environment(
                environment,
                self.backend.bucket,
                self.backend.prefix,
                self.project_name,
                self.environment_name,
            )
        else:
            raise NotImplementedError("Only local backend is supported")

    def lock_environment(self, operation: LockOperation) -> Lock:
        if isinstance(self.backend, LocalBackend):
            env_path = os.path.join(
                self.backend.path, self.project_name, self.environment_name
            )
            return LocalLock(env_path, operation)
        elif isinstance(self.backend, GCSBackend):
            return GCSLock(
                self.backend.bucket,
                self.backend.prefix,
                self.project_name,
                self.environment_name,
                operation,
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            return LaunchFlowLock(
                project=self.project_name,
                entity_path=f"environments/{self.environment_name}",
                operation=operation,
                launch_url=self.backend.lf_cloud_url,
                launchflow_account_id=config.get_account_id(),
                launchflow_api_key=self.backend.launchflow_api_key,
            )
        else:
            raise NotImplementedError("Only local backend is supported")

    async def delete_environment(self, lock_id: str):
        if isinstance(self.backend, LocalBackend):
            shutil.rmtree(
                os.path.join(
                    self.backend.path, self.project_name, self.environment_name
                )
            )
        elif isinstance(self.backend, GCSBackend):

            def delete_blobs():
                client = get_storage_client()
                blobs = client.list_blobs(
                    bucket_or_name=self.backend.bucket,
                    prefix=os.path.join(
                        self.backend.prefix, self.project_name, self.environment_name
                    ),
                )
                for blob in blobs:
                    blob.delete()

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, delete_blobs)
        elif isinstance(self.backend, LaunchFlowBackend):
            async with httpx.AsyncClient() as client:
                env_client = EnvironmentsAsyncClient(
                    client,
                    self.backend.lf_cloud_url,
                    config.get_account_id(),
                    self.backend.launchflow_api_key,
                )
                await env_client.delete(
                    project_name=self.project_name,
                    env_name=self.environment_name,
                    lock_id=lock_id,
                )

    async def list_resources(self) -> Dict[str, ResourceState]:
        if isinstance(self.backend, LocalBackend):
            return _list_resources_from_local_backend(
                self.backend, self.project_name, self.environment_name
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            async with httpx.AsyncClient() as client:
                resource_client = ResourcesAsyncClient(
                    client,
                    self.backend.lf_cloud_url,
                    config.get_account_id(),
                    self.backend.launchflow_api_key,
                )
                resources = await resource_client.list(
                    project_name=self.project_name,
                    environment_name=self.environment_name,
                )
                return resources
        elif isinstance(self.backend, GCSBackend):
            resources = {}

            def read_blobs():
                gcs_client = get_storage_client()
                bucket = gcs_client.bucket(self.backend.bucket)
                prefix = os.path.join(
                    self.backend.prefix,
                    self.project_name,
                    self.environment_name,
                    "resources",
                )
                blobs = bucket.list_blobs(prefix=prefix)
                for blob in blobs:
                    relative_path = blob.name.replace(prefix + "/", "")
                    split_path = relative_path.split("/")
                    if relative_path.endswith("flow.state") and len(split_path) == 2:
                        resource_name = blob.name.split("/")[-2]
                        resource = ResourceState.model_validate(
                            yaml.safe_load(blob.download_as_string())
                        )
                        resources[resource_name] = resource
                return resources

            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, read_blobs)
        else:
            raise NotImplementedError(f"Unsupported backend: {self.backend}")

    async def list_docker_resources(self) -> Dict[str, ResourceState]:
        backend_path = os.path.join(
            os.path.dirname(config.launchflow_yaml.config_path), ".launchflow", "docker"
        )
        backend = LocalBackend(backend_path)
        return _list_resources_from_local_backend(
            backend, self.project_name, self.environment_name
        )

    async def list_services(self) -> Dict[str, ServiceState]:
        if isinstance(self.backend, LocalBackend):
            services = {}
            services_path = os.path.join(
                self.backend.path,
                self.project_name,
                self.environment_name,
                "services",
            )
            if os.path.exists(services_path):
                for dir in os.scandir(services_path):
                    if dir.is_dir():
                        if os.path.exists(os.path.join(dir.path, "flow.state")):
                            service_name = os.path.basename(dir.path)
                            service_path = os.path.join(dir.path, "flow.state")
                            with open(service_path, "r") as f:
                                service = ServiceState.model_validate(yaml.safe_load(f))
                                services[service_name] = service
            return services
        elif isinstance(self.backend, LaunchFlowBackend):
            async with httpx.AsyncClient() as client:
                services_client = ServicesAsyncClient(
                    client,
                    self.backend.lf_cloud_url,
                    config.get_account_id(),
                    self.backend.launchflow_api_key,
                )
                services = await services_client.list(
                    project_name=self.project_name,
                    environment_name=self.environment_name,
                )
                return services
        elif isinstance(self.backend, GCSBackend):
            services = {}

            def read_blobs():
                gcs_client = get_storage_client()
                bucket = gcs_client.bucket(self.backend.bucket)
                prefix = os.path.join(
                    self.backend.prefix,
                    self.project_name,
                    self.environment_name,
                    "services",
                )
                blobs = bucket.list_blobs(prefix=prefix)
                for blob in blobs:
                    relative_path = blob.name.replace(prefix + "/", "")
                    split_path = relative_path.split("/")
                    if relative_path.endswith("flow.state") and len(split_path) == 2:
                        service_name = blob.name.split("/")[-2]
                        service = ServiceState.model_validate(
                            yaml.safe_load(blob.download_as_string())
                        )
                        services[service_name] = service
                return services

            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, read_blobs)
        else:
            raise NotImplementedError("Unsupported backend: {self.backend}")

    def create_resource_manager(self, resource_name: str) -> ResourceManager:
        return ResourceManager(
            project_name=self.project_name,
            environment_name=self.environment_name,
            resource_name=resource_name,
            backend=self.backend,
        )

    def create_docker_resource_manager(self, resource_name: str) -> ResourceManager:
        backend_path = os.path.join(
            os.path.dirname(config.launchflow_yaml.config_path), ".launchflow", "docker"
        )
        return ResourceManager(
            project_name=self.project_name,
            environment_name=self.environment_name,
            resource_name=resource_name,
            backend=LocalBackend(backend_path),
        )

    def create_service_manager(self, service_name):
        return ServiceManager(
            project_name=self.project_name,
            environment_name=self.environment_name,
            service_name=service_name,
            backend=self.backend,
        )
