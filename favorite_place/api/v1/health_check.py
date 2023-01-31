import fastapi
from fastapi import status
from loguru import logger
from motor import motor_asyncio as async_mongo

from favorite_place import config
from favorite_place.schemas import errors, health_check
from favorite_place.utils import responses


router = fastapi.APIRouter()


@router.get(
    "/ping",
    response_model=health_check.PingResponse,
    status_code=status.HTTP_200_OK,
    tags=["Health"],
)
async def ping() -> health_check.PingResponse:
    return health_check.PingResponse()


@router.get(
    "/ping_db",
    response_model=health_check.PingResponse,
    status_code=status.HTTP_200_OK,
    responses=responses.get_responses(errors.ServiceUnavailable),
    tags=["Health"],
)
async def ping_db(
    db: async_mongo.AsyncIOMotorDatabase = fastapi.Depends(config.get_mongodb),
) -> health_check.PingResponse:
    try:
        await db.command("ping")
    except Exception:
        logger.error("Unable to access the database.")
        raise errors.ServiceUnavailable("Unable to access the database.") from None
    else:
        return health_check.PingResponse()
