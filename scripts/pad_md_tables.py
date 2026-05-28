#!/usr/bin/env python3
"""Normalize MDX/Markdown pipe tables so columns align vertically.

Per the Domo KB Style Guide (Tables): pipe tables must be padded with
spaces so columns align across all rows, including the separator row.

Usage:
    python3 scripts/pad_md_tables.py FILE [FILE ...]

Reformats every pipe table in place. Skips fenced code blocks. Cells are
left-aligned; the separator row uses dashes sized to each column. Cell
contents are not otherwise modified (no pipe characters inside cells are
expected; escaped \\| is preserved as-is).
"""
from __future__ import annotations
import sys
from pathlib import Path


def _split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def _is_sep(cells: list[str]) -> bool:
    if not cells:
        return False
    for c in cells:
        c = c.strip()
        if not c or set(c) - set("-:"):
            return False
        if "-" not in c:
            return False
    return True


def _wcwidth(s: str) -> int:
    """Approximate display width: count East Asian wide chars as 2."""
    import unicodedata
    w = 0
    for ch in s:
        w += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return w


def _pad(cell: str, width: int) -> str:
    return cell + " " * (width - _wcwidth(cell))


def _format_table(rows: list[list[str]]) -> list[str]:
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    # widths from header + data rows (skip the separator at index 1)
    data_rows = [rows[0]] + rows[2:]
    widths = [3] * ncols
    for r in data_rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], _wcwidth(c))
    out = []
    # header
    out.append("| " + " | ".join(_pad(c, widths[i]) for i, c in enumerate(rows[0])) + " |")
    # separator
    out.append("| " + " | ".join("-" * widths[i] for i in range(ncols)) + " |")
    # data
    for r in rows[2:]:
        out.append("| " + " | ".join(_pad(c, widths[i]) for i, c in enumerate(r)) + " |")
    return out


def process(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    in_fence = False
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue
        if not in_fence and line.strip().startswith("|") and i + 1 < len(lines):
            nxt = lines[i + 1]
            if nxt.strip().startswith("|") and _is_sep(_split_row(nxt)):
                # gather the full table block
                block = [line, nxt]
                j = i + 2
                while j < len(lines) and lines[j].strip().startswith("|"):
                    block.append(lines[j])
                    j += 1
                rows = [_split_row(b) for b in block]
                out.extend(_format_table(rows))
                i = j
                continue
        out.append(line)
        i += 1
    return "\n".join(out)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1
    for arg in sys.argv[1:]:
        p = Path(arg)
        original = p.read_text()
        updated = process(original)
        if updated != original:
            p.write_text(updated)
            print(f"padded tables in {arg}")
        else:
            print(f"no change {arg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
