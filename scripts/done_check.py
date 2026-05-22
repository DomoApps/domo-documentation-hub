#!/usr/bin/env python3
"""
Done-check, Tier 1: for each manifest item whose article(s) exist in the
repo, look at git history since the migration commit (fa0541ee, 2026-01-09).

  • No post-migration commits to any of the item's articles → the change
    cannot have been applied; mark done_check.git_status = "untouched"
    and skip Tier 2.
  • At least one post-migration commit → mark "edited" and surface the
    record on a candidate queue for Tier 2 (an LLM content comparison
    that Claude Code runs from the conversation, not from this script).

Outputs:
  • scripts/backlog_manifest.json — updated in place. Each processed
    record gets a `done_check` object:
        {
          "git_status": "untouched" | "edited" | "skipped",
          "checked_at": ISO8601 UTC,
          "articles": [
              {"path": "...", "commits": [{"sha", "date", "subject"}, ...]},
              ...
          ],
          "content_check": null | "pending" | "applied" | "partially" | "not_applied",
          "content_check_reasoning": null | "..."
        }
  • scripts/reports/done_check_candidates.json — slim list of records that
    need Tier 2 (Claude Code consumes this to fan out sub-agents).
  • scripts/reports/done_check_report.md — human-readable summary.

Usage:
    python scripts/done_check.py
    python scripts/done_check.py --since fa0541ee     # override boundary
    python scripts/done_check.py --task-id 1212...    # one task
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "scripts" / "backlog_manifest.json"
REPORT_DIR = REPO_ROOT / "scripts" / "reports"
DEFAULT_SINCE = "fa0541ee"  # initial migration commit, 2026-01-09


def git_log_since(path: str, since: str) -> list[dict]:
    """Return commits touching `path` since `since` (exclusive of `since` itself)."""
    try:
        out = subprocess.check_output(
            ["git", "log", f"{since}..HEAD", "--format=%H%x1f%ad%x1f%s",
             "--date=short", "--", path],
            cwd=REPO_ROOT, text=True, stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        print(f"git log failed for {path}: {e.stderr.strip()}", file=sys.stderr)
        return []
    commits = []
    for line in out.strip().splitlines():
        if not line:
            continue
        sha, date, subject = line.split("\x1f", 2)
        commits.append({"sha": sha[:8], "date": date, "subject": subject})
    return commits


def should_check(rec: dict) -> bool:
    """Process bucket B and C records — those reference an existing article
    that we're meant to update. Skip already-dispositioned, net-new, meta,
    or unparseable records."""
    if rec.get("disposition"):
        return False
    if rec["bucket"] not in {"B", "C"}:
        return False
    return any(a.get("resolved_path") for a in rec["articles"])


def process_record(rec: dict, since: str) -> dict:
    article_results = []
    has_any_commits = False
    for a in rec["articles"]:
        path = a.get("resolved_path")
        if not path:
            continue
        commits = git_log_since(path, since)
        if commits:
            has_any_commits = True
        article_results.append({"path": path, "commits": commits})

    return {
        "git_status": "edited" if has_any_commits else "untouched",
        "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "since": since,
        "articles": article_results,
        "content_check": "pending" if has_any_commits else None,
        "content_check_reasoning": None,
    }


def build_candidates(manifest: list[dict]) -> list[dict]:
    """Slim record shape for the Tier 2 dispatcher (Claude Code in conversation)."""
    out = []
    for rec in manifest:
        dc = rec.get("done_check")
        if not dc or dc.get("git_status") != "edited":
            continue
        if dc.get("content_check") not in (None, "pending"):
            # Already content-checked; don't re-queue.
            continue
        out.append({
            "task_id": rec["task_id"],
            "name": rec["name"],
            "bucket": rec["bucket"],
            "asana_url": rec["asana_url"],
            "description": rec["description"],
            "articles": [
                {
                    "path": a["path"],
                    "post_migration_commits": a["commits"],
                }
                for a in dc["articles"]
            ],
            "attachment_paths": [
                att.get("local_path") for att in rec.get("attachments", [])
                if att.get("local_path")
            ],
        })
    return out


def write_report(manifest: list[dict], candidates: list[dict]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / "done_check_report.md"

    processed = [r for r in manifest if r.get("done_check")]
    untouched = [r for r in processed if r["done_check"]["git_status"] == "untouched"]
    edited = [r for r in processed if r["done_check"]["git_status"] == "edited"]
    skipped = [r for r in manifest if not r.get("done_check") and not r.get("disposition")]
    dispositioned = [r for r in manifest if r.get("disposition")]

    lines: list[str] = [
        "# Done-check report (Tier 1: git log)",
        "",
        f"Migration boundary: `{DEFAULT_SINCE}` (initial migration, 2026-01-09)",
        "",
        f"- Records processed: **{len(processed)}**",
        f"- `untouched` since migration (assume work not done): **{len(untouched)}**",
        f"- `edited` since migration (queued for Tier 2): **{len(edited)}**",
        f"- Skipped (not bucket B/C, no resolved path, etc.): **{len(skipped)}**",
        f"- Already dispositioned (obsolete / completed in Asana): **{len(dispositioned)}**",
        "",
        "## Tier 2 candidates",
        "",
        f"Saved to `scripts/reports/done_check_candidates.json` "
        f"({len(candidates)} items). Claude Code will fan these out to "
        "sub-agents that read the current article and the requested "
        "change, then judge applied/partially/not_applied.",
        "",
    ]
    if edited:
        lines.append("### Edited articles by task")
        lines.append("")
        for r in edited:
            paths = ", ".join(a["path"] for a in r["done_check"]["articles"] if a["commits"])
            commit_count = sum(len(a["commits"]) for a in r["done_check"]["articles"])
            lines.append(f"- **{r['name']}** — {commit_count} commit(s) — {paths}")
        lines.append("")
    out.write_text("\n".join(lines))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, default=MANIFEST)
    ap.add_argument("--since", default=DEFAULT_SINCE,
                    help="git ref to bound history against (default: migration commit)")
    ap.add_argument("--task-id", help="process a single task and exit")
    ap.add_argument("--force", action="store_true",
                    help="re-run git check even if done_check is already set")
    args = ap.parse_args()

    if not args.manifest.exists():
        print(f"Manifest not found: {args.manifest}", file=sys.stderr)
        return 1

    manifest = json.loads(args.manifest.read_text())

    if args.task_id:
        targets = [r for r in manifest if r["task_id"] == args.task_id]
    else:
        targets = [r for r in manifest if should_check(r)]
        if not args.force:
            targets = [r for r in targets if not r.get("done_check")]

    print(f"Tier 1 done-check against `{args.since}` for {len(targets)} records...")

    for i, rec in enumerate(targets, 1):
        rec["done_check"] = process_record(rec, args.since)
        status = rec["done_check"]["git_status"]
        commit_total = sum(len(a["commits"]) for a in rec["done_check"]["articles"])
        print(f"  [{i:3d}/{len(targets)}] {status:9s} ({commit_total} commits) — {rec['name'][:55]}")

    args.manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    candidates = build_candidates(manifest)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "done_check_candidates.json").write_text(
        json.dumps(candidates, indent=2, ensure_ascii=False)
    )
    report = write_report(manifest, candidates)

    print(f"\nUpdated {args.manifest.relative_to(REPO_ROOT)}")
    print(f"Candidates → scripts/reports/done_check_candidates.json ({len(candidates)} items)")
    print(f"Report     → {report.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
