import datetime

import pandas as pd

import streamlit as st
from chill_units import calculate_utah_chill_units
from env import env_global


def format_data(data, type: str, start_datetime, end_datetime):
    sensor = "TEMPERATURE"
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

    df = df[[type]]

    df_hour = df.resample("H").mean()
    df_hour["chill"] = df_hour[type].apply(lambda x: calculate_utah_chill_units(x))

    df_chill = df_hour[["chill"]].resample("D").sum()

    df_chill["chill_cum"] = df_chill["chill"].cumsum()

    return df_chill


def create_daily_chill(df):
    """Create a DataFrame with daily chill data."""
    df_day = df.resample("D").sum()
    df_chill = df_day[["chill"]].copy()
    df_chill["chill_cum"] = df_chill["chill"].cumsum()
    return df_chill


def plot_chill_data(df_chill):
    """Plot the chill data with improved appearance."""
    import matplotlib.pyplot as plt

    st.subheader("Chill Data")

    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(
        df_chill.index,
        df_chill["chill"],
        label="Daily Chill",
        color="tab:blue",
        marker="o",
    )
    ax1.set_title("Daily Chill Units")
    ax1.set_ylabel("Daily Chill Units", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    ax1.set_xlabel("Date")
    ax1.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    ax2 = ax1.twinx()
    ax2.plot(
        df_chill.index,
        df_chill["chill_cum"],
        label="Cumulative Chill",
        color="tab:orange",
        marker="s",
    )
    ax2.set_ylabel("Cumulative Chill Units", color="tab:orange")
    ax2.tick_params(axis="y", labelcolor="tab:orange")

    fig.tight_layout()
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    st.pyplot(fig)

    st.write("Chill data is calculated based on the selected temperature type.")


def plot_hourly_chill(df):
    """Plot the hourly chill data."""
    import matplotlib.pyplot as plt

    # fig, ax = plt.subplots()
    # # df.plot(figsize=(12, 5), title=f"{sensor} Readings Inside vs Outside")
    # ax.set_title(f"{sensor}")
    # ax.set_xlabel("Datetime")
    # ax.set_ylabel(sensor)
    # df.plot(ax=ax)
    # df_inside[sensor].plot(ax=ax, label="Inside", color="blue")
    # df_outside[sensor].plot(ax=ax, label="Outside", color="orange")
    # ax.grid(True)
    # st.pyplot(fig)

    df["chill_cum"] = df["chill"].cumsum()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        df.index,
        df["chill_cum"],
        label="Hourly Chill",
        color="tab:green",
    )
    ax.set_title("Hourly Chill Units")
    ax.set_xlabel("Datetime")
    ax.set_ylabel("Chill Units")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


def plot_daily_chill(df):
    """Plot the hourly chill data."""
    import matplotlib.pyplot as plt

    df_chill = create_daily_chill(df)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        df_chill.index,
        df_chill["chill_cum"],
        label="Daily Chill Cumulative",
        color="tab:green",
        marker="o",
    )
    ax.plot(
        df_chill.index,
        df_chill["chill"],
        label="Daily Chill",
        color="tab:blue",
        marker="o",
    )
    ax.set_title("Daily Chill Units")
    ax.set_xlabel("Datetime")
    ax.set_ylabel("Chill Units")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


def display_hourly(df):

    with st.expander("Hourly Chill", expanded=False):
        df = df.rename(
            columns={
                "chill": "Hourly Chill",
                "chill_cum": "Cumulative Chill",
                "temp": "Temperature",
            }
        )
        st.dataframe(df)


def display_daily(df):
    df_chill = create_daily_chill(df)

    with st.expander("Daily Chill", expanded=False):
        df_chill = df_chill.rename(
            columns={
                "chill": "Daily Chill",
                "chill_cum": "Cumulative Chill",
            }
        )
        st.dataframe(df_chill)


@st.cache_data()
def load_data(file):
    df = pd.read_csv(file, parse_dates=["datetime"], index_col="datetime")
    return df


def filter_date(df, data_start_date=None, data_end_date=None):
    # Retrieve the start and end dates from session state or set default values
    if not data_start_date:
        data_start_date = pd.to_datetime("today")
    if not data_end_date:
        data_end_date = pd.to_datetime("today")

    # Use datetime_range_picker to create a datetime range picker
    with st.expander("Filter Date:"):
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

    df = df[start_datetime:end_datetime]
    df_hour = df.resample("H").mean()
    df_hour["chill"] = df_hour["TEMPERATURE"].apply(
        lambda x: calculate_utah_chill_units(x)
    )
    df_hour["chill_cum"] = df_hour["chill"].cumsum()

    return df_hour


def filter_columns(df):

    columns = df.columns.tolist()
    selected_column = st.selectbox(
        "Select a column to display",
        options=columns,
        index=0,
    )
    if selected_column:
        value_min = df[selected_column].min()
        value_max = df[selected_column].max()
        input_min, input_max = st.slider(
            f"Filter {selected_column}",
            min_value=value_min,
            max_value=value_max,
            value=(value_min, value_max),
        )
        df = df[(df[selected_column] >= input_min) & (df[selected_column] <= input_max)]
        return df


def ui_metrics(df):
    """Display UI metrics for the chill page."""
    last_row = df["chill_cum"].tail(1)
    # Count missing values in 'colB'
    values_missing = df["chill"].isnull().sum()
    values_total = df["chill"].count()
    percent_missing = (values_missing / values_total) * 100
    with st.expander("Metrics:", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            st.metric(
                "Last Chill Cumulative",
                f"{last_row.values[0]:.2f}",
                delta=f"{last_row.values[0] - df['chill_cum'].iloc[-2]:.2f}",
            )
        with cols[1]:
            st.metric("Missing Hours", f"{percent_missing:.2f}%")


def apply_custom_css():
    css = """
        <style>
            [data-testid='stFileUploader'] {
                width: max-content;
            }
            [data-testid='stFileUploader'] section {
                padding: 0;
                float: left;
            }
            [data-testid='stFileUploader'] section > input + div {
                display: none;
            }
            [data-testid='stFileUploader'] section + div {
                float: right;
                padding-top: 0;
            }
        </style>
        """

    st.markdown(css, unsafe_allow_html=True)


def chill():
    apply_custom_css()
    st.title("Chill Page")
    debug = st.sidebar.checkbox("Debug Mode", value=False)

    view = st.sidebar.selectbox(
        "View",
        ["Chill Hourly", "Chill Daily"],
        index=0,
    )

    location = st.sidebar.selectbox(
        "Location",
        ["Outside", "Inside"],
        index=0,
    )

    # You can add more content here, such as images, text, or interactive elements.

    uploaded_file = st.sidebar.file_uploader("Choose a file")

    if not debug:
        # if uploaded_file is not None:
        #     dataframe = load_data(uploaded_file)
        #     st.write(f"File uploaded: {uploaded_file}")
        #     st.session_state.import_data = dataframe

        if st.session_state.data:
            data = st.session_state.data
            if location == "Outside":
                df = data["df_outside"]
            else:
                df = data["df_inside"]
            data_start_date = df.index.min()
            data_end_date = df.index.max()
            cols = st.columns(2)
            with cols[1]:
                df_filtered = filter_date(df, data_start_date, data_end_date)
                with st.expander("Filter Columns", expanded=False):
                    df_filtered = filter_columns(df_filtered)
            with cols[0]:
                ui_metrics(df_filtered)

            if view == "Chill Hourly":
                st.subheader("Hourly Chill")
                with st.expander("Plot", expanded=True):
                    plot_hourly_chill(df_filtered)
                display_hourly(df_filtered)
            elif view == "Chill Daily":
                st.subheader("Daily Chill")
                with st.expander("Plot", expanded=False):
                    plot_daily_chill(df_filtered)
                display_daily(df_filtered)
        else:
            st.write("No data available. Please upload a file or fetch data.")
    else:
        project_path = env_global("project_path")
        file_example = "data/readings/chill/Outside_Chill_2025-06-24.csv"
        file = f"{project_path}/{file_example}"
        # For debugging, you can use a sample DataFrame
        st.session_state.import_data = load_data(file)
    if not st.session_state.import_data.empty:
        df = st.session_state.import_data
        # data_start_date=None, data_end_date=None
        data_start_date = df.index.min()
        data_end_date = df.index.max()
        cols = st.columns(2)
        with cols[1]:
            df_filtered = filter_date(df, data_start_date, data_end_date)
            with st.expander("Filter Columns", expanded=False):
                df_filtered = filter_columns(df_filtered)
        with cols[0]:
            ui_metrics(df_filtered)

        if view == "Chill Hourly":
            st.subheader("Hourly Chill")
            with st.expander("Plot", expanded=True):
                plot_hourly_chill(df_filtered)
            display_hourly(df_filtered)
        elif view == "Chill Daily":
            st.subheader("Daily Chill")
            with st.expander("Plot", expanded=False):
                plot_daily_chill(df_filtered)
            display_daily(df_filtered)

    # else:
    #     st.write("No data available. Please upload a file or fetch data.")


chill()
