import uuid

import pydantic

from favorite_place.database.models import common


class PlaceLocation(pydantic.BaseModel):
    street: str | None = pydantic.Field(min_length=1)
    city: str = pydantic.Field(..., min_length=1)
    state: str | None = pydantic.Field(min_length=1)
    country: str = pydantic.Field(..., min_length=1)
    coordinates: list[float, float] | None

    class Config:
        schema_extra = {
            "example": {
                "city": "London",
                "country": "United Kingdom",
                "coordinates": [-0.156667, 51.532222],
            }
        }


class PlaceRating(pydantic.BaseModel):
    sum: int = pydantic.Field(...)
    number: int = pydantic.Field(...)


class Place(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4, alias="_id")
    name: str = pydantic.Field(..., min_length=1, example="Regent's Park")
    rating: PlaceRating | None
    location: PlaceLocation = pydantic.Field(...)

    class Config:
        allow_population_by_field_name = True


class PlaceLocationUpdate(pydantic.BaseModel):
    street: str | None = pydantic.Field(min_length=1)
    city: str | None = pydantic.Field(min_length=1)
    state: str | None = pydantic.Field(min_length=1)
    country: str | None = pydantic.Field(min_length=1)
    coordinates: list[float, float] | None


class PlaceUpdate(common.UpdateModel):
    name: str | None = pydantic.Field(min_length=1)
    location: PlaceLocationUpdate | None
