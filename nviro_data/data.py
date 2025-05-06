from nviro_data.fetch import fetch_device_sensors, fetch_devices
import pandas as pd


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


def list_to_df(lst):
    return add_id(pd.DataFrame(lst))


def get_nviro_data(token):
    devices = fetch_devices(token, is_print=False)
    device_list = []
    group_list = []
    for device in devices:
        group_params = {
            "name": device["device_group"],
            "description": device["device_group"],
            "department": device["department"],
        }
        device_params = {
            "name": device["device_name"],
            "devEui": device["devEui"],
            "group": device["device_group"],
        }

        device_list.append(device_params)
        if group_params not in group_list:
            group_list.append(group_params)
    df_devices = list_to_df(device_list)
    df_groups = list_to_df(group_list)
    sensor_list = get_sensors(token, df_devices.to_dict("records"))
    df_sensors = list_to_df(sensor_list)

    data = [
        {
            "name": "Devices",
            "data": df_devices,
        },
        {
            "name": "Groups",
            "data": df_groups,
        },
        {
            "name": "Sensors",
            "data": df_sensors,
        },
    ]

    return data
