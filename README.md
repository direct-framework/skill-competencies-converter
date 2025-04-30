# Code to extract skill & competencies

[Python code](./code) to convert skills and competency categories from CSV to YAML format.

## Usage

```bash
Usage:
  python script.py <csv_file>
  python script.py <google_sheet_id> <sheet_name>
``


From a local file:

```bash
python convert-skills.py data.csv > data.yml
```

From a public google sheet:

```bash
python convert-skills.py 1IJydvoI9H-M1TDLakVlIuHb55auUiKKhE6YP8uD_Sso "Competency framework - v0.2" > data.yml
```
