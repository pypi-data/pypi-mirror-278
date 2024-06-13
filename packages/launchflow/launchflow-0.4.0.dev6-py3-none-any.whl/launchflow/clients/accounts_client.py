from typing import Optional

import httpx

from launchflow.clients.response_schemas import AccountResponse
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure


class AccountsSyncClient:
    def __init__(
        self,
        http_client: httpx.Client,
        service_address: str,
        api_key: Optional[str] = None,
    ):
        self.http_client = http_client
        self.url = f"{config.get_launchflow_cloud_url()}/accounts"
        self._api_key = api_key

    @property
    def access_token(self):
        if self._api_key is not None:
            return self._api_key
        else:
            return config.get_access_token()

    def list(self):
        response = self.http_client.get(
            self.url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return [
            AccountResponse.model_validate(account)
            for account in response.json()["accounts"]
        ]

    def get(self, account_id: str):
        response = self.http_client.get(
            f"{self.url}/{account_id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return AccountResponse.model_validate(response.json())


class AccountsAsyncClient:
    def __init__(self, http_client: httpx.AsyncClient, api_key: Optional[str] = None):
        self.http_client = http_client
        self.url = f"{config.get_launchflow_cloud_url()}/accounts"
        self._api_key = api_key

    @property
    def access_token(self):
        if self._api_key is not None:
            return self._api_key
        else:
            return config.get_access_token()

    async def list(self):
        response = await self.http_client.get(
            self.url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return [
            AccountResponse.model_validate(account)
            for account in response.json()["accounts"]
        ]

    async def get(self, account_id: str):
        response = await self.http_client.get(
            f"{self.url}/{account_id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return AccountResponse.model_validate(response.json())
