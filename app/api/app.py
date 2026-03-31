from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.dependencies import get_templates
from app.api.router import router
from app.core.settings import Settings


def create_fastapi_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    add_exception_handlers(app=app, settings=settings)
    mount_static(app=app, settings=settings)
    app.include_router(router)
    return app


def add_exception_handlers(app: FastAPI, settings: Settings) -> None:
    templates = get_templates(settings=settings)  # noqa: F841

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ) -> RedirectResponse:
        return RedirectResponse(url=request.url_for("home"))


def mount_static(app: FastAPI, settings: Settings) -> None:
    app.mount(
        path="/static",
        app=StaticFiles(directory=settings.paths.static),
        name="static",
    )
