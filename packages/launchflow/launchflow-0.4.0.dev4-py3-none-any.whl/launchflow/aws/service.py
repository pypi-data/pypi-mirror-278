from dataclasses import dataclass

from launchflow.service import Service, ServiceOutputs


@dataclass
class AWSServiceOutputs(ServiceOutputs):
    aws_arn: str


class AWSService(Service):
    def outputs(self) -> AWSServiceOutputs:
        raise NotImplementedError

    async def outputs_async(self) -> AWSServiceOutputs:
        raise NotImplementedError
