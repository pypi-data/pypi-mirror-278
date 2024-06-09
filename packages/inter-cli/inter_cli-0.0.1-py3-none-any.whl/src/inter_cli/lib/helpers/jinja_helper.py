from jinja2 import FileSystemLoader, Environment, Template
import pathlib
from dataclasses import dataclass
from typing import List
from src.inter_cli.schemas.env import KubernetesEnv


@dataclass
class BuildOnlineDeploymentManifestsReturn:
    deployment: str
    service: str


class JinjaTemplateHelper:

    def _get_jinja_template(
        self, templates_folder: str, template_file: str
    ) -> Template:
        file_loader = FileSystemLoader(templates_folder)
        env = Environment(loader=file_loader)

        return env.get_template(template_file)

    def build_online_deployment_manifests(
        self,
        image_name_n_tag: str | None,
        resources: dict[str, dict[str, float | str]],
        env_vars: List[KubernetesEnv] | None,
        project_name: str,
        template_version: str,
        developer: str,
        environment: str,
    ) -> BuildOnlineDeploymentManifestsReturn:
        current_path = pathlib.Path(__file__).parent.resolve()
        template_folder = (
            f"{current_path}/../../templates/{template_version}/online_deployment"
        )
        deployment_template = self._get_jinja_template(
            template_folder, "deployment.yaml.jinja"
        )
        service_template = self._get_jinja_template(
            template_folder, "service.yaml.jinja"
        )

        deployment_manifest = deployment_template.render(
            project_name=project_name,
            developer=developer,
            environment=environment,
            image=image_name_n_tag,
            resources=resources,
            env_vars=env_vars,
        )
        service_manifest = service_template.render(
            project_name=project_name, developer=developer
        )

        return BuildOnlineDeploymentManifestsReturn(
            deployment=deployment_manifest, service=service_manifest
        )
