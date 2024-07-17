from os import getenv, environ
from typing import Any, Awaitable, Callable, Sequence
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pydantic import BaseModel
from redis.asyncio.client import Redis
import json

REDIS_HOST = getenv("REDIS_HOST", "localhost")
REDIS_PORT = getenv("REDIS_PORT", "6379")
REDIS_USERNAME = getenv("REDIS_USERNAME", "default")
REDIS_PASSWORD = getenv("REDIS_PASSWORD", "")

def init_cache():
    global redis
    redis = Redis(host=REDIS_HOST, port=int(REDIS_PORT), ssl=True, password=REDIS_PASSWORD, username=REDIS_USERNAME)

class CacheManager:
    def __init__(self, topic: str, namespace: str = "zomauto"):
        self.prefix = f"{namespace}:{topic}"

    async def cached(self, key: str, func: Callable[[], Awaitable[BaseModel | Sequence[BaseModel]]], expire: int = 604800) -> BaseModel | Sequence[BaseModel]:
        if (dump := await redis.get(f"{self.prefix}:{key}")) is not None:
            data = json.loads(dump)
        else:
            data = await func()
            if isinstance(data, list) or isinstance(data, Sequence):
                dump = json.dumps([e.model_dump() for e in data], default=lambda e: e.dict())
            else:
                dump = json.dumps(data.model_dump(), default=lambda e: e.dict())
            await redis.set(f"{self.prefix}:{key}", dump, ex=expire)

        return data
    