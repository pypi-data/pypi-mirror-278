import importlib
import os
from src.inter_cli.exceptions import UnsupportedFunctionalityException
from src.inter_cli.functionalities.base_functionality import BaseFunctionality
from typing import Callable

__all__ = ["factory"]

FUNCTIONALITY: dict[str, BaseFunctionality] = dict()


def factory(name: str, *args, **kwargs) -> BaseFunctionality:
    try:
        return FUNCTIONALITY[name](*args, **kwargs)
    except KeyError:
        raise UnsupportedFunctionalityException(
            f"functionality {name} is not supported"
        )


def register_functionality(name: str) -> Callable:
    def register_class_fn(cls) -> BaseFunctionality:
        if name in FUNCTIONALITY:
            raise ValueError(f"Name {name} already registered!")
        if not issubclass(cls, BaseFunctionality):
            raise ValueError(f"Class {cls} is not a subclass of {BaseFunctionality}")
        FUNCTIONALITY[name] = cls
        return cls

    return register_class_fn


def import_modules(m_type: str) -> None:
    for file in os.listdir(f"{os.path.dirname(__file__)}/{m_type}"):
        if file.endswith(".py") and not file.startswith("+") and file != "factory.py":
            module_name = file[: file.find(".py")]
            importlib.import_module(
                f"src.inter_cli.functionalities.{m_type}." + module_name
            )
