#!/usr/bin/env python3
"""Roll the current Minor Release Notes into a dated weekly archive.

Companion to scripts/build_minor_release_notes.py. Before the build step
overwrites s/article/Current-Minor-Release-Notes.mdx with a new week, this
module copies the outgoing content to a dated archive file and registers it in
docs.json under the "Archived Minor Release Notes" group, nested Year -> Month
-> per-week page. It does NOT touch the published ledger (that is the build
step's job) and does NOT delete the current file (build overwrites it).

`roll_current_to_archive()` is imported and called by the build script when a
new week is being published. The CLI entry point runs the same roll standalone,
with --dry-run, for testing the nav insertion.

Mirrors the surgical-text-edit approach of archive-current-release-notes.py:
docs.json is not re-serialized (it contains inline arrays that a json round-trip
would reformat), so edits are inserted as text, with nested blocks built via
json.dumps and re-indented to match context.

Usage:
    python3 scripts/archive_minor_release_notes.py --dry-run
    python3 scripts/archive_minor_release_notes.py
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
CURRENT = ROOT / "s/article/Current-Minor-Release-Notes.mdx"
ARTICLE_DIR = ROOT / "s/article"
DOCS_JSON = ROOT / "docs.json"

ARCHIVE_GROUP = "Archived Minor Release Notes"
# The English nav entry that anchors the English Release Notes tab (first match).
ANCHOR = '"s/article/Current-Minor-Release-Notes"'

HEADING_RE = re.compile(r"^##\s+([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})\s+Release\s*$", re.MULTILINE)
TITLE_RE = re.compile(r'^title:\s*".*?"\s*$', re.MULTILINE)


def derive_release_date(text):
    """Parse the '## {Month} {D}, {Year} Release' heading into a date, or None
    when the file has no such heading (e.g. a go-live placeholder current)."""
    m = HEADING_RE.search(text)
    if not m:
        return None
    month, day, year = m.group(1), int(m.group(2)), int(m.group(3))
    try:
        return datetime.strptime(f"{month} {day} {year}", "%B %d %Y").date()
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# docs.json surgical editing
# --------------------------------------------------------------------------- #
def _match_bracket(text, open_idx):
    """Index of the ']' matching the '[' at open_idx (respecting strings)."""
    depth, i, in_str = 0, open_idx, False
    while i < len(text):
        ch = text[i]
        if ch == '"' and text[i - 1] != "\\":
            in_str = not in_str
        elif not in_str:
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    raise ValueError("Unbalanced brackets in docs.json")


def _pages_array_after(text, group_pos, limit=None):
    """Given the index of a '"group": "..."' key, return (open, close) of its
    sibling "pages" array. Searches only up to `limit` if given."""
    pages_kw = text.find('"pages"', group_pos)
    if pages_kw == -1 or (limit is not None and pages_kw >= limit):
        return None
    open_br = text.find("[", pages_kw)
    if open_br == -1:
        return None
    return open_br, _match_bracket(text, open_br)


def _item_indent(text, open_br, close_br):
    """Indentation string for items inside an array, inferred from existing
    entries or (empty array) from the array's own line indent + 2 spaces."""
    body = text[open_br + 1:close_br]
    first = re.search(r"\n([ \t]*)\S", body)
    if first:
        return first.group(1)
    line_start = text.rfind("\n", 0, open_br) + 1
    base = re.match(r"[ \t]*", text[line_start:]).group(0)
    return base + "  "


def _reindent_block(obj, indent):
    """json.dumps(obj) with every line prefixed by `indent`."""
    block = json.dumps(obj, indent=2, ensure_ascii=False)
    return "\n".join(indent + ln for ln in block.split("\n"))


def _append_to_array(text, open_br, close_br, obj):
    """Insert `obj` (dict or str) as a new last entry in the array."""
    indent = _item_indent(text, open_br, close_br)
    new_block = _reindent_block(obj, indent)
    body = text[open_br + 1:close_br]
    has_items = bool(re.search(r"\S", body))
    if has_items:
        # after the last entry (the char before close_br, trimmed of whitespace)
        insert_at = close_br
        while insert_at > open_br and text[insert_at - 1] in " \t\r\n":
            insert_at -= 1
        return text[:insert_at] + ",\n" + new_block + text[insert_at:]
    # empty array: place the block on its own lines, close bracket re-indented
    close_indent = re.match(
        r"[ \t]*", text[text.rfind("\n", 0, open_br) + 1:]
    ).group(0)
    return text[:open_br + 1] + "\n" + new_block + "\n" + close_indent + text[close_br:]


def _find_group_within(text, name, open_br, close_br):
    """Index of a '"group": "<name>"' key between open_br and close_br, or -1."""
    needle = f'"group": "{json_escape(name)}"'
    pos = text.find(needle, open_br, close_br)
    return pos


def json_escape(s):
    return json.dumps(s, ensure_ascii=False)[1:-1]


def insert_into_nav(docs_text, year, month, archived_path):
    """Insert archived_path under Archived Minor Release Notes -> year -> month,
    creating the group/year/month levels as needed. Returns (new_text, note)."""
    if f'"{archived_path}"' in docs_text:
        return docs_text, f"{archived_path} already present in docs.json — nav untouched."

    anchor = docs_text.find(ANCHOR)
    if anchor == -1:
        sys.exit(f"Could not find {ANCHOR} in docs.json (English nav).")

    month_page = archived_path  # the leaf is a bare page string

    grp_pos = docs_text.find(f'"group": "{ARCHIVE_GROUP}"', anchor)
    if grp_pos == -1:
        sys.exit(
            f'The "{ARCHIVE_GROUP}" group is not in docs.json yet. '
            "Create it via the one-time migration before archiving."
        )
    grp_open, grp_close = _pages_array_after(docs_text, grp_pos)

    year_pos = _find_group_within(docs_text, str(year), grp_open, grp_close)
    if year_pos == -1:
        # create year -> month -> page
        obj = {"group": str(year), "pages": [{"group": month, "pages": [month_page]}]}
        new_text = _append_to_array(docs_text, grp_open, grp_close, obj)
        return new_text, f"Created {year} -> {month} -> {archived_path}"

    year_open, year_close = _pages_array_after(docs_text, year_pos)
    month_pos = _find_group_within(docs_text, month, year_open, year_close)
    if month_pos == -1:
        obj = {"group": month, "pages": [month_page]}
        new_text = _append_to_array(docs_text, year_open, year_close, obj)
        return new_text, f"Created {month} under {year} -> {archived_path}"

    month_open, month_close = _pages_array_after(docs_text, month_pos)
    new_text = _append_to_array(docs_text, month_open, month_close, month_page)
    return new_text, f"Appended {archived_path} to {year} -> {month}"


# --------------------------------------------------------------------------- #
def roll_current_to_archive(dry_run=False):
    """Copy the current file to a dated archive and register it in nav.

    Returns the archived path (repo-relative, no extension) or None if the
    current file is missing or already archived."""
    if not CURRENT.exists():
        print("No Current-Minor-Release-Notes.mdx to archive — skipping.")
        return None

    current_text = CURRENT.read_text(encoding="utf-8")
    rel = derive_release_date(current_text)
    if rel is None:
        print("Current file has no '## {Month} {D}, {Year} Release' heading "
              "(placeholder?) — nothing to archive.")
        return None
    archived_stem = f"Minor-Release-{rel.isoformat()}"
    archived_file = ARTICLE_DIR / f"{archived_stem}.mdx"
    archived_path = f"s/article/{archived_stem}"
    title_date = rel.strftime("%B %-d, %Y")
    new_title = f'title: "Minor Release | {title_date}"'

    if archived_file.exists():
        print(f"{archived_file.name} already exists — nothing to archive.")
        return None

    archived_text, n = TITLE_RE.subn(new_title, current_text, count=1)
    if n != 1:
        sys.exit("Could not rewrite the title line in the current file.")

    docs_text = DOCS_JSON.read_text(encoding="utf-8")
    new_docs, note = insert_into_nav(docs_text, rel.year, rel.strftime("%B"), archived_path)

    print(f"Archiving current week ({title_date})")
    print(f"  Archive file : s/article/{archived_stem}.mdx")
    print(f"  Nav          : {note}")

    if dry_run:
        print("--- DRY RUN (no files written) ---")
        return archived_path

    archived_file.write_text(archived_text, encoding="utf-8")
    DOCS_JSON.write_text(new_docs, encoding="utf-8")
    print(f"Wrote {archived_file.relative_to(ROOT)} and updated docs.json nav.")
    return archived_path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = ap.parse_args()
    roll_current_to_archive(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
