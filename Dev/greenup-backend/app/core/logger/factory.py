from app.core.config import settings

from .console_logger import console_logger
from .file_logger import file_logger
from .protocols import LoggerProtocol


def get_logger() -> LoggerProtocol:
    logger_channel = getattr(settings, "LOGGER_CHANNEL", "file").lower()
    if logger_channel == "file":
        return file_logger
    elif logger_channel == "console":
        return console_logger
    else:
        raise ValueError(f"Unknown LOGGER_CHANNEL: {logger_channel}")
