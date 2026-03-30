from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from app.api.dependencies import AppContext, get_app_context
from app.domain.service import get_resume
from app.domain.utils import generate_data

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    context: Annotated[AppContext, Depends(get_app_context)],
) -> HTMLResponse:
    data = generate_data()
    resume = await get_resume(settings=context.settings, repository=context.repository)
    return context.templates.TemplateResponse(
        request=request,
        name="temp.html",
        context={
            "data": data.model_dump_json(indent=2),
            "resume": resume.model_dump_json(indent=2),
        },
    )
