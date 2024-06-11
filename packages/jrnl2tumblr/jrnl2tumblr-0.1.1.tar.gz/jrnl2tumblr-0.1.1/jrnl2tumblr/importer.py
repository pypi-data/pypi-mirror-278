import json

def read_jrnl_file(jrnl_file_path):
    with open(jrnl_file_path, 'r') as file:
        entries = json.load(file)

    return entries
