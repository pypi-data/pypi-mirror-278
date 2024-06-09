"""
Actus
-----

A logging library for python development

Includes:
- `info`
- `warn`
- `error`
- `LogSection`
- `Theme`
- `set_theme`
- `get_theme`
"""

__version__ = "0.3.0"
__all__ = [
    "info",
    "warn",
    "error",
    "LogSection",
    "Theme",
    "set_theme",
    "get_theme"
]

from ._log_section import LogSection
from ._theme import Theme, set_theme, get_theme


info = LogSection("Info", theme_key="info")
warn = LogSection("Warning", theme_key="warn")
error = LogSection("Error", theme_key="error")
