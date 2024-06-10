from typing import Any, Union, Iterable

import operator
import functools
import itertools

import pyspark

# from pyspark.sql import functions as F
from pyspark.sql import types
from pyspark.sql.column import Column

from pyod.core.decorators import validate_columns, process_columns
# from pyod.core.utils import get_function


def function_multiplication(func: callable, args: list):
    return itertools.product(func, args)


@process_columns
@validate_columns
def summarize_data(
    data: pyspark.sql.DataFrame,
    columns: Union[str, list[str]] = None,
    groups: Union[str, list[str]] = None,
    agg_func: Union[str, list[str]] = ["count", "count_distinct"],
    dtype: str = None,
) -> Column:
    """Generic summary function"""
    # if groups is not None:
    #     data = data.groupBy(groups)

    # agg_func = map(get_function, agg_func)
    # queue = map(lambda queue: queue[0](queue[1]), itertools.product(agg_func, columns))
    queue = map(
        lambda queue: f"{queue[0]}({queue[1]})", itertools.product(agg_func, columns)
    )

    return queue

    # if dtype is None:
    #     summarize_generic()


@process_columns
@validate_columns
def summarize_generic(data: pyspark.sql.DataFrame, queue: Iterable):
    pass


@process_columns
@validate_columns
def summarize_character(data: pyspark.sql.DataFrame, queue: Iterable):
    pass


@process_columns
@validate_columns
def summarize_numeric(data: pyspark.sql.DataFrame, queue: Iterable):
    pass


@process_columns
@validate_columns
def summarize_datetime(data: pyspark.sql.DataFrame, queue: Iterable):
    pass
