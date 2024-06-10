import sys
import functools
import attrs
from loguru import logger

import pyspark
from pyspark.sql import types, functions as F

import pyod.core.selectors as cs
import pyod.core.filter as tf


@attrs.define
class TidyDataFrame:
    _data: pyspark.sql.DataFrame = attrs.field(
        validator=attrs.validators.instance_of(pyspark.sql.DataFrame)
    )
    toggle_options: dict[str, bool] = attrs.field(factory=dict)
    _n_rows: int = attrs.field(default=0)
    _n_cols: int = attrs.field(default=0)

    def __attrs_post_init__(self):
        logger.remove()
        logger.add(sink=sys.stdout, format="{time:HH:mm:ss} | {level} | {message}")
        self.toggle_options.setdefault("count", True)
        self.toggle_options.setdefault("display", True)

    @property
    def data(self):
        return self._data

    @property
    def unknown_dimension(self):
        return "???"

    def count(self, result: pyspark.sql.DataFrame = None):
        """
        Retrieve number of rows from DataFrame-like object
        """
        if not self.toggle_options.get("count"):
            self._n_rows = self._unknown_dimension
            return 0
        else:
            if self._n_rows == self._unknown_dimension:  # not defined, compute
                self._n_rows = self._data.count()
            if result is not None:  # result computed, recompute row count
                self._n_rows = result._data.count()
            return self._n_rows  # defined and no new result, return row count

    def tidy_logger(
        self, operation="custom", message="user-defined message here", level="info"
    ):
        """Method for logging operations to console.

        Note
        ====
        Previously returned None, but now returns self so that
        users can include the method within their chain of command.

        Example
        =======
        >>> (
            TidyDataFrame(data)
            .select('ID')
            .tidy_logger("Removing null values from ID column")
            .filter(~ col('ID').isNull())
        )
        #> Removing null values from ID column
        #> filter: contains N rows, removed X rows, returned N-X rows
        """
        getattr(logger, level)(f"#> {operation}: {message}")
        return self

    def tidy_controller(message: str, alias: str = None):
        """Orchestrator for decorated DataFrame methods.

        This function packages common operations such that any decorated
        DataFrame method will perform the following in addition to the
        user's results.
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                if hasattr(self, func.__name__):
                    result = func(self, *args, **kwargs)
                    self._n_cols = len(result._data.columns)
                    if not kwargs.get("disable_message", False):
                        self.tidy_logger(
                            operation=func.__name__ if alias is None else alias,
                            message=eval(f"f'{message}'"),
                        )
                    return result

            return wrapper

        return decorator

    @tidy_controller("removed X rows, N - X remaining")
    def filter(self, condition):
        self._data = self._data.filter(condition)
        return self

    @tidy_controller("something goes here")
    def get_columns(self, *args, **kwargs):
        return cs.get_columns(data=self._data, *args, **kwargs)

    @tidy_controller("something goes here")
    def filter_nulls(self, *args, **kwargs):
        self._data = tf.filter_nulls(data=self._data, *args, **kwargs)
        return self

    @tidy_controller("something goes here")
    def filter_range(self, *args, **kwargs):
        self._data = tf.filter_range(data=self._data, *args, **kwargs)
        return self
