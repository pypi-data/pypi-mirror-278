"""
Actus
-----

A logging library for python development

Includes:
- `info`
- `warn`
- `error`
- `Theme`
- `set_theme`
- `get_theme`
"""

__version__ = "0.2.0"
__all__ = [
    "info",
    "warn",
    "error",
    "Theme",
    "set_theme",
    "get_theme"
]

import sys as _sys
from string import Formatter as _Formatter

import colex as _colex

from ._theme import Theme
from ._annotations import (
    FileLike as _FileLike
)


def set_theme(new_theme: Theme) -> None:
    """Sets the global theme

    Args:
        new_theme (Theme): new global theme
    """
    global _theme
    _theme = new_theme

_theme: Theme = Theme() # global theme

def get_theme() -> Theme: # 
    """Returns a unique copy of the global theme

    Returns:
        Theme: unique copy of current global theme
    """
    return Theme(
        info=_theme.info,
        warn=_theme.warn,
        error=_theme.error
    )


def _highlight(string: str) -> str:
    colored = _colex.colorize(string, _theme.text)
    keys = [
        result[1]
        for result in _Formatter().parse(string)
        if result[1]
    ]
    highlighted_values = [
        _theme.highlight + key + _theme.text
        for key in keys
    ]
    pairs = dict(zip(keys, highlighted_values))
    highlighted = colored.format_map(pairs)
    return highlighted


def info(
    *values: str,
    sep: str = " ",
    end: str = "\n",
    file: _FileLike[str] | None = None,
    flush: bool = True
) -> None:
    message = (
        _colex.colorize("[Info]", _theme.info)
        + " "
        + _highlight(sep.join(values))
        + end
    )
    if file is not None:
        file.write(message)
        if flush:
            file.flush()
    _sys.stdout.write(message)
    if flush:
        _sys.stdout.flush()


def warn(
    *values: str,
    sep: str = " ",
    end: str = "\n",
    file: _FileLike[str] | None = None,
    flush: bool = True
) -> None:
    message = (
        _colex.colorize("[Warning]", _theme.warn)
        + " "
        + _highlight(sep.join(values))
        + end
    )
    if file is not None:
        file.write(message)
        if flush:
            file.flush()
    _sys.stdout.write(message)
    if flush:
        _sys.stdout.flush()


def error(
    *values: str,
    sep: str = " ",
    end: str = "\n",
    file: _FileLike[str] | None = None,
    flush: bool = True
) -> None:
    message = (
        _colex.colorize("[Error]", _theme.error)
        + " "
        + _highlight(sep.join(values))
        + end
    )
    if file is not None:
        file.write(message)
        if flush:
            file.flush()
    _sys.stdout.write(message)
    if flush:
        _sys.stdout.flush()
