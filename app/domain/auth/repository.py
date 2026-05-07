from typing import Protocol

from app.domain.auth.entities import RefreshToken
from app.domain.entities import EntityId


class RefreshTokenRepositoryProtocol(Protocol):
    async def save(self, entity: RefreshToken, /) -> None: ...

    async def get_by_hash(self, value: str, /) -> RefreshToken | None: ...

    async def revoke(self, token_id: EntityId) -> None: ...

    async def revoke_for_user(self, user_id: EntityId) -> None: ...
