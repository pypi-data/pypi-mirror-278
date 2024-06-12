from dataclasses import dataclass
from typing import Union

from launchflow.backend import GCSBackend, LaunchFlowBackend, LocalBackend
from launchflow.models.launchflow_uri import LaunchFlowURI


@dataclass
class DestroyServiceInputs:
    launchflow_uri: LaunchFlowURI
    backend: Union[LocalBackend, GCSBackend, LaunchFlowBackend]
    lock_id: str
    logs_dir: str


@dataclass
class DestroyGCPServiceInputs(DestroyServiceInputs):
    gcp_project_id: str


@dataclass
class DestroyAWSServiceInputs(DestroyServiceInputs):
    aws_region: str
