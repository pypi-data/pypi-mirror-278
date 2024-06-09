from src.inter_cli.schemas.resources import SpecResources
from pydantic import BaseModel
import os
from typing import List, Optional
from src.inter_cli.schemas.env import KubernetesEnv


class OnlineDeploymentSpec(BaseModel):
    class Config:
        extra = "forbid"
        use_enum_values = True

    resources: SpecResources
    envVars: Optional[List[KubernetesEnv]] = None
    image: str | None = os.getenv("DOKCER_IMAGE", None)
