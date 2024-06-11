import importlib.util
import json
from pathlib import Path
from typing import Union

import pandas as pd
import yaml
from pandera.errors import SchemaErrors

from . import settings
from .app_logger import log
from .assets.constants import FILE_EXTENSIONS
from .utils import format_output

module_name = "rules"
validation_output_columns = settings.DEFAULT_VALIDATION_COLUMNS


class VirusEngine:
    """
    Object facilitate to get the mapping for dataset and schema, and validate the dataset with schema
    """

    def __init__(
        self,
        config_path: str = settings.DEFAULT_DATASET_RULES,
        module_path: str = settings.DEFAULT_VALIDATION_RULES,
    ):
        # Current working directory is always at datasets project dir
        self.cwd = Path.cwd()
        self.schema_config_path = self.cwd / config_path
        self.module_path = module_path

    def _get_schema_mapping(self):
        # There are only 2 file extensions supported: .yaml and .json
        if self.schema_config_path.suffix == ".yaml":
            with open(str(self.schema_config_path), "r") as f:
                schema_mapping = yaml.safe_load(f)
        elif self.schema_config_path.suffix == ".json":
            with open(str(self.schema_config_path), "r") as f:
                schema_mapping = json.load(f)
        else:
            raise ValueError("File format not supported")
        schema_mapping = {
            str(path) if path.endswith(".csv") else f"{path}*.csv": schema
            for path, schema in schema_mapping.items()
        }
        current_dir = Path(".")
        iterated_path_schema_mapping = {
            str(path): schema
            for paths, schema in schema_mapping.items()
            for path in current_dir.glob(paths)
        }
        return iterated_path_schema_mapping

    def retrieve_dataset(self, src: Union[str, Path], **kwargs):
        real_paths = self.cwd.glob(src)
        ## Checks if the generator is empty
        try:
            _ = next(real_paths)
        except StopIteration:
            log.warning(f"Path does not exist: {src}")

        if src.endswith(FILE_EXTENSIONS):
            glob_path = src
        else:
            glob_path = src + "**/*.csv"
        for each_file in (self.cwd).glob(glob_path):
            yield each_file, pd.read_csv(each_file, low_memory=False, **kwargs)

    def validate_with_schema(self, schema_name: str, df: pd.DataFrame) -> pd.DataFrame:
        # create a module spec
        spec = importlib.util.spec_from_file_location(module_name, self.module_path)

        # create a module object
        module = importlib.util.module_from_spec(spec)

        # load the module
        spec.loader.exec_module(module)

        rule_class = getattr(module, schema_name)

        try:
            _ = rule_class.validate(df, lazy=True)
            return pd.DataFrame(columns=validation_output_columns), False
        except SchemaErrors as err:
            return format_output(err, rule_class, len(df.columns)), True
