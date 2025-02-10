import json
import os

def load_config(config_file: str = "config.json") -> dict:
    """
    Loads configuration from the provided JSON file.

    Args:
        config_file (str): Name of the config file (default "config.json").

    Returns:
        dict: The configuration dictionary.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Assuming config.json is in the parent of utils (i.e. in src/)
    config_path = os.path.join(base_dir, "..", config_file)
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)
