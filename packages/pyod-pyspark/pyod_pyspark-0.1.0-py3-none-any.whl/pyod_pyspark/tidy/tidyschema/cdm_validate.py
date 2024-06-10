from typing import Callable

import functools
import operator
import pydantic

from pyspark.sql import functions as F


def cdm_validate(model):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            print(f"Validating as {model.__name__}")
            ### check all required fields exist
            required_fields = set(model.schema().get("required"))
            missing_fields = required_fields.difference(set(data.columns))
            if missing_fields != set():
                print(f"Missing required fields: {', '.join(missing_fields)}")
            for field in model.schema().get("properties"):
                field_info = model.schema().get("properties").get(field)
                field_title = field_info.get("title")
                # field_type = field_info.get("type")
                validators = dict()
                if "maximum" in field_info:
                    validators["maximum"] = operator.le(
                        F.col(field), field_info.get("maximum")
                    )
                if "minimum" in field_info:
                    validators["minimum"] = operator.ge(
                        F.col(field), field_info.get("minimum")
                    )
                RETURN_DATA = True
                if validators != dict():
                    for validator_name, validator_function in validators.items():
                        n_invalid = data.filter(~validator_function).count()
                        if n_invalid > 0:
                            print(
                                f"Fail: {validator_name} for `{field_info.get('title')}` flagged {n_invalid:,} row(s)"
                            )
                            RETURN_DATA = False
                        else:
                            print(
                                f"Success: {validator_name} for `{field_info.get('title')}` passed"
                            )
            if not RETURN_DATA:
                raise AssertionError(
                    "Invalid data! Please review validation summary before proceeding."
                )

        return wrapper

    return decorator
