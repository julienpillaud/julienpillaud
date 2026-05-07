import datetime
import hashlib
import secrets
import uuid

import jwt

from app.core.settings import Settings
from app.domain.auth.entities import IssuedTokens, RefreshToken
from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.exceptions import InvalidRefreshToken
from app.domain.users.commands import logout_user_command


async def create_session_command(
    context: ContextProtocol,
    /,
    settings: Settings,
    user_id: EntityId,
) -> IssuedTokens:
    current_date = datetime.datetime.now(datetime.UTC)
    access_token = generate_access_token(
        settings=settings,
        user_id=user_id,
        current_date=current_date,
    )
    raw_refresh_token = secrets.token_urlsafe(32)
    refresh_token = generate_refresh_token(
        settings=settings,
        raw_value=raw_refresh_token,
        user_id=user_id,
        current_date=current_date,
    )
    await context.refresh_token_repository.save(refresh_token)
    return IssuedTokens(
        access_token=access_token,
        refresh_token=raw_refresh_token,
        user_id=user_id,
    )


async def refresh_session_command(
    context: ContextProtocol,
    /,
    settings: Settings,
    raw_value: str,
) -> IssuedTokens:
    previous_token = await context.refresh_token_repository.get_by_hash(
        hash_refresh_token(raw_value)
    )
    if not previous_token:
        raise InvalidRefreshToken("Invalid refresh token")

    if previous_token.revoked_at:
        await logout_user_command(context, user_id=previous_token.user_id)
        raise InvalidRefreshToken("Refresh token reuse detected")

    if not previous_token.is_valid:
        raise InvalidRefreshToken("Refresh token expired")

    await context.refresh_token_repository.revoke(token_id=previous_token.id)

    return await create_session_command(
        context,
        settings=settings,
        user_id=previous_token.user_id,
    )


def generate_access_token(
    settings: Settings,
    user_id: EntityId,
    current_date: datetime.datetime | None = None,
) -> str:
    current_date = current_date or datetime.datetime.now(datetime.UTC)
    delta = datetime.timedelta(seconds=settings.access_token_expire)
    return jwt.encode(
        payload={
            "sub": str(user_id),
            "exp": current_date + delta,
            "iat": current_date,
        },
        key=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def generate_refresh_token(
    settings: Settings,
    raw_value: str,
    user_id: EntityId,
    current_date: datetime.datetime | None = None,
) -> RefreshToken:
    current_date = current_date or datetime.datetime.now(datetime.UTC)
    delta = datetime.timedelta(seconds=settings.refresh_token_expire)
    return RefreshToken(
        id=uuid.uuid7(),
        hash_value=hash_refresh_token(raw_value),
        user_id=user_id,
        created_at=current_date,
        expires_at=current_date + delta,
    )


def hash_refresh_token(value: str, /) -> str:
    return hashlib.sha256(value.encode()).hexdigest()
