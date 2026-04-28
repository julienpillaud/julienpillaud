import datetime

from pymongo import UpdateOne
from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.database import AsyncDatabase

from app.domain.admin.entities import RefreshToken, RefreshTokenExternal, User
from app.domain.entities import DomainEntity, EntityId
from app.domain.repository import RepositoryProtocol
from app.domain.resume.entities import Experience, Metadata
from app.domain.skills.entities import EntityReorder, Skill, SkillCategory
from app.infrastructure.utils import MongoDocument, to_domain_entity


class MongoRepositoryError(Exception):
    pass


def to_database_entity[T: DomainEntity](
    entity: T,
    exclude: set[str] | None = None,
) -> MongoDocument:
    exclude = {"id"} | (exclude or set())
    document = entity.model_dump(exclude=exclude)
    document["_id"] = entity.id
    return document


class MongoRepository(RepositoryProtocol):
    def __init__(
        self,
        database: AsyncDatabase[MongoDocument],
        session: AsyncClientSession | None = None,
    ) -> None:
        self.database = database
        self.session = session

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

    # --------------------------------------------------------------------------
    # Skill
    async def get_skill(self, skill_id: EntityId) -> Skill | None:
        result = await self.database["skills"].find_one({"_id": skill_id})
        if not result:
            return None

        return to_domain_entity(result, Skill)

    async def create_skill(self, entity: Skill, /) -> Skill:
        document = to_database_entity(entity)

        result = await self.database["skills"].insert_one(document)
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to create skill")

        return entity

    async def reorder_skills(self, entities: list[EntityReorder], /) -> None:
        requests = [
            UpdateOne(
                {"_id": entity.id},
                {"$set": {"display_order": entity.display_order}},
            )
            for entity in entities
        ]
        await self.database["skills"].bulk_write(requests=requests)

    async def delete_skill(self, entity: Skill, /) -> None:
        result = await self.database["skills"].delete_one({"_id": entity.id})
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to delete skill")

    # --------------------------------------------------------------------------
    # SkillCategory
    @staticmethod
    def _skill_categories_pipeline(
        match: MongoDocument | None = None,
    ) -> list[MongoDocument]:
        pipeline = []
        if match:
            pipeline.append({"$match": match})

        pipeline += [
            {
                "$lookup": {
                    "from": "skills",
                    "localField": "_id",
                    "foreignField": "category_id",
                    "pipeline": [{"$sort": {"display_order": 1}}],
                    "as": "skills",
                }
            },
            {"$sort": {"display_order": 1}},
        ]
        return pipeline

    async def get_skill_categories(self) -> list[SkillCategory]:
        pipeline = self._skill_categories_pipeline()
        cursor = await self.database["skills_categories"].aggregate(pipeline=pipeline)
        result = await cursor.to_list()
        return [to_domain_entity(data, SkillCategory) for data in result]

    async def get_skill_category(self, category_id: EntityId) -> SkillCategory | None:
        pipeline = self._skill_categories_pipeline(match={"_id": category_id})
        cursor = await self.database["skills_categories"].aggregate(pipeline=pipeline)
        result = await cursor.to_list()
        if not result:
            return None

        return to_domain_entity(result[0], SkillCategory)

    async def create_skill_category(self, entity: SkillCategory, /) -> SkillCategory:
        document = to_database_entity(entity, exclude={"skills"})

        result = await self.database["skills_categories"].insert_one(document=document)
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to create category")

        return entity

    async def update_skill_category(self, entity: SkillCategory, /) -> SkillCategory:
        document = to_database_entity(entity, exclude={"skills"})

        result = await self.database["skills_categories"].replace_one(
            filter={"_id": entity.id},
            replacement=document,
        )
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to update skills")

        return entity

    async def reorder_skill_categories(
        self,
        entities: list[EntityReorder],
        /,
    ) -> None:
        requests = [
            UpdateOne(
                {"_id": entity.id},
                {"$set": {"display_order": entity.display_order}},
            )
            for entity in entities
        ]
        await self.database["skills_categories"].bulk_write(requests=requests)

    async def delete_skill_category(self, entity: SkillCategory, /) -> None:
        await self.database["skills_categories"].delete_one(
            filter={"_id": entity.id},
            session=self.session,
        )
        await self.database["skills"].delete_many(
            filter={"category_id": entity.id},
            session=self.session,
        )
