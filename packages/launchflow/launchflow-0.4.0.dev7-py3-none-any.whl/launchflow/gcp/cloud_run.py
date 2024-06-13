from dataclasses import dataclass
from typing import List, Literal, Optional

from launchflow.gcp.service import GCPService
from launchflow.models.enums import ServiceProduct
from launchflow.node import Inputs


@dataclass
class CloudRunInputs(Inputs):
    # TODO: add tf var for this
    region: Optional[str]
    cpu: Optional[int]
    memory: Optional[str]
    port: Optional[int]
    publicly_accessible: Optional[bool]
    min_instance_count: Optional[int]
    max_instance_count: Optional[int]
    max_instance_request_concurrency: Optional[int]
    invokers: Optional[List[str]]
    custom_audiences: Optional[List[str]]
    ingress: Optional[
        Literal[
            "INGRESS_TRAFFIC_ALL",
            "INGRESS_TRAFFIC_INTERNAL_ONLY",
            "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER",
        ]
    ]


class CloudRun(GCPService):
    """A service hosted on GCP Cloud Run.

    ****Example usage:****
    ```python
    import launchflow as lf

    service = lf.gcp.CloudRun("my-service", cpu=4)
    ```

    **NOTE:** This will create the following infrastructure in your GCP project:
    - A [Cloud Run](https://cloud.google.com/run) service with the specified configuration.
    - A [Load Balancer](https://cloud.google.com/load-balancing) to route traffic to the service.
    - A [Cloud Build](https://cloud.google.com/build) trigger that builds and deploys the service.
    - An [Artifact Registry](https://cloud.google.com/artifact-registry) repository to store the service's Docker image.
    """

    def __init__(
        self,
        name: str,
        dockerfile: str = "Dockerfile",
        build_directory: str = ".",
        build_ignore: List[str] = [],
        region: Optional[str] = None,
        cpu: Optional[int] = None,
        memory: Optional[str] = None,
        port: Optional[int] = None,
        publicly_accessible: Optional[bool] = None,
        min_instance_count: Optional[int] = None,
        max_instance_count: Optional[int] = None,
        max_instance_request_concurrency: Optional[int] = None,
        invokers: Optional[List[str]] = None,
        custom_audiences: Optional[List[str]] = None,
        ingress: Optional[
            Literal[
                "INGRESS_TRAFFIC_ALL",
                "INGRESS_TRAFFIC_INTERNAL_ONLY",
                "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER",
            ]
        ] = None,
    ) -> None:
        """Creates a new Cloud Run service.

        **Args:**
        - `name`: The name of the service.
        - `build_directory`: The directory to build the service from. This should be a relative path from the project root where your `launchflow.yaml` is defined.
        - `dockerfile`: The Dockerfile to use for building the service. This should be a relative path from the `build_directory`.
        - `build_ignore`: A list of files to ignore when building the service. This can be in the same syntax you would use for a `.gitignore`.
        - `region`: The region to deploy the service to.
        - `cpu`: The number of CPUs to allocate to each instance of the service.
        - `memory`: The amount of memory to allocate to each instance of the service.
        - `port`: The port the service listens on.
        - `publicly_accessible`: Whether the service is publicly accessible. Defaults to True.
        - `min_instance_count`: The minimum number of instances to keep running.
        - `max_instance_count`: The maximum number of instances to run.
        - `max_instance_request_concurrency`: The maximum number of requests each instance can handle concurrently.
        - `invokers`: A list of invokers that can access the service.
        - `custom_audiences`: A list of custom audiences that can access the service. See: [https://cloud.google.com/run/docs/configuring/custom-audiences](https://cloud.google.com/run/docs/configuring/custom-audiences)
        - `ingress`: The ingress settings for the service. See: [https://cloud.google.com/run/docs/securing/ingress](https://cloud.google.com/run/docs/configuring/custom-audiences)
        """
        super().__init__(
            name=name,
            product=ServiceProduct.GCP_CLOUD_RUN,
            dockerfile=dockerfile,
            build_directory=build_directory,
            build_ignore=build_ignore,
        )
        self.region = region
        self.cpu = cpu
        self.memory = memory
        self.port = port
        self.publicly_accessible = publicly_accessible
        self.min_instance_count = min_instance_count
        self.max_instance_count = max_instance_count
        self.max_instance_request_concurrency = max_instance_request_concurrency
        self.invokers = invokers
        self.custom_audiences = custom_audiences
        self.ingress = ingress

    def inputs(self) -> CloudRunInputs:
        return CloudRunInputs(
            region=self.region,
            cpu=self.cpu,
            memory=self.memory,
            port=self.port,
            publicly_accessible=self.publicly_accessible,
            min_instance_count=self.min_instance_count,
            max_instance_count=self.max_instance_count,
            max_instance_request_concurrency=self.max_instance_request_concurrency,
            invokers=self.invokers,
            custom_audiences=self.custom_audiences,
            ingress=self.ingress,
        )
