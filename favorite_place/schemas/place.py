import uuid

import pydantic

from favorite_place.database.models import place as place_models
from favorite_place.schemas import record as record_schemas


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
    id: uuid.UUID = pydantic.Field(...)
    name: str = pydantic.Field(..., example="Riverview Park")
    location: place_models.PlaceLocation = pydantic.Field(...)
    rating: float | None = pydantic.Field(ge=1, le=10)
    last_records: list[record_schemas.RecordPlaceInfoResponse] | None


class PlaceAddResponse(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(...)


class PlaceUpdateResponse(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(...)
    name: str = pydantic.Field(..., example="Susquehannock State Forest")
    location: place_models.PlaceLocation = pydantic.Field(...)
