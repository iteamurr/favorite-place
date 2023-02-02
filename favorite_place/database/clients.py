from __future__ import annotations

from loguru import logger
from motor import motor_asyncio as async_mongo
from pymongo import errors

from favorite_place.config import settings
from favorite_place.database import indexes


class MongoClient:
    _db: str
    _client: async_mongo.AsyncIOMotorClient
    indexes: list[indexes.BaseIndex] = [indexes.RecordUserIDPlaceIDUniqueIndex]

    def __new__(cls: MongoClient) -> MongoClient:
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    async def on_startup(self, mongo_settings: settings.MongoSettings = None) -> None:
        self._db = mongo_settings.database
        try:
            self._client = async_mongo.AsyncIOMotorClient(
                mongo_settings.uri,
                serverSelectionTimeoutMS=10000,
                uuidRepresentation="pythonLegacy",
            )
            await self._client.server_info()
        except errors.ServerSelectionTimeoutError as err:
            logger.critical(
                f"Failed to establish a connection to the '{self._db}' database."
            )
            raise errors.ServerSelectionTimeoutError(
                "Failed to establish a connection to the database."
            ) from err
        else:
            logger.info(
                f"Connection to the '{self._db}' database has been established."
            )

    async def on_shutdown(self) -> None:
        if self._client:
            self._client.close()
        logger.info(f"Connection to the '{self._db}' database has been closed.")

    async def create_indexes(self) -> None:
        for index in self.indexes:
            await self._client[self._db][index.collection].create_indexes(
                [index.to_index_model()]
            )
        if len(self.indexes) > 0:
            logger.info(f"Indexes for the database '{self._db}' have been created.")

    def get_client(self) -> async_mongo.AsyncIOMotorClient:
        return self._client

    def get_db(self) -> async_mongo.AsyncIOMotorDatabase:
        return self._client[self._db]
