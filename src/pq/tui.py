"""Main Textual application module."""

from typing import Any, ClassVar, cast

from rich.syntax import Syntax
from textual._path import CSSPathType
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.widgets import Footer, Header, OptionList, Static
from textual.widgets.option_list import Option
from textual.widgets._input import Input as BaseInput, Selection
from textual.widget import Widget

from pq.completion import FuzzyMatcher, PathExtractor
from pq.evaluator import QueryEvaluationError, evaluate_query
from pq.output import OutputFormatter
from pq.theme_mapping import map_theme_to_pygments


class QueryInput(BaseInput):
    """Custom input widget with tab support."""

    def on_key(self, event) -> None:
        """Handle key events for tab navigation.

        Args:
            event: Key event
        """
        if event.key == "tab":
            event.stop()
            option_list = cast(QueryApp, self.app).query_one(
                "#suggestion-list", OptionList
            )
            suggestion_box = cast(QueryApp, self.app).query_one(
                "#suggestion-box", SuggestionBox
            )
            if suggestion_box.suggestions:
                option_list.highlighted = 0
                option_list.focus()


class QueryPrompt(Widget):
    """Input prompt for Python expressions."""

    def __init__(self, query: str) -> None:
        self.query_string: str = query
        super().__init__()

    def on_mount(self) -> None:
        """Position cursor at end of input value to prevent replacement."""
        input_widget = self.query_one("#query-input", QueryInput)
        input_widget.cursor_position = len(self.query_string)

    def on_input_submitted(self, event: QueryInput.Submitted) -> None:
        """Handle Enter key press in the input field.

        Args:
            event: Input submitted event
        """
        event.stop()
        cast(QueryApp, self.app).action_accept_query()

    def compose(self) -> ComposeResult:
        yield QueryInput(
            value=self.query_string,
            placeholder="Enter Python expression, use '_' to access data",
            id="query-input",
        )


class ResultDisplay(Static):
    """Display query results or errors."""

    def update_result(self, result: Any, is_error: bool = False) -> None:
        """Update the display with new result.

        Args:
            result: Result to display
            is_error: Whether this is an error message
        """
        if is_error:
            self.update(f"[error]{result}[/error]")
        else:
            formatted = OutputFormatter.format_output(result)
            pygments_theme = map_theme_to_pygments(cast(QueryApp, self.app).theme)
            syntax = Syntax(formatted, "json", theme=pygments_theme, line_numbers=False)
            self.update(syntax)


class SuggestionBox(Widget):
    """Display fuzzy path suggestions."""

    def __init__(self, id: str | None = None) -> None:
        self.suggestions: list[str] = []
        super().__init__(id=id)

    def update_suggestions(self, suggestions: list[str]) -> None:
        """Update the suggestions display.

        Args:
            suggestions: List of suggestion strings
        """
        self.suggestions = suggestions[:10]
        option_list = self.query_one("#suggestion-list", OptionList)
        option_list.clear_options()

        pygments_theme = map_theme_to_pygments(cast(QueryApp, self.app).theme)

        for suggestion in self.suggestions:
            syntax = Syntax(
                suggestion, "python", theme=pygments_theme, line_numbers=False
            )
            option_list.add_option(Option(syntax))

        header = self.query_one("#suggestion-header", SectionHeader)
        if not suggestions:
            self.remove_class("visible")
            header.remove_class("visible")
        else:
            self.add_class("visible")
            header.add_class("visible")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle suggestion selection.

        Args:
            event: Option selected event
        """
        event.stop()
        suggestion = str(event.option.prompt)
        input_widget = cast(QueryApp, self.app).query_one("#query-input", QueryInput)
        input_widget.value = suggestion
        input_widget.focus()
        end_pos = len(suggestion)
        input_widget.selection = Selection.cursor(end_pos)

    def compose(self) -> ComposeResult:
        yield SectionHeader("Suggestions", id="suggestion-header")
        yield OptionList(id="suggestion-list")


class SectionHeader(Static):
    """Section header for UI sections."""

    def __init__(self, title: str, id: str | None = None) -> None:
        super().__init__(f"[dim]{title}[/dim]", id=id)


class StatusBar(Static):
    """Display status and helpful hints."""

    def set_status(self, message: str) -> None:
        """Update the status message.

        Args:
            message: Status message to display
        """
        self.update(f"[dim]{message}[/dim]")


class QueryApp(App[None]):
    """Main Textual application for interactive Python querying."""

    CSS_PATH: ClassVar[CSSPathType | None] = "styles.tcss"
    TITLE: str | None = "pq - Interactive Python Query Tool"
    SUB_TITLE: str | None = "Type Python expressions to query your data"

    BINDINGS: ClassVar[list[BindingType]] = [
        ("ctrl+c", "quit", "Cancel & Quit"),
    ]

    def __init__(self, data: dict[str, Any], theme: str | None = None) -> None:
        """Initialize app with document data.

        Args:
            data: Document data to query
            theme: Textual theme name (optional)
        """
        self.data = data
        self.final_result: Any = None

        path_extractor = PathExtractor(data)
        self.paths = path_extractor.get_paths()
        self.fuzzy_matcher = FuzzyMatcher(self.paths)
        self.query_string: str = "_"

        super().__init__()

        if theme is not None:
            if theme not in self.available_themes:
                available = ", ".join(sorted(self.available_themes))
                raise ValueError(
                    f"Invalid theme '{theme}'. Available themes: {available}"
                )
            self.theme = theme

    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header()
        yield QueryPrompt(query=self.query_string)
        yield SuggestionBox(id="suggestion-box")
        yield SectionHeader("Results", id="results-header")
        yield ResultDisplay(id="result-display")
        yield StatusBar(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Set up the app on mount."""
        self.query_one("#query-input", QueryInput).focus()
        status_bar = self.query_one("#status-bar", StatusBar)
        status_bar.set_status(
            "Type a Python expression to query the data. Press Enter to exit."
        )

    def on_input_changed(self, event: QueryInput.Changed) -> None:
        """Handle input changes for real-time evaluation.

        Args:
            event: Input changed event
        """
        query = event.value
        result_display = self.query_one("#result-display", ResultDisplay)
        suggestion_box = self.query_one("#suggestion-box", SuggestionBox)

        if not query.strip():
            result_display.update_result("")
            suggestion_box.update_suggestions([])
            self.final_result = None
            return

        suggestions = self.fuzzy_matcher.find_matches(query)
        suggestion_box.update_suggestions(suggestions)

        try:
            result = evaluate_query(query, self.data)
            result_display.update_result(result, is_error=False)
            self.query_string = query
            self.final_result = result
        except QueryEvaluationError as e:
            result_display.update_result(str(e), is_error=True)
            self.final_result = None

    def action_accept_query(self) -> None:
        """Accept the current query and exit."""
        self.exit(return_code=0)

    async def action_quit(self) -> None:
        """Quit without printing."""
        self.exit(return_code=130)
