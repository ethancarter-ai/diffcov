# diffcov

Show whether the lines in your **current diff** are covered by tests, without converting the full report by untouched files.

## About

`diffcov` ships a small CLI that renders coverage for the exact changed lines between two git refs. By combining a parsed patch with `coverage` data, it isolates the signal that matters during code review and local development.

## Features

- Base-diff aware reporting, scoped to added lines
- Per-file and overall diff coverage percentage
- Rich table output in the terminal
- Built with typed data structures

## Installation

### From source

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

### Via pip (after publish)

```bash
pip install diffcov
```

## Usage

```bash
# Report diff coverage between main and current working tree
diffcov report --base main

# Experimentally run coverage for an app package, then report
diffcov report --base main --source app --run-coverage
```

## Project structure

```
diffcov/
  src/diffcov/
    __init__.py
    cli.py
    coverage_report.py
    diff.py
  tests/
  pyproject.toml
```

## License

[diffcov](https://github.com/ethancarter-ai/diffcov) is released under the MIT License.
