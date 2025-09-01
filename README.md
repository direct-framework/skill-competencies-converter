# Code to extract skill & competencies

Python package to convert skills and competency categories from CSV to JSON/YAML format.

## Install

You can either clone the repository and run the [src/skill_competencies_converter/convert_skills.py](src/skill_competencies_converter/convert_skills.py)
conversion script directly, or install this as a Python package via:

```bash
pip install git+https://github.com/softwaresaved/skill-competencies-converter
```

Installing it as a package will give you access to the `skill_competencies_converter` and `create_user_profile` commands which can be run from any location on your machine.

## Usage

### Via command line interface (if installed as a Python package)

```bash
usage: skill_competencies_converter [-h] [--output-path OUTPUT_PATH] [--print-output | --no-print-output] [inputs ...]

Convert skills CSV or Google Sheet to YAML/JSON.

positional arguments:
  inputs                Either CSV file path or Google Sheet ID and sheet name

options:
  -h, --help            show this help message and exit
  --output-path OUTPUT_PATH
                        Output filepath. Default: ./framework.json
  --print-output, --no-print-output
                        Print output to stdout

Examples:

    skill_competencies_converter <csv_file>
    skill_competencies_converter <csv_file> --output-path <file-name>
    skill_competencies_converter <google_sheet_id> <sheet_name>
    skill_competencies_converter <google_sheet_id> <sheet_name> --print-output
```

```bash
usage: create_user_profile [-h] [--profile-name PROFILE_NAME] [--output-path OUTPUT_PATH] [--print-output | --no-print-output] [inputs ...]

Create user profile file in JSON from skills CSV or Google Sheet file.

positional arguments:
  inputs                Either CSV file path or Google Sheet ID and sheet name

options:
  -h, --help            show this help message and exit
  --profile-name PROFILE_NAME
                        Profile header/column name to read skill level values from. If not provided, use the first column that contains the word 'profile'.
  --output-path OUTPUT_PATH
                        Output filepath. Default: ./user_profile.json
  --print-output, --no-print-output
                        Print output to stdout

Examples:

    create_user_profile <csv_file>
    create_user_profile <csv_file> --profile-name <profile_name> --output-path <output_file>
    create_user_profile <google_sheet_id> <sheet_name>
    create_user_profile <google_sheet_id> <sheet_name> --print-output
```

If you would like to print the converted result directly to screen along with saving it to file, add the `--print-output` option to the end of the command.

#### Using a local data file

```bash
skill_competencies_converter data/data.csv
```
By default, if the `--output-path` is not specified for `skill_competencies_converter`, it will output to `./framework.json`.


```bash
create_user_profile data/data.csv --profile-name "RSE Team Lead profile" --output-path "data/profile.json"
```
By default, if the `--output-path` is not specified for `create_user_profile`, it will output to `./user_profile.json`.


#### Using a public Google sheet with data

```bash
skill_competencies_converter 1umVxBzuZGDgins6XqJwuGVf6BK_DgjknhuwDQpNwyjo "Competency framework - v1.0" --output-path framework.json
```

```bash
create_user_profile 1umVxBzuZGDgins6XqJwuGVf6BK_DgjknhuwDQpNwyjo "Competency profiles - v1.0" --profile-name "RSE Team Lead profile" --output-path "data/profile.json"
```

### Via command line interface - calling the conversion script directly (legacy)

Make sure to activate a virtual environment and install dependencies from `requirements.txt` before running the code.

#### Using a local data file

```bash
python3 src/skill_competencies_converter/convert_skills.py data/data.csv --output-path framework.json
```
```bash
python3 src/skill_competencies_converter/create_user_profile.py data/data.csv --profile-name "RSE Team Lead profile" --output-path "data/profile.json"
```

#### Using a public Google sheet with data

```bash
python3 src/skill_competencies_converter/convert_skills.py 1umVxBzuZGDgins6XqJwuGVf6BK_DgjknhuwDQpNwyjo "Competency framework - v1.0" --output-path framework.json
```

```bash
python3 src/skill_competencies_converter/convert_skills.py 1umVxBzuZGDgins6XqJwuGVf6BK_DgjknhuwDQpNwyjo "Competency profiles - v1.0" --profile-name "RSE Team Lead profile" --output-path "data/profile.json"
```

If you would like to print the converted result directly to screen along with saving it to file, add the `--print-output` option to the end of the command.

## Acknowledgements

The code was written by [Finn Bacall](https://github.com/fbacall/) with small tweaks by [Aleks Nenadic](https://github.com/anenadic/). [Bryn Ubald](https://github.com/bnubald) converted it to a Python package.
