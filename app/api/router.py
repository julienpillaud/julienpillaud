from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from app.api.dependencies import AppContext, get_app_context
from app.domain.service import get_resume

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    context: Annotated[AppContext, Depends(get_app_context)],
) -> HTMLResponse:
    resume = await get_resume(repository=context.repository)
    return context.templates.TemplateResponse(
        request=request,
        name="cv.html",
        context={"resume": resume},
    )
