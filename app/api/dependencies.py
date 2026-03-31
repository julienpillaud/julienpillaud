from functools import lru_cache

from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict
from pymongo import AsyncMongoClient

from app.core.settings import Settings
from app.infrastructure.repository import MongoDocument, MongoRepository


class AppContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    settings: Settings
    repository: MongoRepository
    templates: Jinja2Templates


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
    return AppContext(
        settings=settings,
        repository=repository,
        templates=get_templates(settings=settings),
    )
