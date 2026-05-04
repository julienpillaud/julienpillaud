from collections.abc import AsyncIterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import AsyncClientSession

from app.core.context import Context
from app.core.settings import Settings
from app.infrastructure.utils import MongoDocument


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_templates(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Jinja2Templates:
    return Jinja2Templates(directory=settings.paths.templates)


async def get_session(request: Request) -> AsyncIterator[AsyncClientSession]:
    client: AsyncMongoClient[MongoDocument] = request.app.state.mongo_client
    async with client.start_session() as session:
        async with await session.start_transaction():
            yield session


class ContextFactory:
    @staticmethod
    def query(
        request: Request,
        settings: Annotated[Settings, Depends(get_settings)],
    ) -> Context:
        client: AsyncMongoClient[MongoDocument] = request.app.state.mongo_client
        return Context(
            settings=settings,
            redis_client=request.app.state.redis_client,
            mongo_database=client[settings.mongo_database],
            mongo_session=None,
        )

    @staticmethod
    def command(
        request: Request,
        settings: Annotated[Settings, Depends(get_settings)],
        session: Annotated[AsyncClientSession, Depends(get_session)],
    ) -> Context:
        client: AsyncMongoClient[MongoDocument] = request.app.state.mongo_client
        return Context(
            settings=settings,
            redis_client=request.app.state.redis_client,
            mongo_database=client[settings.mongo_database],
            mongo_session=session,
        )
