import pydantic


class PingResponse(pydantic.BaseModel):
    message: str = pydantic.Field(default="Pong!")
