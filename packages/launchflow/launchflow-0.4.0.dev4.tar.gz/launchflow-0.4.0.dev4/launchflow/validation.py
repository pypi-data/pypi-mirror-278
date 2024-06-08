import re

from launchflow import exceptions

MAX_ENVIRONMENT_NAME_LENGTH = 15
MIN_ENVIRONMENT_NAME_LENGTH = 1
ENVIRONMENT_PATTERN = "^[a-z0-9-]+$"
RESERVED_ENVIRONMENT_NAMES = {
    "gcp",
    "aws",
    "azure",
    "local",
    "base",
    "default",
    "nix",
}


MIN_RESOURCE_NAME_LENGTH = 3
MAX_RESOURCE_NAME_LENGTH = 63
RESOURCE_PATTERN = "^[a-zA-Z0-9-_]+$"


MIN_SERVICE_NAME_LENGTH = 3
MAX_SERVICE_NAME_LENGTH = 63
SERVICE_PATTERN = "^[a-zA-Z0-9-_]+$"


def validate_environment_name(environment_name: str):
    if len(environment_name) > MAX_ENVIRONMENT_NAME_LENGTH:
        raise ValueError(
            f"Environment name must be at most {MAX_ENVIRONMENT_NAME_LENGTH} characters long"
        )
    if len(environment_name) < MIN_ENVIRONMENT_NAME_LENGTH:
        raise ValueError(
            f"Environment name must be at least {MIN_ENVIRONMENT_NAME_LENGTH} characters long"
        )
    if not re.match(ENVIRONMENT_PATTERN, environment_name):
        raise ValueError(f"Environment name must match pattern {ENVIRONMENT_PATTERN}")

    if environment_name in RESERVED_ENVIRONMENT_NAMES:
        raise ValueError(f"Environment name is reserved: {environment_name}")


def validate_resource_name(resource_name: str):
    if len(resource_name) > MAX_RESOURCE_NAME_LENGTH:
        raise exceptions.InvalidResourceName(
            f"Resource name must be at most {MAX_RESOURCE_NAME_LENGTH} characters long"
        )
    if len(resource_name) < MIN_RESOURCE_NAME_LENGTH:
        raise exceptions.InvalidResourceName(
            f"Resource name must be at least {MIN_RESOURCE_NAME_LENGTH} characters long"
        )
    if not re.match(RESOURCE_PATTERN, resource_name):
        raise exceptions.InvalidResourceName(
            f"Resource name must match pattern {RESOURCE_PATTERN}"
        )


def validate_service_name(service_name: str):
    if len(service_name) > MAX_SERVICE_NAME_LENGTH:
        raise exceptions.InvalidResourceName(
            f"Service name must be at most {MAX_SERVICE_NAME_LENGTH} characters long"
        )
    if len(service_name) < MIN_SERVICE_NAME_LENGTH:
        raise exceptions.InvalidResourceName(
            f"Service name must be at least {MIN_SERVICE_NAME_LENGTH} characters long"
        )
    if not re.match(SERVICE_PATTERN, service_name):
        raise exceptions.InvalidResourceName(
            f"Service name must match pattern {SERVICE_PATTERN}"
        )
