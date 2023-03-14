import fastapi
from fastapi import security, status
from motor import motor_asyncio as async_mongo

from favorite_place.dependencies import database as db_depends
from favorite_place.schemas import auth as auth_schemas
from favorite_place.schemas import errors
from favorite_place.services import auth as auth_services
from favorite_place.utils import responses


router = fastapi.APIRouter()


@router.post(
    "/login",
    response_model=auth_schemas.Token,
    status_code=status.HTTP_200_OK,
    responses=responses.get_responses(errors.Unauthorized),
    tags=["Auth"],
)
async def login(
    form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(),
    db: async_mongo.AsyncIOMotorDatabase = fastapi.Depends(db_depends.get_mongodb),
) -> auth_schemas.Token:
    db_user = await auth_services.authenticate_user(
        db, form_data.username, form_data.password
    )
    if db_user is None:
        raise errors.Unauthorized
    access_token = auth_services.create_access_token(
        {"sub": db_user.username, "scopes": db_user.scopes}
    )
    return auth_schemas.Token(access_token=access_token, token_type="bearer")
