#!/usr/bin/env python3
"""Normalize MDX/Markdown pipe tables so columns align vertically.

Per the Domo KB Style Guide (Tables): pipe tables must be padded with
spaces so columns align across all rows, including the separator row.

Usage:
    python3 scripts/pad_md_tables.py FILE [FILE ...]

Reformats every pipe table in place. Skips fenced code blocks. Cells are
padded per the column's alignment (`:--`, `:-:`, `--:`); the separator row
uses dashes sized to each column. Cell contents are not otherwise modified;
escaped \\| stays inside its cell. Output matches the MDX formatter, so
running both on a file never makes them fight.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


def _split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


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
    """Display width, matching the string-width package the MDX formatter uses:
    East Asian wide chars count 2, and a combining mark (e.g. a decomposed
    dakuten) or joined emoji part adds nothing to the character it follows."""
    import unicodedata
    w = 0
    last = 0
    joined = False
    for ch in s:
        cp = ord(ch)
        if cp <= 0x1F or 0x7F <= cp <= 0x9F:
            continue
        if ch == "‍":
            joined = True
            continue
        if joined or unicodedata.category(ch).startswith("M"):
            if ch == "️" and last == 1:
                w += 1
                last = 2
            joined = False
            continue
        last = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        w += last
    return w


def _pad(cell: str, width: int, align: str) -> str:
    space = width - _wcwidth(cell)
    if align == "right":
        return " " * space + cell
    if align == "center":
        return " " * (space - space // 2) + cell + " " * (space // 2)
    return cell + " " * space


def _format_table(rows: list[list[str]]) -> list[str]:
    # Matches remark's table output (markdown-table) so the two tools agree.
    # GFM renders only the header's columns, so rows are cut or padded to it.
    ncols = len(rows[0])
    rows = [(r + [""] * ncols)[:ncols] for r in rows]
    aligns = []
    for c in rows[1]:
        left, right = c.startswith(":"), c.endswith(":")
        aligns.append("center" if left and right else "right" if right else "left" if left else "")
    data_rows = [rows[0]] + rows[2:]
    widths = [max(_wcwidth(r[i]) for r in data_rows) for i in range(ncols)]
    seps = []
    for i, align in enumerate(aligns):
        left = align in ("left", "center")
        right = align in ("right", "center")
        sep = (":" if left else "") + "-" * max(1, widths[i] - left - right) + (":" if right else "")
        widths[i] = max(widths[i], len(sep))
        seps.append(sep)
    row = lambda cells: "| " + " | ".join(_pad(c, widths[i], aligns[i]) for i, c in enumerate(cells)) + " |"
    return [row(rows[0]), row(seps)] + [row(r) for r in rows[2:]]


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
                # preserve the block's leading indentation (e.g. a table
                # nested inside an ordered-list item) on every rebuilt row
                indent = line[: len(line) - len(line.lstrip())]
                out.extend(indent + r for r in _format_table(rows))
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
