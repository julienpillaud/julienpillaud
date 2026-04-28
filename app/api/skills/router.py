from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.app import get_repository
from app.api.dependencies.user import get_current_user
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
from app.infrastructure.repository import MongoRepository

router = APIRouter(prefix="/skills")


@router.get(
    "",
    response_model=list[SkillCategory],
    dependencies=[Depends(get_current_user)],
)
async def get_skill_categories(
    repository: Annotated[MongoRepository, Depends(get_repository)],
) -> Any:
    return await get_skill_categories_command(repository)


@router.post(
    "",
    response_model=Skill,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def create_skill(
    repository: Annotated[MongoRepository, Depends(get_repository)],
    data: SkillCreate,
) -> Any:
    return await create_skill_command(repository, data=data)


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_skill(
    repository: Annotated[MongoRepository, Depends(get_repository)],
    skill_id: EntityId,
) -> None:
    await delete_skill_command(repository, skill_id=skill_id)


@router.patch(
    "/reorder",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def reorder_skills(
    repository: Annotated[MongoRepository, Depends(get_repository)],
    data: list[EntityReorder],
) -> None:
    await reorder_skills_command(repository, data=data)


@router.patch(
    "/categories/reorder",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def reorder_skill_categories(
    repository: Annotated[MongoRepository, Depends(get_repository)],
    data: list[EntityReorder],
) -> None:
    await reorder_skill_categories_command(repository, data=data)


@router.patch(
    "/categories/{category_id}",
    response_model=SkillCategory,
    dependencies=[Depends(get_current_user)],
)
async def update_skill_category(
    repository: Annotated[MongoRepository, Depends(get_repository)],
    category_id: EntityId,
    data: SkillCategoryUpdate,
) -> Any:
    return await update_skill_category_command(
        repository,
        category_id=category_id,
        data=data,
    )


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_skill_category(
    repository: Annotated[MongoRepository, Depends(get_repository)],
    category_id: EntityId,
) -> None:
    await delete_skill_category_command(repository, category_id=category_id)
