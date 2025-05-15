# Code to extract skill & competencies

[Python code](./code) to convert skills and competency categories from CSV to YAML format.

## Usage

```bash
Usage:
python convert-skills.py [-h] [--output-path OUTPUT_PATH] [--print-output | --no-print-output] [inputs ...]

Convert skills CSV or Google Sheet to YAML/JSON.

positional arguments:
  inputs                Either CSV file path or Google Sheet ID and sheet name

options:
  -h, --help            show this help message and exit
  --output-path OUTPUT_PATH
                        Output filepath. Default: ./data.json
  --print-output, --no-print-output
                        Print output to stdout (default: False)

Example:

    python convert-skills.py convert-skills.py <csv_file>
    python convert-skills.py convert-skills.py <google_sheet_id> <sheet_name>
```
The script will print out the results in YAML format on `stdout`.

From a local file:

```bash
python convert-skills.py data.csv --output-path data.json
```

From a public google sheet:

```bash
python convert-skills.py 1umVxBzuZGDgins6XqJwuGVf6BK_DgjknhuwDQpNwyjo "Competency framework - v1.0" --output-path data.json
```

If you would like to print the converted result directly to screen, add the `--print-output` option to the end of the command.

## Acknowledgements

The code was written by [Finn Bacall](https://github.com/fbacall/) with small tweaks by [Aleks Nenadic](https://github.com/anenadic/).
