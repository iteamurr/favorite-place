import functools

from motor import motor_asyncio as async_mongo

from favorite_place.database import clients


@functools.lru_cache()
def get_mongo_client() -> clients.MongoClient:
    return clients.MongoClient()


async def get_mongodb() -> async_mongo.AsyncIOMotorDatabase:
    return get_mongo_client().get_db()
