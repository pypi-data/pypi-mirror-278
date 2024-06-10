from typing import List

DEFAULT_LOG_FILE: str = "virus.log"
DEFAULT_VALIDATION_RULES: str = "src/validations/rules.py"
DEFAULT_DATASET_RULES: str = "src/validations/config.json"
DEFAULT_VALIDATION_COLUMNS: List[str] = [
    "schema_context",
    "column",
    "check",
    "check_number",
    "failure_case",
    "index",
]
# detects: date_time, date, start_date, end_date. not_detected: candidate, candidate_name
DATE_COLUMN_REGEX: str = r"\b(?:\w*_)?date(?:_\w*)?\b"
# detects: year, year_month, year_month_date. not_detected: years, yearmonth
YEAR_COLUMN_REGEX: str = r"\b(?:\w*_)?year(?:_\w*)?\b"
# detects: month, month_name, month_number. not_detected: months, monthname
MONTH_COLUMN_REGEX: str = r"\b(?:\w*_)?month(?:_\w*)?\b"
# detects: year, month, fiscal_year, month_name. not_detected: year_month
DATE_MONTH_COLUMNS_REGEX: str = r"\b(?:\w*_)?(year|month|date)(?:_\w*)?\b"
STATE_COLUMN_REGEX: str = r"\b(?:\w*_)?state(?:_\w*)?\b"
COUNTRY_COLUMN_REGEX: str = r"\b(?:\w*_)?country(?:_\w*)?\b"
FISCAL_YEAR_MONTH_DICT: dict = {
    "April": 1,
    "May": 2,
    "June": 3,
    "July": 4,
    "August": 5,
    "September": 6,
    "October": 7,
    "November": 8,
    "December": 9,
    "January": 10,
    "February": 11,
    "March": 12,
}
YEAR_MONTH_DICT: dict = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}
