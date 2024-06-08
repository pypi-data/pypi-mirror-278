import dataclasses
from typing import Dict

import launchflow
from launchflow.models.enums import EnvironmentType, ResourceProduct
from launchflow.models.flow_state import EnvironmentState
from launchflow.node import Inputs, Outputs
from launchflow.resource import Resource


@dataclasses.dataclass
class SecretManagerOutputs(Outputs):
    secret_name: str


@dataclasses.dataclass
class SecretManagerInputs(Inputs):
    pass


class SecretManagerSecret(Resource[SecretManagerOutputs]):
    """
    A Secret Manager secret resource.

    This creates the container for the secret and allows you to access the secret's value. You will need to manually add a value to the secret.

    Like all [Resources](/docs/concepts/resources), this class configures itself across multiple [Environments](/docs/concepts/environments).

    For more information see [the official documentation](https://cloud.google.com/secret-manager/docs/overview).

    ## Example Usage
    ```python
    import launchflow as lf

    # Automatically configures a SecretManager Secret in your GCP project
    api_key = lf.gcp.SecretManagerSecret("api-key")
    # Get the latest version of the secret
    value = secret.version()
    ```

    ## Utility Methods
    """

    def __init__(self, name: str) -> None:
        """Create a new Secret Manager secret resource.

        **Args**:
        - `name` (str): The name of the secret.
        """
        super().__init__(
            name=name,
            product=ResourceProduct.GCP_SECRET_MANAGER_SECRET,
            success_message=f"Set value of secret with `[cyan]launchflow secrets set --environment={launchflow.environment} {name} <VALUE>[/cyan]`",
        )
        self._cached_versions: Dict[str, bytes] = {}

    def inputs(self, environment_type: EnvironmentType) -> SecretManagerInputs:
        return SecretManagerInputs()

    def version(self, version: str = "latest", use_cache: bool = False) -> bytes:
        """Access a version of the secret.

        Args:
        - `version` (str): The version of the secret to access. Defaults to "latest".
        - `cache` (bool): Whether to cache the value of the secret in memory. Defaults to False.

        Returns:
        - The value of the secret as bytes.

        **Example usage:**

        ```python
        import launchflow as lf

        api_key = lf.gcp.SecretManagerSecret("api-key")
        secret = api_key.version()
        ```
        """
        if use_cache and version in self._cached_versions:
            return self._cached_versions[version]
        try:
            from google.cloud import secretmanager
        except ImportError:
            raise ImportError(
                "google-cloud-storage not found. "
                "You can install it with pip install launchflow[gcp]"
            )
        connection_info = self.outputs()
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(
            name=f"{connection_info.secret_name}/versions/{version}"
        )
        data = response.payload.data
        if use_cache:
            self._cached_versions[version] = data
        return data

    def add_version(self, payload: bytes):
        """Add a version of the secret.

        Args:
        - `payload` (str): The payload to add to the secret.

        **Example usage:**

        ```python
        import launchflow as lf

        api_key = lf.gcp.SecretManagerSecret("api-key")
        api_key.add_version(open("api-key.txt", "rb").read())
        ```
        """
        try:
            from google.cloud import secretmanager
        except ImportError:
            raise ImportError(
                "google-cloud-storage not found. "
                "You can install it with pip install launchflow[gcp]"
            )
        connection_info = self.outputs()
        client = secretmanager.SecretManagerServiceClient()
        client.add_secret_version(
            parent=connection_info.secret_name,
            payload=secretmanager.SecretPayload(data=payload),
        )

    def import_resource(self, environment: EnvironmentState) -> Dict[str, str]:
        return {
            "google_secret_manager_secret.secret": f"projects/{environment.gcp_config.project_id}/secrets/{self.name}",
        }
