from redis.asyncio import from_url, Redis
import json

from loguru import logger

from infra import config


class RedisService:
    def __init__(self):
        self._redis_url = config.REDIS_HOST
        self._redis_client = None

    async def connect(self):
        logger.debug("Connecting to Redis: {}".format(self._redis_url))
        self._redis_client = await from_url(self._redis_url, decode_responses=True)


    async def close(self):
        if self._redis_client:
            await self._redis_client.close()


    async def get_data(self, key: str):
        if not self._redis_client:
            await self.connect()

        data = await self._redis_client.get(key)
        return json.loads(data) if data else None

    async def set_data_with_ttl(self, key: str, value: dict | list[dict], expire: int = 300):
        if not self._redis_client:
            await self.connect()

        await self._redis_client.set(key, json.dumps(value), ex=expire)


redis_service: RedisService = RedisService()