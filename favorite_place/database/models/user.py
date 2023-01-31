import uuid

import pydantic

from favorite_place.database.models import common


class UserName(pydantic.BaseModel):
    first: str = pydantic.Field(..., min_length=1, example="Tom")
    last: str = pydantic.Field(..., min_length=1, example="Sawyer")


class UserLocation(pydantic.BaseModel):
    city: str | None = pydantic.Field(min_length=1)
    state: str | None = pydantic.Field(min_length=1)
    country: str | None = pydantic.Field(min_length=1)
    coordinates: list[float, float] | None

    class Config:
        schema_extra = {
            "example": {
                "city": "Hannibal",
                "state": "Missouri",
                "country": "United States",
                "coordinates": [-91.357611, 39.711861],
            }
        }


class User(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4, alias="_id")
    name: UserName = pydantic.Field(...)
    location: UserLocation | None

    class Config:
        allow_population_by_field_name = True


class UserUpdate(common.UpdateModel):
    name: UserName | None
    location: UserLocation | None
