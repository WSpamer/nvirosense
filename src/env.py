import os

from loguru import logger

from common import read_json

# get_project_path() = "/Users/wspamer/Dev/python/projects/ccr-system/nvirosense"


def get_project_path(OS="WSL") -> str:
    """
    Returns the project path.
    """
    if OS not in ["WSL", "Mac"]:
        logger.error(f"Unsupported OS: {OS}. Supported OS are 'WSL' and 'Mac'.")
        raise ValueError(f"Unsupported OS: {OS}. Supported OS are 'WSL' and 'Mac'.")
    if OS == "WSL":
        return "/home/wspamer/dev/python/nvirosense"
    elif OS == "Mac":
        return "/Users/wspamer/Dev/python/projects/ccr-system/nvirosense"
    else:
        logger.error(f"Unsupported OS: {OS}. Supported OS are 'WSL' and 'Mac'.")
        raise ValueError(f"Unsupported OS: {OS}. Supported OS are 'WSL' and 'Mac'.")


def read_global(file_path: str = "global.json") -> dict:
    """
    Reads global settings from a JSON file.
    Returns:
        dict: Global settings loaded from the JSON file.
    """
    file_path = os.path.join(get_project_path(), file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Global settings file '{file_path}' not found.")
    return read_json(file_path)


def env_global(name: str = "start_date", file_path: str = "global.json") -> str:
    """
    Returns global settings for the application.
    """

    global_settings = read_global(file_path=file_path)
    if not global_settings:
        logger.error("Global settings are empty or not properly loaded.")
        raise ValueError("Global settings are empty or not properly loaded.")
    if name == "project_path":
        return get_project_path()
    if name not in global_settings:
        logger.error(f"Global settings must contain '{name}' key.")
        raise KeyError(f"Global settings must contain '{name}' key.")
    if name == "path_data":
        global_settings[name] = os.path.join(get_project_path(), global_settings[name])
        logger.info(f"Updated 'path_data' to: {global_settings[name]}")

    return global_settings[name]
