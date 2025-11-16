from app.core.cache.memory_cache import memory_cache
from app.core.cache.protocols import CacheProtocol
from app.core.cache.redis_cache import redis_cache
from app.core.config import settings


def get_cache_instance() -> CacheProtocol:
    """
    Фабрика: возвращает нужный кэш по настройке.
    """
    if settings.CACHE_STORAGE == "redis":
        return redis_cache
    elif settings.CACHE_STORAGE == "memory":
        return memory_cache
    else:
        raise ValueError(f"Unknown CACHE_STORAGE: {settings.CACHE_STORAGE}")
