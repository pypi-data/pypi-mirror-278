"""Stores a base logging config dict in `BASE_LOGGING_CONFIG_DICT`.

This can be imported and updated to create a valid logging dictConfig.

```python title="Base logging config dict" linenums="1"
BASE_LOGGING_CONFIG_DICT: dict[str, t.Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "propagate": True,
    "root": {},
    "formatters": {},
    "handlers": {},
    "loggers": {},
}
```
"""

from __future__ import annotations

import typing as t

BASE_LOGGING_CONFIG_DICT: dict[str, t.Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "propagate": True,
    "root": {},
    "formatters": {},
    "handlers": {},
    "loggers": {},
}
