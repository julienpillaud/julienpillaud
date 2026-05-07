from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.api.dependencies.app import ContextFactory, get_settings, get_templates
from app.api.dependencies.user import get_current_user, get_optional_current_user
from app.api.logger import logger
from app.api.utils import delete_cookie, set_cookie
from app.core.context import Context
from app.core.settings import Settings
from app.domain.auth.commands import create_session_command
from app.domain.exceptions import ForbiddenError, NotFoundError
from app.domain.users.commands import authenticate_user_command, logout_user_command
from app.domain.users.entities import UserPublic

router = APIRouter(prefix="/auth")


@router.get("")
async def get_login(
    request: Request,
    current_user: Annotated[UserPublic | None, Depends(get_optional_current_user)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    if current_user:
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

    message = request.cookies.pop("message", None)
    response = templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": message},
    )
    response.delete_cookie(key="message")
    return response


@router.post("")
async def post_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
    context: Annotated[Context, Depends(ContextFactory.command)],
) -> Response:
    try:
        current_user = await authenticate_user_command(
            context,
            username=form_data.username,
            password=form_data.password,
        )
    except NotFoundError, ForbiddenError:
        response = RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="message", value="Invalid credentials", max_age=10)
        return response

    issued_tokens = await create_session_command(
        context,
        settings=settings,
        user_id=current_user.id,
    )

    logger.info(f"User '{current_user.id}' - Logged in")
    response = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    set_cookie(
        response,
        key="access_token",
        value=issued_tokens.access_token,
        max_age=settings.access_token_expire,
        secure=settings.cookie_secure,
    )
    set_cookie(
        response,
        key="refresh_token",
        value=issued_tokens.refresh_token,
        max_age=settings.refresh_token_expire,
        secure=settings.cookie_secure,
    )
    return response


@router.post("/logout")
async def logout(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
    context: Annotated[Context, Depends(ContextFactory.command)],
) -> Response:
    await logout_user_command(context, user_id=current_user.id)

    response = RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)
    delete_cookie(response, key="access_token", secure=settings.cookie_secure)
    delete_cookie(response, key="refresh_token", secure=settings.cookie_secure)

    logger.info(f"User '{current_user.id}' - Logged out")
    return response
