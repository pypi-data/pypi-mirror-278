import pytest
from src.inter_cli.functionalities.v1.lib.common import validate_schema
from src.inter_cli.functionalities.v1.schemas.deployment.mlops_config import MLOpsConfig


@pytest.fixture
def valid_parsed_mlops_config():
    return {
        "version": "v1",
        "kind": "OnlineDeployment",
        "metadata": {
            "developers": ["victor"],
            "team": "mlops",
            "emails": ["victor@victor.com"],
            "environment": "hml",
            "version": "1.0",
            "description": "descricao",
            "type": "classification",
            "project_name": "meu projeto",
        },
        "spec": {
            "resources": {
                "requests": {"cpu": 1, "memory": "128Mi"},
                "limits": {"cpu": 2, "memory": "512Mi"},
            },
            "envVars": [{"name": "ENV1", "value": "VALUE1"}],
        },
    }


def test_validation_success(valid_parsed_mlops_config):
    mlops_config = validate_schema(valid_parsed_mlops_config)
    assert isinstance(mlops_config, MLOpsConfig)


@pytest.fixture
def invalid_parsed_mlops_config():
    return {
        "version": "v1",
        "kind": "OnlineDeployment",
        "metadata": {
            "developers": ["victor"],
            "team": "mlops",
            "emails": ["victor@victor.com"],
            "environment": "hml",
            "version": "1.0",
            "description": "descricao",
            "type": "classification",
            "project_name": "meu projeto",
        },
        "spec": {
            "resources": {
                "requests": {"cpu": 1, "memory": "a"},
                "limits": {"cpu": 2, "memory": "512Mi"},
            },
            "envVars": [{"name": "ENV1", "value": "VALUE1"}],
        },
    }


def test_validation_not_successfull_with_invalid_resources_requests_memory(
    invalid_parsed_mlops_config,
):
    with pytest.raises(ValueError) as exc_info:
        _ = validate_schema(invalid_parsed_mlops_config)

    assert "Schema validation failed because of" in str(exc_info.value)
