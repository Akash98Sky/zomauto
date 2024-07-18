from os import getenv
import time
from typing import Awaitable, Callable, Sequence
from pydantic import BaseModel
from redis.asyncio.client import Redis
import json
from cacheout import Cache

REDIS_URL = getenv("REDIS_URL")

def init_cache():
    global redis
    global local_cache
    if REDIS_URL and REDIS_URL.strip() != "":
        redis = Redis.from_url(REDIS_URL)
        local_cache = None
    else:
        redis = None
        local_cache = Cache(ttl=604800, timer=time.time, default=None)

class CacheManager:
    def __init__(self, topic: str, namespace: str = "zomauto"):
        self.prefix = f"{namespace}:{topic}"

    async def __get__(self, key: str):
        if redis is not None:
            return await redis.get(f"{self.prefix}:{key.lower()}")
        elif local_cache is not None:
            return local_cache.get(f"{self.prefix}:{key.lower()}")
        else:
            return None
    
    async def __set__(self, key: str, value: str, ex: int = 604800):
        if redis is not None:
            await redis.set(f"{self.prefix}:{key.lower()}", value, ex=ex)
        elif local_cache is not None:
            local_cache.set(f"{self.prefix}:{key.lower()}", value, ttl=ex)

    async def cached(self, key: str, func: Callable[[], Awaitable[BaseModel | Sequence[BaseModel]]], expire: int = 604800) -> BaseModel | Sequence[BaseModel]:
        if (dump := await self.__get__(f"{self.prefix}:{key}")) is not None:
            data = json.loads(dump)
        else:
            data = await func()
            if isinstance(data, list) or isinstance(data, Sequence):
                dump = json.dumps([e.model_dump() for e in data], default=lambda e: e.dict())
            else:
                dump = json.dumps(data.model_dump(), default=lambda e: e.dict())
            await self.__set__(f"{self.prefix}:{key}", dump, ex=expire)

        return data
    