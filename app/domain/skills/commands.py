import uuid
from itertools import groupby

from app.domain.entities import EntityId
from app.domain.exceptions import NotFoundError
from app.domain.repository import RepositoryProtocol
from app.domain.skills.entities import (
    Skill,
    SkillCategory,
    SkillCreate,
    SkillItem,
    SkillSummary,
    SkillUpdate,
)


async def get_skills_command(repository: RepositoryProtocol, /) -> list[SkillSummary]:
    raw_skills = await repository.get_skills()

    output: list[SkillSummary] = []
    for key, group in groupby(raw_skills, lambda x: (x.category.id, x.category.name)):
        category_id, category_name = key

        output.append(
            SkillSummary(
                id=category_id,
                category_name=category_name,
                skills=[SkillItem(id=skill.id, name=skill.name) for skill in group],
            )
        )

    return output


async def create_skill_command(
    repository: RepositoryProtocol,
    /,
    data: SkillCreate,
) -> Skill:
    if data.category.id:
        category = await repository.get_category_by_id(data.category.id)
        if not category:
            raise NotFoundError(f"Category {data.category.id} not found")

    skill = Skill(
        id=uuid.uuid7(),
        category=SkillCategory(
            id=data.category.id or uuid.uuid7(),
            name=data.category.name,
            display_order=data.category.display_order,
        ),
        name=data.name,
        display_order=data.display_order,
    )

    return await repository.create_skill(skill)


async def update_skill_command(
    repository: RepositoryProtocol,
    /,
    skill_id: EntityId,
    data: SkillUpdate,
) -> Skill:
    skill = await repository.get_skill(skill_id=skill_id)
    if not skill:
        raise NotFoundError(f"Skill {skill_id} not found")

    skill.name = data.name

    return await repository.update_skill(skill)


async def delete_skill_command(
    repository: RepositoryProtocol,
    /,
    skill_id: EntityId,
) -> None:
    skill = await repository.get_skill(skill_id=skill_id)
    if not skill:
        raise NotFoundError(f"Skill {skill_id} not found")

    await repository.delete_skill(skill)


async def delete_skills_by_category_command(
    repository: RepositoryProtocol,
    /,
    category_id: EntityId,
) -> None:
    category = await repository.get_category_by_id(category_id)
    if not category:
        raise NotFoundError(f"Category {category_id} not found")

    await repository.delete_skills_by_category(category_id=category_id)
