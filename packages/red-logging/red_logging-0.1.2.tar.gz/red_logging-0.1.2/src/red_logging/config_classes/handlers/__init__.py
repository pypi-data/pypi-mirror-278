"""Handlers for a logging dictConfig.

Handlers define what to do with log messages as they are created.
"""

from __future__ import annotations

from ._handlers import (
    FileHandlerConfig,
    QueueHandlerConfig,
    QueueListenerConfig,
    RotatingFileHandlerConfig,
    SMTPHandlerConfig,
    SocketHandlerConfig,
    StreamHandlerConfig,
    TimedRotatingFileHandlerConfig,
)
