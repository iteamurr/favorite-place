from fastapi import exceptions, status


class BaseError(exceptions.HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    description: str = "Error message!"
    headers: dict | None = None

    def __init__(self, detail: str | None = None, headers: dict | None = None) -> None:
        description = detail if detail else self.description
        super_headers = headers if headers else self.headers
        super().__init__(
            status_code=self.status_code, detail=description, headers=super_headers
        )

    @classmethod
    def to_responses(cls) -> dict:
        return {cls.status_code: {"description": cls.description}}


class BadRequest(BaseError):
    status_code: int = status.HTTP_400_BAD_REQUEST
    description: str = (
        "The service cannot or will not process the request due "
        "to something that is perceived to be a client error."
    )


class Unauthorized(BaseError):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    description: str = "Incorrect username or password."
    headers: dict = {"WWW-Authenticate": "Bearer"}


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
