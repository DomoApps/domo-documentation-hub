#!/usr/bin/env python3
"""One-off: close 8 of 11 Bucket M tickets (all title-only, zero body).

Per Jared 2026-05-27: keep 3 open (Analyzer Overview, Beast Mode
Overview, DomoStats project with Dan) for live triage; batch-close the
other 8.

For each task:
  1. POST /tasks/{gid}/stories with the uniform resolution comment.
  2. PUT  /tasks/{gid} with {data: {completed: true}}.

Appends results to scripts/reports/asana_close_results.json and
updates the manifest disposition for each task closed.
"""
from __future__ import annotations
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from fetch_asana import SSL_CTX, load_env, ASANA_BASE  # type: ignore

ENV_FILE = REPO_ROOT / ".env.local"
MANIFEST = REPO_ROOT / "scripts" / "backlog_manifest.json"
RESULTS = REPO_ROOT / "scripts" / "reports" / "asana_close_results.json"

KEEP_OPEN = {
    "1205980130684558",  # Analyzer Overview
    "1209622077811472",  # Beast Mode Overview
    "1209815237834256",  # DomoStats project with Dan
}

UNIFORM_COMMENT = (
    "Closing as part of the Asana backlog cleanup on docs branch "
    "`update/asanaBacklog`. This ticket was submitted as a title only "
    "with no description body, so no actionable request can be "
    "reconstructed. If the work is still needed, please re-file with a "
    "target article URL (or new-article scope) and a concrete "
    "description of what should change."
)


def asana_post(path: str, token: str, body: dict) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        ASANA_BASE + path,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
        return json.loads(resp.read())


def asana_put(path: str, token: str, body: dict) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        ASANA_BASE + path,
        data=data,
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
        return json.loads(resp.read())


def main() -> int:
    load_env(ENV_FILE)
    token = os.environ.get("ASANA_TOKEN")
    if not token:
        print("error: ASANA_TOKEN not set", file=sys.stderr)
        return 1

    data = json.loads(MANIFEST.read_text())
    records = data if isinstance(data, list) else data.get("tasks", data)
    iter_records = records if isinstance(records, list) else list(records.values())

    targets = [
        r for r in iter_records
        if r.get("bucket") == "M"
        and not r.get("disposition")
        and r.get("task_id") not in KEEP_OPEN
    ]
    print(f"Closing {len(targets)} Bucket M tickets "
          f"(keeping {len(KEEP_OPEN)} open) …\n")

    existing = json.loads(RESULTS.read_text()) if RESULTS.exists() else []
    new_results = []
    closed_ids: set[str] = set()

    for r in targets:
        gid = r["task_id"]
        name = r.get("name", "")
        try:
            story = asana_post(
                f"/tasks/{gid}/stories",
                token,
                {"data": {"text": UNIFORM_COMMENT}},
            )
            story_gid = story.get("data", {}).get("gid")

            completion = asana_put(
                f"/tasks/{gid}",
                token,
                {"data": {"completed": True}},
            )
            completed_at = completion.get("data", {}).get("completed_at")

            result = {
                "task_id": gid,
                "name": name,
                "ok": True,
                "story_gid": story_gid,
                "completed_at": completed_at,
            }
            closed_ids.add(gid)
            print(f"  ✓ {gid}  {name[:55]}")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            result = {
                "task_id": gid,
                "name": name,
                "ok": False,
                "error": f"HTTP {e.code}: {body[:300]}",
            }
            print(f"  ✗ {gid}  {name[:55]} → {result['error']}")
        new_results.append(result)
        time.sleep(0.3)

    RESULTS.write_text(json.dumps(existing + new_results, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {len(new_results)} new entries to {RESULTS.relative_to(REPO_ROOT)}")

    disp = (
        "won't do: bucket M title-only submission with no description "
        "body. Closed in Asana on 2026-05-27 with uniform comment "
        "inviting re-submission with a target article URL and a "
        "concrete description."
    )
    changed = 0
    for r in iter_records:
        if r.get("task_id") in closed_ids:
            r["disposition"] = disp
            changed += 1
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"Updated manifest disposition on {changed} records.")

    return 0 if all(r["ok"] for r in new_results) else 2


if __name__ == "__main__":
    sys.exit(main())
