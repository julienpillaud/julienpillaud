from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict
from pymongo import AsyncMongoClient

from app.core.settings import Settings
from app.infrastructure.pdf_converter import GotenbergPDFConverter
from app.infrastructure.repository import MongoDocument, MongoRepository


class AppContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    settings: Settings
    templates: Jinja2Templates
    repository: MongoRepository
    pdf_converter: GotenbergPDFConverter


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_templates(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Jinja2Templates:
    return Jinja2Templates(directory=settings.paths.templates)


@lru_cache
def get_repository(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> MongoRepository:
    client: AsyncMongoClient[MongoDocument] = request.app.state.mongo_client
    database = client[settings.mongo_database]
    return MongoRepository(database=database)


@lru_cache
def get_app_context(
    settings: Annotated[Settings, Depends(get_settings)],
    repository: Annotated[MongoRepository, Depends(get_repository)],
) -> AppContext:
    pdf_converter = GotenbergPDFConverter(host=settings.gotenberg_host)
    return AppContext(
        settings=settings,
        templates=get_templates(settings=settings),
        repository=repository,
        pdf_converter=pdf_converter,
    )
