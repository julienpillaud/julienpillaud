from functools import lru_cache

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
def get_templates(settings: Settings) -> Jinja2Templates:
    return Jinja2Templates(directory=settings.paths.templates)


@lru_cache
def get_app_context() -> AppContext:
    settings = get_settings()
    client: AsyncMongoClient[MongoDocument] = AsyncMongoClient(settings.mongo_uri)
    database = client[settings.mongo_database]
    repository = MongoRepository(database=database)
    pdf_converter = GotenbergPDFConverter(host=settings.gotenberg_host)
    return AppContext(
        settings=settings,
        templates=get_templates(settings=settings),
        repository=repository,
        pdf_converter=pdf_converter,
    )
