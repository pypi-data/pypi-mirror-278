from dataclasses import dataclass
from typing import Dict, Optional, Union

from launchflow.config.launchflow_yaml import (
    GCSBackend,
    LaunchFlowBackend,
    LocalBackend,
)
from launchflow.models.flow_state import (
    AWSEnvironmentConfig,
    GCPEnvironmentConfig,
    ResourceState,
)
from launchflow.models.launchflow_uri import LaunchFlowURI


@dataclass
class ImportResourceTofuInputs:
    launchflow_uri: LaunchFlowURI
    backend: Union[LocalBackend, GCSBackend, LaunchFlowBackend]
    gcp_env_config: Optional[GCPEnvironmentConfig]
    aws_env_config: Optional[AWSEnvironmentConfig]
    # NOTE: This is the new state to commit not the current state
    resource: ResourceState
    imports: Dict[str, str]
    lock_id: str
    logs_dir: str


@dataclass
class ImportResourceTofuOutputs:
    gcp_id: Optional[str]
    aws_arn: Optional[str]
