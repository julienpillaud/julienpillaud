from collections.abc import AsyncIterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict
from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import AsyncClientSession

from app.core.settings import Settings
from app.infrastructure.pdf_converter import GotenbergPDFConverter
from app.infrastructure.repository import MongoRepository
from app.infrastructure.utils import MongoDocument


class AppContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    settings: Settings
    templates: Jinja2Templates
    pdf_converter: GotenbergPDFConverter


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


def get_repository(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    session: Annotated[AsyncClientSession, Depends(get_session)],
) -> MongoRepository:
    client: AsyncMongoClient[MongoDocument] = request.app.state.mongo_client
    return MongoRepository(
        database=client[settings.mongo_database],
        session=session,
    )


@lru_cache
def get_app_context(settings: Annotated[Settings, Depends(get_settings)]) -> AppContext:
    pdf_converter = GotenbergPDFConverter(host=settings.gotenberg_host)
    return AppContext(
        settings=settings,
        templates=get_templates(settings=settings),
        pdf_converter=pdf_converter,
    )
