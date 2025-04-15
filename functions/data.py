from functions.fetch import fetch_device_sensors


def get_sensors(token, devices: list):
    sensor_list = []
    for device in devices:
        sensors = fetch_device_sensors(token, device)
        for sensor in sensors:
            params = {
                "device_id": device["id"],
                "name": sensor["sensor_name"],
                "unit": sensor["unit"],
            }
            sensor_list.append(params)
    return sensor_list


def add_id(df):
    df.insert(0, "id", range(1, 1 + len(df)))
    return df
