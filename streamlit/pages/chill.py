import pandas as pd

import streamlit as st
from chill_units import calculate_utah_chill_units


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
        marker="o",
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
        st.dataframe(df)


def display_daily(df):
    df_chill = create_daily_chill(df)

    with st.expander("Daily Chill", expanded=False):
        st.dataframe(df_chill)


@st.cache_data()
def load_data(file):
    df = pd.read_csv(file, parse_dates=["datetime"], index_col="datetime")
    return df


def chill():
    st.title("Chill Page")

    # You can add more content here, such as images, text, or interactive elements.

    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        dataframe = load_data(uploaded_file)
        st.session_state.import_data = dataframe
    if not st.session_state.import_data.empty:
        df = st.session_state.import_data

        st.subheader("Hourly Chill")
        display_hourly(df)
        with st.expander("Plot", expanded=False):
            plot_hourly_chill(df)
        st.subheader("Daily Chill")
        display_daily(df)
        with st.expander("Plot", expanded=False):
            plot_daily_chill(df)
    else:
        st.write("No data available. Please upload a file.")

    # if st.session_state.data:
    #     data = st.session_state.data
    #     df_chill = format_data(
    #         data,
    #         type="Outside",
    #         start_datetime=st.session_state.data_start_date,
    #         end_datetime=st.session_state.data_end_date,
    #     )
    #     if df_chill is not None:
    #         plot_chill_data(df_chill)
    #     else:
    #         st.write("No chill data available for the selected date range.")


# if st.session_state.import_data.empty:
#     st.header("No data available. Please fetch data first.")
# else:
#     chill()
chill()
