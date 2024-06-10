from typing import Iterable
import re
import datetime
import json

import pyspark
from pyspark.sql import types
from pyspark.sql import functions as F

import jinja2
import docxtpl


DIC_COL_LINES = "Number_of_Affected_Lines"


def read_dataset(_func_read: callable, path: str) -> pyspark.sql.DataFrame:
    """Read and return dataset at path"""
    path = (
        path[:-1] if path.endswith("/") else path
    )  # cp.read thinks "/" indicates folder
    data = _func_read(path)
    if "DQC" in path:
        return data.filter(F.col(DIC_COL_LINES).isNotNull())
    return data


def get_file(
    _func_ls: callable, directory: str, pattern: str, recursive: bool = True
) -> str:
    all_files = _func_ls(directory, recursive=True)
    matched_files = list(filter(lambda x: re.search(re.compile(pattern), x), all_files))
    if len(matched_files) > 1:
        from pprint import pprint

        pprint(matched_files)
        raise ValueError("Multiple files matched pattern - refine output directory!")
    return matched_files[0]


def collect_as_json(data: pyspark.sql.DataFrame) -> list[str]:
    return data.toJSON().collect()


def get_total_lines(
    data_recon: pyspark.sql.DataFrame,
    column_lines: str = "number_of_lines",
    _alias: str = "Lines",
) -> int:
    return data_recon.agg(
        F.sum(F.col(column_lines).cast(types.IntegerType())).alias(_alias)
    ).collect()[0][_alias]


def format_datetime(dt: datetime.datetime, format: str = "%m/%d/%Y") -> str:
    def format_quarter(dt: datetime.datetime) -> str:
        return f"Q{((dt.month - 1) // 3) + 1}"

    if format == "%Q":
        if isinstance(dt, Iterable):
            formatted = sorted(set(map(format_quarter, dt)))
            return " - ".join(formatted)
        return format_quarter(dt)

    if isinstance(dt, Iterable):
        formatted = sorted(set(map(lambda x: x.strftime(format), dt)))
        return " - ".join(formatted)
    return dt.strftime(format)


def generate_output(
    engagement_context: dict[str, str],
    data_dic: pyspark.sql.DataFrame,
    data_recon: pyspark.sql.DataFrame,
    output_dir: str,
    output_file: str = "result.docx",
) -> None:
    TEMPLATE_PATH = "/Workspace/Clients/AEROVIRONMENT, INC/2024/AEROVIRONMENT, INC FY23/Notebooks/journal_entry_email_template - pyspark.docx"

    COL_RECONCILIATION = "reconciliation"
    CONST_UNRECONCILED = "Unreconciled"

    NUMBER_OF_UNRECONCILED_ACCOUNTS = data_recon.filter(
        F.col(COL_RECONCILIATION).rlike(f"^{CONST_UNRECONCILED}$")
    ).count()
    NUMBER_OF_LINES = get_total_lines(data_recon)

    def collect_as_json(data: pyspark.sql.DataFrame) -> list[str]:
        return data.toJSON().collect()

    def calculate_proportion(n: int, total: int = NUMBER_OF_LINES):
        return f"{n/total:1%}"

    def get_length(obj: Iterable) -> int:
        if hasattr(obj, "__len__"):
            return len(obj)
        return 1

    json_dic = json.loads(f"[{', '.join(collect_as_json(data_dic))}]")
    context = {
        "DQCFlags": json_dic,
        "UnreconciledAccounts": NUMBER_OF_UNRECONCILED_ACCOUNTS,
        "SummaryText": "**Possible high-level summary of information above**",
        "IsReconciled": "**Possibly statistical summary of datasets**",
    }
    context = engagement_context | context

    jinja_env = jinja2.Environment()
    jinja_env.filters["calculate_proportion"] = calculate_proportion
    jinja_env.filters["get_length"] = get_length
    jinja_env.filters["format_datetime"] = format_datetime

    if not output_file.endswith(".docx") and "docx" not in output_file:
        output_file = f"{output_file}.docx"

    doc = docxtpl.DocxTemplate(TEMPLATE_PATH)
    doc.render(context, jinja_env=jinja_env, autoescape=True)
    doc.save(f"{output_dir}/{output_file}")
