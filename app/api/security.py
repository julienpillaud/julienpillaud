from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyQuery

from app.api.dependencies import AppContext, get_app_context

query_scheme = APIKeyQuery(name="api_key")


def check_api_key(
    context: Annotated[AppContext, Depends(get_app_context)],
    api_key: Annotated[str, Depends(query_scheme)],
) -> None:
    if api_key != context.settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
