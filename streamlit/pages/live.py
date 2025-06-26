import datetime
import os

import pandas as pd
from matplotlib import pyplot as plt
from nviro_fetch.auth import authenticate

import streamlit as st
from common import date_string
from data import data_processing, load_data
from devices import check_and_load_devices
from env import env_global


@st.cache_data
def get_devices():
    devices = check_and_load_devices()
    df = pd.DataFrame(devices)
    return df


# @st.cache_data
def fetch_data(start_date: str, end_date: str) -> dict:
    """Fetch data from the NViro API and return it as a DataFrame."""
    token = authenticate()
    devices = get_devices()
    if devices.empty:
        st.write("No devices available. Please check your device configuration.")
        return dict()
    data_list = load_data(
        token=token,
        devices=devices.to_dict(orient="records"),
        start_date=start_date,
        end_date=end_date,
    )
    if not data_list:
        st.write("No data available for the selected date range.")
        return dict()
    # Assuming data_list is a list of dicts that can be converted to a DataFrame
    data = data_processing(data_list)

    return data


def plot_data(data, sensor: str, start_datetime, end_datetime):
    """Plot the data for a specific sensor."""
    df_inside = data["df_inside"]
    df_outside = data["df_outside"]

    if start_datetime and end_datetime:
        df_inside = df_inside[start_datetime:end_datetime]
        df_outside = df_outside[start_datetime:end_datetime]
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


def filter_data():
    # Retrieve the start and end dates from session state or set default values
    if "data_start_date" in st.session_state:
        data_start_date = st.session_state.data_start_date
    else:
        data_start_date = pd.to_datetime("today")
    if "data_end_date" in st.session_state:
        data_end_date = st.session_state.data_end_date
    else:
        data_end_date = pd.to_datetime("today")

    # Use datetime_range_picker to create a datetime range picker
    with st.expander("Filter Data:"):
        cols = st.columns(2)
        with cols[0]:
            start_date = st.date_input(
                "Start Date",
                value=data_start_date,
                min_value=data_start_date,
                max_value=data_end_date,
            )
        with cols[1]:
            end_date = st.date_input(
                "End Date",
                value=data_end_date,
                min_value=data_start_date,
                max_value=data_end_date,
            )
        cols = st.columns(2)
        with cols[0]:
            start_time = st.time_input("Start Time", value=datetime.time(0, 0))
        with cols[1]:
            end_time = st.time_input("End Time", value=datetime.time(23, 59))
    start_datetime = f"{start_date} {start_time}"
    end_datetime = f"{end_date} {end_time}"

    start_datetime = pd.to_datetime(start_datetime, utc=True)
    end_datetime = pd.to_datetime(end_datetime, utc=True)

    return start_datetime, end_datetime


def live():

    st.sidebar.header("Inputs")

    sensor_list = env_global("sensor_list")
    sensor = st.sidebar.selectbox("Choose a sensor", sensor_list)

    # end_date = end_date + pd.Timedelta(days=1)  # Include the end date in the range
    # start_date = date_string(start_date, "long")
    # end_date = date_string(end_date, "long")
    # start_date = date_string(start_date, "long")
    start_datetime, end_datetime = filter_data()
    if st.session_state.data:
        data = st.session_state.data
        plot_data(data, sensor, start_datetime, end_datetime)


if not st.session_state.data:
    st.header("No data available. Please fetch data first.")
else:
    st.title("Live Data Stream")
    st.write("This page will display live data from the NViro API.")
    live()
