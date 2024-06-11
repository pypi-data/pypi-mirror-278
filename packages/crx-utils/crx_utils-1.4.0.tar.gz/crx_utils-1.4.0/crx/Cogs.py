import os
import sys

from loguru import logger

async def load_extensions(bot):
    try:
        logger.info("Load modules...")
        src_directory = os.path.join("src")
        sys.path.append(src_directory)

        for directory in os.listdir(src_directory):
            directory_path = os.path.join(src_directory, directory)

            if os.path.isdir(directory_path) and directory != "utils":
                for filename in os.listdir(directory_path):

                    if filename.endswith(".py"):
                        bot.load_extension(f"{directory}.{filename[:-3]}")

    except Exception as e:
        logger.error(f"Произошла ошибка при загрузке модулей\n╰─> Ошибка: {e}")
