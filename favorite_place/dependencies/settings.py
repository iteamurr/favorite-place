import functools

from favorite_place.config import settings


@functools.lru_cache()
def get_api_settings() -> settings.APISettings:
    return settings.APISettings()


@functools.lru_cache()
def get_mongo_settings() -> settings.MongoSettings:
    return settings.MongoSettings()


@functools.lru_cache()
def get_redis_settings() -> settings.RedisSettings:
    return settings.RedisSettings()


@functools.lru_cache()
def get_oauth2_settings() -> settings.OAuth2Settings:
    return settings.OAuth2Settings()
