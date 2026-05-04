from pymongo import AsyncMongoClient

from app.core.settings import Settings
from app.infrastructure.logger import logger
from app.infrastructure.utils import MongoDocument


async def create_mongo_client(settings: Settings) -> AsyncMongoClient[MongoDocument]:
    client: AsyncMongoClient[MongoDocument] = AsyncMongoClient(
        host=settings.mongo_uri,
        uuidRepresentation="standard",
    )
    await client.admin.command("ping")
    logger.info("MongoDB client up")
    return client
