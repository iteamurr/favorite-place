from fastapi import exceptions, status


class BaseError(exceptions.HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    description: str = "Error message!"

    def __init__(self, detail: str | None = None) -> None:
        description = detail if detail else self.description
        super().__init__(status_code=self.status_code, detail=description)

    @classmethod
    def to_responses(cls) -> dict:
        return {cls.status_code: {"description": cls.description}}


class NotFound(BaseError):
    status_code: int = status.HTTP_404_NOT_FOUND
    description: str = "The service could not find information on the request."


class Conflict(BaseError):
    status_code: int = status.HTTP_409_CONFLICT
    description: str = (
        "The request could not be completed due to a conflict "
        "with the current state of the resource."
    )


class ServiceUnavailable(BaseError):
    status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE
    description: str = "The service is currently unavailable."
