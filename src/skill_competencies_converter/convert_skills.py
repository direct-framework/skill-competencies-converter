import argparse
import csv
import importlib
import os
import sys
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


def parse_framework(csv_data):
    output = {
        'categories': []
    }

    reader = csv.reader(csv_data.splitlines())
    headers = next(reader)

    def find_idx(list, str):
        for i, x in enumerate(list):
            if str in x.lower():
                return i
        raise Exception(f"Couldn't find {str} in {list}")

    desc_idx = find_idx(headers, "desc")
    tools_idx = find_idx(headers, "tools")
    training_idx = find_idx(headers, "training")

    for row in reader:
        if not is_blank(row[0]):
            category = {
                'title': row[0],
                'description': row[desc_idx],
                'subcategories': []
            }
            output['categories'].append(category)
        if not is_blank(row[1]):
            subcategory = {
                'title': row[1],
                'description': row[desc_idx],
                'skills': []
            }
            category['subcategories'].append(subcategory)
        if not is_blank(row[2]):
            skill = {
                'title': row[2],
                'description': row[desc_idx],
                'tools_languages_methods_behaviours': [],  # row[tools_idx], - currently set to empty list
                'training_resources': []  # row[training_idx] - currently set to empty list
            }
            subcategory['skills'].append(skill)
        else:
            continue

    return output


def get_parser():
    """
    Parse input arguments, and return the parser.
    """
    example_text = """Examples:

    %(prog)s <csv_file>
    %(prog)s <google_sheet_id> <sheet_name>"""
    parser = argparse.ArgumentParser(
        description="Convert skills CSV or Google Sheet to YAML/JSON.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        help="Either CSV file path or Google Sheet ID and sheet name"
    )
    parser.add_argument(
        "--output-path",
        default="data.json",
        help="Output filepath. Default: ./data.json"
    )
    parser.add_argument(
        "--print-output",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Print output to stdout"
    )

    return parser


def main():
    """
    Main conversion function.
    """
    parser = get_parser()
    args = parser.parse_args()

    if len(args.inputs) == 1:
        filename = args.inputs[0]
        csv_content = read_csv_from_file(filename)
    elif len(args.inputs) == 2:
        sheet_id = args.inputs[0]
        sheet_name = args.inputs[1]
        csv_content = read_csv_from_url(sheet_id, sheet_name)
    else:
        parser.print_help()
        sys.exit(1)

    output = parse_framework(csv_content)

    # Get the output extension (whether JSON or yml)
    _, ext = os.path.splitext(args.output_path)
    ext = ext.lower().lstrip(".")
    if ext == "yml":
        ext = "yaml"
    if ext not in SUPPORTED_OUTPUTS:
        supported_extensions = [fmt for fmt in SUPPORTED_OUTPUTS.keys()]
        print(f"Unsupported output file extension. Use one of {supported_extensions}")
        exit(1)

    # Call the relevant output function to output to either JSON/yml
    # At this time, either `save_json` or `save_yaml`
    module_name, func_name = SUPPORTED_OUTPUTS[ext]
    module = importlib.import_module(module_name)
    save_func = getattr(module, func_name)
    save_func(output, args.output_path, args.print_output)


if __name__ == "__main__":
    main()
