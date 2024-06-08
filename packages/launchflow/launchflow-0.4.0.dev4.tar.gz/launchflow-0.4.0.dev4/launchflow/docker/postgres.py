try:
    import asyncpg
except ImportError:
    asyncpg = None

try:
    import pg8000
except ImportError:
    pg8000 = None

try:
    import psycopg2
except ImportError:
    psycopg2 = None

try:
    from sqlalchemy.ext.asyncio import create_async_engine
except ImportError:
    async_sessionmaker = None
    create_async_engine = None

try:
    from sqlalchemy import create_engine
except ImportError:
    create_engine = None
    DeclarativeBase = None
    sessionmaker = None

from dataclasses import dataclass
from typing import Optional

from launchflow.docker.resource import DockerResource
from launchflow.node import Inputs, Outputs


@dataclass
class DockerPostgresOutputs(Outputs):
    container_id: str
    password: str
    postgres_port: int


@dataclass
class DockerPostgresInputs(Inputs):
    postgres_port: int


class DockerPostgres(DockerResource[DockerPostgresOutputs]):
    def __init__(self, name: str, *, password: str = "password") -> None:
        """A Postgres resource running in a Docker container.

        **Args**:
        - `name` (str): The name of the Postgres resource. This must be globally unique.
        - `password` (str): The password for the Postgres DB. If not provided, a standard password will be used.

        **Example usage**:
        ```python
        from sqlalchemy import text
        import launchflow as lf

        postgres = lf.docker.Postgres("postgres-db")
        engine = postgres.sqlalchemy_engine()

        with engine.connect() as connection:
            print(connection.execute(text("SELECT 1")).fetchone())  # prints (1,)
        ```
        """
        self.password = password

        super().__init__(
            name=name,
            env_vars={
                "POSTGRES_PASSWORD": self.password,
                "POSTGRES_DB": "postgres",
                "POSTGRES_USER": "postgres",
            },
            command=None,
            ports={"5432/tcp": None},  # Lazy-loaded
            docker_image="postgres",
            running_container_id=None,  # Lazy-loaded
        )

    def _lazy_load_container_info(self) -> None:
        """Lazy-load the information about the running container."""
        if self.running_container_id is not None and self.ports["5432/tcp"] is not None:
            return

        try:
            connection_info = self.outputs()

            self.running_container_id = connection_info.container_id
            self.ports["5432/tcp"] = connection_info.postgres_port
        except Exception:
            return

    def connection_info(self) -> Optional[DockerPostgresOutputs]:
        self._lazy_load_container_info()

        if self.ports["5432/tcp"] is None or self.running_container_id is None:
            return None

        return DockerPostgresOutputs(
            password=self.password,
            postgres_port=self.ports["5432/tcp"],
            container_id=self.running_container_id,
        )

    def inputs(self, *args, **kwargs) -> DockerPostgresInputs:
        self._lazy_load_container_info()
        return DockerPostgresInputs(self.ports["5432/tcp"])

    async def inputs_async(self, *args, **kwargs) -> DockerPostgresInputs:
        return self.inputs(*args, **kwargs)

    def django_settings(self):
        if psycopg2 is None:
            raise ImportError(
                "psycopg2 is not installed. Please install it with `pip install psycopg2`."
            )

        connection_info = self.outputs()
        return {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": connection_info.password,
            "HOST": "localhost",
            "PORT": connection_info.postgres_port,
        }

    def sqlalchemy_engine_options(self):
        if pg8000 is None:
            raise ImportError(
                "pg8000 is not installed. Please install it with `pip install pg8000`."
            )

        connection_info = self.outputs()
        return {
            "url": f"postgresql+pg8000://postgres:{connection_info.password}@localhost:{connection_info.postgres_port}/postgres",
        }

    async def sqlalchemy_async_engine_options(self):
        if asyncpg is None:
            raise ImportError(
                "asyncpg is not installed. Please install it with `pip install asyncpg`."
            )

        connection_info = await self.outputs_async()
        return {
            "url": f"postgresql+asyncpg://postgres:{connection_info.password}@localhost:{connection_info.postgres_port}/postgres"
        }

    def sqlalchemy_engine(self, **engine_kwargs):
        """Returns a SQLAlchemy engine for connecting to a postgres instance hosted on Docker.

        Args:
        - `**engine_kwargs`: Additional keyword arguments to pass to `sqlalchemy.create_engine`.

        **Example usage:**
        ```python
        import launchflow as lf
        db = lf.docker.Postgres("my-pg-db")
        engine = db.sqlalchemy_engine()
        ```
        """
        if create_engine is None:
            raise ImportError(
                "SQLAlchemy is not installed. Please install it with "
                "`pip install sqlalchemy`."
            )

        engine_options = self.sqlalchemy_engine_options()
        engine_options.update(engine_kwargs)

        return create_engine(**engine_options)

    async def sqlalchemy_async_engine(self, **engine_kwargs):
        """Returns an async SQLAlchemy engine for connecting to a postgres instance hosted on Docker.

        Args:
        - `**engine_kwargs`: Additional keyword arguments to pass to `create_async_engine`.

        **Example usage:**
        ```python
        import launchflow as lf
        db = lf.docker.Postgres("my-pg-db")
        engine = await db.sqlalchemy_async_engine()
        ```
        """
        if create_async_engine is None:
            raise ImportError(
                "SQLAlchemy asyncio extension is not installed. "
                "Please install it with `pip install sqlalchemy[asyncio]`."
            )

        engine_options = await self.sqlalchemy_async_engine_options()
        engine_options.update(engine_kwargs)

        return create_async_engine(**engine_options)
