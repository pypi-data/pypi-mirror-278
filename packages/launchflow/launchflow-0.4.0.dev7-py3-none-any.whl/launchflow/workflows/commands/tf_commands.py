import asyncio
import dataclasses
import importlib
import importlib.resources
import importlib.util
import json
import logging
import os
import shutil
from typing import Any, Dict, Optional, Union

from launchflow import exceptions
from launchflow.backend import GCSBackend, LaunchFlowBackend, LocalBackend
from launchflow.config import config
from launchflow.dependencies import opentofu
from launchflow.utils import logging_output

_GCS_BACKEND_TEMPLATE = """
terraform {
  backend "gcs" {
  }
}
"""

_LOCAL_BACKEND_TEMPLATE = """
terraform {
  backend "local" {
  }
}
"""

_LAUNCHFLOW_BACKEND_TEMPLATE = """
terraform {
  backend "http" {
  }
}
"""


def parse_value(value, type_info):
    if value is None:
        return None
    if type_info == "string":
        return str(value)
    elif type_info == "number":
        return float(value) if "." in str(value) else int(value)
    elif type_info == "bool":
        return bool(value)
    elif isinstance(type_info, list):
        type_category = type_info[0]
        if type_category == "list":
            element_type = type_info[1][1]
            return [parse_value(elem, element_type) for elem in value]
        elif type_category == "map":
            value_type = type_info[1]
            return {key: parse_value(val, value_type) for key, val in value.items()}
        elif type_category == "set":
            element_type = type_info[1][1]
            return {parse_value(elem, element_type) for elem in value}
        elif type_category == "object":
            properties = type_info[1]
            return {key: parse_value(value[key], properties[key]) for key in properties}
    return value


def parse_tf_outputs(tf_outputs_json: dict) -> Dict[str, Any]:
    parsed_outputs = {}
    for key, output in tf_outputs_json.items():
        value = output["value"]
        type_info = output["type"]
        parsed_value = parse_value(value, type_info)
        parsed_outputs[key] = parsed_value
    return parsed_outputs


@dataclasses.dataclass
class TFCommand:
    tf_module_dir: str
    backend: Union[LocalBackend, LaunchFlowBackend, GCSBackend]
    tf_state_prefix: str
    # The directory to write logs to, if not provided, logs will be written to stdout
    logging_dir: Optional[str] = None

    def initialize_working_dir(self, working_dir: str):
        # TODO(oss): maybe we should verify there is no existing backend definition
        # I think tf will fail there is, but might nice to have a better error message
        backed_config_path = os.path.join(working_dir, "backend.tf")
        with open(backed_config_path, "w") as f:
            if isinstance(self.backend, LocalBackend):
                f.write(_LOCAL_BACKEND_TEMPLATE)
            elif isinstance(self.backend, GCSBackend):
                f.write(_GCS_BACKEND_TEMPLATE)
            elif isinstance(self.backend, LaunchFlowBackend):
                f.write(_LAUNCHFLOW_BACKEND_TEMPLATE)
            else:
                raise ValueError(f"Unsupported backend type: {self.backend}")

        module_path = importlib.resources.files(
            f"launchflow.{self.tf_module_dir.replace('/', '.')}"
        )
        for file in module_path.iterdir():
            shutil.copy(file, working_dir)

    def tf_init_command(self) -> str:
        if isinstance(self.backend, LocalBackend):
            path = os.path.join(
                self.tf_state_prefix,
                "default.tfstate",
            )
            command_lines = [
                f"{opentofu.TOFU_PATH} init -reconfigure",
                f'-backend-config "path={os.path.abspath(path)}"',
            ]
        elif isinstance(self.backend, GCSBackend):
            command_lines = [
                f"{opentofu.TOFU_PATH} init -reconfigure",
                f'-backend-config "bucket={self.backend.bucket}"',
                f'-backend-config "prefix={self.tf_state_prefix}"',
            ]
        elif isinstance(self.backend, LaunchFlowBackend):
            auth_header = f'"Authorization" = "Bearer {config.get_access_token()}"'
            command_lines = [
                f"{opentofu.TOFU_PATH} init -reconfigure",
                f'-backend-config "address={self.backend.lf_cloud_url}/v1/projects/{self.tf_state_prefix}"',
                f"-backend-config 'headers={{{auth_header}}}'",
            ]
        else:
            raise ValueError(f"Unsupported backend type: {self.backend}")
        return " ".join(command_lines)

    async def run(self, working_dir: str):
        raise NotImplementedError("run method not implemented")

    def _var_flags(self):
        var_flags = []
        for key, value in self.tf_vars.items():
            if isinstance(value, list):
                value = json.dumps(value)
            if isinstance(value, dict):
                json_encoded_str = json.dumps(value).replace('"', '\\"')
                value = f"{json_encoded_str}"
            if isinstance(value, bool):
                value = str(value).lower()
            var_flags.append(f'-var "{key}={value}"')
        return var_flags


@dataclasses.dataclass
class TFDestroyCommand(TFCommand):
    tf_vars: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def tf_destroy_command(self) -> str:
        command_lines = [
            f"{opentofu.TOFU_PATH} destroy",
            "-auto-approve",
            "-input=false",
            *self._var_flags(),
        ]
        return " ".join(command_lines)

    async def run(self, working_dir: str):
        with logging_output(self.logging_dir) as f:
            self.initialize_working_dir(working_dir)

            # Run tofu init
            logging.info(f"Running tofu init command: {self.tf_init_command()}")
            proc = await asyncio.create_subprocess_shell(
                self.tf_init_command(),
                cwd=working_dir,
                # Stops the child process from receiving signals sent to the parent
                preexec_fn=os.setpgrp,
                stdout=f,
                stderr=f,
            )
            status_code = await proc.wait()
            if status_code != 0:
                raise exceptions.TofuInitFailure()

            # Run tofu destroy
            logging.info(f"Running tofu destroy command: {self.tf_destroy_command()}")
            proc = await asyncio.create_subprocess_shell(
                self.tf_destroy_command(),
                cwd=working_dir,
                # Stops the child process from receiving signals sent to the parent
                preexec_fn=os.setpgrp,
                stdout=f,
                stderr=f,
            )
            await proc.communicate()

            if proc.returncode != 0:
                raise exceptions.TofuDestroyFailure()

            return True


@dataclasses.dataclass
class TFApplyCommand(TFCommand):
    tf_vars: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def tf_apply_command(self) -> str:
        command_lines = [
            f"{opentofu.TOFU_PATH} apply",
            "-auto-approve",
            "-input=false",
            *self._var_flags(),
        ]
        return " ".join(command_lines)

    def tf_import_command(self, resource: str, resource_id: str) -> str:
        import_command = [
            f"{opentofu.TOFU_PATH} import",
            "-input=false",
            *self._var_flags(),
            resource,
            resource_id,
        ]
        return " ".join(import_command)

    async def import_resource(
        self,
        working_dir: str,
        resource: str,
        resource_id: str,
        drop_logs: bool = False,
    ):
        self.initialize_working_dir(working_dir)

        with logging_output(self.logging_dir, drop_logs=drop_logs) as f:
            # Run tofu init
            logging.info(f"Running tofu init command: {self.tf_init_command()}")
            proc = await asyncio.create_subprocess_shell(
                self.tf_init_command(),
                cwd=working_dir,
                # Stops the child process from receiving signals sent to the parent
                preexec_fn=os.setpgrp,
                stdout=f,
                stderr=f,
            )
            status_code = await proc.wait()
            if status_code != 0:
                raise exceptions.TofuInitFailure()

            # Run tofu import
            command = self.tf_import_command(resource, resource_id)
            logging.info(f"Running tofu import command: {command}")
            proc = await asyncio.create_subprocess_shell(
                command,
                cwd=working_dir,
                # Stops the child process from receiving signals sent to the parent
                preexec_fn=os.setpgrp,
                stdout=f,
                stderr=f,
            )
            status_code = await proc.wait()
            if status_code != 0:
                raise exceptions.TofuImportFailure()

    async def run(self, working_dir: str) -> Dict[str, Any]:
        self.initialize_working_dir(working_dir)

        with logging_output(self.logging_dir) as f:
            # Run tofu init
            logging.info(f"Running tofu init command: {self.tf_init_command()}")
            proc = await asyncio.create_subprocess_shell(
                self.tf_init_command(),
                cwd=working_dir,
                # Stops the child process from receiving signals sent to the parent
                preexec_fn=os.setpgrp,
                stdout=f,
                stderr=f,
            )
            status_code = await proc.wait()
            if status_code != 0:
                raise exceptions.TofuInitFailure()

            # Run tofu apply
            logging.info(f"Running tofu apply command: {self.tf_apply_command()}")
            proc = await asyncio.create_subprocess_shell(
                self.tf_apply_command(),
                cwd=working_dir,
                # Stops the child process from receiving signals sent to the parent
                preexec_fn=os.setpgrp,
                stdout=f,
                stderr=f,
            )
            tf_logs, _ = await proc.communicate()
            if proc.returncode != 0:
                raise exceptions.TofuApplyFailure()

            # Run tofu output
            tofu_output_command = f"{opentofu.TOFU_PATH} output --json"
            logging.info(f"Running tofu output command: {tofu_output_command}")
            proc = await asyncio.create_subprocess_shell(
                tofu_output_command,
                cwd=working_dir,
                stdout=asyncio.subprocess.PIPE,
                # Stops the child process from receiving signals sent to the parent
                preexec_fn=os.setpgrp,
            )
            stdout, _ = await proc.communicate()
            if proc.returncode != 0:
                raise exceptions.TofuOutputFailure()
            tf_outputs_json = json.loads(stdout)
            return parse_tf_outputs(tf_outputs_json)
