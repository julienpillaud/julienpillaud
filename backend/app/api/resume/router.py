from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, StreamingResponse
from starlette.templating import Jinja2Templates

from app.api.dependencies.app import (
    get_domain,
    get_pdf_converter,
    get_templates,
)
from app.core.domain import Domain
from app.domain.pdf_converter import PDFConverterProtocol
from app.domain.resume.use_cases import get_resume

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> HTMLResponse:
    resume = await domain.run(get_resume)
    return templates.TemplateResponse(
        request=request,
        name="resume/base.html",
        context={"format": "html", "resume": resume},
    )


@router.get("/pdf/download")
async def download_pdf(
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    domain: Annotated[Domain, Depends(get_domain)],
    pdf_converter: Annotated[PDFConverterProtocol, Depends(get_pdf_converter)],
) -> StreamingResponse:
    resume = await domain.run(get_resume)
    html_content = templates.get_template("resume/pdf.html").render(
        {"format": "pdf", "resume": resume}
    )
    name = resume.metadata.contact.full_name.lower().replace(" ", "-")
    filename = f"{name}-cv.pdf"
    return StreamingResponse(
        pdf_converter.stream_pdf(html_content),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
