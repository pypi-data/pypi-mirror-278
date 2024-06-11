from __future__ import annotations

import logging

from .tests_logging import setup_tests_logging

setup_tests_logging()

log = logging.getLogger("tests")

log.info("Running validation tests, expect passes")

from .test_suites.validation_tests.expect_pass import (
    test_return_valid_formatter_class,
    test_return_valid_formatter_dict,
    test_valid_formatter_class,
    test_valid_formatter_dict,
)

log.info("Running validation tests, expect fails")
