from src.inter_cli.functionalities.factory import factory
from src.inter_cli.functionalities.v1.project_initializer import ProjectInitializer
from src.inter_cli.functionalities.base_functionality import BaseFunctionality
from src.inter_cli.exceptions import UnsupportedFunctionalityException
import pytest


def test_factory_v1_project_initializer():
    functionality = factory("v1_ProjectInitializer")
    assert isinstance(functionality, ProjectInitializer)
    assert issubclass(type(functionality), BaseFunctionality)


def test_factory_wrong_functionality_name():
    wrong_functionality_name = "groselha"
    with pytest.raises(UnsupportedFunctionalityException) as exc_info:
        factory(wrong_functionality_name)
    assert (
        str(exc_info.value)
        == f"functionality {wrong_functionality_name} is not supported"
    )
