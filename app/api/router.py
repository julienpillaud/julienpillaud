from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, StreamingResponse

from app.api.dependencies import AppContext, get_app_context
from app.api.security import check_api_key
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
        name="html/cv.html",
        context={"resume": resume},
    )


@router.get("/pdf/download")
async def download_pdf(
    context: Annotated[AppContext, Depends(get_app_context)],
) -> StreamingResponse:
    resume = await get_resume(repository=context.repository)
    html = context.templates.get_template("pdf/cv.html").render({"resume": resume})
    return StreamingResponse(
        context.pdf_converter.stream_pdf(html),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=cv.pdf"},
    )


@router.get("/pdf/view", dependencies=[Depends(check_api_key)])
async def view_pdf(
    request: Request,
    context: Annotated[AppContext, Depends(get_app_context)],
) -> HTMLResponse:
    resume = await get_resume(repository=context.repository)
    return context.templates.TemplateResponse(
        request=request,
        name="pdf/cv.html",
        context={"resume": resume},
    )
