import functools

from motor import motor_asyncio as async_mongo

from favorite_place.config import settings
from favorite_place.database import clients


async def get_mongodb() -> async_mongo.AsyncIOMotorDatabase:
    return get_mongo_client().get_db()


@functools.lru_cache()
def get_mongo_client() -> clients.MongoClient:
    return clients.MongoClient()


@functools.lru_cache()
def get_api_settings() -> settings.APISettings:
    return settings.APISettings()


@functools.lru_cache()
def get_mongo_settings() -> settings.MongoSettings:
    return settings.MongoSettings()


@functools.lru_cache()
def get_redis_settings() -> settings.RedisSettings:
    return settings.RedisSettings()
