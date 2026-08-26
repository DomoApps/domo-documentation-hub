---
name: localization-retrospective
user-invocable: true
description: "Learn from human translator corrections: diff a merged (human-corrected) localized PR against what the localize skill originally produced, and fold the term-level corrections back into the deterministic glossaries. Runs as Step 0 of the localize skill; also invocable on its own."
argument-hint: "PR number(s) to analyze, or 'none' (e.g., 456 or 456,457)"
---

Run a retrospective on human-corrected localized articles and update the deterministic
glossaries so future translations improve — a self-improving translation memory.

The user has provided: $ARGUMENTS

## What this skill is for

After the `localize` skill translates an article, the file goes to a CAT tool where a human
translator reviews and corrects it. The corrected batch returns to the repo as a **merged PR**.
This skill reads that merged PR, compares the final (human-corrected) article against **what the
localize skill originally produced**, extracts the term-level corrections, and writes them into
`localization/glossary/<lang>.csv` so the same mistake is not repeated.

**Forward-looking:** the Japanese CAT-tool correction loop may not have produced any merged PRs
yet. If there is nothing to analyze, that is the normal, expected state early on — exit cleanly.
Snapshots (the record of the AI's original output) only begin accumulating once the updated
`localize` skill has run at least once.

---

## Step 1: Get the PR(s) to analyze

If `$ARGUMENTS` already contains PR number(s), use them. Otherwise ask the user exactly:

> **What PR or PRs would you like me to run a diff-analysis retrospective on to improve my
> deterministic memory? (Enter PR number(s), or say 'none'.)**

If the user says `none` / `skip` / gives nothing: report "No retrospective to run" and stop. When
called from `localize` Step 0, return control to `localize` so translation proceeds.

---

## Step 2: For each PR, find the corrected localized files

```bash
gh pr view <N> --json number,title,mergedAt,mergeCommit,headRefName,files
```

- Confirm the PR is **merged** (`mergedAt` is non-null). If not merged, tell the user and skip it —
  this skill only learns from merged, human-approved corrections.
- From `files`, keep only changed paths under `es/s/article/`, `fr/s/article/`, `de/s/article/`, or
  `ja/s/article/`. Each file's language is its top-level directory.
- Skip the PR (with a note) if its branch/title signals a **structural-only** pass rather than a
  translation correction — e.g. branch names containing `formatting-fixes` or work done by the
  `fix-ja-formatting` skill. Those change MDX structure, not terminology.

---

## Step 3: Obtain the "AI original" for each file

For each corrected file, get the version the localize skill produced, in this order of preference:

1. **Snapshot (preferred).** Look under `localization/retrospective/.snapshots/` for a saved copy of
   this file (same `<lang>/<filename>`). If several snapshots exist, use the most recent one whose
   content differs from the merged version. This is the true pre-correction AI output.

   ```bash
   ls localization/retrospective/.snapshots/*/<lang>/<filename> 2>/dev/null
   ```

2. **Git fallback.** If no snapshot exists, inspect the PR's own history. Get the file's content at
   the PR branch's **first** commit and compare to the merged content:

   ```bash
   gh pr view <N> --json commits         # list commits oldest-first
   git show <first-commit-sha>:<path>    # AI-original candidate
   git show <merge-commit-sha>:<path>    # final human-corrected
   ```

   Note: batch localization PRs often land the corrected article as a single net-new commit, so this
   fallback frequently yields no usable "before" version.

3. **Skip.** If neither a snapshot nor a distinguishable earlier commit exists, skip the file and
   record it as `no-baseline` in the run summary. Do **not** re-translate from scratch to fabricate a
   baseline — that invents corrections that never happened.

---

## Step 4: Extract term-level corrections

For each file where you have both an AI-original and the merged version:

1. Diff them (read both; focus on changed lines).
2. Identify **term-level** changes: a Domo/technical/UI term where the human chose a different
   target rendering than the skill did, or corrected a keep-in-English term that had been translated
   (or vice versa). Map each back to its **English source term** using the paired English article in
   `s/article/<filename>`.
3. **Ignore non-terminology changes:** pure MDX/formatting fixes, blank-line/callout wrapping,
   punctuation-only edits, whole-sentence rephrasings that don't reassign a specific term. Those are
   not deterministic glossary facts.
4. For each real term correction, record: `english_term`, corrected `translation` (or
   `keep_in_english` flip), `context` if the term is context-dependent, and the source PR number.

Cross-check every candidate against the current `localization/glossary/<lang>.csv` and the
`Localization-Style-Guide.mdx` before writing it — only record genuine deltas.

---

## Step 5: Update the glossary

For each confirmed correction, update `localization/glossary/<lang>.csv`:

- **New term** (not in the glossary): add a row with `source=retrospective:PR#<N>` and today's date
  (`date +%Y-%m-%d`).
- **Existing `mined-*` or `branded-terms` row:** update its `translation`/`keep_in_english`, set
  `source=retrospective:PR#<N>`, refresh `last_updated`, and note the prior value in `notes`.
- **Existing `style-guide` (authoritative) row that conflicts:** do **not** silently overwrite.
  Show the user the conflict (glossary value vs. human correction) and ask whether to (a) override
  the glossary, (b) keep the style-guide value and treat the correction as a one-off, or (c) update
  the style guide too. Apply only what the user approves.

These `retrospective:*` rows are preserved across `build-localization-glossary.py` rebuilds, so
learned corrections are never lost.

Keep the CSV valid: same 7 columns, no stray blank lines, quote any field containing a comma.

---

## Step 6: Log the run

Append one row to `localization/retrospective/retrospective-log.csv`:

```bash
echo "$(date +%Y-%m-%d),$(git config user.name),PRS,LANGS,FILES_REVIEWED,TERMS_LEARNED,NOTES" >> localization/retrospective/retrospective-log.csv
```

- `PRS` = slash-separated PR numbers analyzed (e.g. `456/457`).
- `LANGS` = slash-separated language codes touched (e.g. `ja`).
- `FILES_REVIEWED`, `TERMS_LEARNED` = integers.
- `NOTES` = short free text (quote if it contains a comma), e.g. `2 no-baseline skipped`.

---

## Step 7: Report

Tell the user:

1. PRs analyzed (and any skipped, with the reason — not merged, formatting-only, no-baseline).
2. Files reviewed per language.
3. Terms learned — list each `english_term → corrected translation (context)` and whether it was a
   new row, an updated mined row, or a flagged style-guide conflict.
4. Any style-guide conflicts awaiting the user's decision.

If invoked from `localize` Step 0, then return control so translation continues with the freshly
updated glossary.
