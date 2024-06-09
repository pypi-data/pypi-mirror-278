import sys as _sys
from traceback import TracebackException as _TracebackException

from ._highlighting import highlight as _highlight
from ._theme import theme as _theme
from ._annotations import FileLike as _FileLike

import colex as _colex


class LogSection:
    def __init__(
        self,
        label: str,
        /,
        *,
        fd: _FileLike[str] | None = None,
        theme_key: str = "default_label",
        left_deco: str = "[",
        right_deco: str = "]",
        indent_size: int = 2,
        indent_filler: str = " ",
        indent_deco: str = " ",
        indent_delimiter: str = " "
    ) -> None:
        self._label = label
        self._fallback_fd: _FileLike[str] = fd or _sys.stdout
        self._theme_key = theme_key
        self._left_deco = left_deco
        self._right_deco = right_deco
        self._indent_size = indent_size
        self._indent_filler = indent_filler
        self._indent_deco = indent_deco
        self._indent_delimiter = indent_delimiter
        self._indent_level = 0
    
    def __enter__(self):
        self.indent()
        return self
    
    def __exit__(
        self,
        exc_type: type | None,
        exc_value: Exception | None,
        traceback: _TracebackException | None
    ) -> bool:
        self.dedent()
        return exc_type is None
    
    def indent(self, prefix: str | None = None, count: int = 1, /):
        self._indent_level += count
        if prefix is not None:
            self._indent_deco = prefix
        return self
    
    def dedent(self, count: int = 1, /):
        self._indent_level = min(0, self._indent_level - count)
        return self
    
    def dedent_all(self):
        self._indent_level = 0
        return self

    def set_theme_key(self, theme_key: str):
        self._theme_key = theme_key
        return self
    
    def set_left_deco(self, left_deco: str):
        self._left_deco = left_deco
        return self
        
    def set_right_deco(self, right_deco: str):
        self._right_deco = right_deco
        return self

    def set_indent_size(self, size: int):
        self._indent_size = size
        return self

    def set_indent_filler(self, filler: str):
        self._indent_filler = filler
        return self
    
    def set_indent_deco(self, deco: str):
        self._indent_deco = deco
        return self

    def set_indent_delimiter(self, delimiter: str):
        self._indent_delimiter = delimiter
        return self
    
    def __call__(
        self,
        *values: str,
        sep: str = " ",
        end: str = "\n",
        fd: _FileLike[str] | None = None,
        flush: bool = True
    ):
        body = _highlight(sep.join(values))
        if self._indent_level == 0:
            label_color = _theme.get_color(self._theme_key, _theme.default_label)
            header = self._left_deco + self._label + self._right_deco
            content = _colex.colorize(header, label_color) + " " + body
        else:
            indent_suffix = self._indent_deco + self._indent_delimiter
            indent_chars = self._indent_size * self._indent_level
            indentation = indent_suffix.rjust(indent_chars, self._indent_filler)
            content = _colex.colorize(indentation, _theme.indent) + body
        final_fd: _FileLike[str] = fd or self._fallback_fd
        final_fd.write(content + end)
        if flush:
            final_fd.flush()
        return self
