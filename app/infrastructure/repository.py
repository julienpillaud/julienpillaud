from typing import Any

from pymongo.asynchronous.database import AsyncDatabase

from app.domain.entities import Experience, Metadata, Skill
from app.domain.repository import RepositoryProtocol

type MongoDocument = dict[str, Any]


class MongoRepository(RepositoryProtocol):
    def __init__(self, database: AsyncDatabase[MongoDocument]) -> None:
        self.database = database

    async def get_metadata(self) -> Metadata:
        result = await self.database["metadata"].find_one()
        return Metadata.model_validate(result)

    async def get_experiences(self) -> list[Experience]:
        result = await self.database["experiences"].find().sort({"id": 1}).to_list()
        return [Experience.model_validate(data) for data in result]

    async def get_skills(self) -> list[Skill]:
        result = await self.database["skills"].find().sort({"order": 1}).to_list()
        return [Skill.model_validate(data) for data in result]
