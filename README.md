# Code to extract skill & competencies

[Python code](./code) to convert skills and competency categories from CSV to YAML format.

## Usage

```bash
Usage:
  python convert-skills.py <csv_file>
  python convert-skills.py <google_sheet_id> <sheet_name>
```
The script will print out the results in YAML format on `stdout`.

From a local file:

```bash
python convert-skills.py data.csv > data.yml
```

From a public google sheet:

```bash
python convert-skills.py 1IJydvoI9H-M1TDLakVlIuHb55auUiKKhE6YP8uD_Sso "Competency framework - v0.2" > data.yml
```
## Acknowledgements

The code was written by [Finn Bacall](https://github.com/fbacall/) with small tweaks by [Aleks Nenadic](https://github.com/anenadic/).
