import sys
from typing import List, Optional

from launchflow import config
from launchflow.aws.ecs_fargate import ECSFargate
from launchflow.cli.ast_search import find_launchflow_services
from launchflow.cli.utils import import_from_string
from launchflow.config.launchflow_yaml import ServiceConfig
from launchflow.gcp.cloud_run import CloudRun
from launchflow.service import Service


def import_services_from_directory(scan_directory: str) -> List[Service]:
    service_import_strs = find_launchflow_services(scan_directory)
    sys.path.insert(0, "")
    services: List[Service] = []
    for service_str in service_import_strs:
        imported_service = import_from_string(service_str)
        if not isinstance(imported_service, Service):
            raise ValueError(f"Service {imported_service} is not a valid Service")
        services.append(imported_service)
    return services


def _get_service_infos(service_name: Optional[str]) -> List[ServiceConfig]:
    service_configs = config.list_service_configs()
    if service_name is None:
        return service_configs
    if service_name is not None:
        for service in service_configs:
            if service.name == service_name:
                return [service]
    return []


def import_services_from_config(
    service_name: Optional[str], environment_name: str
) -> List[Service]:
    service_infos = _get_service_infos(service_name)
    services: List[Service] = []
    service_names = set()
    # Load services from the yaml config
    for service_info in service_infos:
        service_names.add(service_info.name)
        product_config = service_info.product_configs.get("base")
        env_config = service_info.product_configs.get(environment_name)
        if product_config is not None and env_config is not None:
            product_config.merge(env_config)
        elif env_config is not None:
            product_config = env_config
        if service_info.product == "gcp_cloud_run":
            services.append(
                CloudRun(
                    name=service_info.name,
                    dockerfile=service_info.dockerfile,
                    build_directory=service_info.build_directory,
                    build_ignore=service_info.build_ignore,
                    region=product_config.region if product_config else None,
                    cpu=product_config.cpu if product_config else None,
                    memory=product_config.memory if product_config else None,
                    port=product_config.port if product_config else None,
                    publicly_accessible=(
                        product_config.publicly_accessible if product_config else None
                    ),
                    min_instance_count=(
                        product_config.min_instance_count if product_config else None
                    ),
                    max_instance_count=(
                        product_config.max_instance_count if product_config else None
                    ),
                    max_instance_request_concurrency=(
                        product_config.max_instance_request_concurrency
                        if product_config
                        else None
                    ),
                    invokers=(product_config.invokers if product_config else None),
                    custom_audiences=(
                        product_config.custom_audiences if product_config else None
                    ),
                    ingress=product_config.ingress if product_config else None,
                )
            )
        elif service_info.product == "aws_ecs_fargate":
            services.append(
                ECSFargate(
                    name=service_info.name,
                    dockerfile=service_info.dockerfile,
                    build_directory=service_info.build_directory,
                    build_ignore=service_info.build_ignore,
                )
            )
        else:
            raise NotImplementedError(
                f"Product {service_info.product} is not supported yet."
            )

    return services
