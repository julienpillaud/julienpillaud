from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from app.core.settings import Settings


def mount_static(app: FastAPI, settings: Settings) -> None:
    app.mount(
        path="/static",
        app=StaticFiles(directory=settings.paths.static),
        name="static",
    )


def set_cookie(
    response: Response,
    /,
    key: str,
    value: str,
    max_age: int,
    secure: bool,
) -> None:
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        secure=secure,
        httponly=True,
        samesite="lax",
    )


def delete_cookie(response: Response, /, key: str, secure: bool) -> None:
    response.delete_cookie(
        key=key,
        secure=secure,
        httponly=True,
        samesite="lax",
    )
