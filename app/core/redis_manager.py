import redis.asyncio as aioredis
import asyncio
from app.core.config import app_settings


class RedisManager:
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(
        self, host=app_settings.REDIS_HOST, port=app_settings.REDIS_PORT, db=0
    ):
        if not hasattr(self, "_client"):
            self._client = aioredis.Redis(
                host=host, port=port, db=db, decode_responses=True
            )

    def get_client(self):
        return self._client

    async def set_value(self, key, value, ex=None):
        return await self._client.set(name=key, value=value, ex=ex)

    async def get_value(self, key):
        return await self._client.get(name=key)

    async def delete_key(self, key):
        return await self._client.delete(key)

    async def key_exists(self, key):
        return await self._client.exists(key) > 0
