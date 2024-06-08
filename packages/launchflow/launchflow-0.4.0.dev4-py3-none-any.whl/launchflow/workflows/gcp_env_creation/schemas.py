from typing import Optional

from pydantic import BaseModel

from launchflow.models.launchflow_uri import LaunchFlowURI


class GCPEnvironmentCreationInputs(BaseModel):
    launchflow_uri: LaunchFlowURI
    lock_id: str
    gcp_project_id: Optional[str] = None
    environment_service_account_email: Optional[str] = None
    org_name: Optional[str] = None
    artifact_bucket: Optional[str] = None


class GCPEnvironmentCreationOutputs(BaseModel):
    gcp_project_id: Optional[str]
    environment_service_account_email: Optional[str]
    artifact_bucket: Optional[str]
    success: bool
