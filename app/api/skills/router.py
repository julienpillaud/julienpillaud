from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.app import ContextFactory
from app.api.dependencies.user import get_current_user
from app.core.context import Context
from app.domain.entities import EntityId
from app.domain.skills.commands.categories import (
    delete_skill_category_command,
    reorder_skill_categories_command,
    update_skill_category_command,
)
from app.domain.skills.commands.skills import (
    create_skill_command,
    delete_skill_command,
    get_skill_categories_command,
    reorder_skills_command,
)
from app.domain.skills.entities import (
    EntityReorder,
    Skill,
    SkillCategory,
    SkillCategoryUpdate,
    SkillCreate,
)

router = APIRouter(prefix="/skills")


@router.get(
    "",
    response_model=list[SkillCategory],
    dependencies=[Depends(get_current_user)],
)
async def get_skill_categories(
    context: Annotated[Context, Depends(ContextFactory.query)],
) -> Any:
    return await get_skill_categories_command(context)


@router.post(
    "",
    response_model=Skill,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def create_skill(
    context: Annotated[Context, Depends(ContextFactory.command)],
    data: SkillCreate,
) -> Any:
    return await create_skill_command(context, data=data)


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_skill(
    context: Annotated[Context, Depends(ContextFactory.command)],
    skill_id: EntityId,
) -> None:
    await delete_skill_command(context, skill_id=skill_id)


@router.patch(
    "/reorder",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def reorder_skills(
    context: Annotated[Context, Depends(ContextFactory.command)],
    data: list[EntityReorder],
) -> None:
    await reorder_skills_command(context, data=data)


@router.patch(
    "/categories/reorder",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def reorder_skill_categories(
    context: Annotated[Context, Depends(ContextFactory.command)],
    data: list[EntityReorder],
) -> None:
    await reorder_skill_categories_command(context, data=data)


@router.patch(
    "/categories/{category_id}",
    response_model=SkillCategory,
    dependencies=[Depends(get_current_user)],
)
async def update_skill_category(
    context: Annotated[Context, Depends(ContextFactory.command)],
    category_id: EntityId,
    data: SkillCategoryUpdate,
) -> Any:
    return await update_skill_category_command(
        context,
        category_id=category_id,
        data=data,
    )


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_skill_category(
    context: Annotated[Context, Depends(ContextFactory.command)],
    category_id: EntityId,
) -> None:
    await delete_skill_category_command(context, category_id=category_id)
