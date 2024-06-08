from dataclasses import dataclass
from typing import List

from launchflow.models.enums import ServiceProduct
from launchflow.node import Node, Outputs


@dataclass
class ServiceOutputs(Outputs):
    service_url: str
    docker_image: str


class Service(Node):
    def __init__(
        self,
        name: str,
        product: ServiceProduct,
        dockerfile: str = "Dockerfile",
        build_directory: str = ".",
        build_ignore: List[str] = [],  # type: ignore
    ) -> None:
        self.name = name
        self.product = product
        self._dockerfile = dockerfile
        self._build_directory = build_directory
        self._build_ignore = build_ignore

    def outputs(self) -> ServiceOutputs:
        raise NotImplementedError

    async def outputs_async(self) -> ServiceOutputs:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def __eq__(self, value: "Service") -> bool:
        return (
            isinstance(value, Service)
            and value.name == self.name
            and value.product == self.product
            and value.inputs() == self.inputs()
            and value._dockerfile == self._dockerfile
            and value._build_directory == self._build_directory
            and value._build_ignore == self._build_ignore
        )
