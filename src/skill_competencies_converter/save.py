import json
import yaml


def save_json(data: dict, output_path: str = "data.json", print_output: bool = False):
    """
    Saves parsed CSV to JSON file.
    """
    json_output = json.dumps(data, ensure_ascii=False, indent=2)
    if print_output:
        print(json_output)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_output)
    return


def save_yaml(data: dict, output_path: str = "data.yml", print_output: bool = False):
    """
    Saves parsed CSV to YAML file.
    """
    yaml_output = yaml.dump(data, allow_unicode=True, sort_keys=False)
    if print_output:
        print(yaml_output)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(yaml_output)
    return
