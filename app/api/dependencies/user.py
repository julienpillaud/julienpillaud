from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from app.api.dependencies.app import get_domain, get_settings
from app.api.logger import logger
from app.api.security import decode_access_token
from app.core.domain import Domain
from app.core.settings import Settings
from app.domain.auth.use_cases import refresh_session
from app.domain.exceptions import AuthorizationError, NotFoundError
from app.domain.users.entities import UserPublic
from app.domain.users.use_cases import get_user


async def get_current_user(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> UserPublic:
    user = await _get_user_from_tokens(
        request=request,
        settings=settings,
        domain=domain,
    )
    if not user:
        logger.warning("No valid token found")
        raise AuthorizationError("No valid token found")

    return user


async def get_optional_current_user(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> UserPublic | None:
    return await _get_user_from_tokens(
        request=request,
        settings=settings,
        domain=domain,
    )


async def _get_user_from_tokens(
    request: Request,
    settings: Settings,
    domain: Domain,
) -> UserPublic | None:
    request.state.access_token = None
    request.state.refresh_token = None

    access_token = request.cookies.get("access_token")
    if access_token:
        return await _get_user_from_access_token(
            access_token=access_token,
            settings=settings,
            domain=domain,
        )

    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        return await _get_user_from_refresh_token(
            request=request,
            refresh_token=refresh_token,
            settings=settings,
            domain=domain,
        )

    # None of the tokens were found
    return None


async def _get_user_from_access_token(
    access_token: str,
    settings: Settings,
    domain: Domain,
) -> UserPublic:
    access_payload = decode_access_token(settings=settings, value=access_token)
    try:
        return await domain.query(get_user, user_id=access_payload.sub)
    except NotFoundError as error:
        raise AuthorizationError("User not found") from error


async def _get_user_from_refresh_token(
    request: Request,
    refresh_token: str,
    settings: Settings,
    domain: Domain,
) -> UserPublic:
    issued_tokens = await domain.command(
        refresh_session,
        settings=settings,
        raw_value=refresh_token,
    )

    try:
        user = await domain.query(get_user, user_id=issued_tokens.user_id)
    except NotFoundError as error:
        raise AuthorizationError("User not found") from error

    request.state.access_token = issued_tokens.access_token
    request.state.refresh_token = issued_tokens.refresh_token
    return user
