from nviro_data.fetch import fetch_sensor_readings
from nviro_data.data import list_to_df
import pandas as pd


def get_df(data, name):
    df = [x["data"] for x in data if x["name"] == name][0]
    return df


def update_cols(df, name):
    df_new = df.copy(deep=True)
    df_new.rename(columns={"id": f"{name}_id"}, inplace=True)
    df_new.rename(columns={"name": f"{name}_name"}, inplace=True)
    return df_new


def fetch_device_readings(
    token, selected_device, df_sensors, start_date, end_date, limit, page
):
    readings = fetch_sensor_readings(
        token, selected_device, start_date, end_date, limit=limit, page=page
    )
    reading_list = []
    for reading in readings:
        datetime = reading["received_at"]
        sensors = reading["sensor_data"]
        for sensor in sensors:
            device_sensor = [
                device_sensor
                for device_sensor in df_sensors.to_dict("records")
                if device_sensor["name"] == sensor["sensor_name"]
            ][0]
            value = sensor["value"]
            params = {
                # 'device_id': device_id,
                "sensor_id": device_sensor["id"],
                "sensor_name": sensor["sensor_name"],
                "datetime": datetime,
                "value": value,
            }
            reading_list.append(params)
    df_readings = list_to_df(reading_list)
    return df_readings


def fetch_readings(token, data, start_date, end_date, limit, page):
    df_devices = get_df(data, "device")
    df_sensors = get_df(data, "sensor")
    reading_list = pd.DataFrame()
    for device in df_devices.to_dict("records"):
        device_readings = fetch_device_readings(
            token, device, df_sensors, start_date, end_date, limit, page
        )
        reading_list = pd.concat([reading_list, device_readings], ignore_index=True)
    return reading_list
