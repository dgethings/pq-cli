from typing import Annotated
from pathlib import Path
import typer
import importlib.metadata
from pq.types import FileTypes


def version_callback(v: bool) -> None:
    if v:
        print(
            f"pq-cli Version: {importlib.metadata.version(distribution_name='pq-cli')}"
        )
        raise typer.Exit(0)


Query = Annotated[
    str,
    typer.Argument(help="Python expression that returns a subset of given file"),
]
FilePath = Annotated[
    Path | None, typer.Argument(help="Input file, use '-' to read from stdin")
]
FileTypeJSON = Annotated[
    bool,
    typer.Option(
        "-j",
        "--json",
        help="Specify JSON format for stdin input",
    ),
]
FileTypeYAML = Annotated[
    bool,
    typer.Option(
        "-y",
        "--yaml",
        help="Specify YAML format for stdin input",
    ),
]
FileTypeXML = Annotated[
    bool,
    typer.Option(
        "-x",
        "--xml",
        help="Specify XML format for stdin input",
    ),
]
FileTypeTOML = Annotated[
    bool,
    typer.Option(
        "-t",
        "--toml",
        help="Specify TOML format for stdin input",
    ),
]
Theme = Annotated[
    str | None,
    typer.Option(
        "--theme",
        "-T",
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


def consolidate_file_type_flags(
    json_flag: bool,
    yaml_flag: bool,
    xml_flag: bool,
    toml_flag: bool,
) -> FileTypes | None:
    """Consolidate mutually exclusive file type flags.

    Args:
        json_flag: JSON format flag
        yaml_flag: YAML format flag
        xml_flag: XML format flag
        toml_flag: TOML format flag

    Returns:
        FileTypes value if exactly one flag is set, None otherwise

    Raises:
        typer.BadParameter: If more than one flag is set
    """
    flags_set = [json_flag, yaml_flag, xml_flag, toml_flag]
    flags_count = sum(flags_set)

    if flags_count == 0:
        return None

    if flags_count > 1:
        raise typer.BadParameter("Only one file type flag may be specified")

    if json_flag:
        return FileTypes.json
    if yaml_flag:
        return FileTypes.yaml
    if xml_flag:
        return FileTypes.xml
    return FileTypes.toml
