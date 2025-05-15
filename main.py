from nviro_data.data import get_nviro_data
from nviro_data.auth import authenticate
from nviro_data.readings import fetch_readings


def get_data(token):
    data = get_nviro_data(token)
    return data


def print_data(data):
    for item in data:
        name = item["name"]
        df = item["data"]
        print(f"Data for {name}:")
        print(df)
        print("\n")


def get_readings(token, data):
    start_date = "2025-03-01T00:00:00"  # Start date in ISO8601 format
    end_date = "2025-03-24T23:59:59"
    limit = 1000000
    page = 1
    readings = fetch_readings(token, data, start_date, end_date, limit, page)
    return readings


def main():
    token = authenticate()
    data = get_data(token)
    print_data(data)
    # readings = get_readings(token, data)
    # print(readings)


main()
