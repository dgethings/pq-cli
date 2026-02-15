"""CLI argument parsing module."""

from pathlib import Path
import sys

import typer
from rich import print

from pq.config import load_config
from pq.evaluator import evaluate_query
from pq.loader import content_from_file, load_content
from pq.cli_arg import (
    Query,
    FilePath,
    FileTypeJSON,
    FileTypeYAML,
    FileTypeXML,
    FileTypeTOML,
    Theme,
    Version,
    consolidate_file_type_flags,
)
from pq.tui import QueryApp

app = typer.Typer()


@app.command()
def main(
    query: Query,
    file_path: FilePath = None,
    file_type_json: FileTypeJSON = False,
    file_type_yaml: FileTypeYAML = False,
    file_type_xml: FileTypeXML = False,
    file_type_toml: FileTypeTOML = False,
    theme: Theme = None,
    v: Version = None,
) -> None:
    """Run a query against a document.

    Query a document using Python syntax.
    Reads from a file or stdin and evaluates the query against document data.
    """
    data = None
    content = None
    file_type = consolidate_file_type_flags(
        file_type_json, file_type_yaml, file_type_xml, file_type_toml
    )
    if file_path is None and not file_type and not Path(query).exists():
        raise typer.BadParameter(
            "Must supply file path, or use a file type flag (-j/-y/-x/-t) when reading from stdin"
        )
    src = "stdin"
    if Path(query).exists():
        content, file_type = content_from_file(file_path=Path(query))
        data = load_content(content=content, file_type=file_type, src=query)

        config = load_config()
        selected_theme = theme or config.theme

        tui = QueryApp(data=data, theme=selected_theme)
        tui.run()
        result = str(tui.query_string)
        print(result)
        raise typer.Exit(0)

    if query and file_path:
        content, file_type = content_from_file(file_path=file_path)
        src = str(file_path)
    elif file_type and file_path is None:
        content = sys.stdin.read()
    if not file_type and not (file_path and query):
        raise typer.BadParameter(
            "When reading from stdin, you must specify file type with -j/--json, -y/--yaml, -x/--xml, or -t/--toml"
        )

    assert file_type is not None, "file_type must be set"
    assert content is not None, "content must be set"
    data = load_content(content=content, file_type=file_type, src=src)
    result = evaluate_query(query, data)
    print(result)


if __name__ == "__main__":
    app()
