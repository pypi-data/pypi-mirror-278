from typing import Union

from launchflow import exceptions
from launchflow.backend import GCSBackend, LaunchFlowBackend, LocalBackend


class BaseManager:
    def __init__(
        self,
        backend: Union[LocalBackend, LaunchFlowBackend, GCSBackend],
    ) -> None:
        self.backend = backend

    def set_launchflow_api_key(self, launchflow_api_key: str) -> None:
        if isinstance(self.backend, LaunchFlowBackend):
            self.backend.launchflow_api_key = launchflow_api_key
        else:
            raise exceptions.APIKeySetOnNonLaunchFlowBackend(self.backend)
