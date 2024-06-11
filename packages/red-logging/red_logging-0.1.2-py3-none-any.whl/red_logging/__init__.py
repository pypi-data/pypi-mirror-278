"""Classes and utilities to help configure the stdlib `logging` library for Python.

Configurations (formatters, handlers, loggers, filters) can be created as classes, which
can be compiled down to `logging.config.dictConfig`-compatible dicts using each class's
`.get_dictconfig()` method, or by passing multiple initialized configuration classes to the
`assemble_configdict()` method.
"""

from __future__ import annotations

from . import config_classes, fmts, helpers
from .__base import BASE_LOGGING_CONFIG_DICT
from .helpers import (
    assemble_configdict,
    get_formatter_config,
    get_logger_config,
    get_rotatingfilehandler_config,
    get_streamhandler_config,
)
