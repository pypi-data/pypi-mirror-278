"""Logger for the FAST-HEP toolkit"""

from __future__ import annotations

import logging
import threading
from typing import Any

from rich.logging import RichHandler

DEFAULT_LOGGER_NAME = "FASTHEP"
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_TIME_FORMAT = "%H:%M:%S"
TRACE = 5  # log level for trace messages, below DEBUG (10)
TIMING = 11  # log level for timing, between DEBUG (10) and WARNING (30)
CONSOLE_HANDLER = "fasthep-console-handler"
FILE_HANDLER = "fasthep-file-handler"

_lock = threading.RLock()


def log_function_factory(custom_log_level: int) -> Any:
    """Factory function for creating a function that logs at a custom level"""

    def log_function(
        self: logging.Logger, message: str, *args: list[Any], **kws: dict[str, Any]
    ) -> None:
        """Log at custom_log_level"""
        if self.isEnabledFor(custom_log_level):
            # pylint: disable=protected-access
            self._log(custom_log_level, message, args, **kws)  # type: ignore[arg-type]

    return log_function


class FASTHEPLogger(logging.Logger):
    """Logger for the FAST-HEP toolkit"""

    TRACE: int = TRACE
    TIMING: int = TIMING
    trace = log_function_factory(TRACE)
    timing = log_function_factory(TIMING)

    def __init__(
        self, name: str = DEFAULT_LOGGER_NAME, level: int = logging.INFO
    ) -> None:
        super().__init__(name, level)

        # add TRACE log level and function to logger
        logging.addLevelName(TRACE, "TRACE")
        logging.TRACE = TRACE  # type: ignore[attr-defined]
        logging.addLevelName(TIMING, "TIMING")
        logging.TIMING = TIMING  # type: ignore[attr-defined]


class LevelFormatter(logging.Formatter):
    """
    From https://stackoverflow.com/a/28636024/362457
    """

    def __init__(self, fmt: str, datefmt: str, level_fmts: dict[int, str]):
        self._level_formatters = {}
        for level, _format in level_fmts.items():
            # Could optionally support level names too
            self._level_formatters[level] = logging.Formatter(
                fmt=_format, datefmt=datefmt
            )
        # self._fmt will be the default format
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record: logging.LogRecord) -> str:
        if record.levelno in self._level_formatters:
            return self._level_formatters[record.levelno].format(record)

        return super().format(record)


def create_console_handler(default_level: int = logging.INFO) -> RichHandler:
    """Create a RichHandler for logging to console with custom formatting."""
    console_handler = RichHandler(
        # rich_tracebacks=True, # does not work with custom formatters
        markup=True,
        show_level=False,
        show_time=False,
        show_path=False,
    )

    console_formatter = LevelFormatter(
        fmt="%(asctime)s [%(name)s]  %(levelname)s: %(message)s",
        datefmt=f"[{DEFAULT_DATE_FORMAT} {DEFAULT_TIME_FORMAT}]",
        level_fmts={
            logging.INFO: "%(message)s",
            logging.WARNING: "[bold dark_orange]%(levelname)s[/]: %(message)s",
            logging.ERROR: "[bold red]%(levelname)s[/]: %(message)s",
            logging.DEBUG: "[bold hot_pink]%(levelname)s[/]: %(message)s",
            FASTHEPLogger.TRACE: "[bold hot_pink]%(levelname)s[/]: %(message)s",
            FASTHEPLogger.TIMING: "[bold hot_pink]%(levelname)s[/]: %(message)s",
            logging.CRITICAL: "[bold blink bright_red]%(levelname)s[/]: %(message)s",
        },
    )

    console_handler.name = CONSOLE_HANDLER
    console_handler.setLevel(default_level)
    console_handler.setFormatter(console_formatter)
    console_handler.formatter = console_formatter

    return console_handler


def setup_logger(
    logger_name: str = DEFAULT_LOGGER_NAME,
    default_level: int = logging.INFO,
    log_file: str | None = None,
) -> logging.Logger:
    """Sets up a logging.Logger with specified log level and log file.
    If log_file is None, logs to stdout."""
    logging.setLoggerClass(FASTHEPLogger)
    logger = logging.getLogger(logger_name)

    with _lock:
        logger.propagate = False

        handler_names = [handler.name for handler in logger.handlers]
        if not log_file and CONSOLE_HANDLER not in handler_names:
            # only log to console if no log file is specified
            console_handler = create_console_handler(default_level)

            logger.addHandler(console_handler)
            logger.setLevel(default_level)

            return logger

        if not log_file or FILE_HANDLER in handler_names:
            # do not add file handler if it already exists
            return logger

        logfile_formatter = logging.Formatter(
            "%(asctime)s [%(name)s]  %(levelname)s: %(message)s"
        )
        logfile_handler = logging.FileHandler(log_file)
        logfile_handler.name = FILE_HANDLER
        logfile_handler.setLevel(default_level)
        logfile_handler.setFormatter(logfile_formatter)
        logger.addHandler(logfile_handler)
        logger.setLevel(default_level)

    return logger


def get_logger(
    logger_name: str = DEFAULT_LOGGER_NAME,
    default_level: int = logging.INFO,
    log_file: str | None = None,
) -> logging.Logger:
    """Returns the logger for the FAST-HEP toolkit"""
    tmp_class = logging.getLoggerClass()
    setup_logger(logger_name, default_level, log_file)
    logging.setLoggerClass(tmp_class)
    return logging.getLogger(logger_name)


def getLogger(  # pylint: disable=invalid-name
    name: str = DEFAULT_LOGGER_NAME,
) -> logging.Logger:
    """Compatible with the standard logging.getLogger() function"""
    return get_logger(name)
