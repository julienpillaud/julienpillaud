import uuid

from pymongo.database import Database

from app.domain.skills.entities import (
    Skill,
    SkillCategory,
    SkillCategoryCreate,
    SkillCreate,
)
from app.infrastructure.repository import MongoDocument, to_database_entity


def generate_skills(n_skills: int = 1, n_categories: int = 1) -> list[Skill]:
    if n_skills < n_categories:
        raise ValueError("n_skills must be greater than n_categories")

    quotient, remainder = divmod(n_skills, n_categories)

    skills = []
    for i in range(n_categories):
        category = SkillCategory(
            id=uuid.uuid7(),
            name=f"Category {i + 1}",
            display_order=i + 1,
        )
        for j in range(quotient + (1 if i < remainder else 0)):
            skills.append(
                Skill(
                    id=uuid.uuid7(),
                    category=category,
                    name=f"Skill {j + 1}",
                    display_order=j + 1,
                )
            )

    return skills


class SkillFactory:
    def __init__(self, database: Database[MongoDocument]):
        self.database = database

    @property
    def skill_create(self) -> SkillCreate:
        skill = generate_skills()[0]
        return SkillCreate(
            category=SkillCategoryCreate(
                id=skill.category.id,
                name=skill.category.name,
                display_order=skill.category.display_order,
            ),
            name=skill.name,
            display_order=skill.display_order,
        )

    def create_one(self) -> Skill:
        skill = generate_skills()[0]
        self._save([skill])
        return skill

    def create_many(self, n_skills: int = 1, n_categories: int = 1) -> list[Skill]:
        skills = generate_skills(n_skills=n_skills, n_categories=n_categories)
        self._save(skills)
        return skills

    def _save(self, skills: list[Skill]) -> None:
        documents = [to_database_entity(entity) for entity in skills]
        self.database["skills"].insert_many(documents)
