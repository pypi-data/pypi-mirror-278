import os

from loguru import logger
from tortoise import Tortoise


class Database:

    def __init__(self):
        self.db_path = "sqlite://settings/database/bot.db"
        self.db_models = {"models": [os.path.join("src.utils")]}

    async def database_connect(self):
        try:
            logger.info("Database connected")
            await Tortoise.init(db_url=self.db_path, modules=self.db_models)
            await Tortoise.generate_schemas()
        except Exception as e:
            logger.error(f"Ошибка подключение к базе данных\n╰─> Ошибка: {e}")

    async def database_close(self):
        logger.error("Database disconnected")
        await Tortoise.close_connections()
