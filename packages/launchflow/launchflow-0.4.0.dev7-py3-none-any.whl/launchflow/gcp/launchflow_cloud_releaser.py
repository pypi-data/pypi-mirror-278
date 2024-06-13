import dataclasses

import httpx
import rich

import launchflow
from launchflow import exceptions
from launchflow.backend import LaunchFlowBackend
from launchflow.clients.accounts_client import AccountsSyncClient
from launchflow.clients.environments_client import EnvironmentsSyncClient
from launchflow.config import config
from launchflow.models.enums import EnvironmentType, ResourceProduct
from launchflow.node import Inputs, Outputs
from launchflow.resource import Resource


@dataclasses.dataclass
class LaunchFlowReleaserOutputs(Outputs):
    service_account_email: str


@dataclasses.dataclass
class LaunchFlowReleaserInputs(Inputs):
    launchflow_service_account: str


class LaunchFlowCloudReleaser(Resource[LaunchFlowReleaserOutputs]):
    def __init__(self, name: str = "launchflow-releaser") -> None:
        super().__init__(
            name=name, product=ResourceProduct.GCP_LAUNCHFLOW_CLOUD_RELEASER
        )

    def inputs(self, environment_type: EnvironmentType) -> LaunchFlowReleaserInputs:
        backend = config.launchflow_yaml.backend
        if not isinstance(backend, LaunchFlowBackend):
            raise exceptions.LaunchFlowBackendRequired()
        with httpx.Client() as http_client:
            client = AccountsSyncClient(
                http_client=http_client,
                service_address=backend.lf_cloud_url,
                api_key=backend.launchflow_api_key,
            )
            account = client.get(config.get_account_id())
        return LaunchFlowReleaserInputs(
            launchflow_service_account=account.gcp_service_account_email
        )

    async def connect_to_launchflow(self):
        outputs = await self.outputs_async()
        backend = config.launchflow_yaml.backend
        if not isinstance(backend, LaunchFlowBackend):
            raise exceptions.LaunchFlowBackendRequired()
        with httpx.Client() as http_client:
            client = EnvironmentsSyncClient(
                http_client=http_client,
                launch_service_url=backend.lf_cloud_url,
                api_key=backend.launchflow_api_key,
                launchflow_account_id=config.get_account_id(),
            )
            client.connect(
                project_name=launchflow.project,
                env_name=launchflow.environment,
                gcp_releaser_service_account=outputs.service_account_email,
            )
        rich.print(
            f"[green]Environment `{launchflow.environment}` is now connected to LaunchFlow Cloud![/green]"
        )
