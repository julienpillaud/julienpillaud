from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.dependencies.app import (
    get_domain,
)
from app.api.resume.schemas import Resume
from app.core.domain import Domain
from app.domain.resume.use_cases import get_resume

router = APIRouter(prefix="/api/resume", tags=["Resume"])


@router.get("", response_model=Resume)
async def get_resume_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
) -> Any:  # noqa: ANN401
    return await domain.run(get_resume)


# @router.get("/pdf/download")
# async def download_pdf(
#     templates: Annotated[Jinja2Templates, Depends(get_templates)],
#     domain: Annotated[Domain, Depends(get_domain)],
#     pdf_converter: Annotated[PDFConverterProtocol, Depends(get_pdf_converter)],
# ) -> StreamingResponse:
#     resume = await domain.run(get_resume)
#     html_content = templates.get_template("resume/pdf.html").render(
#         {"format": "pdf", "resume": resume}
#     )
#     name = resume.metadata.contact.full_name.lower().replace(" ", "-")
#     filename = f"{name}-cv.pdf"
#     return StreamingResponse(
#         pdf_converter.stream_pdf(html_content),
#         media_type="application/pdf",
#         headers={"Content-Disposition": f"attachment; filename={filename}"},
#     )
