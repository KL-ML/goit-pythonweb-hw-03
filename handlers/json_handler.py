
import json
from datetime import datetime


def read_json_file():
    file_path = "./storage/data.json"
    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read().strip()  # Remove leading/trailing whitespace

    if raw:
        try:
            file_data = json.loads(raw)
        except json.JSONDecodeError as e:
            print("JSON error:", e)
            file_data = {}
    else:
        print("File is empty.")
        file_data = {}
    return file_data


def update_data_json(data):

    # Path to your JSON file
    file_path = "./storage/data.json"
    timestamp = datetime.now().isoformat(sep=" ", timespec="microseconds")

    # New entry
    new_entry = {timestamp: {"username": data["username"], "message": data["message"]}}

    file_data = read_json_file()

    # Update and write back to file
    # file_data.update(new_entry)
    file_data[timestamp] = new_entry[timestamp]

    with open(file_path, "w") as f:
        json.dump(file_data, f, indent=2)
