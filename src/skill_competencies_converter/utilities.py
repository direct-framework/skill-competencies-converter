import urllib.request

# Dynamically figure out import (if package is installed, or this script is run directly)
if __package__:
    module_name = f"{__package__}.save"
else:
    module_name = "save"

# Define the output formats supported, and the relevant function calls.
SUPPORTED_OUTPUTS = {
    "yaml": (module_name, "save_yaml"),
    "json": (module_name, "save_json"),
}


def is_blank(val):
    return val is None or val.strip() == ''


def read_csv_from_url(sheet_id, sheet_name):
    sheet_name_encoded = urllib.parse.quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name_encoded}"
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')


def read_csv_from_file(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        return f.read()


def find_idx(list, str):
    for i, x in enumerate(list):
        if str.lower() in x.lower():
            return i
    raise Exception(f"Couldn't find '{str}' in {list}")