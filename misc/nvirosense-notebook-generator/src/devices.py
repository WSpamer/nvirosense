def check_and_load_devices(json_file_path):
    import json
    import os

    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"The JSON file at {json_file_path} does not exist.")

    with open(json_file_path, 'r') as file:
        devices = json.load(file)

    return devices

def get_device_by_name(devices, device_name):
    device = next((device for device in devices if device["device_name"] == device_name), None)
    if device is None:
        raise ValueError(f"Device '{device_name}' not found in the device list.")
    return device