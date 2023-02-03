import uuid

import fastapi
from fastapi import status
from loguru import logger
from motor import motor_asyncio as async_mongo
from pymongo import errors as mongo_errors

from favorite_place import config
from favorite_place.database.crud import place as place_crud
from favorite_place.database.crud import record as record_crud
from favorite_place.schemas import errors
from favorite_place.schemas import place as place_schemas
from favorite_place.utils import responses


router = fastapi.APIRouter()


@router.post(
    "/place",
    response_model=place_schemas.PlaceAddResponse,
    status_code=status.HTTP_201_CREATED,
    responses=responses.get_responses(errors.Conflict, errors.ServiceUnavailable),
    tags=["Place"],
)
async def add_place(
    place: place_schemas.PlaceAddRequest = fastapi.Body(...),
    db: async_mongo.AsyncIOMotorDatabase = fastapi.Depends(config.get_mongodb),
) -> place_schemas.PlaceAddResponse:
    try:
        place_id = await place_crud.create_place(db, place.dict(exclude_none=True))
    except mongo_errors.DuplicateKeyError:
        raise errors.Conflict(
            "The request could not be completed due to a conflict. "
            "Unique data is repeated with an existing place."
        ) from None
    except Exception:
        logger.error("Unable to create a place.")
        raise errors.ServiceUnavailable from None
    else:
        return place_schemas.PlaceAddResponse(id=place_id)


@router.get(
    "/place/{place_id}",
    response_model=place_schemas.PlaceInfoResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses=responses.get_responses(errors.NotFound),
    tags=["Place"],
)
async def get_place(
    place_id: uuid.UUID,
    db: async_mongo.AsyncIOMotorDatabase = fastapi.Depends(config.get_mongodb),
) -> place_schemas.PlaceInfoResponse:
    if (db_place := await place_crud.get_place_by_id(db, place_id)) is None:
        raise errors.NotFound("Couldn't find a place with the specified id.")

    place_info = db_place.dict(exclude={"rating"})
    if (db_place.rating is not None) and (db_place.rating.number > 0):
        place_info["rating"] = round(db_place.rating.sum / db_place.rating.number, 1)
    if len(db_records := await record_crud.get_last_records(db, place_id)) > 0:
        place_info["last_records"] = db_records

    return place_schemas.PlaceInfoResponse(**place_info)


@router.put(
    "/place/{place_id}",
    response_model=place_schemas.PlaceUpdateResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses=responses.get_responses(errors.NotFound),
    tags=["Place"],
)
async def update_place(
    place_id: uuid.UUID,
    place: place_schemas.PlaceUpdateRequest = fastapi.Body(...),
    db: async_mongo.AsyncIOMotorDatabase = fastapi.Depends(config.get_mongodb),
) -> place_schemas.PlaceUpdateResponse:
    if (await place_crud.get_place_by_id(db, place_id)) is None:
        raise errors.NotFound("Couldn't find a place with the specified id.")
    await place_crud.update_place(db, place_id, place.dict(exclude_none=True))
    db_place = await place_crud.get_place_by_id(db, place_id)
    return place_schemas.PlaceUpdateResponse(**db_place.dict())


@router.delete(
    "/place/{place_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=responses.get_responses(errors.NotFound),
    tags=["Place"],
)
async def delete_place(
    place_id: uuid.UUID,
    db: async_mongo.AsyncIOMotorDatabase = fastapi.Depends(config.get_mongodb),
) -> fastapi.Response:
    if await place_crud.delete_place(db, place_id):
        return fastapi.Response(status_code=status.HTTP_204_NO_CONTENT)
    raise errors.NotFound("Couldn't find a place with the specified id.")
