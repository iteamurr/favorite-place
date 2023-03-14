import fastapi
import uvicorn

from favorite_place.dependencies import database, settings
from favorite_place.utils import setups


def get_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    app_settings = settings.get_api_settings()

    setups.setup_logger(app_settings)
    setups.setup_routes(app)

    return app


application = get_application()
api_settings = settings.get_api_settings()
mongo_settings = settings.get_mongo_settings()
mongo_client = database.get_mongo_client()


@application.on_event("startup")
async def startup_event():
    await mongo_client.on_startup(mongo_settings)
    await mongo_client.create_indexes()


@application.on_event("shutdown")
async def shutdown_event():
    await mongo_client.on_shutdown()


if __name__ == "__main__":
    uvicorn.run(
        application,
        host=api_settings.host,
        port=api_settings.port,
        log_level=api_settings.log_level,
    )
