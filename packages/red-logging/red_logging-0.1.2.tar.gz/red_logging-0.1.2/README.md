# red-log

Helpful classes, functions, & utilities for the stdlib `logging` module. No external dependencies.

## Project Links

| Site         | URL                                                                 |
| ------------ | ------------------------------------------------------------------- |
| 🏠 Repository | [Github: redjax/red-logging](https://github.com/redjax/red-logging) |
| 📚 Docs       | [ReadTheDocs](https://red-logging.readthedocs.io/en/stable/)        |
| 🐍 Pypi       | [projects/red-logging](https://pypi.org/project/red-logging)        |

## Why?

I wanted to learn the stdlib `logging` module, and found I liked configuring my logger(s) with `logging.config.dictConfig()`. However, I did not want to have to continually check reference pages, copy/paste code, and do all the logging setup by hand each time.

`red-log` does not import any 3rd party modules, only Python's stdlib modules are used. This package does not necessarily aim to simplify configuring logging, but the [config classes](https://github.com/redjax/red-logging/tree/main/src/red_logging/config_classes) help by exposing configuration options for the `logging` module's formatters, handlers, and loggers.

## Logger Configuration

### With dictConfig()

Base config dict:

```python
{
    "version": 1,
    "disable_existing_loggers": False,
    "propagate": True,
    "root": {},
    "formatters": {},
    "handlers": {},
    "loggers": {}
}
```

```python
from logging.config import dictConfig

logging_configdict: dict = {
    "version": 1,
    "disable_existing_loggers": false,
    "propagate": true,
    "root": {
        "": {
            "handlers": [
                "console"
            ],
            "level": "NOTSET"
        }
    },
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] > [%(filename)s:%(lineno)d] [%(funcName)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "": {
            "handlers": [
                "console"
            ],
            "level": "NOTSET"
        }
    }
}

dictConfig(logging_configdict)
log = logging.getLogger(__name__)

log.info("Logger configured")

```

## Links

- [python-guide.org: Logging in a library](https://docs.python-guide.org/writing/logging/#logging-in-a-library)
- [docs.python.org: Configuring logging for a library](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library)
- [RealPython: Logging in Python](https://realpython.com/python-logging/)
- [dev.to: Using the logger class in Python](https://dev.to/luca1iu/using-the-logger-class-in-python-for-effective-logging-4ghc)
- [machinelearningplus.com: Python logging guide](https://www.machinelearningplus.com/python/python-logging-guide/)
- [askpython.com: Configure logging in Python](https://www.askpython.com/python-modules/configure-logging-in-python)
- [betterprogramming.pub: How to implement logging in your Python application](https://betterprogramming.pub/how-to-implement-logging-in-your-python-application-1730315003c4)
- [Medium.com: Create a reusable logger factory](https://medium.com/geekculture/create-a-reusable-logger-factory-for-python-projects-419ad408665d)