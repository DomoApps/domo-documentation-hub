#!/usr/bin/env python3
"""One-off: close the 37 Bucket A meta/tracker/audit Asana tickets.

Per Jared 2026-05-27: aggressive batch close with a uniform comment.
Tickets were triaged as tracker/audit/empty-notes parents rather than
concrete article-edit requests. Submitters can re-open or re-file if a
specific edit was missed.

For each task:
  1. POST /tasks/{gid}/stories with the uniform resolution comment.
  2. PUT  /tasks/{gid} with {data: {completed: true}}.

Appends results to scripts/reports/asana_close_results.json and
updates the manifest disposition for each task.
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

UNIFORM_COMMENT = (
    "Closing as part of the Asana backlog cleanup on docs branch "
    "`update/asanaBacklog`. This ticket was triaged as a "
    "tracker/audit/meta parent (or had empty notes) rather than a "
    "concrete single-article edit request, so no specific repo change "
    "is pending. If a particular edit was intended, please re-open or "
    "re-file as a discrete ticket with a target article URL."
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

    targets = [r for r in iter_records if r.get("bucket") == "A" and not r.get("disposition")]
    print(f"Closing {len(targets)} Bucket A tickets …\n")

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
        "won't do: bucket A tracker/audit/empty-notes parent; no concrete "
        "single-article edit pending. Closed in Asana on 2026-05-27 with "
        "uniform comment inviting re-submission for any specific edit "
        "that was intended."
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
