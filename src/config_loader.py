import yaml
from pathlib import Path
from typing import Any, Dict


def load_config(path: str) -> Dict[str, Any]:
    """
    Load and parse a YAML configuration file.

    Args:
        path (str): Path to the YAML config file.

    Returns:
        dict: Parsed configuration dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the file is not valid YAML.
        KeyError: If required fields are missing.
    """
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    # Basic validation
    if "sheets" not in config:
        raise KeyError("Missing required key: 'sheets'")

    for sheet in config["sheets"]:
        required_keys = ["name", "id", "worksheet"]
        for key in required_keys:
            if key not in sheet:
                raise KeyError(f"Missing required key in sheet config: '{key}'")

    return config
