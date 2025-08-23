"""Loads and validates the application's YAML configuration.

Provides a helper function to read a YAML config file from disk,
parse it, and return a validated `Config` object based on the schema.
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from src.observability.logging_setup import get_logger

from .config_schema import Config  # or adjust as needed

log = get_logger(__name__)


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
    log.info("config_loading", path=str(path_obj))

    if not path_obj.exists():
        log.exception("config_not_found", path=str(path_obj))
        raise FileNotFoundError(f"Config file not found: {path}")

    try:
        raw_text = path_obj.read_text(encoding="utf-8")
        data: Any = yaml.safe_load(raw_text)
    except yaml.YAMLError as ye:
        log.exception("config_yaml_error", path=str(path_obj), error=str(ye))
        raise
    except Exception as e:
        log.exception("config_read_error", path=str(path_obj), error=str(e))
        raise

    try:
        cfg = Config(**data)  # validates automatically (Pydantic v1/2 compat kwargs)
        log.info(
            "config_loaded",
            doc_blocks=len(cfg.doc_blocks),
            spreadsheet_id=cfg.google_sheets.spreadsheet_id,
            time_zone=cfg.google_sheets.time_zone,
        )
        return cfg
    except ValidationError as ve:
        # Provide structured error details for easier debugging
        try:
            errs = ve.errors()  # pydantic v1/v2 both expose .errors()
        except Exception:
            errs = str(ve)
        log.exception("config_validation_error", path=str(path_obj), errors=errs)
        raise
