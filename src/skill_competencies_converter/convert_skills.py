from utilities import *
import argparse
import csv
import importlib
import os
import sys


def parse_framework(csv_data):
    output = {
        'competency_domains': []
    }

    reader = csv.reader(csv_data.splitlines())
    headers = next(reader)

    desc_idx = find_idx(headers, "description")
    tools_languages_methodologies_idx = find_idx(headers, "tools_languages_methodologies")
    learning_resources_idx = find_idx(headers, "learning_resources")

    for row in reader:
        if not is_blank(row[0]):
            competency_domain = {
                'title': row[0],
                'description': row[desc_idx],
                'competencies': []
            }
            output['competency_domains'].append(competency_domain)
        if not is_blank(row[1]):
            competency = {
                'title': row[1],
                'description': row[desc_idx],
                'skills': []
            }
            competency_domain['competencies'].append(competency)
        if not is_blank(row[2]):
            skill = {
                'title': row[2],
                'description': row[desc_idx],
                'tools_languages_methodologies': row[tools_languages_methodologies_idx],
                'training_resources': row[learning_resources_idx]
            }
            competency['skills'].append(skill)
        else:
            continue

    return output


def get_parser():
    """
    Parse input arguments, and return the parser.
    """
    example_text = """Examples:

    %(prog)s <csv_file>
    %(prog)s <csv_file> --output-path <file-name>
    %(prog)s <google_sheet_id> <sheet_name>
    %(prog)s <google_sheet_id> <sheet_name> --print-output"""
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
        default="framework.json",
        help="Output filepath. Default: ./framework.json"
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
