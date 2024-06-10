from dataclasses import dataclass


@dataclass
class Remote:
    name: str
    fetch: str

    @property
    def host_type(self) -> str:
        if "github.com" in self.fetch:
            return "github"
        elif "gitlab.com" in self.fetch:
            return "gitlab"
        elif "bitbucket.org" in self.fetch:
            return "bitbucket"
        else:
            return "unknown"

    @property
    def host_account(self) -> str | None:
        if "github.com/" in self.fetch:
            account = self.fetch.split("github.com/")[1].split('/')[0]
            return account if account != "" else None
        return None
