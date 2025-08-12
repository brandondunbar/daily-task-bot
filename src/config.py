"""Loads and validates the application's YAML configuration.

Provides a helper function to read a YAML config file from disk,
parse it, and return a validated `Config` object based on the schema.
"""

from pathlib import Path

import yaml

from .config_schema import Config  # or adjust as needed


def load_config(path: str) -> Config:
    """Load and parse a YAML configuration file into a validated Config object.

    Args:
        path (str): Path to the YAML config file.

    Returns:
        Config: Parsed and validated configuration object.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the file is not valid YAML.
        pydantic.ValidationError: If the config does not match schema.
    """
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, 'r') as f:
        raw_config = yaml.safe_load(f)

    return Config(**raw_config)  # validates automatically
