from pyspark.sql import types
import pandas as pd

from pydantic import BaseModel, fields

from pyod_pyspark.tidy.tidyschema.datatypes import PYSPARK_TYPES


class DataModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_fields(cls):
        return cls.__annotations__.items()

    @classmethod
    def as_struct_field(
        cls, field_name: str, field_info: fields.FieldInfo
    ) -> types.StructField:
        field_type = field_info.annotation
        field_null = not field_info.is_required
        return types.StructField(
            name=field_name,
            dataType=PYSPARK_TYPES.get(field_type, types.NullType()),
            nullable=field_null,
        )

    @classmethod
    def get_schema(cls):
        return types.StructType(
            [
                cls.as_struct_field(field_name, field_info)
                for field_name, field_info in cls.model_fields.items()
            ]
        )

    @classmethod
    def get_required_fields(cls):
        return cls.model_json_schema().get("required")

    @classmethod
    def get_optional_fields(cls):
        return set(cls.model_fields.keys()).difference(cls.get_required_fields())

    @classmethod
    def request_form(cls):
        COLUMN_NAMES = ["title", "description", "type"]
        parsed_request_form = {
            k: {
                name.title(): detail
                for name, detail in v.items()
                if name in COLUMN_NAMES
            }
            for k, v in cls.model_json_schema().get("properties").items()
        }
        return pd.DataFrame.from_dict(parsed_request_form).T
