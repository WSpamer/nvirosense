import os
from datetime import datetime

import pandas as pd
from loguru import logger

from common import extract_date
from env import env_global

"""
This module provides functions to list CSV files in a directory, extract dates from file names, find the latest file based on date, and import readings from the latest file.
"""


def list_files_os(folder_path, is_print=False):
    """Lists all CSV files in the specified folder."""
    if not os.path.exists(folder_path):
        logger.error(f"Folder path '{folder_path}' does not exist.")
        return []
    if not os.path.isdir(folder_path):
        logger.error(f"Path '{folder_path}' is not a directory.")
        return []
    files = os.listdir(folder_path)
    ans = [file for file in files if file.endswith(".csv")]
    if is_print:
        logger.info(f"Listing files in folder: {folder_path}")
        for file in ans:
            print(f"Found CSV file: {file}")
    return ans


def find_file(folder_path, file_name="willow_creek_weather"):
    """Finds the matching file in the specified folder."""
    files = list_files_os(folder_path)
    if not files:
        logger.warning("No CSV files found in the specified folder.")
        raise ValueError("No CSV files found in the specified folder.")

    # Find the file that matches the device name
    matching_files = [
        file for file in files if file_name in file and file.endswith(".csv")
    ]
    if not matching_files:
        logger.warning(
            f"No files found for device '{file_name}' in the specified folder."
        )
        raise ValueError(
            f"No files found for device '{file_name}' in the specified folder."
        )
    file = matching_files[0]  # Assuming we take the first match
    logger.info(f"Found file: {file} for device: {file_name}")
    return file


def fix_index(df, index_col="dt"):
    """Fixes the index of the DataFrame based on the specified column."""
    if index_col not in df.columns:
        logger.error(f"Column '{index_col}' not found in DataFrame.")
        raise ValueError(f"Column '{index_col}' not found in DataFrame.")
    # Convert the index column to datetime if it's not already
    df[index_col] = pd.to_datetime(df[index_col], errors="coerce")
    if df[index_col].isnull().any():
        logger.error(f"Column '{index_col}' contains invalid datetime values.")
        raise ValueError(f"Column '{index_col}' contains invalid datetime values.")
    # Set the index to the specified column
    df = df.set_index(index_col)
    return df


def parse_csv_file_info(data_path):
    folder_files = list_files_os(data_path)
    file_details = []
    for file in folder_files:
        file = file.replace(".csv", "")
        date = extract_date(file)
        file_name = file.replace(date, "").replace("_", "")
        params = {
            "file_name": file_name,
            "date": date,
            "datetime": pd.to_datetime(date, errors="coerce"),
            "file_path": os.path.join(data_path, file + ".csv"),
        }
        file_details.append(params)
    return file_details


def get_latest_file(data_path, file_name="Outside"):
    logger.info(f"Getting latest file for device: {file_name} in path: {data_path}")
    if not os.path.exists(data_path):
        logger.error(f"Data path '{data_path}' does not exist.")
        raise ValueError(f"Data path '{data_path}' does not exist.")
    if not os.path.isdir(data_path):
        logger.error(f"Path '{data_path}' is not a directory.")
        raise ValueError(f"Path '{data_path}' is not a directory.")
    file_details = parse_csv_file_info(data_path)
    file_match = [file for file in file_details if file_name in file["file_name"]]
    logger.info(f"File match: {file_match}")
    if file_match:
        logger.info(f"Found {len(file_match)} matching files for device: {file_name}")
        file_latest = max(file_match, key=lambda x: x["datetime"])
        return file_latest
    else:
        logger.warning(f"No matching files found for device: {file_name}")
        raise ValueError(f"No matching files found for device: {file_name}")


def export_dataframe(df, folder_path, filename):
    """Exports the readings DataFrame to a CSV file."""
    project_path = env_global("project_path")
    file_path = os.path.join(project_path, folder_path)
    end_date = df.index.max()
    date_end = pd.to_datetime(end_date).strftime("%Y-%m-%d")
    path = os.path.join(
        file_path, f"{filename}_{date_end.replace(' ', '_').replace(':', '-')}.csv"
    )
    df.to_csv(path)


def import_dataframe(file_name, folder_path="data/readings/current"):
    """Imports a CSV file into a DataFrame."""
    project_path = env_global("project_path")
    data_path = os.path.join(project_path, folder_path)
    logger.info(f"Importing data from file: {file_name} in path: {data_path}")
    file = get_latest_file(data_path, file_name=file_name)
    file_path = file["file_path"]
    df = pd.read_csv(file_path, parse_dates=["datetime"], index_col="datetime")
    return df


# Example usage:
# folder_path = "../data"  # Replace with the actual path
# files = list_files_os(folder_path)


# def file_date(file_name, device_name="willow_creek_weather"):
#     """Extracts the date from the file name."""
#     logger.info(f"Extracting date from file name: {file_name}")
#     logger.info(f"Extracting date for device name: {device_name}")
#     date_str = file_name.replace(f"{device_name}_", "").replace(".csv", "")
#     try:
#         date = datetime.strptime(date_str, "%Y-%m-%d")
#         logger.debug(f"Extracted date from file name '{file_name}': {date}")
#     except ValueError:
#         logger.error(
#             f"Date format '{date_str}' in file name '{file_name}' is incorrect."
#         )
#         return None
#     return date


# def latest_file(folder_path, device_name="willow_creek_weather"):
#     """Finds the latest file in the specified folder."""
#     files = list_files_os(folder_path)
#     if not files:
#         logger.warning("No CSV files found in the specified folder.")
#         raise ValueError("No CSV files found in the specified folder.")

#     # Filter out files where file_date returns None
#     valid_files = [
#         file for file in files if file_date(file, device_name=device_name) is not None
#     ]
#     if not valid_files:
#         logger.warning("No valid CSV files with correct date format found.")
#         raise ValueError("No valid CSV files with correct date format found.")

#     latest = max(valid_files, key=file_date)  # type: ignore
#     logger.info(f"Latest file: {latest}")
#     return latest
