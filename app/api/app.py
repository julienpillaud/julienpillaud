from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.dependencies import get_templates
from app.api.router import router
from app.core.settings import Settings
from app.domain.utils import generate_data


def create_fastapi_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    add_exception_handlers(app=app, settings=settings)
    app.include_router(router)
    return app


def add_exception_handlers(app: FastAPI, settings: Settings) -> None:
    templates = get_templates(settings=settings)

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
            context={"data": data.model_dump_json(indent=2)},
        )
