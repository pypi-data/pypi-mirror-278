from pydantic import BaseModel, field_validator
import re


class Resources(BaseModel):

    class Config:
        extra = "forbid"

    cpu: float
    memory: str

    @field_validator("memory")
    @classmethod
    def validate_schedule(cls, memory: str) -> str:
        pattern = r"^[1-9][0-9]*[MG]i$"
        if not re.fullmatch(pattern, memory):
            raise ValueError(f"memory {memory} is not valid")

        return memory


class SpecResources(BaseModel):
    requests: Resources
    limits: Resources
