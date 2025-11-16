import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from pythonjsonlogger import jsonlogger

from app.core.config import settings

from .protocols import LoggerProtocol, LogLevel

LOG_DIR = Path("var/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"


class FileLogger(LoggerProtocol):
    def __init__(self):
        self.logger = logging.getLogger("app")
        if self.logger.handlers:
            return

        level = logging.DEBUG if settings.APP_ENVIRONMENT != "prod" else logging.INFO
        self.logger.setLevel(level)

        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d %(funcName)s",
            timestamp=True,
        )

        # Консоль
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

        # Файл с ротацией
        file_handler = TimedRotatingFileHandler(
            LOG_FILE, when="midnight", interval=1, backupCount=7, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.suffix = "%Y-%m-%d"
        file_handler.namer = lambda name: name
        self.logger.addHandler(file_handler)

        # Ротация при старте
        file_handler.doRollover()

        self.logger.propagate = False

    def _log(self, level: int, message: str, context: dict | None):
        extra = context or {}
        self.logger.log(level, message, extra=extra)

    def emergency(self, message: str, context: dict | None = None):
        self._log(logging.CRITICAL, message, context)

    def alert(self, message: str, context: dict | None = None):
        self._log(logging.CRITICAL, message, context)

    def critical(self, message: str, context: dict | None = None):
        self._log(logging.CRITICAL, message, context)

    def error(self, message: str, context: dict | None = None):
        self._log(logging.ERROR, message, context)

    def warning(self, message: str, context: dict | None = None):
        self._log(logging.WARNING, message, context)

    def notice(self, message: str, context: dict | None = None):
        self._log(logging.INFO, message, context)

    def info(self, message: str, context: dict | None = None):
        self._log(logging.INFO, message, context)

    def debug(self, message: str, context: dict | None = None):
        self._log(logging.DEBUG, message, context)

    def log(self, level: LogLevel, message: str, context: dict | None = None):
        levels = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.NOTICE: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL,
            LogLevel.ALERT: logging.CRITICAL,
            LogLevel.EMERGENCY: logging.CRITICAL,
        }
        self._log(levels[level], message, context)


# Singleton
file_logger = FileLogger()
