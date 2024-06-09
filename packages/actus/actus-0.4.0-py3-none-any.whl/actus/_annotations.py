from typing import TypeVar as _TypeVar, Protocol as _Protocol


_T_contra = _TypeVar("_T_contra", contravariant=True)


class FileLike(_Protocol[_T_contra]):
    def write(self, stream: _T_contra, /) -> object: ...
    def flush(self, /) -> None: ...
