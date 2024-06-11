from pathlib import Path

from rich.console import Console
from rich.progress import track

from repo_find_orphans.manifest import Manifest
from repo_find_orphans.remote import GitHosting
from repo_find_orphans.selections import Selections
from repo_find_orphans.types.project import Project

ignored_files = {
    ".DS_Store",
}


def find_remote_orphans(manifest: Manifest, selections: Selections):
    github = GitHosting()
    projects = set(p.canonical_form for p in manifest.projects if p.host_type == "github")
    repos = github.get_repos()

    for repo in repos:
        if (f"{repo}.git" not in projects and repo not in projects) and repo in selections:
            yield repo


def find_local_orphans(path: Path, projects: list[Project]) -> set[Path]:
    project_paths = {Path(project.path) for project in projects}
    dirs: set[Path] = set()

    rglob = list(Path(path).rglob("*"))
    if Console().is_terminal:
        rglob = track(rglob, description="Scan: ")

    for gpath in rglob:
        # Filter out directories that are part of the project paths
        if gpath.is_dir():
            continue
        if gpath.name in ignored_files:
            continue

        clean_path = gpath.relative_to(Path(path))

        if any((str(clean_path.parent) + "/").startswith(str(proj_path) + "/") for proj_path in project_paths):
            continue
        if any(str(clean_path).startswith(str(proj_path)) for proj_path in dirs):
            continue

        dirs.add(clean_path.parent)

    return dirs
