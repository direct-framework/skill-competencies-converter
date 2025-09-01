# Code to extract skill & competencies

Python package to convert skills and competency categories from CSV to JSON/YAML format.

## Install

You can either clone the repository and run the [src/skill_competencies_converter/convert_skills.py](src/skill_competencies_converter/convert_skills.py)
conversion script directly, or install this as a Python package via:

```bash
pip install git+https://github.com/softwaresaved/skill-competencies-converter
```

Installing it as a package will give you access to the `skill_competencies_converter` command which can be run 
from any location.

## Usage

### Via command line interface (if installed as a Python package)

```bash
usage: convert_skills.py [-h] [--output-path OUTPUT_PATH] [--print-output | --no-print-output] [inputs ...]

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

    convert_skills.py <csv_file>
    convert_skills.py <csv_file> --output-path <file-name>
    convert_skills.py <google_sheet_id> <sheet_name>
    convert_skills.py <google_sheet_id> <sheet_name> --print-output
```

#### Using a local data file

```bash
skill_competencies_converter data/data.csv
```

By default, if the `--output-path` is not specified, it will output to `framework.json`.

#### Using a public Google sheet with data

```bash
skill_competencies_converter 1umVxBzuZGDgins6XqJwuGVf6BK_DgjknhuwDQpNwyjo "Competency framework - v1.0" --output-path framework.json
```

### Via command line interface - calling the conversion script directly (legacy)

Make sure to activate a virtual environment and install dependencies from `requirements.txt` before running the code.


#### Using a local data file

```bash
python3 src/skill_competencies_converter/convert_skills.py data/data.csv --output-path framework.json
```

#### Using a public Google sheet with data

```bash
python3 src/skill_competencies_converter/convert_skills.py 1umVxBzuZGDgins6XqJwuGVf6BK_DgjknhuwDQpNwyjo "Competency framework - v1.0" --output-path framework.json
```

If you would like to print the converted result directly to screen along with saving it to file, add the `--print-output` option 
to the end of the command.

## Acknowledgements

The code was written by [Finn Bacall](https://github.com/fbacall/) with small tweaks by [Aleks Nenadic](https://github.com/anenadic/). [Bryn Ubald](https://github.com/bnubald) converted it to a Python package.
