import uuid

import pydantic

from favorite_place.database.models import place as place_models


class PlaceAddRequest(pydantic.BaseModel):
    name: str = pydantic.Field(..., min_length=1, example="Riverview Park")
    location: place_models.PlaceLocation = pydantic.Field(...)


class PlaceUpdateRequest(pydantic.BaseModel):
    name: str | None = pydantic.Field(min_length=1)
    location: place_models.PlaceLocationUpdate | None

    class Config:
        schema_extra = {
            "example": {
                "name": "Susquehannock State Forest",
                "location": {"state": "Pennsylvania", "country": "United States"},
            }
        }


class PlaceInfoResponse(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(..., example="f2828ba8-d02f-447e-9661-188d0bde3770")
    name: str = pydantic.Field(..., example="Riverview Park")
    location: place_models.PlaceLocation = pydantic.Field(...)


class PlaceAddResponse(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(..., example="f2828ba8-d02f-447e-9661-188d0bde3770")
