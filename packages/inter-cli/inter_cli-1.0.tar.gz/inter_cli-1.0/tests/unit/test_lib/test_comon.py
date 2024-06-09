from src.inter_cli.lib.common import read_yaml
import pathlib
import pytest


def test_read_yaml_valid_yaml():
    current_path = pathlib.Path(__file__).parent.resolve()
    valid_yaml_path = f"{current_path}/files/valid_yaml.yaml"
    parsed_yaml = read_yaml(valid_yaml_path)
    assert isinstance(parsed_yaml, dict)


def test_read_yaml_invalid_yaml():
    current_path = pathlib.Path(__file__).parent.resolve()
    valid_yaml_path = f"{current_path}/files/invalid_yaml.yaml"
    with pytest.raises(ValueError) as exc_info:
        read_yaml(valid_yaml_path)

    assert str(exc_info.value) == "Could not parse mlops_config"
