import fastapi
import uvicorn

from favorite_place import config
from favorite_place.utils import setups


def get_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    api_settings = config.get_api_settings()

    setups.setup_logger(api_settings)
    setups.setup_routes(app)

    return app


application = get_application()
settings = config.get_api_settings()
mongo_settings = config.get_mongo_settings()
mongo_client = config.get_mongo_client()


@application.on_event("startup")
async def startup_event():
    await mongo_client.on_startup(mongo_settings)


@application.on_event("shutdown")
async def shutdown_event():
    await mongo_client.on_shutdown()


if __name__ == "__main__":
    uvicorn.run(
        application,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
    )
