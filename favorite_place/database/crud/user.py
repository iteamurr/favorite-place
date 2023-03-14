import uuid

from motor import motor_asyncio as async_mongo

from favorite_place.database.models import user as user_models


async def create_user(
    db: async_mongo.AsyncIOMotorDatabase,
    user_info: dict,
) -> uuid.UUID:
    db_user = user_models.User(**user_info).dict(exclude_none=True, by_alias=True)
    new_user = await db.users.insert_one(db_user)
    return new_user.inserted_id


async def get_user_by_id(
    db: async_mongo.AsyncIOMotorDatabase,
    user_id: uuid.UUID,
) -> user_models.User | None:
    if (db_user := await db.users.find_one({"_id": user_id})) is not None:
        return user_models.User(**db_user)
    return None


async def get_user_by_username(
    db: async_mongo.AsyncIOMotorDatabase,
    username: str,
) -> user_models.User | None:
    if (db_user := await db.users.find_one({"username": username})) is not None:
        return user_models.User(**db_user)
    return None


async def update_user(
    db: async_mongo.AsyncIOMotorDatabase,
    user_id: uuid.UUID,
    user_info: dict,
) -> bool:
    db_user = user_models.UserUpdate(**user_info).dict(
        exclude_none=True, update_query=True
    )
    update_res = await db.users.update_one({"_id": user_id}, {"$set": db_user})
    return update_res.modified_count == 1


async def delete_user(
    db: async_mongo.AsyncIOMotorDatabase,
    user_id: uuid.UUID,
) -> bool:
    delete_res = await db.users.delete_one({"_id": user_id})
    return delete_res.deleted_count == 1
