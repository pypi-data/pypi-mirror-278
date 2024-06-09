import sys
import typing

from .engine import process_class as _process_class

if sys.version_info >= (3, 11):
    @typing.dataclass_transform()
    def dictparser(cls=None, *, kw_only=False):
        def wrap(cls):
            return _process_class(cls, kw_only)

        if cls is None:
            return wrap

        return wrap(cls)
else:
    def dictparser(cls=None, *, kw_only=False):
        def wrap(cls):
            return _process_class(cls, kw_only)

        if cls is None:
            return wrap

        return wrap(cls)
