from cookiecutter.main import cookiecutter
from src.inter_cli.functionalities.base_functionality import BaseFunctionality
import pathlib
from . import version
from src.inter_cli.functionalities.factory import register_functionality
from typing import Optional


@register_functionality(f"{version}_ProjectInitializer")
class ProjectInitializer(BaseFunctionality):
    def execute(self, mlops_config: Optional[dict] = None) -> None:
        current_path = pathlib.Path(__file__).parent.resolve()
        cookiecutter_template_folder = f"{current_path}/../../templates/v1/cookiecutter"
        cookiecutter(cookiecutter_template_folder)
