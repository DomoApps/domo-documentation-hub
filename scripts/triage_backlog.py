#!/usr/bin/env python3
"""
Triage KB_Content_Tracker.csv → scripts/backlog_manifest.json

Parses the Asana CSV export, filters to actionable sections, parses each
task's notes into structured fields, and emits a manifest JSON consumed
by downstream scripts (fetch_asana.py, done_check.py) and agent batches.

Idempotent: re-running preserves any fields downstream scripts have set
(e.g., attachment_paths, done_check) by merging with the existing manifest.

Usage:
    python scripts/triage_backlog.py
    python scripts/triage_backlog.py --csv KB_Content_Tracker.csv --out scripts/backlog_manifest.json
    python scripts/triage_backlog.py --summary    # print bucket counts + samples and exit
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = REPO_ROOT / "KB_Content_Tracker.csv"
DEFAULT_OUT = REPO_ROOT / "scripts" / "backlog_manifest.json"

ACTIONABLE_SECTIONS = {
    "Backlog — Non-Release",
    "Backlog — Release Content",
    "L10N In Progress",
    "G&A Backlog",
    "Project planning",
    "On Hold/Blocked",
}

# Sections that are tracking buckets, not article work — auto-skip unless
# the notes clearly describe a single concrete update.
META_SECTIONS = {"Project planning"}

ATTACHMENT_KEYWORDS = re.compile(
    r"\b(attached|attachment|\.docx?|\.pdf|see screenshot|screenshots?|"
    r"word file|word doc|draft (file|attached)|see (the )?(image|file))\b",
    re.IGNORECASE,
)

ARTICLE_URL_RE = re.compile(
    r"(?:"
    r"domo-support\.domo\.com/(?P<ja>minasan/)?s/article/(?P<id>[A-Za-z0-9]+)"
    r"|domohelp\.domo\.com/hc/[^/\s]+/articles/(?P<id_dh>\d+)"
    r")"
)

# Form field extractors. Asana exports notes as plain text with the question
# label on one line and the answer on the next (or several next) lines.
FIELD_RES = {
    "submitter": re.compile(
        r"(?:Submitter's )?[Ee]mail address:\s*\n([^\n]+)"
    ),
    "ja_request": re.compile(
        r"Is this in response to a Japanese customer request\?:\s*\n([^\n]+)"
    ),
    "doc_contact": re.compile(
        r"Who is the doc contact[^\n:]*:\s*\n([^\n]+)"
    ),
    "update_type_raw": re.compile(
        r"Is this net new content or updates to existing content\?:\s*\n([^\n]+)"
    ),
    "release_status": re.compile(
        r"If release related, is this content for beta or GA release\?:\s*\n([^\n]+)"
    ),
    "priority": re.compile(
        r"Requested Priority Level:\s*\n([^\n]+)"
    ),
    "needed_by": re.compile(
        r"Content is needed by[^\n:]*:\s*\n([^\n]+)"
    ),
}

# The "detailed explanation" field is multi-paragraph — capture until the
# next known form header or the trailing form footer.
DESCRIPTION_RE = re.compile(
    r"Provide a detailed explanation of what needs to be created/updated:\s*\n"
    r"(?P<body>.*?)"
    r"(?=\n(?:Please include the URL|Juliana and Jared|Requested Priority|"
    r"Content is needed|Who will need to approve|—————|This task was submitted|$))",
    re.DOTALL,
)


def build_article_index() -> dict[str, str]:
    """Map article ID → relative repo path for both EN and JA."""
    index: dict[str, str] = {}
    for sub in ("s/article", "ja/s/article"):
        d = REPO_ROOT / sub
        if not d.exists():
            continue
        for p in d.glob("*.mdx"):
            stem = p.stem
            # Key by both the literal stem (for slug-named files) and bare
            # numeric form. We treat (lang, id) as composite via prefix.
            prefix = "ja:" if sub.startswith("ja/") else "en:"
            index[prefix + stem] = str(p.relative_to(REPO_ROOT))
    return index


def first(pattern: re.Pattern[str], text: str) -> str | None:
    m = pattern.search(text)
    return m.group(1).strip() if m else None


def classify_update_type(raw: str | None) -> str:
    if not raw:
        return "unknown"
    v = raw.lower()
    if "net new" in v:
        return "net_new"
    if "update" in v:
        return "update"
    return "unknown"


def extract_description(notes: str) -> str | None:
    m = DESCRIPTION_RE.search(notes)
    if not m:
        return None
    body = m.group("body").strip()
    return body or None


def resolve_articles(notes: str, index: dict[str, str]) -> tuple[list[dict], bool]:
    """Return (article_records, has_any_url). Each record has id, is_ja, resolved_path."""
    seen = set()
    records: list[dict] = []
    for m in ARTICLE_URL_RE.finditer(notes):
        aid = m.group("id") or m.group("id_dh")
        is_ja = bool(m.group("ja"))
        if not aid:
            continue
        key = (aid, is_ja)
        if key in seen:
            continue
        seen.add(key)
        prefix = "ja:" if is_ja else "en:"
        records.append({
            "id": aid,
            "is_ja": is_ja,
            "resolved_path": index.get(prefix + aid),
        })
    return records, bool(records)


def is_meta_task(name: str, notes: str, section: str) -> bool:
    if section in META_SECTIONS:
        return True
    if not notes.strip():
        return True
    lower_name = name.lower()
    meta_signals = ("audit", "drafts to save", "checklist template", "style guide")
    return any(s in lower_name for s in meta_signals) and not DESCRIPTION_RE.search(notes)


def assign_bucket(*, update_type: str, attachment_hint: bool,
                  articles: list[dict], has_url: bool, is_meta: bool,
                  has_substantive_notes: bool) -> str:
    """
    A = skip (meta or empty notes)
    B = update, self-contained
    C = update, needs attachment
    D = net-new, self-contained
    E = net-new, needs attachment
    F = update but referenced article not found in repo
    M = manual review — non-empty notes but no parseable form structure
    """
    if is_meta:
        return "A"
    if update_type == "update":
        if has_url and not any(a["resolved_path"] for a in articles):
            return "F"
        return "C" if attachment_hint else "B"
    if update_type == "net_new":
        return "E" if attachment_hint else "D"
    # update_type == "unknown"
    if has_substantive_notes:
        return "M"
    return "A"


def parse_row(row: dict, index: dict[str, str]) -> dict | None:
    section = row.get("Section/Column", "").strip()
    if section not in ACTIONABLE_SECTIONS:
        return None

    # The Task ID column has a BOM in the export.
    task_id = (row.get("﻿Task ID") or row.get("Task ID") or "").strip()
    name = row.get("Name", "").strip()
    notes = row.get("Notes", "") or ""

    fields = {k: first(p, notes) for k, p in FIELD_RES.items()}
    update_type = classify_update_type(fields["update_type_raw"])
    description = extract_description(notes)
    articles, has_url = resolve_articles(notes, index)
    attachment_hint = bool(ATTACHMENT_KEYWORDS.search(notes))
    meta = is_meta_task(name, notes, section)
    # Substantive = enough free-text to plausibly describe a task, not just
    # a placeholder line. 80 chars filters out things like a bare URL.
    body_only = re.sub(r"https?://\S+", "", notes).strip()
    has_substantive_notes = len(body_only) >= 80
    bucket = assign_bucket(
        update_type=update_type,
        attachment_hint=attachment_hint,
        articles=articles,
        has_url=has_url,
        is_meta=meta,
        has_substantive_notes=has_substantive_notes,
    )

    return {
        "task_id": task_id,
        "asana_url": f"https://app.asana.com/0/0/{task_id}/f" if task_id else None,
        "name": name,
        "section": section,
        "assignee": row.get("Assignee", "").strip() or None,
        "due_date": row.get("Due Date", "").strip() or None,
        "current_status": row.get("Current Status", "").strip() or None,
        "submitter": fields["submitter"],
        "doc_contact": fields["doc_contact"],
        "ja_request": (fields["ja_request"] or "").lower().startswith("y") if fields["ja_request"] else False,
        "update_type": update_type,
        "update_type_raw": fields["update_type_raw"],
        "release_status": fields["release_status"],
        "priority": fields["priority"],
        "needed_by": fields["needed_by"],
        "description": description,
        "articles": articles,
        "attachment_hint": attachment_hint,
        "is_meta": meta,
        "bucket": bucket,
        # Reserved for downstream scripts.
        "attachments": [],   # populated by fetch_asana.py
        "done_check": None,  # populated by done_check.py
        "execution": None,   # populated by execution phase
        "disposition": None, # user decisions: "obsolete", "skip", etc.
    }


def merge_with_existing(new_records: list[dict], out_path: Path) -> list[dict]:
    """Preserve downstream-script fields (attachments, done_check, execution)
    from any prior manifest on disk."""
    if not out_path.exists():
        return new_records
    try:
        existing = {r["task_id"]: r for r in json.loads(out_path.read_text())}
    except (json.JSONDecodeError, KeyError):
        return new_records
    for rec in new_records:
        prior = existing.get(rec["task_id"])
        if not prior:
            continue
        for preserved in ("attachments", "done_check", "execution", "disposition"):
            if prior.get(preserved):
                rec[preserved] = prior[preserved]
    return new_records


def print_summary(records: list[dict]) -> None:
    from collections import Counter
    by_bucket = Counter(r["bucket"] for r in records)
    bucket_labels = {
        "A": "Skip (meta or empty notes)",
        "B": "Update — self-contained",
        "C": "Update — needs attachment",
        "D": "Net-new — self-contained",
        "E": "Net-new — needs attachment",
        "F": "Update — referenced article missing",
        "M": "Manual review — unparseable notes",
    }
    print(f"\nTotal actionable tasks: {len(records)}\n")
    print("=== Bucket counts ===")
    for b in "ABCDEFM":
        print(f"  {b}  {by_bucket.get(b, 0):3d}   {bucket_labels[b]}")

    print("\n=== Sample per bucket (first 3) ===")
    for b in "BCDEFM":
        samples = [r for r in records if r["bucket"] == b][:3]
        if not samples:
            continue
        print(f"\n--- Bucket {b} ({bucket_labels[b]}) ---")
        for r in samples:
            paths = ", ".join(a["resolved_path"] or f"!{a['id']}" for a in r["articles"]) or "—"
            attach = " 📎" if r["attachment_hint"] else ""
            print(f"  • {r['name'][:55]:55s} | {paths}{attach}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--summary", action="store_true",
                    help="print bucket summary and skip writing manifest")
    args = ap.parse_args()

    if not args.csv.exists():
        print(f"CSV not found: {args.csv}", file=sys.stderr)
        return 1

    index = build_article_index()
    print(f"Indexed {len(index)} article files (EN + JA).")

    with args.csv.open(newline="") as f:
        reader = csv.DictReader(f)
        records = [r for row in reader if (r := parse_row(row, index))]

    records.sort(key=lambda r: (r["bucket"], r["section"], r["name"]))

    if args.summary:
        print_summary(records)
        return 0

    records = merge_with_existing(records, args.out)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(records, indent=2, ensure_ascii=False))
    print(f"Wrote {len(records)} records → {args.out.relative_to(REPO_ROOT)}")
    print_summary(records)
    return 0


if __name__ == "__main__":
    sys.exit(main())
