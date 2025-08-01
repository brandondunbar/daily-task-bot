import pytest
from src.config_loader import load_config
import yaml
import tempfile
import os


# Sample valid config for testing
VALID_CONFIG = {
    "sheets": [
        {
            "name": "Test Sheet",
            "id": "fake-sheet-id",
            "worksheet": "Schedule",
            "date_column": "Date",
            "output_folder_id": "fake-folder-id",
            "template_blurb": "Today's focus is on {{ Pattern Focus }}.",
            "column_mapping": {
                "Pattern Focus": "Pattern Focus",
                "Problem Title": "Problem Title",
                "LeetCode Link": "LeetCode Link"
            },
            "calendar": {
                "title_template": "LeetCode – {{ Pattern Focus }}",
                "time": "08:00",
                "duration_minutes": 30
            }
        }
    ]
}


def write_temp_config(data: dict):
    """
    Write a temporary YAML config file for testing purposes.

    Args:
        data (dict): A dictionary to serialize into YAML.

    Returns:
        str: Path to the temporary YAML file.
    """
    temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".yaml")
    yaml.dump(data, temp_file)
    temp_file.close()
    return temp_file.name


def test_load_valid_config():
    """
    Test that load_config successfully loads a valid YAML config file
    and returns the expected dictionary structure.
    """
    path = write_temp_config(VALID_CONFIG)
    config = load_config(path)

    assert isinstance(config, dict)
    assert "sheets" in config
    assert len(config["sheets"]) == 1
    assert config["sheets"][0]["name"] == "Test Sheet"

    os.remove(path)


def test_missing_required_key():
    """
    Test that load_config raises a KeyError when required fields
    (like 'id') are missing in the YAML config.
    """
    bad_config = {
        "sheets": [
            {
                # missing 'id'
                "name": "Broken Config",
                "worksheet": "Schedule"
            }
        ]
    }
    path = write_temp_config(bad_config)

    with pytest.raises(KeyError):
        load_config(path)

    os.remove(path)
