# Automated Workflows — Technical Contributor Guide

This document explains the repository's scheduled, PR-opening GitHub Actions for technical contributors. It is **not** writer-facing: non-technical KB authors never need to read or run anything here.

> **Note:** This is a `.md` file in `.github/workflows/`. GitHub Actions only loads `.yml`/`.yaml` files from this directory, so this doc is ignored by the Actions runner and exists purely as documentation alongside the workflows it describes.

The three workflows below share a common safe-by-default shape: they **regenerate content → push to a dedicated `auto/*` branch → open or update a reviewable PR**, and never publish directly to `main`. Nothing goes live until a human merges the PR. The Mermaid diagrams trace each workflow from its trigger through every decision point to its terminal states (including the quiet "nothing to do" exits).

These diagrams render natively on GitHub and in Mintlify (both support the ` ```mermaid ` fence).

---

## `sync-video-library.yml` — Sync Video Library

Rebuilds `s/article/Domo-Video-Library.mdx` and its thumbnails from a Domo DataSet, pushes to `auto/video-library`, and opens/updates a PR with a Mintlify preview.

- **Schedule:** Monday & Wednesday, 13:00 UTC (≈ 6–7am Mountain); also manual via `workflow_dispatch`.
- **Requires:** secret `DOMO_DEVELOPER_TOKEN`; variable `DOMO_VIDEO_DATASET_ID`; optional `DOMO_INSTANCE`, plus `MINTLIFY_KEY` / `MINTLIFY_PROJECT_ID` for the preview.

```mermaid
flowchart TD
    A([Trigger]) --> A1["schedule: Mon & Wed 13:00 UTC"]
    A --> A2["workflow_dispatch (manual)"]
    A1 --> B
    A2 --> B

    B["Checkout repo + set up Python 3.12"] --> C["Run build_video_library.py<br/>(rebuild Domo-Video-Library.mdx + thumbnails<br/>from the Domo DataSet)"]
    C --> D{"git status:<br/>changes in<br/>article or images/kb/?"}

    D -->|No| E([changed=false → stop])

    D -->|Yes| F["checkout -B auto/video-library<br/>commit + force-push"]
    F --> G{"Open PR for<br/>auto/video-library?"}
    G -->|Exists| H["Push refreshed the PR"]
    G -->|None| I["gh pr create → main"]
    H --> J
    I --> J

    J{"MINTLIFY_KEY &<br/>PROJECT_ID set?"}
    J -->|No| K([Warn, skip preview])
    J -->|Yes| L["POST Mintlify preview API"]
    L --> M{"HTTP 202?"}
    M -->|No| N([Warn, no preview URL])
    M -->|Yes| O["Sticky PR comment<br/>with preview URL"]
    O --> P([PR ready for review<br/>— merge to publish])
```

---

## `sync-minor-release-notes.yml` — Sync Minor Release Notes

Rebuilds `s/article/Current-Minor-Release-Notes.mdx` from the Domo hotfix enrichment DataSet (notes scored ≥ 7, not yet published, restyled into house voice via the Anthropic API), archives the outgoing week into a dated file + `docs.json` nav, pushes to `auto/minor-release-notes`, and opens/updates a PR. A one-time `seed_ledger` run bootstraps the published ledger without writing an article.

- **Schedule:** Friday, 13:17 UTC (≈ 6–7am Mountain, just before the release is cut); also manual via `workflow_dispatch` with a `seed_ledger` boolean input.
- **Requires:** secrets `DOMO_DEVELOPER_TOKEN`, `ANTHROPIC_API_KEY`; variable `DOMO_MINOR_RN_DATASET_ID`; optional `DOMO_INSTANCE`, `DOMO_MINOR_RN_TYPE_COLUMN`, plus the Mintlify preview secrets.

```mermaid
flowchart TD
    A([Trigger]) --> A1["schedule: Friday 13:17 UTC<br/>(before the release cut)"]
    A --> A2["workflow_dispatch<br/>(input: seed_ledger)"]
    A1 --> B
    A2 --> B

    B["Checkout + Python 3.12<br/>+ pip install anthropic"] --> C{"seed_ledger = true?"}

    C -->|Yes| D["build_minor_release_notes.py --seed-ledger<br/>(mark current score≥7 notes as published;<br/>writes NO article, publishes nothing)"]
    C -->|No| E["build_minor_release_notes.py<br/>(select week's score≥7 unpublished notes,<br/>restyle via Anthropic, archive prior week)"]

    D --> F
    E --> F
    F{"git status: changes in<br/>article / docs.json / ledger /<br/>Minor-Release-*.mdx?"}

    F -->|No| G([changed=false → stop])

    F -->|Yes| H["checkout -B auto/minor-release-notes<br/>commit (seed vs sync message) + force-push"]
    H --> I{"Open PR?"}
    I -->|Exists| J["Push refreshed PR"]
    I -->|None| K["gh pr create → main"]
    J --> L
    K --> L

    L{"MINTLIFY keys set?"}
    L -->|No| M([Warn, skip preview])
    L -->|Yes| N["POST Mintlify preview"]
    N --> O{"HTTP 202?"}
    O -->|No| P([Warn, no URL])
    O -->|Yes| Q["Sticky PR comment with preview URL"]
    Q --> R([PR ready for review<br/>— merge to publish with Friday release])
```

---

## `connector-review-daily.yml` — Connector Review Daily

Runs the `connector-review` skill unattended via Claude Code headless. It matches open connector PRs to their Jira tickets and, for each PR the secondary approver has already signed off on in Jira, runs the site-safety gate (`scripts/connector-review-gate.py`) in place of a manual GitHub approval. If the gate passes, the PR is auto-revised for style, approved, merged, and its Jira ticket commented + closed. **Content is never fact-checked** — this is code and rendering only; content approval still comes from the Jira secondary approver.

- **Schedule:** daily, 13:11 UTC (≈ 5–6am PST); also manual via `workflow_dispatch` with a `dry_run` boolean input.
- **Requires:** secrets `ANTHROPIC_API_KEY`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, and `CONNECTOR_REVIEW_PAT` (an admin GitHub PAT exported as `GH_TOKEN` so merges bypass the `main` ruleset).

```mermaid
flowchart TD
    A([Trigger]) --> A1["schedule: daily 13:11 UTC<br/>(~5–6am PST)"]
    A --> A2["workflow_dispatch<br/>(input: dry_run)"]
    A1 --> B
    A2 --> B

    B["Checkout (full history, admin PAT)<br/>fetch main · Node 22 · Corepack · yarn install<br/>mint CLI · Python 3.12 · Claude Code CLI<br/>git identity"] --> C["Run claude -p headless<br/>(--dangerously-skip-permissions)<br/>invoke connector-review skill"]

    C --> D["Run dashboard:<br/>connector-review.py<br/>match open PRs ↔ Jira tickets"]
    D --> E{"dry_run = true?"}
    E -->|Yes| E1([Print what it WOULD do;<br/>no merges / comments / pushes])

    E -->|No| F{"For each ticket:<br/>which state?"}

    F -->|"ready-to-merge /<br/>awaiting-jared /<br/>publish-request /<br/>escalation"| G["Checkout PR branch<br/>apply revise-submission style/MDX fixes<br/>pad tables · commit + push to PR"]
    G --> H["Run connector-review-gate.py<br/>(renderable MDX, repo+docs.json integrity,<br/>no new broken links, no case collisions, alt text)"]
    H --> I{"Gate exit code?"}
    I -->|"0 (pass)"| J["--merge DOMO-id<br/>→ comment + close Jira ticket"]
    I -->|"non-zero / error (2)"| K["Leave PR open<br/>record failing checks for manual review"]
    J --> R
    K --> R

    F -->|"stale-1 / stale-2"| L["Post next follow-up<br/>(--follow-up)"] --> R
    F -->|"migration-request"| M["Defer to manual<br/>(no action)"] --> R
    F -->|"changes-requested /<br/>on-hold"| N["Leave untouched"] --> R

    R["Run --check-holds"] --> S["Append dated entry to run-log.md<br/>commit run-log + connector-on-hold.json → push main"]
    S --> T["Find-or-create 'connector-review-log' issue<br/>post dated summary comment"]
    T --> U([Done · content never fact-checked;<br/>content approval stays with Jira approver])
```
