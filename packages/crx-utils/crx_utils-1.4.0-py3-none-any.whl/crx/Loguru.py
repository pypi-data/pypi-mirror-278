import os
import sys

from loguru import logger
from datetime import datetime

os.makedirs("settings/logs", exist_ok=True)

log_file_path = os.path.join("settings/logs", f"{datetime.now().strftime('%Y-%m-%d')}.log")
logger.remove(0)

logger.add(
    sys.stderr,
    format="<blue>[{time:HH:mm:ss}]</blue> <yellow>({level})</yellow> <red>|→</red> <green>{message}</green>",
    colorize=True,
    level="INFO",
    filter=lambda record: record["level"].name == "INFO",
)

logger.add(
    sys.stderr,
    format="<blue>[{time:HH:mm:ss}]</blue> <yellow>({level})</yellow> |> <yellow>{message}</yellow>",
    colorize=True,
    level="WARNING",
    filter=lambda record: record["level"].name == "WARNING",
)

logger.add(
    sys.stderr,
    format="<blue>[{time:HH:mm:ss}]</blue> <red>({level})|→ {message}</red>",
    colorize=True,
    level="ERROR",
    filter=lambda record: record["level"].name == "ERROR"
)

logger.add(
    log_file_path,
    format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {file}:{line} - {message}",
    level="ERROR",
    enqueue=True,
    rotation="1 day",
    retention="7 day"
)
