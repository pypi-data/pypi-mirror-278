from typing import Dict, Optional

import httpx

from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.models.flow_state import ResourceState


class ResourcesSyncClient:
    def __init__(
        self,
        http_client: httpx.Client,
        launchflow_account_id: str,
        api_key: Optional[str] = None,
    ):
        self.http_client = http_client
        self._launchflow_account_id = launchflow_account_id
        self._api_key = api_key

    @property
    def access_token(self):
        if self._api_key is not None:
            return self._api_key
        else:
            return config.get_access_token()

    def base_url(self, project_name: str, environment_name: str) -> str:
        return f"{config.settings.launch_service_address}/projects/{project_name}/environments/{environment_name}/resources"

    def get(
        self,
        project_name: str,
        environment_name: str,
        resource_name: str,
    ):
        url = f"{self.base_url(project_name, environment_name)}/{resource_name}?account_id={self._launchflow_account_id}"
        response = self.http_client.get(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)

        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)

        return ResourceState.model_validate(response.json())


class ResourcesAsyncClient:
    def __init__(
        self,
        http_client: httpx.AsyncClient,
        base_url: str,
        launchflow_account_id: str,
        api_key: Optional[str] = None,
    ):
        self.http_client = http_client
        self._base_url = base_url
        self._api_key = api_key
        self._launchflow_account_id = launchflow_account_id

    @property
    def access_token(self):
        if self._api_key is not None:
            return self._api_key
        else:
            return config.get_access_token()

    def base_url(self, project_name: str, environment_name: str) -> str:
        return f"{self._base_url}/v1/projects/{project_name}/environments/{environment_name}/resources"

    async def save(
        self,
        project_name: str,
        environment_name: str,
        resource_name: str,
        lock_id: str,
        flow_state: ResourceState,
    ):
        response = await self.http_client.post(
            f"{self.base_url(project_name, environment_name)}/{resource_name}?lock_id={lock_id}&account_id={self._launchflow_account_id}",
            json=flow_state.to_dict(),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return ResourceState.model_validate(response.json())

    async def get(
        self,
        project_name: str,
        environment_name: str,
        resource_name: str,
    ):
        url = f"{self.base_url(project_name, environment_name)}/{resource_name}?account_id={self._launchflow_account_id}"
        response = await self.http_client.get(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)

        return ResourceState.model_validate(response.json())

    async def list(
        self, project_name: str, environment_name: str
    ) -> Dict[str, ResourceState]:
        url = f"{self.base_url(project_name, environment_name)}?account_id={self._launchflow_account_id}"
        response = await self.http_client.get(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return {
            name: ResourceState.model_validate(resource)
            for name, resource in response.json()["resources"].items()
        }

    async def delete(
        self, project_name: str, environment_name: str, resource_name: str, lock_id: str
    ):
        url = f"{self.base_url(project_name, environment_name)}/{resource_name}?lock_id={lock_id}&account_id={self._launchflow_account_id}"
        response = await self.http_client.delete(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
