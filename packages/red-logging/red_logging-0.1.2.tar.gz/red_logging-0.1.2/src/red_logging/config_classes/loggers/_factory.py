"""Class to simplify generating loggers."""

from __future__ import annotations

import logging
import logging.config

class LoggerFactory:
    """Generate loggers based on LoggerFactory's config."""

    _LOG: logging.Logger | None = None

    @staticmethod
    def __create_logger(
        name: str,
        log_level: str,
        handlers: dict[str, dict],
        formatters: dict[str, dict],
        loggers: dict[str, dict],
    ) -> logging.Logger:
        """Create a logger cnofig from inputs.

        Params:
            name (str): The name of the logger.
            log_level (str): The log levels to show (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL).
            handlers (dict[str, dict[str, Any]]): A dict describing the handlers for this logger config.
            formatters (dict[str, dict[str, Any]]): A dict describing the formatters for this logger config.
            loggers (dict[str, dict[str, Any]]): A dict describing the loggers for this logger config.
        """
        log_level = log_level.upper()

        # Configure logging using dictConfig
        logging_config = {
            "version": 1,
            "handlers": handlers,
            "formatters": formatters,
            "loggers": loggers,
            "root": {
                "level": log_level,
                "handlers": list(handlers.keys()),
            },
        }

        try:
            logging.config.dictConfig(logging_config)
        except Exception as exc:
            msg = Exception(f"Unhandled exception configuring logger. Details: {exc}")
            # log.error(msg)

            raise msg

        # Get or create logger
        LoggerFactory._LOG = logging.getLogger(name)

        return LoggerFactory._LOG

    @staticmethod
    def get_logger(
        name: str,
        log_level: str,
        handlers: dict[str, dict],
        formatters: dict[str, dict],
        loggers: dict[str, dict],
    ) -> logging.Logger:
        """Initialize a logger.

        Params:
            name (str): The name of the logger.
            log_level (str): The log levels to show (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL).
            handlers (dict[str, dict[str, Any]]): A dict describing the handlers for this logger config.
            formatters (dict[str, dict[str, Any]]): A dict describing the formatters for this logger config.
            loggers (dict[str, dict[str, Any]]): A dict describing the loggers for this logger config.
        """
        logger = LoggerFactory.__create_logger(
            name=name,
            log_level=log_level,
            handlers=handlers,
            formatters=formatters,
            loggers=loggers,
        )

        return logger
