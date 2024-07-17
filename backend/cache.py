from os import getenv
from typing import Awaitable, Callable, Sequence
from pydantic import BaseModel
from redis.asyncio.client import Redis
import json

REDIS_URL = getenv("REDIS_URL", "redis://localhost:6379")

def init_cache():
    global redis
    redis = Redis.from_url(REDIS_URL)

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
    