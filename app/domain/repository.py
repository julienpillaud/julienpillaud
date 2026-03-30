from typing import Protocol

from app.domain.entities import Experience


class RepositoryProtocol(Protocol):
    async def get_experiences(self) -> list[Experience]: ...
