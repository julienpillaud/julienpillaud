from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response

from app.api.dependencies.app import AppContext, get_app_context, get_repository
from app.api.dependencies.user import get_current_user
from app.domain.resume.commands import get_resume_command
from app.infrastructure.repository import MongoRepository

router = APIRouter(prefix="/admin")


@router.get("", dependencies=[Depends(get_current_user)])
async def home_admin(
    request: Request,
    context: Annotated[AppContext, Depends(get_app_context)],
) -> Response:
    return context.templates.TemplateResponse(request=request, name="admin.html")


@router.get("/skills", dependencies=[Depends(get_current_user)])
async def admin_skills(
    request: Request,
    context: Annotated[AppContext, Depends(get_app_context)],
) -> Response:
    return context.templates.TemplateResponse(request=request, name="skills.html")


@router.get("/pdf", dependencies=[Depends(get_current_user)])
async def admin_pdf(
    request: Request,
    context: Annotated[AppContext, Depends(get_app_context)],
    repository: Annotated[MongoRepository, Depends(get_repository)],
) -> Response:
    resume = await get_resume_command(repository)
    return context.templates.TemplateResponse(
        request=request,
        name="resume/pdf.html",
        context={"format": "pdf", "resume": resume},
    )
