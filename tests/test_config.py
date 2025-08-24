from tempfile import NamedTemporaryFile
from unittest.mock import patch

import pytest
import yaml
from pydantic import ValidationError
from src.config import load_config


def test_valid_config_load():
    """Loads a valid YAML config into a Config object."""
    config_dict = {
        "google_sheets": {
            "spreadsheet_id": "abc123",
            "time_zone": "UTC",
            "date_column_name": "Date",
        },
        "doc_blocks": [
            {
                "name": "Block A",
                "sheet_name": "Sheet1",
                "template_path": "templates/block_a.md",
                "block_title_template": "Block A - {{ date }}",
                "doc_id": "doc-1",
                "enabled": True,
            }
        ],
    }

    with NamedTemporaryFile(mode="w+", suffix=".yaml") as tmp:
        yaml.dump(config_dict, tmp)
        tmp.seek(0)
        config = load_config(tmp.name)
        assert config.google_sheets.spreadsheet_id == "abc123"


def test_missing_required_key_logs_and_raises():
    """Raises ValidationError and logs when required schema fields are missing."""
    bad_config = {
        "google_sheets": {
            "spreadsheet_id": "abc123",
            "time_zone": "UTC",
        },
        "doc_blocks": [
            {
                # Missing required key: template_path
                "name": "Block A",
                "sheet_name": "Sheet1",
                "block_title_template": "Oops - {{ date }}",
                "enabled": True,
            }
        ],
    }

    with NamedTemporaryFile(mode="w+", suffix=".yaml") as tmp:
        yaml.dump(bad_config, tmp)
        tmp.seek(0)
        with patch("src.config.log.exception") as mock_log:
            with pytest.raises(ValidationError):
                load_config(tmp.name)
            mock_log.assert_called()  # validation error logged


def test_invalid_yaml_logs_and_raises():
    """Logs and raises yaml.YAMLError for malformed YAML content."""
    invalid_yaml = "google_sheets: [unclosed_list\n  spreadsheet_id: abc123"
    with NamedTemporaryFile(mode="w+", suffix=".yaml") as tmp:
        tmp.write(invalid_yaml)
        tmp.flush()
        with patch("src.config.log.exception") as mock_log:
            with pytest.raises(yaml.YAMLError):
                load_config(tmp.name)
            mock_log.assert_called()  # YAML error logged


def test_nonexistent_file_logs_and_raises(tmp_path):
    """Logs and raises FileNotFoundError when config file does not exist."""
    missing = tmp_path / "no_such_config.yaml"
    with patch("src.config.log.exception") as mock_log:
        with pytest.raises(FileNotFoundError):
            load_config(str(missing))
        mock_log.assert_called()  # not found logged
