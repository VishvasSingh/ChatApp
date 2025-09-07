import redis.asyncio as aioredis
import logging
from app.core.config import app_settings

# This object will hold the Redis connection pool instance
redis_client: aioredis.Redis = None

logger = logging.getLogger(__name__)


async def get_redis_client() -> aioredis.Redis:
    """
    Dependency function to get the Redis client.
    This ensures that the Redis client is available in your path operations.
    """
    if redis_client is None:
        raise RuntimeError("Redis client is not initialized.")
    return redis_client


async def connect_to_redis():
    """
    Initializes the Redis connection pool.
    This is called once on application startup.
    """
    global redis_client
    logger.info("Connecting to Redis...")
    redis_client = aioredis.from_url(
        f"redis://{app_settings.REDIS_HOST}:{app_settings.REDIS_PORT}",
        decode_responses=True,
    )
    try:
        await redis_client.ping()
        logger.info("Successfully connected to Redis.")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise


async def close_redis_connection():
    """
    Closes the Redis connection pool.
    This is called once on application shutdown.
    """
    global redis_client
    if redis_client:
        logger.info("Closing Redis connection...")
        await redis_client.close()
        logger.info("Redis connection closed.")
