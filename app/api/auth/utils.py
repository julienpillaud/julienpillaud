from fastapi import Response, status
from fastapi.responses import RedirectResponse

from app.api.security import generate_tokens
from app.api.utils import set_cookie
from app.core.settings import Settings
from app.domain.entities import EntityId
from app.infrastructure.repository import MongoRepository


async def build_login_response(
    settings: Settings,
    repository: MongoRepository,
    user_id: EntityId,
) -> Response:
    # Generate tokens
    access_token, refresh_token = generate_tokens(
        settings=settings,
        user_id=user_id,
    )

    # Save refresh token in database
    await repository.save_token(refresh_token)

    # Create response with cookies
    response = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    set_cookie(
        response=response,
        key="access_token",
        value=access_token,
        max_age=settings.access_token_expire,
    )
    set_cookie(
        response=response,
        key="refresh_token",
        value=refresh_token.value,
        max_age=settings.refresh_token_expire,
    )
    return response
