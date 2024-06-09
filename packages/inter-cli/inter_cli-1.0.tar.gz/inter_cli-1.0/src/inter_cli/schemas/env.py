from pydantic import BaseModel


class KubernetesEnv(BaseModel):
    name: str
    value: str
