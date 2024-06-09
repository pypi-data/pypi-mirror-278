from src.inter_cli.decorators import singleton
from dataclasses import dataclass, field
import os


@dataclass
class RepositoryConfig:
    repository_url: str
    repository_id: str


@dataclass
class GitlabConfig:
    token: str | None = os.getenv("GITLAB_TOKEN", None)
    manifest_repository: RepositoryConfig = field(
        default_factory=lambda: RepositoryConfig(
            "https://gitlab.com/victormacedo996/inter_test_manifests", "58648093"
        )
    )
    url: str = "https://gitlab.com"


@singleton
@dataclass
class Config:
    gitlab_config: GitlabConfig = field(default_factory=lambda: GitlabConfig())
