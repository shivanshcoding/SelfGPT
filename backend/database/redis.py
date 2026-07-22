"""
SelfGPT — Database: Redis

Provides async Redis client for caching, short-term memory, and session storage.
"""

import redis.asyncio as aioredis

from config.settings import get_settings

_redis_client: aioredis.Redis | None = None


async def init_redis() -> aioredis.Redis:
    """Create and return the Redis connection pool."""
    global _redis_client
    settings = get_settings()
    _redis_client = aioredis.from_url(
        settings.redis_url,
        decode_responses=True,
        max_connections=20,
    )
    # Verify connectivity
    await _redis_client.ping()
    return _redis_client


async def close_redis():
    """Gracefully close the Redis connection pool."""
    global _redis_client
    if _redis_client:
        await _redis_client.aclose()
        _redis_client = None


def get_redis() -> aioredis.Redis:
    """Return the active Redis client."""
    if _redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return _redis_client
