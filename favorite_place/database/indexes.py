import pydantic
import pymongo

from favorite_place.database.models import common as common_models
from favorite_place.database.models import record as record_models


IndexField = tuple[str, common_models.MongoDirections]


class BaseIndex:
    model: pydantic.BaseModel
    collection: str
    name: str
    fields: list[IndexField]
    unique: bool = False
    partial_filter_expression: dict | None = None

    def __repr__(self) -> str:
        return f"Index(name='{self.name}', collection='{self.collection}')"

    @classmethod
    def to_index_model(cls):
        if cls.partial_filter_expression:
            return pymongo.IndexModel(
                keys=cls.fields,
                name=cls.name,
                unique=cls.unique,
                partialFilterExpression=cls.partial_filter_expression,
            )
        return pymongo.IndexModel(keys=cls.fields, name=cls.name, unique=cls.unique)


class RecordUserIDPlaceIDUniqueIndex(BaseIndex):
    model: pydantic.BaseModel = record_models.Record
    collection: str = "records"
    name: str = "record_user_id_place_id_unique_index"
    fields: list[IndexField] = [
        ("place_id", common_models.MongoDirections.ASCENDING.value),
        ("user_id", common_models.MongoDirections.ASCENDING.value),
    ]
    unique: bool = True
