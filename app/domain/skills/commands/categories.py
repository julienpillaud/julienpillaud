import uuid

from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.exceptions import NotFoundError
from app.domain.skills.entities import (
    EntityReorder,
    SkillCategory,
    SkillCategoryUpdate,
    SkillCreate,
)


async def get_or_create_skill_category_command(
    context: ContextProtocol,
    /,
    data: SkillCreate,
) -> SkillCategory:
    if data.category.id:
        category = await context.repository.get_skill_category(data.category.id)
        if not category:
            raise NotFoundError(f"Category {data.category.id} not found")

        return category

    category = SkillCategory(
        id=uuid.uuid7(),
        name=data.category.name,
        display_order=data.category.display_order,
        skills=[],
    )
    return await context.repository.create_skill_category(category)


async def update_skill_category_command(
    context: ContextProtocol,
    /,
    category_id: EntityId,
    data: SkillCategoryUpdate,
) -> SkillCategory:
    category = await context.repository.get_skill_category(category_id=category_id)
    if not category:
        raise NotFoundError(f"Category {category_id} not found")

    category.name = data.name

    return await context.repository.update_skill_category(category)


async def reorder_skill_categories_command(
    context: ContextProtocol,
    /,
    data: list[EntityReorder],
) -> None:
    await context.repository.reorder_skill_categories(data)


async def delete_skill_category_command(
    context: ContextProtocol,
    /,
    category_id: EntityId,
) -> None:
    category = await context.repository.get_skill_category(category_id=category_id)
    if not category:
        raise NotFoundError(f"Category {category_id} not found")

    await context.repository.delete_skill_category(category)
