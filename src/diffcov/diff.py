import re
from pathlib import Path
from typing import Iterable


RE_PLUS_FILE = re.compile(r"^\+\+\+\s+b/(?P<path>[^\t]+)")
RE_PLUS_LINE = re.compile(r"^\+(?!\+)(?P<line>.+)$")
RE_MINUS_LINE = re.compile(r"^-(?!-)(?P<line>.+)$")
RE_HUNK = re.compile(r"^@@ .+ \+(\d+),?(?P<length>\d+)? .*$")


def parse_diff(diff_text: str) -> list[dict]:
    entries: list[dict] = []
    current: dict | None = None
    line_no: int | None = None

    def reset() -> None:
        nonlocal current, line_no
        current = None
        line_no = None

    def start_hunk(match: re.Match[str]) -> None:
        nonlocal line_no
        line_no = int(match.group(1)) - 1

    def add_line(line: str) -> None:
        nonlocal line_no
        if current is None or line_no is None:
            return
        current.setdefault("additions", []).append((Path(current["path"]), line, line_no))
        line_no += 1

    for raw_line in diff_text.splitlines():
        if raw_line == "" or raw_line.isspace():
            continue
        line = raw_line.rstrip(" ")

        if re.match(r"^diff --git ", line):
            reset()
            continue

        if re.match(r"^\+\+\+ b/", line):
            m = RE_PLUS_FILE.match(line)
            if m:
                current = {"path": m.group("path")}
            continue

        if line.startswith("@@"):
            start_hunk(RE_HUNK.match(line))
            continue

        if line.startswith("+") and not line.startswith("+++"):
            add_line(line[1:])
            continue

        if line.startswith("-"):
            if current is not None:
                current.setdefault("lint", []).append(line[1:])
            continue

        if current is not None:
            current.setdefault("context", []).append(line)
            continue

    if current and current.get("path"):
        entries.append(current)

    return entries


def changed_paths(repo_root: Path) -> Iterable[Path]:
    repo_root = Path(repo_root).resolve()
    for path in repo_root.rglob("*"):
        if path.is_file() and ".git" in path.parts:
            continue
        yield path
