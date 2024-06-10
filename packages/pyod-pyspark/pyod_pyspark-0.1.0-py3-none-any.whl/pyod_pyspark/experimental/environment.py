from typing import Callable


def bucket_local_vars(_locals: dict):
    """Categorize locals dictionary by constants, kwargs, and callables.

    >>> def f(): pass
    >>> _locals = {
    ...     'a': 1,
    ...     'b': 2,
    ...     'kwargs': {'d': 4, 'e': 5},
    ...     'c': 3,
    ...     'f': f,
    ...     'g': lambda x: x
    ... }
    >>> locals, kwargs, callables = bucket_local_vars(_locals=_locals)
    >>> locals
    {'a': 1, 'b': 2, 'c': 3}
    >>> kwargs
    {'d': 4, 'e': 5}
    >>> callables # doctest: +ELLIPSIS
    {'f': <function f at ...>, 'g': <function <lambda> at ...>}
    >>> all(isinstance(f, Callable) for f in callables.values())
    True
    """
    ### extract, remove keyword arguments from local scope
    _kwargs = _locals.get("kwargs")
    del _locals["kwargs"]

    ### extract, remove callables from local scope
    _callables = {k: v for k, v in _locals.items() if isinstance(v, Callable)}
    for callable in _callables:
        del _locals[callable]

    ### return groups of objects
    return _locals, _kwargs, _callables
