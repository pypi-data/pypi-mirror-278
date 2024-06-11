import calendar
import re

import pandera as pa

from . import settings
from .app_logger import log
from .assets.geography import COUNTRY, STATES
from .utils import check_dfcols, convert_month_values, get_date_month_cols


class BaseSchemaModel(pa.SchemaModel):
    class Config:
        strict = True
        ordered = True
        coerce = True


class FactlyDatasetSchema(BaseSchemaModel):
    _duplicate_cols = None
    _sorting_cols = None

    _check_sort = True
    _check_state_names = True
    _check_country_names = True
    _check_null_values_in_temporal = True

    @pa.dataframe_check
    def check_duplicates(cls, df):
        """
        Check for duplicates in the dataframe
        """
        if cls._duplicate_cols is not None and check_dfcols(df, cls._duplicate_cols):
            return False

        cls._duplicate_cols = (
            df.columns.tolist() if cls._duplicate_cols is None else cls._duplicate_cols
        )
        log.info(f"Checking for Duplicates on columns: {cls._duplicate_cols}")

        return ~df.duplicated(subset=cls._duplicate_cols)

    @pa.dataframe_check
    def check_sorting(cls, df):
        """
        Check for sorting in the dataframe
        """
        if not cls._check_sort:
            return True
        if cls._sorting_cols is None:
            cls._sorting_cols = get_date_month_cols(df)
        elif check_dfcols(df, cls._sorting_cols):
            return False

        if not cls.check_null_values_in_temporal(df):
            log.error(f"Null values found in columns {cls._sorting_cols}")
            return False

        if not cls.month_values_check(df):
            log.error(
                f"Invalid month values found in columns {[value for value in cls._sorting_cols if re.search(settings.MONTH_COLUMN_REGEX, value)]}"
            )
            return False

        data = df.copy()
        log.info(f"Checking for Sorting on columns: {cls._sorting_cols}")
        data = convert_month_values(data, cls._sorting_cols)
        return data[cls._sorting_cols].equals(
            data[cls._sorting_cols].sort_values(cls._sorting_cols, ascending=False)
        )

    @pa.dataframe_check
    def check_column_names(cls, df):
        """
        Check for special characters and capital letters in all column names at once
        """
        return df.columns.str.contains(r"^[a-z]+(?:_[a-z]+)*$", regex=True).all()

    @pa.dataframe_check
    def white_space_check(cls, df):
        """
        Check for multiple_white_spaces in middle and leading or tailing spaces in the dataframe
        """
        return (
            ~df.applymap(
                lambda x: isinstance(x, str) and bool(re.search(r"\s{2,}|^\s|\s$", x))
            )
            .any()
            .any()
        )

    @pa.dataframe_check
    def state_names_check(cls, df):
        """
        Check for state names in the dataframe
        """
        if not cls._check_state_names:
            return True

        state_cols = df.columns[
            df.columns.str.contains(settings.STATE_COLUMN_REGEX, regex=True)
        ].values.tolist()
        for state_col in state_cols:
            if not df[state_col].isin(STATES).all():
                return False
        return True

    @pa.dataframe_check
    def country_names_check(cls, df):
        """
        Check for country names in the dataframe
        """
        if not cls._check_country_names:
            return True

        country_cols = df.columns[
            df.columns.str.contains(settings.COUNTRY_COLUMN_REGEX, regex=True)
        ].values.tolist()
        for country_col in country_cols:
            if not df[country_col].isin([COUNTRY]).all():
                return False
        return True

    @pa.dataframe_check
    def month_values_check(cls, df):
        """
        Check for month values in the dataframe
        """
        month_cols = df.columns[
            df.columns.str.contains(settings.MONTH_COLUMN_REGEX, regex=True)
        ].values.tolist()
        for month_col in month_cols:
            if (
                not df[month_col]
                .isin([month for month in calendar.month_name[1:]])
                .all()
            ):
                return False
        return True

    @pa.dataframe_check
    def check_null_values_in_temporal(cls, df):
        """
        Check for null values in year or month columns
        """
        if not cls._check_null_values_in_temporal:
            return True
        cols = get_date_month_cols(df)
        if cols:
            return ~df.loc[:, cols].isnull().any().any()
        return True
