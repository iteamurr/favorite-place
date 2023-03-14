import functools

import fastapi
import jose
import pydantic
from fastapi import security
from jose import jwt
from motor import motor_asyncio as async_mongo
from passlib import context as passlib_context

from favorite_place.database.crud import user as user_crud
from favorite_place.database.models import user as user_models
from favorite_place.dependencies import database as db_depends
from favorite_place.dependencies import settings as settings_depends
from favorite_place.schemas import auth as auth_schemas
from favorite_place.schemas import errors


oauth2_scheme = security.OAuth2PasswordBearer(
    tokenUrl="api/v1/login",
    scopes=user_models.UserScopes.import_scopes(),
)


@functools.lru_cache()
def get_passlib_context():
    return passlib_context.CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(
    security_scopes: security.SecurityScopes,
    token: str = fastapi.Depends(oauth2_scheme),
    db: async_mongo.AsyncIOMotorDatabase = fastapi.Depends(db_depends.get_mongodb),
) -> user_models.User:
    headers = {"WWW-Authenticate": "Bearer"}
    if security_scopes.scopes:
        headers["WWW-Authenticate"] = f"Bearer scope='{security_scopes.scope_str}'"

    auth_settings = settings_depends.get_oauth2_settings()
    try:
        payload = jwt.decode(
            token=token,
            key=auth_settings.secret_key,
            algorithms=[auth_settings.algorithm],
        )
        if (username := payload.get("sub")) is None:
            raise errors.Unauthorized(
                detail="Could not validate credentials.", headers=headers
            )
        token_scopes = payload.get("scopes", [])
        token_data = auth_schemas.TokenData(username=username, scopes=token_scopes)
    except (jose.JWTError, pydantic.ValidationError):
        raise errors.Unauthorized(
            detail="Could not validate credentials.", headers=headers
        ) from None

    db_user = await user_crud.get_user_by_username(db, token_data.username)
    if db_user is None:
        raise errors.Unauthorized(
            detail="Could not validate credentials.", headers=headers
        )

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise errors.Unauthorized(detail="Not enough permissions.", headers=headers)

    return db_user


async def get_current_active_user(
    current_user: user_models.User = fastapi.Security(get_current_user, scopes=[])
) -> user_models.User:
    if current_user.disabled:
        raise errors.BadRequest
    return current_user
