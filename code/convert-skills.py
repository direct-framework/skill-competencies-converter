import csv
import sys
import yaml
import urllib.request


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


def parse_csv(csv_data):
    category = None
    subcategory = None
    output = {}

    reader = csv.reader(csv_data.splitlines())
    headers = next(reader)

    for row in reader:
        if not is_blank(row[0]):
            category = row[0]
        if not is_blank(row[1]):
            subcategory = row[1]
        if not is_blank(row[2]):
            skill = row[2]
        else:
            continue

        output.setdefault(category, {}).setdefault(subcategory, {}).setdefault(skill, {
            'description': row[4],
            'tools_languages_methods_behaviours': row[3],
            'training_resources': row[5]
        })

    return output


def print_help_message():
    print("Usage:")
    print("  python convert-skills.py <csv_file>")
    print("  python convert-skills.py <google_sheet_id> <sheet_name>")
    sys.exit(1)


if __name__ == '__main__':
    if "--help" or "-h" in sys.argv:
        print_help_message()
    elif len(sys.argv) == 3:
        sheet_id = sys.argv[1]
        sheet_name = sys.argv[2]
        csv_content = read_csv_from_url(sheet_id, sheet_name)
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        csv_content = read_csv_from_file(filename)
    else:
        print_help_message()

    output = parse_csv(csv_content)
    print(yaml.dump(output, allow_unicode=True, sort_keys=False))
