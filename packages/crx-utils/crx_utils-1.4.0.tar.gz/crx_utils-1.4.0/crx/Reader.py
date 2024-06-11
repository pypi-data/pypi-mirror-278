from loguru import logger
from aiofiles import open
from fastenv import load_dotenv
from json import JSONDecodeError, loads, dumps

async def read_json(path: str, *keys):
    try:
        async with open(path, mode="r", encoding="utf-8") as file:
            file_content = await file.read()
            file_data = loads(file_content)

            if keys:
                for key in keys:
                    if key not in file_data:
                        logger.error(f"Ключ: {key} не найден в файле {path}")
                        return None
                    
                    file_data = file_data[key]

                return file_data
            else:
                return file_data
    
    except FileNotFoundError as e:
        logger.error(f"Указанный файл по пути: {path} не найден\n╰─> Ошибка: {e}")
    except JSONDecodeError as e:
        logger.error(f"Ошибка в файле: {path}\n╰─> Ошибка: {e}")
    except Exception as e:
        logger.error(f"Произошла неизвестная ошибка при чтений файла: {path}\n╰─> Ошибка: {e}")

async def write_json(path: str, data: dict, encoding="utf-8"):
    async with open(path, mode="w", encoding=encoding) as file:
        await file.write(dumps(data, ensure_ascii=False, indent=2))

async def read_env(path):
    bot_settings = await load_dotenv(path)
    return bot_settings
