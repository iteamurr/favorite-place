import uuid

from motor import motor_asyncio as async_mongo

from favorite_place.database.models import place as place_models


async def create_place(
    db: async_mongo.AsyncIOMotorDatabase,
    place_info: dict,
) -> uuid.UUID:
    db_place = place_models.Place(**place_info).dict(exclude_none=True, by_alias=True)
    new_place = await db.places.insert_one(db_place)
    return new_place.inserted_id


async def get_place_by_id(
    db: async_mongo.AsyncIOMotorDatabase,
    place_id: uuid.UUID,
) -> place_models.Place | None:
    if (db_place := await db.places.find_one({"_id": place_id})) is not None:
        return place_models.Place(**db_place)
    return None


async def update_place(
    db: async_mongo.AsyncIOMotorDatabase,
    place_id: uuid.UUID,
    place_info: dict,
) -> bool:
    db_place = place_models.PlaceUpdate(**place_info).dict(
        exclude_none=True, update_query=True
    )
    update_res = await db.places.update_one({"_id": place_id}, {"$set": db_place})
    return update_res.modified_count == 1


async def delete_place(
    db: async_mongo.AsyncIOMotorDatabase,
    place_id: uuid.UUID,
) -> bool:
    delete_res = await db.places.delete_one({"_id": place_id})
    return delete_res.deleted_count == 1
