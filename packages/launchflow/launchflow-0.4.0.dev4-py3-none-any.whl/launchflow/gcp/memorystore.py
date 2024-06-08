# Handling imports and missing dependencies
try:
    import redis
except ImportError:
    redis = None

import dataclasses

from launchflow.gcp.resource import GCPResource
from launchflow.generic_clients import RedisClient
from launchflow.models.enums import EnvironmentType, ResourceProduct
from launchflow.node import Inputs, Outputs


def _check_installs():
    if redis is None:
        raise ImportError(
            "redis library is not installed. Please install it with `pip install redis`."
        )


@dataclasses.dataclass
class MemorystoreRedisOutputs(Outputs):
    host: str
    port: int
    password: str


@dataclasses.dataclass
class MemoryStoreInputs(Inputs):
    memory_size_gb: int
    redis_tier: str


class MemorystoreRedis(GCPResource[MemorystoreRedisOutputs], RedisClient):
    """A Redis cluster running on Google Cloud's Memorystore service.

    Like all [Resources](/docs/concepts/resources), this class configures itself across multiple [Environments](/docs/concepts/environments).

    For more information see [the official documentation](https://cloud.google.com/memorystore/docs/redis).

    **NOTE**: This resource can only be accessed from within the same VPC it is created in.
    Use [ComputeEngineRedis](/reference/gcp-resources/compute-engine#compute-engine-redis) to create a Redis instance that can be accessed from outside the VPC.

    ## Example Usage
    ```python
    import launchflow as lf

    # Automatically creates / connects to a Memorystore Redis cluster in your GCP project
    memorystore = lf.gcp.MemorystoreRedis("my-redis-cluster")

    # Set a key-value pair
    client = memorystore.redis()
    client.set("my-key", "my-value")

    # Async compatible
    async_client = await memorystore.redis_async()
    await async_client.set("my-key", "my-value")
    ```

    ## Optional Arguments
    - `memory_size_gb` (int): The memory size of the Redis instance in GB. Defaults to 1.

    ```python
    import launchflow as lf

    memorystore = lf.gcp.MemorystoreRedis("my-redis-cluster", memory_size_gb=2)
    ```

    ## Utility Methods
    """

    def __init__(self, name: str, *, memory_size_gb: int = 1) -> None:
        """Create a new Memorystore Redis resource.

        **Args**:
        - `name` (str): The name of the Redis VM resource. This must be globally unique.
        - `memory_size_gb` (int): The memory size of the Redis instance in GB. Defaults to 1.
        """
        super().__init__(
            name=name,
            product=ResourceProduct.GCP_MEMORYSTORE_REDIS,
        )
        self.memory_size_gb = memory_size_gb

    def inputs(self, environment_type: EnvironmentType) -> MemoryStoreInputs:
        if environment_type == EnvironmentType.PRODUCTION:
            return MemoryStoreInputs(
                memory_size_gb=self.memory_size_gb,
                redis_tier="STANDARD_HA",
            )
        else:
            return MemoryStoreInputs(
                memory_size_gb=self.memory_size_gb,
                redis_tier="BASIC",
            )

    def django_settings(self):
        """Returns a Django settings dictionary for connecting to the Memorystore Redis cluster.

        **Example usage:**
        ```python
        import launchflow as lf

        memorystore = lf.gcp.MemorystoreRedis("my-redis-cluster")

        # settings.py
        CACHES = {
            # Connect Django's cache backend to the Memorystore Redis cluster
            "default": memorystore.django_settings(),
        }
        ```
        """
        connection_info = self.outputs()
        return {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": f"redis://default:{connection_info.password}@{connection_info.host}:{connection_info.port}",
        }

    def redis(self):
        """Get a Generic Redis Client object from the redis-py library.

        **Returns**:
        - The [Generic Redis Client](https://redis-py.readthedocs.io/en/stable/connections.html#generic-client) from the redis-py library.
        """
        _check_installs()
        connection_info = self.outputs()
        return redis.Redis(
            host=connection_info.host,
            port=connection_info.port,
            password=connection_info.password,
            decode_responses=True,
        )

    async def redis_async(self):
        """Get an Async Redis Client object from the redis-py library.

        **Returns**:
        - The [Async Redis Client object](https://redis-py.readthedocs.io/en/stable/connections.html#async-client) from the redis-py library.
        """
        _check_installs()
        connection_info = await self.outputs_async()
        return await redis.asyncio.from_url(
            f"redis://{connection_info.host}:{connection_info.port}",
            password=connection_info.password,
            decode_responses=True,
        )
