def calculate_utah_chill_units(temperature_celsius):
    """
    Calculates Utah Chill Units for a given hourly temperature in Celsius.

    Args:
        temperature_celsius (float): Hourly temperature in Celsius.

    Returns:
        float: The corresponding Utah Chill Units for that hour.
    """
    if temperature_celsius < 1.4:  # Below this temperature, no chill is accumulated
        return 0.0  # No chill
    # Define the ranges for chill accumulation
    elif 1.4 <= temperature_celsius <= 2.4:
        return 0.5  # Low chill
    elif 2.4 < temperature_celsius <= 9.1:
        return 1.0  # Optimal chill range
    elif 9.1 < temperature_celsius <= 12.4:
        return 0.5  # Reduced chill
    elif 12.5 <= temperature_celsius <= 15.9:
        return 0.0  # No chill
    elif 16.0 <= temperature_celsius <= 18.0:
        return -0.5  # Negative chill
    elif temperature_celsius > 18.0:
        return -1.0  # Strong negative chill
    else:
        return None


def create_hourly_chill(df, type="temperature"):
    """
    Create a DataFrame with hourly chill data based on the specified type.

    Args:
        df (pd.DataFrame): DataFrame containing hourly temperature data.
        type (str): Type of temperature data to use for chill calculation.

    Returns:
        pd.DataFrame: DataFrame with hourly chill data.
    """
    if type not in df.columns:
        raise ValueError(f"Type '{type}' not found in DataFrame columns.")

    df_hour = df.resample("H").mean()
    df_hour["chill"] = df_hour[type].apply(lambda x: calculate_utah_chill_units(x))

    return df_hour
