from src.inter_cli.functionalities.base_functionality import BaseFunctionality
from . import version
from src.inter_cli.functionalities.factory import register_functionality
from typing import Optional
from src.inter_cli.config import Config
import tempfile
from src.inter_cli.lib.helpers import (
    GitHelper,
    JinjaTemplateHelper,
    GitlabHelper,
)
from src.inter_cli.functionalities.v1.lib.common import validate_schema
from datetime import datetime
from loguru import logger
import yaml


@register_functionality(f"{version}_OnlineDeployment")
class OnlineDeployment(BaseFunctionality):
    def execute(self, parsed_mlops_config: Optional[dict]) -> None:
        logger.info("validating schema")
        mlops_config = validate_schema(parsed_mlops_config)

        context_path = tempfile.TemporaryDirectory()
        context_path_name = context_path.name
        config = Config()
        git_helper = GitHelper()
        gitlab_helper = GitlabHelper()
        jinja_helper = JinjaTemplateHelper()

        logger.info("building manifests")
        online_deployment_manifests = jinja_helper.build_online_deployment_manifests(
            developer=mlops_config.metadata.developers[0],
            env_vars=mlops_config.spec.envVars,
            environment=mlops_config.metadata.environment,
            template_version=version,
            project_name=mlops_config.metadata.project_name,
            image_name_n_tag=mlops_config.spec.image,
            resources=mlops_config.spec.resources,
        )
        logger.info("cloning central manifests repository")
        manifests_repo = git_helper.clone_repository(
            repo_url=config.gitlab_config.manifest_repository.repository_url,
            destination_folder=f"{context_path_name}/manifests",
        )

        now = datetime.now()
        TARGET_BRANCH = f"{mlops_config.metadata.developers[0]}_{mlops_config.metadata.project_name}-{now.strftime('%m%d%Y%H%M%S')}"
        SOURCE_BRANCH = "main"

        logger.info(f"creating new branch with name {TARGET_BRANCH}")
        git_helper.create_new_branch_from_current_branch(manifests_repo, TARGET_BRANCH)
        git_helper.add_file_to_repository(
            manifests_repo,
            online_deployment_manifests.deployment,
            f"/{mlops_config.metadata.environment}",
            "deployment.yaml",
        )
        git_helper.add_file_to_repository(
            manifests_repo,
            online_deployment_manifests.service,
            f"/{mlops_config.metadata.environment}",
            "service.yaml",
        )
        logger.info("commiting changes")
        git_helper.add_changes(manifests_repo)
        git_helper.commit_changes(
            manifests_repo,
            f"feat: online model deployment: {mlops_config.metadata.project_name}",
        )
        git_helper.push_changes(manifests_repo, TARGET_BRANCH)

        gl_session = gitlab_helper.create_gitlab_session(
            config.gitlab_config.url, config.gitlab_config.token
        )

        mr_title = f"Deployment of online model {mlops_config.metadata.project_name}"
        mr_description = f"""

MLOps config that generated this deployment


```yaml
{yaml.dump(mlops_config.model_dump())}

"""

        mr_url = gitlab_helper.open_merge_request(
            gitlab_session=gl_session,
            project_id=config.gitlab_config.manifest_repository.repository_id,
            source_branch=TARGET_BRANCH,
            target_branch=SOURCE_BRANCH,
            title=mr_title,
            description=mr_description,
        )

        logger.success(f"Merge request succefully opened, cheit out at {mr_url}")
