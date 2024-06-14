"""A module for logging enhancements.

This module provides a function for setting up a fancy logging configuration.
Rich is used for console logging and python-json-logger is used for file
logging.
"""

from __future__ import annotations

import logging
import logging.config
import pathlib
from typing import Optional, Union

from pythonjsonlogger.jsonlogger import RESERVED_ATTRS
from rich.console import Console as RichConsole
from rich.traceback import install as install_rich_traceback


def setup_fancy_logging(
    base_logger_name: str,
    console_log_level: Union[str, int] = logging.INFO,
    file_log_level: Union[str, int] = logging.NOTSET,
    file_log_path: Optional[Union[str, pathlib.Path]] = None,
    log_attributes: Optional[list[str]] = None,
    file_mode: str = "w",
    console: Optional[RichConsole] = None,
):
    """
    Creates a logging configuration dictionary for logging.config.dictConfig,

    Uses rich logger for console and python-json-logger for file logging.


    for more info on the rich logger see:
    https://rich.readthedocs.io/en/stable/logging.html

    for more info on the JSON logger see:
    https://github.com/madzak/python-json-logger

    This function configures a logger using the provided `base_logger_name`. It
    ensures that all loggers created under this base name will inherit its
    configuration. This is particularly useful for creating a unified logging
    setup across different modules in an application.

    When a logger is created with a name that is a 'dot-separated' hierarchical
    path starting with `base_logger_name`, it inherits the configuration from
    this base logger. For example, if `base_logger_name` is 'myapp', loggers
    with names like 'myapp.module' or 'myapp.module.submodule' will inherit the
    settings from the 'myapp' logger.

    Args:
        base_logger_name: The name of the base logger. This is the logger that
            will be used by all modules that do not have a logger set in
            "loggers".
        console_log_level: The level at which to log to the console.
        file_log_level: The level at which to log to the file. to the log file.
            `file_log_level` options are 'w' and 'a'. Defaults to 'w'.
        log_attributes: The attributes to log. See:
            https://docs.python.org/3/library/logging.html#logrecord-attributes
            If 'w', the log file will be overwritten. If 'a', the log file will
            be appended to.
        console: The rich console to use for logging. If None, a new console
            will be created.
    """
    if log_attributes is None:
        log_attributes = [
            "levelname",
            "levelno",
            "name",
            "module",
            "filename",
            "lineno",
            "funcName",
            "pathname",
            "message",
            "msg",
            "created",
            "asctime",
            "process",
            "processName",
            "exc_info",
            "stack_info",
        ]

    if file_log_level != logging.NOTSET:
        if file_log_path is None:
            file_log_path = (
                pathlib.Path(__file__).parent
                / "logs"
                / f"{base_logger_name}.json"
            )
        else:
            file_log_path = pathlib.Path(file_log_path)
        file_log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers_list = ["rich_console", "json_file"]
    else:
        handlers_list = ["rich_console"]

    log_format = " ".join(f"%({field})s" for field in log_attributes)

    logging_config_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": log_format,
                "reserved_attrs": RESERVED_ATTRS
                + ("taskName",),  # to make it work with Python 3.12
            },
        },
        "handlers": {
            "rich_console": {
                "class": "rich.logging.RichHandler",
                "level": console_log_level,
                "show_time": True,
                "omit_repeated_times": True,
                "show_level": True,
                "show_path": True,
                "enable_link_path": True,
                "markup": True,
                "rich_tracebacks": True,
                "tracebacks_word_wrap": True,
                "tracebacks_show_locals": False,
                "locals_max_length": 10,
                "locals_max_string": 80,
                "log_time_format": "[%X]",
                "console": console,
            },
            "json_file": {
                "class": "logging.FileHandler",
                "level": file_log_level,
                "filename": file_log_path,
                "mode": file_mode,
                "formatter": "json",
            },
        },
        "loggers": {
            base_logger_name: {
                # the default logger whenever logging.getLogger is called
                "handlers": handlers_list,
                "propagate": False,
                "level": "DEBUG",
            },
            "unhandled_exception": {
                "handlers": handlers_list,
                "propagate": False,
                "level": "ERROR",
            },
        },
        "root": {
            # the default logger for all modules without a logger in "loggers"
            "handlers": ["json_file"]
            if file_log_level != logging.NOTSET
            else [],
            "level": "WARNING",
        },
    }

    install_rich_traceback(console=console)
    logging.config.dictConfig(logging_config_dict)


if __name__ == "__main__":
    print("Started")
    setup_fancy_logging(
        base_logger_name="test",
        console_log_level="DEBUG",
        file_log_level="DEBUG",
        file_log_path="test.json",
        log_attributes=[
            "levelname",
            "levelno",
            "name",
            "module",
            "filename",
            "lineno",
            "funcName",
            "pathname",
            "message",
            "msg",
            "created",
            "asctime",
            "process",
            "processName",
            "exc_info",
            "stack_info",
        ],
    )
    logger = logging.getLogger("test")

    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    logger.critical("critical message")
    logger.log(99, "custom level message")

    logger = logging.getLogger("test.test")

    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    logger.critical("critical message")
    logger.log(99, "custom level message")

    raise ValueError("Test exception")
