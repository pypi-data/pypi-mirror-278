from pydantic import BaseModel, field_validator, model_validator
from typing import List, Union, Self
from src.inter_cli.functionalities.v1.schemas.deployment import enums
from src.inter_cli.functionalities.v1.schemas.deployment.online_deployment.online_deployment_spec import (
    OnlineDeploymentSpec,
)
import re


class Metadata(BaseModel):

    class Config:
        extra = "forbid"
        use_enum_values = True

    developers: List[str]
    emails: List[str]
    team: str
    environment: enums.Environment
    version: str
    description: str
    project_name: str
    type: enums.ModelType

    @field_validator("emails")
    @classmethod
    def validate_emails(cls, emails: List[str]) -> List[str]:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        for email in emails:
            if not re.fullmatch(pattern, email):
                raise ValueError(f"email {email} is not valid")

        return emails


class MLOpsConfig(BaseModel):

    class Config:
        extra = "forbid"
        use_enum_values = True

    version: str
    kind: enums.SchemaKind
    metadata: Metadata
    spec: Union[OnlineDeploymentSpec]

    @model_validator(mode="after")
    @classmethod
    def validate_spec_acording_to_kind(cls, values: Self) -> Self:
        kind = values.kind
        spec = values.spec

        if kind == enums.SchemaKind.onlineDeployment:
            try:
                OnlineDeploymentSpec.model_validate(spec)
            except Exception:
                raise ValueError("OnlineDeployment.spec is invalid")

        return values
