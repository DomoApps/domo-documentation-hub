#!/usr/bin/env python3
"""Rebuild the live Minor Release Notes article from a Domo DataSet.

Queries the hotfix-enrichment DataSet through the Domo instance API using a
developer access token, selects the week's publishable notes, restyles each into
Domo house voice, and regenerates s/article/Current-Minor-Release-Notes.mdx.
Output is deterministic, so a run with no new notes produces no git diff.

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

# --- Publish gate and column contract ---
MIN_SCORE = 7
SCORE_COL = "AI_ReleaseNotesScore"
NOTE_COL = "AI_release_notes"
DATE_COL = "master_targetdate"
COMPONENT_COL = "Public_Parent_Component"
KEY_COL = "master_key"
REQUIRED_COLUMNS = {SCORE_COL, NOTE_COL, DATE_COL, COMPONENT_COL}

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

# --- Style rewrite: the house-style spec shared by the LLM and manual reruns.
# Mirrored in the `minor-release-notes` skill; keep the two in sync. ---
STYLE_SYSTEM = (
    "You rewrite internal Domo hotfix release-note sentences into the Domo "
    "Knowledge Base Minor Release Notes house style. Rules:\n"
    "- Return ONE sentence, nothing else: no preamble, no quotes, no bullet "
    "marker, no trailing commentary.\n"
    "- Never begin with \"This update\". For an Issue Resolved, state the "
    "problem that was fixed as a past-tense fact (e.g. \"Hidden calculations "
    "were not being properly deleted from cards.\"). For an Update, use a "
    "present-tense imperative or descriptive statement of the new behavior "
    "(e.g. \"Add new rows in Linked Tables.\").\n"
    "- Keep it factual and customer-facing. Preserve product and feature names "
    "exactly. Do not invent detail that isn't in the source.\n"
    "- American English. End with a period."
)


def log(msg):
    print(msg, flush=True)


# --------------------------------------------------------------------------- #
# Data loading (Domo instance query API, or a local CSV for testing)
# --------------------------------------------------------------------------- #
def query_dataset_csv(instance, token, dataset_id):
    url = f"https://{instance}/api/query/v1/execute/{dataset_id}?includeHeader=true"
    sql = (
        f"SELECT `{KEY_COL}`, `{DATE_COL}`, `{COMPONENT_COL}`, "
        f"`{NOTE_COL}`, `{SCORE_COL}` FROM table "
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
    """Update vs Issue Resolved, inferred from the sentence (no source column)."""
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
    """Rough rules-based transform used with --no-llm. The LLM path does better."""
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

    def restyle(note, kind):
        prompt = f"Type: {kind}\nSource sentence: {note.strip()}"
        try:
            resp = client.messages.create(
                model="claude-haiku-5-5",
                max_tokens=400,
                output_config={"effort": "low"},
                system=STYLE_SYSTEM,
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


def render_article(selected, restyle, release_date):
    """Pure render: selected rows -> full MDX string.

    Groups by friendly component (alphabetical), then Updates before Issues
    Resolved, bullets sorted for deterministic output.
    """
    groups = {}  # component -> {"Update": [...], "Issue Resolved": [...]}
    for r in selected:
        comp = friendly_component(r.get(COMPONENT_COL))
        kind = classify(note_text(r))
        bullet = restyle(note_text(r), kind)
        groups.setdefault(comp, {"Update": [], "Issue Resolved": []})[kind].append(bullet)

    lines = [
        "---",
        f'title: "{TITLE}"',
        f'excerpt: "{EXCERPT}"',
        "---",
        "",
        f"## {fmt_date(release_date)} Release",
        "",
    ]
    for comp in sorted(groups):
        lines.append(f"### {comp}")
        lines.append("")
        for label, key in (("Updates", "Update"), ("Issues Resolved", "Issue Resolved")):
            bullets = sorted(set(groups[comp][key]), key=str.lower)
            if not bullets:
                continue
            lines.append(f"**{label}:**")
            lines.append("")
            for b in bullets:
                lines.append(f"- {b}")
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
    rows = filter_publishable(rows)
    log(f"{len(rows)} rows at score >= {MIN_SCORE} with a note.")
    rows = dedup(rows)
    log(f"{len(rows)} unique notes after dedup.")

    ledger = load_ledger()
    selected = select_week(rows, ledger, run_date)
    log(f"{len(selected)} notes selected for the current week "
        f"(run date {run_date.isoformat()}, {len(ledger)} already published).")

    if not selected:
        log("No new notes for this week — leaving the current article unchanged.")
        return 0

    release_date = max(parse_date(r) for r in selected)
    restyle = make_restyler(use_llm)
    content = render_article(selected, restyle, release_date)

    if dry_run:
        log("--- DRY RUN (nothing written: no archive, no ledger update) ---")
        print(content)
        return len(selected)

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
