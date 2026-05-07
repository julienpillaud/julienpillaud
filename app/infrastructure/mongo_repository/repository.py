from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.database import AsyncDatabase

from app.infrastructure.mongo_repository.utils import MongoDocument


class MongoRepository:
    def __init__(
        self,
        database: AsyncDatabase[MongoDocument],
        session: AsyncClientSession | None = None,
    ) -> None:
        self.database = database
        self.session = session
