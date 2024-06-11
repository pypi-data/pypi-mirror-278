"""Define filter classes for logging configs."""

from __future__ import annotations

from dataclasses import dataclass
import logging

from red_logging.config_classes.base import BaseLoggingConfig

@dataclass
class FilterConfig(BaseLoggingConfig):
    """Define a logging filter.

    Params:
        name (str): A name for the filter, which can be added to a dictConfig's `filters` param.
        func (callable): The filter function to use when this class is called by a handler.
    """

    name: str
    func: callable

    def get_filter(self) -> logging.Filter:
        filter_obj = logging.Filter(name=self.name)
        filter_obj.filter = self.func
        return filter_obj
