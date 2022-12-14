
import json

def read_json(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)


def write_json(data, file_name):
    with open(file_name, 'w') as w:
        json.dump(data, w, indent=2)


