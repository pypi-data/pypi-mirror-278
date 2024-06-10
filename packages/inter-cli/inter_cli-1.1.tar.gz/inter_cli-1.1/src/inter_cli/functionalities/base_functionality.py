import abc
from typing import Optional


class BaseFunctionality(abc.ABC):
    @abc.abstractmethod
    def execute(self, mlops_config: Optional[dict]) -> None:
        raise NotImplementedError()
