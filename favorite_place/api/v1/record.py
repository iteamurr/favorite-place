import uuid

import fastapi
from motor import motor_asyncio as async_mongo
from pymongo import errors as mongo_errors
from starlette import status

from favorite_place.database.crud import place as place_crud
from favorite_place.database.crud import record as record_crud
from favorite_place.dependencies import database as db_depends
from favorite_place.schemas import errors
from favorite_place.schemas import record as record_schemas
from favorite_place.utils import responses


router = fastapi.APIRouter()


@router.post(
    "/place/{place_id}/record",
    response_model=record_schemas.RecordAddResponse,
    status_code=status.HTTP_201_CREATED,
    responses=responses.get_responses(errors.NotFound, errors.Conflict),
    tags=["Record"],
)
async def add_record(
    place_id: uuid.UUID,
    record: record_schemas.RecordAddRequest = fastapi.Body(...),
    db: async_mongo.AsyncIOMotorDatabase = fastapi.Depends(db_depends.get_mongodb),
) -> record_schemas.RecordAddResponse:
    if (await place_crud.get_place_by_id(db, place_id)) is None:
        raise errors.NotFound("Couldn't find a place with the specified id.")
    try:
        record_id = await record_crud.create_record(
            db=db,
            place_id=place_id,
            user_id=record.user_id,
            record_info=record.dict(exclude={"user_id"}, exclude_none=True),
        )
    except mongo_errors.DuplicateKeyError:
        raise errors.Conflict(
            "The request could not be completed due to a conflict. "
            "Unique data is repeated with an existing record."
        ) from None
    await place_crud.update_place_rating(db, place_id, record.rating)
    return record_schemas.RecordAddResponse(id=record_id)
