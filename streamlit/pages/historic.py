import pandas as pd
from loguru import logger
from matplotlib import pyplot as plt

import streamlit as st
from devices import check_and_load_devices


@st.cache_data
def get_devices():
    devices = check_and_load_devices()
    df = pd.DataFrame(devices)
    return df


def plot_data(data, sensor: str):
    """Plot the data for a specific sensor."""
    df_inside = data["df_inside"]
    df_outside = data["df_outside"]
    if sensor not in df_inside.columns or sensor not in df_outside.columns:
        st.write(f"Sensor '{sensor}' not found in the data.")
        return

    s1 = df_inside[sensor]
    s2 = df_outside[sensor]
    df = pd.concat([s1, s2], axis=1)
    df.columns = ["Inside", "Outside"]
    df.plot(figsize=(12, 5), title=f"Readings: {sensor}")

    st.write(f"Data for sensor: {sensor}")
    # st.dataframe(df)
    # st.line_chart(df)
    fig, ax = plt.subplots()
    # df.plot(figsize=(12, 5), title=f"{sensor} Readings Inside vs Outside")
    ax.set_title(f"{sensor}")
    ax.set_xlabel("Datetime")
    ax.set_ylabel(sensor)
    df.plot(ax=ax)
    df_inside[sensor].plot(ax=ax, label="Inside", color="blue")
    df_outside[sensor].plot(ax=ax, label="Outside", color="orange")
    ax.grid(True)
    st.pyplot(fig)


def format_data(filename: str = "Inside.csv") -> pd.DataFrame:
    """Read data from a CSV file and return it as a DataFrame."""
    df = pd.read_csv(f"data/readings/final/{filename}.csv")
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df.set_index("datetime", inplace=True, drop=True)
    return df


def df_sensor(
    sensor: str, df_inside: pd.DataFrame, df_outside: pd.DataFrame
) -> pd.DataFrame:
    """Return a DataFrame with the selected sensor data from inside and outside."""
    if sensor not in df_inside.columns or sensor not in df_outside.columns:
        raise ValueError(f"Sensor '{sensor}' not found in the data.")

    df_sensor = pd.DataFrame(
        {"Inside": df_inside[sensor], "Outside": df_outside[sensor]}
    )
    return df_sensor


@st.cache_data
def import_device_records():
    """Load data from CSV files and return DataFrames."""
    df_inside = format_data("Inside")
    df_outside = format_data("Outside")
    return df_inside, df_outside


def page_historical():
    st.title("Device Selection App")
    st.write("Select devices from the list below:")

    # Load devices and create a multiselect widget
    st.sidebar.header("Inputs")
    df = get_devices()
    df_inside, df_outside = import_device_records()
    sensor_list = list(df_inside.columns)
    sensor_list = [
        sensor for sensor in sensor_list if sensor not in ["datetime.1", "datetime.2"]
    ]
    sensor = st.sidebar.selectbox("Choose sensors", sensor_list)

    df = df_sensor(sensor, df_inside, df_outside)
    st.write(f"Data for sensor: {sensor}")
    # st.dataframe(df)
    # st.line_chart(df)
    fig, ax = plt.subplots()
    # df.plot(figsize=(12, 5), title=f"{sensor} Readings Inside vs Outside")
    ax.set_title(f"{sensor} Readings Inside vs Outside")
    ax.set_xlabel("Datetime")
    ax.set_ylabel(sensor)
    df.plot(ax=ax)
    df_inside[sensor].plot(ax=ax, label="Inside", color="blue")
    df_outside[sensor].plot(ax=ax, label="Outside", color="orange")
    ax.grid(True)
    st.pyplot(fig)


page_historical()
