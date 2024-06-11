"""Define loggers for a logging dictConfig."""

from __future__ import annotations

from dataclasses import dataclass
import typing as t

from red_logging.config_classes.base import BaseLoggingConfig

@dataclass
class LoggerConfig(BaseLoggingConfig):
    """Define a logging Logger.

    Params:
        name (str): The name of the logger.
        level (str): The level of log messages this logger should show (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL).
        handlers (list[str]): List of handler names this logger should use. These handlers must exist in the logging dictConfig.
        propagate (bool): If `True`, messages will be propagated up/down to the root logger.
    """

    name: str
    level: str
    handlers: list[str]
    propagate: bool = False

    def get_configdict(self) -> dict:
        """Return a dict representation of the logger described by this class."""
        logger_dict: dict[str, dict[str, t.Any]] = {
            self.name: {
                "level": self.level,
                "handlers": self.handlers,
                "propagate": self.propagate,
            }
        }
        return logger_dict
