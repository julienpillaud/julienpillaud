from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from app.api.logger import logger
from app.core.settings import Settings
from app.infrastructure.cache_manager import create_redis_client
from app.infrastructure.client import create_mongo_client


def lifespan_factory(
    settings: Settings,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.redis_client = await create_redis_client(settings=settings)
        app.state.mongo_client = await create_mongo_client(settings=settings)
        logger.info("Application startup complete")

        yield

        await app.state.mongo_client.close()
        await app.state.redis_client.aclose()
        logger.info("Application shutdown complete")

    return lifespan


def mount_static(app: FastAPI, settings: Settings) -> None:
    app.mount(
        path="/static",
        app=StaticFiles(directory=settings.paths.static),
        name="static",
    )


def set_cookie(
    response: Response,
    key: str,
    value: str,
    max_age: int,
) -> None:
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        secure=True,
        httponly=True,
        samesite="lax",
    )
