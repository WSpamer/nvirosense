import requests
import json
import time
import sys
import os
import dotenv


# Logging function (minimal logging)
def log_response(response, action):
    print("----------------------")
    print(f"[LOG] {action} Response: Status {response.status_code}")
    print("----------------------")


def parse_json(response_body):
    try:
        return json.loads(response_body)
    except json.JSONDecodeError:
        print("[ERROR] Response is not valid JSON!")
        sys.exit(1)


def fetch_login():
    JWT_ENDPOINT = "https://ant.nvirosense.com/api/v1/login"

    dotenv.load_dotenv()
    NVIRO_USERNAME = os.environ.get("NVIRO_USERNAME")
    NVIRO_PASSWORD = os.environ.get("NVIRO_PASSWORD")
    print(f"[INFO] Authenticating with {JWT_ENDPOINT}...")
    headers = {"Content-Type": "application/json"}
    payload = {
        "user": {
            "login": NVIRO_USERNAME,
            "password": NVIRO_PASSWORD,
        }
    }
    response = requests.post(JWT_ENDPOINT, json=payload, headers=headers)

    return response


def authenticate():

    retries = 0
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    while True:
        try:
            response = fetch_login()
            if response.status_code == 200:
                json_response = parse_json(response.text)
                print(json_response)
                jwt_token = json_response.get("token")
                print(jwt_token)
                if not jwt_token:
                    auth_header = response.headers.get("Authorization")
                    if auth_header:
                        parts = auth_header.split(" ")
                        if len(parts) >= 2:
                            jwt_token = parts[-1]
                            print(jwt_token)
                if jwt_token:
                    print("[SUCCESS] Authentication successful! Token received.")
                    return jwt_token
                else:
                    print("[ERROR] Failed to extract token from response!")
                    sys.exit(1)
            else:
                print("[ERROR] Authentication failed! Retrying...")
                raise Exception(f"Auth failed with status {response.status_code}")
        except Exception as e:
            retries += 1
            print(f"[WARN] Attempt {retries}/{MAX_RETRIES} failed: {e}")
            if retries < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                print(f"[FATAL] Authentication failed after {MAX_RETRIES} attempts.")
                sys.exit(1)
