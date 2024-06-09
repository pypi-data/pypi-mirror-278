import asyncio
import traceback
from datetime import datetime
from typing import Any, Callable, Coroutine, Type

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


class Logger:
    """MongoDB async logger."""

    def __init__(self, **kwargs):
        """Initialise with a PyMongo collection."""
        self.collection: AsyncIOMotorCollection | None = self._collection_from_host(kwargs)

        if self.collection is None:
            self.collection = self._collection_from_uri(kwargs)

        if self.collection is None:
            self.collection = kwargs.get("collection")

        if self.collection is None:
            raise ValueError("No collection provided.")

        if not isinstance(self.collection, AsyncIOMotorCollection):
            raise TypeError("Collection must be an instance of AsyncIOMotorCollection.")

        self.serializers: dict[Type, Callable] = {}

    def _collection_from_host(self, kwargs) -> AsyncIOMotorCollection | None:
        if "host" not in kwargs:
            return None

        username = kwargs["username"]
        password = kwargs["password"]
        host = kwargs["host"]
        port = kwargs["port"]
        uri = f"mongodb://{username}:{password}@{host}:{port}/"

        db_name = kwargs["db_name"]
        collection_name = kwargs["collection_name"]

        client = AsyncIOMotorClient(uri)
        return client[db_name][collection_name]

    def _collection_from_uri(self, kwargs) -> AsyncIOMotorCollection | None:
        if "uri" not in kwargs:
            return None

        uri = kwargs["uri"]
        client = AsyncIOMotorClient(uri)

        db_name = kwargs["db_name"]
        collection_name = kwargs["collection_name"]

        return client[db_name][collection_name]

    def serializer(self, kwarg_type: Type) -> Callable:
        """Decorator to add a serializer for a kwarg."""

        def wrapper(serializer: Callable) -> Callable:
            self.add_serializer(kwarg_type, serializer)
            return serializer

        return wrapper

    def add_serializer(self, kwarg_type: Type, serializer: Callable) -> None:
        """Add a serializer for a kwarg."""
        if not isinstance(kwarg_type, type):
            raise ValueError("kwarg_type must be a type.")

        if not callable(serializer):
            raise ValueError("Serializer must be a callable.")

        self.serializers[kwarg_type] = serializer

    async def _insert_document(self, document: dict[str, Any]) -> None:
        """Insert a document to mongo (separated for better control)."""
        assert self.collection is not None, "Collection not initialised."

        await self.collection.insert_one(document)

    async def _write(self, **kwargs) -> None:
        """Write a single log to the log backend."""
        time = datetime.utcnow()
        self._serialize_kwargs(kwargs)

        await self._insert_document(
            {
                "timestamp": time,
                **kwargs,
            }
        )

    def _serialize_kwargs(self, kwargs: dict[str, Any]):
        """In-place serialization of kwargs."""
        for kwarg in kwargs:
            if hasattr(kwargs[kwarg], "__mongo__") and callable(kwargs[kwarg].__mongo__):
                kwargs[kwarg] = kwargs[kwarg].__mongo__()
            elif kwarg in self.serializers:
                kwargs[kwarg] = self.serializers[kwarg](kwargs[kwarg])

    async def a_debug(self, **kwargs) -> None:
        """Write a log at the DEBUG level."""
        await self._debug_task(**kwargs)

    def debug(self, **kwargs) -> asyncio.Task[None]:
        """Write a log at the DEBUG level."""
        task = self._debug_task(**kwargs)
        return asyncio.create_task(task)

    def _debug_task(self, **kwargs) -> Coroutine[None, None, None]:
        """Write a log at the DEBUG level."""
        return self._write(level="DEBUG", **kwargs)

    async def a_info(self, **kwargs) -> None:
        """Write a lot at the INFO level."""
        await self._info_task(**kwargs)

    def info(self, **kwargs) -> asyncio.Task[None]:
        """Write a log at the INFO level."""
        task = self._info_task(**kwargs)
        return asyncio.create_task(task)

    def _info_task(self, **kwargs) -> Coroutine[None, None, None]:
        """Write a log at the INFO level."""
        return self._write(level="INFO", **kwargs)

    async def a_warning(self, **kwargs) -> None:
        """Write a log at the WARNING level."""
        await self._warning_task(**kwargs)

    def warning(self, **kwargs) -> asyncio.Task[None]:
        """Write a log at the WARNING level."""
        task = self._warning_task(**kwargs)
        return asyncio.create_task(task)

    def _warning_task(self, **kwargs) -> Coroutine[None, None, None]:
        """Write a log at the WARNING level."""
        return self._write(level="WARNING", **kwargs)

    async def a_error(self, **kwargs) -> None:
        """Write a log at the ERROR level."""
        await self._error_task(**kwargs)

    def error(self, **kwargs) -> asyncio.Task[None]:
        """Write a log at the ERROR level."""
        task = self._error_task(**kwargs)
        return asyncio.create_task(task)

    def _error_task(self, **kwargs) -> Coroutine[None, None, None]:
        """Write a log at the ERROR level."""
        return self._write(level="ERROR", **kwargs)

    async def a_exception(self, exception: Exception, **kwargs) -> None:
        """Write a log at the ERROR level with an exception."""
        await self.exception_task(exception, **kwargs)

    def exception(self, exception: Exception, **kwargs) -> asyncio.Task[None]:
        """Write a log at the ERROR level with an exception."""
        task = self.exception_task(exception, **kwargs)
        return asyncio.create_task(task)

    def exception_task(self, exception: Exception, **kwargs) -> Coroutine[None, None, None]:
        """Write a log at the ERROR level with an exception."""
        return self._write(
            level="EXCEPTION",
            exception={
                "type": type(exception).__name__,
                "message": str(exception),
                "traceback": traceback.format_exc(),
            },
            **kwargs,
        )
