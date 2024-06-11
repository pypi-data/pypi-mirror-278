"""Data-extraction module"""

from typing import Dict, Any
import json


def open_json_file(input_file_path: str, mode: str = "r") -> Dict[str, Any]:
    """Open json file"""

    with open(file=input_file_path, mode=mode) as file:
        data = json.load(file)
    return data


# Call function to extract data from JSON file
sr_input_example: dict = open_json_file(
    input_file_path="src/pkg_support_resistance/data_set/example.json"
)
