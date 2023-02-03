import uuid

from motor import motor_asyncio as async_mongo

from favorite_place.database.models import common as common_models
from favorite_place.database.models import record as record_models
from favorite_place.schemas import record as record_schemas


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
    db: async_mongo.AsyncIOMotorDatabase,
    place_id: uuid.UUID,
    limit: int = 5,
) -> list[record_schemas.RecordPlaceInfoResponse]:
    cursor = db.records.aggregate(
        [
            {"$match": {"place_id": place_id, "rating": {"$exists": True}}},
            {
                "$project": {
                    "record_id": "$_id",
                    "user_id": 1,
                    "rating": 1,
                    "creation_date": 1,
                    "feedback": 1,
                }
            },
            {
                "$sort": {
                    "creation_date": common_models.MongoDirections.DESCENDING.value
                }
            },
            {"$limit": min(max(limit, 1), 10)},
        ]
    )
    return [record_schemas.RecordPlaceInfoResponse(**record) async for record in cursor]


async def get_top_rated_records_by_user(
    db: async_mongo.AsyncIOMotorDatabase,
    user_id: uuid.UUID,
    limit: int = 5,
) -> list[record_schemas.RecordUserInfoResponse]:
    cursor = db.records.aggregate(
        [
            {"$match": {"user_id": user_id, "rating": {"$exists": True}}},
            {
                "$lookup": {
                    "from": "places",
                    "localField": "place_id",
                    "foreignField": "_id",
                    "as": "place_info",
                }
            },
            {
                "$project": {
                    "record_id": "$_id",
                    "place_id": 1,
                    "place_name": {"$first": "$place_info.name"},
                    "rating": 1,
                    "status": 1,
                    "creation_date": 1,
                    "feedback": 1,
                    "visit_date": 1,
                }
            },
            {
                "$sort": {
                    "rating": common_models.MongoDirections.DESCENDING.value,
                    "creation_date": common_models.MongoDirections.DESCENDING.value,
                }
            },
            {"$limit": min(max(limit, 1), 10)},
        ]
    )
    return [record_schemas.RecordUserInfoResponse(**record) async for record in cursor]
