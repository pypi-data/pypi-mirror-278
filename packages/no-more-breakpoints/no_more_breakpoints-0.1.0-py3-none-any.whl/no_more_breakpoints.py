import click
from pathlib import Path
import subprocess

import sys


@click.group()
def cli():
    pass


def validate_file(file: Path) -> None:
    sys.tracebacklimit = 0
    res = subprocess.run(["rg", r"breakpoint\(\)", file], capture_output=True)
    if res.stdout:
        raise ValueError(f"Found at least one breakpoint in {file}.")


@cli.command("validate")
@click.argument(
    "file_paths", type=click.Path(exists=True, file_okay=True, dir_okay=False), nargs=-1
)
def validate(file_paths):
    for file_path in file_paths:
        path = Path(file_path)
        validate_file(path)
