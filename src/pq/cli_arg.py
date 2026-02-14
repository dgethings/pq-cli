from typing import Annotated
from pathlib import Path
import typer
import importlib.metadata
from pq.types import FileTypes


def version_callback(v: bool) -> None:
    if v:
        print(f"pq Version: {importlib.metadata.version(distribution_name='pq')}")
        raise typer.Exit(0)


Query = Annotated[
    str,
    typer.Argument(help="Python expression that returns a subset of given file"),
]
FilePath = Annotated[
    Path | None, typer.Argument(help="Input file, use '-' to read from stdin")
]
FileType = Annotated[
    FileTypes | None,
    typer.Option(
        "--file-type",
        "-f",
        help="When reading from stdin you need to specify the file format",
    ),
]
Theme = Annotated[
    str | None,
    typer.Option(
        "--theme",
        "-t",
        help="Textual color theme (overrides config file)",
    ),
]
Version = Annotated[
    bool | None,
    typer.Option(
        "--version",
        "-v",
        help="show version information",
        callback=version_callback,
    ),
]
