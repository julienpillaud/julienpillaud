from typing import Protocol

from app.domain.entities import EntityId
from app.domain.skills.entities import EntityReorder, Skill, SkillCategory


class SkillRepositoryProtocol(Protocol):
    # Skill
    async def get_skill(self, skill_id: EntityId) -> Skill | None: ...

    async def save_skill(self, entity: Skill, /) -> Skill: ...

    async def reorder_skills(self, entities: list[EntityReorder], /) -> None: ...

    async def remove_skill(self, entity: Skill, /) -> None: ...

    # SkillCategory
    async def get_skill_categories(self) -> list[SkillCategory]: ...

    async def get_skill_category(
        self,
        category_id: EntityId,
    ) -> SkillCategory | None: ...

    async def save_skill_category(
        self,
        entity: SkillCategory,
        /,
    ) -> SkillCategory: ...

    async def update_skill_category(
        self,
        entity: SkillCategory,
        /,
    ) -> SkillCategory: ...

    async def reorder_skill_categories(
        self,
        entities: list[EntityReorder],
        /,
    ) -> None: ...

    async def remove_skill_category(self, entity: SkillCategory, /) -> None: ...
