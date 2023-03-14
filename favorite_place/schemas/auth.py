import pydantic


class Token(pydantic.BaseModel):
    access_token: str = pydantic.Field(...)
    token_type: str = pydantic.Field(...)


class TokenData(pydantic.BaseModel):
    username: str | None
    scopes: list[str] = pydantic.Field(default_factory=list)
