from typing import Optional

import redis.asyncio as redis

from app.core.cache.protocols import CacheProtocol
from app.core.config import settings
from app.core.logger.factory import get_logger

DEFAULT_CACHE_TTL = 3600

logger = get_logger()


class RedisCache(CacheProtocol):
    def __init__(self):
        self.client: Optional[redis.Redis] = None

    async def connect(self):
        if self.client is None:
            self.client = redis.from_url(
                settings.CACHE_REDIS_URL, decode_responses=True
            )
            await self.client.ping()
            logger.info("Redis cache connected")
        return self

    async def get(self, key: str) -> Optional[str]:
        if not self.client:
            await self.connect()
        return await self.client.get(key)

    async def set(self, key: str, value: str, ttl: int = DEFAULT_CACHE_TTL):
        if not self.client:
            await self.connect()
        await self.client.setex(key, ttl, value)

    async def delete(self, key: str):
        if not self.client:
            await self.connect()
        await self.client.delete(key)

    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None
            logger.info("Redis cache closed")


# Singleton
redis_cache = RedisCache()
