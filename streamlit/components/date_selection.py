import pandas as pd

import streamlit as st

with st.expander("Select Date Range:"):
    cols = st.columns(2)
    with cols[0]:
        start_date = st.date_input("Start Date", value=pd.to_datetime("today"))
    with cols[1]:
        end_date = st.date_input("End Date", value=pd.to_datetime("today"))
    cols = st.columns(2)
