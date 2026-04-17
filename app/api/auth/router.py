from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth.utils import build_login_response
from app.api.dependencies.app import AppContext, get_app_context
from app.api.dependencies.user import get_current_user, get_optional_current_user
from app.api.logger import logger
from app.domain.admin.commands import authenticate_user, revoke_all_tokens_for_user
from app.domain.admin.entities import UserExternal
from app.domain.exceptions import ForbiddenError, NotFoundError

router = APIRouter(prefix="/auth")


@router.get("")
async def get_login(
    request: Request,
    current_user: Annotated[UserExternal | None, Depends(get_optional_current_user)],
    context: Annotated[AppContext, Depends(get_app_context)],
) -> Response:
    if current_user:
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

    message = request.cookies.pop("message", None)
    response = context.templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": message},
    )
    response.delete_cookie(key="message")
    return response


@router.post("")
async def post_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    context: Annotated[AppContext, Depends(get_app_context)],
) -> Response:
    try:
        current_user = await authenticate_user(
            context.repository,
            username=form_data.username,
            password=form_data.password,
        )
    except NotFoundError, ForbiddenError:
        logger.warning("Invalid credentials")
        response = RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="message", value="Invalid credentials", max_age=10)
        return response

    logger.info(f"User {current_user.id} logged in")
    return await build_login_response(context=context, user_id=current_user.id)


@router.post("/logout")
async def logout(
    current_user: Annotated[UserExternal, Depends(get_current_user)],
    context: Annotated[AppContext, Depends(get_app_context)],
) -> Response:
    await revoke_all_tokens_for_user(context.repository, user_id=current_user.id)

    response = RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    logger.info(f"User {current_user.id} logged out")
    return response
