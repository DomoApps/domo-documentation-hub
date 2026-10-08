# Minor Release Notes Automation — Project Handoff

> **TEMPORARY FILE.** This lives at the repo root only to carry context on the
> branch `jared.peterson/minor-release-notes-automation`. **Delete it before
> merging to `main`.** It is not registered in `docs.json`, so Mintlify will not
> publish it, but it still shouldn't land on `main`.

---

## 1. What this is and why

The Knowledge Base's **Minor Release Notes** (incremental updates + resolved
issues that ship between the monthly feature releases) were maintained by hand.
A Domo Magic ETL DataFlow already enriches every hotfix/EC ticket and writes an
AI-drafted release-note sentence plus a quality score to an output DataSet. This
project turns that into a **true weekly automation**, modeled exactly on the
existing **Video Library** GitHub Action (`sync-video-library.yml`):

> Every Friday morning (just before the release is cut), a GitHub Action pulls
> the week's qualifying notes from the DataSet, restyles them into KB house
> voice, archives the previous week into a dated file + nav, and opens a PR. The
> KB Administrator's only manual step is the Friday double-check + merge.

Nothing publishes until that PR is merged, and the normal KB publishing cadence
still holds the merge for the Monday release.

**Why it's safe / how Domo access works:** a GitHub Action can't query a
DataFlow or a card — it queries the DataFlow's **output DataSet** via
`POST https://domo.domo.com/api/query/v1/execute/{datasetId}` with an
`X-DOMO-Developer-Token` header. The token is a revocable API credential (not a
login) that lives as an encrypted GitHub secret. This is the identical
mechanism the Video Library sync already uses.

---

## 2. The source DataSet (the data contract)

- **Instance:** `domo.domo.com`
- **DataSet:** `HOTFIX_Release_Enriched_PUBLIC`
- **DataSet ID:** `1aa127f4-edf6-4294-b509-186645a9e15b`

Interrogated from a sample export (12,511 rows). The columns that matter:

| Column | Role in the automation |
|---|---|
| `AI_release_notes` | **Source text** — one release-note sentence per row |
| `AI_ReleaseNotesScore` | **Publish gate: only score ≥ 7 is eligible** (per PM direction) |
| `master_targetdate` | **Week bucketing** — planned deploy date, 100% populated |
| `Public_Parent_Component` | **Section heading** (AI Labs, App Studio, Cards, Connectors, …) |
| `master_key` | EC ticket — a *batch* id that repeats across many rows; traceback only, **not** a feature title |

Key realities discovered in the data (these drove the design):

- Only ~378 of 12,511 rows have an AI note; 277 score ≥ 7; **but only ~166 are
  unique** — roughly 40% are exact duplicates, so **dedup is mandatory**.
- `master_summary` is the *batch* label ("Minor Release of 9/8 … on October
  15"), not a feature title. Feature titles aren't shown in the output anyway
  (bare-bullet format), so this doesn't matter for rendering.
- There is **no Update-vs-Issue-Resolved column** — it's inferred from the
  sentence ("resolves an issue"/"fixed"/"no longer"/"restored"/"preventing" →
  Issue Resolved; otherwise Update).
- Raw notes all open with **"This update …"**; published KB bullets never do. So
  the style rewrite is a *consistent transform on every bullet*, not an
  occasional touch-up.

---

## 3. Design decisions (all confirmed with Jared)

| Decision | Choice |
|---|---|
| Publish gate | `AI_ReleaseNotesScore >= 7` |
| Week date | `master_targetdate` |
| Weekly window | **Published ledger** (`tracking/minor-release-ledger.json`) — self-correcting; never double-publishes, never misses a late-scored note |
| Section grouping | `Public_Parent_Component` (with a small friendly-rename map, e.g. `PDP` → "Personalized Data Permissions") |
| Update vs Issue Resolved | Semantic keyword heuristic (no source column) |
| Bullet format | Current bare-bullet style — component → **Updates** / **Issues Resolved** → one sentence each (matches the old article) |
| Style rewrite | **Anthropic API** inside the Action, model `claude-haiku-5-5` (cheap, pennies/week) |
| Live file | **New** `s/article/Current-Minor-Release-Notes.mdx` (mirrors `Current-Release-Notes.mdx`) |
| Old article | `000005908` content archived as the first historical week; English article retired with a redirect |
| Archive nav | New **Archived Minor Release Notes** group → **Year → Month → per-week file** |

---

## 4. What was built

### Scripts
- **`scripts/build_minor_release_notes.py`** — the engine. Queries the DataSet
  (or a local CSV via `MINOR_RN_CSV`), filters score ≥ 7 + non-empty, dedups,
  selects notes dated on/before the run day **not already in the ledger**,
  classifies Update/Issue Resolved, restyles each (Claude Haiku), archives the
  outgoing week (calls the archiver), writes
  `s/article/Current-Minor-Release-Notes.mdx`, and appends the ledger.
  Flags: `--no-llm` (deterministic restyle, offline), `--run-date YYYY-MM-DD`
  (pins "today"), `--dry-run` (print, write nothing), `--seed-ledger` (go-live;
  see §7).
- **`scripts/archive_minor_release_notes.py`** — rolls the current file into
  `s/article/Minor-Release-{YYYY-MM-DD}.mdx` and inserts it into `docs.json`
  under Archived Minor Release Notes → Year → Month (creating subgroups as
  needed) via surgical text edits (no 307 KB reformat). Importable
  (`roll_current_to_archive`) and runnable standalone with `--dry-run`.

### Workflow
- **`.github/workflows/sync-minor-release-notes.yml`** — Friday **13:17 UTC**
  cron (≈ 6–7am Mountain, before the release cut) + manual `workflow_dispatch`.
  Bot branch `auto/minor-release-notes`, PR to `main`, Mintlify preview sticky
  comment, clean no-op when there's nothing new. A faithful clone of the Video
  Library action.

### Skill
- **`.claude/skills/minor-release-notes/SKILL.md`** — operator guide + the
  authoritative data contract, ledger logic, style spec, and go-live procedure.

### One-time content migration (part of this branch)
- Created `s/article/Current-Minor-Release-Notes.mdx` (**placeholder** until the
  first run populates it).
- Archived the old `000005908` content as
  `s/article/Minor-Release-2025-10-01.mdx` (retitled "Minor Release | October 1,
  2025") — the first historical week.
- Retired the English `s/article/000005908.mdx` (`git rm`) with a `docs.json`
  **redirect** `/s/article/000005908` → `/s/article/Current-Minor-Release-Notes`
  so the old URL still resolves.
- `docs.json` English nav: swapped the `000005908` entry for
  `Current-Minor-Release-Notes` and added the Archived Minor Release Notes group
  seeded with 2025 → October → the archived week.
- Updated `Article-PM-Ownership-Reference.mdx` and the CLAUDE.md Scripts +
  Skills tables.
- Committed an empty ledger `tracking/minor-release-ledger.json`.

### Deliberately NOT done
- The **4 localized** `000005908` nav entries (ja/fr/de/es) are **left in
  place**. Localization is English-first and handled in its own phase; migrating
  them now is out of scope.

---

## 5. How the weekly flow works (mental model)

1. CI checks out a clean `main`. The current file holds last week; the ledger
   holds everything published so far.
2. **build** selects this week's new notes (score ≥ 7, dated ≤ today, not in the
   ledger). If none → no-op, clean exit, no PR.
3. If there are new notes: the outgoing current file is rolled into a dated
   archive (+ nav), the new week is written to the current file, and the week's
   notes are appended to the ledger.
4. The changed files are force-pushed to `auto/minor-release-notes`; a PR is
   opened/updated with a Mintlify preview link.
5. Because CI always starts from `main`, re-running the same day is idempotent.

---

## 6. Status — where we are

- **Everything is built and verified offline** on this branch.
- Offline test (sample CSV, `--no-llm`, run-date 2026-10-07): 12,511 rows → 277
  at score ≥ 7 → 166 unique → **163 selected** (3 future-dated Oct-15 notes
  correctly held). Re-run with a populated ledger → **0 selected** (no
  double-publish). Archiver dry-run against the real `docs.json` correctly
  creates the 2026 → October nesting. Both scripts compile; `docs.json` and the
  ledger are valid JSON.
- **GitHub repo variable `DOMO_MINOR_RN_DATASET_ID` is ADDED** (done by Jared).

### The one thing NOT yet tested
The **live Haiku rewrite** against real Domo data — because there's no Anthropic
API key locally yet. The deterministic `--no-llm` fallback was tested; the real
model output has not been eyeballed on a live week.

---

## 7. What's needed to go live (remaining steps)

1. **Anthropic API key** — Jared is obtaining access to create one
   (console.anthropic.com → Settings → API Keys). Add it as the GitHub **secret**
   `ANTHROPIC_API_KEY`.
2. **Domo token** — the repo secret `DOMO_DEVELOPER_TOKEN` already exists (Video
   Library uses it). **Confirm its owner can read `HOTFIX_Release_Enriched_PUBLIC`.**
   If not, re-mint a token under an account that can, or share the DataSet.
3. **Seed the ledger** so the first automated run doesn't dump the entire
   backlog:
   ```bash
   python3 scripts/build_minor_release_notes.py --seed-ledger
   ```
   (needs the Domo token in env/`.env`, or `MINOR_RN_CSV`). This marks every
   current note as already published; the first Friday run then emits only notes
   that appear afterward. **Commit the seeded ledger.**
4. **First run:** trigger the workflow manually (Actions → Sync Minor Release
   Notes → Run workflow) and review the opened PR + preview before relying on the
   Friday schedule.
5. **Delete this handoff file** before merging to `main`.

### Secrets / variables summary
| Name | Type | Status |
|---|---|---|
| `DOMO_DEVELOPER_TOKEN` | secret | exists (verify DataSet read access) |
| `ANTHROPIC_API_KEY` | secret | **TODO** — Jared obtaining access |
| `DOMO_MINOR_RN_DATASET_ID` | variable | ✅ added |
| `MINTLIFY_KEY`, `MINTLIFY_PROJECT_ID` | secrets | exist (preview comment) |
| `DOMO_INSTANCE` | variable | not needed (defaults to `domo.domo.com`) |

---

## 8. How to test

```bash
# Offline, no credentials — deterministic restyle, prints without writing:
MINOR_RN_CSV=/path/to/HOTFIX_Release_Enriched_PUBLIC.csv \
  python3 scripts/build_minor_release_notes.py --no-llm --run-date 2026-10-07 --dry-run

# Live, with real Haiku rewrite (needs DOMO_DEVELOPER_TOKEN + ANTHROPIC_API_KEY
# in the environment or a gitignored .env):
python3 scripts/build_minor_release_notes.py --dry-run

# Preview the archive roll + nav insertion without writing:
python3 scripts/archive_minor_release_notes.py --dry-run

# Validate docs.json after any nav edit:
python3 -c "import json; json.load(open('docs.json')); print('valid')"
```

A sample DataSet export was used during development at
`HOTFIX_Release_Enriched_PUBLIC.csv` (kept off the repo — it's internal data).

---

## 9. Where to pick this up later

The project memory also records this (slug `project_minor_release_notes_automation`).
The skill `minor-release-notes` is the long-lived operator reference — this file
is the throwaway branch-context note.
