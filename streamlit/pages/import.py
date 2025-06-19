import os

import pandas as pd
from matplotlib import pyplot as plt
from nviro_fetch.auth import authenticate

import streamlit as st
from common import date_string
from data import data_processing, load_data
from devices import check_and_load_devices
from env import env_global


def local_css(file_name):
    project_path = env_global("project_path")
    file_path = os.path.join(project_path, "streamlit", "pages", file_name)
    if not os.path.exists(file_path):
        st.error(f"CSS file '{file_name}' not found in {file_path}.")
        return
    print(f"Loading local CSS file: {file_name}")
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")


@st.cache_data
def get_devices():
    devices = check_and_load_devices()
    df = pd.DataFrame(devices)
    return df


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


def display_data(data):
    if not data:
        st.write("No data available.")
        return

    df_inside = data["df_inside"]
    df_outside = data["df_outside"]

    with st.expander("Inside Data", expanded=True):
        st.dataframe(df_inside)
    with st.expander("Outside Data", expanded=True):
        st.dataframe(df_outside)


def main():
    st.title("Import Data")
    st.write("This page is used to import data from the NViro API.")

    st.sidebar.header("Import Data Settings")
    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("today"))
    end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))
    # start_time = st.time_input("Start Time", value=pd.to_datetime("now").time())
    # end_time = st.time_input("End Time", value=pd.to_datetime("now").time())
    import_btn = st.sidebar.button(
        "Fetch Data",
        key="btn_scrape",
    )

    end_date = end_date + pd.Timedelta(days=1)  # Include the end date in the range
    start_date = date_string(start_date, "long")
    end_date = date_string(end_date, "long")

    if start_date:
        st.session_state.data_start_date = start_date
    if end_date:
        st.session_state.data_end_date = end_date

    # Fetch and display live data
    if st.session_state.get("btn_scrape"):
        try:
            msg_info = st.sidebar.info(
                f"Fetching data from \n {start_date} to {end_date}..."
            )
            data = fetch_data(start_date, end_date)
            msg_info.empty()  # Clear the loading message
            if not data:
                st.write("No data available for the selected date range.")
            else:
                st.write("Data fetched successfully.")
        except Exception as e:
            st.write(f"Error fetching data: {e}")
        finally:
            st.session_state.data = data
    if st.session_state.data:
        data = st.session_state.data
        display_data(data)


main()
