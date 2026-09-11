#!/usr/bin/env python3
"""
Archive the outgoing Current Release Notes before a new draft overwrites it.

For the product-release-notes skill, step "archive". Given the current
`s/article/Current-Release-Notes.mdx` (titled e.g. "May 2026 Release Notes"):

  1. Derive Month + Year from its title.
  2. Compute the archived filename `s/article/{Month}-{Year}-Release.mdx`.
  3. Compute the archived release number = (highest existing "{Year} Release N"
     among archived articles) + 1.
  4. Copy the current content into the archived file, replacing only the
     frontmatter `title:` with "{Year} Release {N} | {Month}".
  5. Insert the archived path at the END of the English "2025-2026" subgroup
     under "Archived Feature Release Notes" in docs.json (surgical text edit;
     English nav only -- localized nav is handled later by the localize flow).

It does NOT overwrite Current-Release-Notes.mdx -- the skill draft step does that
afterward. Run with --dry-run first to preview.

Usage:
    python3 scripts/archive-current-release-notes.py --dry-run
    python3 scripts/archive-current-release-notes.py
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
CURRENT = ROOT / "s/article/Current-Release-Notes.mdx"
ARTICLE_DIR = ROOT / "s/article"
DOCS_JSON = ROOT / "docs.json"

TITLE_RE = re.compile(r'^title:\s*"?([A-Za-z]+)\s+(\d{4})\s+Release Notes"?\s*$', re.MULTILINE)
ARCHIVED_TITLE_RE = re.compile(r'^title:\s*"?(\d{4})\s+Release\s+(\d+)\s*\|', re.MULTILINE)


def derive_month_year():
    text = CURRENT.read_text(encoding="utf-8")
    m = TITLE_RE.search(text)
    if not m:
        sys.exit('Could not parse a "{Month} {Year} Release Notes" title from Current-Release-Notes.mdx.')
    return m.group(1), int(m.group(2)), text


def highest_release_number(year):
    """Scan all archived articles for '{year} Release N | ...' titles; return max N (0 if none)."""
    best = 0
    for p in ARTICLE_DIR.glob("*.mdx"):
        try:
            head = p.read_text(encoding="utf-8")[:400]
        except Exception:
            continue
        m = ARCHIVED_TITLE_RE.search(head)
        if m and int(m.group(1)) == year:
            best = max(best, int(m.group(2)))
    return best


def insert_into_nav(docs_text, archived_path):
    """Append "{archived_path}" to the end of the English 2025-2026 pages array.
    Returns (new_text, preview_snippet) or exits on failure."""
    if f'"{archived_path}"' in docs_text:
        print(f"NOTE: {archived_path} already present in docs.json -- leaving nav untouched.")
        return docs_text, None

    # English nav is the first language block, so the FIRST Current-Release-Notes
    # occurrence (no language prefix) anchors the English Release Notes tab.
    anchor = docs_text.find('"s/article/Current-Release-Notes"')
    if anchor == -1:
        sys.exit("Could not find English s/article/Current-Release-Notes in docs.json.")
    grp = docs_text.find('"group": "2025-2026"', anchor)
    if grp == -1:
        sys.exit("Could not find the English 2025-2026 group after Current-Release-Notes.")
    pages_kw = docs_text.find('"pages"', grp)
    open_br = docs_text.find("[", pages_kw)
    if pages_kw == -1 or open_br == -1:
        sys.exit("Could not locate the 2025-2026 pages array.")

    # find matching close bracket (respect quotes)
    depth, i, in_str = 0, open_br, False
    while i < len(docs_text):
        ch = docs_text[i]
        if ch == '"' and docs_text[i - 1] != "\\":
            in_str = not in_str
        elif not in_str:
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    break
        i += 1
    close_br = i
    array_body = docs_text[open_br + 1:close_br]

    # last string entry inside the array
    entries = list(re.finditer(r'"[^"]+"', array_body))
    if not entries:
        sys.exit("The 2025-2026 pages array appears empty -- aborting.")
    last = entries[-1]
    last_end_abs = open_br + 1 + last.end()

    # indentation of the last entry's line
    line_start = docs_text.rfind("\n", 0, open_br + 1 + last.start()) + 1
    indent = re.match(r"[ \t]*", docs_text[line_start:]).group(0)

    insertion = f',\n{indent}"{archived_path}"'
    new_text = docs_text[:last_end_abs] + insertion + docs_text[last_end_abs:]
    preview = docs_text[line_start:last_end_abs] + insertion
    return new_text, preview


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = ap.parse_args()

    month, year, current_text = derive_month_year()
    archived_name = f"{month}-{year}-Release"
    archived_file = ARTICLE_DIR / f"{archived_name}.mdx"
    archived_path = f"s/article/{archived_name}"
    n = highest_release_number(year) + 1
    new_title = f'"{year} Release {n} | {month}"'

    print(f"Outgoing Current Release Notes : {month} {year}")
    print(f"Archived file                  : s/article/{archived_name}.mdx")
    print(f"Archived title                 : title: {new_title}")
    print(f"Release number (max+1)         : {n}")
    print()

    if archived_file.exists():
        sys.exit(f"{archived_file} already exists -- aborting so nothing is clobbered.")

    # rewrite only the title line
    archived_text, count = TITLE_RE.subn(f"title: {new_title}", current_text, count=1)
    if count != 1:
        sys.exit("Failed to rewrite the title line.")

    docs_text = DOCS_JSON.read_text(encoding="utf-8")
    new_docs, preview = insert_into_nav(docs_text, archived_path)

    if args.dry_run:
        print("--- DRY RUN (no files written) ---")
        print(f"Would create {archived_file} with new title.")
        if preview:
            print("\ndocs.json 2025-2026 group would become (tail):")
            print(preview)
        return

    archived_file.write_text(archived_text, encoding="utf-8")
    DOCS_JSON.write_text(new_docs, encoding="utf-8")
    print(f"Wrote {archived_file}")
    print(f'Inserted "{archived_path}" into docs.json 2025-2026 group')
    print("\nNext: draft the new release into s/article/Current-Release-Notes.mdx (overwrites it).")


if __name__ == "__main__":
    main()
