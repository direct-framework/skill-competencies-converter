# Code to extract skill & competencies

Python package to convert skills and competency categories from CSV to JSON/YAML format.

## Install

You can either clone the repository and run the [src/skill_competencies_converter/convert_skills.py](src/skill_competencies_converter/convert_skills.py)
conversion script directly, or install this as a Python package via:

```bash
pip install git+https://github.com/softwaresaved/skill-competencies-converter
```

Installing it as a package will give you acces to the `skill_competencies_converter` command which can be run 
from any location.

## Usage

### Calling via command line interface (If installed as Python package)

```bash
Usage:
skill_competencies_converter [-h] [--output-path OUTPUT_PATH] [--print-output | --no-print-output] [inputs ...]

Convert skills CSV or Google Sheet to YAML/JSON.

positional arguments:
  inputs                Either CSV file path or Google Sheet ID and sheet name

optional arguments:
  -h, --help            show this help message and exit
  --output-path OUTPUT_PATH
                        Output filepath. Default: ./data.json
  --print-output, --no-print-output
                        Print output to stdout (default: False)

Examples:

    skill_competencies_converter <csv_file>
    skill_competencies_converter <google_sheet_id> <sheet_name>
```

#### From a local file:
```bash
skill_competencies_converter data/data.csv
```

By default, if the `--output-path` is not specified, it will output to `data.json`.

#### From a public Google sheet:

```bash
skill_competencies_converter 1umVxBzuZGDgins6XqJwuGVf6BK_DgjknhuwDQpNwyjo "Competency framework - v1.0" --output-path data.json
```

### Calling the conversion script directly (Legacy)

#### From a local file:

```bash
python src/skill_competencies_converter/convert_skills.py data/data.csv --output-path data.json
```

#### From a public google sheet:

```bash
python src/skill_competencies_converter/convert_skills.py 1umVxBzuZGDgins6XqJwuGVf6BK_DgjknhuwDQpNwyjo "Competency framework - v1.0" --output-path data.json
```

If you would like to print the converted result directly to screen along with saving it to file, add the `--print-output` option 
to the end of the command.

## Acknowledgements

The code was written by [Finn Bacall](https://github.com/fbacall/) with small tweaks by [Aleks Nenadic](https://github.com/anenadic/). [Bryn Ubald](https://github.com/bnubald) converted it to a Python package.
