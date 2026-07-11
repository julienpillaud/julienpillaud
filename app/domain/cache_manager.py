from typing import Any, Protocol


class CacheManagerProtocol(Protocol):
    async def set(self, key: str, value: str, ttl: int = 3600) -> None: ...

    async def get(self, key: str) -> Any | None: ...  # noqa: ANN401

    async def delete(self, key: str) -> None: ...
