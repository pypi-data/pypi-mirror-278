from dataclasses import dataclass
from typing import Optional


@dataclass
class LaunchFlowServiceOperationInputs:
    deployment_id: str
    # LaunchFlow entity names
    project_name: str
    environment_name: str
    service_name: str
    notify_on_failure: bool = False


@dataclass
class GCPEnvironmentInputs:
    gcp_project_id: str
    gcp_default_region: str
    gcp_artifact_bucket: str
    gcp_service_account_email: str


@dataclass
class AWSCredentialsInputs:
    # Contains all information needed to assume an AWS role
    aws_account_id: str
    aws_external_role_id: str
    aws_iam_role_arn: str


@dataclass
class AWSEnvironmentInputs:
    # AWS creds fields
    credentials_info: AWSCredentialsInputs
    # AWS env fields
    aws_region: str
    aws_vpc_id: str
    aws_ecs_cluster_name: str
    aws_artifact_bucket: str


# TODO: move these out of common inputs
@dataclass
class GCPPromotionInputs:
    source_docker_image: str
    source_env_service_account_email: str
    source_env_region: str


@dataclass
class AWSPromotionInputs:
    source_docker_image: str
    source_env_region: str
    source_env_credentials: AWSCredentialsInputs


@dataclass
class DockerBuildInputs:
    source_tarball_bucket: Optional[str]
    source_tarball_path: Optional[str]
    dockerfile_path: Optional[str]
    local_source_dir: str


@dataclass
class AWSCredentialsInputs:
    # Contains all information needed to assume an AWS role
    aws_account_id: str
    aws_external_role_id: str
    aws_iam_role_arn: str
