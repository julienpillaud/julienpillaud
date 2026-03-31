from typing import Protocol

from app.domain.entities import Experience, Metadata, Skill


class RepositoryProtocol(Protocol):
    async def get_metadata(self) -> Metadata: ...

    async def get_experiences(self) -> list[Experience]: ...

    async def get_skills(self) -> list[Skill]: ...
