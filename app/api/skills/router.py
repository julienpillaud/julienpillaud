from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.app import get_domain
from app.api.dependencies.user import get_current_user
from app.core.domain import Domain
from app.domain.entities import EntityId
from app.domain.skills.entities import (
    EntityReorder,
    Skill,
    SkillCategory,
    SkillCategoryUpdate,
    SkillCreate,
)
from app.domain.skills.use_cases.categories import (
    delete_skill_category,
    reorder_skill_categories,
    update_skill_category,
)
from app.domain.skills.use_cases.skills import (
    create_skill,
    delete_skill,
    get_skill_categories,
    reorder_skills,
)

router = APIRouter(prefix="/skills")


@router.get("", dependencies=[Depends(get_current_user)])
async def get_skill_categories_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
) -> list[SkillCategory]:
    return await domain.query(get_skill_categories)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def create_skill_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    data: SkillCreate,
) -> Skill:
    return await domain.command(create_skill, data=data)


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_skill_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    skill_id: EntityId,
) -> None:
    await domain.command(delete_skill, skill_id=skill_id)


@router.patch(
    "/reorder",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def reorder_skills_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    data: list[EntityReorder],
) -> None:
    await domain.command(reorder_skills, data=data)


@router.patch(
    "/categories/reorder",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def reorder_skill_categories_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    data: list[EntityReorder],
) -> None:
    await domain.command(reorder_skill_categories, data=data)


@router.patch(
    "/categories/{category_id}",
    dependencies=[Depends(get_current_user)],
)
async def update_skill_category_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    category_id: EntityId,
    data: SkillCategoryUpdate,
) -> SkillCategory:
    return await domain.command(
        update_skill_category,
        category_id=category_id,
        data=data,
    )


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_skill_category_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    category_id: EntityId,
) -> None:
    await domain.command(delete_skill_category, category_id=category_id)
