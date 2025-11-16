from typing import AsyncGenerator

from app.core.cache import get_cache_instance
from app.core.cache.protocols import CacheProtocol


async def get_cache() -> AsyncGenerator[CacheProtocol, None]:
    cache: CacheProtocol = get_cache_instance()
    await cache.connect()
    try:
        yield cache
    finally:
        await cache.close()
