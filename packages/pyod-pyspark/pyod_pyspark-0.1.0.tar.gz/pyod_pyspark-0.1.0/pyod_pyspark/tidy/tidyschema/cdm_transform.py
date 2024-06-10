from typing import Callable
import functools
import datetime

from pyspark.sql import types, functions as F
import pydantic

from pyod_pyspark.tidy.tidyschema.datatypes import PYSPARK_TYPES


def cdm_transform(model: pydantic._internal._model_construction.ModelMetaclass):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            model_schema = model.get_schema()
            for field in model_schema:
                if field.dataType in (
                    PYSPARK_TYPES.get(datetime.datetime),
                    PYSPARK_TYPES.get(datetime.date),
                ):
                    data = data.withColumn(
                        field.name,
                        F.date_format(
                            F.col(field.name).cast(field.dataType), "MM/dd/yyyy"
                        ),
                    )
                else:
                    data = data.withColumn(
                        field.name, F.col(field.name).cast(field.dataType)
                    )
            return data

        return wrapper

    return decorator
