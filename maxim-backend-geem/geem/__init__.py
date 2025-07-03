from tortoise import Tortoise

from .api import app  # noqa: F401
from .settings.main import DB_NAME, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER


async def run(generate_schemas=False):
    await Tortoise.init(
        config={
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "database": DB_NAME,
                        "host": DB_HOST,
                        "password": DB_PASSWORD,
                        "port": DB_PORT,
                        "user": DB_USER
                    }
                }
            },
            "apps": {
                "models": {
                    "models": ["geem.models"],
                    "default_connection": "default",
                }
            },
        }
    )
    if generate_schemas:
        await Tortoise.generate_schemas()
