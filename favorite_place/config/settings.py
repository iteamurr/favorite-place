import pydantic


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class APISettings(BaseSettings):
    host: str
    port: int
    log_file: str
    log_level: str

    class Config(BaseSettings.Config):
        env_prefix = "API_"


class MongoSettings(BaseSettings):
    uri: str
    database: str

    class Config(BaseSettings.Config):
        env_prefix = "MONGO_"


class RedisSettings(BaseSettings):
    uri: str

    class Config(BaseSettings.Config):
        env_prefix = "REDIS_"


class OAuth2Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config(BaseSettings.Config):
        env_prefix = "OAUTH2_"
