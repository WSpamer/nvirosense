import os

import pandas as pd
from loguru import logger
from nviro_fetch.auth import authenticate
from nviro_fetch.fetch import fetch_devices

from src.env import env_global


def get_devices():
    token = authenticate()
    devices = fetch_devices(token)
    return devices


def store_devices(devices):
    """
    Stores the fetched devices in a JSON file.

    Args:
        devices (list): List of device dictionaries to be stored.
    """
    if not devices:
        logger.warning("No devices to store.")
        return

    logger.info(f"Storing {len(devices)} devices.")
    for device in devices:
        logger.debug(f"Device: {device['device_name']}")
    path_data = env_global("path_data")
    if not path_data:
        logger.error(
            "Path to data is not set in global settings. Returning default path."
        )
        path_data = "../data"
    file_path = os.path.join(path_data, "devices.json")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    pd.DataFrame(devices).to_json(file_path, orient="records", indent=4)
    logger.info(f"Devices stored successfully at {file_path}")


def load_devices():
    """
    Loads devices from a JSON file.

    Returns:
        list: List of device dictionaries loaded from the file.
    """
    path_data = env_global("path_data")
    if not path_data:
        logger.error(
            "Path to data is not set in global settings. Returning default path."
        )
        path_data = "../data"

    file_path = os.path.join(path_data, "devices.json")
    if not os.path.exists(file_path):
        logger.error(f"Devices file '{file_path}' not found.")
        return []

    devices = pd.read_json(file_path, orient="records").to_dict(orient="records")
    return devices


# device_names = [device["device_name"] for device in devices]


# Convert the list of devices to a DataFrame and save it as JSON
def save_devices():
    """
    Fetches devices and saves them to a JSON file.
    """
    devices = get_devices()
    store_devices(devices)

    return devices


def device_names():
    """
    Returns a list of device names from the stored devices.

    Returns:
        list: List of device names.
    """
    devices = load_devices()
    if not devices:
        logger.warning("No devices found. Returning an empty list.")
        return []

    device_names = [device["device_name"] for device in devices]
    return device_names

def device_file_name(device_name):
    """
    Returns the file name for a device based on its name.

    Args:
        device_name (str): The name of the device.

    Returns:
        str: The file name for the device.
    """
    return f"{device_name.replace(' ', '_').lower()}.json"


# Check if devices.json exists and load devices if it does
def check_and_load_devices():
    """
    Checks if the devices file exists and loads devices if it does.

    Returns:
        list: List of device dictionaries or an empty list if the file does not exist.
    """
    path_data = env_global("path_data")
    if not path_data:
        logger.error(
            "Path to data is not set in global settings. Returning default path."
        )
        path_data = "../data"

    file_path = os.path.join(path_data, "devices.json")
    if os.path.exists(file_path):
        return load_devices()
    else:
        logger.warning(
            f"Devices file '{file_path}' does not exist. Returning an empty list."
        )
        return []


if __name__ == "__main__":
    devices = check_and_load_devices()
    if devices:
        logger.info(f"Loaded {len(devices)} devices.")
    else:
        logger.warning("No devices found.")
