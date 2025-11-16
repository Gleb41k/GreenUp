import logging
import sys

from pythonjsonlogger import jsonlogger

from .protocols import LoggerProtocol, LogLevel

# Цвета для консоли
COLORS = {
    LogLevel.DEBUG: "\033[36m",  # cyan
    LogLevel.INFO: "\033[32m",  # green
    LogLevel.NOTICE: "\033[34m",  # blue
    LogLevel.WARNING: "\033[33m",  # yellow
    LogLevel.ERROR: "\033[31m",  # red
    LogLevel.CRITICAL: "\033[41m",  # red bg
    LogLevel.ALERT: "\033[41m\033[37m",  # red bg + white
    LogLevel.EMERGENCY: "\033[41m\033[37m",
}
RESET = "\033[0m"


class ConsoleLogger(LoggerProtocol):
    def __init__(self):
        self.logger = logging.getLogger("console")
        if self.logger.handlers:
            return

        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d %(funcName)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def _log(self, level: LogLevel, message: str, context: dict | None):
        level_name = level.value.upper()
        color = COLORS.get(level, "")
        extra = context or {}
        extra.update({"level": level_name, "color": color, "reset": RESET})
        log_func = {
            LogLevel.DEBUG: self.logger.debug,
            LogLevel.INFO: self.logger.info,
            LogLevel.NOTICE: self.logger.info,
            LogLevel.WARNING: self.logger.warning,
            LogLevel.ERROR: self.logger.error,
            LogLevel.CRITICAL: self.logger.critical,
            LogLevel.ALERT: self.logger.critical,
            LogLevel.EMERGENCY: self.logger.critical,
        }[level]

        # Формируем цветной вывод
        prefix = f"{color}[{level_name}]{RESET} " if color else f"[{level_name}] "
        log_func(f"{prefix}{message}", extra=extra)

    def emergency(self, message: str, context: dict | None = None):
        self._log(LogLevel.EMERGENCY, message, context)

    def alert(self, message: str, context: dict | None = None):
        self._log(LogLevel.ALERT, message, context)

    def critical(self, message: str, context: dict | None = None):
        self._log(LogLevel.CRITICAL, message, context)

    def error(self, message: str, context: dict | None = None):
        self._log(LogLevel.ERROR, message, context)

    def warning(self, message: str, context: dict | None = None):
        self._log(LogLevel.WARNING, message, context)

    def notice(self, message: str, context: dict | None = None):
        self._log(LogLevel.NOTICE, message, context)

    def info(self, message: str, context: dict | None = None):
        self._log(LogLevel.INFO, message, context)

    def debug(self, message: str, context: dict | None = None):
        self._log(LogLevel.DEBUG, message, context)

    def log(self, level: LogLevel, message: str, context: dict | None = None):
        self._log(level, message, context)


# Singleton
console_logger = ConsoleLogger()
