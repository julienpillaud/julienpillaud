from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response

from app.api.dependencies.app import AppContext, get_app_context
from app.api.dependencies.user import get_current_user
from app.domain.resume.commands import get_resume_command

router = APIRouter(prefix="/admin")


@router.get("", dependencies=[Depends(get_current_user)])
async def home_admin(
    request: Request,
    context: Annotated[AppContext, Depends(get_app_context)],
) -> Response:
    return context.templates.TemplateResponse(request=request, name="admin.html")


@router.get("/pdf", dependencies=[Depends(get_current_user)])
async def view_pdf(
    request: Request,
    context: Annotated[AppContext, Depends(get_app_context)],
) -> Response:
    resume = await get_resume_command(context.repository)
    return context.templates.TemplateResponse(
        request=request,
        name="resume/pdf.html",
        context={"format": "pdf", "resume": resume},
    )
