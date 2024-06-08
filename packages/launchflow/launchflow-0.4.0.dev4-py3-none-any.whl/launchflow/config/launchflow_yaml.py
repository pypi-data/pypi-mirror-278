import os
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Literal, Optional, Union

import requests
import yaml

# Define the allowed product types
ProductType = Literal["gcp_cloud_run", "aws_ecs_fargate"]


@dataclass
class ProductConfig:
    pass

    def to_dict(self):
        to_ret = {}
        for k, v in asdict(self).items():
            if v is None:
                continue
            elif isinstance(v, list):
                to_ret[k] = ",".join(v)
            else:
                to_ret[k] = v
        return to_ret

    def merge(self, other):
        for k, v in asdict(other).items():
            if isinstance(v, list):
                curr = getattr(self, k)
                if curr is not None:
                    curr.extend(v)
                    setattr(self, k, curr)
                else:
                    setattr(self, k, v)
            elif v is not None:
                setattr(self, k, v)


@dataclass
class GcpCloudRunConfig(ProductConfig):
    region: Optional[str] = None
    cpu: Optional[int] = None
    memory: Optional[str] = None
    port: Optional[int] = None
    publicly_accessible: Optional[bool] = None
    min_instance_count: Optional[int] = None
    max_instance_count: Optional[int] = None
    max_instance_request_concurrency: Optional[int] = None
    invokers: Optional[List[str]] = None
    custom_audiences: Optional[List[str]] = None
    ingress: Optional[
        Literal[
            "INGRESS_TRAFFIC_ALL",
            "INGRESS_TRAFFIC_INTERNAL_ONLY",
            "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER",
        ]
    ] = None


@dataclass
class AwsEcsFargateConfig(ProductConfig):
    cpu: Optional[str] = None
    memory: Optional[int] = None


# Factory function to create product config instances based on type
def create_product_config(product_type: ProductType, config: Dict) -> ProductConfig:
    if product_type == "gcp_cloud_run":
        return GcpCloudRunConfig(**config)
    elif product_type == "aws_ecs_fargate":
        return AwsEcsFargateConfig(**config)
    else:
        raise ValueError(f"Unsupported product type: {product_type}")


@dataclass
class ServiceConfig:
    name: str
    product: ProductType
    product_configs: Dict[str, Union[GcpCloudRunConfig, AwsEcsFargateConfig]] = field(
        default_factory=dict
    )
    # The directory to run the build from
    build_directory: str = "."
    # Files to ignore uploading in the build context
    # This can be of the gitignore format
    build_ignore: List[str] = field(default_factory=list)
    # The path to the dockerfile. Defaults to the Docker file being in the build directory
    # This should be relative to the build directory
    dockerfile: str = "Dockerfile"
    domain_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        product_type = data.get("product")
        product_configs = data.get("product_configs", {})
        for env, config in product_configs.items():
            product_configs[env] = create_product_config(product_type, config)
        return cls(
            name=data.get("name", ""),
            product=product_type,
            product_configs=product_configs,
            build_directory=data.get("build_directory", "."),
            build_ignore=data.get("build_ignore", []),
            dockerfile=data.get("dockerfile", "Dockerfile"),
            domain_name=data.get("domain_name"),
        )

    def to_dict(self):
        to_return = {
            "name": self.name,
            "product": self.product,
        }
        if self.product_configs:
            configs = {}
            for env, config in self.product_configs.items():
                configs[env] = config.to_dict()
            to_return["product_configs"] = configs
        if self.build_directory:
            to_return["build_directory"] = self.build_directory
        if self.build_ignore:
            to_return["build_ignore"] = self.build_ignore
        if self.dockerfile:
            to_return["dockerfile"] = self.dockerfile
        if self.domain_name:
            to_return["domain_name"] = self.domain_name
        return to_return


class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


@dataclass
class LocalBackend:
    path: str


@dataclass
class LaunchFlowBackend:
    launchflow_url: str = "https://launch.launchflow.com"
    auth_url: str = "https://account.launchflow.com"
    launchflow_api_key: Optional[str] = None
    # TODO:allow this to be set via the cli too
    _launchflow_account_id: Optional[str] = None

    def get_launchflow_account_id(self):
        if self._launchflow_account_id is not None:
            return self._launchflow_account_id
        if self.launchflow_api_key is not None:
            response = requests.get(
                f"{self.auth_url}/accounts",
                headers={
                    "Authorization": f"Bearer {self.launchflow_api_key}",
                },
            )
            accounts = response.json()["accounts"]
            if len(accounts) > 1:
                raise ValueError(
                    "Multiple accounts found for api key. Please reach out to support@launchflow.com for help."
                )
            self.launchflow_account_id = accounts[0]["id"]
        else:
            raise ValueError(
                "No account ID found. Please set on with `launchflow config set-account acountXXXXX`"
            )


@dataclass
class GCSBackend:
    bucket: str
    # Defaults to an empty string, or no string
    prefix: str = ""


@dataclass
class LaunchFlowDotYaml:
    project: str
    environment: str
    path: str
    backend: Union[LocalBackend, LaunchFlowBackend, GCSBackend]
    services: List[ServiceConfig] = field(default_factory=list)

    @classmethod
    def load_from_cwd(
        cls,
        default_account_id: Optional[str],
        account_service_address: str,
        launch_service_address: str,
        start_path=".",
    ):
        file_path = find_launchflow_yaml(start_path)
        if file_path is None:
            raise FileNotFoundError("Could not find 'launchflow.yaml' file.")
        lf_yaml: LaunchFlowDotYaml = cls.load_from_file(file_path)
        if isinstance(lf_yaml.backend, LaunchFlowBackend):
            if lf_yaml.backend._launchflow_account_id is None:
                if default_account_id is not None:
                    lf_yaml.backend._launchflow_account_id = default_account_id
            if lf_yaml.backend.launchflow_url is None:
                lf_yaml.backend.launchflow_url = launch_service_address
            if lf_yaml.backend.auth_url is None:
                lf_yaml.backend.auth_url = account_service_address
        return lf_yaml

    @classmethod
    def load_from_file(cls, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
            project = data.get("project", "")
            environment = data.get("environment", "")
            backend = data.get("backend", {})
            services_data = data.get("services", [])
            services = [ServiceConfig.from_dict(service) for service in services_data]

        if len(backend) > 1:
            raise ValueError("Only one backend type is allowed in the configuration.")
        if "local" in backend:
            backend = LocalBackend(**backend["local"])
        elif "gcs" in backend:
            backend = GCSBackend(**backend["gcs"])
        elif "launchflow" in backend:
            backend = LaunchFlowBackend(**backend["launchflow"])
        elif len(backend) == 0:
            backend = LocalBackend(path="launchflow_state")
        else:
            raise ValueError(f"Unsupported backend type: {backend}")

        return cls(
            project=project,
            environment=environment,
            services=services,
            path=file_path,
            backend=backend,
        )

    def save_to_file(self, file_path: str):
        services_data = [service.to_dict() for service in self.services]

        if isinstance(LocalBackend, self.backend):
            backend_key = "local"
        elif isinstance(LaunchFlowBackend, self.backend):
            backend_key = "launchflow"
        else:
            raise ValueError(f"Unsupported backend type: {self.backend}")
        data = {
            "project": self.project,
            "environment": self.environment,
            "backend": {backend_key: asdict(self.backend)},
        }
        if services_data:
            data["services"] = services_data

        with open(file_path, "w") as file:
            yaml.dump(data, file, Dumper=Dumper)


def find_launchflow_yaml(start_path="."):
    current_path = os.path.abspath(start_path)

    while True:
        file_path = os.path.join(current_path, "launchflow.yaml")
        if os.path.isfile(file_path):
            return file_path

        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            break

        current_path = parent_path

    return None


launchflow_config = None


def load_launchflow_dot_yaml(
    default_account_id: str, account_service_address: str, launch_service_address: str
):
    global launchflow_config
    if launchflow_config is None:
        launchflow_config = LaunchFlowDotYaml.load_from_cwd(
            default_account_id, account_service_address, launch_service_address
        )
    return launchflow_config
