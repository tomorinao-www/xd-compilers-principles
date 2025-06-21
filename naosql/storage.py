# storage.py
import json
import os
from catalog import get_current_db

def get_table_path(table_name):
    return os.path.join(get_current_db(), f"{table_name}.json")

def load_table(table_name):
    path = get_table_path(table_name)
    with open(path) as f:
        return json.load(f)

def save_table(table_name, data):
    path = get_table_path(table_name)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
