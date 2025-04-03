import logging
from functools import lru_cache
from typing import Optional

from db import redis_service_instance
from fastapi import Depends
from redis.asyncio import Redis
from services.interfaces import ICacheService


class RedisCacheService(ICacheService):
    """A cache service implementation backed by Redis."""

    def __init__(self, redis: Redis) -> None:
        """Initialize the RedisCacheService.

        Args:
            redis (Redis): The Redis client instance.
        """
        self._redis = redis

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> None:
        """Store a value in Redis with an optional expiration time."""
        await self._redis.set(key, value, ex=ex)
        logging.info("Key '%s' set in Redis with TTL %s.", key, ex)

    async def get(self, key: str) -> Optional[str]:
        """Retrieve a value from Redis by key."""
        value = await self._redis.get(key)
        logging.info("Retrieved key '%s' from Redis with value: %s.", key, value)
        return value

    async def delete(self, key: str) -> None:
        """Delete a key-value pair from Redis."""
        await self._redis.delete(key)
        logging.info("Key '%s' deleted from Redis.", key)

    async def exists(self, key: str) -> bool:
        """Check if a key exists in Redis."""
        exists = await self._redis.exists(key)
        logging.info("Key '%s' exists in Redis: %s.", key, bool(exists))
        return bool(exists)


@lru_cache()
def get_cache_service(
    redis: Redis = Depends(redis_service_instance.get_connection),
) -> ICacheService:
    """Provide a RedisCacheService instance."""
    return RedisCacheService(redis)
