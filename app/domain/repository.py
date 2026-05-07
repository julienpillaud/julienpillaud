from typing import Protocol

from app.domain.resume.entities import Experience, Metadata


class RepositoryProtocol(Protocol):
    async def get_metadata(self) -> Metadata: ...

    async def get_experiences(self) -> list[Experience]: ...
