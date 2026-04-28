from pydantic import BaseModel

from app.domain.entities import DomainEntity, EntityId


class Skill(DomainEntity):
    name: str
    display_order: int
    category_id: EntityId


class SkillCategory(DomainEntity):
    name: str
    display_order: int
    skills: list[Skill]


class SkillCategoryCreate(BaseModel):
    id: EntityId | None
    name: str
    display_order: int


class SkillCreate(BaseModel):
    category: SkillCategoryCreate
    name: str
    display_order: int


class SkillCategoryUpdate(BaseModel):
    name: str


class EntityReorder(BaseModel):
    id: EntityId
    display_order: int
