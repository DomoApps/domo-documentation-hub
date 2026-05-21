#!/usr/bin/env python3
"""
Pull current task state + attachments from Asana for items in
scripts/backlog_manifest.json that need them.

Reads $ASANA_TOKEN from the environment, falling back to .env.local at the
repo root (a single ASANA_TOKEN=... line; never committed — already in
.gitignore via .env.*).

For each manifest record that needs Asana data, fetches:
  • Task state — if `completed=true`, marks the record's `disposition` as
    "completed in asana" so the execution phase will skip it.
  • Attachments — Asana-hosted files are downloaded into
    .asana-cache/{task_id}/{filename}; externally-hosted attachments
    (SharePoint, Google Drive, etc.) are recorded as URL-only so you can
    fetch them manually.

Targets:
  • Bucket C / E — items already flagged attachment_hint=true.
  • Bucket M — substantive-but-unparseable notes; an attachment may rescue
    these and let us re-bucket.

Output:
  • Updates scripts/backlog_manifest.json in place.
  • Writes scripts/reports/asana_fetch_report.md — summary of what was
    pulled, what's still missing, and a checklist of attachments you need
    to feed manually (e.g. SharePoint Word docs).

Usage:
    python scripts/fetch_asana.py            # process all targets
    python scripts/fetch_asana.py --task-id 1212852269509381   # one task
    python scripts/fetch_asana.py --dry-run  # report what would be fetched
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "scripts" / "backlog_manifest.json"
CACHE_DIR = REPO_ROOT / ".asana-cache"
REPORT_DIR = REPO_ROOT / "scripts" / "reports"
ENV_FILE = REPO_ROOT / ".env.local"

ASANA_BASE = "https://app.asana.com/api/1.0"
SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")


def load_env(env_file: Path) -> None:
    """Minimal .env.local reader. Sets os.environ entries that aren't already set."""
    if not env_file.exists():
        return
    for raw in env_file.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def asana_get(path: str, token: str, params: dict | None = None) -> dict:
    url = ASANA_BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def download(url: str, dest: Path) -> None:
    """Stream a (possibly large) URL to dest. Skips if dest exists."""
    if dest.exists() and dest.stat().st_size > 0:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as resp, dest.open("wb") as f:
        while chunk := resp.read(64 * 1024):
            f.write(chunk)


def safe_filename(name: str) -> str:
    return SAFE_NAME.sub("_", name).strip("._") or "attachment"


def needs_fetch(rec: dict) -> bool:
    """Buckets C/E (attachment_hint=true) and M (manual review, might be rescued)."""
    if rec.get("disposition"):
        return False
    return rec["bucket"] in {"C", "E", "M"} or rec.get("attachment_hint")


def process_task(rec: dict, token: str, dry_run: bool) -> dict:
    """Returns a per-task report dict."""
    task_id = rec["task_id"]
    report = {
        "task_id": task_id,
        "name": rec["name"],
        "bucket": rec["bucket"],
        "asana_completed": None,
        "attachments_downloaded": [],
        "attachments_external": [],
        "errors": [],
    }

    if not task_id:
        report["errors"].append("no task_id in record")
        return report

    # 1) Task state — is it already done in Asana?
    try:
        task = asana_get(f"/tasks/{task_id}", token,
                         params={"opt_fields": "completed,name"})["data"]
    except urllib.error.HTTPError as e:
        report["errors"].append(f"task lookup HTTP {e.code}")
        return report
    except Exception as e:
        report["errors"].append(f"task lookup: {e!r}")
        return report

    report["asana_completed"] = bool(task.get("completed"))
    if task.get("completed"):
        if not dry_run:
            rec["disposition"] = "completed in asana (closed since CSV export)"
        return report

    # 2) Attachments list.
    try:
        attachments_resp = asana_get(f"/tasks/{task_id}/attachments", token,
                                     params={"opt_fields": "name,host,resource_subtype,download_url,permanent_url,view_url"})
        attachments = attachments_resp.get("data", [])
    except Exception as e:
        report["errors"].append(f"attachments list: {e!r}")
        return report

    if not attachments:
        return report

    # 3) Fetch each attachment.
    task_cache = CACHE_DIR / task_id
    for att in attachments:
        att_id = att["gid"]
        try:
            full = asana_get(f"/attachments/{att_id}", token,
                             params={"opt_fields": "name,host,download_url,permanent_url,view_url"})["data"]
        except Exception as e:
            report["errors"].append(f"attachment {att_id}: {e!r}")
            continue

        name = full.get("name") or f"attachment-{att_id}"
        host = (full.get("host") or "").lower()
        download_url = full.get("download_url")
        external_url = full.get("permanent_url") or full.get("view_url")

        # Asana-hosted (host=='asana') has a signed download_url we can fetch.
        # External (gdrive/onedrive/sharepoint/dropbox/box/vimeo etc.) only
        # gives us a link the user has to open in a browser.
        if host == "asana" and download_url:
            local = task_cache / safe_filename(name)
            entry = {
                "attachment_id": att_id,
                "name": name,
                "host": host,
                "local_path": str(local.relative_to(REPO_ROOT)),
            }
            if not dry_run:
                try:
                    download(download_url, local)
                except Exception as e:
                    report["errors"].append(f"download {name}: {e!r}")
                    continue
            report["attachments_downloaded"].append(entry)
        else:
            entry = {
                "attachment_id": att_id,
                "name": name,
                "host": host,
                "external_url": external_url,
            }
            report["attachments_external"].append(entry)

    # 4) Stamp the record.
    if not dry_run:
        rec["attachments"] = (
            report["attachments_downloaded"] + report["attachments_external"]
        )

    return report


def rebucket_after_fetch(rec: dict, report: dict) -> str | None:
    """If a bucket M item now has downloaded attachments, try to rescue it.
    Returns a one-line explanation if anything changed."""
    if rec["bucket"] != "M":
        return None
    if not report["attachments_downloaded"]:
        return None
    # We have file(s) but still no parseable structure. Promote to a
    # "review with attachment" sub-status of M. The execution phase will
    # treat M-with-attachments differently from M alone.
    rec.setdefault("_rebucket_note", "M but has Asana-hosted attachments — likely actionable")
    return f"{rec['task_id']}: M + {len(report['attachments_downloaded'])} attachment(s) → flagged actionable"


def write_report(reports: list[dict], rebucket_notes: list[str]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / "asana_fetch_report.md"

    completed = [r for r in reports if r["asana_completed"]]
    downloaded = [r for r in reports if r["attachments_downloaded"]]
    external_only = [r for r in reports
                     if r["attachments_external"] and not r["attachments_downloaded"]]
    errors = [r for r in reports if r["errors"]]
    empty = [r for r in reports
             if not r["asana_completed"]
             and not r["attachments_downloaded"]
             and not r["attachments_external"]
             and not r["errors"]]

    lines: list[str] = ["# Asana fetch report", ""]
    lines.append(f"Processed {len(reports)} tasks.")
    lines.append("")
    lines.append(f"- Already completed in Asana (auto-dispositioned): **{len(completed)}**")
    lines.append(f"- Attachments downloaded to `.asana-cache/`: **{len(downloaded)}**")
    lines.append(f"- Only external-host attachments (needs your manual download): **{len(external_only)}**")
    lines.append(f"- No attachments and not closed (needs manual brief): **{len(empty)}**")
    lines.append(f"- Errors: **{len(errors)}**")
    lines.append("")

    if rebucket_notes:
        lines.append("## Rebucketed during fetch")
        for n in rebucket_notes:
            lines.append(f"- {n}")
        lines.append("")

    if external_only:
        lines.append("## ⚠️ External attachments — please download these manually")
        lines.append("")
        lines.append("These tasks reference files hosted outside Asana (SharePoint, Google Drive, etc.).")
        lines.append("Save them under `.asana-cache/{task_id}/` so the execution phase can find them.")
        lines.append("")
        for r in external_only:
            lines.append(f"### {r['name']}")
            lines.append(f"- Task: https://app.asana.com/0/0/{r['task_id']}/f")
            lines.append(f"- Drop files into: `.asana-cache/{r['task_id']}/`")
            for a in r["attachments_external"]:
                lines.append(f"  - **{a['name']}** ({a['host']}) → {a.get('external_url') or 'no URL'}")
            lines.append("")

    if empty:
        lines.append("## Needs a brief — no Asana attachment and notes were unparseable")
        lines.append("")
        lines.append("These items have substantive notes but no recoverable attachment. ")
        lines.append("You'll need to feed me the source material (docx, screenshots, etc.) by hand. ")
        lines.append("Drop into `.asana-cache/{task_id}/` and re-run `fetch_asana.py` to re-index.")
        lines.append("")
        for r in empty:
            lines.append(f"- **{r['name']}** — `.asana-cache/{r['task_id']}/` ([task]({f'https://app.asana.com/0/0/{r["task_id"]}/f'}))")
        lines.append("")

    if errors:
        lines.append("## Errors")
        lines.append("")
        for r in errors:
            lines.append(f"- **{r['name']}** ({r['task_id']}): {'; '.join(r['errors'])}")
        lines.append("")

    out.write_text("\n".join(lines))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, default=MANIFEST)
    ap.add_argument("--task-id", help="process a single task_id and exit")
    ap.add_argument("--dry-run", action="store_true",
                    help="don't write anything; just report what would happen")
    ap.add_argument("--sleep", type=float, default=0.2,
                    help="seconds between tasks (rate-limit cushion)")
    args = ap.parse_args()

    load_env(ENV_FILE)
    token = os.environ.get("ASANA_TOKEN")
    if not token:
        print(f"ASANA_TOKEN not set. Put it in {ENV_FILE.relative_to(REPO_ROOT)} "
              f"as a line: ASANA_TOKEN=...", file=sys.stderr)
        return 1

    if not args.manifest.exists():
        print(f"Manifest not found: {args.manifest}. Run triage_backlog.py first.",
              file=sys.stderr)
        return 1

    manifest = json.loads(args.manifest.read_text())
    if args.task_id:
        targets = [r for r in manifest if r["task_id"] == args.task_id]
        if not targets:
            print(f"No record with task_id={args.task_id}", file=sys.stderr)
            return 1
    else:
        targets = [r for r in manifest if needs_fetch(r)]

    print(f"Fetching Asana data for {len(targets)} tasks "
          f"({'dry-run' if args.dry_run else 'live'})...")

    reports: list[dict] = []
    rebucket_notes: list[str] = []
    for i, rec in enumerate(targets, 1):
        print(f"  [{i:3d}/{len(targets)}] {rec['name'][:60]}")
        r = process_task(rec, token, dry_run=args.dry_run)
        reports.append(r)
        note = rebucket_after_fetch(rec, r)
        if note:
            rebucket_notes.append(note)
        if args.sleep:
            time.sleep(args.sleep)

    if not args.dry_run:
        args.manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
        print(f"Updated {args.manifest.relative_to(REPO_ROOT)}")

    report_path = write_report(reports, rebucket_notes)
    print(f"Report → {report_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
