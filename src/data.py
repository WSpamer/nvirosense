import os

import pandas as pd
from loguru import logger
from nviro_fetch.auth import authenticate

from readings import get_readings

logger.enable("nviro_fetch")


def load_data(token, devices, start_date, end_date):
    """
    Load data for all devices within the specified date range.
    Args:
        devices (list): List of device dictionaries containing 'devEui' and 'device_name'.
        start_date (str): Start date for fetching readings.
        end_date (str): End date for fetching readings.
    """
    # token = authenticate()
    data_list = []
    for device in devices:
        device_id = device["devEui"]
        print(f"Fetching readings for {device['device_name']} ({device_id})")
        df = get_readings(token, device_id, start_date, end_date)
        params = {
            "device_name": device["device_name"],
            "df": df,
        }
        data_list.append(params)

    return data_list


def data_processing(data_list):
    dfs_inside = [
        x["df"] for x in data_list if x["device_name"] != "Willow Creek Weather"
    ]
    df_inside = pd.concat(dfs_inside, axis=1)
    df_inside["SOLAR RADIATION"] = df_inside["LIGHT"].apply(
        lambda x: round(float(x) * 0.0079, 2)
    )
    df_inside = df_inside.drop(columns=["WIND DIRECTION", "LIGHT"])
    # ------------- Process Outside Data -------------
    df_outside = [
        data for data in data_list if data["device_name"] == "Willow Creek Weather"
    ][0]["df"]

    sensor_list = list(df_inside.columns)
    df_outside = df_outside[sensor_list]

    df_inside[sensor_list] = df_inside[sensor_list].astype(float)
    df_outside[sensor_list] = df_outside[sensor_list].astype(float)

    params = {
        "df_inside": df_inside,
        "df_outside": df_outside,
        # "sensor_list": sensor_list,
    }

    return params
