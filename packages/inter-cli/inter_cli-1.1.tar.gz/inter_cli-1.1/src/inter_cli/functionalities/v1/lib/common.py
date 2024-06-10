from src.inter_cli.functionalities.v1.schemas.deployment.mlops_config import MLOpsConfig
from typing import Any


def validate_schema(parsed_mlops_config: dict[Any, Any] | None) -> MLOpsConfig:
    try:
        return MLOpsConfig.model_validate(parsed_mlops_config)
    except Exception as e:
        raise ValueError(f"Schema validation failed because of: {e}")
