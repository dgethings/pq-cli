"""CLI argument parsing module."""

from pathlib import Path
import sys

import typer
from rich import print

from pq.config import load_config
from pq.evaluator import evaluate_query
from pq.loader import content_from_file, load_content
from pq.cli_arg import Query, FilePath, FileType, Theme, Version
from pq.tui import QueryApp

app = typer.Typer()


@app.command()
def main(
    query: Query,
    file_path: FilePath = None,
    file_type: FileType = None,
    theme: Theme = None,
    v: Version = None,
) -> None:
    """Run a query against a document.

    Query a document using Python syntax.
    Reads from a file or stdin and evaluates the query against document data.
    """
    data = None
    if file_path is None and file_type is None and not Path(query).exists():
        raise typer.BadParameter(
            "Must supply either file path or if reading from stdin must supply file type"
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
    if file_type and not (query or file_path):
        content = sys.stdin.read()
    if not file_type and not (file_path and query):
        raise typer.BadParameter("when reading from stdin you must supply a file type")

    data = load_content(content=content, file_type=file_type, src=src)
    result = evaluate_query(query, data)
    print(result)


if __name__ == "__main__":
    app()
