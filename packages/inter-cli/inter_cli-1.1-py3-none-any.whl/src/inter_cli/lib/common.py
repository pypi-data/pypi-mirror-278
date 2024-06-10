from typing import Any
from yaml import safe_load, YAMLError


def read_yaml(mlops_config_path: str) -> dict[str, Any]:
    with open(mlops_config_path) as stream:
        try:
            return safe_load(stream)
        except YAMLError:
            raise ValueError("Could not parse mlops_config")
