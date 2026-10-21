# Connector Review automation — status & re-enable checklist

**Status as of 2026-10-20 (PT) / 2026-10-21 UTC:** built and merged, but the daily
**schedule is intentionally DISABLED** pending a network fix. Manual dispatch still works.
This file is the single place to resume from once the network issue is resolved.

---

## What was built

A fully-automated daily connector review that replaces Jared's manual GitHub approval with
an automated **site-safety gate** (renderable MDX, docs.json integrity, no new broken links,
no case collisions, alt text on added images). Content approval is unchanged — it still comes
from the secondary approver in the Jira ticket. No fact-checking; code and rendering only.

Shipped in **PR #647** (merged to `main` 2026-10-21 00:31 UTC):

| File | Role |
|---|---|
| `.github/workflows/connector-review-daily.yml` | The Action. Installs the toolchain, runs the skill headless via `claude -p`. Schedule now commented out; `workflow_dispatch` (with a `dry_run` toggle) still active. |
| `scripts/connector-review-gate.py` | Deterministic site-safety gate for one PR branch. Exits 0 (pass) / 1 (fail → don't merge) / 2 (couldn't run). |
| `scripts/test-connector-review-gate.py` | No-framework tests for the gate (`python3 scripts/test-connector-review-gate.py`). |
| `.claude/skills/connector-review/SKILL.md` | New **"Automated Daily Review (CI)"** section; guardrails qualified — interactive runs still ask Jared, CI mode uses the gate. |
| `.claude/skills/connector-review/run-log.md` | Append-only run log; each run adds a dated "what it did and why" note, committed back to `main` and mirrored to a `connector-review-log` GitHub issue. |

A later commit on branch `jared.peterson/connector-review-auth-fix` added an **Anthropic API
key preflight probe** to the workflow (a `GET /v1/models` curl that prints the HTTP status at
the top of the run) — the fastest way to tell a key/network failure (401) from a working key
(200). Keep it; it's the first thing to read when verifying the fix.

## Secrets (all added to the repo)

- `JIRA_EMAIL` — Domo Atlassian account email (Jira Basic auth)
- `JIRA_API_TOKEN` — Jira API token
- `CONNECTOR_REVIEW_PAT` — admin GitHub PAT; `gh` acts as Jared and merges past the `main`
  ruleset via the Admin-role bypass
- `ANTHROPIC_API_KEY` — the headless Claude run (pre-existing)

## Why it's paused — the blocker

The first dry run (`workflow_dispatch`, `dry_run=true`) passed **every** setup step — checkout,
Yarn 4 install, Mintlify CLI, Claude Code CLI install, git config — and failed only at the
headless Claude step with:

```
Invalid API key · Fix external API key
```

This is an API auth failure reaching Anthropic from the GitHub-hosted `ubuntu-latest` runner.
The same `ANTHROPIC_API_KEY` works for the repo's Python-SDK path, and the cause is understood
to be a **network-authorization requirement** (the runner must call the API from an authorized
network). A fix is in progress with a dev team.

**Important:** the failure is safe. The run errors *before* taking any action — no merges, no
Jira comments, no pushes happen on failure.

## Re-enable checklist (do this once the network fix is in)

1. **Set the runner.** The fix most likely means running on a **self-hosted runner on the
   authorized network**. In `.github/workflows/connector-review-daily.yml`, change
   `runs-on: ubuntu-latest` to the authorized self-hosted runner label (confirm the label with
   the dev team). If the fix instead allowlists GitHub-hosted runners, leave `ubuntu-latest`.
2. **Manual dry run.** Dispatch with `dry_run` checked:
   `gh workflow run connector-review-daily.yml -f dry_run=true` (add `--ref <branch>` to test a
   branch first). Confirm the **preflight prints `HTTP 200`**. If it prints `401`, the key/network
   is still not right — stop and fix that before anything else.
3. **Verify the dry run.** The Claude step should run the dashboard + the gate on any candidates
   and print what it *would* do, with no merges/comments/pushes.
4. **One live run, watched.** Dispatch with `dry_run` unchecked and watch a real candidate end to
   end: branch checked out → style auto-fix pushed → gate pass → approve + merge → Jira comment +
   close → run-log entry + `connector-review-log` issue comment.
5. **Re-enable the schedule.** Uncomment the `schedule:`/`cron` lines in the workflow `on:` block
   (restores daily ~5:11am PST / 6:11am PDT). Because `main` is protected, land this via a PR and
   merge with admin privileges (`gh pr merge <n> --merge --admin`) or a normal approval.

## Pointers

- Full design & rationale: the approved plan and PR #647 description.
- Gate internals and the per-candidate automated flow: `SKILL.md` › **Automated Daily Review (CI)**.
- Diagnostic branch with the preflight probe: `jared.peterson/connector-review-auth-fix`.
