import uuid

from app.domain.entities import EntityId
from app.domain.exceptions import NotFoundError
from app.domain.repository import RepositoryProtocol
from app.domain.skills.commands.categories import get_or_create_skill_category_command
from app.domain.skills.entities import EntityReorder, Skill, SkillCategory, SkillCreate


async def get_skill_categories_command(
    repository: RepositoryProtocol,
    /,
) -> list[SkillCategory]:
    return await repository.get_skill_categories()


async def create_skill_command(
    repository: RepositoryProtocol,
    /,
    data: SkillCreate,
) -> Skill:
    category = await get_or_create_skill_category_command(repository, data=data)
    skill = Skill(
        id=uuid.uuid7(),
        name=data.name,
        display_order=data.display_order,
        category_id=category.id,
    )
    return await repository.create_skill(skill)


async def reorder_skills_command(
    repository: RepositoryProtocol,
    /,
    data: list[EntityReorder],
) -> None:
    await repository.reorder_skills(data)


async def delete_skill_command(
    repository: RepositoryProtocol,
    /,
    skill_id: EntityId,
) -> None:
    skill = await repository.get_skill(skill_id=skill_id)
    if not skill:
        raise NotFoundError(f"Skill {skill_id} not found")

    await repository.delete_skill(skill)

    skill_category = await repository.get_skill_category(skill.category_id)
    if skill_category and not skill_category.skills:
        await repository.delete_skill_category(skill_category)
