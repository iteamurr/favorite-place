from __future__ import annotations

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


class ScopesModel(str, enum.Enum):
    def __new__(cls, value: str, *args, **kwargs) -> ScopesModel:
        obj = str.__new__(cls, value)
        obj._value_ = value
        return obj

    def __init__(self, _: str, description: str = None) -> None:
        self._description_ = description

    def __str__(self) -> str:
        return self.value

    @property
    def description(self) -> str:
        return self._description_

    @classmethod
    def import_scopes(cls) -> dict:
        return {scope.value: scope.description for scope in cls}


class Coordinates(pydantic.BaseModel):
    longitude: float = pydantic.Field(default=0.0, alias="lon")
    latitude: float = pydantic.Field(default=0.0, alias="lat")
