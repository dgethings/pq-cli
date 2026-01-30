# PRD - Product Requirements Document

**Project**: `pq` - Python Query Tool
**Version**: 0.1.0
**Date**: 2026-01-30
**Status**: Planning Phase

---

## Table of Contents

1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Solution](#solution)
4. [Functional Requirements](#functional-requirements)
5. [Non-Functional Requirements](#non-functional-requirements)
6. [User Stories](#user-stories)
7. [Architecture](#architecture)
8. [Technical Implementation](#technical-implementation)
9. [Development Roadmap](#development-roadmap)
10. [Success Criteria](#success-criteria)
11. [Future Enhancements](#future-enhancements)

---

## Overview

`pq` is a command-line tool that enables interactive querying of structured documents using Python expressions. It provides a real-time terminal UI (TUI) where users can type Python data structure syntax and instantly see matching results, similar to the `jq-zsh-plugin` but built with Python and the Textual TUI framework.

### Key Behavior
Like the `jq-zsh-plugin`, when the user presses Enter, the app exits and prints the final query result to stdout, enabling seamless piping to other commands.

---

## Problem Statement

Developers often need to quickly explore and query structured data (JSON, YAML, etc.) to understand its structure or extract specific information. Existing tools like `jq` have a learning curve due to their custom query syntax, and interactive shells like the `jq-zsh-plugin` are tied to zsh.

**Current Challenges:**
- `jq` requires learning a domain-specific language
- No native Python alternative with interactive feedback
- Tools are either CLI-only (no real-time feedback) or shell-specific (zsh-only)
- Developers prefer using familiar Python syntax for data manipulation

---

## Solution

`pq` provides a Python-native interactive query tool with:
- Real-time query evaluation as you type
- Pure Python expression syntax (no DSL to learn)
- Fuzzy path completion for quick exploration
- Seamless integration into Unix pipelines
- Support for JSON (with TOML/XML planned)

---

## Functional Requirements

### FR1: Document Loading
- **FR1.1**: Load documents from file path argument
- **FR1.2**: Load documents from stdin (piped input)
- **FR1.3**: Support JSON format (v0.1.0)
- **FR1.4**: Reject files larger than 2GB with clear error message
- **FR1.5**: Validate file format and provide friendly error messages for malformed data

### FR2: Query Evaluation
- **FR2.1**: Evaluate Python expressions in real-time
- **FR2.2**: Provide `data` variable as context for the loaded document
- **FR2.3**: Restrict dangerous Python builtins for safety
- **FR2.4**: Display query results instantly as user types
- **FR2.5**: Show user-friendly error messages for invalid expressions

### FR3: Path Completion
- **FR3.1**: Extract all valid paths from the document structure
- **FR3.2**: Provide fuzzy matching for path suggestions
- **FR3.3**: Display suggestions as user types
- **FR3.4**: Allow selecting suggestions to auto-complete

### FR4: User Interface
- **FR4.1**: Provide input field for Python expressions
- **FR4.2**: Display query results in pretty-printed format
- **FR4.3**: Show document metadata (e.g., item count)
- **FR4.4**: Display status/error messages
- **FR4.5**: Support keyboard shortcuts (Enter to exit, Ctrl+C to cancel)

### FR5: Output & Piping
- **FR5.1**: Exit application when user presses Enter
- **FR5.2**: Print final result to stdout on exit
- **FR5.3**: Support piping results to other Unix commands
- **FR5.4**: Format output as JSON for structured data

### FR6: Error Handling
- **FR6.1**: Display friendly error messages (no stack traces)
- **FR6.2**: Show errors inline in the result panel
- **FR6.3**: Provide context for common errors (e.g., missing keys, type errors)

---

## Non-Functional Requirements

### NFR1: Performance
- **NFR1.1**: Query evaluation must be non-blocking (use workers)
- **NFR1.2**: Real-time updates within 100ms of keystroke
- **NFR1.3**: Support documents up to 2GB in size

### NFR2: Usability
- **NFR2.1**: Zero configuration required
- **NFR2.2**: Intuitive interface for Python developers
- **NFR2.3**: Clear error messages without technical jargon
- **NFR2.4**: Responsive UI with no noticeable lag

### NFR3: Compatibility
- **NFR3.1**: Python 3.11+ required
- **NFR3.2**: Works on Linux, macOS, and Windows
- **NFR3.3**: Compatible with terminal emulators supporting UTF-8

### NFR4: Security
- **NFR4.1**: Restrict dangerous Python builtins
- **NFR4.2**: Prevent code execution vulnerabilities
- **NFR4.3**: Validate file sizes before loading

### NFR5: Maintainability
- **NFR5.1**: Clean modular architecture
- **NFR5.2**: Comprehensive inline documentation
- **NFR5.3**: Type hints throughout codebase
- **NFR5.4**: Follow Python best practices (PEP 8, etc.)

---

## User Stories

### US1: Quick Document Exploration
> As a developer, I want to load a JSON file and quickly explore its structure using familiar Python syntax, so that I can understand the data without learning a new query language.

**Acceptance Criteria:**
- Can load JSON from file: `pq data.json`
- Can explore data: typing `data['items'][0]` shows immediate results
- See all keys and nested structures

### US2: Interactive Querying
> As a developer, I want to see query results in real-time as I type, so that I can quickly iterate on my queries without running a command repeatedly.

**Acceptance Criteria:**
- Results update instantly on each keystroke
- No lag or blocking during typing
- Errors appear immediately if syntax is invalid

### US3: Path Completion
> As a developer, I want fuzzy path suggestions as I type, so that I don't need to remember exact key names or navigate through deeply nested structures.

**Acceptance Criteria:**
- Suggestions appear as I type
- Can type partial key name and see matches
- Can select suggestion to auto-complete

### US4: Pipeline Integration
> As a developer, I want to pipe the query result to another command, so that I can integrate `pq` into my existing workflows.

**Acceptance Criteria:**
- Press Enter to exit and print result to stdout
- Can pipe to other tools: `pq data.json | grep "Alice"`
- Can receive input from pipes: `curl api.com/data | pq`

### US5: Error Feedback
> As a developer, I want clear, friendly error messages when my query is invalid, so that I can quickly fix mistakes without debugging cryptic error traces.

**Acceptance Criteria:**
- Errors displayed in plain English
- Errors explain what went wrong and how to fix it
- No stack traces or technical jargon

---

## Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────┐
│                    pq CLI Entry Point                   │
│              (handles args, pipes, file I/O)            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Document Loader & Validator                │
│         (file size check, parsing, error handling)      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 Textual Application                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │   Input Widget      │   Path Completion System  │   │
│  │   (Python expr)     │   (fuzzy finder)          │   │
│  └────────────────────┴─────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │   Query Evaluator     │   Pretty Display Widget  │   │
│  │   (safe eval)         │   (real-time results)    │   │
│  └────────────────────┴─────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            Output Handler (on Enter/Exit)               │
│         (pretty print to stdout for piping)              │
└─────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | File | Responsibility |
|-----------|------|----------------|
| **CLI Module** | `cli.py` | Parse arguments, handle stdin, invoke app |
| **Document Loader** | `loader.py` | Load files/pipes, validate size, detect format, parse |
| **Query Evaluator** | `evaluator.py` | Safely evaluate Python expressions with context |
| **Path Completion** | `completion.py` | Extract valid paths, provide fuzzy search suggestions |
| **Textual App** | `main.py` | Manage UI, handle events, coordinate components |
| **Output Handler** | `output.py` | Format results, print to stdout, handle piping |

### Module Dependencies

```
cli.py
  ├── loader.py
  ├── main.py
  └── output.py

main.py
  ├── evaluator.py
  ├── completion.py
  └── utils.py

loader.py (standalone)
evaluator.py (standalone)
completion.py (standalone)
output.py (standalone)
```

---

## Technical Implementation

### Project Structure

```
pq/
├── pyproject.toml           # Project config (uv, entry points, deps)
├── .python-version          # Python 3.11+
├── PRD.md                   # This document
├── README.md                # User documentation
├── AGENTS.md                # Agent guidelines
└── src/
    └── pq/
        ├── __init__.py      # Package init
        ├── __main__.py      # Entry point
        ├── main.py          # Main Textual app
        ├── cli.py           # CLI argument parsing
        ├── loader.py        # Document loading & validation
        ├── evaluator.py     # Query evaluation logic
        ├── completion.py    # Path completion & fuzzy matching
        ├── output.py        # Output formatting & printing
        ├── utils.py         # Shared utilities
        └── styles.tcss      # CSS for Textual UI
```

### Key Technical Decisions

#### 1. Why `eval()` vs `exec()`?
- `eval()` returns a value directly
- We want single expressions, not multi-line statements
- Better for REPL-style querying

#### 2. Why restrict builtins?
- **Security**: Prevent malicious code execution
- **Predictability**: Consistent behavior across environments
- **Simplicity**: Users know exactly what's available

#### 3. Why fuzzy matching instead of exact?
- Better UX for large documents
- More forgiving for typos
- Common in modern CLI tools (fzf, ripgrep)

#### 4. Why exit on Enter?
- Matches `jq-zsh-plugin` behavior
- Enables piping workflow
- Keeps session short and focused

#### 5. Why 2GB limit?
- Prevents loading huge files into memory
- Reasonable for typical use cases
- Can be increased if needed

### Security Considerations

1. **Restricted Builtins**: Only allow safe builtins (len, sum, map, filter, etc.)
2. **No File Access**: No file I/O in expressions
3. **No Network**: No network operations allowed
4. **No Code Execution**: Prevent `exec`, `eval`, `__import__`, etc.
5. **Size Validation**: Reject files > 2GB before loading

### Dependencies

```toml
[project]
name = "pq"
version = "0.1.0"
description = "Interactive Python query tool for structured documents"
requires-python = ">=3.11"
dependencies = [
    "textual>=0.50.0",
]

[project.scripts]
pq = "pq.cli:main"
```

---

## Development Roadmap

### Phase 1: Core Foundation (Week 1)

**Goal**: Establish project structure and basic functionality

**Tasks**:
- [ ] Set up project with `uv`
- [ ] Configure `pyproject.toml` with dependencies
- [ ] Create module structure
- [ ] Implement `loader.py` (JSON loading, size validation)
- [ ] Implement `evaluator.py` (safe eval with context)
- [ ] Implement `cli.py` (basic file/stdin handling)
- [ ] Test basic document loading with sample JSON

**Acceptance Criteria**:
- Can load JSON file from command line
- Can load JSON from stdin
- Validates file size (< 2GB)
- Shows friendly error messages

### Phase 2: Textual App (Week 1-2)

**Goal**: Build interactive TUI with real-time evaluation

**Tasks**:
- [ ] Implement `main.py` with Textual app skeleton
- [ ] Create UI layout (Header, Input, Pretty display, Footer)
- [ ] Implement real-time query evaluation
- [ ] Add error display in result panel
- [ ] Implement Enter key to exit
- [ ] Test with sample JSON files

**Acceptance Criteria**:
- TUI launches successfully
- Can type Python expressions
- Results update in real-time
- Errors display clearly
- Enter exits the app

### Phase 3: Path Completion (Week 2)

**Goal**: Add fuzzy path suggestions

**Tasks**:
- [ ] Implement `PathExtractor` class
- [ ] Extract all valid paths from document
- [ ] Implement `FuzzyMatcher` class
- [ ] Add suggestion dropdown/popover to UI
- [ ] Integrate with Input widget
- [ ] Test fuzzy matching with various data structures

**Acceptance Criteria**:
- Paths extracted from nested structures
- Fuzzy matching works for partial key names
- Suggestions appear as user types
- Can select suggestion to auto-complete

### Phase 4: Exit & Output (Week 2)

**Goal**: Handle exit and output for piping

**Tasks**:
- [ ] Implement `OutputFormatter` class
- [ ] Pretty print results as JSON
- [ ] Handle stdout printing on exit
- [ ] Test piping: `pq file.json | jq .`
- [ ] Test: `cat file.json | pq | grep pattern`
- [ ] Handle different result types (dict, list, primitive)

**Acceptance Criteria**:
- Enter key exits and prints result to stdout
- Results formatted as JSON for structured data
- Can pipe to other commands
- Can receive input from pipes

### Phase 5: Polish & Error Handling (Week 3)

**Goal**: Refine user experience and handle edge cases

**Tasks**:
- [ ] Add comprehensive error messages for all error types
- [ ] Test 2GB file size limit
- [ ] Test edge cases (empty files, malformed JSON, large files)
- [ ] Add keyboard shortcuts help to Footer
- [ ] Optimize query evaluation performance
- [ ] Add status bar with helpful hints
- [ ] Implement Cancel (Ctrl+C) action

**Acceptance Criteria**:
- Clear error messages for all scenarios
- Graceful handling of edge cases
- Good performance with large documents
- Helpful UI hints

### Phase 6: Documentation (Week 3)

**Goal**: Complete documentation for users and developers

**Tasks**:
- [ ] Write comprehensive README
- [ ] Document all modules with docstrings
- [ ] Add usage examples
- [ ] Create sample data files for testing
- [ ] Document keyboard shortcuts
- [ ] Add troubleshooting section

**Acceptance Criteria**:
- README covers all features
- All modules documented
- Examples provided for common use cases
- Troubleshooting guide available

---

## Success Criteria

### Technical Metrics
- [ ] All functional requirements implemented
- [ ] Query evaluation < 100ms response time
- [ ] Zero blocking operations in UI
- [ ] Files > 2GB rejected with clear message
- [ ] All unit tests passing
- [ ] All integration tests passing

### User Experience Metrics
- [ ] Can load and query JSON within 10 seconds
- [ ] No crashes or unhandled exceptions
- [ ] Clear error messages for all error scenarios
- [ ] Real-time updates visible on every keystroke
- [ ] Fuzzy completion works reliably
- [ ] Piping to other commands works seamlessly

### Quality Metrics
- [ ] Code follows PEP 8 style guidelines
- [ ] Type hints on all functions
- [ ] Docstrings on all modules and classes
- [ ] < 10% code duplication
- [ ] All imports organized and used

---

## Future Enhancements

### Post-MVP Features

#### Format Support
- [ ] TOML format support
- [ ] XML format support
- [ ] YAML format support
- [ ] CSV format support
- [ ] Format auto-detection

#### Advanced Querying
- [ ] Query history (up/down arrows)
- [ ] Save/bookmark favorite queries
- [ ] Multiple queries (tab switching)
- [ ] Query templates
- [ ] Export queries to file

#### UI Enhancements
- [ ] Syntax highlighting in input
- [ ] Color-coded results
- [ ] Dark/light theme toggle
- [ ] Customizable keyboard shortcuts
- [ ] Resizable panels

#### Data Handling
- [ ] Multiple documents (tab switching)
- [ ] Document comparison
- [ ] Merge/join documents
- [ ] Lazy loading for large files
- [ ] Pagination for large lists

#### Integration
- [ ] Copy to clipboard
- [ ] Export results to file
- [ ] Import from URL
- [ ] API mode (non-interactive)
- [ ] Web UI mode

---

## Appendix

### A. Example Usage

```bash
# Load from file
pq data.json

# Pipe from another command
cat data.json | pq

# Query and pipe to another tool
pq data.json | grep "Alice"

# Interactive examples:
# Type: data['items'][0]['name']
# Result shows immediately: "Alice"
# Press Enter: exits and prints "Alice" to stdout

# Complex query:
# Type: [item for item in data['items'] if item['age'] > 25]
# Result shows: [{"name": "Alice", "age": 30, ...}, ...]
```

### B. Sample Data Structure

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

### C. Allowed Python Builtins

```
len, sum, min, max, sorted, filter, map, list, dict, set,
tuple, str, int, float, bool, type, isinstance, range,
zip, enumerate, any, all, abs, round, slice
```

### D. Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Accept query, exit, and print result |
| `Ctrl+C` | Cancel and exit without printing |
| `Tab` | Select path suggestion (future) |
| `Esc` | Clear suggestions (future) |

---

**Document Version**: 1.0
**Last Updated**: 2026-01-30
**Maintained By**: Development Team
