from typing import Any, Union, Iterable

import operator
import functools

import pyspark
from pyspark.sql import functions as F
from pyspark.sql import types
from pyspark.sql.column import Column

from pyod.core.decorators import validate_columns, process_columns
from pyod.core.queries import query_nulls, query_range


def structure_filter(
    query: callable, *args, columns: list[str], strict: bool
) -> Column:
    """Compose filtering function given list of functions"""
    comp_op = operator.and_ if strict else operator.or_
    query_map = map(lambda c: query(c, *args), columns)
    return functools.reduce(lambda x, y: comp_op(x, y), query_map)


@process_columns
@validate_columns
def filter_nulls(
    data: pyspark.sql.DataFrame, columns: Union[str, list[str]], strict: bool = False
) -> Column:
    """Function composition for filtering multiple columns by null values

    Considerably reduces two errors that arise when filtering null values on
    multiple columns:
        - user does not structure the query's logic "correctly"
        - user does not include empty values in filter

    Additionally, reduces the amount of code needed to perform a repetitive
    procedure like filtering on multiple columns.

    Example
    =======
    # without function composition
    # >>> data.filter((F.col('var1').isNull() | F.col('var1').rlike("^\s*$")) & ... & (F.col('varN').isNull() | F.col('varN').rlike("^\s*$")))
    # with function composition
    # >>> filter_nulls(data, columns=['var1', ..., 'varN'])
    """
    query_expression = structure_filter(query_nulls, columns=columns, strict=strict)
    return data.filter(condition=~query_expression)


@process_columns
@validate_columns
def filter_boundaries(
    data: pyspark.sql.DataFrame,
    columns: Union[str, list[str]],
    boundaries: Iterable,
    interval: str = "closed",
    strict: bool = False,
):
    # ensure columns are of same type; else cannot infer how to apply range
    #   + if date/numeric, filter on boundaries: (col() >= range[0]) & (col() <= range[1])
    #   + if character, filter on membership: (col().isin(range))
    #   + sort range? range.get('start'), range.get('end')?
    assert interval in (
        "open",
        "closed",
    ), "Interval boundaries must be 'open' (a < x < b) or 'closed' (a <= x <= b)"
    assert len(boundaries) == 2, "Interval boundaries must contain two elements"
    query_expression = structure_filter(
        query_range, boundaries, interval, columns=columns, strict=strict
    )
    return data.filter(condition=~query_expression)
