"""Abstract base classes for logging object classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import typing as t

@dataclass
class BaseLoggingConfig(ABC):
    """Abstract base class for a full logging config dict."""

    @abstractmethod
    def get_configdict(self) -> None:
        pass


@dataclass
class BaseHandlerConfig(BaseLoggingConfig):
    """Abstract base class for a logging handler dict.

    Params:
        name (str): The handler's name.
        level (str): The handler's logging level (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL).
        formatter (str): The name of a formatter that exists in the logging config.
        filters (list[str] | None): The names of logging filter methods/classes. These methods/classes
            must be imported into the script where `logging.config.dictConfig()` is run.
    """

    name: str = None
    level: str = "NOTSET"
    formatter: str = None
    filters: list[str] | None = field(default=None)

    @abstractmethod
    def get_configdict(self) -> None:
        """Return a dict representation of the handler config."""
        handler_dict: dict[str, dict[str, t.Any]] = {
            self.name: {
                "class": self.get_handler_class(),
                "level": self.level,
                "formatter": self.formatter,
            }
        }
        if self.filters:
            handler_dict[self.name]["filters"] = self.filters
        return handler_dict

    def get_handler_class(self) -> str:
        """Return the logging handler's class name."""
        raise NotImplementedError("Subclasses must implement get_handler_class method")
