from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.dependencies.app import get_templates
from app.api.exceptions import AuthorizationError
from app.api.logger import logger
from app.core.settings import Settings


def add_exception_handlers(app: FastAPI, settings: Settings) -> None:
    templates = get_templates(settings=settings)

    @app.exception_handler(AuthorizationError)
    async def auth_exception_handler(
        request: Request,
        exc: AuthorizationError,
    ) -> Response:
        exc_name = exc.__class__.__name__
        message = f"{request.method} {request.url.path} - {exc_name}: {exc}"
        logger.warning(message)
        return templates.TemplateResponse(request=request, name="error.html")

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ) -> Response:
        exc_name = exc.__class__.__name__
        message = f"{request.method} {request.url.path} - {exc_name}: {exc}"
        logger.warning(message)
        return templates.TemplateResponse(request=request, name="error.html")
