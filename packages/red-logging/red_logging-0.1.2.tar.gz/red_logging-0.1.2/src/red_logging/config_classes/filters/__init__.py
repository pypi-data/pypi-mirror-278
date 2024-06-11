"""Apply filters to handlers to control the types of log messages displayed by the logger.

When using a dictConfig, you only need to reference these filters by name, i.e. `filters=["info_filter", "debug_filter", ...]`, but you
do need to import the filter function into whatever script runs the `logging.config.dictConfig()` function.
"""

from __future__ import annotations

from . import loglevel_filters
from .loglevel_filters import (
    critical_filter,
    debug_filter,
    error_filter,
    info_filter,
    warning_filter,
)
