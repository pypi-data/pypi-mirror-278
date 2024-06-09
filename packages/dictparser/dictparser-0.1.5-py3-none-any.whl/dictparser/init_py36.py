from .engine import process_class as _process_class


def dictparser(cls=None, *, kw_only=False):
    def wrap(cls):
        return _process_class(cls, kw_only)

    if cls is None:
        return wrap

    return wrap(cls)
