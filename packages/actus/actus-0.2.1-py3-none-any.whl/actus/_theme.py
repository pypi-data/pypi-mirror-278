from dataclasses import dataclass as _dataclass

from colex import (
    ColorValue as _ColorValue,
    # default colors
    SEA_GREEN as _DEFAULT_INFO_COLOR,
    ORANGE as _DEFAULT_WARN_COLOR,
    CRIMSON as _DEFAULT_ERROR_COLOR,
    GRAY as _DEFAULT_TEXT_COLOR,
    WHITE as _DEFAULT_HIGHLIGHT_COLOR
)


@_dataclass
class Theme:
    info: _ColorValue = _DEFAULT_INFO_COLOR
    warn: _ColorValue = _DEFAULT_WARN_COLOR
    error: _ColorValue = _DEFAULT_ERROR_COLOR
    text: _ColorValue = _DEFAULT_TEXT_COLOR
    highlight: _ColorValue = _DEFAULT_HIGHLIGHT_COLOR
