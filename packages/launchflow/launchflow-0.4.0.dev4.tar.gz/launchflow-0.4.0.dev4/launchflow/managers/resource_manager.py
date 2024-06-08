import asyncio
import os
import shutil
from typing import Optional, Union

import httpx
import yaml

from launchflow import exceptions
from launchflow.clients.resources_client import ResourcesAsyncClient
from launchflow.config.launchflow_yaml import (
    GCSBackend,
    LaunchFlowBackend,
    LocalBackend,
)
from launchflow.gcp_clients import get_storage_client, read_from_gcs, write_to_gcs
from launchflow.locks import GCSLock, LaunchFlowLock, LocalLock, Lock, LockOperation
from launchflow.managers.base import BaseManager
from launchflow.models.flow_state import ResourceState

# TODO: need to add tests to this file once it is all working


def _load_local_resource(path: str, name: str, project_name: str, env_name: str):
    base_resource_path = os.path.join(path, project_name, env_name, "resources", name)
    resource_path = os.path.join(base_resource_path, "flow.state")
    try:
        with open(resource_path, "r") as f:
            raw_resource = yaml.safe_load(f)
            resource = ResourceState.model_validate(raw_resource)
    except FileNotFoundError:
        raise exceptions.ResourceNotFound(name)
    return resource


async def _load_gcs_resource(
    bucket: str,
    prefix: str,
    project_name: str,
    environment_name: str,
    resource_name: str,
):
    env_path = os.path.join(
        prefix, project_name, environment_name, "resources", resource_name, "flow.state"
    )
    try:
        raw_state = yaml.safe_load(await read_from_gcs(bucket, env_path))
        state = ResourceState.model_validate(raw_state)
    except exceptions.GCSObjectNotFound:
        raise exceptions.ResourceNotFound(resource_name)
    return state


async def _load_launchflow_resource(
    project_name: str,
    environment_name: str,
    resource_name: str,
    launch_url: str,
    launchflow_account_id: str,
    launch_api_key: Optional[str],
) -> ResourceState:
    async with httpx.AsyncClient(timeout=60) as client:
        resources_client = ResourcesAsyncClient(
            client,
            base_url=launch_url,
            launchflow_account_id=launchflow_account_id,
            api_key=launch_api_key,
        )
        try:
            state = await resources_client.get(
                project_name, environment_name, resource_name
            )
        except exceptions.LaunchFlowRequestFailure as e:
            if e.status_code == 404:
                raise exceptions.ResourceNotFound(resource_name)
            raise e

        return state


def _save_local_resource(
    resource: ResourceState,
    path: str,
    project_name: str,
    environment_name: str,
    resource_name: str,
):
    resource_path = os.path.join(
        path, project_name, environment_name, "resources", resource_name
    )
    resource_file = os.path.join(resource_path, "flow.state")
    if not os.path.exists(resource_path):
        os.makedirs(resource_path)
    with open(resource_file, "w") as f:
        json_data = resource.to_dict()
        yaml.dump(json_data, f, sort_keys=False)


def _delete_local_resource(
    path: str, project_name: str, environment_name: str, resource_name: str
):
    resource_path = os.path.join(
        path, project_name, environment_name, "resources", resource_name
    )
    shutil.rmtree(resource_path)


async def _save_gcs_resource(
    resource: ResourceState,
    bucket: str,
    prefix: str,
    project_name: str,
    environment_name: str,
    resource_name: str,
):
    resource_path = os.path.join(
        prefix, project_name, environment_name, "resources", resource_name, "flow.state"
    )
    await write_to_gcs(
        bucket,
        resource_path,
        yaml.dump(resource.to_dict(), sort_keys=False),
    )


async def _save_launchflow_resource(
    resource: ResourceState,
    project_name: str,
    environment_name: str,
    resource_name: str,
    lock_id: str,
    launch_url: str,
    launchflow_account_id: str,
    launch_api_key: Optional[str],
):
    async with httpx.AsyncClient() as client:
        resource_client = ResourcesAsyncClient(
            client, launch_url, launchflow_account_id, launch_api_key
        )
        await resource_client.save(
            project_name=project_name,
            environment_name=environment_name,
            resource_name=resource_name,
            flow_state=resource,
            lock_id=lock_id,
        )


class ResourceManager(BaseManager):
    def __init__(
        self,
        project_name: str,
        environment_name: str,
        resource_name: str,
        backend: Union[LocalBackend, LaunchFlowBackend, GCSBackend],
    ) -> None:
        super().__init__(backend)
        self.project_name = project_name
        self.environment_name = environment_name
        self.resource_name = resource_name

    async def load_resource(self) -> ResourceState:
        if isinstance(self.backend, LocalBackend):
            return _load_local_resource(
                self.backend.path,
                self.resource_name,
                self.project_name,
                self.environment_name,
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            return await _load_launchflow_resource(
                self.project_name,
                self.environment_name,
                self.resource_name,
                self.backend.launchflow_url,
                self.backend.get_launchflow_account_id(),
                self.backend.launchflow_api_key,
            )
        elif isinstance(self.backend, GCSBackend):
            return await _load_gcs_resource(
                self.backend.bucket,
                self.backend.prefix,
                self.project_name,
                self.environment_name,
                self.resource_name,
            )

    async def save_resource(self, resource: ResourceState, lock_id: str):
        if isinstance(self.backend, LocalBackend):
            _save_local_resource(
                resource,
                self.backend.path,
                self.project_name,
                self.environment_name,
                self.resource_name,
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            await _save_launchflow_resource(
                resource,
                self.project_name,
                self.environment_name,
                self.resource_name,
                lock_id,
                self.backend.launchflow_url,
                self.backend.get_launchflow_account_id(),
                self.backend.launchflow_api_key,
            )
        elif isinstance(self.backend, GCSBackend):
            await _save_gcs_resource(
                resource,
                self.backend.bucket,
                self.backend.prefix,
                self.project_name,
                self.environment_name,
                self.resource_name,
            )

    async def delete_resource(self, lock_id: str):
        if isinstance(self.backend, LocalBackend):
            _delete_local_resource(
                self.backend.path,
                self.project_name,
                self.environment_name,
                self.resource_name,
            )
        elif isinstance(self.backend, GCSBackend):

            def delete_blobs():
                client = get_storage_client()
                blobs = client.list_blobs(
                    bucket_or_name=self.backend.bucket,
                    prefix=os.path.join(
                        self.backend.prefix,
                        self.project_name,
                        self.environment_name,
                        "resources",
                        self.resource_name,
                    )
                    # NOTE: the trailing slash is important here
                    # otherwise we would delete other resources with a similar prefix
                    + "/",
                )
                for blob in blobs:
                    blob.delete()

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, delete_blobs)
        elif isinstance(self.backend, LaunchFlowBackend):
            async with httpx.AsyncClient() as client:
                resource_client = ResourcesAsyncClient(
                    client,
                    self.backend.launchflow_url,
                    self.backend.get_launchflow_account_id(),
                    self.backend.launchflow_api_key,
                )
                await resource_client.delete(
                    project_name=self.project_name,
                    environment_name=self.environment_name,
                    resource_name=self.resource_name,
                    lock_id=lock_id,
                )
        else:
            raise NotImplementedError(f"Backend: {self.backend} not supported")

    async def lock_resource(self, operation: LockOperation) -> Lock:
        if isinstance(self.backend, LocalBackend):
            env_path = os.path.join(
                self.backend.path,
                self.project_name,
                self.environment_name,
                "resources",
                self.resource_name,
            )
            lock = LocalLock(env_path, operation)
        elif isinstance(self.backend, GCSBackend):
            lock = GCSLock(
                self.backend.bucket,
                self.backend.prefix,
                self.project_name,
                f"{self.environment_name}/resources/{self.resource_name}",
                operation,
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            lock = LaunchFlowLock(
                project=self.project_name,
                entity_path=f"environments/{self.environment_name}/resources/{self.resource_name}",
                operation=operation,
                launch_url=self.backend.launchflow_url,
                launchflow_account_id=self.backend.get_launchflow_account_id(),
                launchflow_api_key=self.backend.launchflow_api_key,
            )
        else:
            raise NotImplementedError(f"Backend: {self.backend} not supported")
        lock_info = await lock.acquire()
        lock.lock_info = lock_info
        return lock
