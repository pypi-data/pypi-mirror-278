import re

import pandas as pd
import pandera as pa

from . import settings
from .app_logger import log


def format_output(
    err: pa.errors.SchemaErrors, rule_class: str, no_of_cols: int
) -> pd.core.frame.DataFrame:
    """Reframe the output of the validation engine

    Args:
        err (pandera.errors.SchemaErrors): The error object from the validation engine

    Returns:
        pandas.core.frame.DataFrame: The reframed output
    """
    df = err.failure_cases.drop(columns=["index"])
    # mask of check_duplicates and failure_case containing True
    mask = (df["check"] == "check_duplicates") & (df["failure_case"])
    df.loc[mask, ["column", "failure_case"]] = [
        rule_class,
        f"{mask.sum() // no_of_cols} rows",
    ]

    return df.drop_duplicates()


def check_dfcols(df: pd.core.frame.DataFrame, cols: list) -> bool:
    """
    Check if the columns are present in the dataframe
    """
    if not set(cols).issubset(df.columns):
        log.error(f"Columns {cols} not found in the DataFrame")
        return True
    else:
        return False


def get_date_month_cols(df: pd.core.frame.DataFrame) -> list:
    return df.columns[
        df.columns.str.extract(
            settings.DATE_MONTH_COLUMNS_REGEX, expand=False
        ).notna()
    ].tolist()


def convert_month_values(df, sorting_cols):
    cols = [
        value
        for value in sorting_cols
        if re.search(settings.MONTH_COLUMN_REGEX, value)
    ]

    # if fiscal_year then months start from April else January
    if "fiscal_year" in df.columns:
        map_values = settings.FISCAL_YEAR_MONTH_DICT
    else:
        map_values = settings.YEAR_MONTH_DICT
    for col in cols:
        df[col] = df[col].map(map_values)

    return df
