import uuid

from pymongo.database import Database

from app.domain.skills.entities import (
    Skill,
    SkillCategory,
    SkillCategoryCreate,
    SkillCreate,
)
from app.infrastructure.repository import to_database_entity
from app.infrastructure.utils import MongoDocument


def generate_skills(n_skills: int = 1, n_categories: int = 1) -> list[SkillCategory]:
    if n_skills < n_categories:
        raise ValueError("n_skills must be greater than n_categories")

    quotient, remainder = divmod(n_skills, n_categories)

    skill_categories = []
    for i in range(n_categories):
        skill_category = SkillCategory(
            id=uuid.uuid7(),
            name=f"Category {i + 1}",
            display_order=i + 1,
            skills=[],
        )
        for j in range(quotient + (1 if i < remainder else 0)):
            skill_category.skills.append(
                Skill(
                    id=uuid.uuid7(),
                    name=f"Skill {j + 1}",
                    display_order=j + 1,
                    category_id=skill_category.id,
                )
            )
        skill_categories.append(skill_category)

    return skill_categories


class SkillFactory:
    def __init__(self, database: Database[MongoDocument]):
        self.database = database

    @property
    def skill_create(self) -> SkillCreate:
        skill_category = generate_skills()[0]
        skill = skill_category.skills[0]

        return SkillCreate(
            category=SkillCategoryCreate(
                id=skill_category.id,
                name=skill_category.name,
                display_order=skill_category.display_order,
            ),
            name=skill.name,
            display_order=skill.display_order,
        )

    def create_one(self) -> Skill:
        skill_category = generate_skills()[0]
        self._save([skill_category])
        return skill_category.skills[0]

    def create_many(self, n_skills: int = 1, n_categories: int = 1) -> list[Skill]:
        skill_categories = generate_skills(n_skills=n_skills, n_categories=n_categories)
        self._save(skill_categories)
        skills = []
        for skill_category in skill_categories:
            skills.extend(skill_category.skills)
        return skills

    def _save(self, skill_categories: list[SkillCategory]) -> None:
        for skill_category in skill_categories:
            skill_category_doc = to_database_entity(skill_category, exclude={"skills"})
            self.database["skills_categories"].insert_one(skill_category_doc)

            skill_docs = [
                to_database_entity(entity) for entity in skill_category.skills
            ]
            self.database["skills"].insert_many(skill_docs)
