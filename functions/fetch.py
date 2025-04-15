import requests
import json
from functions.auth import log_response, parse_json


# Function to fetch devices using JWT token
def fetch_devices(jwt_token, is_print=False):
    DEVICES_ENDPOINT = "https://ant.nvirosense.com/api/v1/devices"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }
    if is_print:
        print(f"[INFO] Fetching devices from {DEVICES_ENDPOINT}...")
    response = requests.get(DEVICES_ENDPOINT, headers=headers)
    if is_print:
        log_response(response, "Fetch Devices")
    if response.status_code == 200:
        devices = parse_json(response.text)
        if is_print:
            print("[SUCCESS] Devices fetched successfully!")
        if is_print:
            print(json.dumps(devices, indent=4))
        return devices
    else:
        print(f"[ERROR] Failed to fetch devices! Status: {response.status_code}")
        return []


def fetch_device_sensors(jwt_token, device, is_print=False):
    DEVICES_ENDPOINT = "https://ant.nvirosense.com/api/v1/devices"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }
    deviceId = device["devEui"]
    url_endpoint = f"{DEVICES_ENDPOINT}/{deviceId}/sensors"
    if is_print:
        print(f"[INFO] Fetching devices from {url_endpoint}...")
    response = requests.get(url_endpoint, headers=headers)
    if is_print:
        log_response(response, "Fetch Devices")
    if response.status_code == 200:
        devices = parse_json(response.text)
        if is_print:
            print("[SUCCESS] Devices fetched successfully!")
        if is_print:
            print(json.dumps(devices, indent=4))
        return devices["sensors"]
    else:
        print(f"[ERROR] Failed to fetch devices! Status: {response.status_code}")
        return {}
