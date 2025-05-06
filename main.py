from functions.data import get_nviro_data
from functions.auth import authenticate

token = authenticate()
data = get_nviro_data(token)

for item in data:
    name = item["name"]
    df = item["data"]
    print(f"Data for {name}:")
    print(df)
    print("\n")
