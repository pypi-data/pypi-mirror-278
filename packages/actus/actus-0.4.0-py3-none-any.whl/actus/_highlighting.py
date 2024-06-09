import re as _re

from ._theme import theme as _theme

import colex as _colex


_BRACKET_CONTENT_PATTERN = _re.compile(r"\$\[([^]]+)\]")


def _replace_match(match: _re.Match[str]) -> str:
    return _theme.highlight + match.group(1) + _theme.text


def highlight(string: str) -> str:
    return (
        _theme.text
        + _BRACKET_CONTENT_PATTERN.sub(_replace_match, string)
        + _colex.RESET
    )
