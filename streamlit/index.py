import os

import pandas as pd
from loguru import logger
from matplotlib import pyplot as plt
from nviro_fetch.auth import authenticate

import streamlit as st
from common import date_formats, date_string
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


def intro():

    st.write("# Welcome to Streamlit! 👋")
    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.

        **👈 Select a demo from the dropdown on the left** to see some examples
        of what Streamlit can do!

        ### Want to learn more?

        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)

        ### See more complex demos

        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


def live():
    st.title("Live Data Stream")
    st.write("This page will display live data from the NViro API.")
    username = os.environ.get("NVIRO_USERNAME")
    password = os.environ.get("NVIRO_PASSWORD")
    st.sidebar.write(
        f"Logged in as: {username}"
        if username
        else "Not logged in. Please set NVIRO_USERNAME and NVIRO_PASSWORD environment variables."
    )

    st.sidebar.header("Inputs")

    sensor_list = env_global("sensor_list")
    sensor = st.sidebar.selectbox("Choose a sensor", sensor_list)

    # Use datetime_range_picker to create a datetime range picker
    with st.expander("Select Date Range:"):
        cols = st.columns(2)
        with cols[0]:
            start_date = st.date_input("Start Date", value=pd.to_datetime("today"))
        with cols[1]:
            end_date = st.date_input("End Date", value=pd.to_datetime("today"))
        # end_time = st.time_input("End Time", value=pd.to_datetime("now").time())
        # start_time = st.time_input("Start Time", value=pd.to_datetime("now").time())
    # start_date = start_date.strftime(date_formats["short"])
    # end_date = end_date.strftime(date_formats["short"])
    end_date = end_date + pd.Timedelta(days=1)  # Include the end date in the range
    start_date = date_string(start_date, "long")
    end_date = date_string(end_date, "long")
    # start_date = date_string(start_date, "long")

    st.sidebar.button(
        "Fetch Data",
        key="btn_scrape",
    )
    if "data" not in st.session_state:
        st.session_state.data = None
    # Fetch and display live data
    if st.session_state.get("btn_scrape"):
        st.sidebar.write(f"Fetching data from {start_date} to {end_date}...")
        try:
            data = fetch_data(start_date, end_date)
            if not data:
                st.sidebar.write("No data available for the selected date range.")
            else:
                st.sidebar.write("Data fetched successfully.")
        except Exception as e:
            st.sidebar.write(f"Error fetching data: {e}")
        finally:
            st.session_state.data = data

    if st.session_state.data:
        data = st.session_state.data
        plot_data(data, sensor)

    # df = fetch_data()
    # if df.empty:
    #     st.write("No data available.")
    # else:
    #     st.dataframe(df)
    #     st.line_chart(df)


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


page_names_to_funcs = {
    "Live": live,
    "Home": intro,
    "Historical Demo": page_historical,
}
# page_historical()

st.set_page_config(layout="wide")

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
