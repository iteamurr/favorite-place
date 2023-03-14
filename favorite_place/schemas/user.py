import uuid

import pydantic

from favorite_place.database.models import user as user_models
from favorite_place.schemas import record as record_schemas


class UserAddRequest(pydantic.BaseModel):
    name: user_models.UserName = pydantic.Field(...)
    username: str = pydantic.Field(...)
    password: str = pydantic.Field(...)
    scopes: list[user_models.UserScopes] | None
    location: user_models.UserLocation | None


class UserUpdateRequest(pydantic.BaseModel):
    name: user_models.UserName | None
    location: user_models.UserLocation | None

    class Config:
        schema_extra = {
            "example": {"location": {"city": "Auckland", "country": "New Zealand"}}
        }


class UserInfoResponse(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(...)
    name: user_models.UserName = pydantic.Field(...)
    location: user_models.UserLocation | None
    top_places: list[record_schemas.RecordUserInfoResponse] | None


class UserAddResponse(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(...)


class UserUpdateResponse(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(...)
    name: user_models.UserName = pydantic.Field(...)
    location: user_models.UserLocation | None
