from pymongo import UpdateOne

from app.domain.entities import EntityId
from app.domain.skills.entities import EntityReorder, Skill, SkillCategory
from app.domain.skills.repository import SkillRepositoryProtocol
from app.infrastructure.mongo_repository.repository import MongoRepository
from app.infrastructure.mongo_repository.utils import (
    MongoDocument,
    MongoRepositoryError,
    to_database_entity,
    to_domain_entity,
)


class SkillRepository(SkillRepositoryProtocol, MongoRepository):
    # Skill
    async def get_skill(self, skill_id: EntityId) -> Skill | None:
        result = await self.database["skills"].find_one({"_id": skill_id})
        if not result:
            return None

        return to_domain_entity(result, Skill)

    async def save_skill(self, entity: Skill, /) -> Skill:
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

    async def remove_skill(self, entity: Skill, /) -> None:
        result = await self.database["skills"].delete_one({"_id": entity.id})
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to delete skill")

    # SkillCategory
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

    async def save_skill_category(self, entity: SkillCategory, /) -> SkillCategory:
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

    async def remove_skill_category(self, entity: SkillCategory, /) -> None:
        await self.database["skills_categories"].delete_one(
            filter={"_id": entity.id},
            session=self.session,
        )
        await self.database["skills"].delete_many(
            filter={"category_id": entity.id},
            session=self.session,
        )

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
