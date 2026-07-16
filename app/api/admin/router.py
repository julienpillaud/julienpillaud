from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies.app import get_domain, get_templates
from app.api.dependencies.user import get_current_user
from app.core.domain import Domain
from app.domain.resume.use_cases import get_resume

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
    domain: Annotated[Domain, Depends(get_domain)],
) -> Response:
    resume = await domain.run(get_resume)
    return templates.TemplateResponse(
        request=request,
        name="resume/pdf.html",
        context={"format": "pdf", "resume": resume},
    )
