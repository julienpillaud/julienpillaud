from collections.abc import Iterator

import pytest
from pymongo import MongoClient
from pymongo.database import Database

from app.core.settings import Settings
from app.infrastructure.repository import MongoDocument


@pytest.fixture(scope="session")
def mongo_client(settings: Settings) -> Iterator[MongoClient[MongoDocument]]:
    client: MongoClient[MongoDocument] = MongoClient(
        settings.mongo_uri,
        uuidRepresentation="standard",
    )
    yield client
    client.close()


@pytest.fixture
def database(
    settings: Settings,
    mongo_client: MongoClient[MongoDocument],
) -> Iterator[Database[MongoDocument]]:
    database = mongo_client[settings.mongo_database]

    yield database

    for collection in database.list_collection_names():
        database[collection].delete_many({})
