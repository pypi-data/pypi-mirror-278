from typing import Iterable

import re

import pyspark
from pyspark.sql import types


def get_columns(
    data: pyspark.sql.DataFrame,
    columns: list[str] = None,
    pattern: str = None,
    dtype: types.DataType = None,
) -> list[str]:
    if dtype is not None:
        return get_columns_by_dtype(data=data, dtype=dtype)
    if pattern is not None:
        return get_columns_by_pattern(data=data, pattern=pattern)
    if columns is not None:
        return [c for c in columns if c in data.columns]
    return data.columns


def get_columns_by_pattern(data: pyspark.sql.DataFrame, pattern: str) -> list[str]:
    re_pattern = re.compile(pattern)
    matching_columns = filter(
        lambda c: isinstance(re_pattern.match(c.name), re.Match), data.schema
    )
    return list(map(lambda c: c.name, matching_columns))


def get_columns_by_dtype(
    data: pyspark.sql.DataFrame, dtype: types.DataType
) -> list[str]:
    if isinstance(dtype, list):
        dtype = tuple(dtype)
    if not isinstance(dtype, Iterable):
        dtype = (dtype,)
    assert all(
        dt.__name__ in pyspark.sql.types.__dir__() for dt in dtype
    ), f"Invalid datatype: {dtype.__name__}"
    matching_columns = filter(lambda c: isinstance(c.dataType, dtype), data.schema)
    return list(map(lambda c: c.name, matching_columns))
