"""Types and annotations for my customer logging config objects."""

from __future__ import annotations

import typing as t

from .handlers import (
    FileHandlerConfig,
    QueueHandlerConfig,
    QueueListenerConfig,
    RotatingFileHandlerConfig,
    SocketHandlerConfig,
    StreamHandlerConfig,
    TimedRotatingFileHandlerConfig,
)

HANDLER_CLASSES_TYPE = t.Union[
    FileHandlerConfig,
    RotatingFileHandlerConfig,
    TimedRotatingFileHandlerConfig,
    StreamHandlerConfig,
    SocketHandlerConfig,
    QueueHandlerConfig,
    QueueListenerConfig,
]
HANDLER_CLASSES_TYPE_ANNOTATION = t.Annotated[
    HANDLER_CLASSES_TYPE,
    "A logging handler config class.",
]
LOGGING_CONFIG_DICT_TYPE = dict[str, dict[str, t.Any]]
LOGGING_CONFIG_DICT_TYPE_ANNOTATION = t.Annotated[
    LOGGING_CONFIG_DICT_TYPE, "A logging dictConfig-compatible dict."
]
