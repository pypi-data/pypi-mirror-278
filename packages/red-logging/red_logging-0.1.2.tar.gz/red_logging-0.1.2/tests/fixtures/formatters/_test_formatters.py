from __future__ import annotations

import logging
import logging.handlers

from pytest import fixture
import red_logging

@fixture
def default_formatter_class() -> red_logging.config_classes.FormatterConfig:
    _formatter: red_logging.config_classes.FormatterConfig = (
        red_logging.config_classes.FormatterConfig(name="test_default")
    )

    return _formatter


@fixture
def default_formatter_dict() -> dict:
    _formatter: red_logging.config_classes.FormatterConfig = (
        red_logging.config_classes.FormatterConfig(name="test_default")
    )

    return _formatter.get_configdict()
