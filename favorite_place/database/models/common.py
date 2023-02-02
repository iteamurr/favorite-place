import enum

import pydantic
import pymongo

from favorite_place.database import utils


class MongoDirections(enum.Enum):
    ASCENDING = pymongo.ASCENDING
    DESCENDING = pymongo.DESCENDING
    GEO2D = pymongo.GEO2D
    GEOSPHERE = pymongo.GEOSPHERE
    HASHED = pymongo.HASHED
    TEXT = pymongo.TEXT


class UpdateModel(pydantic.BaseModel):
    def dict(self, *args, update_query: bool = False, **kwargs) -> dict:
        res = super().dict(*args, **kwargs)
        if update_query:
            return utils.update_query(res)
        return res


class Coordinates(pydantic.BaseModel):
    longitude: float = pydantic.Field(default=0.0, alias="lon")
    latitude: float = pydantic.Field(default=0.0, alias="lat")
