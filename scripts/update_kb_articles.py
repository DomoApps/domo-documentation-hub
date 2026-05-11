#!/usr/bin/env python3
"""
Programmatically updates the Domo KB article repository from a Salesforce CSV export.

Reads: *CURRENT* Knowledge Article Mod 1Aug2025 - 13Feb2026.csv

Supported languages and their repo directories:
  en_US  →  s/article/
  ja     →  ja/s/article/
  de     →  de/s/article/
  fr     →  fr/s/article/
  es     →  es/s/article/

Three operations (run together by default, or individually via --action):

  UPDATE   Articles that exist in the repo AND are Online in the CSV.
           Replaces the current MDX with a freshly converted version.

  ARCHIVE  Articles that are Archived in the CSV AND exist in the repo.
           Deletes the MDX file from the language directory.

  CREATE   Articles that are Online in the CSV but NOT yet in the repo.
           Creates a new MDX file using the converted HTML.

Images are shared across all language versions of an article.  They are downloaded
once from Salesforce using a session ID (SID) cookie and saved to images/kb/.
Pass --skip-images to skip downloading (e.g. for a dry run or when the SID is
unavailable).

Usage:
  # Full run — all languages, downloading images
  python scripts/update_kb_articles.py --sid YOUR_SID

  # Dry run — see what would change across all languages, nothing written
  python scripts/update_kb_articles.py --dry-run

  # Only Japanese and German, skipping images
  python scripts/update_kb_articles.py --sid YOUR_SID --languages ja de --skip-images

  # Only English, only net-new articles, test with 5 articles first
  python scripts/update_kb_articles.py --sid YOUR_SID --languages en_US --action create --limit 5

Notes:
  - When a URLNAME appears as both Online and Draft, the Online version is used.
  - Short numeric IDs (< 10 digits) are zero-padded to 9 chars to match the repo
    convention, e.g. URLNAME 5387 → file 000005387.mdx.
  - Long numeric IDs and non-numeric slugs (e.g. Current-Release-Notes) are used as-is.
  - The image downloader is shared across all languages — images are not re-downloaded
    if already present from a previous language's processing.
  - Archived articles are deleted from disk; commit with `git rm` to record removal.
  - A run log is written to scripts/articleUpdateMigration/update_articles.log.
"""

import csv
import sys
import re
import logging
import argparse
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# Path configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
LOG_DIR = REPO_ROOT / "scripts" / "articleUpdateMigration"

CSV_GLOB = "*CURRENT* Knowledge Article Mod 1Aug2025 - 13Feb2026.csv"

# Language code → per-language configuration.
# images_dir:      where downloaded images are saved on disk
# image_base_path: repo-relative URL prefix embedded in MDX src attributes
# articles_dir:    where .mdx files live
LANGUAGE_CONFIG: dict[str, dict] = {
    "en_US": {
        "articles_dir":   REPO_ROOT / "s" / "article",
        "images_dir":     REPO_ROOT / "images" / "kb",
        "image_base_path": "/images/kb",
        "display": "English (en_US)",
    },
    "ja": {
        "articles_dir":   REPO_ROOT / "ja" / "s" / "article",
        "images_dir":     REPO_ROOT / "images" / "kb" / "ja",
        "image_base_path": "/images/kb/ja",
        "display": "Japanese (ja)",
    },
    "de": {
        "articles_dir":   REPO_ROOT / "de" / "s" / "article",
        "images_dir":     REPO_ROOT / "images" / "kb" / "de",
        "image_base_path": "/images/kb/de",
        "display": "German (de)",
    },
    "fr": {
        "articles_dir":   REPO_ROOT / "fr" / "s" / "article",
        "images_dir":     REPO_ROOT / "images" / "kb" / "fr",
        "image_base_path": "/images/kb/fr",
        "display": "French (fr)",
    },
    "es": {
        "articles_dir":   REPO_ROOT / "es" / "s" / "article",
        "images_dir":     REPO_ROOT / "images" / "kb" / "es",
        "image_base_path": "/images/kb/es",
        "display": "Spanish (es)",
    },
}

# ---------------------------------------------------------------------------
# Logging setup (file + console)
# ---------------------------------------------------------------------------

LOG_DIR.mkdir(parents=True, exist_ok=True)
_log_path = LOG_DIR / "update_articles.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(_log_path, encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# CSV loading
# ---------------------------------------------------------------------------

def find_csv(repo_root: Path) -> Path:
    """Locate the CSV file in the repo root (handles glob-unfriendly names)."""
    matches = list(repo_root.glob(CSV_GLOB))
    if not matches:
        matches = list(repo_root.glob("*Knowledge Article*"))
    if not matches:
        raise FileNotFoundError(
            f"Could not find CSV matching '{CSV_GLOB}' in {repo_root}"
        )
    if len(matches) > 1:
        log.warning("Multiple matching CSVs found; using: %s", matches[0].name)
    return matches[0]


def load_csv(path: Path) -> list[dict[str, str]]:
    """Load all rows from the CSV export."""
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------
# Article ID normalisation
# ---------------------------------------------------------------------------

def normalize_urlname(urlname: str) -> str:
    """
    Map a Salesforce URLNAME to a repo filename stem.

    Short numeric IDs (1–9 digits) are zero-padded to 9 characters to match
    the s/article/ naming convention.  Long numeric IDs (≥ 10 digits) and
    non-numeric slugs are returned unchanged.

    Examples:
        "5387"              → "000005387"
        "360042932514"      → "360042932514"
        "Current-Release-Notes" → "Current-Release-Notes"
    """
    try:
        n = int(urlname)
        if 0 < n < 1_000_000_000:
            return str(n).zfill(9)
    except ValueError:
        pass
    return urlname


# ---------------------------------------------------------------------------
# Repository scanning
# ---------------------------------------------------------------------------

def get_repo_article_ids(articles_dir: Path) -> set[str]:
    """Return the set of article filename stems (without .mdx) that exist in dir."""
    if not articles_dir.exists():
        return set()
    return {p.stem for p in articles_dir.glob("*.mdx")}


# ---------------------------------------------------------------------------
# Categorisation (per language)
# ---------------------------------------------------------------------------

def categorize_articles(
    rows: list[dict[str, str]],
    repo_ids: set[str],
    language: str,
) -> dict[str, list[dict]]:
    """
    Partition articles for one language into three action categories.

    Returns a dict with keys:
        "to_update"  – in repo AND Online in CSV   → replace MDX
        "to_archive" – in repo AND Archived in CSV → delete file
        "to_create"  – Online in CSV AND not in repo → create file

    De-duplication: when a URLNAME has both Online and Draft rows for the same
    language, the Online row is kept.  Draft-only articles are skipped.
    """
    # Filter to the requested language; de-duplicate preferring Online > Draft > Archived
    best: dict[str, dict[str, str]] = {}   # normalized_id → best row

    priority = {"Online": 2, "Draft": 1, "Archived": 0}

    for row in rows:
        if row.get("LANGUAGE") != language:
            continue
        nid = normalize_urlname(row["URLNAME"])
        status = row["PUBLISHSTATUS"]

        if nid not in best:
            best[nid] = row
        elif priority.get(status, -1) > priority.get(best[nid]["PUBLISHSTATUS"], -1):
            best[nid] = row

    to_update: list[dict] = []
    to_archive: list[dict] = []
    to_create: list[dict] = []

    for nid, row in best.items():
        status = row["PUBLISHSTATUS"]
        in_repo = nid in repo_ids

        if status == "Archived":
            if in_repo:
                to_archive.append({"id": nid, "row": row})
        elif status == "Online":
            if in_repo:
                to_update.append({"id": nid, "row": row})
            else:
                to_create.append({"id": nid, "row": row})
        # Draft-only: skip

    return {"to_update": to_update, "to_archive": to_archive, "to_create": to_create}


# ---------------------------------------------------------------------------
# Image URL extraction
# ---------------------------------------------------------------------------

_IMG_SRC_RE = re.compile(
    r"""<img[^>]*?\ssrc=["']([^"']+)["'][^>]*?>""",
    re.IGNORECASE,
)


def extract_image_urls(html: str) -> list[str]:
    """Return a deduplicated list of image src URLs found in the HTML."""
    seen: set[str] = set()
    result: list[str] = []
    for url in _IMG_SRC_RE.findall(html):
        canonical = url.replace("&amp;", "&")
        if canonical not in seen:
            seen.add(canonical)
            result.append(canonical)
    return result


# ---------------------------------------------------------------------------
# Article processing
# ---------------------------------------------------------------------------

def process_article(
    article_id: str,
    row: dict[str, str],
    downloader,            # SalesforceImageDownloader | None
    skip_images: bool,
    language: str,
    image_base_path: str = "/images/kb",
) -> str | None:
    """
    Download images (if needed) and convert HTML → MDX for one article.

    Returns the MDX string on success, None on failure.
    The `language` parameter controls the internal link prefix written into the MDX.
    The `image_base_path` parameter controls the repo-relative directory prefix
    embedded in MDX image src attributes (e.g. '/images/kb/ja' for Japanese).
    """
    from html_to_mdx import html_to_mdx  # local import to avoid module-level circularity

    title = row["TITLE"]
    html = row["ARTICLE_BODY__C"]

    image_urls = extract_image_urls(html)
    image_local_map: dict[str, str] = {}

    if image_urls and not skip_images:
        if downloader is not None:
            log.info("    Downloading %d image(s)…", len(image_urls))
            image_local_map = downloader.download_all(image_urls)
        else:
            log.warning(
                "    %d image(s) found but no downloader available (no --sid)",
                len(image_urls),
            )
    elif image_urls and skip_images:
        log.info("    Skipping %d image(s) (--skip-images)", len(image_urls))

    try:
        return html_to_mdx(
            html, title, image_local_map,
            language=language,
            image_base_path=image_base_path,
        )
    except Exception as exc:
        log.error(
            "    Conversion failed for [%s] %s: %s", article_id, title[:50], exc
        )
        return None


# ---------------------------------------------------------------------------
# Per-language runner
# ---------------------------------------------------------------------------

def run_language(
    lang: str,
    rows: list[dict[str, str]],
    articles_dir: Path,
    images_dir: Path,
    image_base_path: str,
    action: str,
    sid: str | None,
    skip_images: bool,
    limit: int | None,
    dry_run: bool,
) -> dict[str, int]:
    """
    Execute update/archive/create operations for one language.
    Returns a stats dict: {updated, skipped, created, archived, failed, created_ids, changed_ids}.

    A per-language SalesforceImageDownloader is created here so each language
    saves its images to the correct subdirectory (e.g. images/kb/ja for Japanese).
    """
    # Create a language-specific image downloader
    downloader = None
    if not skip_images and sid:
        from image_downloader import SalesforceImageDownloader
        images_dir.mkdir(parents=True, exist_ok=True)
        downloader = SalesforceImageDownloader(sid, images_dir)

    repo_ids = get_repo_article_ids(articles_dir)
    categories = categorize_articles(rows, repo_ids, lang)

    n_upd = len(categories["to_update"])
    n_arc = len(categories["to_archive"])
    n_cre = len(categories["to_create"])

    log.info("  Plan: UPDATE %d | ARCHIVE %d | CREATE %d", n_upd, n_arc, n_cre)

    if dry_run:
        _print_dry_run_details(categories, limit)
        return {"updated": 0, "created": 0, "archived": 0, "failed": 0}

    stats = {"updated": 0, "skipped": 0, "created": 0, "archived": 0, "failed": 0, "created_ids": [], "changed_ids": []}

    # ARCHIVE
    if action in ("all", "archive"):
        arc_list = categories["to_archive"]
        if limit:
            arc_list = arc_list[:limit]
        for item in arc_list:
            article_id, title = item["id"], item["row"]["TITLE"]
            filepath = articles_dir / f"{article_id}.mdx"
            log.info("  ARCHIVE [%s] %s", article_id, title[:60])
            if filepath.exists():
                filepath.unlink()
                stats["archived"] += 1
                log.info("    Deleted: %s", filepath.name)
            else:
                log.warning("    File not found (already absent?): %s", filepath)

    # UPDATE
    if action in ("all", "update"):
        upd_list = categories["to_update"]
        if limit:
            upd_list = upd_list[:limit]
        for item in upd_list:
            article_id, title = item["id"], item["row"]["TITLE"]
            log.info("  UPDATE [%s] %s", article_id, title[:60])
            mdx = process_article(article_id, item["row"], downloader, skip_images, lang, image_base_path)
            if mdx:
                filepath = articles_dir / f"{article_id}.mdx"
                if _content_differs(filepath, mdx):
                    _write_mdx(filepath, mdx)
                    stats["updated"] += 1
                    stats["changed_ids"].append(article_id)
                else:
                    log.info("    No change — skipping %s", filepath.name)
                    stats["skipped"] += 1
            else:
                stats["failed"] += 1

    # CREATE
    if action in ("all", "create"):
        cre_list = categories["to_create"]
        if limit:
            cre_list = cre_list[:limit]
        for item in cre_list:
            article_id, title = item["id"], item["row"]["TITLE"]
            log.info("  CREATE [%s] %s", article_id, title[:60])
            mdx = process_article(article_id, item["row"], downloader, skip_images, lang, image_base_path)
            if mdx:
                _write_mdx(articles_dir / f"{article_id}.mdx", mdx)
                stats["created"] += 1
                stats["created_ids"].append(article_id)
            else:
                stats["failed"] += 1

    if downloader:
        downloader.report()

    return stats


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
            Update the Domo KB article repo from a Salesforce CSV export.

            Processes English, Japanese, German, French, and Spanish articles.
            Three operations: UPDATE (replace), ARCHIVE (delete), CREATE (new).
            Defaults to running all three for all languages.
        """),
    )

    parser.add_argument(
        "--sid",
        metavar="SESSION_ID",
        help=(
            "Salesforce session ID for image downloads.  "
            "Find it in browser devtools → Application → Cookies → sid.  "
            "Images are downloaded once and reused across all languages."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without writing or deleting any files.",
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        metavar="LANG",
        choices=list(LANGUAGE_CONFIG.keys()),
        default=list(LANGUAGE_CONFIG.keys()),
        help=(
            "Language(s) to process.  "
            f"Choices: {', '.join(LANGUAGE_CONFIG.keys())}.  "
            "Default: all languages."
        ),
    )
    parser.add_argument(
        "--action",
        choices=["all", "update", "archive", "create"],
        default="all",
        help="Which operation to perform (default: all).",
    )
    parser.add_argument(
        "--skip-images",
        action="store_true",
        help=(
            "Skip image downloads.  Images in the converted MDX will appear as "
            "'<!-- TODO: embed image → … -->' comments."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        metavar="N",
        help="Process at most N articles per category per language (for testing).",
    )
    parser.add_argument(
        "--csv",
        metavar="PATH",
        help="Explicit path to the CSV file (auto-detected by default).",
    )

    args = parser.parse_args()

    # ------------------------------------------------------------------
    # Add scripts/ to sys.path so sibling modules can be imported
    # ------------------------------------------------------------------
    scripts_dir = str(Path(__file__).parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)

    # ------------------------------------------------------------------
    # Load CSV
    # ------------------------------------------------------------------
    csv_path = Path(args.csv) if args.csv else find_csv(REPO_ROOT)
    log.info("CSV: %s", csv_path.name)

    rows = load_csv(csv_path)
    log.info("Loaded %d rows from CSV", len(rows))

    # ------------------------------------------------------------------
    # Preview: total article counts per language in CSV
    # ------------------------------------------------------------------
    from collections import Counter
    lang_status_counts: dict[str, Counter] = {}
    for row in rows:
        l = row.get("LANGUAGE", "?")
        if l not in lang_status_counts:
            lang_status_counts[l] = Counter()
        lang_status_counts[l][row["PUBLISHSTATUS"]] += 1

    log.info("CSV breakdown by language:")
    for lang in args.languages:
        counts = lang_status_counts.get(lang, Counter())
        log.info(
            "  %-6s  Online: %d  Archived: %d  Draft: %d",
            lang,
            counts.get("Online", 0),
            counts.get("Archived", 0),
            counts.get("Draft", 0),
        )

    if args.dry_run:
        log.info("\nDRY RUN — no files will be written or deleted.")

    # ------------------------------------------------------------------
    # Image download setup
    # Each language gets its own downloader pointed at its own images_dir.
    # Warn once here if no SID was provided.
    # ------------------------------------------------------------------
    if not args.skip_images and not args.sid:
        log.warning(
            "No --sid provided. Images will NOT be downloaded.  "
            "Pass --skip-images to suppress this warning, or provide --sid."
        )

    # ------------------------------------------------------------------
    # Process each requested language
    # ------------------------------------------------------------------
    total_stats = {"updated": 0, "skipped": 0, "created": 0, "archived": 0, "failed": 0}
    # English articles created this run — each needs /add-to-nav in docs.json
    created_en_articles: list[tuple[str, str]] = []  # [(article_id, title), ...]
    # English articles whose content actually changed — candidates for /update-kb-article review
    changed_en_articles: list[tuple[str, str]] = []  # [(article_id, title), ...]

    for lang in args.languages:
        config = LANGUAGE_CONFIG[lang]
        articles_dir = config["articles_dir"]
        images_dir = config["images_dir"]
        image_base_path = config["image_base_path"]

        log.info("")
        log.info("=== %s ===", config["display"])
        log.info("  Articles:  %s", articles_dir.relative_to(REPO_ROOT))
        log.info("  Images:    %s", images_dir.relative_to(REPO_ROOT))

        lang_stats = run_language(
            lang=lang,
            rows=rows,
            articles_dir=articles_dir,
            images_dir=images_dir,
            image_base_path=image_base_path,
            action=args.action,
            sid=args.sid,
            skip_images=args.skip_images,
            limit=args.limit,
            dry_run=args.dry_run,
        )

        if not args.dry_run:
            log.info(
                "  %s done: updated=%d  skipped=%d  created=%d  archived=%d  failed=%d",
                lang,
                lang_stats["updated"],
                lang_stats["skipped"],
                lang_stats["created"],
                lang_stats["archived"],
                lang_stats["failed"],
            )
            for k in total_stats:
                total_stats[k] += lang_stats[k]
            # Collect newly created / actually changed English articles for the prompts below
            if lang == "en_US":
                lang_rows_by_id = {
                    normalize_urlname(r["URLNAME"]): r
                    for r in rows
                    if r.get("LANGUAGE") == "en_US"
                }
                for aid in lang_stats.get("created_ids", []):
                    title = lang_rows_by_id.get(aid, {}).get("TITLE", aid)
                    created_en_articles.append((aid, title))
                for aid in lang_stats.get("changed_ids", []):
                    title = lang_rows_by_id.get(aid, {}).get("TITLE", aid)
                    changed_en_articles.append((aid, title))

    # ------------------------------------------------------------------
    # Final summary
    # ------------------------------------------------------------------
    if not args.dry_run:
        log.info("")
        log.info("=== TOTAL ACROSS ALL LANGUAGES ===")
        log.info("  Updated:  %d  (content changed and rewritten)", total_stats["updated"])
        log.info("  Skipped:  %d  (content unchanged — file not touched)", total_stats["skipped"])
        log.info("  Created:  %d", total_stats["created"])
        log.info("  Archived: %d", total_stats["archived"])
        log.info("  Failed:   %d", total_stats["failed"])

        log.info("Log written to: %s", _log_path)

        if total_stats["created"] or total_stats["updated"]:
            log.info("")
            log.info(
                "NEXT STEPS:\n"
                "  1. Review TODO comments in converted files (missing images,\n"
                "     headings that may need imperative-mood edits, etc.).\n"
                "  2. Add new English articles to docs.json navigation using the\n"
                "     /add-to-nav skill in Claude Code — run it for each article\n"
                "     listed below. Localized articles don't need separate nav entries.\n"
                "  3. Commit: git add s/ ja/ de/ fr/ es/ images/kb/ && git commit"
            )

        if changed_en_articles:
            log.info("")
            log.info(
                "English articles with content changes (%d) — review each with /update-kb-article:",
                len(changed_en_articles),
            )
            for aid, title in changed_en_articles:
                log.info("    s/article/%s  —  %s", aid, title[:60])

        if created_en_articles:
            log.info("")
            log.info("New English articles requiring /add-to-nav (%d):", len(created_en_articles))
            for aid, title in created_en_articles:
                log.info("    s/article/%s  —  %s", aid, title[:60])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _content_differs(existing_path: Path, new_content: str) -> bool:
    """
    Return True if new_content differs meaningfully from the file at existing_path.

    Normalises trailing whitespace and line endings before comparing so that
    cosmetic-only differences (e.g. a trailing newline added by an editor) do
    not trigger an unnecessary overwrite and a misleading "updated" count.
    Returns True (differs) if the file doesn't exist yet.
    """
    if not existing_path.exists():
        return True
    try:
        existing = existing_path.read_text(encoding="utf-8")
    except OSError:
        return True

    def _normalise(text: str) -> str:
        return "\n".join(line.rstrip() for line in text.splitlines()).strip()

    return _normalise(existing) != _normalise(new_content)


def _write_mdx(path: Path, content: str) -> None:
    """Write MDX content to a file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    log.info("    Written: %s", path.name)


def _print_dry_run_details(
    categories: dict[str, list[dict]],
    limit: int | None,
) -> None:
    """Print a human-readable preview of what would change for one language."""

    def _section(label: str, items: list[dict]) -> None:
        cap = items[:limit] if limit else items
        if not items:
            return
        print(f"    {label} ({len(items)}):")
        for item in cap:
            print(f"      [{item['id']}]  {item['row']['TITLE'][:65]}")
        if limit and len(items) > limit:
            print(f"      … and {len(items) - limit} more")

    _section("to UPDATE", categories["to_update"])
    _section("to ARCHIVE", categories["to_archive"])
    _section("to CREATE", categories["to_create"])


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
