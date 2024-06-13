import asyncio
from typing import TYPE_CHECKING

from launchflow import exceptions

if TYPE_CHECKING:
    from google.cloud import storage

_storage_client: "storage.Client" = None


def get_storage_client() -> "storage.Client":
    try:
        from google.cloud import storage
    except ImportError:
        raise exceptions.MissingGCPDependency()
    global _storage_client
    if _storage_client is None:
        _storage_client = storage.Client()
    return _storage_client


async def write_to_gcs(bucket: str, prefix: str, data: str):
    client = get_storage_client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(prefix)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, blob.upload_from_string, data)


async def read_from_gcs(bucket: str, prefix: str):
    try:
        from google.api_core.exceptions import NotFound
    except ImportError:
        raise exceptions.MissingGCPDependency()
    client = get_storage_client()
    bucket = client.bucket(bucket)
    try:
        blob = bucket.blob(prefix)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, blob.download_as_string)
    except NotFound:
        raise exceptions.GCSObjectNotFound(bucket, prefix)


def read_from_gcs_sync(bucket: str, prefix: str):
    try:
        from google.api_core.exceptions import NotFound
    except ImportError:
        raise exceptions.MissingGCPDependency()
    client = get_storage_client()
    bucket = client.bucket(bucket)
    try:
        blob = bucket.blob(prefix)
        return blob.download_as_string()
    except NotFound:
        raise exceptions.GCSObjectNotFound(bucket, prefix)
