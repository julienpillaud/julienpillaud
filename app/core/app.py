import datetime
from pathlib import Path
from typing import Any

import logfire
from faker import Faker
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.settings import Settings

settings = Settings()
logfire.configure(
    send_to_logfire="if-token-present",
    token=settings.logfire_token,
    service_name="app",
    environment=settings.environment,
    console=False,
)

faker = Faker()
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

logfire.instrument_fastapi(app, capture_headers=True, extra_spans=True)

app_path = Path(__file__).resolve().parents[1]
template_path = app_path / "templates"
templates = Jinja2Templates(directory=template_path)


def generate_data(
    message: str,
    status_code: int = status.HTTP_200_OK,
) -> dict[str, Any]:
    return {
        "title": "CV",
        "message": message,
        "status_code": status_code,
        "status": "IN_PROGRESS" if status_code == status.HTTP_200_OK else "ERROR",
        "last_update": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    data = generate_data(message=faker.sentence())
    return templates.TemplateResponse(
        request=request,
        name="temp.html",
        context={"data": data},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> HTMLResponse:
    data = generate_data(
        message=exc.detail,
        status_code=exc.status_code,
    )
    return templates.TemplateResponse(
        request=request,
        name="temp.html",
        context={"data": data},
    )
