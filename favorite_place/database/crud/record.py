import uuid

from motor import motor_asyncio as async_mongo

from favorite_place.database.models import common as common_models
from favorite_place.database.models import record as record_models


async def create_record(
    db: async_mongo.AsyncIOMotorDatabase,
    place_id: uuid.UUID,
    user_id: uuid.UUID,
    record_info: dict,
) -> uuid.UUID:
    db_record = record_models.Record(
        place_id=place_id, user_id=user_id, **record_info
    ).dict(exclude_none=True, by_alias=True)
    new_record = await db.records.insert_one(db_record)
    return new_record.inserted_id


async def get_last_records(
    db: async_mongo.AsyncIOMotorDatabase, place_id: uuid.UUID, limit: int = 5
) -> list[record_models.Record]:
    cursor = (
        db.records.find({"place_id": place_id, "rating": {"$exists": True}})
        .sort("creation_date", common_models.MongoDirections.DESCENDING.value)
        .limit(min(max(limit, 1), 10))
    )
    return [record_models.Record(**record) async for record in cursor]
