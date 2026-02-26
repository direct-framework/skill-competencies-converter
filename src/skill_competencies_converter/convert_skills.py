from skill_competencies_converter.utilities import (
    is_blank,
    read_csv_from_file,
    read_csv_from_url,
    SUPPORTED_OUTPUTS,
)
import argparse
import csv
import importlib
import os
import sys
from pathlib import Path


def parse_core_framework(csv_data):
    output = {"competency_domains": [], "competencies": [], "skills": []}

    reader = csv.reader(csv_data.splitlines())
    headers = next(reader)

    desc_idx = headers.index("description")
    related_skills_idx = headers.index("related_skills")
    slug_idx = headers.index("slug")
    tools_idx = headers.index("tools_languages_methods_behaviours")
    learning_idx = headers.index("learning_resources")

    for idx, row in enumerate(reader):
        if not is_blank(row[0]):
            competency_domain = {
                "name": row[0],
                "description": row[desc_idx],
                "slug": row[slug_idx],
                "rank": idx,
            }
            output["competency_domains"].append(competency_domain)
        if not is_blank(row[1]):
            competency = {
                "name": row[1],
                "description": row[desc_idx],
                "slug": row[slug_idx],
                "competency_domain": competency_domain["slug"],
            }
            output["competencies"].append(competency)
        if not is_blank(row[2]):
            skill = {
                "name": row[2],
                "description": row[desc_idx],
                "related_skills": row[related_skills_idx],
                "slug": row[slug_idx],
                "competency": competency["slug"],
                "tools_languages_methods_behaviours": row[tools_idx],
                "learning_resources": row[learning_idx],
            }
            output["skills"].append(skill)
        else:
            continue

    return output


def parse_csv(csv_data) -> list[str, str]:
    reader = csv.reader(csv_data.splitlines())
    headers = next(reader)

    # Remove all empty values from the headers
    if "" in headers:
        headers = headers[: headers.index("")]

    output = []
    for row in reader:
        output.append({header.lower(): row[idx] for idx, header in enumerate(headers)})
    return output


def parse_framework(sheet_id):
    csv_data = read_csv_from_url(sheet_id, "Competency framework - v1.1")
    output = parse_core_framework(csv_data)

    csv_data = read_csv_from_url(sheet_id, "Skills Scale - v1.1")
    output["skill_levels"] = parse_csv(csv_data)

    csv_data = read_csv_from_url(sheet_id, "Tools and Behaviours - v1.1")
    output["tools_languages_methods_behaviours"] = parse_csv(csv_data)

    csv_data = read_csv_from_url(sheet_id, "Learning Resources - v1.1")
    output["learning_resources"] = parse_csv(csv_data)

    csv_data = read_csv_from_url(sheet_id, "Providers - v1.1")
    output["providers"] = parse_csv(csv_data)

    return output


def get_parser():
    """
    Parse input arguments, and return the parser.
    """
    example_text = """Examples:

    %(prog)s --google-sheet <google_sheet_id>
    %(prog)s --legacy-csv <csv_file>
    %(prog)s --legacy-csv <csv_file> --output-path <file-name>
    %(prog)s --google-sheet <google_sheet_id> --print-output"""
    parser = argparse.ArgumentParser(
        description="Convert skills CSV or Google Sheet to YAML/JSON.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--google-sheet",
        help="Google Sheet ID. Processes full framework based on assumed sheet names.",
    )
    parser.add_argument(
        "--legacy-csv",
        default=None,
        help="CSV filepath for V1 of framework structure.",
    )
    parser.add_argument(
        "--output-path",
        default="framework.json",
        help="Output filepath. Default: ./framework.json",
    )
    parser.add_argument(
        "--print-output",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Print output to stdout",
    )

    return parser


def main():
    """
    Main conversion function.
    """
    parser = get_parser()
    args = parser.parse_args()

    if args.legacy_csv:
        csv_content = read_csv_from_file(args.legacy_csv)
        output = parse_core_framework(csv_content)
    elif args.google_sheet:
        output = parse_framework(args.google_sheet)
    else:
        parser.print_help()
        sys.exit(1)

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

    if args.google_sheet:
        path = Path(args.output_path)
        for key, val in output.items():
            save_func(val, path.with_stem(path.stem + f"-{key}"), args.print_output)


if __name__ == "__main__":
    main()
