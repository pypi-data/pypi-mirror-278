from enum import Enum


class SchemaKind(str, Enum):
    onlineDeployment = "OnlineDeployment"


class Environment(str, Enum):
    hml = "hml"
    stg = "stg"
    prd = "prd"


class ModelType(str, Enum):
    classification = "classification"
    regression = "regression"
    clusterization = "clusterization"
