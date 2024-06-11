from __future__ import annotations

import logging
import logging.config
import logging.handlers

from pytest import mark
import red_logging

log = logging.getLogger("tests.test_suites.validation_tests.expect_pass")


@mark.validation
def test_return_valid_formatter_class(
    default_formatter_class: red_logging.config_classes.FormatterConfig,
):
    log.debug(f"[FIXTURE: default_formatter_class] ({type(default_formatter_class)})")

    assert default_formatter_class, ValueError(
        "Formatter class should not have been None"
    )


@mark.validation
def test_return_valid_formatter_dict(default_formatter_dict: dict):
    log.debug(f"[FIXTURE: default_formatter_dict] ({type(default_formatter_dict)})")

    assert default_formatter_dict, ValueError(
        "Formatter dict should not have been None"
    )


@mark.validation
def test_valid_formatter_class(
    default_formatter_class: red_logging.config_classes.FormatterConfig,
):
    log.debug(f"[FIXTURE: default_formatter_class] ({type(default_formatter_class)})")

    assert default_formatter_class, ValueError(
        "Formatter class should not have been None"
    )
    assert isinstance(
        default_formatter_class, red_logging.config_classes.FormatterConfig
    ), TypeError(
        f"Formatter class should have been of type red_utils.config_classes.FormatterConfig. Got type: ({type(default_formatter_class)})"
    )


@mark.validation
def test_valid_formatter_dict(default_formatter_dict: dict):
    log.debug(f"[FIXTURE: default_formatter_dict] ({type(default_formatter_dict)})")

    assert default_formatter_dict, ValueError(
        "Formatter dict should not have been None"
    )
    assert isinstance(default_formatter_dict, dict), TypeError(
        f"Formatter dict should have been of type dict. Got type: ({type(default_formatter_dict)})"
    )
