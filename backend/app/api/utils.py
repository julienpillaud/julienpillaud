from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.settings import Settings
from app.domain.auth.entities import IssuedTokens


def mount_static(app: FastAPI, settings: Settings) -> None:
    app.mount(
        path="/static",
        app=StaticFiles(directory=settings.paths.static),
        name="static",
    )


# https://www.rfc-editor.org/info/rfc9110/#name-401-unauthorized
def unauthorized_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer, Cookie"},
    )


def build_response_with_cookies(
    settings: Settings,
    content: str,
    tokens: IssuedTokens,
) -> JSONResponse:
    response = JSONResponse(content=content, status_code=status.HTTP_200_OK)
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        max_age=settings.access_token_expire,
        secure=settings.cookie_secure,
        httponly=True,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        max_age=settings.refresh_token_expire,
        path="/api/auth",
        secure=settings.cookie_secure,
        httponly=True,
        samesite="lax",
    )
    return response


def build_logout_response(
    settings: Settings,
    content: str,
) -> JSONResponse:
    response = JSONResponse(content=content, status_code=status.HTTP_200_OK)
    response.delete_cookie(
        key="access_token",
        secure=settings.cookie_secure,
        httponly=True,
        samesite="lax",
    )
    response.delete_cookie(
        key="refresh_token",
        path="/api/auth",
        secure=settings.cookie_secure,
        httponly=True,
        samesite="lax",
    )
    return response
