"""
Copyright (c) 2022 Luke Kreczko. All rights reserved.

fasthep-logging: Enhanced logging for the FAST-HEP toolkit
"""


from __future__ import annotations

from ._logging import DEFAULT_LOG_LEVEL, TIMING, TRACE, get_logger, getLogger
from ._version import version as __version__

__all__ = (
    "__version__",
    "getLogger",
    "get_logger",
    "DEFAULT_LOG_LEVEL",
    "TIMING",
    "TRACE",
)
