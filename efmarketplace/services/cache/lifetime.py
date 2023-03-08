from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from efmarketplace.settings import settings


def init_cache(app: FastAPI) -> None:
    redis = aioredis.from_url(
        url=str(settings.redis_url), encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
