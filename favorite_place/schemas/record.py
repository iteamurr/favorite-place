import datetime
import uuid

import pydantic

from favorite_place.database.models import record as record_models


class RecordAddRequest(pydantic.BaseModel):
    user_id: uuid.UUID = pydantic.Field(...)
    rating: int | None = pydantic.Field(ge=1, le=10)
    status: record_models.RecordStatus | None
    feedback: str | None
    note: str | None
    visit_date: datetime.date | None

    # pylint: disable=E0213
    @pydantic.validator("visit_date")
    def visit_date_to_datetime(cls, value):
        return datetime.datetime.combine(value, datetime.datetime.min.time())

    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "user_id": "980cf906-b892-4afb-8b01-cd9427a4cd2b",
                "rating": 7,
                "status": "favorite",
                "feedback": "My favorite place!",
                "note": "My favorite place.",
                "visit_date": "2023-01-22",
            }
        }


class RecordPlaceInfoResponse(pydantic.BaseModel):
    record_id: uuid.UUID = pydantic.Field(...)
    user_id: uuid.UUID = pydantic.Field(...)
    rating: int = pydantic.Field(..., ge=1, le=10)
    creation_date: datetime.datetime = pydantic.Field(...)
    feedback: str | None = pydantic.Field(example="My favorite place!")


class RecordUserInfoResponse(pydantic.BaseModel):
    record_id: uuid.UUID = pydantic.Field(...)
    place_id: uuid.UUID = pydantic.Field(...)
    place_name: str = pydantic.Field(..., example="Riverview Park")
    rating: int = pydantic.Field(..., ge=1, le=10)
    status: record_models.RecordStatus = pydantic.Field(...)
    creation_date: datetime.datetime = pydantic.Field(...)
    visit_date: datetime.date | None
    feedback: str | None = pydantic.Field(example="My favorite place!")


class RecordAddResponse(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(...)
