import datetime

from jose import jwt
from motor import motor_asyncio as async_mongo

from favorite_place.database.crud import user as user_crud
from favorite_place.database.models import user as user_models
from favorite_place.dependencies import auth as auth_depends
from favorite_place.dependencies import settings as settings_depends


def get_password_hash(password: str) -> str:
    return auth_depends.get_passlib_context().hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return auth_depends.get_passlib_context().verify(plain_password, hashed_password)


async def authenticate_user(
    db: async_mongo.AsyncIOMotorDatabase,
    username: str,
    password: str,
) -> user_models.User | None:
    if (db_user := await user_crud.get_user_by_username(db, username)) is None:
        return None
    if not verify_password(password, db_user.hashed_password):
        raise None
    return db_user


def create_access_token(
    data: dict,
    expires_delta: datetime.timedelta | None = None,
) -> str:
    auth_settings = settings_depends.get_oauth2_settings()

    expire = datetime.datetime.utcnow()
    if expires_delta:
        expire += expires_delta
    elif auth_settings.access_token_expire_minutes:
        expire += datetime.timedelta(minutes=auth_settings.access_token_expire_minutes)
    else:
        expire += datetime.timedelta(minutes=15)

    to_encode = data.copy()
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=auth_settings.secret_key,
        algorithm=auth_settings.algorithm,
    )
    return encoded_jwt
