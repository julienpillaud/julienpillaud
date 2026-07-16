from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

import httpx2
from fastapi import FastAPI

from app.core.logger import logger
from app.core.settings import Settings
from app.infrastructure.cache_manager import create_redis_client
from app.infrastructure.mongo_repository.resource.asynchronous import (
    MongoResource,
)


def lifespan_factory(
    settings: Settings,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.mongo_resource = await MongoResource.from_settings(settings)
        app.state.redis_client = await create_redis_client(settings=settings)
        app.state.http_client = httpx2.AsyncClient(timeout=settings.http_client_timeout)
        logger.info("Application startup complete")

        yield

        await app.state.http_client.aclose()
        await app.state.redis_client.aclose()
        await app.state.mongo_resource.release()
        logger.info("Application shutdown complete")

    return lifespan
