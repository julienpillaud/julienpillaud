import datetime
import secrets
import uuid

import jwt
from pydantic import BaseModel, ValidationError

from app.api.exceptions import InvalidAccessToken, InvalidRefreshToken
from app.api.logger import logger
from app.core.settings import Settings
from app.domain.admin.commands import revoke_all_tokens_for_user
from app.domain.admin.entities import RefreshTokenExternal, hash_token
from app.domain.entities import EntityId
from app.domain.repository import RepositoryProtocol


class TokenPayload(BaseModel):
    sub: uuid.UUID
    exp: datetime.datetime
    iat: datetime.datetime


def decode_access_token(settings: Settings, value: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            jwt=value,
            key=settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError as error:
        logger.warning("Token expired")
        raise InvalidAccessToken("Token expired") from error
    except jwt.PyJWTError as error:
        logger.warning("Could not decode token")
        raise InvalidAccessToken("Could not decode token") from error

    try:
        return TokenPayload.model_validate(payload)
    except ValidationError as error:
        logger.warning("Invalid token payload")
        raise InvalidAccessToken("Invalid token payload") from error


def generate_tokens(
    settings: Settings,
    user_id: EntityId,
) -> tuple[str, RefreshTokenExternal]:
    current_date = datetime.datetime.now(datetime.UTC)
    access_token = generate_access_token(
        settings=settings,
        user_id=user_id,
        current_date=current_date,
    )
    refresh_token = generate_refresh_token(
        settings=settings,
        user_id=user_id,
        current_date=current_date,
    )
    return access_token, refresh_token


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
    user_id: EntityId,
    current_date: datetime.datetime,
) -> RefreshTokenExternal:
    delta = datetime.timedelta(seconds=settings.refresh_token_expire)
    return RefreshTokenExternal(
        value=secrets.token_urlsafe(32),
        user_id=user_id,
        created_at=current_date,
        expires_at=current_date + delta,
    )


async def rotate_refresh_token(
    settings: Settings,
    repository: RepositoryProtocol,
    refresh_token: str,
) -> RefreshTokenExternal:
    previous_token = await repository.get_token_by_hash(hash_token(refresh_token))
    if not previous_token:
        logger.warning("Invalid refresh token")
        raise InvalidRefreshToken("Invalid refresh token")

    if previous_token.revoked_at:
        await revoke_all_tokens_for_user(repository, user_id=previous_token.user_id)
        logger.error("Refresh token reuse detected")
        raise InvalidRefreshToken("Refresh token reuse detected")

    await repository.revoke_token(token_id=previous_token.id)

    new_token = generate_refresh_token(
        settings=settings,
        user_id=previous_token.user_id,
        current_date=datetime.datetime.now(datetime.UTC),
    )
    await repository.save_token(new_token)
    return new_token
