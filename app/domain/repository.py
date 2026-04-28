from typing import Protocol

from app.domain.admin.entities import RefreshToken, RefreshTokenExternal, User
from app.domain.entities import EntityId
from app.domain.resume.entities import Experience, Metadata
from app.domain.skills.entities import EntityReorder, Skill, SkillCategory


class RepositoryProtocol(Protocol):
    # refresh_tokens
    async def save_token(self, value: RefreshTokenExternal, /) -> None: ...

    async def get_token_by_hash(self, value: str, /) -> RefreshToken | None: ...

    async def revoke_token(self, token_id: EntityId) -> None: ...

    async def revoke_all_tokens_for_user(self, user_id: EntityId) -> None: ...

    # users
    async def get_user(self, user_id: EntityId) -> User | None: ...

    async def get_user_by_username(self, username: str) -> User | None: ...

    # metadata
    async def get_metadata(self) -> Metadata: ...

    # experiences
    async def get_experiences(self) -> list[Experience]: ...

    # --------------------------------------------------------------------------
    # Skill
    async def get_skill(self, skill_id: EntityId) -> Skill | None: ...

    async def create_skill(self, entity: Skill, /) -> Skill: ...

    async def reorder_skills(self, entities: list[EntityReorder], /) -> None: ...

    async def delete_skill(self, entity: Skill, /) -> None: ...

    # --------------------------------------------------------------------------
    # SkillCategory
    async def get_skill_categories(self) -> list[SkillCategory]: ...

    async def get_skill_category(
        self,
        category_id: EntityId,
    ) -> SkillCategory | None: ...

    async def create_skill_category(
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

    async def delete_skill_category(self, entity: SkillCategory, /) -> None: ...
