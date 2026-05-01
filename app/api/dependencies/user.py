from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from app.api.dependencies.app import get_context, get_settings
from app.api.exceptions import AuthorizationError
from app.api.logger import logger
from app.api.security import (
    decode_access_token,
    generate_access_token,
    rotate_refresh_token,
)
from app.core.context import Context
from app.core.settings import Settings
from app.domain.admin.commands import get_user
from app.domain.admin.entities import UserExternal
from app.domain.context import ContextProtocol
from app.domain.exceptions import NotFoundError


async def get_current_user(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    context: Annotated[Context, Depends(get_context)],
) -> UserExternal:
    user = await _get_user_from_tokens(
        request=request,
        settings=settings,
        context=context,
    )
    if not user:
        logger.warning("No valid token found")
        raise AuthorizationError("No valid token found")

    return user


async def get_optional_current_user(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    context: Annotated[Context, Depends(get_context)],
) -> UserExternal | None:
    return await _get_user_from_tokens(
        request=request,
        settings=settings,
        context=context,
    )


async def _get_user_from_tokens(
    request: Request,
    settings: Settings,
    context: ContextProtocol,
) -> UserExternal | None:
    request.state.access_token = None
    request.state.refresh_token = None

    access_token = request.cookies.get("access_token")
    if access_token:
        return await _get_user_from_access_token(
            access_token=access_token,
            settings=settings,
            context=context,
        )

    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        return await _get_user_from_refresh_token(
            request=request,
            refresh_token=refresh_token,
            settings=settings,
            context=context,
        )

    # None of the tokens were found
    return None


async def _get_user_from_access_token(
    access_token: str,
    settings: Settings,
    context: ContextProtocol,
) -> UserExternal:
    access_payload = decode_access_token(settings=settings, value=access_token)
    try:
        return await get_user(context, user_id=access_payload.sub)
    except NotFoundError as error:
        logger.warning("User not found")
        raise AuthorizationError("User not found") from error


async def _get_user_from_refresh_token(
    request: Request,
    refresh_token: str,
    settings: Settings,
    context: ContextProtocol,
) -> UserExternal:
    new_refresh_token = await rotate_refresh_token(
        settings=settings,
        context=context,
        refresh_token=refresh_token,
    )

    try:
        user = await get_user(context, user_id=new_refresh_token.user_id)
    except NotFoundError as error:
        logger.warning("User not found")
        raise AuthorizationError("User not found") from error

    new_acces_token = generate_access_token(settings=settings, user_id=user.id)
    request.state.access_token = new_acces_token
    request.state.refresh_token = new_refresh_token.value
    return user
