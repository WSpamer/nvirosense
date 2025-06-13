import os
from loguru import logger

from src.common import read_json


def read_global():
    """
    Reads global settings from a JSON file.
    Returns:
        dict: Global settings loaded from the JSON file.
    """
    file_path = "global.json"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Global settings file '{file_path}' not found.")
    return read_json(file_path)


def env_global(name: str = "start_date") -> str:
    """
    Returns global settings for the application.
    """

    global_settings = read_global()
    if not global_settings:
        logger.error("Global settings are empty or not properly loaded.")
        raise ValueError("Global settings are empty or not properly loaded.")
    if name not in global_settings:
        logger.error(f"Global settings must contain '{name}' key.")
        raise KeyError(f"Global settings must contain '{name}' key.")
    return global_settings[name]
