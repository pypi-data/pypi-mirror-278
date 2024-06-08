import dataclasses
from typing import Optional

from launchflow import config
from launchflow.config.launchflow_yaml import (
    GCSBackend,
    LaunchFlowBackend,
    LocalBackend,
)


@dataclasses.dataclass
class LaunchFlowURI:
    project_name: str
    environment_name: str
    resource_name: Optional[str] = None
    service_name: Optional[str] = None

    def __post_init__(self):
        if self.resource_name and self.service_name:
            raise ValueError("resource_name and service_name cannot be used together")

    # TODO: move this method to the Manager classes and let them use their own backend
    def tf_state_prefix(self, lock_id: str, module: Optional[str] = None) -> str:
        suffix = ""
        if self.resource_name:
            suffix = f"/resources/{self.resource_name}"
        elif self.service_name:
            suffix = f"/services/{self.service_name}"
        else:
            suffix = ""
        if isinstance(config.launchflow_yaml.backend, LaunchFlowBackend):
            suffix = f"{suffix}/tofu-state"
        if module is not None:
            suffix = f"{suffix}/{module}"
        if isinstance(config.launchflow_yaml.backend, LocalBackend):
            state_prefix = f"{config.launchflow_yaml.backend.path}/{self.project_name}/{self.environment_name}{suffix}"
        elif isinstance(config.launchflow_yaml.backend, GCSBackend):
            state_prefix = f"{config.launchflow_yaml.backend.prefix}/{self.project_name}/{self.environment_name}{suffix}"
        elif isinstance(config.launchflow_yaml.backend, LaunchFlowBackend):
            # TODO: it's not great that we have to set the lock ID here, but otherwise the tf appply stuff needs
            # to be more aware of the backend.
            state_prefix = f"{self.project_name}/environments/{self.environment_name}{suffix}?lock_id={lock_id}&account_id={config.launchflow_yaml.backend.get_launchflow_account_id()}"
        else:
            raise NotImplementedError(
                f"Unsupported backend: {config.launchflow_yaml.backend}"
            )
        return state_prefix
