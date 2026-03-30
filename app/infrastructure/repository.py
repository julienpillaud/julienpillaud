from typing import Any

from pymongo.asynchronous.database import AsyncDatabase

from app.domain.entities import Experience
from app.domain.repository import RepositoryProtocol

type MongoDocument = dict[str, Any]


class MongoRepository(RepositoryProtocol):
    def __init__(self, database: AsyncDatabase[MongoDocument]) -> None:
        self.database = database

    async def get_experiences(self) -> list[Experience]:
        result = await self.database["experiences"].find().sort({"id": 1}).to_list()
        return [Experience.model_validate(data) for data in result]
