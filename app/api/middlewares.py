from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

from app.api.utils import set_cookie
from app.core.settings import Settings


def add_security_middleware(app: FastAPI, settings: Settings) -> None:
    @app.middleware("http")
    async def security_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        response = await call_next(request)

        # Get tokens set by dependency and set them as cookies
        access_token = getattr(request.state, "access_token", None)
        if access_token:
            set_cookie(
                response=response,
                key="access_token",
                value=access_token,
                max_age=settings.access_token_expire,
            )
        refresh_token = getattr(request.state, "refresh_token", None)
        if refresh_token:
            set_cookie(
                response=response,
                key="refresh_token",
                value=refresh_token,
                max_age=settings.refresh_token_expire,
            )
        return response
