import datetime
import enum
import uuid

import pydantic


class RecordStatus(str, enum.Enum):
    WISH = "wish"
    PLANNED = "planned"
    VISITED = "visited"
    FAVORITE = "favorite"


class Record(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4, alias="_id")
    place_id: uuid.UUID = pydantic.Field(...)
    user_id: uuid.UUID = pydantic.Field(...)
    rating: int | None = pydantic.Field()
    status: RecordStatus = pydantic.Field(default=RecordStatus.VISITED)
    feedback: str | None = pydantic.Field()
    note: str | None = pydantic.Field()
    creation_date: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.now
    )
    visit_date: datetime.datetime | None = pydantic.Field()

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
