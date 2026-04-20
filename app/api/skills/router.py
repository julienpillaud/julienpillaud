from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.app import AppContext, get_app_context
from app.api.dependencies.user import get_current_user
from app.domain.entities import EntityId
from app.domain.skills.commands import (
    create_skill_command,
    delete_skill_command,
    delete_skills_by_category_command,
    get_skills_command,
    update_skill_command,
)
from app.domain.skills.entities import Skill, SkillCreate, SkillSummary, SkillUpdate

router = APIRouter(prefix="/skills")


@router.get(
    "",
    response_model=list[SkillSummary],
    dependencies=[Depends(get_current_user)],
)
async def get_skills(context: Annotated[AppContext, Depends(get_app_context)]) -> Any:
    return await get_skills_command(context.repository)


@router.post(
    "",
    response_model=Skill,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def create_skill(
    context: Annotated[AppContext, Depends(get_app_context)],
    data: SkillCreate,
) -> Any:
    return await create_skill_command(context.repository, data=data)


@router.patch(
    "/{skill_id}",
    response_model=Skill,
    dependencies=[Depends(get_current_user)],
)
async def update_skill(
    context: Annotated[AppContext, Depends(get_app_context)],
    skill_id: EntityId,
    data: SkillUpdate,
) -> Any:
    return await update_skill_command(context.repository, skill_id=skill_id, data=data)


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_skill(
    context: Annotated[AppContext, Depends(get_app_context)],
    skill_id: EntityId,
) -> None:
    await delete_skill_command(context.repository, skill_id=skill_id)


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_skills_by_category(
    context: Annotated[AppContext, Depends(get_app_context)],
    category_id: EntityId,
) -> None:
    await delete_skills_by_category_command(context.repository, category_id=category_id)
