from typing import Protocol

from app.domain.entities import EntityId
from app.domain.users.entities import User


class UserRepositoryProtocol(Protocol):
    async def get_by_id(self, user_id: EntityId) -> User | None: ...

    async def get_by_username(self, username: str) -> User | None: ...
