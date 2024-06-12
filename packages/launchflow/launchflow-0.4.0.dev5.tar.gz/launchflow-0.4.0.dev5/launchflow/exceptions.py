from typing import Any, List, Optional

from launchflow.utils import get_failure_text


class LaunchFlowException(Exception):
    def pretty_print(self):
        print(self)


class LaunchFlowRequestFailure(LaunchFlowException):
    def __init__(self, response) -> None:
        super().__init__(get_failure_text(response))
        self.status_code = response.status_code


class LaunchFlowOperationFailure(LaunchFlowException):
    def __init__(self, status_message: str) -> None:
        super().__init__(status_message)


class NoLaunchFlowCredentials(Exception):
    def __init__(self) -> None:
        super().__init__("No launchflow credentials found.")


class InvalidBackend(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CannotDefaultMultipleAccounts(Exception):
    def __init__(self, account_ids: List[str]) -> None:
        super().__init__(
            f"The lf://default backend cannot be used when you have multiple accounts. Please use a specific account id (e.g. lf://{account_ids[0]}).\n\nYou have access tothe following accounts: {account_ids}\n"
        )


# TODO: Move "potential fix" messsages into the server.
# Server should return a json payload with a message per client type, i.e.
# {status: 409, message: "Conflict...", fix: {"cli": "Run this command..."}}
# Use details to return the fix payload:
# details = {message: "...", fix: {"cli": "Run this command..."}}
class ResourceOutputsNotFound(Exception):
    def __init__(self, resource_name: str) -> None:
        super().__init__(
            f"Outputs for resource '{resource_name}' not found. "
            f"\n\nPotential Fix:\nRun `launchflow create` it.\n\n"
        )


class PermissionCannotReadOutputs(Exception):
    def __init__(self, resource_name: str, bucket_path: str) -> None:
        super().__init__(
            f"Permission denied reading outputs for resource '{resource_name}' please ensure you have access to read the bucket: {bucket_path}"
        )


class ForbiddenOutputs(Exception):
    def __init__(self, bucket_url) -> None:
        super().__init__(
            f"Failed to read outputs from bucket. Please ensure you have access at: {bucket_url}"
        )


class ProjectOrEnvironmentNotSet(Exception):
    def __init__(self, project: Optional[str], environment: Optional[str]) -> None:
        super().__init__(
            f"Project or environment name not set. Set the project and environment names using "
            f"launchflow.yaml or the environment variables LAUNCHFLOW_PROJECT and LAUNCHFLOW_ENVIRONMENT. "
            f"\n\nCurrent project: {project}\nCurrent environment: {environment}\n\n"
        )


class OperationNotStarted(Exception):
    def __init__(self, operation: str) -> None:
        super().__init__(f"Operation '{operation}' not started. ")


class OperationAlreadyStarted(Exception):
    def __init__(self, operation: str) -> None:
        super().__init__(
            f"Operation '{operation}' already started. "
            f"\n\nPotential Fix:\nRun `launchflow start` to start the operation.\n\n"
        )


class ResourceReplacementRequired(Exception):
    def __init__(self, resource_name: str) -> None:
        super().__init__(
            f"Resource '{resource_name}' already exists but the create operation "
            "requires replacement, which must be explicitly specified. "
        )


class ResourceProductMismatch(Exception):
    def __init__(self, existing_product: str, new_product: str) -> None:
        super().__init__(
            "Cannot change the product of an existing resource. Please delete the existing resource before creating a new one."
        )


class ServiceProductMismatch(Exception):
    def __init__(self, product: str, service: str) -> None:
        super().__init__(
            f"Product '{product}' does not match the product of service '{service}'."
        )


class ServiceProductEnvironmentTypeMismatch(Exception):
    def __init__(self, service: str, environment_type: str) -> None:
        super().__init__(
            f"Cannot deploy service '{service}' to environment of type '{environment_type}'."
        )


class GCPConfigNotFound(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(
            f"GCP configuration not found for environment '{environment_name}'. "
            "This environment is most likely an AWS environment."
        )


class AWSConfigNotFound(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(
            f"AWS configuration not found for environment '{environment_name}'. "
            "This environment hasn't been configured for AWS yet."
        )


class EnvironmentNotFound(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(
            f"Environment '{environment_name}' not found. Create the environment with `launchflow environments create {environment_name}`."
        )


class LaunchFlowProjectNotFound(Exception):
    def __init__(self, project_name: str) -> None:
        super().__init__(
            f"LaunchFlow project '{project_name}' not found. Create the project with `launchflow projects create {project_name}`."
        )


class ServiceNotFound(Exception):
    def __init__(self, service_name: str) -> None:
        super().__init__(f"Service '{service_name}' not found.")


class ResourceNotFound(Exception):
    def __init__(self, resource_name: str) -> None:
        super().__init__(f"Resource '{resource_name}' not found.")


class MultipleBillingAccounts(Exception):
    def __init__(self) -> None:
        super().__init__(
            "You have access to multiple billing accounts. This is currently not supported.",
        )


class NoBillingAccountAccess(Exception):
    def __init__(self) -> None:
        super().__init__(
            "You do not have access to a billing account. Ensure you have access to a billing account and try again.",
        )


class MultipleOrgs(Exception):
    def __init__(self) -> None:
        super().__init__(
            "You have access to multiple organizations. This is currently not supported.",
        )


class NoOrgs(Exception):
    def __init__(self) -> None:
        super().__init__(
            "You do not have access to any organizations. Ensure you have access to an organiztaion and try again."
        )


class TofuOutputFailure(Exception):
    def __init__(self) -> None:
        super().__init__("Tofu output failed")


class TofuApplyFailure(Exception):
    def __init__(self) -> None:
        super().__init__("Tofu apply failed")


class TofuInitFailure(Exception):
    def __init__(self) -> None:
        super().__init__("Tofu init failed")


class TofuImportFailure(Exception):
    def __init__(self) -> None:
        super().__init__("Tofu import failed")


class TofuDestroyFailure(Exception):
    def __init__(self) -> None:
        super().__init__("Tofu destroy failed")


class EntityLocked(Exception):
    def __init__(self, entity: str) -> None:
        super().__init__(
            f"Entity is locked (`{entity}`). Wait for the operation to complete."
        )


class LockMismatch(Exception):
    def __init__(self, entity: str) -> None:
        super().__init__(
            f"Cannot unlock an entity (`{entity}`) that you do not hold the lock for."
        )


class MissingGCPDependency(Exception):
    def __init__(self) -> None:
        super().__init__(
            "GCP dependencies are not installed. Install them with: `pip install launchflow[gcp]`"
        )


class MissingAWSDependency(Exception):
    def __init__(self) -> None:
        super().__init__(
            "AWS dependencies are not installed. Install them with: `pip install launchflow[aws]`"
        )


class MissingDockerDependency(Exception):
    def __init__(self, details: str = "") -> None:
        msg = "Docker is not installed."
        if details:
            msg += f" {details}"
        super().__init__(msg)


class LaunchFlowYamlNotFound(Exception):
    def __init__(self) -> None:
        super().__init__(
            "No launchflow.yaml could be found, please ensure you are in the correct directory."
        )


class LaunchFlowBackendRequired(Exception):
    def __init__(self) -> None:
        super().__init__("A LaunchFlow backend is required.")


# TODO: Add a link to documentation for setting up AWS credentials.
class NoAWSCredentialsFound(Exception):
    def __init__(self) -> None:
        super().__init__(
            "No AWS credentials found. Please ensure you have AWS credentials set up in your environment."
        )


class ExistingEnvironmentDifferentEnvironmentType(Exception):
    def __init__(self, environment_name: str, environment_type: str) -> None:
        super().__init__(
            f"Environment '{environment_name}' already exists with a different environment type '{environment_type}'."
        )


class ExistingEnvironmentDifferentCloudProvider(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(
            f"Environment '{environment_name}' already exists with a different cloud provider type."
        )


class ExistingEnvironmentDifferentGCPProject(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(
            f"Environment '{environment_name}' already exists with a different GCP project."
        )


class ExistingEnvironmentDifferentGCPBucket(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(
            f"Environment '{environment_name}' already exists with a different GCS artifact bucket."
        )


class ExistingEnvironmentDifferentGCPServiceAccount(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(
            f"Environment '{environment_name}' already exists with a different environment service account email."
        )


class GCPEnvironmentMissingServiceAccount(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(
            f"Environment '{environment_name}' does not have a service account set up."
        )


class FailedToDeleteEnvironment(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(f"Failed to delete environment '{environment_name}'.")


class GCSObjectNotFound(Exception):
    def __init__(self, bucket: str, prefix: str) -> None:
        super().__init__(
            f"GCS object not found in bucket '{bucket}' with prefix '{prefix}'."
        )


class ProjectStateNotFound(Exception):
    def __init__(self) -> None:
        super().__init__("Project state not found.")


class UploadSrcTarballFailed(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to upload source tar file")


class OpenTofuInstallFailure(Exception):
    def __init__(self) -> None:
        super().__init__("OpenTofu install failed.")


class EnvironmentNotReady(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(f"Environment '{environment_name}' is not ready.")


class ServiceStateMismatch(Exception):
    def __init__(self, service_name: str) -> None:
        super().__init__(
            f"Service '{service_name}' was updated before changes were approved, please rerun the command to deploy the service."
        )


class InvalidResourceName(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class APIKeySetOnNonLaunchFlowBackend(Exception):
    def __init__(self, backend: Any) -> None:
        super().__init__(
            f"Cannot set launchflow_api_key on non-LaunchFlowBackend. You are currently using {backend}."
        )


class DuplicateResourceProductMismatch(Exception):
    def __init__(
        self, resource_name: str, existing_product: str, new_product: str
    ) -> None:
        super().__init__(
            f"Resource `{resource_name}` was defined twice as different resource types. Existing type: {existing_product}, new type: {new_product}."
        )


class ServiceIsPending(Exception):
    def __init__(self, service_name: str) -> None:
        super().__init__(
            f"Service '{service_name}' is pending, please wait for it to complete then try again."
        )


class ServiceNotReady(Exception):
    def __init__(self, service_name: str) -> None:
        super().__init__(
            f"Service '{service_name}' is not in a ready state, please wait if its pending or fix the service if it's failed."
        )


class EnvironmentNotEmpty(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(
            f"Environment '{environment_name}' is not empty. Please delete all resources and services before deleting the environment."
            "You can list and delete all resources / services with the following command:"
            "\n\n"
            f"    $ launchflow destroy {environment_name}"
            "\n\n"
        )


class ServiceBuildDirectoryNotFound(Exception):
    def __init__(self, service_name: str, build_directory: str) -> None:
        super().__init__(
            f"Service '{service_name}' build directory '{build_directory}' not found."
        )


class ServiceDockerfileNotFound(Exception):
    def __init__(self, service_name: str, build_directory: str) -> None:
        super().__init__(
            f"Service '{service_name}' dockerfile not found at '{build_directory}'."
        )
