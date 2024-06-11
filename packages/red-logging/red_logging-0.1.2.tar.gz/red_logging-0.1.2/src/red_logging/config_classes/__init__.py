"""The 'secret sauce' of the logging module.

These classes serve as configuration containers for various logging objects, like formatters,
handlers, and loggers. Each class inherits from a "base" configuration, which has a `.get_configdict()`
method. So for each formatter, handler, or logger, you can use `.get_configdict()` to return a dict representation
of the class's configuration, which is compatible with the logging dictConfig.

These dicts must be added to the configuration using the `.assemble_configdict()` method in `logging_utils()`. The classes
exist to aid in creating formatters, handlers, and loggers for a logging configuration by presenting all available options.

"""

from __future__ import annotations

from . import prefab
from .base import BASE_LOGGING_CONFIG_DICT
from .filters import (
    critical_filter,
    debug_filter,
    error_filter,
    info_filter,
    warning_filter,
)
from .formatters import FormatterConfig
from .handlers import FileHandlerConfig, RotatingFileHandlerConfig, StreamHandlerConfig
from .loggers import LoggerConfig, LoggerFactory
from .prefab import third_party
from .prefab.third_party.prefab_red_logging import (
    get_red_logging_console_handler,
    get_red_logging_formatter,
    get_red_logging_logger,
)
from .types import (
    HANDLER_CLASSES_TYPE,
    HANDLER_CLASSES_TYPE_ANNOTATION,
    LOGGING_CONFIG_DICT_TYPE,
    LOGGING_CONFIG_DICT_TYPE_ANNOTATION,
)
