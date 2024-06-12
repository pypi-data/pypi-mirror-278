from enum import Enum
from typing import Optional


class CloudProvider(str, Enum):
    GCP = "gcp"
    AWS = "aws"


class ResourceProduct(str, Enum):
    # GCP product types
    GCP_SQL_POSTGRES = "gcp_sql_postgres"
    GCP_SQL_USER = "gcp_sql_user"
    GCP_SQL_DATABASE = "gcp_sql_database"
    GCP_PUBSUB_TOPIC = "gcp_pubsub_topic"
    GCP_PUBSUB_SUBSCRIPTION = "gcp_pubsub_subscription"
    GCP_STORAGE_BUCKET = "gcp_storage_bucket"
    GCP_BIGQUERY_DATASET = "gcp_bigquery_dataset"
    GCP_MEMORYSTORE_REDIS = "gcp_memorystore_redis"
    GCP_COMPUTE_ENGINE = "gcp_compute_engine"
    GCP_SECRET_MANAGER_SECRET = "gcp_secret_manager_secret"
    GCP_LAUNCHFLOW_CLOUD_RELEASER = "gcp_launchflow_cloud_releaser"
    GCP_CLOUD_TASKS_QUEUE = "gcp_cloud_tasks_queue"
    # AWS product types
    AWS_RDS_POSTGRES = "aws_rds_postgres"
    AWS_ELASTICACHE_REDIS = "aws_elasticache_redis"
    AWS_EC2 = "aws_ec2"
    AWS_SQS_QUEUE = "aws_sqs_queue"
    AWS_S3_BUCKET = "aws_s3_bucket"
    AWS_SECRETS_MANAGER_SECRET = "aws_secrets_manager_secret"
    # Local product types
    LOCAL_DOCKER = "local_docker"

    def cloud_provider(self) -> Optional[CloudProvider]:
        if self.name.startswith("GCP"):
            return CloudProvider.GCP
        elif self.name.startswith("AWS"):
            return CloudProvider.AWS
        elif self.name.startswith("LOCAL"):
            return None
        else:
            raise NotImplementedError(
                f"Product type {self.name} could not be mapped to a cloud provider."
            )


class ServiceProduct(str, Enum):
    # GCP product types
    GCP_CLOUD_RUN = "gcp_cloud_run"
    # AWS product types
    AWS_ECS_FARGATE = "aws_ecs_fargate"

    def cloud_provider(self):
        if self.name.startswith("GCP"):
            return CloudProvider.GCP
        elif self.name.startswith("AWS"):
            return CloudProvider.AWS


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class EnvironmentStatus(str, Enum):
    READY = "ready"
    CREATE_FAILED = "create_failed"
    DELETE_FAILED = "delete_failed"
    CREATING = "creating"
    DELETING = "deleting"


class ResourceStatus(str, Enum):
    READY = "ready"
    CREATE_FAILED = "create_failed"
    DELETE_FAILED = "delete_failed"
    UPDATE_FAILED = "update_failed"
    CREATING = "creating"
    DELETING = "deleting"
    UPDATING = "updating"


class ServiceStatus(str, Enum):
    READY = "ready"
    DEPLOY_FAILED = "deploy_failed"
    DELETE_FAILED = "delete_failed"
    PROMOTE_FAILED = "promote_failed"
    DEPLOYING = "deploying"
    DELETING = "deleting"
    PROMOTING = "promoting"

    def is_pending(self):
        return self in [
            ServiceStatus.DEPLOYING,
            ServiceStatus.DELETING,
            ServiceStatus.PROMOTING,
        ]
