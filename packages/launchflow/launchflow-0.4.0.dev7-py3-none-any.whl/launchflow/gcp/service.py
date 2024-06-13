from dataclasses import dataclass

from launchflow.service import Service, ServiceOutputs


@dataclass
class GCPServiceOutputs(ServiceOutputs):
    gcp_id: str


class GCPService(Service):
    def outputs(self) -> GCPServiceOutputs:
        raise NotImplementedError

    async def outputs_async(self) -> GCPServiceOutputs:
        raise NotImplementedError
