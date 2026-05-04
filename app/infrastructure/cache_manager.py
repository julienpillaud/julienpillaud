from typing import cast

from redis.asyncio import Redis

from app.core.settings import Settings
from app.domain.cache_manager import CacheManagerProtocol
from app.infrastructure.logger import logger


async def create_redis_client(settings: Settings) -> Redis:
    client = Redis.from_url(
        str(settings.redis_dsn),
        decode_responses=True,
    )
    await client.info()
    logger.info("Redis client up")
    return client


class RedisCacheManager(CacheManagerProtocol):
    def __init__(self, client: Redis) -> None:
        self.client = client

    async def set(self, key: str, value: str, ttl: int = 3600) -> None:
        await self.client.set(name=key, value=value, ex=ttl)

    async def get(self, key: str) -> str | None:
        result = await self.client.get(name=key)
        return cast(str | None, result)

    async def delete(self, key: str) -> None:
        await self.client.delete(key)
