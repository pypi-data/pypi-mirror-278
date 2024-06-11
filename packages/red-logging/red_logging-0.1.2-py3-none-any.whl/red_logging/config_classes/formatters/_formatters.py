"""Use these classes to instantiate logging formatters for a logging dictConfig.

Each class has a `.get_configdict()` method, which returns a dict representation of the class
that can be added to a logging config dict.
"""

from __future__ import annotations

from dataclasses import dataclass

from red_logging.config_classes.base import BaseLoggingConfig
from red_logging.fmts._formats import (
    DATE_FMT_DATE_ONLY,
    DATE_FMT_STANDARD,
    DATE_FMT_TIME_ONLY,
    MESSAGE_FMT_BASIC,
    MESSAGE_FMT_DETAILED,
    MESSAGE_FMT_STANDARD,
    red_logging_DETAIL_FMT,
    red_logging_FMT,
)

@dataclass
class FormatterConfig(BaseLoggingConfig):
    """Define a logging formatter.

    Params:
        name (str): The name of the formatter.
        fmt (str): The string formatting to use for log messages.
        datefmt (str): The string formatting to use for log message timestamps.
        style (str): The string substitution style to use for log formats. Default is `%`, which
            means formats need to be written like `%(asctime)s %(levelname)s %(message)s`. If
            you change this style, make sure the `fmt` you pass uses the correct formatting style.
        validate (bool): When `True`, the configuration dict this formatter returns will be validated by the logging module.

    """

    name: str = None
    fmt: str = MESSAGE_FMT_STANDARD
    datefmt: str = DATE_FMT_STANDARD
    style: str = "%"
    validate: bool = True

    def get_configdict(self) -> dict[str, dict[str, str]]:
        """Return a dict representation of the formatter described by this class."""
        formatter_dict: dict[str, dict[str, str]] = {self.name: {"format": self.fmt}}
        if self.datefmt:
            formatter_dict[self.name]["datefmt"] = self.datefmt
        if self.style:
            formatter_dict[self.name]["style"] = self.style
        formatter_dict[self.name]["validate"] = self.validate

        return formatter_dict
