#!/usr/bin/env python3
"""
html-table-to-mdx.py — convert HTML <table> blocks in stdin to padded pipe
tables and write to stdout.

Designed to be wired up to VS Code: select a <table>...</table> block, run
the "Convert HTML table to pipe table" task, and the selection is replaced
with a pipe table that conforms to Domo-KB-Style-Guide.mdx › Tables.

Each <table>…</table> block is replaced independently; surrounding text in
the input is passed through unchanged. A table is left as HTML (with a
warning written to stderr) if it uses features pipe tables can't express:

  - rowspan or colspan > 1
  - nested tables
  - block elements in cells (<ul>, <ol>, <h1>-<h6>, blockquote, pre, hr)

Pure regex, no external dependencies. Tolerant of MDX/JSX inside cells
(<img style={{...}}/>, <Note>, etc.) — those are preserved verbatim.
"""

import re
import sys

TABLE_RE = re.compile(r"<table\b[^>]*>.*?</table>", re.IGNORECASE | re.DOTALL)
ROW_RE = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.IGNORECASE | re.DOTALL)
CELL_RE = re.compile(r"<t([hd])\b[^>]*>(.*?)</t\1>", re.IGNORECASE | re.DOTALL)
THEAD_RE = re.compile(r"<thead\b[^>]*>(.*?)</thead>", re.IGNORECASE | re.DOTALL)
TBODY_RE = re.compile(r"<tbody\b[^>]*>(.*?)</tbody>", re.IGNORECASE | re.DOTALL)
OUTER_P_RE = re.compile(r"^\s*<p\b[^>]*>(.*)</p>\s*$", re.IGNORECASE | re.DOTALL)


def warn(msg):
    print(f"html-table-to-mdx: {msg}", file=sys.stderr)


def has_unsupported(html):
    """Return reason string if this table can't be converted, else None."""
    for m in re.finditer(r'(?:row|col)span\s*=\s*["\']?(\d+)', html, re.IGNORECASE):
        if int(m.group(1)) > 1:
            return f"uses {m.group(0)} — pipe tables can't express row/col spans"
    if len(re.findall(r"<table\b", html, re.IGNORECASE)) > 1:
        return "contains a nested <table>"
    for _, content in CELL_RE.findall(html):
        inner = OUTER_P_RE.sub(r"\1", content)
        if re.search(r"<(ul|ol|li|h[1-6]|blockquote|pre|hr)\b", inner, re.IGNORECASE):
            return "a cell contains a block element (<ul>, <ol>, <h1>–<h6>, etc.)"
    return None


def clean_cell(html):
    c = html.strip()
    c = OUTER_P_RE.sub(r"\1", c).strip()
    c = re.sub(r"<br\s*/?>", "<br/>", c, flags=re.IGNORECASE)
    c = re.sub(r"\s+", " ", c)
    c = c.replace("|", r"\|")
    return c.strip()


def extract_rows(html):
    return [
        [m.group(2) for m in CELL_RE.finditer(row.group(1))]
        for row in ROW_RE.finditer(html)
    ]


def convert_table(html):
    reason = has_unsupported(html)
    if reason:
        warn(f"skipped table — {reason}")
        return html

    thead = THEAD_RE.search(html)
    tbody = TBODY_RE.search(html)

    header_rows = extract_rows(thead.group(1)) if thead else []
    body_rows = extract_rows(tbody.group(1)) if tbody else []

    if not thead and not tbody:
        all_rows = extract_rows(html)
        if not all_rows:
            warn("no rows found")
            return html
        header_rows, body_rows = [all_rows[0]], all_rows[1:]

    # Legacy migration artifact: data rows stuffed inside <thead>, no <tbody>
    if header_rows and not body_rows and len(header_rows) > 1:
        warn("data rows were inside <thead>; using first row as header, rest as body")
        body_rows = header_rows[1:]
        header_rows = header_rows[:1]

    if not header_rows:
        warn("no header row — pipe tables require one")
        return html
    if len(header_rows) > 1:
        warn(f"multi-row header ({len(header_rows)} rows); using only the first")

    header = [clean_cell(c) for c in header_rows[0]]
    rows = [[clean_cell(c) for c in r] for r in body_rows]

    ncols = len(header)
    for i, r in enumerate(rows):
        while len(r) < ncols:
            r.append("")
        if len(r) > ncols:
            warn(f"row {i + 1} has {len(r)} cells (header has {ncols}); truncating")
            del r[ncols:]

    widths = [max(3, max(len(r[i]) for r in [header] + rows)) for i in range(ncols)]

    def fmt(cells):
        return "| " + " | ".join(c.ljust(widths[i]) for i, c in enumerate(cells)) + " |"

    lines = [fmt(header), "| " + " | ".join("-" * w for w in widths) + " |"]
    lines.extend(fmt(r) for r in rows)
    return "\n".join(lines)


def main():
    text = sys.stdin.read()
    sys.stdout.write(TABLE_RE.sub(lambda m: convert_table(m.group(0)), text))


if __name__ == "__main__":
    main()
