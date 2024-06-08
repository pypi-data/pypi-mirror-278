from launchflow import config, exceptions
from launchflow.workflows.aws_env_deletion.schemas import AWSEnvironmentDeletionInputs
from launchflow.workflows.commands.tf_commands import TFDestroyCommand
from launchflow.workflows.utils import run_tofu


def _delete_artifact_bucket(bucket_name: str):
    try:
        import boto3
        import botocore
    except ImportError:
        raise exceptions.MissingAWSDependency()
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    try:
        # First delete all objects in the bucket
        bucket.objects.all().delete()
        # Then delete the bucket
        bucket.delete()
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucket":
            return
        raise


async def _run_tofu(inputs: AWSEnvironmentDeletionInputs):
    command = TFDestroyCommand(
        tf_module_dir="workflows/tf/empty/aws_empty",
        backend=config.launchflow_yaml.backend,
        tf_state_prefix=inputs.launchflow_uri.tf_state_prefix(inputs.lock_id),
        tf_vars={
            "aws_region": inputs.aws_region,
        },
    )
    return await run_tofu(command)


async def delete_aws_environment(inputs: AWSEnvironmentDeletionInputs):
    _delete_artifact_bucket(inputs.artifact_bucket)
    return await _run_tofu(inputs)
