import logging

from core.config import settings
from db.base import BaseService
from redis.asyncio import Redis


class RedisService(BaseService[Redis]):
    """Service handling the Redis connection."""

    def __init__(self) -> None:
        """Initialize the RedisService with no active connection by default."""
        self.connection: Redis | None = None

    async def init(self) -> None:
        """Initialize the Redis connection."""
        if self.connection is None:
            self.connection = Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                decode_responses=True,
            )
            logging.info("Redis connection initialized.")
