#!/usr/bin/env python3
"""
Diffs CSV-converted MDX against existing repo files and produces a structured
change report designed for targeted, surgical edits.

For each Online article in the CSV that already exists in the repo, this script:
  1. Converts the Salesforce HTML using the same pipeline as update_kb_articles.py
  2. Strips image-only change blocks (Frame, img tags, TODO comments) — these are
     almost never the meaningful change in a connector or KB article update
  3. Reports the remaining content changes with:
       - The exact file path to edit
       - The nearest section heading above each change (for navigation context)
       - The exact OLD text (from the repo file) and NEW text (from the CSV)
         formatted for direct use as Edit tool old_string / new_string values

The output is designed to be passed directly to Claude Code for targeted edits
via /update-kb-article — precise enough to use the Edit tool without re-running
the full import pipeline or re-downloading images.

Usage:
  # All changed articles, all languages
  python scripts/diff_kb_articles.py

  # Filter by title keyword (case-insensitive) — e.g. connector articles
  python scripts/diff_kb_articles.py --filter connector

  # Only specific languages
  python scripts/diff_kb_articles.py --languages en_US --filter connector

  # Save the report to a file for use in a Claude Code session
  python scripts/diff_kb_articles.py --filter connector --output changes.txt

  # Show articles with NO non-image changes (to confirm they are clean)
  python scripts/diff_kb_articles.py --filter connector --show-clean
"""

import csv
import sys
import re
import difflib
import argparse
import textwrap
from pathlib import Path
from urllib.parse import urlparse, parse_qs


# ---------------------------------------------------------------------------
# Path configuration  (mirrors LANGUAGE_CONFIG in update_kb_articles.py)
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent

CSV_GLOB = "*CURRENT* Knowledge Article Mod 1Aug2025 - 13Feb2026.csv"

LANGUAGE_CONFIG: dict[str, dict] = {
    "en_US": {
        "articles_dir":     REPO_ROOT / "s" / "article",
        "images_dir":       REPO_ROOT / "images" / "kb",
        "image_base_path":  "/images/kb",
        "display":          "English (en_US)",
    },
    "ja": {
        "articles_dir":     REPO_ROOT / "ja" / "s" / "article",
        "images_dir":       REPO_ROOT / "images" / "kb" / "ja",
        "image_base_path":  "/images/kb/ja",
        "display":          "Japanese (ja)",
    },
    "de": {
        "articles_dir":     REPO_ROOT / "de" / "s" / "article",
        "images_dir":       REPO_ROOT / "images" / "kb" / "de",
        "image_base_path":  "/images/kb/de",
        "display":          "German (de)",
    },
    "fr": {
        "articles_dir":     REPO_ROOT / "fr" / "s" / "article",
        "images_dir":       REPO_ROOT / "images" / "kb" / "fr",
        "image_base_path":  "/images/kb/fr",
        "display":          "French (fr)",
    },
    "es": {
        "articles_dir":     REPO_ROOT / "es" / "s" / "article",
        "images_dir":       REPO_ROOT / "images" / "kb" / "es",
        "image_base_path":  "/images/kb/es",
        "display":          "Spanish (es)",
    },
}

# Lines matching any of these patterns are considered image-related.
# A change block where EVERY changed line matches is suppressed.
_IMAGE_PATTERNS = re.compile(
    r"""
    <Frame>         # Mintlify Frame open tag
    | </Frame>      # Mintlify Frame close tag
    | <img\s        # raw <img> tag
    | /images/kb/   # any image path reference
    | <!--\s*TODO:\s*embed\s*image  # TODO placeholder from missing download
    | !\[.*?\]\(    # Markdown image syntax  ![alt](path)
    """,
    re.VERBOSE,
)

_IMG_SRC_RE = re.compile(r"""<img[^>]*?\ssrc=["']([^"']+)["'][^>]*?>""", re.IGNORECASE)
_HEADING_RE = re.compile(r"^(#{1,4})\s+(.+)$")

# Change blocks larger than this many lines will be flagged as "large" and
# the user is advised to use update_kb_articles.py for that article instead.
LARGE_CHANGE_THRESHOLD = 30


# ---------------------------------------------------------------------------
# CSV / normalisation helpers
# ---------------------------------------------------------------------------

def find_csv(repo_root: Path) -> Path:
    matches = list(repo_root.glob(CSV_GLOB))
    if not matches:
        matches = list(repo_root.glob("*Knowledge Article*"))
    if not matches:
        raise FileNotFoundError(
            f"Could not find CSV matching '{CSV_GLOB}' in {repo_root}"
        )
    if len(matches) > 1:
        print(f"Warning: multiple CSVs found; using {matches[0].name}", file=sys.stderr)
    return matches[0]


def load_csv(path: Path) -> list[dict[str, str]]:
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def normalize_urlname(urlname: str) -> str:
    try:
        n = int(urlname)
        if 0 < n < 1_000_000_000:
            return str(n).zfill(9)
    except ValueError:
        pass
    return urlname


# ---------------------------------------------------------------------------
# Image map reconstruction from disk
# ---------------------------------------------------------------------------

def extract_image_urls(html: str) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for url in _IMG_SRC_RE.findall(html):
        canonical = url.replace("&amp;", "&")
        if canonical not in seen:
            seen.add(canonical)
            result.append(canonical)
    return result


def build_image_map_from_disk(html: str, images_dir: Path) -> dict[str, str]:
    """
    Reconstruct {salesforce_url: local_filename} from images already on disk.
    Uses the refid query-parameter as the filename stem (same as the downloader).
    """
    img_map: dict[str, str] = {}
    for url in extract_image_urls(html):
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        refid_list = params.get("refid", [])
        if not refid_list:
            continue
        refid = refid_list[0]
        matches = list(images_dir.glob(f"{refid}.*"))
        if matches:
            local_name = matches[0].name
            img_map[url] = local_name
            img_map[url.replace("&", "&amp;")] = local_name
    return img_map


# ---------------------------------------------------------------------------
# Diff analysis
# ---------------------------------------------------------------------------

def is_image_line(line: str) -> bool:
    """Return True if this line is purely an image embed."""
    stripped = line.strip()
    if not stripped:
        return False
    return bool(_IMAGE_PATTERNS.search(stripped))


def find_nearest_heading(lines: list[str], before_index: int) -> str:
    """
    Scan backwards from before_index and return the first markdown heading found.
    Returns the heading text, or '(top of file)' if none is found.
    """
    for i in range(before_index - 1, -1, -1):
        m = _HEADING_RE.match(lines[i])
        if m:
            return lines[i].strip()
    return "(top of file)"


def get_content_changes(
    old_lines: list[str],
    new_lines: list[str],
) -> list[dict]:
    """
    Use SequenceMatcher to find changed blocks between old and new lines.

    Returns a list of change dicts, each containing:
      tag           'replace' | 'delete' | 'insert'
      old_start     0-based line index in old_lines (1-based in report)
      old_lines     list of lines being removed from the repo file
      new_lines     list of lines being added from the CSV conversion
      image_only    True if every changed line is image-related (suppressed by default)
      large         True if the combined change exceeds LARGE_CHANGE_THRESHOLD lines
      heading       nearest heading above this block in old_lines
    """
    matcher = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
    changes = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue

        old_block = old_lines[i1:i2]
        new_block = new_lines[j1:j2]

        # Determine whether every changed line is image-related
        changed_lines = [l for l in old_block + new_block if l.strip()]
        image_only = bool(changed_lines) and all(is_image_line(l) for l in changed_lines)

        total_changed = len(old_block) + len(new_block)
        large = total_changed > LARGE_CHANGE_THRESHOLD

        heading = find_nearest_heading(old_lines, i1)

        changes.append({
            "tag":        tag,
            "old_start":  i1,          # 0-based
            "old_block":  old_block,
            "new_block":  new_block,
            "image_only": image_only,
            "large":      large,
            "heading":    heading,
        })

    return changes


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def _indent(lines: list[str], prefix: str = "    ") -> str:
    return "\n".join(prefix + l.rstrip() for l in lines) if lines else f"{prefix}(empty)"


def format_article_report(
    article_id: str,
    title: str,
    lang_display: str,
    filepath: Path,
    content_changes: list[dict],
) -> str:
    """
    Format the full change report for one article.
    Suppresses image-only blocks; flags large blocks.
    """
    rel_path = filepath.relative_to(REPO_ROOT)
    lines = [
        "=" * 78,
        f"FILE:   {rel_path}",
        f"TITLE:  {title}",
        f"LANG:   {lang_display}",
        f"ID:     {article_id}",
        "=" * 78,
        "",
    ]

    meaningful = [c for c in content_changes if not c["image_only"]]
    image_only_count = len(content_changes) - len(meaningful)

    if not meaningful:
        lines.append("  (No non-image content changes)")
        if image_only_count:
            lines.append(f"  [{image_only_count} image-only change(s) suppressed]")
        return "\n".join(lines)

    change_num = 0
    large_count = 0

    for change in meaningful:
        change_num += 1
        tag       = change["tag"]
        old_start = change["old_start"] + 1   # convert to 1-based
        old_end   = old_start + len(change["old_block"]) - 1
        heading   = change["heading"]
        large     = change["large"]

        line_ref = (
            f"line {old_start}"
            if len(change["old_block"]) <= 1
            else f"lines {old_start}–{old_end}"
        )

        lines.append(f"CHANGE {change_num}  [{heading}]  ({line_ref} in repo file)")
        lines.append("")

        if large:
            large_count += 1
            total = len(change["old_block"]) + len(change["new_block"])
            lines.append(f"  ⚠ LARGE CHANGE ({total} lines).  Consider re-running")
            lines.append(f"    update_kb_articles.py for this article instead.")
            lines.append("")

        if tag in ("replace", "delete") and change["old_block"]:
            lines.append("  OLD (remove from repo):")
            lines.append(_indent(change["old_block"]))
            lines.append("")

        if tag in ("replace", "insert") and change["new_block"]:
            lines.append("  NEW (replace with / insert from CSV):")
            lines.append(_indent(change["new_block"]))
            lines.append("")

    if image_only_count:
        lines.append(f"  [{image_only_count} image-only change(s) suppressed — handle separately if needed]")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
            Diff Salesforce CSV content against repo files and produce a targeted
            change report for surgical edits — without re-importing or re-downloading.
        """),
    )
    parser.add_argument(
        "--filter",
        metavar="KEYWORD",
        help="Only check articles whose title contains KEYWORD (case-insensitive).",
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        metavar="LANG",
        choices=list(LANGUAGE_CONFIG.keys()),
        default=list(LANGUAGE_CONFIG.keys()),
        help=f"Languages to check (default: all). Choices: {', '.join(LANGUAGE_CONFIG.keys())}",
    )
    parser.add_argument(
        "--csv",
        metavar="PATH",
        help="Explicit path to the CSV file (auto-detected by default).",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Write the change report to FILE instead of stdout.",
    )
    parser.add_argument(
        "--show-clean",
        action="store_true",
        help="Also list articles that have NO non-image changes (confirmed clean).",
    )

    args = parser.parse_args()

    scripts_dir = str(Path(__file__).parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)

    from html_to_mdx import html_to_mdx

    # ------------------------------------------------------------------
    # Load and de-duplicate CSV rows
    # ------------------------------------------------------------------
    csv_path = Path(args.csv) if args.csv else find_csv(REPO_ROOT)
    print(f"CSV:  {csv_path.name}", file=sys.stderr)
    if args.filter:
        print(f"Filter: '{args.filter}'", file=sys.stderr)

    rows = load_csv(csv_path)

    priority = {"Online": 2, "Draft": 1, "Archived": 0}
    best_by_lang: dict[str, dict[str, dict]] = {}

    for row in rows:
        lang = row.get("LANGUAGE", "")
        if lang not in LANGUAGE_CONFIG:
            continue
        nid = normalize_urlname(row.get("URLNAME", ""))
        if not nid:
            continue
        status = row.get("PUBLISHSTATUS", "")
        best_by_lang.setdefault(lang, {})
        existing = best_by_lang[lang].get(nid)
        if existing is None or priority.get(status, -1) > priority.get(
            existing.get("PUBLISHSTATUS", ""), -1
        ):
            best_by_lang[lang][nid] = row

    # ------------------------------------------------------------------
    # Diff pass
    # ------------------------------------------------------------------
    report_sections: list[str] = []
    clean_articles:  list[str] = []   # articles with no non-image changes
    summary_rows:    list[str] = []   # one line per article for the header table

    total_checked = 0
    total_with_changes = 0

    for lang in args.languages:
        config          = LANGUAGE_CONFIG[lang]
        articles_dir    = config["articles_dir"]
        images_dir      = config["images_dir"]
        image_base_path = config["image_base_path"]
        rows_for_lang   = best_by_lang.get(lang, {})

        for nid, row in sorted(rows_for_lang.items()):
            if row.get("PUBLISHSTATUS") != "Online":
                continue

            filepath = articles_dir / f"{nid}.mdx"
            if not filepath.exists():
                continue

            title = row.get("TITLE", nid)
            if args.filter and args.filter.lower() not in title.lower():
                continue

            total_checked += 1
            html    = row.get("ARTICLE_BODY__C", "")
            img_map = build_image_map_from_disk(html, images_dir)

            try:
                new_mdx = html_to_mdx(
                    html, title, img_map,
                    language=lang,
                    image_base_path=image_base_path,
                )
            except Exception as exc:
                print(f"  [ERROR] [{nid}] {title[:60]}: {exc}", file=sys.stderr)
                continue

            existing_mdx = filepath.read_text(encoding="utf-8")

            # Quick check: identical after normalisation → skip entirely
            def _norm(t: str) -> str:
                return "\n".join(l.rstrip() for l in t.splitlines()).strip()

            if _norm(existing_mdx) == _norm(new_mdx):
                continue

            old_lines = existing_mdx.splitlines()
            new_lines = new_mdx.splitlines()
            changes   = get_content_changes(old_lines, new_lines)

            meaningful = [c for c in changes if not c["image_only"]]
            rel_path   = str(filepath.relative_to(REPO_ROOT))

            if not meaningful:
                clean_articles.append(f"  {rel_path}  —  {title}")
                continue

            total_with_changes += 1
            n_changes = len(meaningful)
            large_flag = "  ⚠ LARGE" if any(c["large"] for c in meaningful) else ""
            summary_rows.append(
                f"  {rel_path:<55}  {n_changes} change(s){large_flag}"
            )

            section = format_article_report(
                nid, title, config["display"], filepath, changes
            )
            report_sections.append(section)

    # ------------------------------------------------------------------
    # Assemble output
    # ------------------------------------------------------------------
    out_lines: list[str] = []

    filter_note = f" matching '{args.filter}'" if args.filter else ""
    out_lines.append(f"KB ARTICLE CHANGE REPORT")
    out_lines.append(f"CSV:     {csv_path.name}")
    out_lines.append(f"Checked: {total_checked} articles{filter_note}")
    out_lines.append(f"Changed: {total_with_changes} articles with non-image content differences")
    out_lines.append("")

    if summary_rows:
        out_lines.append("ARTICLES REQUIRING EDITS:")
        out_lines.extend(summary_rows)
        out_lines.append("")

    if clean_articles and args.show_clean:
        out_lines.append("ARTICLES WITH NO NON-IMAGE CHANGES (clean):")
        out_lines.extend(clean_articles)
        out_lines.append("")

    out_lines.append("")
    out_lines.extend(report_sections)

    if not report_sections:
        out_lines.append("No non-image content differences found.")

    output = "\n".join(out_lines)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Report written to: {args.output}", file=sys.stderr)
        print(f"  {total_with_changes} article(s) with changes  |  {total_checked} checked", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
