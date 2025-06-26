import datetime

import pandas as pd

import streamlit as st


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
