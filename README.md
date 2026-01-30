# pq - Interactive Python Query Tool

`pq` is a command-line tool that enables interactive querying of structured documents using Python expressions. It provides a real-time terminal UI (TUI) where you can type Python data structure syntax and instantly see matching results.

## Features

- **Real-time query evaluation** - See results update instantly as you type
- **Pure Python syntax** - No DSL to learn, use familiar Python expressions
- **Fuzzy path completion** - Get smart suggestions as you type
- **Seamless piping** - Exit with Enter and pipe results to other commands
- **JSON support** - Load and query JSON files (TOML/XML coming soon)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd pq

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

## Quick Start

```bash
# Query a JSON file
pq data.json

# Pipe JSON from another command
cat data.json | pq

# Query and pipe to another tool
pq data.json | grep "Alice"
```

## Usage

### Basic Queries

```bash
# Load the entire document
data

# Access a nested key
data['items']

# Access an array element
data['items'][0]

# Access a deeply nested value
data['items'][0]['name']
```

### Advanced Queries

```bash
# List comprehension
[item['name'] for item in data['items']]

# Filter list
[item for item in data['items'] if item['age'] > 25]

# Get length
len(data['items'])

# Get unique values
list(set(item['city'] for item in data['items']))

# Sort items
sorted(data['items'], key=lambda x: x['age'])
```

### Available Functions

The following Python builtins are available in your queries:

- **Collection operations**: `len`, `sum`, `min`, `max`, `sorted`
- **Type conversions**: `list`, `dict`, `set`, `tuple`, `str`, `int`, `float`, `bool`
- **Functional**: `filter`, `map`, `any`, `all`
- **Iteration**: `range`, `zip`, `enumerate`
- **Other**: `type`, `isinstance`, `abs`, `round`, `slice`

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Accept query, exit, and print result to stdout |
| `Ctrl+C` | Cancel and exit without printing |
| Arrow keys | Navigate through suggestions (future) |
| `Tab` | Select path suggestion (future) |

## UI Elements

### Input Field
Type your Python expression at the `>` prompt. Suggestions appear automatically as you type.

### Suggestions Panel
Shows fuzzy-matched paths from your document. Type to filter, use arrows to navigate (coming soon).

### Result Display
Shows the query result in real-time. Errors are displayed in red.

### Status Bar
Provides helpful hints about available actions and current state.

## Examples

### Sample Data

```json
{
  "items": [
    {"name": "Alice", "age": 30, "city": "NYC", "active": true},
    {"name": "Bob", "age": 25, "city": "LA", "active": false},
    {"name": "Charlie", "age": 35, "city": "NYC", "active": true}
  ],
  "metadata": {
    "count": 3,
    "version": "1.0",
    "updated": "2026-01-30"
  }
}
```

### Example Queries

```python
# Get all names
[item['name'] for item in data['items']]
# Result: ["Alice", "Bob", "Charlie"]

# Get active users
[item['name'] for item in data['items'] if item['active']]
# Result: ["Alice", "Charlie"]

# Count items by city
from collections import Counter
Counter(item['city'] for item in data['items'])
# Result: Counter({'NYC': 2, 'LA': 1})

# Find maximum age
max(item['age'] for item in data['items'])
# Result: 35
```

## Troubleshooting

### "File not found" Error
- Verify the file path is correct
- Use absolute paths if relative paths don't work
- Check file permissions

### "Invalid JSON" Error
- Validate your JSON with a linter: `jq '.' data.json`
- Check for missing commas, quotes, or braces
- Ensure the file is valid UTF-8 encoded

### "Key not found" Error
- Use the fuzzy suggestions to find available keys
- Check the document structure with `data` query
- Verify the exact spelling of keys

### "Type error" Error
- Ensure you're accessing dictionaries with `data['key']` syntax
- Check that list indices are integers: `data['items'][0]`
- Verify operations are compatible with your data types

### Performance Issues
- Large files (>100MB) may be slow
- Use filters to reduce the dataset size early: `[x for x in data if x['field'] == value]`
- Avoid complex nested operations on large lists

## Limitations

- **File size**: Maximum 2GB (to prevent memory issues)
- **Format**: Currently supports JSON only (TOML/XML planned)
- **Builtins**: Only safe builtins available (no `exec`, `eval`, `__import__`)
- **Type**: Root document must be a JSON object (dict), not an array

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test
uv run pytest test_app.py
```

### Code Quality

```bash
# Lint
uv run ruff check .

# Format
uv run ruff format .
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

[Your License Here]

## Roadmap

### v0.2.0 (Planned)
- TOML format support
- XML format support
- Query history (up/down arrows)

### v0.3.0 (Planned)
- Tab completion
- Syntax highlighting
- Dark/light theme toggle

### Future Enhancements
- YAML format support
- CSV format support
- Multiple document tabs
- Query bookmarks
- Save/export queries
- Web UI mode
