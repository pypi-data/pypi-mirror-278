# Handling imports and missing dependencies
try:
    import redis
except ImportError:
    redis = None

from dataclasses import dataclass
from typing import Optional

from launchflow.docker.resource import DockerResource
from launchflow.node import Inputs, Outputs


def _check_redis_installs():
    if redis is None:
        raise ImportError(
            "redis library is not installed. Please install it with `pip install redis`."
        )


@dataclass
class DockerRedisOutputs(Outputs):
    container_id: str
    password: str
    redis_port: int


@dataclass
class DockerRedisInputs(Inputs):
    redis_port: int


class DockerRedis(DockerResource[DockerRedisOutputs]):
    def __init__(self, name: str, *, password: str = "password") -> None:
        """A Redis resource running in a Docker container.

        **Args**:
        - `name` (str): The name of the Redis docker resource. This must be globally unique.
        - `password` (str): The password for the Redis DB. If not provided, a standard password will be used.

        **Example usage:**
        ```python
        import launchflow as lf

        redis = lf.DockerRedis("my-redis-instance")

        # Set a key-value pair
        client = redis.redis()
        client.set("my-key", "my-value")

        # Async compatible
        async_client = await redis.redis_async()
        await async_client.set("my-key", "my-value")
        ```
        """
        self.password = password

        super().__init__(
            name=name,
            env_vars={},
            command=f"redis-server --appendonly yes --requirepass {password}",
            ports={"6379/tcp": None},  # Lazy-loaded
            docker_image="redis",
            running_container_id=None,  # Lazy-loaded
        )

        self._sync_client = None
        self._async_pool = None

    def _lazy_load_container_info(self) -> None:
        """Lazy-load the information about the running container."""
        if self.running_container_id is not None and self.ports["6379/tcp"] is not None:
            return

        try:
            connection_info = self.outputs()

            self.running_container_id = connection_info.container_id
            self.ports["6379/tcp"] = connection_info.redis_port
        except Exception:
            return

    def connection_info(self) -> Optional[DockerRedisOutputs]:
        self._lazy_load_container_info()

        if self.ports["6379/tcp"] is None or self.running_container_id is None:
            return None

        return DockerRedisOutputs(
            password=self.password,
            redis_port=self.ports["6379/tcp"],
            container_id=self.running_container_id,
        )

    def inputs(self, *args, **kwargs) -> DockerRedisInputs:
        self._lazy_load_container_info()
        return DockerRedisInputs(self.ports["6379/tcp"])

    async def inputs_async(self, *args, **kwargs) -> DockerRedisInputs:
        return self.inputs(*args, **kwargs)

    def django_settings(self):
        connection_info = self.outputs()
        return {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": f"redis://default:{connection_info.password}@localhost:{connection_info.redis_port}",
        }

    def redis(self, **client_kwargs):
        """Get a Generic Redis Client object from the redis-py library.

        **Returns**:
        - The [Generic Redis Client](https://redis-py.readthedocs.io/en/stable/connections.html#generic-client) from the redis-py library.
        """
        _check_redis_installs()
        connection_info = self.outputs()
        if self._sync_client is None:
            self._sync_client = redis.Redis(
                host="localhost",
                port=int(connection_info.redis_port),
                password=connection_info.password,
                **client_kwargs,
            )
        return self._sync_client

    async def redis_async(self, *, decode_responses: bool = True):
        """Get an Async Redis Client object from the redis-py library.

        **Returns**:
        - The [Async Redis Client object](https://redis-py.readthedocs.io/en/stable/connections.html#async-client) from the redis-py library.
        """
        _check_redis_installs()
        connection_info = await self.outputs_async()
        if self._async_pool is None:
            self._async_pool = await redis.asyncio.from_url(
                f"redis://localhost:{connection_info.redis_port}",
                password=connection_info.password,
                decode_responses=decode_responses,
            )
        return self._async_pool
