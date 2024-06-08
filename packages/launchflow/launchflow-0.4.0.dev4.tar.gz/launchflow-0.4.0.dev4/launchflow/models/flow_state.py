import datetime
from typing import Any, Dict, List, Optional

# TODO: Move to dataclasses
from pydantic import BaseModel, Field

from launchflow.models.enums import (
    CloudProvider,
    EnvironmentStatus,
    EnvironmentType,
    ResourceProduct,
    ResourceStatus,
    ServiceProduct,
    ServiceStatus,
)


class _Entity(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime


class GCPEnvironmentConfig(BaseModel):
    project_id: Optional[str]
    default_region: str
    default_zone: str
    service_account_email: Optional[str]
    artifact_bucket: Optional[str]


class AWSEnvironmentConfig(BaseModel):
    account_id: str
    region: str
    iam_role_arn: Optional[str]
    vpc_id: Optional[str]
    ecs_cluster_name: Optional[str]
    artifact_bucket: Optional[str]


# TODO: Added name to this, might as well add name to everything?
class ResourceState(_Entity):
    name: str
    cloud_provider: Optional[CloudProvider]
    product: ResourceProduct
    status: ResourceStatus
    gcp_id: Optional[str] = None
    aws_arn: Optional[str] = None
    inputs: Optional[Dict[str, Any]] = None
    depends_on: List[str] = Field(default_factory=list)

    def to_dict(self):
        return self.model_dump(
            mode="json", exclude_defaults=True, exclude=["environments"]
        )


class ServiceState(_Entity):
    name: str
    cloud_provider: CloudProvider
    product: ServiceProduct
    status: ServiceStatus
    gcp_id: Optional[str] = None
    aws_arn: Optional[str] = None
    inputs: Optional[Dict[str, Any]] = None
    service_url: Optional[str] = None
    docker_image: Optional[str] = None

    def to_dict(self):
        return self.model_dump(mode="json", exclude_defaults=True)


# TODO: Maybe move env_name into the Environment model
class EnvironmentState(_Entity):
    environment_type: EnvironmentType
    gcp_config: Optional[GCPEnvironmentConfig] = None
    aws_config: Optional[AWSEnvironmentConfig] = None
    status: EnvironmentStatus = EnvironmentStatus.READY

    def to_dict(self):
        return self.model_dump(
            mode="json", exclude_defaults=True, exclude=["resources", "services"]
        )


class ProjectState(_Entity):
    name: str

    def to_dict(self):
        return self.model_dump(mode="json")
