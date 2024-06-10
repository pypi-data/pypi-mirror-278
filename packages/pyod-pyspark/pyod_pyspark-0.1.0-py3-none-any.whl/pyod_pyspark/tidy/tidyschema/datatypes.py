from types import MappingProxyType

import decimal
import datetime

from pyspark.sql.types import (
    StringType,
    IntegerType,
    FloatType,
    DecimalType,
    DateType,
    TimestampType,
    DoubleType,
)


PYSPARK_TYPES = MappingProxyType(
    {
        # builtin types
        str: StringType(),
        int: IntegerType(),
        float: FloatType(),
        # standard library types
        decimal.Decimal: DecimalType(),
        datetime.date: DateType(),
        datetime.datetime: TimestampType(),
        # custom types
        "double": DoubleType(),
    }
)
