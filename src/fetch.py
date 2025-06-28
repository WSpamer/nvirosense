import pandas as pd
from loguru import logger
from nviro_fetch.auth import authenticate

from data import data_processing, load_data
from devices import check_and_load_devices


# TODO: Update to fetch devices from the API if not available locally
def get_devices():
    devices = check_and_load_devices()
    df = pd.DataFrame(devices)
    return df


def fetch_data(start_date: str, end_date: str) -> dict:
    """Fetch data from the NViro API and return it as a DataFrame."""
    token = authenticate()
    devices = get_devices()
    if devices.empty:
        logger.warning("No devices available. Please check your device configuration.")
        return dict()
    data_list = load_data(
        token=token,
        devices=devices.to_dict(orient="records"),
        start_date=start_date,
        end_date=end_date,
    )
    if not data_list:
        logger.warning("No data available for the selected date range.")
        return dict()
    # Assuming data_list is a list of dicts that can be converted to a DataFrame
    data = data_processing(data_list)

    return data
