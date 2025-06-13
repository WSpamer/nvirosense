import json


def read_json(file_path):
    """
    Reads settings from a JSON file.
    Args:
        file_path (str): The path to the JSON file.
    Returns:
        dict: Settings loaded from the JSON file.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def append_to_json(filename, new_data):
    """
    Appends new data to a JSON file. If the file does not exist, it creates it.
    If the file contains a JSON object, it updates it with the new data.
    If the file contains a JSON array, it appends the new data to the array.
    Args:
        filename (str): The path to the JSON file.
        new_data (dict or list): The data to append or update in the JSON file.
    """
    try:
        with open(filename, "r+") as file:
            file_data = json.load(file)
            if isinstance(file_data, list):
                file_data.append(new_data)
            elif isinstance(file_data, dict):
                file_data.update(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    except FileNotFoundError:
        with open(filename, "w") as file:
            json.dump(
                [new_data] if not isinstance(new_data, dict) else new_data,
                file,
                indent=4,
            )
    except json.JSONDecodeError:
        with open(filename, "w") as file:
            json.dump(
                [new_data] if not isinstance(new_data, dict) else new_data,
                file,
                indent=4,
            )


# Example usage:
# filename = "data.json"
# new_data = {"item": "New Item", "price": 19.99}
# append_to_json(filename, new_data)
