#!/usr/bin/env python3
"""Close a single Asana KB-tracker ticket with a custom comment.

Usage:
    python3 scripts/close_ticket.py <task_id> "resolution comment"

Posts the comment as a story, then marks the task complete, and appends
the result to scripts/reports/asana_close_results.json. Reuses the SSL +
env-loading helpers from fetch_asana.py.
"""
from __future__ import annotations
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from fetch_asana import SSL_CTX, load_env, ASANA_BASE  # type: ignore

ENV_FILE = REPO_ROOT / ".env.local"
RESULTS = REPO_ROOT / "scripts" / "reports" / "asana_close_results.json"


def _req(path: str, token: str, body: dict, method: str) -> dict:
    req = urllib.request.Request(
        ASANA_BASE + path,
        data=json.dumps(body).encode(),
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
        return json.loads(resp.read())


def close_ticket(gid: str, comment: str, token: str) -> dict:
    story = _req(f"/tasks/{gid}/stories", token, {"data": {"text": comment}}, "POST")
    completion = _req(f"/tasks/{gid}", token, {"data": {"completed": True}}, "PUT")
    return {
        "task_id": gid,
        "ok": True,
        "story_gid": story.get("data", {}).get("gid"),
        "completed_at": completion.get("data", {}).get("completed_at"),
        "comment": comment,
    }


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 1
    gid, comment = sys.argv[1], sys.argv[2]
    load_env(ENV_FILE)
    token = os.environ.get("ASANA_TOKEN")
    if not token:
        print("error: ASANA_TOKEN not set", file=sys.stderr)
        return 1
    try:
        result = close_ticket(gid, comment, token)
    except urllib.error.HTTPError as e:
        print(f"✗ {gid} → HTTP {e.code}: {e.read().decode('utf-8','replace')[:300]}", file=sys.stderr)
        return 2
    existing = json.loads(RESULTS.read_text()) if RESULTS.exists() else []
    existing.append(result)
    RESULTS.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n")
    print(f"✓ closed {gid} at {result['completed_at']} (story {result['story_gid']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
