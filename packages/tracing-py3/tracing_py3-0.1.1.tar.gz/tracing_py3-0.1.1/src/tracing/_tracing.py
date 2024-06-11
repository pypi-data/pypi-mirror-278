# -- Future Imports -- (Use with caution, may not work as expected in all cases)
from __future__ import annotations

# -- STL Imports --
from dataclasses import dataclass
from os import environ
from types import TracebackType
from typing import (
    Optional,
    Type,
    TypeAlias,
    Mapping,
   # override, # Python 3.12 feature, enable when available
)
import logging
import traceback

# -- Libray Imports --
from basic_panic import Panic, PanicHandler

# -- Package Imports --
from tracing._store import Store
from tracing._level import Level

ENV_TRUTHY = ("1", "on", "true", "t", "yes", "y", "enable", "enabled")
"""Represents the truthy values for string parsed boolean values."""


class CliLogFormatter(logging.Formatter):
    """
    This is a custom log formatter for command line interface. It extends the
    built-in Formatter class of the logging module.

    Inhertance:
        logging.Formatter
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        This method formats the specified log record as text.

        Args:
            record (logging.LogRecord): The record to be formatted.

        Returns:
            str: The formatted record.
        """

        # Depending on the severity level of the log record, we color the level name
        # differently. This is done by wrapping the level name with ANSI escape codes.

        # Debug logging level; Blue
        if record.levelno == logging.DEBUG:
            record.__dict__["color"] = "\033[1;34m"
            record.__dict__["icon"] = "[*]"

        # Info logging level; Green
        elif record.levelno == logging.INFO:
            record.__dict__["color"] = "\033[1;32m"
            record.__dict__["icon"] = "[+]"

        # Warning logging level; Yellow
        elif record.levelno == logging.WARNING:
            record.__dict__["color"] = "\033[1;33m"
            record.__dict__["icon"] = "[?]"

        # Error logging level; Red
        elif record.levelno == logging.ERROR:
            record.__dict__["color"] = "\033[1;31m"
            record.__dict__["icon"] = "[!]"

        # Critical logging level; Red Background
        elif record.levelno == logging.CRITICAL:
            record.__dict__["color"] = "\033[1;41m"
            record.__dict__["icon"] = "[~]"

        # Call the parent class format method to do the actual formatting
        return super().format(record)

    def __init__(self) -> None:
        """
        Initialize the formatter with a specific format and date format.
        """
        super().__init__(fmt = "%(color)s%(icon)s %(message)s\033[0m")


def _build_logger(pkgname: str | None, file: str | None, level: Level) -> logging.Logger:
    """
    This function builds and returns a logger with a stream handler and a custom formatter.

    Args:
        pkgname (str | None): The package name.
        file (str | None): The file to log to.
        level (Level): The logging level.

    Returns:
        logging.Logger: The logger.
    """
    # Get a logger with the package name
    logger = logging.getLogger(pkgname)

    # Create a stream handler that sends log messages to the console
    sh = logging.StreamHandler()
    sh.setFormatter(CliLogFormatter())
    logger.addHandler(sh)

    # If a file is specified, create a file handler that sends log messages to the file
    if file is not None:
        fh = logging.FileHandler(file)
        fh.setFormatter(logging.Formatter("[%(asctime)s - %(name)s - %(levelname)s] %(message)s"))
        logger.addHandler(fh)

    # Add the stream handler to the logger
    logger.setLevel(level.value)

    # Return the logger
    return logger


_g_logger: logging.Logger = _build_logger("unkown", None, Level.INFO)
"""Global logger variable. Will be initialized by the setup function. Default is None."""


def _g_logger_guard() -> logging.Logger:
    """
    This function returns the global logger. If the global logger is not initialized, it raises a
    ValueError.

    Returns:
        logging.Logger: The global logger.
    """
    global _g_logger

    if _g_logger is None:
        raise ValueError("Logger is not initialized")

    return _g_logger


_SysExcInfoType: TypeAlias = tuple[Type[BaseException], BaseException,
                                   TracebackType | None] | tuple[None, None, None]
"""Type alias for the sys.exc_info() tuple."""

_ExcInfoType: TypeAlias = None | bool | _SysExcInfoType | BaseException
"""Type alias for the exc_info argument of the logging functions."""


def setup(pkgname: str | None = None, level: Level = Level.INFO, file: str | None = None) -> None:
    """Initializes the logger with a stream handler and a custom formatter.

    Args:
        pkgname (str | None): The package name. Defaults to None.
        level (Level): The logging level. Defaults to Level.INFO.
        file (str | None): The file to log to. Defaults to None.
    """
    global _g_logger

    _g_logger.handlers.clear()
    del _g_logger

    _g_logger = _build_logger(pkgname, file, level)


def set_level(level: Level) -> None:
    """Sets the logging level of the logger.

    Args:
        level (Level): The logging level.
    """
    _g_logger_guard().setLevel(level.value)


def get_level() -> Level:
    """Returns the logging level of the logger.

    Returns:
        Level: The logging level.
    """
    return Level.from_int(_g_logger_guard().getEffectiveLevel())


def dbg(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None
) -> None:
    """
    Log 'msg % args' with severity 'DEBUG'.
    To pass exception information, use the keyword argument exc_info with a true value, e.g.::

        tracing.debug("Houston, we have a %s", "message", exc_info=True)

    Args:
        msg (object): The message to log.
        *args (object): The arguments for the message.
        exc_info (bool | tuple[Type[BaseException], BaseException, TracebackType | None]): If true,
        exception information is added to the logging message.
        stack_info (bool): If true, stack information is added to the logging message.
        stacklevel (int): If greater than 1, the stacklevel is adjusted.
        extra (Mapping[str, object] | None): Extra information to be added to the log record.
    """
    _g_logger_guard().log(
        logging.DEBUG,
        msg,
        *args,
        exc_info = exc_info,
        stack_info = stack_info,
        stacklevel = stacklevel,
        extra = extra
    )


def info(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None
) -> None:
    """
    Log 'msg % args' with severity 'INFO'.
    To pass exception information, use the keyword argument exc_info with a true value, e.g.::

        tracing.info("Houston, we have a %s", "message", exc_info=True)

    Args:
        msg (object): The message to log.
        *args (object): The arguments for the message.
        exc_info (bool | tuple[Type[BaseException], BaseException, TracebackType | None]): If true,
        exception information is added to the logging message.
        stack_info (bool): If true, stack information is added to the logging message.
        stacklevel (int): If greater than 1, the stacklevel is adjusted.
        extra (Mapping[str, object] | None): Extra information to be added to the log record.
    """
    _g_logger_guard().log(
        logging.INFO,
        msg,
        *args,
        exc_info = exc_info,
        stack_info = stack_info,
        stacklevel = stacklevel,
        extra = extra
    )


def warn(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None
) -> None:
    """
    Log 'msg % args' with severity 'WARNING'.
    To pass exception information, use the keyword argument exc_info with a true value, e.g.::

        tracing.warn("Houston, we have a %s", "problem", exc_info=True)

    Args:
        msg (object): The message to log.
        *args (object): The arguments for the message.
        exc_info (bool | tuple[Type[BaseException], BaseException, TracebackType | None]): If true,
        exception information is added to the logging message.
        stack_info (bool): If true, stack information is added to the logging message.
        stacklevel (int): If greater than 1, the stacklevel is adjusted.
        extra (Mapping[str, object] | None): Extra information to be added to the log record.
    """
    _g_logger_guard().log(
        logging.WARNING,
        msg,
        *args,
        exc_info = exc_info,
        stack_info = stack_info,
        stacklevel = stacklevel,
        extra = extra
    )


def err(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None
) -> None:
    """
    Log 'msg % args' with severity 'ERROR'.
    To pass exception information, use the keyword argument exc_info with a true value, e.g.::

        tracing.error("Houston, we have a %s", "major problem", exc_info=True)

    Args:
        msg (object): The message to log.
        *args (object): The arguments for the message.
        exc_info (bool | tuple[Type[BaseException], BaseException, TracebackType | None]): If true,
        exception information is added to the logging message.
        stack_info (bool): If true, stack information is added to the logging message.
        stacklevel (int): If greater than 1, the stacklevel is adjusted.
        extra (Mapping[str, object] | None): Extra information to be added to the log record.
    """
    _g_logger_guard().log(
        logging.ERROR,
        msg,
        *args,
        exc_info = exc_info,
        stack_info = stack_info,
        stacklevel = stacklevel,
        extra = extra
    )


def crit(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None
) -> None:
    """
    Log 'msg % args' with severity 'CRITICAL'.
    To pass exception information, use the keyword argument exc_info with a true value, e.g.::

        tracing.crit("Houston, we have a %s", "major disaster", exc_info=True)

    Args:
        msg (object): The message to log.
        *args (object): The arguments for the message.
        exc_info (bool | tuple[Type[BaseException], BaseException, TracebackType | None]): If true,
        exception information is added to the logging message.
        stack_info (bool): If true, stack information is added to the logging message.
        stacklevel (int): If greater than 1, the stacklevel is adjusted.
        extra (Mapping[str, object] | None): Extra information to be added to the log record.
    """
    _g_logger_guard().log(
        logging.CRITICAL,
        msg,
        *args,
        exc_info = exc_info,
        stack_info = stack_info,
        stacklevel = stacklevel,
        extra = extra
    )


@dataclass
class TracingPanicHandler(PanicHandler):
    """
    A custom panic handler that logs panics with severity 'CRITICAL'. If the environment variable
    TRACING_BACKTRACE is set to a truthy value, the backtrace is printed to stderr. The panic can
    also be saved to a store, by default the panic is not saved.

    Attributes:
        panic_store (Store[Panic] | None): The store to save the panic to. Default is None.

    Example usage:

        without TRACING_BACKTRACE env variable set::

            >>> with TracePanicHandler():
            ...    panic("Something went wrong")
            ...
            [~] PANIC [Errno 1]: Something went wrong

        with TRACING_BACKTRACE env variable set::

            >>> with TracePanicHandler():
            ...    panic("Something went wrong")
            ...
            [~] PANIC [Errno 1]: Something went wrong
            <backtrace>
    """

    panic_store: Optional[Store[Panic]] = None

    # @override # Python 3.12 feature, enable when available
    def on_panic(self, p: Panic) -> None:
        tb = ""

        if environ.get("TRACING_BACKTRACE", "").lower() in ENV_TRUTHY:
            tb = "\n... " + "\n... ".join(traceback.format_exc().splitlines())

        crit("PANIC [Errno %i]: %s%s", p.code, p.message, tb)

        if self.panic_store is not None:
            self.panic_store.set(p)
