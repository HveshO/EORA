import logging
import sys
from config import settings

_LOGGER_NAME = "eora_bot"


def _create_logger() -> logging.Logger:
    logger = logging.getLogger(_LOGGER_NAME)
    logger.propagate = False
    if logger.handlers:
        return logger

    level = logging.DEBUG if settings.DEBUG else logging.INFO
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


logger = _create_logger()
