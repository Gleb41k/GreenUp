from collections import OrderedDict
from typing import Optional

from app.core.cache.protocols import CacheProtocol


class InMemoryCache(CacheProtocol):
    def __init__(self, max_size: int = 1000):
        self.store = OrderedDict()
        self.max_size = max_size

    async def connect(self):
        return self

    async def get(self, key: str) -> Optional[str]:
        if key in self.store:
            self.store.move_to_end(key)
            return self.store[key]
        return None

    async def set(self, key: str, value: str, ttl: int = 3600):
        if len(self.store) >= self.max_size:
            self.store.popitem(last=False)
        self.store[key] = value
        self.store.move_to_end(key)

    async def delete(self, key: str):
        self.store.pop(key, None)

    async def close(self):
        self.store.clear()


# Singleton
memory_cache = InMemoryCache()
