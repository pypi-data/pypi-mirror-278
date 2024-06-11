import os
from collections.abc import Mapping
from functools import lru_cache

from github import Auth
from github import Github
from github.Repository import Repository


class RemoteHosting:
    pass


class GitHosting(RemoteHosting):
    def __init__(self, token: str | None = None):
        super().__init__()
        if token is None:
            token = os.getenv("GH_TOKEN")
        if token is None:
            raise ValueError("GitHub token must be provided")
        auth = Auth.Token(token)
        self.github = Github(auth=auth)

    @lru_cache(maxsize=128, typed=True)  # noqa: B019
    def get_repos(self) -> Mapping[str, Repository]:
        repos: dict[str, Repository] = {}
        user = self.github.get_user()
        for repo in user.get_repos(type="all"):  # Fetch all types of repos including private
            repos[repo.full_name] = repo
        return repos
