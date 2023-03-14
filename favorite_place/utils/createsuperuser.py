import asyncio
from getpass import getpass

from motor import motor_asyncio as async_mongo

from favorite_place.database.crud import user as user_crud
from favorite_place.database.models import user as user_models
from favorite_place.dependencies import database as db_depends
from favorite_place.dependencies import settings as settings_depends
from favorite_place.services import auth as auth_services
from favorite_place.utils import setups


async def create_superuser(db: async_mongo.AsyncIOMotorDatabase) -> None:
    first_name = input("First name: ")
    last_name = input("Last name: ")
    username = input("Username: ")

    while True:
        if (password := getpass()) != getpass("Confirm password: "):
            print("Passwords do not match. Try again.")
        else:
            break

    superuser_info = {
        "name": {"first": first_name, "last": last_name},
        "username": username,
        "hashed_password": auth_services.get_password_hash(password),
        "scopes": [user_models.UserScopes.ADMIN],
    }
    await user_crud.create_user(db, superuser_info)


async def main() -> None:
    app_settings = settings_depends.get_api_settings()
    app_settings.log_level = "critical"
    setups.setup_logger(app_settings)

    mongo_settings = settings_depends.get_mongo_settings()
    mongo_client = db_depends.get_mongo_client()
    await mongo_client.on_startup(mongo_settings)
    await mongo_client.create_indexes()
    db = await db_depends.get_mongodb()

    await create_superuser(db)

    await mongo_client.on_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
