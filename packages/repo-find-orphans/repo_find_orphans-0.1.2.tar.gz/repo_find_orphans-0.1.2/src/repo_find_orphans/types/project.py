from dataclasses import dataclass

from repo_find_orphans.types.remote import Remote


@dataclass
class Project:
    name: str
    path: str
    revision: str
    remote: Remote

    @property
    def host_type(self) -> str | None:
        return self.remote.host_type

    @property
    def host_account(self) -> str:
        if self.host_type == "github":
            if self.remote.host_account is not None:
                return self.remote.host_account
            return self.name.split("/")[0]
        return "Unknown"

    @property
    def canonical_form(self) -> str:
        if self.name.startswith(self.host_account):
            return self.name
        return f"{self.host_account}/{self.name}"

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        return f"Project(name={self.name}, path={self.path}, revision={self.revision}, remote={self.remote})"
