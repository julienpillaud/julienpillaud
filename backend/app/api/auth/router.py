from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.app import get_domain, get_settings
from app.api.dependencies.user import get_current_user
from app.api.exceptions import SecurityError
from app.api.utils import (
    build_logout_response,
    build_response_with_cookies,
    unauthorized_exception,
)
from app.core.domain import Domain
from app.core.logger import logger
from app.core.settings import Settings
from app.domain.auth.use_cases import (
    create_session,
    generate_access_token,
    refresh_session,
)
from app.domain.exceptions import ForbiddenError, NotFoundError
from app.domain.users.entities import UserPublic
from app.domain.users.use_cases import authenticate_user, logout_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> Response:
    try:
        current_user = await domain.run(
            authenticate_user,
            username=form_data.username,
            password=form_data.password,
        )
    except NotFoundError, ForbiddenError:
        raise unauthorized_exception(detail="Invalid credentials") from None

    issued_tokens = await domain.run(
        create_session,
        settings=settings,
        user_id=current_user.id,
    )
    logger.info(f"User '{current_user.id}' - Logged in")
    return build_response_with_cookies(
        settings=settings,
        content="Logged in",
        tokens=issued_tokens,
    )


@router.post("/token")
async def post_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> dict[str, str]:
    try:
        current_user = await domain.run(
            authenticate_user,
            username=form_data.username,
            password=form_data.password,
        )
    except NotFoundError, ForbiddenError:
        raise unauthorized_exception(detail="Invalid credentials") from None

    access_token = generate_access_token(
        settings=settings,
        user_id=current_user.id,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_me(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
) -> UserPublic:
    return current_user


@router.post("/refresh")
async def refresh(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> Response:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        logger.warning("No valid token found")
        raise unauthorized_exception(detail="No valid token found")

    try:
        issued_tokens = await domain.run(
            refresh_session,
            settings=settings,
            raw_value=refresh_token,
        )
    except SecurityError as error:
        raise unauthorized_exception(detail=str(error)) from error

    return build_response_with_cookies(
        settings=settings,
        content="Session refreshed",
        tokens=issued_tokens,
    )


@router.post("/logout")
async def logout(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> Response:
    await domain.run(logout_user, user_id=current_user.id)
    logger.info(f"User '{current_user.id}' - Logged out")
    return build_logout_response(settings=settings, content="Logged out")
