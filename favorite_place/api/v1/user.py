import uuid

import fastapi
from fastapi import status
from loguru import logger
from motor import motor_asyncio as async_mongo
from pymongo import errors as mongo_errors

from favorite_place import config
from favorite_place.database.crud import user as user_crud
from favorite_place.schemas import errors
from favorite_place.schemas import user as user_schemas
from favorite_place.utils import responses


router = fastapi.APIRouter()


@router.post(
    "/user",
    response_model=user_schemas.UserAddResponse,
    status_code=status.HTTP_201_CREATED,
    responses=responses.get_responses(errors.Conflict, errors.ServiceUnavailable),
    tags=["User"],
)
async def add_user(
    user: user_schemas.UserAddRequest = fastapi.Body(...),
    db: async_mongo.AsyncIOMotorDatabase = fastapi.Depends(config.get_mongodb),
) -> user_schemas.UserAddResponse:
    try:
        user_id = await user_crud.create_user(db, user.dict(exclude_none=True))
    except mongo_errors.DuplicateKeyError:
        raise errors.Conflict(
            "The request could not be completed due to a conflict. "
            "Unique data is repeated with an existing user."
        ) from None
    except Exception:
        logger.error("Unable to create a user.")
        raise errors.ServiceUnavailable from None
    else:
        return user_schemas.UserAddResponse(id=user_id)


@router.get(
    "/user/{user_id}",
    response_model=user_schemas.UserInfoResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses=responses.get_responses(errors.NotFound),
    tags=["User"],
)
async def get_user(
    user_id: uuid.UUID,
    db: async_mongo.AsyncIOMotorDatabase = fastapi.Depends(config.get_mongodb),
) -> user_schemas.UserInfoResponse:
    if (db_user := await user_crud.get_user_by_id(db, user_id)) is not None:
        return user_schemas.UserInfoResponse(**db_user.dict())
    raise errors.NotFound("Couldn't find a user with the specified id.")


@router.put(
    "/user/{user_id}",
    response_model=user_schemas.UserInfoResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses=responses.get_responses(errors.NotFound),
    tags=["User"],
)
async def update_user(
    user_id: uuid.UUID,
    user: user_schemas.UserUpdateRequest = fastapi.Body(...),
    db: async_mongo.AsyncIOMotorDatabase = fastapi.Depends(config.get_mongodb),
) -> user_schemas.UserInfoResponse:
    if (await user_crud.get_user_by_id(db, user_id)) is None:
        raise errors.NotFound("Couldn't find a user with the specified id.")
    await user_crud.update_user(db, user_id, user.dict(exclude_none=True))
    db_user = await user_crud.get_user_by_id(db, user_id)
    return user_schemas.UserInfoResponse(**db_user.dict())


@router.delete(
    "/user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=responses.get_responses(errors.NotFound),
    tags=["User"],
)
async def delete_user(
    user_id: uuid.UUID,
    db: async_mongo.AsyncIOMotorDatabase = fastapi.Depends(config.get_mongodb),
) -> fastapi.Response:
    if await user_crud.delete_user(db, user_id):
        return fastapi.Response(status_code=status.HTTP_204_NO_CONTENT)
    raise errors.NotFound("Couldn't find a user with the specified id.")
