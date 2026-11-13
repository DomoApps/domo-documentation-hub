---
name: minor-release-notes
description: Operate the weekly Minor Release Notes automation — the Friday GitHub Action that drafts s/article/Current-Minor-Release-Notes.mdx from the Domo hotfix DataSet, archives the prior week, and opens a PR. Use to run a manual rebuild, re-style notes, seed the ledger at go-live, understand the data contract, or debug the pipeline. Not for the monthly product feature-release notes (use product-release-notes).
---

# Minor Release Notes automation

A weekly GitHub Action (`.github/workflows/sync-minor-release-notes.yml`) drafts the
Minor Release Notes from a Domo DataFlow's output DataSet, archives the previous
week, and opens a PR every Friday morning for the KB Administrator to double-check
and merge — mirroring the Video Library sync. This skill is the operator's guide and
the single source of truth for the data contract and the rewrite pipeline.

## The DataSet is internal; this skill is the customer-facing last mile

The source DataSet (`AI_release_notes`) is written for an **internal** audience and
stays that way on purpose — internal reviewers reading it on the Domo app need the
real, specific wording (e.g. "we created feature switches that handle this problem").
We deliberately do **not** build a second, external-framed transform in the ETL. This
skill does the customer-facing translation at the **last mile**: it rewrites each
internal note into the public Minor Release Notes house voice, abstracts it to what's
already publicly disclosed, and removes anything that must not be published. (Decision
from the Nov 2026 customer-facing-framing review with Security/Legal.)

The style lives in an **editable house style guide**, not in the Python:

- **`.claude/skills/minor-release-notes/minor-release-notes-style.md`** — the
  authoritative customer-facing writing standard for these notes, derived from the
  product-release-notes house style and extended with the security/legal rules below.
  The build script loads this file **verbatim as the Anthropic system prompt**
  (`load_style_system`), so the nuanced revision is an LLM task and the style is owned
  in one place. Edit this file to change how the notes read — no code change needed.

## The two scripts

- **`scripts/build_minor_release_notes.py`** — the engine. Queries the DataSet,
  selects the week's publishable notes, **screens out security/privacy-sensitive
  notes**, rewrites each into the customer-facing house voice (loading the style guide
  above as the system prompt), archives the outgoing week (by calling the archiver),
  writes `s/article/Current-Minor-Release-Notes.mdx`, and appends the week's notes to
  the ledger.
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
| *(optional)* note-type column | If the DataSet ever adds one, turns the flat list back into Updates / Issues Resolved sections — see below |

The pipeline: filter `score ≥ 7` + non-empty → **dedup** on normalized note text
(~40% are exact duplicates) → select notes dated on/before run day **not already in the
ledger** → restyle → group by component → render.

## No Updates / Issues Resolved split (unless an official column exists)

Published Minor Release Notes list every note in **one flat list under its product
section** — there is deliberately **no "Updates" vs "Issues Resolved" delineation**. The
script never infers that split from the sentence for publishing.

**The one exception (future-proofed):** if the source DataSet gains an *official* column
tagging each note's type, the split comes back automatically, driven by that column:

- **Live Domo run:** set the repo variable **`DOMO_MINOR_RN_TYPE_COLUMN`** to the column's
  exact name. The build then SELECTs it, detects it, and renders **Updates** then **Issues
  Resolved** per section. Leave the variable unset and the output stays flat — the SELECT
  never references the column, so it can't fail against a DataSet that lacks it.
- **Local CSV test:** just include a column named `Public_Note_Type` (the default name) and
  the delineated render activates. Cell values containing "issue"/"resolved"/"fix"/"bug" →
  *Issues Resolved*; anything else → *Updates*.

`classify()` in the build script still infers Update-vs-Issue, but **only to shape each
bullet's voice** (past-tense problem vs present-tense behavior); with no official column it
produces no visible section headers.

## The published ledger

`tracking/minor-release-ledger.json` holds a sha1 of every note already published
(normalized text). This is what makes the Friday run self-correcting: a note is never
published twice, and a note scored ≥ 7 *after* its deploy date is still picked up on the
next run. The build step appends to it; the archiver never touches it. Because CI always
starts from a clean checkout of `main`, re-running the workflow the same day is idempotent.

## Style rewrite (LLM + editable house style guide)

The automation calls Claude Sonnet (`claude-sonnet-5-5`) once per note, passing
**`minor-release-notes-style.md` verbatim as the system prompt** (`load_style_system`).
The guide — not any constant in the script — is the authoritative style spec. It
covers, in full: the one-sentence output contract; secure-and-optimistic voice;
the Issue-Resolved (past-tense) vs Update (present-tense) sentence forms; the ban on
"This update…" openers; no obligations/commitments (legal); abstraction to the level of
already-published Domo docs; removal of internal terminology (no "feature switch" →
**Feature Management**/admin options, no system names, infra, Jira/EC keys); and the
`__EXCLUDE__` rule for security/privacy content. **Change the writing by editing that
file** — there is no style string in the Python to keep in sync anymore.

`--no-llm` falls back to a deterministic rules transform that does **not** apply the
house style (it only strips the "This update…" lead and honors the hard security
screen). It is for offline wiring tests only, never for a real publish.

## Two-layer safety screen (remove, don't abstract)

Security, privacy, information-disclosure, infrastructure-risk, and legal-conflict notes
must be **removed entirely**, not softened. Two layers enforce this:

1. **Deterministic keyword screen** (`screen_external` / `SECURITY_EXCLUDE_PATTERNS` in
   the build script) runs **before** the rewrite, so obviously sensitive text (CVEs,
   "vulnerability," "patched PHP/OpenSSL," "information disclosure," etc.) never reaches
   the model or the article. Broaden the pattern list when a new class of sensitive term
   shows up.
2. **LLM semantic net** — the style guide instructs the rewrite to return `__EXCLUDE__`
   for anything unsafe or non-public it still catches (including intermingled security
   context and internal-only notes with no customer-visible effect). The renderer drops
   every `__EXCLUDE__` bullet and omits any product section left empty; if a week's whole
   selection is removed, the current article is left unchanged (no empty publish).

Both layers err toward removal. They are a safety net under — not a replacement for — the
mandatory human review below.

## Human review is mandatory

Nothing publishes without human validation. The Friday PR is reviewed and merged by the
KB Administrator, and the rewritten copy is sent to Security/Legal (Paul Conover) each
week for feedback and fine-tuning until the framing is dialed in. Any change to the
framing goes into `minor-release-notes-style.md`.

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

Seeding runs **through CI** off the existing `DOMO_DEVELOPER_TOKEN` repo secret, so the
token never has to live on anyone's machine. GitHub Actions secrets are write-only — a
local script can't read them back — which is why the seed is a `workflow_dispatch` option
rather than a local command.

1. Mint a Domo developer access token (Admin → Authentication → Access Tokens).
2. Add repo secret `DOMO_DEVELOPER_TOKEN` and `ANTHROPIC_API_KEY`; add repo variable
   `DOMO_MINOR_RN_DATASET_ID` = `1aa127f4-edf6-4294-b509-186645a9e15b` (and `DOMO_INSTANCE`
   if not `domo.domo.com`).
3. **Merge this workflow to `main` first** — `workflow_dispatch` and `schedule` only work
   for workflows on the default branch.
4. **Seed the ledger** so the first automated run doesn't republish the entire backlog:
   Actions → *Sync Minor Release Notes* → **Run workflow**, with **`seed_ledger` checked**.
   This marks every current note as already published and opens a ledger-only PR ("Seed
   Minor Release Notes ledger"); merge it. The seed writes no article and publishes nothing.
   (The equivalent local command, if ever seeding off a token/`MINOR_RN_CSV` in env, is
   `python3 scripts/build_minor_release_notes.py --seed-ledger`.)
5. **First real run:** Actions → **Run workflow** with `seed_ledger` unchecked (or wait for
   the Friday cron), then review the opened PR + preview.

**Safety guard:** a normal (non-seed, non-`--dry-run`) build aborts if the ledger is empty,
so forgetting to seed can never dump the whole backlog into one week.

## Notes

- Localized (ja/fr/de/es) Minor Release Notes are **not** handled here — the retired
  `000005908` localized nav entries remain in place for the English-first localization
  phase to address.
- The live article's URL `/s/article/000005908` redirects to
  `/s/article/Current-Minor-Release-Notes` (docs.json `redirects`).
