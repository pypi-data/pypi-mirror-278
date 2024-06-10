import functools

from pyod_pyspark.core.utils import coerce_to_list, log_iterable_as_string


def process_columns(func):
    """Decorator for processing functions that require a `columns` parameter"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args = list(args)
        data = args.pop(0) if args else kwargs.pop("data")
        columns = args.pop(0) if args else kwargs.pop("columns")
        columns = coerce_to_list(obj=columns)
        return func(data=data, columns=columns, *args, **kwargs)

    return wrapper


def validate_columns(func):
    """Decorator for validating functions that require a `columns` parameter"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args = list(args)
        data = args.pop(0) if args else kwargs.get("data")
        columns = args.pop(0) if args else kwargs.get("columns")
        invalid_columns = set(columns).difference(data.columns)
        assert (
            invalid_columns == set()
        ), f"The following columns are invalid: {log_iterable_as_string(obj=invalid_columns)}"
        return func(*args, **kwargs)

    return wrapper
