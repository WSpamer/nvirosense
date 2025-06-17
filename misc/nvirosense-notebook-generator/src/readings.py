from datetime import datetime
import pandas as pd
import os

def import_readings(device_name):
    # Function to import readings for a specific device
    path = os.path.join("data", "readings", f"{device_name}.csv")
    return pd.read_csv(path, parse_dates=["dt"])

def export_readings(path_cleaned, df_final, device, end_date):
    # Function to export cleaned readings to a specified path
    if not os.path.exists(path_cleaned):
        os.makedirs(path_cleaned)
    output_file = os.path.join(path_cleaned, f"{device['device_name'].replace(' ', '_').lower()}_cleaned.csv")
    df_final.to_csv(output_file, index=False)
    print(f"Exported cleaned readings to {output_file} with end date {end_date}")

def calculate_time_difference(dt_series):
    # Function to calculate time differences between consecutive readings
    return dt_series.diff().dt.total_seconds() / 60  # Returns difference in minutes