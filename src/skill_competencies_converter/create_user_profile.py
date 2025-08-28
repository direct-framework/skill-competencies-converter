from utilities import *
import argparse
import csv
import importlib
import os
import random
import sys


def parse_user_profile(profile_name, csv_data):
    reader = csv.reader(csv_data.splitlines())
    headers = next(reader)

    category_idx = find_idx(headers, "category")
    subcategory_idx = find_idx(headers, "subcategory")
    skill_idx = find_idx(headers, "skill")
    # Use the exact profile name to locate column with profile data,
    # else find the first column that contains the word "profile"
    profile_idx = find_idx(headers, profile_name) if profile_name else find_idx(headers, "profile")

    user_id = random.randint(0, 100)
    output = {
        "user_id": user_id,
        "name": "User " + str(user_id),
        "role": headers[profile_idx].replace("profile", "").strip(),
        "user_data": []
    }

    for row in reader:
        if not is_blank(row[category_idx]):
            category = row[category_idx]
        if not is_blank(row[subcategory_idx]):
            subcategory = row[subcategory_idx]
        if not is_blank(row[skill_idx]):
            skill = row[skill_idx]
        if not is_blank(row[profile_idx]):
            user_data = {
                'category': category,
                'subcategory': subcategory,
                'skill': skill,
                'skill_level': row[profile_idx][0]  # take the first character which is a number indicating level
            }
            output['user_data'].append(user_data)

    return output


def get_parser():
    """
    Parse input arguments, and return the parser.
    """
    example_text = """Examples:

    %(prog)s <csv_file>
    %(prog)s <csv_file> --profile-name <profile_name> --output-path <output_file>
    %(prog)s <google_sheet_id> <sheet_name>
    %(prog)s <google_sheet_id> <sheet_name> --print-output
    """
    parser = argparse.ArgumentParser(
        description="Create user profile file in JSON from skills CSV or Google Sheet file.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        help="Either CSV file path or Google Sheet ID and sheet name"
    )
    parser.add_argument(
        "--profile-name",
        help="Profile header/column name to read skill level values from"
    )
    parser.add_argument(
        "--output-path",
        default="user_profile.json",
        help="Output filepath. Default: ./user_profile.json"
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

    user_profile_name = args.profile_name
    output = parse_user_profile(user_profile_name, csv_content)

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
