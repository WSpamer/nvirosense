import pandas as pd
import requests
import json


def fetch_request(endpoint):
    baseUrl = "http://127.0.0.1:8000/api"
    url = f"{baseUrl}/{endpoint}"
    print(f"[INFO] Fetching devices from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        devices = json.loads(response.text)
        print("[SUCCESS] Devices fetched successfully!")
        return devices
    else:
        print(f"[ERROR] Failed to fetch devices! Status: {response.status_code}")
        return []


def fetch_data(endpoint):
    df = pd.DataFrame(fetch_request(endpoint))
    return df
