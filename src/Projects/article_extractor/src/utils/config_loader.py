import json
import os

def load_config(config_path: str = "config.json"):
    """Loads search configuration from a JSON file.

    Args:
        config_path (str): Path to the config file.

    Returns:
        tuple: (companies, keywords, num_pages) from the config.
    """
    # Get the absolute path relative to the src folder.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(base_dir, "..", config_path)
    with open(config_file, "r") as file:
        config = json.load(file)
    companies = config.get("companies", [])
    keywords = config.get("keywords", [])
    num_pages = config.get("num_pages", 1)
    return companies, keywords, num_pages
