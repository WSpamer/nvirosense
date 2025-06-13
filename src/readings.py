import os

import pandas as pd
from loguru import logger
from nviro_fetch.data import get_device_readings

from src.files import find_file, fix_index


def readings_as_df(readings):
    df_readings = pd.DataFrame(readings)
    df_readings["datetime"] = pd.to_datetime(df_readings["datetime"], utc=True)
    df_readings = df_readings.drop_duplicates(subset=["datetime", "sensor_name"])
    df = df_readings.pivot(index="datetime", columns="sensor_name", values="value")
    return df


def get_readings(token, device_id, start_date, end_date):
    logger.info(
        f"Fetching readings for device {device_id} from {start_date} to {end_date}"
    )
    readings = get_device_readings(token, device_id, start_date, end_date)
    df = readings_as_df(readings)

    return df


def export_readings(path_data, df, device, end_date):
    """Exports the readings DataFrame to a CSV file."""
    device_name = device["device_name"].replace(" ", "_").lower()
    df['datetime'] = df.index
    date_end = pd.to_datetime(end_date).strftime("%Y-%m-%d")
    file_path = os.path.join(
        path_data, f"{device_name}_{date_end.replace(' ', '_').replace(':', '-')}.csv"
    )
    df.to_csv(file_path, index=False)


def import_readings(
    device_name, readings_directory="data/readings", type="raw"
):
    """import_readings _summary_

    Args:
        readings_directory (str, optional): _description_. Defaults to "data/readings".
        type (str, optional): _description_. Defaults to 'raw'.
        index_fix (bool, optional): _description_. Defaults to True.

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    if type not in ["raw", "cleaned"]:
        logger.error(f"Invalid type '{type}' specified. Must be 'raw' or 'cleaned'.")
        raise ValueError(
            f"Invalid type '{type}' specified. Must be 'raw' or 'cleaned'."
        )
    folder_path = os.path.join(readings_directory, type)
    file = find_file(folder_path, device_name=device_name)
    if file:
        logger.info(f"Importing readings from file: {file}")
    else:
        logger.warning("No valid file found for importing readings.")
    file_path = os.path.join(folder_path, file) if file else None
    if file_path and os.path.exists(file_path):
        df = pd.read_csv(file_path)
        index_col = "datetime"
        df[index_col] = pd.to_datetime(df[index_col], errors="coerce")
        df.set_index(index_col, inplace=True)
        df['dt'] = df.index
        logger.info(f"Readings imported successfully from {file_path}")
        return df
    else:
        logger.error(f"File {file_path} does not exist or is not valid.")
        raise ValueError(f"File {file_path} does not exist or is not valid.")


def calculate_time_difference(df_col):
    """
    Calculate the time difference between consecutive readings in minutes.
    """
    ans = abs(df_col.diff().bfill().dt.total_seconds() / 60)

    return ans.astype(int)
