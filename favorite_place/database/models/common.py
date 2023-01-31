import pydantic

from favorite_place.database import utils


class UpdateModel(pydantic.BaseModel):
    def dict(self, update_query: bool = False, *args, **kwargs) -> dict:
        res = super().dict(*args, **kwargs)
        if update_query:
            return utils.update_query(res)
        return res


class Coordinates(pydantic.BaseModel):
    longitude: float = pydantic.Field(default=0.0, alias="lon")
    latitude: float = pydantic.Field(default=0.0, alias="lat")
