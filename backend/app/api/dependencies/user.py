import secrets
from typing import Annotated

from fastapi import Depends
from fastapi.security import (
    APIKeyCookie,
    HTTPBasic,
    HTTPBasicCredentials,
    OAuth2PasswordBearer,
)

from app.api.dependencies.app import get_domain, get_settings
from app.api.exceptions import InvalidAccessTokenError
from app.api.security import decode_access_token
from app.api.utils import unauthorized_exception
from app.core.domain import Domain
from app.core.logger import logger
from app.core.settings import Settings
from app.domain.exceptions import NotFoundError
from app.domain.users.entities import UserPublic
from app.domain.users.use_cases import get_user

basic_scheme = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token", auto_error=False)
cookie_scheme = APIKeyCookie(name="access_token", auto_error=False)


def check_docs_access(
    settings: Annotated[Settings, Depends(get_settings)],
    credentials: Annotated[HTTPBasicCredentials, Depends(basic_scheme)],
) -> bool:
    is_correct_username = secrets.compare_digest(
        credentials.username.encode("utf8"),
        settings.basic_username.encode("utf8"),
    )
    is_correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"),
        settings.basic_password.encode("utf8"),
    )
    if not (is_correct_username and is_correct_password):
        logger.warning("Docs access check failed")
        raise unauthorized_exception(detail="Invalid credentials")

    return True


async def get_current_user(
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
    bearer_token: Annotated[str | None, Depends(oauth2_scheme)],
    cookie_token: Annotated[str | None, Depends(cookie_scheme)],
) -> UserPublic:
    access_token = bearer_token or cookie_token
    if not access_token:
        logger.warning("No valid token found")
        raise unauthorized_exception(detail="No valid token found")

    try:
        access_payload = decode_access_token(settings=settings, value=access_token)
    except InvalidAccessTokenError as error:
        raise unauthorized_exception(detail=str(error)) from error

    try:
        return await domain.run(get_user, user_id=access_payload.sub)
    except NotFoundError as error:
        raise unauthorized_exception(detail="Not authenticated") from error
