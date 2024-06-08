import contextlib
from typing import Optional

from launchflow import config

from .client import LaunchFlowAsyncClient


@contextlib.asynccontextmanager
async def async_launchflow_client_ctx(
    launchflow_account_id: Optional[str],
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
):
    if base_url is None:
        base_url = config.settings.launch_service_address
    launchflow_async_client = LaunchFlowAsyncClient(
        base_url, launchflow_account_id=launchflow_account_id, api_key=api_key
    )
    try:
        yield launchflow_async_client
    finally:
        await launchflow_async_client.close()
