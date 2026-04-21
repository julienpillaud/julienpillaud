from pydantic import BaseModel

from app.domain.entities import DomainEntity, EntityId


class SkillCategory(DomainEntity):
    name: str
    display_order: int


class Skill(DomainEntity):
    category: SkillCategory
    name: str
    display_order: int


class SkillItem(BaseModel):
    id: EntityId
    name: str


class SkillSummary(BaseModel):
    id: EntityId
    category_name: str
    skills: list[SkillItem]


class SkillCategoryCreate(BaseModel):
    id: EntityId | None
    name: str
    display_order: int


class SkillCreate(BaseModel):
    category: SkillCategoryCreate
    name: str
    display_order: int


class SkillUpdate(BaseModel):
    name: str
