from dataclasses import dataclass as _dataclass

from colex import (
    ColorValue as _ColorValue,
    GRAY as _DEFAULT_TEXT_COLOR,
    WHITE as _DEFAULT_HIGHLIGHT_COLOR,
    WHITE as _DEFAULT_INDENT_COLOR,
    MEDIUM_ORCHID as _DEFAULT_LABEL_COLOR
)


@_dataclass(kw_only=True)
class Style:
    label: _ColorValue = _DEFAULT_LABEL_COLOR
    text: _ColorValue = _DEFAULT_TEXT_COLOR
    highlight: _ColorValue = _DEFAULT_HIGHLIGHT_COLOR
    indent: _ColorValue = _DEFAULT_INDENT_COLOR
