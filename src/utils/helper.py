"""This module contains helper functions."""
import yaml


def read_yaml_file(file_path: str):
    """Read the yaml file."""
    print(f"Reading the yaml file at {file_path}...")
    ## Save it in dict
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data