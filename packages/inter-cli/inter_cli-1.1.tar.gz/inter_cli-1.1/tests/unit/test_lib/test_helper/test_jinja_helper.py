import pytest
from jinja2 import TemplateNotFound, Template

from src.inter_cli.lib.helpers import JinjaTemplateHelper
from src.inter_cli.schemas.env import KubernetesEnv
from src.inter_cli.schemas.resources import Resources, SpecResources
import pathlib


def test_get_jinja_template_success():
    current_path = pathlib.Path(__file__).parent.resolve()
    template_path = f"{current_path}/files"
    template_file_name = "sample_template.yaml.jinja"
    helper = JinjaTemplateHelper()
    template = helper._get_jinja_template(template_path, template_file_name)
    assert isinstance(template, Template)


def test_get_jinja_template_not_found():
    current_path = pathlib.Path(__file__).parent.resolve()
    template_path = f"{current_path}/files"
    template_file_name = "dale.yaml.jinja"
    helper = JinjaTemplateHelper()

    with pytest.raises(TemplateNotFound):
        helper._get_jinja_template(template_path, template_file_name)


def test_build_online_deployment_manifests():
    # Test data
    image_name = "my-image:latest"
    resources = SpecResources(
        requests=Resources(cpu=1, memory="1Gi"), limits=Resources(cpu=2, memory="2Gi")
    )
    env_vars = [KubernetesEnv(name="VAR1", value="value1")]
    project_name = "my-project"
    template_version = "v1"
    developer = "John Doe"
    environment = "dev"

    # Call the method
    helper = JinjaTemplateHelper()
    result = helper.build_online_deployment_manifests(
        image_name_n_tag=image_name,
        resources=resources,
        env_vars=env_vars,
        project_name=project_name,
        template_version=template_version,
        developer=developer,
        environment=environment,
    )

    # Assertions
    assert "VAR1" in result.deployment
    assert "value1" in result.deployment
    assert "apiVersion" in result.deployment
    assert "John Doe" in result.deployment
    assert "dev" in result.deployment

    assert "John Doe" in result.service
