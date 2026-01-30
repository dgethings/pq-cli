# pq - AGENTS.md

## Issue Tracking

This project uses **bd (beads)** for issue tracking.
Run `bd prime` for workflow context, or install hooks (`bd hooks install`) for auto-injection.

**Quick reference:**
- `bd ready` - Find unblocked work
- `bd create "Title" --type task --priority 2` - Create issue
- `bd close <id>` - Complete work
- `bd sync` - Sync with git (run at session end)

For full workflow details: `bd prime`
--- END AGENTS.MD CONTENT ---

For GitHub Copilot users:
Add the same content to .github/copilot-instructions.md

How it works:
   • bd prime provides dynamic workflow context (~80 lines)
   • bd hooks install auto-injects bd prime at session start
   • AGENTS.md only needs this minimal pointer, not full instructions

This file contains guidelines and commands for agentic coding assistants working in this repository.

## Project Overview

This is a Python CLI/TUI application using:
- **textual** - Terminal User Interface framework
- **typer** - Elegant CLI application builder
- **Python 3.11+** - Required minimum version
- **uv** - Fast Python package and project manager

## Build / Lint / Test Commands

### Code Quality (Always run these before committing)
```bash
# Lint check
uv run ruff check .

# Auto-fix lint issues
uv run ruff check . --fix

# Format code
uv run ruff format .

# Check formatting without modifying
uv run ruff format --check .
```

### Running the Application
```bash
# Run the main application
uv run pq

# Run main module directly
uv run python -m pq.main

# Run with entry point
uv run python -m pq.main
```

### Running Tests
No test framework is currently configured. When adding tests:
- Consider using pytest with `uv add pytest pytest-cov`
- Run single test: `uv run pytest tests/test_module.py::test_function -v`
- Run all tests: `uv run pytest`
- Run with coverage: `uv run pytest --cov=pq`

### Package Management
```bash
# Add a dependency
uv add <package>

# Add dev dependency
uv add --dev <package>

# Remove dependency
uv remove <package>

# Update dependencies
uv sync
```

## Code Style Guidelines

### Imports and Module Structure
- Place all imports at the top of the file
- Group imports: stdlib → third-party → local
- Use absolute imports for local modules
- Remove unused imports (ruff will catch these)

### Formatting (Ruff)
- Use **double quotes** for strings
- Maximum line length: 88 characters (Ruff default)
- Indentation: 4 spaces
- No trailing whitespace
- One blank line between top-level definitions
- Two blank lines before classes, one before functions

### Type Annotations
- Always include return type hints on functions: `def foo() -> ReturnType:`
- Use type hints for parameters when types are non-obvious
- Import from typing as needed: `from typing import ComposeResult`
- Textual's `ComposeResult` is used in `compose()` methods

### Naming Conventions
- **Classes**: PascalCase (e.g., `QueryPrompt`, `FuzzyMatch`)
- **Functions/Methods**: snake_case (e.g., `compose`, `run_app`)
- **Variables**: snake_case
- **Constants**: UPPER_SNAKE_CASE
- **Private methods**: leading underscore (e.g., `_internal_method`)

### Classes and Structure
- Use Textual's `App` and `Widget` as base classes
- Implement `compose(self) -> ComposeResult:` for widget composition
- Use `yield` to compose child widgets
- Add docstrings to classes describing their purpose
- Keep classes focused on single responsibility

### Error Handling
- Use Textual's built-in exception handling mechanisms
- Let Textual handle UI-related errors
- Use proper exception types from standard library

### Docstrings
- Use triple double quotes: `"""Docstring"""`
- Keep docstrings concise and descriptive
- Document class purpose, not implementation details

### File Organization
```
src/pq/
├── __init__.py    # Package initialization (can be empty)
└── main.py        # Main application entry point
```

## Working with Textual

### App Structure
- The main app inherits from `textual.app.App`
- Apps can be generic: `App[ReturnType]` to specify return type
- Use `compose(self) -> ComposeResult:` to define widget hierarchy
- Use `yield` to compose child widgets
- Export app instance for CLI entry point (e.g., `app = MyApp()`)
- Entry point defined in pyproject.toml: `pq = "pq.main:app"`

### Widget Structure
- Custom widgets inherit from `textual.widget.Widget` or subclasses like `Static`
- Use `render(self) -> RenderResult:` to define widget content
- For Static widgets, use `update()` method to change content
- Set `can_focus=True` parameter for focusable widgets
- Add docstrings to describe widget purpose

### Event Handling
- Event handlers use `on_` prefix (e.g., `on_mount`, `on_key`, `on_button_pressed`)
- Event handlers can be async (use `async def`)
- Use `@on(Event)` decorator for concise handler definitions
- Event objects are passed as parameters when needed

### CSS and Styling
- Use `.tcss` extension for Textual CSS files
- Use `CSS_PATH = "path.tcss"` class variable to reference external CSS
- Use `CSS = """..."""` class variable for inline CSS in apps
- Use `DEFAULT_CSS = """..."""` class variable in widgets for default styles
- CSS in `DEFAULT_CSS` is scoped by default
- App-level CSS takes precedence over widget `DEFAULT_CSS`

### Reactive Programming
- Use `reactive` decorator from `textual.reactive` for reactive attributes
- Reactive watchers use `watch_` prefix (e.g., `watch_count`)
- Define watchers as methods: `def watch_<attribute>(self, old_value, new_value) -> None`

### Actions and Bindings
- Action methods use `action_` prefix (e.g., `action_next_word`)
- Define bindings in `BINDINGS` class variable: `[("key", "action", "description")]`
- Multiple keys can map to same action: `("up,k", "change_count(1)", "Increment")`
- Actions support parameters: `change_count(1)` passes `1` to action method

### Import Types
- `ComposeResult` from `textual.app` for compose() return type
- `RenderResult` from `textual.app` for render() return type
- `Composable` from `textual.app` for type hints

### Widget Composition
- Use `self.mount(widget)` to add widgets dynamically
- Use `await self.mount(widget)` if you need to access mounted widget immediately
- Use `self.query_one(WidgetType)` to find a specific widget
- Use `self.query(WidgetType)` to find multiple widgets

### Common Patterns
- Initialize state in `on_mount()` handler
- Exit app with `self.exit(return_value)` or `self.exit(return_code=n)`
- Set title/subtitle via `TITLE` and `SUB_TITLE` class variables
- Use tooltips via widget's `tooltip` property
- For static content widgets, prefer `Static` over `Widget` base class

## Development Notes

- The project uses uv for all Python operations (per AGENTS.md uv rules)
- Python version is pinned to 3.11 in `.python-version`
- Virtual environment is `.venv/` (auto-generated by uv)
- Ruff cache is in `.ruff_cache/`
- Always prefer `uv run` over direct python/pip commands

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
