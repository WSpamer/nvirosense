def load_json(file_path):
    import json
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    import json
    with open(file_path, 'w') as file:
        json.dump(data, file)

def format_device_name(device_name):
    return device_name.replace(" ", "_").lower()

def get_device_by_name(devices, device_name):
    return next((device for device in devices if device["device_name"] == device_name), None)

def get_device_names(devices):
    return [device["device_name"] for device in devices]