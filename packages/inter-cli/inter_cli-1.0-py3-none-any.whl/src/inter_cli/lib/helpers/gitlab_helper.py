import gitlab
from gitlab import Gitlab


class GitlabHelper:
    def __init__(self) -> None:
        pass

    def create_gitlab_session(
        self, gitlab_host: str, gitlab_private_token: str
    ) -> Gitlab:
        return gitlab.Gitlab(gitlab_host, private_token=gitlab_private_token)

    def open_merge_request(
        self,
        gitlab_session: Gitlab,
        project_id: str,
        source_branch: str,
        target_branch: str,
        title: str,
        description: str,
    ) -> str:
        project = gitlab_session.projects.get(project_id)
        merge_request = project.mergerequests.create(
            {
                "source_branch": source_branch,
                "target_branch": target_branch,
                "title": title,
                "description": description,
            }
        )

        return merge_request.web_url
