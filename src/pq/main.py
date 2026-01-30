from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Input, Static
from textual.widget import Widget
import sys


class QueryPrompt(Widget):
    """Where the user enters fuzzy findable string"""

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Static("> ", id="prompt")
            yield Input(placeholder="query prompt", id="query-input")


class Querier(App[None]):
    """The app"""

    def __init__(self, file: Path) -> None:
        self.file = file
        super().__init__()

    def compose(self) -> ComposeResult:
        yield QueryPrompt()
        yield Static("fuzzy match")
        yield Static(self.file.read_text())

    def on_mount(self) -> None:
        self.query_one(Input).focus()


def run_app():
    file = Path(sys.argv[1])
    if not file.exists():
        raise ValueError("path to file to query is required")
    Querier(file).run()


if __name__ == "__main__":
    run_app()
