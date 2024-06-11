"""Functions to add in creating/working with the logging config classes in this module."""

from __future__ import annotations

import logging

log = logging.getLogger("red_logging.std.logging_utils")

from copy import deepcopy
from pathlib import Path
import typing as t

from red_logging.__base import BASE_LOGGING_CONFIG_DICT
from red_logging.config_classes.formatters import FormatterConfig
from red_logging.config_classes.handlers import (
    FileHandlerConfig,
    QueueHandlerConfig,
    QueueListenerConfig,
    RotatingFileHandlerConfig,
    SocketHandlerConfig,
    StreamHandlerConfig,
    TimedRotatingFileHandlerConfig,
)
from red_logging.config_classes.loggers import (
    LoggerConfig,
    LoggerFactory,
)
from red_logging.config_classes.types import (
    HANDLER_CLASSES_TYPE,
    HANDLER_CLASSES_TYPE_ANNOTATION,
    LOGGING_CONFIG_DICT_TYPE,
    LOGGING_CONFIG_DICT_TYPE_ANNOTATION,
)
from red_logging.fmts import (
    DATE_FMT_DATE_ONLY,
    DATE_FMT_STANDARD,
    DATE_FMT_TIME_ONLY,
    MESSAGE_FMT_BASIC,
    MESSAGE_FMT_DETAILED,
    MESSAGE_FMT_STANDARD,
    red_logging_DETAIL_FMT,
    red_logging_FMT,
)

def _ensure_logdir(p: t.Union[str, Path] = None) -> None:
    """Ensure a directory exists.

    Used by logging FileHandlers (RotatingFileHandler, TimedRotatingFileHandler, etc) if
    a logging file path is nested, like `logs/example/test.log`.

    Params:
        p (str | Path): A path to a logging directory, i.e. `logs/`, `logs/app/`, `logs/app/dev/`.
            This should *not* be the full path to a logging config, like `logs/app/test.log`; instead,
            call this function like `_ensure_logdir(p=log_filename.parent)`.

    Raises:
        PermissionError: When permission to create the path in `p` is denied.
        Exception: When any unhandled exception occurs.

    """
    p: Path = Path(f"{p}")
    if "~" in f"{p}":
        p = p.expanduser()

    if not p.exists():
        try:
            p.mkdir(parents=True, exist_ok=True)
        except PermissionError as perm_err:
            msg = Exception(f"Permission denied creating path '{p}'. Details: {exc}")
            log.error(msg)

            raise perm_err
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception creating directory '{p}'. Details: {exc}"
            )
            log.error(msg)

            raise exc
    else:
        return


def get_rotatingfilehandler_config(
    name: str = "rotating_app_file",
    level: str = "DEBUG",
    formatter: str = "default",
    filters: list | None = None,
    filename: t.Union[str, Path] = None,
    maxBytes: int = 100000,
    backupCount: int = 3,
    as_dict: bool = False,
) -> dict[str, dict[str, t.Any]] | RotatingFileHandlerConfig:
    """Return a RotatingFileHandlerConfig, or a dict representing a RotatingFileHandler.

    Params:
        name (str): The name for the rotating file handler. Reference this handler by name in a LoggerConfig.
        level (str): The logging level for this handler (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL).
        formatter (str): The name of a formatter that exists in the overall logging dictConfig.
        filters (list[str] | None): A list of function names for logging filters.
        filename (str | Path): The full path to the log file you want to create. If parent directories do not exist,
            this method will handle creating them.
        maxBytes (int): The maximum size (in bytes) before a logfile is rotated.
        backupCount (int): The number of backups to keep as log files rotate.
        as_dict (bool): If `True`, return the configuration as a dict that can be joined into `dictConfig()`.

    Returns:
        (dict[str, dict[str, Any]]): If `as_dict=True`, return a config dict instead of a RotatingFileHandlerConfig object.
        (RotatingFileHandlerConfig): If `as_dict=False`, return a RotatingFileHandlerConfig object.

    """
    ## Convert & optionally expand input path
    filename: Path = Path(f"{filename}")
    if "~" in f"{filename}":
        filename = filename.expanduser()

    ## Create parent dirs for logging file, if they don't exist
    _ensure_logdir(p=filename.parent)

    try:
        ## Initialize handler object
        _handler: RotatingFileHandlerConfig = RotatingFileHandlerConfig(
            name=name,
            level=level,
            formatter=formatter,
            filters=filters,
            filename=filename,
            maxBytes=maxBytes,
            backupCount=backupCount,
        )

        if as_dict:
            ## Return handler representation as a dict
            return _handler.get_configdict()
        else:
            ## Return RotatingFileHandlerConfig object
            return _handler

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception building RotatingFileHandlerConfig. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_streamhandler_config(
    name: str = "console",
    level: str = "INFO",
    formatter: str = "default",
    filters: list | None = None,
    stream: str = "ext://sys.stdout",
    as_dict: bool = False,
) -> dict[str, dict[str, str]] | StreamHandlerConfig:
    """Return a StreamHandlerConfig, or a dict representing a StreamingHandler.

    Params:
        name (str): The name for the stream handler. Reference this handler by name in a LoggerConfig.
        level (str): The logging level for this handler (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL).
        formatter (str): The name of a formatter that exists in the overall logging dictConfig.
        filters (list[str] | None): A list of function names for logging filters.
        stream (str): The stream this handler should use, i.e. `ext://sys.stdout`, `ext://sys.stderr`, etc.
        as_dict (bool): If `True`, return the configuration as a dict that can be joined into `dictConfig()`.

    Returns:
        (dict[str, dict[str, Any]]): If `as_dict=True`, return a config dict instead of a StreamHandlerConfig object.
        (StreamHandlerConfig): If `as_dict=False`, return a StreamHandlerConfig object.

    """
    try:
        ## Initialize handler object
        _handler: StreamHandlerConfig = StreamHandlerConfig(
            name=name, level=level, formatter=formatter, filters=filters, stream=stream
        )

        if as_dict:
            ## Return handler representation as a dict
            return _handler.get_configdict()
        else:
            ## Return StreamHandlerConfig object
            return _handler

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception building StreamHandlerConfig. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_formatter_config(
    name: str = "default",
    fmt: str = MESSAGE_FMT_STANDARD,
    datefmt: str = DATE_FMT_STANDARD,
    style: str = "%",
    validate: bool = True,
    as_dict: bool = False,
) -> dict[str, dict[str, str]] | FormatterConfig:
    """Return a FormatterConfig, or a dict representing a Formatter.

    Params:
        name (str): The name for the formatter. Reference this formatter by name in a LoggerConfig.
        fmt (str): The string format for log messages.
            [Python docs: Log Record Attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes)
        datefmt (str): The format for log message timestamps, if `%(asctime)s` is used in the logging `fmt`.
        style (str): The style of string substitution to use for the formatter. Options include `%` for `'%', some_var`,
            `{` for `'{some_var}`, etc.
        validate (bool): If `True`, the handler will be validated by the logging module before fully initializing.
        as_dict (bool): If `True`, return the configuration as a dict that can be joined into `dictConfig()`.

    Returns:
        (dict[str, dict[str, Any]]): If `as_dict=True`, return a config dict instead of a FormatterConfig object.
        (FormatterConfig): If `as_dict=False`, return a FormatterConfig object.

    """
    try:
        ## Initialize formatter object
        _formatter: FormatterConfig = FormatterConfig(
            name=name, fmt=fmt, datefmt=datefmt, style=style, validate=validate
        )

        if as_dict:
            ## Return formatter representation as a dict
            return _formatter.get_configdict()
        else:
            ## Return FormatterConfig object
            return _formatter
    except Exception as exc:
        msg = Exception(f"Unhandled exception building FormatterConfig. Details: {exc}")
        log.error(msg)

        raise exc


def get_logger_config(
    name: str = "app",
    handlers: list[str] = ["console"],
    level: str = "DEBUG",
    propagate: bool = False,
    as_dict: bool = False,
) -> dict[str, dict[str, str]] | LoggerConfig:
    """Return a LoggerConfig, or a dict representing a Logger.

    Params:
        name (str): The name for the logger. Reference this logger by name in a LoggerConfig.
        level (str): The logging level for this handler (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL).
        handlers (list[str]): List of handler names that exist in the logging configDict that this logger should use.
        propagate (bool): If `True`, log messages will be propagated up/down to the root logger.
        as_dict (bool): If `True`, return the configuration as a dict that can be joined into `dictConfig()`.

    Returns:
        (dict[str, dict[str, Any]]): If `as_dict=True`, return a config dict instead of a RotatingFileHandlerConfig object.
        (RotatingFileHandlerConfig): If `as_dict=False`, return a RotatingFileHandlerConfig object.

    """
    try:
        ## Initialize logger object
        _logger: LoggerConfig = LoggerConfig(
            name=name, level=level.upper(), handlers=handlers, propagate=propagate
        )

        if as_dict:
            ## Return logger representation as a dict
            return _logger.get_configdict()
        else:
            ## Return LoggerConfig object
            return _logger

    except Exception as exc:
        msg = Exception(f"Unhandled exception initializing logger. Details: {exc}")
        log.error(msg)

        raise exc


def assemble_configdict(
    disable_existing_loggers: bool = False,
    propagate: bool = False,
    root_handlers: list[str] = ["console"],
    root_level: str = "DEBUG",
    formatters: (
        t.Union[list[FormatterConfig], list[LOGGING_CONFIG_DICT_TYPE_ANNOTATION]] | None
    ) = None,
    handlers: (
        t.Union[HANDLER_CLASSES_TYPE_ANNOTATION, LOGGING_CONFIG_DICT_TYPE_ANNOTATION]
        | None
    ) = None,
    loggers: (
        t.Union[
            list[t.Union[LoggerConfig, LoggerFactory]],
            list[LOGGING_CONFIG_DICT_TYPE_ANNOTATION],
        ]
        | None
    ) = None,
) -> dict[str, t.Any]:
    """Build a logging dictConfig dict.

    Description:
        ```python title="Example logging config dict" linenums="1"
        logging_config: dict = {
            "version": 1,
            "disable_existing_loggers": False,
            "propagate": True,
            "root": {},
            "formatters": {},
            "handlers": {},
            "loggers": {},
        }
        ```

    Params:
        disable_existing_loggers (bool): When `True`, disables all currently configured loggers to "start fresh."
        propagate (bool): When `True`, log messages will propagate up/down to the root logger.
        root_handlers (list[str]): List of handlers for the root logger. These handler configs must exist in the logging dictConfig.
        root_level (str): The log level for the root logger.
        formatters (list[FormatterConfig] | list[dict[str, dict[str, t.Any]]] | None): List of logging formatter config objects.
        handlers (list[BaseHandlerConfig | dict[str, dict[str, t.Any]]] | None): List of logging handler config objects.
        loggers (list[LoggerConfig | LoggerFactory | dict[str, dict[str, t.Any]]]] | None): List of logging logger config objects.

    Returns:
        (dict[str, Any]): An initialized logging config dict created from inputs. Used with `logging.config.dictConfig()`

    """
    ## Get base logging configDict object, with empty formatters, loggers, etc
    logging_config: dict[str, t.Any] = BASE_LOGGING_CONFIG_DICT

    ## Set logging config options
    logging_config["disable_existing_loggers"] = disable_existing_loggers
    logging_config["propagate"] = propagate

    ## Build root logger
    config_key_root = {
        ## Set handlers
        "handlers": root_handlers,
        ## Set log level string
        "level": root_level.upper(),
    }

    ## Update config dict's `root` key
    logging_config["root"] = config_key_root

    ## Initialize formatter, handler, logger config dicts
    formatter_configdicts: LOGGING_CONFIG_DICT_TYPE = {}
    handler_configdicts: LOGGING_CONFIG_DICT_TYPE = {}
    logger_configdicts: LOGGING_CONFIG_DICT_TYPE = {}

    if formatters is not None:
        ## Formatters passed to function, parse and add to config
        for formatter_dict in formatters:
            if isinstance(formatter_dict, dict):
                pass
            elif isinstance(formatter_dict, FormatterConfig):
                try:
                    formatter_dict: dict = formatter_dict.get_configdict()
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception getting config dict for FormatterConfig object. Details: {exc}"
                    )
                    log.error(msg)

                    raise exc

            formatter_configdicts.update(formatter_dict)

    if handlers is not None:
        ## Handlers passed to function, parse and add to config
        for handler_dict in handlers:
            if isinstance(handler_dict, dict):
                pass
            elif isinstance(handler_dict, HANDLER_CLASSES_TYPE):
                try:
                    handler_dict = handler_dict.get_configdict()
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception getting config dict for *HandlerConfig object. Details: {exc}"
                    )
                    log.error(msg)

                    raise exc

            handler_configdicts.update(handler_dict)

    if loggers:
        ## Loggers passed to function, parse and add to config
        for logger_dict in loggers:
            if isinstance(logger_dict, dict):
                pass
            elif isinstance(logger_dict, LoggerConfig):
                try:
                    logger_dict = logger_dict.get_configdict()
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception getting config dict for LoggerConfig object. Details: {exc}"
                    )
                    log.error(msg)

                    raise exc

            logger_configdicts.update(logger_dict)

    ## Create a copy of the original config
    try:
        return_dict = deepcopy(logging_config)
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception copying original logging config. Proceeding with original logging config"
        )
        log.warning(msg)

        return_dict = logging_config

    ## Update formatters, handlers, loggers in logging config copy
    return_dict["formatters"] = formatter_configdicts
    return_dict["handlers"] = handler_configdicts
    return_dict["loggers"] = logger_configdicts

    ## Return initialized logging config
    return return_dict
