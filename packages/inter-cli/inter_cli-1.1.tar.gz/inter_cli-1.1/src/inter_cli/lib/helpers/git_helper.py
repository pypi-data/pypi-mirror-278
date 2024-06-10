from git import Repo
import pathlib


class GitHelper:

    def clone_repository(self, repo_url: str, destination_folder: str) -> Repo:
        return Repo.clone_from(repo_url, destination_folder)

    def create_new_branch_from_current_branch(
        self, repo: Repo, target_branch: str
    ) -> None:
        repo.git.checkout("-b", target_branch)

    def add_file_to_repository(
        self, repo: Repo, file_content: str, dest_file_path: str, file_name: str
    ) -> None:
        repository_root_path = repo.git.rev_parse("--show-toplevel")
        pathlib.Path(f"{repository_root_path}/{dest_file_path}").mkdir(
            parents=True, exist_ok=True
        )
        destination_path = pathlib.Path(f"{repository_root_path}/{dest_file_path}")

        with open(f"{destination_path}/{file_name}", "w") as file:
            file.write(file_content)

    def add_changes(self, repo: Repo) -> None:
        repo.git.add(".")

    def commit_changes(self, repo: Repo, commit_message: str) -> None:
        repo.git.commit("-m", f"feat: deployment of model - {commit_message}")

    def push_changes(self, repo: Repo, target_branch: str) -> None:
        repo.git.push("--set-upstream", "origin", target_branch)
