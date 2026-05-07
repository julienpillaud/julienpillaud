from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.database import AsyncDatabase

from app.domain.repository import RepositoryProtocol
from app.domain.resume.entities import Experience, Metadata
from app.infrastructure.mongo_repository.utils import MongoDocument


class MongoRepository(RepositoryProtocol):
    def __init__(
        self,
        database: AsyncDatabase[MongoDocument],
        session: AsyncClientSession | None = None,
    ) -> None:
        self.database = database
        self.session = session

    async def get_metadata(self) -> Metadata:
        result = await self.database["metadata"].find_one()
        return Metadata.model_validate(result)

    async def get_experiences(self) -> list[Experience]:
        result = await self.database["experiences"].find().sort({"id": 1}).to_list()
        return [Experience.model_validate(data) for data in result]
