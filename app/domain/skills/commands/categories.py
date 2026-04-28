import uuid

from app.domain.entities import EntityId
from app.domain.exceptions import NotFoundError
from app.domain.repository import RepositoryProtocol
from app.domain.skills.entities import (
    EntityReorder,
    SkillCategory,
    SkillCategoryUpdate,
    SkillCreate,
)


async def get_or_create_skill_category_command(
    repository: RepositoryProtocol,
    /,
    data: SkillCreate,
) -> SkillCategory:
    if data.category.id:
        category = await repository.get_skill_category(data.category.id)
        if not category:
            raise NotFoundError(f"Category {data.category.id} not found")

        return category

    category = SkillCategory(
        id=uuid.uuid7(),
        name=data.category.name,
        display_order=data.category.display_order,
        skills=[],
    )
    return await repository.create_skill_category(category)


async def update_skill_category_command(
    repository: RepositoryProtocol,
    /,
    category_id: EntityId,
    data: SkillCategoryUpdate,
) -> SkillCategory:
    category = await repository.get_skill_category(category_id=category_id)
    if not category:
        raise NotFoundError(f"Category {category_id} not found")

    category.name = data.name

    return await repository.update_skill_category(category)


async def reorder_skill_categories_command(
    repository: RepositoryProtocol,
    /,
    data: list[EntityReorder],
) -> None:
    await repository.reorder_skill_categories(data)


async def delete_skill_category_command(
    repository: RepositoryProtocol,
    /,
    category_id: EntityId,
) -> None:
    category = await repository.get_skill_category(category_id=category_id)
    if not category:
        raise NotFoundError(f"Category {category_id} not found")

    await repository.delete_skill_category(category)
