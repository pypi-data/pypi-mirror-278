from dataclasses import dataclass as _dataclass

from colex import (
    ColorValue as _ColorValue,
    # default colors
    SEA_GREEN as _DEFAULT_INFO_COLOR,
    ORANGE as _DEFAULT_WARN_COLOR,
    CRIMSON as _DEFAULT_ERROR_COLOR,
    GRAY as _DEFAULT_TEXT_COLOR,
    WHITE as _DEFAULT_HIGHLIGHT_COLOR,
    WHITE as _DEFAULT_INDENT_COLOR,
    MEDIUM_ORCHID as _DEFAULT_LABEL_COLOR
)


@_dataclass
class Theme:
    info: _ColorValue = _DEFAULT_INFO_COLOR
    warn: _ColorValue = _DEFAULT_WARN_COLOR
    error: _ColorValue = _DEFAULT_ERROR_COLOR
    text: _ColorValue = _DEFAULT_TEXT_COLOR
    highlight: _ColorValue = _DEFAULT_HIGHLIGHT_COLOR
    indent: _ColorValue = _DEFAULT_INDENT_COLOR
    default_label: _ColorValue = _DEFAULT_LABEL_COLOR

    def get_color(
        self,
        field_name: str,
        default: _ColorValue | None = None
    ) -> _ColorValue:
        return getattr(self, field_name, default or "") # "" means no color


theme: Theme = Theme() # global theme


def set_theme(new_theme: Theme) -> None:
    """Sets the global theme

    Args:
        new_theme (Theme): new global theme
    """
    global theme
    theme = new_theme


def get_theme() -> Theme:
    """Returns a unique copy of the global theme

    Returns:
        Theme: unique copy of current global theme
    """
    return Theme(
        info=theme.info,
        warn=theme.warn,
        error=theme.error,
        text=theme.text,
        highlight=theme.highlight
    )
