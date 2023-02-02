import uuid

import pydantic

from favorite_place.database.models import user as user_models


class UserAddRequest(pydantic.BaseModel):
    name: user_models.UserName = pydantic.Field(...)
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


class UserAddResponse(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(...)
