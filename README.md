# pq-cli

<div align="center">

**Interactive Python Query CLI Tool**

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

</div>

`pq-cli` is a command-line tool that enables interactive querying of structured documents using Python expressions. It provides a real-time terminal UI (TUI) where you can type Python data structure syntax and instantly see matching results.

## Features

- **Real-time query evaluation** - See results update instantly as you type
- **Pure Python syntax** - No DSL to learn, use familiar Python expressions
- **Multiple format support** - Query JSON, YAML, XML, and TOML files
- **Fuzzy path completion** - Get smart suggestions as you type
- **Seamless piping** - Exit with Enter and pipe results to other commands
- **Safe evaluation** - Only safe builtins available
- **Color themes** - Choose from 18 built-in Textual themes

## Why does this exist?

Tools like `jq` and `yq` provide command line querying of JSON  and YAML files respectively. However there is a (steep) learning curve with the query language. This command line tool supports both JSON, YAML and more and uses Python syntax to query it.

I honestly don't know if that is a good idea. It might utterly useless. It might be helpful if you don't know how, or want, to use the Python REPL to construct the Python code to traverse a data structure. For me it was a good opportunity to better learn Typer and Textual.
## Installation

### Requirements

- Python 3.11 or higher

### From PyPI (recommended)

#### Using pip
```bash
pip install pq-cli
```

#### Using uv
```bash
uv add pq-cli
```

#### Using uv tool install
```bash
uv tool install pq-cli
```

#### Using uvx (run without installing)
```bash
uvx pq-cli "_" data.json
```

### From source with uv (recommended for development)

```bash
git clone https://github.com/dgethings/pq-cli.git
cd pq-cli
uv sync
uv run pq-cli --help
```

### From source with pip

```bash
git clone https://github.com/dgethings/pq-cli.git
cd pq-cli
pip install -e .
```

## Quick Start

```bash
# Query a JSON file
pq-cli "_" examples/employees.json

# Query a YAML file
pq-cli "_" examples/products.yaml

# Query a TOML file
pq-cli "_" examples/products.toml

# Query an XML file
pq-cli "_" examples/products.xml

# Use a specific theme
pq-cli "_" examples/employees.json --theme dracula

# Pipe from another command
cat examples/users.json | pq-cli -j

# Query and pipe to another tool
pq-cli "_" examples/employees.json | jq '.'

### File Type Flags for stdin

When piping data to `pq-cli` from stdin, you must specify the file format:

```bash
# Read JSON from stdin
cat data.json | pq-cli -j

# Read YAML from stdin
cat data.yaml | pq-cli --yaml

# Read XML from stdin
curl -s https://example.com/data.xml | pq-cli -x

# Read TOML from stdin
cat config.toml | pq-cli --toml
```

Only one file type flag may be specified at a time.
```

## Usage

### Basic Queries

```python
# Load entire document
_

# Access a nested key
_['employees']

# Access an array element
_['employees'][0]

# Access a deeply nested value
_['employees'][0]['name']
```

### Advanced Queries

```python
# List comprehension
[emp['name'] for emp in _['employees']]

# Filter list
[emp for emp in _['employees'] if emp['salary'] > 100000]

# Get length
len(_['employees'])

# Get unique values
list(set(emp['department'] for emp in _['employees']))

# Sort items
sorted(_['employees'], key=lambda x: x['salary'], reverse=True)

# Nested filtering
[proj['name'] for emp in _['employees'] for proj in emp['projects'] if proj['status'] == 'completed']
```

### Available Functions

The following Python builtins are available in your queries:

- **Collection operations**: `len`, `sum`, `min`, `max`, `sorted`
- **Type conversions**: `list`, `dict`, `set`, `tuple`, `str`, `int`, `float`, `bool`
- **Functional**: `filter`, `map`, `any`, `all`
- **Iteration**: `range`, `zip`, `enumerate`
- **Other**: `type`, `isinstance`, `abs`, `round`, `slice`

## Configuration

You can configure `pq` using a config file or command-line argument.

### Color Themes

`pq` supports 18 built-in Textual color themes:

```
atom-one-dark, atom-one-light, catppuccin-latte, catppuccin-mocha,
dracula, flexoki, gruvbox, monokai, nord, rose-pine,
rose-pine-dawn, rose-pine-moon, solarized-dark, solarized-light,
textual-ansi, textual-dark, textual-light, tokyo-night
```

### Config File

Create a config file at either location (`.pq.toml` takes precedence):

- `./.pq.toml` (current directory)
- `$HOME/.config/pq/config.toml` (XDG config directory)

Example `~/.config/pq/config.toml`:
```toml
[theme]
name = "dracula"
```

### Command-Line Argument

Override config file with `--theme` or `-T`:

```bash
# Use dracula theme
pq-cli "_" data.json --theme dracula

# Use tokyo-night theme
pq-cli "_" data.yaml -T tokyo-night
```

### Priority Order

Theme selection follows this priority (highest to lowest):

1. CLI `--theme` argument
2. Local `.pq.toml` config file
3. `$HOME/.config/pq/config.toml` config file
4. Textual default theme

## Examples

### Example 1: Query Employee Data

```bash
pq-cli "_" examples/employees.json
```

Query: Find all engineers in the Engineering department
```python
[emp['name'] for emp in _['employees'] if emp['department'] == 'Engineering']
# Result: ["Alice Johnson", "Charlie Brown"]
```

Query: Get all completed project names
```python
[proj['name'] for emp in _['employees'] for proj in emp['projects'] if proj['status'] == 'completed']
# Result: ["Project A", "Project C", "Project A"]
```

Query: Calculate average salary
```python
sum(emp['salary'] for emp in _['employees']) / len(data['employees'])
# Result: 105000.0
```

### Example 2: Query Product Inventory

```bash
pq-cli "_" examples/products.yaml
```

Query: Find products in Electronics category
```python
[prod['name'] for prod in _['products'] if prod['category'] == 'Electronics']
# Result: ["Laptop", "Mouse", "Monitor"]
```

Query: Find products with low stock (< 30)
```python
[prod['name'] for prod in _['products'] if prod['stock'] < 30]
# Result: ["Desk"]
```

Query: Calculate total inventory value
```python
sum(prod['price'] * prod['stock'] for prod in _['products'])
# Result: 84749.25
```

### Example 3: Query User Settings

```bash
pq-cli "_" examples/users.json
```

Query: Get all active users with dark theme
```python
[user['name'] for user in _['users'] if user['active'] and user['settings']['theme'] == 'dark']
# Result: ["John Doe", "Bob Johnson"]
```

Query: Find users with admin role
```python
[user['name'] for user in _['users'] if 'admin' in user['roles']]
# Result: ["John Doe"]
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Accept query, exit, and print result to stdout |
| `Ctrl+C` | Cancel and exit without printing |
| Arrow keys | Navigate through query history |

## Supported File Formats

- **JSON** (.json)
- **YAML** (.yaml, .yml)
- **XML** (.xml)
- **TOML** (.toml)

## UI Elements

### Input Field
Type your Python expression at the `>` prompt. The result updates in real-time as you type.

### Result Display
Shows the evaluated result of your query. Errors are displayed in red with helpful messages.

### Status Bar
Provides helpful hints about available actions and current state.

## Troubleshooting

### "File not found" Error
- Verify the file path is correct
- Use absolute paths if relative paths don't work
- Check file permissions

### "Invalid [FORMAT]" Error
- Validate your document with a format-specific linter
- Check for syntax errors (missing commas, quotes, braces, etc.)
- Ensure the file is valid UTF-8 encoded
- Verify the file extension matches the format

### "Document must be a [FORMAT] object" Error
- The root of your document must be an object/dictionary, not an array
- For arrays, wrap them: `{"data": [...]}`

### "Key not found" Error
- Check the document structure with `data` query
- Verify exact spelling of keys (case-sensitive)
- Use list/dict methods to explore available keys

### "Type error" Error
- Ensure you're accessing dictionaries with `data['key']` syntax
- Check that list indices are integers: `data['items'][0]`
- Verify operations are compatible with your data types

### Performance Issues
- Large files (>100MB) may be slow
- Use filters to reduce dataset size early: `[x for x in data if x['field'] == value]`
- Avoid complex nested operations on large lists

## Limitations

- **File size**: Maximum 2GB (to prevent memory issues)
- **Builtins**: Only safe builtins available (no `exec`, `eval`, `__import__`)
- **Root type**: Root document must be an object/dict, not an array
- **Memory**: Entire file is loaded into memory

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/pq.git
cd pq

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

### Running the Application

```bash
# Run with uv
uv run pq-cli "_" examples/employees.json

# Or if installed with pip
pq-cli "_" examples/employees.json
```

### Code Quality

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

### Testing

```bash
# Run tests (requires pytest)
uv run pytest

# Run with coverage
uv run pytest --cov=pq --cov-report=html
```

## Contributing

Contributions are welcome! Please feel free to:

1. Report bugs via [GitHub Issues](https://github.com/dgethings/pq-cli/issues)
2. Suggest new features via [GitHub Discussions](https://github.com/dgethings/pq-cli/discussions)
3. Submit pull requests for bug fixes or new features

Before submitting PRs:
- Run linter: `uv run ruff check .`
- Format code: `uv run ruff format .`
- Add tests for new features
- Update documentation as needed

## Acknowledgments

Built with:
- [Textual](https://textual.textual.io/) - Terminal UI framework
- [Typer](https://typer.tiangolo.com/) - CLI application builder
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager

## Links

- [Issue Tracker](https://github.com/dgethings/pq-cli/issues)
- [Changelog](https://github.com/dgethings/pq-cli/blob/main/CHANGELOG.md)
