from pathlib import Path
from typing import Annotated

import typer

from repo_find_orphans.manifest import Manifest
from repo_find_orphans.scan import find_local_orphans
from repo_find_orphans.scan import find_remote_orphans
from repo_find_orphans.selections import Selections

app = typer.Typer()


@app.command(name="remote")
def find_remote_orphans_cmd(
    manifest_file: Annotated[Path, typer.Argument(help="Manifest file", exists=True, file_okay=True, dir_okay=False)],
    selections_file: Annotated[
        Path, typer.Argument(help="Selections file", exists=True, file_okay=True, dir_okay=False)
    ],
):
    manifest = Manifest(manifest_file)
    selections = Selections(selections_file)

    orphans = find_remote_orphans(manifest, selections)
    for orphan in orphans:
        print(orphan)  # noqa: T201


@app.command(name="local")
def find_local_orphans_cmd(
    manifest_file: Annotated[Path, typer.Argument(help="Manifest file", exists=True, file_okay=True, dir_okay=False)],
    project_dir: Annotated[Path, typer.Argument(help="Project directory", exists=True, file_okay=False, dir_okay=True)],
):
    manifest = Manifest(manifest_file)
    new_dirs = find_local_orphans(project_dir, manifest.projects)

    for orphan in new_dirs:
        print(orphan)  # noqa: T201


app()
