---
name: minor-release-notes
description: Operate the weekly Minor Release Notes automation — the Friday GitHub Action that drafts s/article/Current-Minor-Release-Notes.mdx from the Domo hotfix DataSet, archives the prior week, and opens a PR. Use to run a manual rebuild, re-style notes, seed the ledger at go-live, understand the data contract, or debug the pipeline. Not for the monthly product feature-release notes (use product-release-notes).
---

# Minor Release Notes automation

A weekly GitHub Action (`.github/workflows/sync-minor-release-notes.yml`) drafts the
Minor Release Notes from a Domo DataFlow's output DataSet, archives the previous
week, and opens a PR every Friday morning for the KB Administrator to double-check
and merge — mirroring the Video Library sync. This skill is the operator's guide and
the single source of truth for the data contract and the style rewrite.

## The two scripts

- **`scripts/build_minor_release_notes.py`** — the engine. Queries the DataSet,
  selects the week's publishable notes, restyles each into house voice, archives the
  outgoing week (by calling the archiver), writes `s/article/Current-Minor-Release-Notes.mdx`,
  and appends the week's notes to the ledger.
- **`scripts/archive_minor_release_notes.py`** — rolls the outgoing current file into
  `s/article/Minor-Release-{YYYY-MM-DD}.mdx` and registers it in `docs.json` under
  **Archived Minor Release Notes → {Year} → {Month}**. Importable (`roll_current_to_archive`)
  and runnable standalone with `--dry-run`.

## Data contract (DataSet `HOTFIX_Release_Enriched_PUBLIC`)

Instance `domo.domo.com`, DataSet ID `1aa127f4-edf6-4294-b509-186645a9e15b`.

| Field | Role |
|---|---|
| `AI_release_notes` | Source note text (one sentence per row) |
| `AI_ReleaseNotesScore` | **Publish gate: only score ≥ 7 is eligible** |
| `master_targetdate` | Planned deploy date — buckets notes into weeks |
| `Public_Parent_Component` | Section heading (friendly-renamed where needed) |
| `master_key` | EC ticket (batch id, *not* a feature title) — traceback only |

The pipeline: filter `score ≥ 7` + non-empty → **dedup** on normalized note text
(~40% are exact duplicates) → select notes dated on/before run day **not already in the
ledger** → classify Update vs Issue Resolved → restyle → group by component → render.

**Update vs Issue Resolved** is inferred from the sentence (no column): "resolves an
issue", "fixed", "no longer", "restored", "preventing" → Issue Resolved; otherwise Update.

## The published ledger

`tracking/minor-release-ledger.json` holds a sha1 of every note already published
(normalized text). This is what makes the Friday run self-correcting: a note is never
published twice, and a note scored ≥ 7 *after* its deploy date is still picked up on the
next run. The build step appends to it; the archiver never touches it. Because CI always
starts from a clean checkout of `main`, re-running the workflow the same day is idempotent.

## Style rewrite (Hybrid)

Raw notes open with "This update …"; published bullets must not. The rewrite converts
each note to Minor Release Notes house voice:
- **Issue Resolved** → past-tense problem statement ("Hidden calculations were not being
  properly deleted from cards.").
- **Update** → present-tense imperative/descriptive statement ("Add new rows in Linked Tables.").

The automation calls Claude Haiku (`claude-haiku-5-5`) with the spec in
`STYLE_SYSTEM` inside `build_minor_release_notes.py` — **that constant is the
authoritative style prompt; keep this section and it in sync.** `--no-llm` falls back to a
rules-based transform (rougher — for offline testing only).

## Running it

```bash
# Normal rebuild (needs DOMO + ANTHROPIC creds in env or .env):
python3 scripts/build_minor_release_notes.py

# Offline test against a local CSV export, deterministic restyle, no creds:
MINOR_RN_CSV=/path/to/export.csv python3 scripts/build_minor_release_notes.py --no-llm --dry-run

# Pin the "today" used for week selection (notes dated after it are held):
python3 scripts/build_minor_release_notes.py --run-date 2026-10-16

# Preview the archive roll + nav insertion without writing:
python3 scripts/archive_minor_release_notes.py --dry-run
```

## Go-live procedure (one time, by the KB Administrator)

1. Mint a Domo developer access token (Admin → Authentication → Access Tokens).
2. Add repo secret `DOMO_DEVELOPER_TOKEN` and `ANTHROPIC_API_KEY`; add repo variable
   `DOMO_MINOR_RN_DATASET_ID` = `1aa127f4-edf6-4294-b509-186645a9e15b` (and `DOMO_INSTANCE`
   if not `domo.domo.com`).
3. **Seed the ledger** so the first automated run doesn't republish the entire backlog:
   `python3 scripts/build_minor_release_notes.py --seed-ledger` (needs the token, or
   `MINOR_RN_CSV`). This marks every current note as already published; the first Friday
   run then emits only notes that appear afterward. Commit the seeded ledger.
4. Trigger the workflow manually (`workflow_dispatch`) and review the opened PR + preview.

## Notes

- Localized (ja/fr/de/es) Minor Release Notes are **not** handled here — the retired
  `000005908` localized nav entries remain in place for the English-first localization
  phase to address.
- The live article's URL `/s/article/000005908` redirects to
  `/s/article/Current-Minor-Release-Notes` (docs.json `redirects`).
