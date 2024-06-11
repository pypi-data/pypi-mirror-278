"""Define formatters, handlers, and loggers for third-party dependencies."""

from __future__ import annotations

from . import prefab_red_logging
from .prefab_red_logging import (
    get_red_logging_console_handler,
    get_red_logging_formatter,
    get_red_logging_logger,
)
