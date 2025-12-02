import json
import os 
def get_entries():
    # Get the directory where the current file lives
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "diary_entries.json")

    with open(file_path, "r") as file:
        data = json.load(file)
    return data