import os
from datetime import datetime

import pandas as pd
from loguru import logger

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


def find_file(folder_path, device_name="willow_creek_weather"):
    """Finds the matching file in the specified folder."""
    files = list_files_os(folder_path)
    if not files:
        logger.warning("No CSV files found in the specified folder.")
        raise ValueError("No CSV files found in the specified folder.")

    # Find the file that matches the device name
    matching_files = [
        file for file in files if device_name in file and file.endswith(".csv")
    ]
    if not matching_files:
        logger.warning(
            f"No files found for device '{device_name}' in the specified folder."
        )
        raise ValueError(
            f"No files found for device '{device_name}' in the specified folder."
        )
    file = matching_files[0]  # Assuming we take the first match
    logger.info(f"Found file: {file} for device: {device_name}")
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


# Example usage:
# folder_path = "../data"  # Replace with the actual path
# files = list_files_os(folder_path)
