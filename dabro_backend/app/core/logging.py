import logging
import sys

from app.core.config import settings


def setup_logger() -> None:
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL or logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(levelname)s %(name)s %(message)s",
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
