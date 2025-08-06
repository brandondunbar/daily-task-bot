import pytest
from src.config import load_config
from pydantic import ValidationError
from tempfile import NamedTemporaryFile
import yaml


def test_valid_config_load():
    config_dict = {
        "google_sheets": {
            "spreadsheet_id": "abc123",
            "time_zone": "UTC",
            "date_column_name": "Date"
        },
        "doc_blocks": [
            {
                "name": "Block A",
                "sheet_name": "Sheet1",
                "template_path": "templates/block_a.md",
                "block_title_template": "Block A - {{ date }}",
                "enabled": True
            }
        ]
    }

    with NamedTemporaryFile(mode="w+", suffix=".yaml") as tmp:
        yaml.dump(config_dict, tmp)
        tmp.seek(0)
        config = load_config(tmp.name)
        assert config.google_sheets.spreadsheet_id == "abc123"


def test_missing_required_key():
    bad_config = {
        "google_sheets": {
            "spreadsheet_id": "abc123",
            "time_zone": "UTC"
        },
        "doc_blocks": [
            {
                # Missing required key: template_path
                "name": "Block A",
                "sheet_name": "Sheet1",
                "block_title_template": "Oops - {{ date }}",
                "enabled": True
            }
        ]
    }

    with NamedTemporaryFile(mode="w+", suffix=".yaml") as tmp:
        yaml.dump(bad_config, tmp)
        tmp.seek(0)
        with pytest.raises(ValidationError):
            load_config(tmp.name)
