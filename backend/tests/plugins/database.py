from collections.abc import Iterator

import pytest
from pymongo.database import Database

from app.core.settings import Settings
from app.infrastructure.mongo_repository.resource.synchronous import MongoResource
from app.infrastructure.mongo_repository.utils import MongoDocument


@pytest.fixture(scope="session")
def resource(settings: Settings) -> Iterator[MongoResource]:
    resource = MongoResource.from_settings(settings)
    yield resource
    resource.release()


@pytest.fixture
def database(resource: MongoResource) -> Iterator[Database[MongoDocument]]:
    yield resource.database
    resource.reset()
