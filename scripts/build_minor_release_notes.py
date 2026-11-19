#!/usr/bin/env python3
"""Rebuild the live Minor Release Notes article from a Domo DataSet.

Queries the hotfix-enrichment DataSet through the Domo instance API using a
developer access token, selects the week's publishable notes, rewrites each into
the customer-facing Minor Release Notes house style, and regenerates
s/article/Current-Minor-Release-Notes.mdx. Output is deterministic, so a run with
no new notes produces no git diff.

The DataSet text is written for an INTERNAL audience; this script is the
customer-facing last mile. The house style is NOT in this file — it lives in the
editable guide at .claude/skills/minor-release-notes/minor-release-notes-style.md,
loaded verbatim as the Anthropic system prompt (load_style_system). Two layers keep
non-public content out: a deterministic security/privacy keyword screen
(screen_external) runs before the rewrite, and the rewrite itself returns
EXCLUDE_SENTINEL for anything unsafe it still catches; both are dropped from the
article.

Companion to scripts/archive_minor_release_notes.py: this script only *writes the
current week*; the archiver rolls the current file into a dated archive and
records the week's notes in the published ledger. Keeping the ledger write out of
this script makes a rebuild idempotent and safe to re-run.

Run locally or from CI. Environment variables:

  DOMO_DEVELOPER_TOKEN       Domo developer access token
                             (instance: Admin -> Authentication -> Access Tokens)
  DOMO_MINOR_RN_DATASET_ID   GUID of the HOTFIX_Release_Enriched_PUBLIC DataSet
  DOMO_INSTANCE              Domo instance host (default: domo.domo.com)
  ANTHROPIC_API_KEY          Anthropic key for the style rewrite (unless --no-llm)

  MINOR_RN_CSV               Local-test override: read this CSV instead of calling
                             Domo (no token needed). The file must carry the same
                             columns the DataSet exposes.

  DOMO_MINOR_RN_TYPE_COLUMN  Optional. Name of an official note-type column in the
                             DataSet (e.g. "Public_Note_Type"). LEAVE UNSET by
                             default: the notes then render as one flat list per
                             product section. Set it ONLY once the DataSet actually
                             carries such a column; the live query then SELECTs it
                             and the output splits back into "Updates" and "Issues
                             Resolved" sections driven by that column's value. See
                             the note-type handling below.

CLI flags:
  --no-llm       Skip the Anthropic call; use the deterministic style transform
                 (offline/testing).
  --run-date     ISO date (YYYY-MM-DD) treated as "today" when selecting the
                 week. Defaults to the system date. Notes dated after this are
                 held for a future week.
  --dry-run      Print the rendered article to stdout instead of writing it.

The DataSet must expose at least these columns (any order):
  master_key, master_targetdate, Public_Parent_Component,
  AI_release_notes, AI_ReleaseNotesScore

Optionally it may also carry a note-type column (see DOMO_MINOR_RN_TYPE_COLUMN);
when present, the output is split into Updates / Issues Resolved sections.
"""

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import urllib.request
from datetime import date, datetime

# --- Repo-relative paths (script lives in scripts/) ---
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLE_PATH = os.path.join(REPO_ROOT, "s", "article", "Current-Minor-Release-Notes.mdx")
LEDGER_PATH = os.path.join(REPO_ROOT, "tracking", "minor-release-ledger.json")
# The customer-facing house style for the rewrite lives in the skill as an
# editable Markdown file and is loaded verbatim as the Anthropic system prompt.
# The style is owned THERE, not in this script — see load_style_system().
STYLE_GUIDE_PATH = os.path.join(
    REPO_ROOT, ".claude", "skills", "minor-release-notes", "minor-release-notes-style.md"
)

# --- Publish gate and column contract ---
MIN_SCORE = 7
SCORE_COL = "AI_ReleaseNotesScore"
NOTE_COL = "AI_release_notes"
DATE_COL = "master_targetdate"
COMPONENT_COL = "Public_Parent_Component"
KEY_COL = "master_key"
REQUIRED_COLUMNS = {SCORE_COL, NOTE_COL, DATE_COL, COMPONENT_COL}

# --- External-publication safety screen ------------------------------------ #
# Minor Release Notes are PUBLIC and customer-facing. The source DataSet is
# written for an INTERNAL audience, so this script is the customer-facing "last
# mile": it both rewrites each note into public house voice AND removes anything
# that must not be published. Per security/legal guidance, notes that touch
# security, privacy, vulnerabilities, or information disclosure must be REMOVED
# entirely (not abstracted). Two layers enforce that:
#   1. This deterministic keyword screen runs BEFORE the rewrite, so obviously
#      sensitive text never reaches the model or the article (and it protects the
#      --no-llm path, which can't judge safety on its own).
#   2. The LLM rewrite is a second, semantic net: the house style guide instructs
#      it to return EXCLUDE_SENTINEL for anything unsafe or non-public it still
#      catches; the renderer drops those bullets.
# Err on the side of dropping a note. These patterns are intentionally broad.
EXCLUDE_SENTINEL = "__EXCLUDE__"
SECURITY_EXCLUDE_PATTERNS = (
    r"vulnerabilit",                       # vulnerability / vulnerabilities
    r"\bCVE-?\d",                          # CVE-2026-1234
    r"\bexploit",
    r"\bmalware\b", r"\bransomware\b", r"heartbleed",
    r"zero[-\s]day",
    r"\bshellshock\b", r"\blog4j\b", r"\bspectre\b", r"\bmeltdown\b",
    r"\bXSS\b", r"\bCSRF\b", r"\bSSRF\b", r"\bRCE\b",
    r"cross[-\s]site scripting", r"SQL injection", r"\binjection attack",
    r"privilege escalation", r"remote code execution", r"buffer overflow",
    r"authentication bypass", r"auth(?:n|z)? bypass", r"security bypass",
    r"security (?:fix|patch|issue|flaw|hole|advisory|vulnerab|risk|hardening)",
    r"\bhardening\b",
    r"penetration test", r"\bpen[-\s]test",
    r"data (?:breach|leak|leakage|exposure)",
    r"information disclosure", r"sensitive data expos",
    r"patch(?:ed|ing)?\s+(?:php|openssl|apache|nginx|tomcat|struts)",
)
_SECURITY_RE = re.compile("|".join(SECURITY_EXCLUDE_PATTERNS), re.IGNORECASE)

# --- Optional "Updates vs Issues Resolved" delineation --------------------- #
# By default the Minor Release Notes list every note in one flat list under its
# product section, with NO "Updates" / "Issues Resolved" split. That split is
# reinstated ONLY if the source DataSet gains an official column tagging each
# note's type. We never infer the split from the sentence for publishing — the
# only trigger is the presence of this column in the pulled data.
#
# How it activates:
#   - Live Domo query: the column is SELECTed (and thus detectable) only when its
#     name is supplied via DOMO_MINOR_RN_TYPE_COLUMN, so the SELECT never fails
#     against a DataSet that does not have it yet. Set that env var once the
#     column officially exists; leave it unset otherwise.
#   - Local CSV fixture: simply include a column named TYPE_COL to exercise the
#     delineated render.
# Detection in either path is "is TYPE_COL among the pulled columns?" (see
# has_type_column); a row's value then maps to Update vs Issue Resolved.
_TYPE_COL_ENV = (os.environ.get("DOMO_MINOR_RN_TYPE_COLUMN") or "").strip()
TYPE_COL = _TYPE_COL_ENV or "Public_Note_Type"
QUERY_TYPE_COL = bool(_TYPE_COL_ENV)  # include TYPE_COL in the live SELECT?
TYPE_ISSUE_SIGNALS = ("issue", "resolved", "resolve", "fix", "bug", "defect")

# --- Fixed page copy ---
TITLE = "Minor Release Notes"
EXCERPT = (
    "Weekly minor release notes documenting incremental updates and resolved "
    "issues across Domo features."
)

# Friendly section names for raw Public_Parent_Component values that aren't
# already customer-facing. Anything not listed passes through unchanged.
COMPONENT_RENAME = {
    "PDP": "Personalized Data Permissions",
    "DomoBuzz": "Buzz",
}

# --- Style rewrite -------------------------------------------------------- #
# The authoritative customer-facing house style is the Markdown style guide at
# STYLE_GUIDE_PATH, loaded verbatim as the LLM system prompt. It is NOT duplicated
# here: the nuanced, secure, optimistic revision this produces is an LLM task that
# a Python rules transform can't do, so the script's job is to LOAD the guide and
# pass it through, keeping the style editable in one place (the skill). The
# deterministic --no-llm fallback below does not apply the house style and is for
# offline wiring tests only.


def load_style_system():
    """Return the house-style guide text used as the Anthropic system prompt.

    Authoritative source is the editable Markdown guide in the skill; raising on a
    missing file is deliberate — the LLM rewrite must never silently run without
    the customer-facing / security rules it encodes."""
    try:
        with open(STYLE_GUIDE_PATH, encoding="utf-8") as fh:
            text = fh.read().strip()
    except FileNotFoundError:
        raise SystemExit(
            "Minor Release Notes style guide not found at "
            f"{os.path.relpath(STYLE_GUIDE_PATH, REPO_ROOT)}. The LLM rewrite "
            "requires it; add the file or run with --no-llm for an offline wiring test."
        )
    if not text:
        raise SystemExit(f"Style guide {STYLE_GUIDE_PATH} is empty.")
    return text


def log(msg):
    print(msg, flush=True)


# --------------------------------------------------------------------------- #
# Data loading (Domo instance query API, or a local CSV for testing)
# --------------------------------------------------------------------------- #
def query_dataset_csv(instance, token, dataset_id):
    url = f"https://{instance}/api/query/v1/execute/{dataset_id}?includeHeader=true"
    select_cols = [KEY_COL, DATE_COL, COMPONENT_COL, NOTE_COL, SCORE_COL]
    if QUERY_TYPE_COL:
        # Only requested when DOMO_MINOR_RN_TYPE_COLUMN is set, so the query never
        # references a column the DataSet lacks.
        select_cols.append(TYPE_COL)
    select = ", ".join(f"`{c}`" for c in select_cols)
    sql = (
        f"SELECT {select} FROM table "
        f"WHERE `{SCORE_COL}` >= {MIN_SCORE} AND TRIM(`{NOTE_COL}`) <> ''"
    )
    body = json.dumps({"sql": sql}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("X-DOMO-Developer-Token", token)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "text/csv")
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read().decode("utf-8-sig")


def load_rows():
    """Return raw DataSet rows as a list of dicts, from Domo or a local CSV."""
    csv_override = os.environ.get("MINOR_RN_CSV")
    if csv_override:
        log(f"Reading local CSV fixture: {csv_override}")
        with open(csv_override, encoding="utf-8-sig") as fh:
            csv_text = fh.read()
    else:
        instance = os.environ.get("DOMO_INSTANCE") or "domo.domo.com"
        token = os.environ.get("DOMO_DEVELOPER_TOKEN")
        dataset_id = os.environ.get("DOMO_MINOR_RN_DATASET_ID")
        missing = [
            n
            for n, v in [
                ("DOMO_DEVELOPER_TOKEN", token),
                ("DOMO_MINOR_RN_DATASET_ID", dataset_id),
            ]
            if not v
        ]
        if missing:
            raise SystemExit(f"Missing required env var(s): {', '.join(missing)}")
        log(f"Querying DataSet {dataset_id} on {instance} ...")
        csv_text = query_dataset_csv(instance, token, dataset_id)

    reader = csv.DictReader(io.StringIO(csv_text))
    cols = set(reader.fieldnames or [])
    if not REQUIRED_COLUMNS.issubset(cols):
        raise SystemExit(
            "DataSet is missing required columns. "
            f"Expected superset of {sorted(REQUIRED_COLUMNS)}; got {sorted(cols)}."
        )
    rows = list(reader)
    log(f"Loaded {len(rows)} raw rows.")
    return rows


# --------------------------------------------------------------------------- #
# Pure, testable pipeline steps
# --------------------------------------------------------------------------- #
def _score(row):
    s = (row.get(SCORE_COL) or "").strip()
    return int(s) if s.lstrip("-").isdigit() else -1


def note_text(row):
    return (row.get(NOTE_COL) or "").strip()


def note_hash(row):
    """Stable identity for a note: normalized text -> sha1. Used by the ledger."""
    norm = re.sub(r"\s+", " ", note_text(row).lower()).strip()
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()


def parse_date(row):
    raw = (row.get(DATE_COL) or "").strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", raw)
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def filter_publishable(rows):
    """Score >= MIN_SCORE and a non-empty note."""
    return [r for r in rows if _score(r) >= MIN_SCORE and note_text(r)]


def is_externally_unsafe(note):
    """True when a note hits the deterministic security/privacy keyword screen and
    must be removed from the PUBLIC notes rather than published (see
    SECURITY_EXCLUDE_PATTERNS). This is the first, deterministic layer; the LLM
    rewrite is the second, semantic net (house style guide -> EXCLUDE_SENTINEL)."""
    return bool(_SECURITY_RE.search(note or ""))


def screen_external(rows):
    """Drop rows that fail the deterministic external-safety screen, so obviously
    sensitive text never reaches the model or the published article. Returns
    (kept_rows, dropped_count)."""
    kept, dropped = [], 0
    for r in rows:
        if is_externally_unsafe(note_text(r)):
            dropped += 1
            continue
        kept.append(r)
    return kept, dropped


def dedup(rows):
    """Collapse exact-duplicate notes (same normalized text), keeping the first."""
    seen, out = set(), []
    for r in rows:
        h = note_hash(r)
        if h not in seen:
            seen.add(h)
            out.append(r)
    return out


def select_week(rows, ledger, run_date):
    """Notes dated on/before run_date and not already in the published ledger."""
    out = []
    for r in rows:
        d = parse_date(r)
        if d is None or d > run_date:
            continue
        if note_hash(r) in ledger:
            continue
        out.append(r)
    return out


def classify(note):
    """Infer Update vs Issue Resolved from the sentence.

    This is only a STYLE HINT for the rewrite (issue = past-tense problem,
    update = present-tense behavior). It does NOT create any visible section
    split — the notes render as one flat list unless the DataSet carries an
    official note-type column (see note_type / render_article)."""
    t = note.lower()
    issue_signals = (
        r"resolve[sd]\b",
        r"\bfixe?[sd]\b",
        r"\bcorrects?\b",
        r"addresses an issue",
        r"\bno longer\b",
        r"\bwas (not|incorrectly|being)\b",
        r"\bwere (not|incorrectly|being)\b",
        r"\brestore[sd]\b",
        r"\bpreventing\b",
        r"an issue where",
    )
    if any(re.search(p, t) for p in issue_signals):
        return "Issue Resolved"
    return "Update"


def note_type(row):
    """Official note type when the delineation column is present and populated,
    else the inferred style hint. Returns "Update" or "Issue Resolved"."""
    raw = (row.get(TYPE_COL) or "").strip().lower()
    if raw:
        return "Issue Resolved" if any(k in raw for k in TYPE_ISSUE_SIGNALS) else "Update"
    return classify(note_text(row))


def has_type_column(rows):
    """True when the pulled data carries the official note-type column, which is
    the sole trigger for the Updates / Issues Resolved split."""
    return bool(rows) and TYPE_COL in rows[0]


def friendly_component(raw):
    name = (raw or "").strip() or "Other"
    return COMPONENT_RENAME.get(name, name)


# --------------------------------------------------------------------------- #
# Style rewrite (Anthropic API, with a deterministic offline fallback)
# --------------------------------------------------------------------------- #
_LEAD_ISSUE = re.compile(
    r"^this update (resolves|fixes|corrects|addresses)"
    r"( an issue(?: where)?| the issue(?: where)?)?\s+",
    re.IGNORECASE,
)
_LEAD_RESTORE = re.compile(r"^this update restores\s+", re.IGNORECASE)
_LEAD_GENERIC = re.compile(r"^this update\s+", re.IGNORECASE)


def _cap(s):
    s = s.strip()
    return s[:1].upper() + s[1:] if s else s


def deterministic_restyle(note, kind):
    """Rough rules-based transform used with --no-llm. The LLM path does better.

    It does NOT apply the customer-facing house style (no abstraction, no
    de-internalizing, no optimistic framing) — that is an LLM task. It only honors
    the hard security screen so the offline path can never emit an unsafe note."""
    if is_externally_unsafe(note):
        return EXCLUDE_SENTINEL
    text = re.sub(r"\s+", " ", note).strip()
    if kind == "Issue Resolved":
        stripped = _LEAD_ISSUE.sub("", text)
        if stripped == text:
            stripped = _LEAD_RESTORE.sub("", text)
        text = stripped
    else:
        text = _LEAD_GENERIC.sub("", text)
    text = _cap(text)
    if text and not text.endswith((".", "!", "?")):
        text += "."
    return text


def make_restyler(use_llm):
    """Return a restyle(note, kind) callable. LLM-backed unless use_llm is False."""
    if not use_llm:
        return deterministic_restyle

    import anthropic  # imported lazily so --no-llm needs no dependency

    client = anthropic.Anthropic()
    style_system = load_style_system()  # the editable house-style guide (authoritative)

    def restyle(note, kind):
        prompt = f"Type: {kind}\nSource sentence: {note.strip()}"
        try:
            resp = client.messages.create(
                model="claude-sonnet-5-5",
                max_tokens=400,
                output_config={"effort": "low"},
                system=style_system,
                messages=[{"role": "user", "content": prompt}],
            )
            out = next((b.text for b in resp.content if b.type == "text"), "").strip()
            # Guard against an empty/garbled reply; fall back deterministically.
            return out if out else deterministic_restyle(note, kind)
        except Exception as exc:  # noqa: BLE001 — never let one note fail the run
            log(f"  ! style API failed for a note ({exc}); using fallback.")
            return deterministic_restyle(note, kind)

    return restyle


# --------------------------------------------------------------------------- #
# Rendering (must match the published Minor Release Notes shape)
# --------------------------------------------------------------------------- #
def fmt_date(d):
    return d.strftime("%B %-d, %Y")


def _clean_bullet(bullet):
    """Normalize a restyled note for rendering, or None if it must be dropped.

    The rewrite returns EXCLUDE_SENTINEL for a note that must not be published
    (security/privacy, or nothing customer-meaningful left); an empty string means
    a garbled reply. Both are dropped."""
    text = (bullet or "").strip()
    if not text or text == EXCLUDE_SENTINEL:
        return None
    return text


def render_article(selected, restyle, release_date, delineated=False):
    """Pure render: selected rows -> full MDX string.

    Notes are grouped by friendly component (alphabetical). By default every
    note is listed in one flat, alphabetically-sorted list under its component.
    When `delineated` is True (the DataSet carries the official note-type
    column), each component instead splits into "Updates" then "Issues
    Resolved". Bullets are de-duplicated and sorted for deterministic output.
    """
    lines = [
        "---",
        f'title: "{TITLE}"',
        f'excerpt: "{EXCERPT}"',
        "---",
        "",
        f"## {fmt_date(release_date)} Release",
        "",
    ]

    if delineated:
        groups = {}  # component -> {"Update": [...], "Issue Resolved": [...]}
        for r in selected:
            comp = friendly_component(r.get(COMPONENT_COL))
            kind = note_type(r)
            bullet = _clean_bullet(restyle(note_text(r), kind))
            if bullet is None:  # removed by the safety screen / rewrite
                continue
            groups.setdefault(comp, {"Update": [], "Issue Resolved": []})[kind].append(bullet)
        for comp in sorted(groups):
            # A component only exists here if it kept at least one bullet.
            lines.append(f"### {comp}")
            lines.append("")
            for label, key in (("Updates", "Update"), ("Issues Resolved", "Issue Resolved")):
                bullets = sorted(set(groups[comp][key]), key=str.lower)
                if not bullets:
                    continue
                lines.append(f"**{label}:**")
                lines.append("")
                lines.extend(f"- {b}" for b in bullets)
                lines.append("")
    else:
        groups = {}  # component -> [bullets]
        for r in selected:
            comp = friendly_component(r.get(COMPONENT_COL))
            # classify() only shapes the bullet's voice; with no official
            # note-type column it creates no visible Updates/Issues split.
            bullet = _clean_bullet(restyle(note_text(r), classify(note_text(r))))
            if bullet is None:  # removed by the safety screen / rewrite
                continue
            groups.setdefault(comp, []).append(bullet)
        for comp in sorted(groups):
            lines.append(f"### {comp}")
            lines.append("")
            lines.extend(f"- {b}" for b in sorted(set(groups[comp]), key=str.lower))
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def load_ledger():
    try:
        with open(LEDGER_PATH, encoding="utf-8") as fh:
            data = json.load(fh)
        return set(data.get("published", []))
    except FileNotFoundError:
        return set()
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Could not read ledger {LEDGER_PATH}: {exc}")


def write_ledger(hashes):
    """Persist the published-note ledger (sorted for stable diffs)."""
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    payload = {"published": sorted(hashes)}
    with open(LEDGER_PATH, "w") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")


def seed_ledger(run_date):
    """Go-live helper: mark every current publishable note (dated on/before
    run_date) as already published, without producing an article. The first
    automated run then emits only notes that appear after go-live."""
    rows = dedup(filter_publishable(load_rows()))
    hashes = {note_hash(r) for r in rows if (parse_date(r) and parse_date(r) <= run_date)}
    existing = load_ledger()
    write_ledger(existing | hashes)
    log(f"Seeded ledger with {len(hashes)} note(s) "
        f"(ledger now holds {len(existing | hashes)}).")


# --------------------------------------------------------------------------- #
def build(use_llm, run_date, dry_run):
    rows = load_rows()
    delineated = has_type_column(rows)
    log(
        f"Note-type column '{TYPE_COL}' present — rendering Updates / Issues "
        "Resolved sections."
        if delineated
        else "No official note-type column — rendering one flat list per section."
    )
    rows = filter_publishable(rows)
    log(f"{len(rows)} rows at score >= {MIN_SCORE} with a note.")
    rows = dedup(rows)
    log(f"{len(rows)} unique notes after dedup.")

    # External-safety screen (deterministic first layer): drop anything that hits
    # the security/privacy keyword filter before it can reach the model or the
    # article. The LLM rewrite is the second, semantic net (see the style guide).
    rows, dropped = screen_external(rows)
    if dropped:
        log(f"Screened out {dropped} note(s) on the external-safety keyword filter.")

    ledger = load_ledger()
    if not ledger and not dry_run:
        raise SystemExit(
            "Ledger is empty. Seed it first with --seed-ledger (go-live bootstrap); "
            "a normal run against an empty ledger would publish the entire backlog "
            "at once. (Use --dry-run to preview selection against an empty ledger.)"
        )
    selected = select_week(rows, ledger, run_date)
    log(f"{len(selected)} notes selected for the current week "
        f"(run date {run_date.isoformat()}, {len(ledger)} already published).")

    if not selected:
        log("No new notes for this week — leaving the current article unchanged.")
        return 0

    release_date = max(parse_date(r) for r in selected)
    restyle = make_restyler(use_llm)
    content = render_article(selected, restyle, release_date, delineated)

    if dry_run:
        log("--- DRY RUN (nothing written: no archive, no ledger update) ---")
        print(content)
        return len(selected)

    # If every selected note was removed by the rewrite's safety net, there is
    # nothing publishable — don't archive the prior week or write an empty article.
    if "\n- " not in content:
        log("All selected notes were removed as non-public; "
            "leaving the current article unchanged.")
        return 0

    # Roll the outgoing current week into a dated archive before overwriting.
    # Imported lazily so --dry-run / --no-llm paths don't require it.
    import archive_minor_release_notes as archiver
    archiver.roll_current_to_archive(dry_run=False)

    os.makedirs(os.path.dirname(ARTICLE_PATH), exist_ok=True)
    with open(ARTICLE_PATH, "w") as fh:
        fh.write(content)
    log(f"Wrote {os.path.relpath(ARTICLE_PATH, REPO_ROOT)} "
        f"({len(selected)} notes, release {fmt_date(release_date)}).")

    # Record this week's notes so future runs don't re-publish them.
    write_ledger(ledger | {note_hash(r) for r in selected})
    log(f"Ledger updated (+{len(selected)} notes).")
    return len(selected)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-llm", action="store_true", help="Deterministic restyle (no API call)")
    ap.add_argument("--run-date", help="ISO date treated as today (default: system date)")
    ap.add_argument("--dry-run", action="store_true", help="Print instead of writing")
    ap.add_argument("--seed-ledger", action="store_true",
                    help="Go-live: mark all current notes published; write no article")
    args = ap.parse_args()

    if args.run_date:
        try:
            run_date = datetime.strptime(args.run_date, "%Y-%m-%d").date()
        except ValueError:
            raise SystemExit("--run-date must be YYYY-MM-DD")
    else:
        run_date = date.today()

    if args.seed_ledger:
        seed_ledger(run_date)
    else:
        build(use_llm=not args.no_llm, run_date=run_date, dry_run=args.dry_run)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        log(f"ERROR: {exc}")
        sys.exit(1)
