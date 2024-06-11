"""Use these classes to instantiate logging handlers for a logging dictConfig.

Each class has a `.get_configdict()` method, which returns a dict representation of the class
that can be added to a logging config dict.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from queue import Queue
import typing as t

from red_logging.config_classes.base import (
    BaseHandlerConfig,
    BaseLoggingConfig,
)

@dataclass
class StreamHandlerConfig(BaseHandlerConfig):
    """Define a logging StreamHandler.

    Params:
        stream (Any): The stream this handler controls, i.e. `ext://sys.stdout`, `ext://sys.stderr`, etc.
    """

    level: str = "DEBUG"
    stream: t.Any | None = "ext://sys.stdout"

    def get_configdict(self) -> dict[str, dict[str, str]]:
        """Return a dict representation of the handler described by this class."""
        handler_dict: dict[str, dict[str, str]] = {
            self.name: {
                "class": self.get_handler_class(),
                "level": self.level,
                "formatter": self.formatter,
                "stream": self.stream,
            }
        }
        if self.filters:
            handler_dict["filters"] = self.filters
        return handler_dict

    def get_handler_class(self) -> str:
        """Return the logging handler class this class represents.

        Returns:
            (str): `logging.StreamHandler`.

        """
        return "logging.StreamHandler"


@dataclass
class FileHandlerConfig(BaseHandlerConfig):
    """Define a logging FileHandler.

    Params:
        filename (str): The name of the file to log messages to.
    """

    filename: str | None = field(default="app.log")

    def get_configdict(self) -> dict[str, dict[str, str]]:
        """Return a dict representation of the handler described by this class."""
        handler_dict: dict[str, dict[str, str]] = {
            self.name: {
                "class": self.get_handler_class(),
                "level": self.level,
                "formatter": self.formatter,
                "filename": self.filename,
            }
        }
        return handler_dict

    def get_handler_class(self) -> str:
        """Return the logging handler class this class represents.

        Returns:
            (str): `logging.FileHandler`.

        """
        return "logging.FileHandler"


@dataclass
class RotatingFileHandlerConfig(BaseHandlerConfig):
    """Define a logging RotatingFileHandler.

    Params:
        filename (str | None): The name/path of the file to log messages to.
        maxBytes (int): The maximum size of the file (in bytes) before a new file is rotated.
        backupCount (int): Number of rotated log files to keep.

    """

    filename: str | None = field(default="app.log")
    maxBytes: int = 0
    backupCount: int = 0

    def get_configdict(self) -> dict[str, dict[str, t.Any]]:
        """Return a dict representation of the handler described by this class."""
        handler_dict: dict[str, dict[str, t.Any]] = {
            self.name: {
                "class": self.get_handler_class(),
                "level": self.level,
                "formatter": self.formatter,
                "filename": f"{self.filename}",
                "maxBytes": self.maxBytes,
                "backupCount": self.backupCount,
            }
        }
        return handler_dict

    def get_handler_class(self) -> str:
        """Return the logging handler class this class represents.

        Returns:
            (str): `logging.RotatingFileHandler`.

        """
        return "logging.handlers.RotatingFileHandler"


@dataclass
class TimedRotatingFileHandlerConfig(BaseHandlerConfig):
    """Define a logging TimedRotatingFileHandler.

    Params:
        filename (str): The name/path of the file to log messages to.
        when (str): Time of day to rotate log files, i.e. `midnight`.
        interval (int): When to rotate the file as the interval defined in `when` occurs.
            `1=every occurrence`, `2=every other occurrence`, etc.
        backupCount (int): The number of rotated log files to save.
    """

    filename: str | None = field(default="app.log")
    when: str | None = field(default="midnight")
    interval: int = 1
    backupCount: int = 0

    def get_configdict(self) -> dict[str, dict[str, t.Any]]:
        """Return a dict representation of the handler described by this class."""
        handler_dict: dict[str, dict[str, t.Any]] = {
            self.name: {
                "class": self.get_handler_class(),
                "level": self.level,
                "formatter": self.formatter,
                "filename": self.filename,
                "when": self.when,
                "interval": self.interval,
                "backupCount": self.backupCount,
            }
        }
        return handler_dict

    def get_handler_class(self) -> str:
        """Return the logging handler class this class represents.

        Returns:
            (str): `logging.handlers.TimedRotatingFileHandler`.

        """
        return "logging.handlers.TimedRotatingFileHandler"


@dataclass
class SocketHandlerConfig(BaseHandlerConfig):
    """Define a logging SocketHandler.

    Params:
        host (str): Host IP/FQDN.
        port (int): Host port where log messages should be sent.
    """

    host: str = "localhost"
    port: int = 0

    def get_configdict(self) -> dict[str, dict[str, t.Any]]:
        """Return a dict representation of the handler described by this class."""
        handler_dict: dict[str, dict[str, t.Any]] = {
            self.name: {
                "class": self.get_handler_class(),
                "level": self.level,
                "formatter": self.formatter,
                "host": self.host,
                "port": self.port,
            }
        }
        return handler_dict

    def get_handler_class(self) -> str:
        """Return the logging handler class this class represents.

        Returns:
            (str): `logging.handlers.SocketHandler`.

        """
        return "logging.handlers.SocketHandler"


@dataclass
class SMTPHandlerConfig(BaseHandlerConfig):
    """Define a logging SMTPHandler.

    Params:
        mailhost (Any): ...
        fromaddr (str): ...
        toaddrs (list): ...
        subject (str): ...
        credentials (tuple): ...
        secure (tuple): ...
    """

    mailhost: t.Any = None
    fromaddr: str = "from@example.com"
    toaddrs: list = field(default_factory=lambda: [])
    subject: str = "SMTPHandler Log Event"
    credentials: tuple | None = None
    secure: tuple | None = None

    def get_configdict(self):
        """Return a dict representation of the handler described by this class."""
        handler_dict = {
            self.name: {
                "class": self.get_handler_class(),
                "level": self.level,
                "formatter": self.formatter,
                "mailhost": self.mailhost,
                "fromaddr": self.fromaddr,
                "toaddrs": self.toaddrs,
                "subject": self.subject,
            }
        }
        if self.credentials:
            handler_dict[self.name]["credentials"] = self.credentials
        if self.secure:
            handler_dict[self.name]["secure"] = self.secure
        return handler_dict

    def get_handler_class(self) -> str:
        """Return the logging handler class this class represents.

        Returns:
            (str): `logging.handlers.SMTPHandler`.

        """
        return "logging.handlers.SMTPHandler"


@dataclass
class QueueHandlerConfig(BaseHandlerConfig):
    """Define a logging QueueHandler.

    Params:
        queue (queue.Queue): The queue to send log messages to.
    """

    queue: Queue = field(default=None)

    def get_configdict(self) -> dict[str, dict[str, t.Any]]:
        """Return a dict representation of the handler described by this class."""
        handler_dict: dict[str, dict[str, t.Any]] = {
            self.name: {
                "class": self.get_handler_class(),
                "level": self.level,
                "formatter": self.formatter,
                "queue": self.queue,
            }
        }
        return handler_dict

    def get_handler_class(self) -> str:
        """Return the logging handler class this class represents.

        Returns:
            (str): `logging.handlers.QueueHandler`.

        """
        return "logging.handlers.QueueHandler"


@dataclass
class QueueListenerConfig(BaseLoggingConfig):
    """Define a logging QueueListener.

    Params:
        name (str): The name of the handler.
        queue (queue.Queue): The queue to listen for log messages in.
        handlers (list[str]): List of handler names to apply to this listener.

    """

    name: str
    queue: Queue
    handlers: list

    def get_configdict(self) -> dict[str, dict[str, t.Any]]:
        """Return a dict representation of the handler described by this class."""
        listener_dict: dict[str, dict[str, t.Any]] = {
            self.name: {
                "class": self.get_handler_class(),
                "queue": self.queue,
                "handlers": self.handlers,
            }
        }
        return listener_dict

    def get_handler_class(self) -> str:
        """Return the logging handler class this class represents.

        Returns:
            (str): `logging.handlers.QueueListener`.

        """
        return "logging.handleres.QueueListener"
