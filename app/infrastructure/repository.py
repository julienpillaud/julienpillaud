import datetime
from typing import Any

from pymongo.asynchronous.database import AsyncDatabase

from app.domain.admin.entities import RefreshToken, RefreshTokenExternal, User
from app.domain.entities import DomainEntity, EntityId
from app.domain.repository import RepositoryProtocol
from app.domain.resume.entities import Experience, Metadata, Skill

type MongoDocument = dict[str, Any]


def to_database_entity[T: DomainEntity](entity: T) -> MongoDocument:
    document = entity.model_dump(exclude={"id"})
    document["_id"] = entity.id
    return document


def to_domain_entity[T: DomainEntity](
    document: MongoDocument,
    model_class: type[T],
) -> T:
    document["id"] = str(document.pop("_id"))
    return model_class.model_validate(document)


class MongoRepository(RepositoryProtocol):
    def __init__(self, database: AsyncDatabase[MongoDocument]) -> None:
        self.database = database

    async def save_token(self, value: RefreshTokenExternal, /) -> None:
        document = to_database_entity(value.to_refresh_token())
        await self.database["refresh_tokens"].insert_one(document)

    async def get_token_by_hash(self, value: str, /) -> RefreshToken | None:
        result = await self.database["refresh_tokens"].find_one({"hash_value": value})
        if not result:
            return None

        return to_domain_entity(result, RefreshToken)

    async def revoke_token(self, token_id: EntityId) -> None:
        await self.database["refresh_tokens"].update_one(
            {"_id": token_id},
            {"$set": {"revoked_at": datetime.datetime.now(datetime.UTC)}},
        )

    async def revoke_all_tokens_for_user(self, user_id: EntityId) -> None:
        await self.database["refresh_tokens"].update_many(
            {"user_id": user_id},
            {"$set": {"revoked_at": datetime.datetime.now(datetime.UTC)}},
        )

    async def get_user(self, user_id: EntityId) -> User | None:
        result = await self.database["users"].find_one({"_id": user_id})
        if not result:
            return None

        return to_domain_entity(result, User)

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.database["users"].find_one({"username": username})
        if not result:
            return None

        return to_domain_entity(result, User)

    async def get_metadata(self) -> Metadata:
        result = await self.database["metadata"].find_one()
        return Metadata.model_validate(result)

    async def get_experiences(self) -> list[Experience]:
        result = await self.database["experiences"].find().sort({"id": 1}).to_list()
        return [Experience.model_validate(data) for data in result]

    async def get_skills(self) -> list[Skill]:
        result = (
            await self.database["skills"]
            .find()
            .sort({"category.display_order": 1, "display_order": 1})
            .to_list()
        )
        return [Skill.model_validate(data) for data in result]
