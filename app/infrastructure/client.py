from pymongo import AsyncMongoClient

from app.core.settings import Settings
from app.infrastructure.logger import logger
from app.infrastructure.utils import MongoDocument


def create_mongo_client(settings: Settings) -> AsyncMongoClient[MongoDocument]:
    logger.info("Connecting to MongoDB...")
    return AsyncMongoClient(
        host=settings.mongo_uri,
        uuidRepresentation="standard",
    )
