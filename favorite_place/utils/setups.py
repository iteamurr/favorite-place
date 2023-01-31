import sys

import fastapi
from loguru import logger

from favorite_place import api
from favorite_place.config import settings


def setup_logger(api_settings: settings.APISettings) -> None:
    logger.remove()
    logger.add(
        sys.stderr,
        level=api_settings.log_level.upper(),
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<level>{message}</level>"
        ),
    )
    logger.add(api_settings.log_file, level=api_settings.log_level.upper())


def setup_routes(app: fastapi.FastAPI) -> None:
    for route in api.v1_routes:
        app.include_router(route, prefix="/api/v1")

    for route in api.v2_routes:
        app.include_router(route, prefix="/api/v2")
