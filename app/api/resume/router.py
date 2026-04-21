from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, StreamingResponse

from app.api.dependencies.app import AppContext, get_app_context
from app.api.dependencies.user import get_optional_current_user
from app.domain.admin.entities import UserExternal
from app.domain.resume.commands import get_resume_command

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    current_user: Annotated[UserExternal | None, Depends(get_optional_current_user)],
    context: Annotated[AppContext, Depends(get_app_context)],
) -> HTMLResponse:
    resume = await get_resume_command(context.repository)
    return context.templates.TemplateResponse(
        request=request,
        name="resume/base.html",
        context={
            "format": "html",
            "resume": resume,
            "current_user": current_user,
        },
    )


@router.get("/pdf/download")
async def download_pdf(
    context: Annotated[AppContext, Depends(get_app_context)],
) -> StreamingResponse:
    resume = await get_resume_command(context.repository)
    html = context.templates.get_template("resume/pdf.html").render(
        {"format": "pdf", "resume": resume}
    )
    name = resume.metadata.contact.full_name.lower().replace(" ", "-")
    filename = f"{name}-cv.pdf"
    return StreamingResponse(
        context.pdf_converter.stream_pdf(html),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
