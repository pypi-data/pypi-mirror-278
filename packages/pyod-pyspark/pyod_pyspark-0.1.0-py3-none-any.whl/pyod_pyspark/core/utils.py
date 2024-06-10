from typing import Any, Union, Iterable

from pyspark.sql import functions as F
from pyspark.sql.column import Column


# def get_pyspark_function(function: str) -> Column:
#     """Retrieve PySpark function by name

#     >>> get_pyspark_function("col")

#     """
#     func = getattr(F, function)
#     return func.__name__


# SINGLE DISPATCH
def coerce_to_list(obj: Iterable = None, str_delim: str = ",") -> list[Any]:
    """Convert object into a list of object's contents

    >>> coerce_to_list(obj="elem, elem, elem, elem")
    ['elem', 'elem', 'elem', 'elem']
    >>> coerce_to_list(obj="elem, elem, elem, elem", str_delim=" ")
    ['elem,', 'elem,', 'elem,', 'elem']
    >>> coerce_to_list(obj="random string", str_delim=" ")
    ['random', 'string']
    >>> coerce_to_list(obj=["random string"], str_delim=" ")
    ['random string']
    """
    if obj is None:
        raise ValueError("`object` is None - must be iterable object.")
    if not isinstance(obj, Iterable):
        raise ValueError("`object` is not iterable - must be iterable object.")
    if isinstance(obj, str):
        obj_list = obj.split(str_delim)
        return [o.strip() for o in obj_list]
    return obj


def log_iterable_as_string(obj: Iterable):
    def format_element(elem: Any) -> str:
        return f"'{elem}'"

    def join_elements(obj: Iterable):
        return ", ".join(map(format_element, obj))

    return join_elements(obj)
