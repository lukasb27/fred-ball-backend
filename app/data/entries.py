import json

def get_entries():
    with open("diary_entries.json", "r") as file:
        data = json.load(file)
    return data