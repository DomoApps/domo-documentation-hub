#!/usr/bin/env python3
"""
fix_anchors.py

Scans MDX article files for old Salesforce-style underscore anchors and replaces
them with the correct Mintlify-generated anchors derived from actual ## header text.

Also converts old domo-support.domo.com full URLs to /s/article/ relative paths.

Background
----------
In the previous Salesforce system, in-page anchors were manually created in HTML
and almost never matched the header text verbatim. Words were separated by
underscores (_). In Mintlify, anchors are auto-generated from ## Header text with
words separated by hyphens (-). A simple underscore→hyphen swap is not sufficient
because the old anchor names frequently differ from the actual header text.

Link forms detected
-------------------
  1. [text](https://domo-support.domo.com/s/article/ID?lang=en_US#old_anchor)
  2. [text](/s/article/ID#old_anchor)
  3. [text](#old_anchor)
  4. HTML href="..." variants of all the above

For Salesforce URLs (form 1), the URL is always converted to a /s/article/ relative
path regardless of whether the anchor has underscores.

For root-relative (form 2) and bare (form 3) links, only anchors containing
underscores are processed.

Confidence levels
-----------------
  HIGH (>=0.80) Auto-applied; shown only with --verbose
  MED  (>=0.50) Auto-applied; always shown
  LOW  (<0.50)  Skipped by default; listed in summary for manual review
  UNMATCHED     Left unchanged; listed in summary

  Use --include-low to also apply LOW confidence changes.

Usage
-----
  python3 scripts/fix_anchors.py                       # dry run → unified diff to stdout
  python3 scripts/fix_anchors.py --apply               # write HIGH+MED changes to disk
  python3 scripts/fix_anchors.py --apply --include-low # write all matched changes
  python3 scripts/fix_anchors.py --output diff.txt     # write diff to a file for review
  python3 scripts/fix_anchors.py --file PATH           # single file (PATH relative to repo root)
  python3 scripts/fix_anchors.py --verbose             # show HIGH-confidence matches too
"""

import re
import argparse
import difflib
from pathlib import Path

# Sentinel returned by resolve() when the anchor should be stripped from its link
# rather than kept unchanged.
_STRIP = '\x00STRIP\x00'

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories to scan (relative to repo root)
SEARCH_DIRS = [
    "s/article",
    "s/topic",
    "fr/s/article",
    "fr/s/topic",
    "ja/s/article",
    "ja/s/topic",
    "de/s/article",
    "de/s/topic",
    "es/s/article",
    "es/s/topic",
]

LOCALIZED_PREFIXES = frozenset({"fr", "ja", "de", "es"})

# (relative_path, old_anchor) pairs whose LOW-confidence matches were manually
# reviewed and found to be WRONG. These are skipped even with --include-low.
LOW_MANUAL_SKIP: frozenset[tuple[str, str]] = frozenset({
    # English — wrong section matched
    ("s/article/000005080.mdx",       "switching_asset"),            # "switch" ≠ "update"
    ("s/article/000005146.mdx",       "install_excel_ppt_word_web"), # web ≠ Mac
    ("s/article/000005173.mdx",       "output_parameters"),          # wrong concept
    ("s/article/000005539.mdx",       "retry_a_query"),              # wrong
    ("s/article/000005698.mdx",       "snowflake_key-pair_authentication"), # wrong section
    ("s/article/000005827.mdx",       "sign_authentication_requests"), # wrong
    ("s/article/360042923914.mdx",    "remove_filters"),             # remove ≠ apply
    ("s/article/360043429473.mdx",    "header_row_border_properties"), # wrong
    ("s/article/36004740075.mdx",     "navigate_to_dataflow"),       # wrong
    # French — wrong section matched
    ("fr/s/article/000005377.mdx",    "nested_beast_mode_calculations"),
    ("fr/s/article/000005430.mdx",    "json_no_code"),
    ("fr/s/article/000005459.mdx",    "card_Load_Domo_Stats"),
    ("fr/s/article/000005848.mdx",    "domo_ai_agent_workflows"),
    ("fr/s/article/000005848.mdx",    "cloud_amplifier_integration_sharing"),
    ("fr/s/article/000005848.mdx",    "domo_ai_filesets"),
    # Japanese — wrong section matched (multiple anchors collapsed to wrong header)
    ("ja/s/article/000005143.mdx",    "connect_to_domo_instance"),
    ("ja/s/article/000005143.mdx",    "search_domo_content"),
    ("ja/s/article/000005143.mdx",    "refresh_all_domo_content"),
    ("ja/s/article/000005143.mdx",    "import_domo_content"),
    ("ja/s/article/000005166.mdx",    "push_updates_github"),        # push ≠ create repo
    ("ja/s/article/000005182.mdx",    "remove_an_installed_app"),    # remove ≠ deploy
    ("ja/s/article/000005182.mdx",    "configure_dashboard_app"),
    ("ja/s/article/000005291.mdx",    "model_training"),             # matched a code block
    ("ja/s/article/000005295.mdx",    "edit_an_app"),
    ("ja/s/article/000005377.mdx",    "ai_model_management"),        # model mgmt ≠ service layer
    ("ja/s/article/000005459.mdx",    "workflows_updates"),
    ("ja/s/article/000005500.mdx",    "save_an_app"),                # save ≠ toggle explorer
    ("ja/s/article/000005539.mdx",    "access_ai_chat"),             # access ≠ security
    ("ja/s/article/000005539.mdx",    "use_ai_chat"),
    ("ja/s/article/000005543.mdx",    "custom_themes"),              # matched Frame image header
    ("ja/s/article/000005543.mdx",    "import_from_existing_app"),
    ("ja/s/article/000005544.mdx",    "using_generate_text"),
    ("ja/s/article/000005544.mdx",    "using_summariz_text"),
})


# ─────────────────────────────────────────────────────────────────────────────
# Anchor generation
# ─────────────────────────────────────────────────────────────────────────────

def header_to_anchor(raw_line: str) -> str:
    """
    Convert a raw Markdown header line (e.g. '## My Header') to a Mintlify
    anchor slug (e.g. 'my-header').

    Observed Mintlify behavior:
      - HTML tags are stripped
      - Markdown bold/italic/code/link syntax is stripped
      - Text is lowercased
      - Spaces and underscores become hyphens
      - Unicode word characters are kept (letters incl. Japanese/accented, digits)
      - Em-dashes (—) are kept; other punctuation is removed
      - Multiple consecutive hyphens are collapsed
      - Leading/trailing hyphens are removed
    """
    # Remove leading # markers
    text = re.sub(r'^#+\s*', '', raw_line.strip())
    # Strip HTML tags (including self-closing)
    text = re.sub(r'<[^>]+/?>', '', text)
    # Strip Markdown link syntax: [label](url) → label
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    # Strip bold/italic markers (***text***, **text**, *text*)
    text = re.sub(r'\*{1,3}([^*]*)\*{1,3}', r'\1', text)
    text = re.sub(r'\*+', '', text)
    # Strip inline code backticks
    text = re.sub(r'`([^`]*)`', r'\1', text)
    # Strip remaining brackets
    text = re.sub(r'[\[\]()]', '', text)
    # Lowercase
    text = text.lower()
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Keep Unicode word chars (letters incl. Japanese/accented), digits, hyphens, em-dashes
    text = re.sub(r'[^\w\-—]', '', text)
    # \w preserves underscores — convert any that remain after the first pass
    text = text.replace('_', '-')
    # Collapse runs of hyphens
    text = re.sub(r'-{2,}', '-', text)
    return text.strip('-')


def load_headers(filepath: Path) -> list[tuple[str, str]]:
    """
    Return [(anchor, raw_header_text), ...] for all Markdown headers in a file.
    """
    result = []
    try:
        for line in filepath.read_text(encoding='utf-8').splitlines():
            if re.match(r'^#{1,6}\s', line):
                raw_text = re.sub(r'^#+\s*', '', line.strip())
                anchor = header_to_anchor(line)
                if anchor:
                    result.append((anchor, raw_text))
    except (OSError, UnicodeDecodeError):
        pass
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Anchor matching
# ─────────────────────────────────────────────────────────────────────────────

def match_anchor(
    old_anchor: str,
    headers: list[tuple[str, str]],
) -> tuple[str | None, str | None, float]:
    """
    Find the best-matching new anchor for an old underscore-style anchor.

    Strategy:
      1. Exact match after _ → - substitution (confidence 1.0)
      2. Keyword overlap between old anchor tokens and each header's anchor/text
         (Jaccard-like score, boosted if old anchor's words are fully covered)

    Returns (new_anchor, header_text, confidence) or (None, None, 0.0).
    """
    # Step 1: exact slug match
    direct = re.sub(r'_', '-', old_anchor.lower())
    for anch, txt in headers:
        if anch == direct:
            return anch, txt, 1.0

    # Step 2: keyword matching
    old_words = {w for w in re.split(r'[_\-—]+', old_anchor.lower()) if w}
    best: tuple[str | None, str | None, float] = (None, None, 0.0)

    for anch, txt in headers:
        # Words from the generated anchor
        anch_words = {w for w in re.split(r'[-—]+', anch.lower()) if w}
        # Words from the raw header text (after stripping punctuation)
        plain_txt = re.sub(r'[^a-z0-9\s]', ' ', txt.lower())
        text_words = {w for w in plain_txt.split() if w}
        all_words = anch_words | text_words

        if not all_words:
            continue
        common = old_words & all_words
        if not common:
            continue

        score = len(common) / max(len(old_words), len(all_words))
        # Boost when all old keywords are present in the candidate
        if old_words.issubset(all_words):
            score = min(1.0, score + 0.25)

        if score > best[2]:
            best = (anch, txt, score)

    return best if best[2] >= 0.25 else (None, None, 0.0)


# ─────────────────────────────────────────────────────────────────────────────
# Article index (English articles only — cross-article links always target EN)
# ─────────────────────────────────────────────────────────────────────────────

def build_en_index(repo_root: Path) -> dict[str, Path]:
    """
    Map {article_stem: Path} for English articles in s/article and s/topic.
    Cross-article links in all files (including localized) reference English articles.
    """
    index: dict[str, Path] = {}
    for d in ("s/article", "s/topic"):
        dirpath = repo_root / d
        if not dirpath.is_dir():
            continue
        for f in dirpath.glob("*.mdx"):
            index[f.stem] = f
    return index


# ─────────────────────────────────────────────────────────────────────────────
# File processing
# ─────────────────────────────────────────────────────────────────────────────

def file_language(filepath: Path, repo_root: Path) -> str:
    """Return 'en' or the localized language prefix for a file."""
    try:
        first_part = filepath.relative_to(repo_root).parts[0]
        return first_part if first_part in LOCALIZED_PREFIXES else 'en'
    except (ValueError, IndexError):
        return 'en'


def process_file(
    filepath: Path,
    repo_root: Path,
    en_index: dict[str, Path],
    header_cache: dict[str, list],
    verbose: bool = False,
    include_low: bool = False,
    strip_unresolved: bool = False,
) -> tuple[str, str, list[str]]:
    """
    Scan a single MDX file and build the replacement text.

    Returns (original_text, new_text, log_lines).
    Log lines describe each anchor match or failure.
    """
    try:
        original = filepath.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as e:
        return '', '', [f'  ERROR reading file: {e}']

    current_id = filepath.stem
    is_localized = file_language(filepath, repo_root) != 'en'
    rel_path = str(filepath.relative_to(repo_root))
    log: list[str] = []
    # Track (article_id, old_anchor) pairs already logged to prevent duplicates
    # from re.sub running multiple patterns on converted text.
    logged_issues: set[tuple[str, str]] = set()

    # ── Load self-headers (used for same-article bare anchors) ───────────────
    self_key = str(filepath)
    if self_key not in header_cache:
        header_cache[self_key] = load_headers(filepath)
    self_headers = header_cache[self_key]

    # ── Helper: load headers for a cross-article target ──────────────────────
    def get_cross_headers(article_id: str) -> list[tuple[str, str]]:
        if article_id not in header_cache:
            target = en_index.get(article_id)
            if target:
                header_cache[article_id] = load_headers(target)
            else:
                header_cache[article_id] = []
        return header_cache[article_id]

    # ── Helper: resolve an anchor to its new value ────────────────────────────
    def resolve(
        old_anchor: str,
        article_id: str,
        headers: list[tuple[str, str]],
        is_same_article: bool,
    ) -> str | None:
        """
        Find the new anchor. Returns None if unresolvable (anchor left unchanged).
        Logs the outcome at appropriate verbosity.
        """
        if not headers:
            key = (article_id, old_anchor)
            if key not in logged_issues:
                logged_issues.add(key)
                if strip_unresolved:
                    log.append(
                        f'  STRIPPED   #{old_anchor}'
                        f' → no headers found for article {article_id!r}'
                    )
                else:
                    log.append(
                        f'  UNMATCHED  #{old_anchor}'
                        f' → no headers found for article {article_id!r}'
                    )
            return _STRIP if strip_unresolved else None

        new_anch, header_txt, conf = match_anchor(old_anchor, headers)

        if new_anch is None:
            key = (article_id, old_anchor)
            if key not in logged_issues:
                logged_issues.add(key)
                if strip_unresolved:
                    loc_note = ' (localized)' if (is_same_article and is_localized) else ''
                    log.append(
                        f'  STRIPPED   #{old_anchor}'
                        f' → no match in {article_id!r}{loc_note}'
                    )
                else:
                    flag = 'LOCALIZED' if (is_same_article and is_localized) else 'UNMATCHED'
                    log.append(
                        f'  {flag:<10} #{old_anchor}'
                        f' → no match in {article_id!r}'
                    )
            return _STRIP if strip_unresolved else None

        label = 'HIGH' if conf >= 0.80 else 'MED' if conf >= 0.50 else 'LOW'
        loc_flag = '*' if (is_same_article and is_localized) else ' '

        # LOW confidence: log for review but don't apply unless --include-low
        if label == 'LOW' and not include_low:
            key = (article_id, old_anchor)
            if key not in logged_issues:
                logged_issues.add(key)
                log.append(
                    f'  [LOW{loc_flag} SKIP {conf:.2f}] #{old_anchor}'
                    f' → #{new_anch}  ("{header_txt}") — not applied; verify manually'
                )
            return None  # leave anchor unchanged

        # Manually reviewed bad LOW matches: skip even with --include-low
        if label == 'LOW' and (rel_path, old_anchor) in LOW_MANUAL_SKIP:
            key = (article_id, old_anchor)
            if key not in logged_issues:
                logged_issues.add(key)
                if strip_unresolved:
                    log.append(
                        f'  STRIPPED   #{old_anchor}'
                        f' → wrong match confirmed (manual skip)'
                    )
                else:
                    log.append(
                        f'  [LOW{loc_flag} MSKIP {conf:.2f}] #{old_anchor}'
                        f' → #{new_anch}  ("{header_txt}") — skipped (manual review: wrong match)'
                    )
            return _STRIP if strip_unresolved else None

        # Always record the match for counting; suppress display when verbose=False + HIGH
        key = (article_id, old_anchor, new_anch)
        if key not in logged_issues:
            logged_issues.add(key)
            log.append(
                f'  [{label}{loc_flag}  {conf:.2f}] #{old_anchor}'
                f' → #{new_anch}  ("{header_txt}")'
            )
        return new_anch

    def needs_fixing(anchor: str) -> bool:
        """Only anchors with underscores need updating."""
        return '_' in anchor

    # ── Regex components ──────────────────────────────────────────────────────
    SF   = r'https?://domo-support\.domo\.com/s/article/'
    QS   = r'(?:\?[^#\s"\'>\n]*)?'          # optional ?query_string
    ID   = r'([A-Za-z0-9_\-\.]+)'           # article ID / slug
    ANCH = r'([A-Za-z][A-Za-z0-9_\-]*)'    # anchor fragment (letters/digits/underscores/hyphens)
    TITL = r'(?:\s+"[^"]*")?'               # optional Markdown link title attribute
    # Link text: plain text or one level of nested brackets (e.g. for image alts)
    LT   = r'((?:[^\[\]]|\[[^\[\]]*\])*)'

    # ── Patterns ──────────────────────────────────────────────────────────────
    # 1. Salesforce URL in Markdown: [text](https://domo-support...ID?qs#anchor "title")
    P_SF_MD = re.compile(
        r'\[' + LT + r'\]\(' + SF + ID + QS + r'#' + ANCH + TITL + r'\)'
    )
    # 2. Root-relative in Markdown: [text](/s/article/ID#anchor)
    P_REL_MD = re.compile(
        r'\[' + LT + r'\]\(/s/article/' + ID + r'#' + ANCH + r'\)'
    )
    # 3. Bare anchor in Markdown: [text](#anchor)
    P_BARE_MD = re.compile(
        r'\[' + LT + r'\]\(#' + ANCH + r'\)'
    )
    # 4. Salesforce URL in HTML href attribute
    P_SF_HREF = re.compile(
        r'(href=["\'])' + SF + ID + QS + r'#' + ANCH + r'(["\'])'
    )
    # 5. Root-relative in HTML href
    P_REL_HREF = re.compile(
        r'(href=["\'])/s/article/' + ID + r'#' + ANCH + r'(["\'])'
    )
    # 6. Bare anchor in HTML href
    P_BARE_HREF = re.compile(
        r'(href=["\'])#' + ANCH + r'(["\'])'
    )

    # ── Substitution callbacks ────────────────────────────────────────────────

    def sub_sf_md(m: re.Match) -> str:
        link_text  = m.group(1)
        article_id = m.group(2)
        old_anchor = m.group(3)
        same = (article_id == current_id)
        headers = self_headers if same else get_cross_headers(article_id)
        if needs_fixing(old_anchor):
            resolved = resolve(old_anchor, article_id, headers, same)
            if resolved == _STRIP:
                return link_text if same else f'[{link_text}](/s/article/{article_id})'
            new_anch = resolved or old_anchor
        else:
            new_anch = old_anchor
        if same:
            return f'[{link_text}](#{new_anch})'
        return f'[{link_text}](/s/article/{article_id}#{new_anch})'

    def sub_rel_md(m: re.Match) -> str:
        link_text  = m.group(1)
        article_id = m.group(2)
        old_anchor = m.group(3)
        if not needs_fixing(old_anchor):
            return m.group(0)
        same = (article_id == current_id)
        headers = self_headers if same else get_cross_headers(article_id)
        resolved = resolve(old_anchor, article_id, headers, same)
        if resolved == _STRIP:
            return link_text if same else f'[{link_text}](/s/article/{article_id})'
        new_anch = resolved or old_anchor
        if same:
            return f'[{link_text}](#{new_anch})'
        return f'[{link_text}](/s/article/{article_id}#{new_anch})'

    def sub_bare_md(m: re.Match) -> str:
        link_text  = m.group(1)
        old_anchor = m.group(2)
        if not needs_fixing(old_anchor):
            return m.group(0)
        resolved = resolve(old_anchor, current_id, self_headers, True)
        if resolved == _STRIP:
            return link_text  # bare anchors are always same-article → plain text
        new_anch = resolved or old_anchor
        return f'[{link_text}](#{new_anch})'

    def sub_sf_href(m: re.Match) -> str:
        q_open     = m.group(1)
        article_id = m.group(2)
        old_anchor = m.group(3)
        q_close    = m.group(4)
        same = (article_id == current_id)
        headers = self_headers if same else get_cross_headers(article_id)
        if needs_fixing(old_anchor):
            resolved = resolve(old_anchor, article_id, headers, same)
            if resolved == _STRIP:
                if same:
                    return f'{q_open}{q_close}'  # href="" → links to page top
                return f'{q_open}/s/article/{article_id}{q_close}'
            new_anch = resolved or old_anchor
        else:
            new_anch = old_anchor
        if same:
            return f'{q_open}#{new_anch}{q_close}'
        return f'{q_open}/s/article/{article_id}#{new_anch}{q_close}'

    def sub_rel_href(m: re.Match) -> str:
        q_open     = m.group(1)
        article_id = m.group(2)
        old_anchor = m.group(3)
        q_close    = m.group(4)
        if not needs_fixing(old_anchor):
            return m.group(0)
        same = (article_id == current_id)
        headers = self_headers if same else get_cross_headers(article_id)
        resolved = resolve(old_anchor, article_id, headers, same)
        if resolved == _STRIP:
            if same:
                return f'{q_open}{q_close}'  # href=""
            return f'{q_open}/s/article/{article_id}{q_close}'
        new_anch = resolved or old_anchor
        if same:
            return f'{q_open}#{new_anch}{q_close}'
        return f'{q_open}/s/article/{article_id}#{new_anch}{q_close}'

    def sub_bare_href(m: re.Match) -> str:
        q_open     = m.group(1)
        old_anchor = m.group(2)
        q_close    = m.group(3)
        if not needs_fixing(old_anchor):
            return m.group(0)
        resolved = resolve(old_anchor, current_id, self_headers, True)
        if resolved == _STRIP:
            return f'{q_open}{q_close}'  # href="" → page top
        new_anch = resolved or old_anchor
        return f'{q_open}#{new_anch}{q_close}'

    # ── Apply patterns in order (most specific → least specific) ─────────────
    # resolve() is called inside each callback; include_low is captured via closure.
    text = original
    text = P_SF_MD.sub(sub_sf_md, text)
    text = P_REL_MD.sub(sub_rel_md, text)
    text = P_BARE_MD.sub(sub_bare_md, text)
    text = P_SF_HREF.sub(sub_sf_href, text)
    text = P_REL_HREF.sub(sub_rel_href, text)
    text = P_BARE_HREF.sub(sub_bare_href, text)

    return original, text, log


# ─────────────────────────────────────────────────────────────────────────────
# File discovery
# ─────────────────────────────────────────────────────────────────────────────

def get_files(repo_root: Path, single_file: Path | None) -> list[Path]:
    if single_file:
        return [single_file.resolve()]
    files: list[Path] = []
    for d in SEARCH_DIRS:
        dirpath = repo_root / d
        if dirpath.is_dir():
            files.extend(sorted(dirpath.glob("*.mdx")))
    return files


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Fix old Salesforce underscore anchors in MDX article files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--apply', action='store_true',
        help='Write changes to disk (default: dry run only)',
    )
    parser.add_argument(
        '--include-low', action='store_true',
        help='Also apply LOW confidence matches (< 0.50); by default these are skipped',
    )
    parser.add_argument(
        '--strip-unresolved', action='store_true',
        help=(
            'Strip unresolvable anchors instead of leaving them unchanged. '
            'Cross-article links lose the #fragment; same-article bare-anchor links '
            'become plain text. Applies to UNMATCHED, LOCALIZED, and MSKIP items.'
        ),
    )
    parser.add_argument(
        '--file', type=Path, metavar='PATH',
        help='Process a single file (path relative to repo root, or absolute)',
    )
    parser.add_argument(
        '--output', type=Path, metavar='PATH',
        help='Write diff output to a file instead of stdout',
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help='Show HIGH-confidence matches in addition to MED/LOW',
    )
    args = parser.parse_args()

    if args.file:
        single = args.file if args.file.is_absolute() else REPO_ROOT / args.file
    else:
        single = None

    out = open(args.output, 'w', encoding='utf-8') if args.output else None

    def emit(text: str = '') -> None:
        if out:
            out.write(text + '\n')
        else:
            print(text)

    files = get_files(REPO_ROOT, single)
    en_index = build_en_index(REPO_ROOT)
    header_cache: dict[str, list] = {}

    files_changed    = 0
    anchors_applied  = 0
    anchors_stripped = 0
    unmatched_items: list[str] = []
    localized_items: list[str] = []
    low_items:       list[str] = []
    stripped_items:  list[str] = []

    for filepath in files:
        original, new_text, log = process_file(
            filepath, REPO_ROOT, en_index, header_cache,
            verbose=args.verbose,
            include_low=args.include_low,
            strip_unresolved=args.strip_unresolved,
        )
        if not original and not log:
            continue

        changed = original != new_text
        rel = filepath.relative_to(REPO_ROOT)

        # Partition log lines by type
        stripped  = [l for l in log if 'STRIPPED' in l]
        unmatched = [l for l in log if 'UNMATCHED' in l or 'WARN' in l]
        localized = [l for l in log if 'LOCALIZED' in l]
        low_skip  = [l for l in log if 'SKIP' in l]
        # For display: applied matches; suppress HIGH when not verbose
        applied_log = [
            l for l in log
            if '→ #' in l and 'SKIP' not in l
        ]
        display_log = [
            l for l in applied_log
            if args.verbose or not l.strip().startswith('[HIGH')
        ] + stripped  # always show what was stripped

        unmatched_items.extend(f'{rel}: {l.strip()}' for l in unmatched)
        localized_items.extend(f'{rel}: {l.strip()}' for l in localized)
        low_items.extend(f'{rel}: {l.strip()}' for l in low_skip)
        stripped_items.extend(f'{rel}: {l.strip()}' for l in stripped)

        if not changed:
            continue

        applied_count = len(applied_log)
        anchors_applied += applied_count
        anchors_stripped += len(stripped)
        files_changed += 1

        # ── File block ────────────────────────────────────────────────────
        emit(f'\n{"=" * 72}')
        emit(f'FILE: {rel}')
        emit(f'{"=" * 72}')

        for line in display_log:
            emit(line)

        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f'a/{rel}',
            tofile=f'b/{rel}',
            n=2,
        )
        for chunk in diff:
            emit(chunk.rstrip('\n'))

        if args.apply:
            filepath.write_text(new_text, encoding='utf-8')
            emit('  [WRITTEN]')

    # ── Summary ───────────────────────────────────────────────────────────────
    emit(f'\n{"=" * 72}')
    emit('SUMMARY')
    emit(f'{"=" * 72}')
    emit(f'  Mode:             {"APPLY — changes written to disk" if args.apply else "DRY RUN — no files modified"}')
    emit(f'  LOW included:     {"yes (--include-low)" if args.include_low else "no  (LOW items skipped; see below)"}')
    emit(f'  Strip unresolved: {"yes (--strip-unresolved)" if args.strip_unresolved else "no  (unresolved anchors left unchanged)"}')
    emit(f'  Files changed:    {files_changed}')
    emit(f'  Anchors applied:  {anchors_applied}')
    emit(f'  Anchors stripped: {anchors_stripped}')

    if low_items:
        emit(f'\nLOW CONFIDENCE ({len(low_items)}) — skipped; verify and fix manually:')
        for item in low_items:
            emit(f'  {item}')

    if stripped_items:
        emit(
            f'\nSTRIPPED ({len(stripped_items)}) — anchor removed; '
            f'cross-article links keep path, same-article links become plain text:'
        )
        for item in stripped_items:
            emit(f'  {item}')

    if unmatched_items:
        emit(f'\nUNMATCHED ({len(unmatched_items)}) — no header found; fix manually:')
        for item in unmatched_items:
            emit(f'  {item}')

    if localized_items:
        emit(
            f'\nLOCALIZED SAME-ARTICLE ({len(localized_items)}) — '
            f'English anchor names vs foreign-language headers; fix manually:'
        )
        for item in localized_items:
            emit(f'  {item}')

    if out:
        out.close()
        print(f'Diff written to: {args.output}')


if __name__ == '__main__':
    main()
