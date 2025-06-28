import os

import pandas as pd
from loguru import logger
from nviro_fetch.auth import authenticate

from env import env_global
from readings import get_readings

logger.enable("nviro_fetch")


def load_data(token, devices, start_date, end_date):
    """
    Load data for all devices within the specified date range.
    Args:
        devices (list): List of device dictionaries containing 'devEui' and 'device_name' and 'location'.
        start_date (str): Start date for fetching readings.
        end_date (str): End date for fetching readings.
    Returns:
        list: List of dictionaries containing device names and their corresponding DataFrames.
    Each dictionary in the list has the keys 'device_name' and 'df' where 'df' is a DataFrame
        containing the readings for that device.
    """
    # token = authenticate()
    date_stable = pd.to_datetime(env_global("end_date"))
    start_date_dt = pd.to_datetime(start_date)
    if start_date_dt < date_stable:
        logger.warning(
            f"Start date {start_date} is after the stable date {date_stable}. "
            "Using stable date as the start date."
        )
        start_date = date_stable.strftime("%Y-%m-%dT%H:%M:%S")
    data_list = []
    for device in devices:
        device_id = device["devEui"]
        print(f"Fetching readings for {device['device_name']} ({device_id})")
        df = get_readings(token, device_id, start_date, end_date)
        params = {
            "device_name": device["device_name"],
            "location": device["location"],
            "df": df,
        }
        data_list.append(params)

    return data_list


def data_processing(data_list):
    """Process the fetched data for analysis.

    Args:
        data_list (list): List of dictionaries containing device data.
    Each dictionary should have the keys 'device_name' and 'df' where 'df' is a DataFrame.

    Returns:
        dict: Processed dataframes for inside and outside sensors.
    The returned dictionary contains:
        - df_inside: DataFrame containing inside sensor data.
        - df_outside: DataFrame containing outside sensor data.
    """
    dfs_inside = [x["df"] for x in data_list if x["location"] != "Outside"]
    df_inside = pd.concat(dfs_inside, axis=1)
    df_inside["SOLAR RADIATION"] = df_inside["LIGHT"].apply(
        lambda x: round(float(x) * 0.0079, 2)
    )
    df_inside = df_inside.drop(columns=["WIND DIRECTION", "LIGHT"])
    # ------------- Process Outside Data -------------
    df_outside = [data for data in data_list if data["location"] == "Outside"][0]["df"]

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


# TODO: Refactor this function to data remotely
def import_historical_data():
    """Import historical data from a CSV file."""
    project_path = env_global("project_path")
    data_path = "data/readings/final"
    folder_path = os.path.join(project_path, data_path)
    if not os.path.exists(folder_path):
        logger.error(f"Data folder '{folder_path}' does not exist.")
        return
    df_inside = pd.read_csv(
        f"{folder_path}/Inside.csv", parse_dates=["datetime"], index_col="datetime"
    )
    df_outside = pd.read_csv(
        f"{folder_path}/Outside.csv", parse_dates=["datetime"], index_col="datetime"
    )
    ans = [
        {"name": "Inside", "df": df_inside},
        {"name": "Outside", "df": df_outside},
    ]

    return ans


def append_data(df_live, df_import):
    """Append imported data to live data."""
    if df_live.empty:
        return df_import
    if df_import.empty:
        return df_live
    # Ensure both DataFrames have the same columns
    common_columns = df_live.columns.intersection(df_import.columns)
    df_live = df_live[common_columns]
    df_import = df_import[common_columns]
    dt_end = df_import.index.max()

    df_live = df_live[df_live.index > dt_end]

    # Append the imported data to the live data
    return pd.concat([df_live, df_import], axis=0).sort_index()


def current_data(data_live):
    data_import = import_historical_data()
    if not data_import:
        logger.warning("No historical data available.")
        return
    df_hist_inside = data_import[0]["df"]
    df_hist_outside = data_import[1]["df"]
    df_live_inside = data_live["df_inside"]
    df_live_outside = data_live["df_outside"]

    df_inside = append_data(df_live_inside, df_hist_inside)
    df_outside = append_data(df_live_outside, df_hist_outside)

    params = {
        "df_inside": df_inside,
        "df_outside": df_outside,
    }

    return params


def df_aggregate(df, interval):
    if interval == "hour":
        return df.resample("H").mean()
    elif interval == "day":
        return df.resample("D").mean()
    else:
        raise ValueError(f"Unsupported interval: {interval}")
