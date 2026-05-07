import datetime
import uuid

import jwt
from pydantic import BaseModel, ValidationError

from app.core.settings import Settings
from app.domain.exceptions import InvalidAccessToken


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
        raise InvalidAccessToken("Token expired") from error
    except jwt.PyJWTError as error:
        raise InvalidAccessToken("Could not decode token") from error

    try:
        return TokenPayload.model_validate(payload)
    except ValidationError as error:
        raise InvalidAccessToken("Invalid token payload") from error
