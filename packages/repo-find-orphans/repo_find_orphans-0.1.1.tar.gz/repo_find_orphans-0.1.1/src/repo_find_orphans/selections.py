from collections.abc import Iterator
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

import yaml


@dataclass
class RepoSelection:
    account_name: str
    include: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)

    def __contains__(self, item: str) -> bool:
        # Allow is always True if 'include' is empty,
        # otherwise check if 'item' starts with any prefix in 'include'
        allow = any(item.startswith(prefix) for prefix in self.include) if self.include else True
        if allow and self.exclude:
            # Disallow if item starts with any prefix in exclude
            allow = not any(item.startswith(prefix) for prefix in self.exclude)
        return allow


class Selections:
    def __init__(self, file_path: Path):
        super().__init__()
        self.selections: dict[str, RepoSelection] = {}
        self.file_path: Path = file_path
        self.parse()

    def __getitem__(self, user: str) -> RepoSelection:
        return self.selections[user]

    def __setitem__(self, user: str, selection: RepoSelection) -> None:
        self.selections[user] = selection

    def __iter__(self) -> Iterator[RepoSelection]:
        return iter(self.selections.values())

    def __len__(self) -> int:
        return len(self.selections)

    def __contains__(self, item: str) -> bool:
        account, repo = item.split("/", 1)
        return account not in self.selections or repo in self.selections[account]

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        return f"Selections(file_path={self.file_path}, selections={self.selections})"

    def parse(self) -> None:
        with self.file_path.open() as f:
            selections = yaml.safe_load(f)
            for user, data in selections.items():
                if not data:
                    self[user] = RepoSelection(account_name=user)
                else:
                    self[user] = RepoSelection(
                        account_name=user, include=data.get("include", []), exclude=data.get("exclude", [])
                    )
