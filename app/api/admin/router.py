from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies.app import get_context, get_templates
from app.api.dependencies.user import get_current_user
from app.core.context import Context
from app.domain.resume.commands import get_resume_command

router = APIRouter(prefix="/admin")


@router.get("", dependencies=[Depends(get_current_user)])
async def home_admin(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    return templates.TemplateResponse(request=request, name="admin.html")


@router.get("/skills", dependencies=[Depends(get_current_user)])
async def admin_skills(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    return templates.TemplateResponse(request=request, name="skills.html")


@router.get("/pdf", dependencies=[Depends(get_current_user)])
async def admin_pdf(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    context: Annotated[Context, Depends(get_context)],
) -> Response:
    resume = await get_resume_command(context)
    return templates.TemplateResponse(
        request=request,
        name="resume/pdf.html",
        context={"format": "pdf", "resume": resume},
    )
