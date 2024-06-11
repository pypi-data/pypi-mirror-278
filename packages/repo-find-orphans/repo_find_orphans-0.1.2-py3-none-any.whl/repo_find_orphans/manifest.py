from pathlib import Path
from typing import TYPE_CHECKING

from defusedxml import ElementTree as ET  # noqa: N817

from repo_find_orphans.types.project import Project
from repo_find_orphans.types.remote import Remote

if TYPE_CHECKING:
    from collections.abc import Mapping


class Manifest:
    def __init__(self, file_path: Path):
        super().__init__()
        self.file_path = file_path
        self.projects: list[Project] = []
        self.remotes: list[Remote] = []
        self.defaults: Mapping[str, str] = {}
        self.parse()

    def parse(self) -> None:
        with self.file_path.open() as f:
            file_content = f.read()
            self._extract_remotes(file_content)
            self._extract_defaults(file_content)
            self._extract_projects(file_content)

    def _extract_projects(self, file_content: str):
        tree = ET.fromstring(file_content, forbid_dtd=True, forbid_entities=True, forbid_external=True)
        for project_elem in tree.findall("project"):
            name = project_elem.get("name") or "default_name"
            path = project_elem.get("path") or "default_path"
            revision = project_elem.get("revision") or self.defaults.get("revision", "default_revision")
            remote_name = project_elem.get("remote") or self.defaults.get("remote", "default_remote")
            remote = next(r for r in self.remotes if r.name == remote_name)
            self.projects.append(Project(name, path, revision, remote))

    def _extract_remotes(self, file_content: str):
        tree = ET.fromstring(file_content, forbid_dtd=True, forbid_entities=True, forbid_external=True)
        for remote_elem in tree.findall("remote"):
            name = remote_elem.get("name") or "unknown_name"
            fetch = remote_elem.get("fetch") or "unkown_fetch"
            self.remotes.append(Remote(name, fetch))

    def _extract_defaults(self, file_content: str):
        tree = ET.fromstring(file_content, forbid_dtd=True, forbid_entities=True, forbid_external=True)
        default_elem = tree.find("default")
        if default_elem is not None:
            self.defaults = {
                "remote": default_elem.get("remote", "unknown_remote"),
                "revision": default_elem.get("revision", "unknown_revision"),
            }

    def get_projects_for_remote(self, name: str) -> list[Project]:
        return [project for project in self.projects if project.remote.name == name]

    def remotes_by_type(self, host_type: str) -> list[Remote]:
        return [remote for remote in self.remotes if remote.host_type == host_type]
