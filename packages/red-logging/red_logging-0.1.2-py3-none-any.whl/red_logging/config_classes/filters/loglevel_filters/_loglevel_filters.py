"""Filter functions that can be referenced by function name in a logging dictConfig to apply filtering to a handler.

For example, to only show DEBUG level messages, you could add `filters=["debug_filter"]` to a logging dictConfig.

When adding these methods to a config, you must import the function into the same script where `logging.config.dictConfig()` is executed.
"""

from __future__ import annotations

import logging

def debug_filter(record: logging.LogRecord) -> bool:
    """Filter to only show DEBUG and above."""
    return record.levelno >= logging.DEBUG


def info_filter(record: logging.LogRecord) -> bool:
    """Filter to only show INFO and above."""
    return record.levelno >= logging.INFO


def warning_filter(record: logging.LogRecord) -> bool:
    """Filter to only show WARNING and above."""
    return record.levelno >= logging.WARNING


def error_filter(record: logging.LogRecord) -> bool:
    """Filter to only show ERROR and above."""
    return record.levelno >= logging.ERROR


def critical_filter(record: logging.LogRecord) -> bool:
    """Filter to only show CRITICAL and above."""
    return record.levelno >= logging.CRITICAL
