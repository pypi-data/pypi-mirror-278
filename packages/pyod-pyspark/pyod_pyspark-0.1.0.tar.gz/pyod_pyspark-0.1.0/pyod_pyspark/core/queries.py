from typing import Iterable
import operator

import pyspark
from pyspark.sql.column import Column
from pyspark.sql.dataframe import DataFrame
from pyspark.sql import functions as F


def query_nulls(column: str) -> Column:
    """Returns function filtering a column for null or whitespace values"""
    return F.col(column).isNull() | F.col(column).rlike("^\s*")


def query_range(column: str, boundaries: Iterable, interval: str) -> Column:
    """Returns function filtering a column within the specified boundaries."""
    if interval == "open":
        lower_op, upper_op = operator.gt, operator.lt
    if interval == "closed":
        lower_op, upper_op = operator.ge, operator.le
    return lower_op(F.col(column), boundaries[0]) & upper_op(
        F.col(column), boundaries[1]
    )
