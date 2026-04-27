import os
import json

def ensure_dir(directory_path):
    # Creates directories recursively if they don't exist
    os.makedirs(directory_path, exist_ok=True)

def load_json(filepath):
    # Reads a JSON file and returns the dictionary
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing JSON file: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(filepath, data):
    # Writes a dictionary to a JSON file with pretty formatting
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def read_file(filepath):
    # Reads a generic text file
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing file: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    # Writes string content to a file
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)