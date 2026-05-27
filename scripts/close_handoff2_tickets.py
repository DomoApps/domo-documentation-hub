#!/usr/bin/env python3
"""One-off: close the 3 HANDOFF-2 unaccounted Asana tickets.

For each task:
  1. POST /tasks/{gid}/stories with a one-sentence resolution comment.
  2. PUT  /tasks/{gid} with {data: {completed: true}}.

Appends results to scripts/reports/asana_close_results.json.
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

PLAN = [
    {
        "task_id": "1208693640056137",
        "name": "PUBLISH Migrate from Federated to Cloud Amplifier",
        "comment": (
            "Already shipped — article lives at s/article/000005675.mdx "
            "(EN) and ja/s/article/000005675.mdx (JA) on docs branch "
            "`update/asanaBacklog` (pending merge to `main`). Title: "
            "\"Migrate from Federated to Cloud Integrations\". Covers "
            "migrate + revert steps. Closing as complete."
        ),
    },
    {
        "task_id": "1205295264301383",
        "name": "Missing required role - Achievements",
        "comment": (
            "Closing as obsolete: the two target articles (360042934434 "
            "and 000005149) were retired during the SF→Mintlify migration "
            "and the role-description snippets the request would amend no "
            "longer exist in the docs. If a current article needs this "
            "role-grant clarification, please re-submit pointing at the "
            "live KB URL."
        ),
    },
    {
        "task_id": "1208496418472569",
        "name": "Update Group Ownership of accounts",
        "comment": (
            "Closing as obsolete: target article 4403537355543 was "
            "retired during the SF→Mintlify migration and the "
            "\"Manage all accounts\" grant string does not appear in any "
            "current article, so there is no surviving FAQ home for this "
            "request. If a current article needs this FAQ, please "
            "re-submit pointing at the live KB URL."
        ),
    },
]


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

    existing = []
    if RESULTS.exists():
        existing = json.loads(RESULTS.read_text())

    new_results = []
    for item in PLAN:
        gid = item["task_id"]
        try:
            story = asana_post(
                f"/tasks/{gid}/stories",
                token,
                {"data": {"text": item["comment"]}},
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
                "name": item["name"],
                "ok": True,
                "story_gid": story_gid,
                "completed_at": completed_at,
            }
            print(f"  ✓ {gid} {item['name'][:50]} → closed at {completed_at}")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            result = {
                "task_id": gid,
                "name": item["name"],
                "ok": False,
                "error": f"HTTP {e.code}: {body[:300]}",
            }
            print(f"  ✗ {gid} {item['name'][:50]} → {result['error']}")
        new_results.append(result)

    RESULTS.write_text(json.dumps(existing + new_results, indent=2) + "\n")
    print(f"\nWrote {len(new_results)} new entries to {RESULTS.relative_to(REPO_ROOT)}")
    return 0 if all(r["ok"] for r in new_results) else 2


if __name__ == "__main__":
    sys.exit(main())
