# Localization

Everything the `localize` and `localization-retrospective` skills need to translate
Domo KB articles into Spanish (`es/`), French (`fr/`), German (`de/`), and Japanese
(`ja/`) **deterministically**, and to **learn** from human translator corrections.

This directory is for AI and technical contributors. Non-technical writers do not
need to read or touch anything here.

## What's here

| Path | What it is |
| --- | --- |
| `Localization-Style-Guide.mdx` | The authoritative prose style guide: tone, register, MDX rules, per-language conventions, release-notes conventions. Read in full before translating. |
| `glossary/{es,fr,de,ja}.csv` | **Deterministic term glossaries.** English term → fixed target translation, plus keep-in-English rules. Consulted while translating and during the QA check so terminology is identical every run. |
| `sources/Domo_BrandedTerms_PMMupdates_092425 1.csv` | PMM branded-terms glossary (89 rows). The cross-language seed for what stays in English vs. what is OK to translate. |
| `sources/JA-XTM-TM.csv` | Raw XTM Japanese translation memory (~97 MB, **gitignored**). Kept on disk for term mining and consultation; never committed. |
| `retrospective/retrospective-log.csv` | Append log of every retrospective run (what PRs were analyzed, what terms were learned). |
| `retrospective/.snapshots/` | **Gitignored.** Per-run snapshots of the skill's raw translation output, keyed by commit SHA, so the retrospective can diff human-corrected merged PRs against the AI original. |

## Glossary CSV schema

```
english_term,translation,keep_in_english,context,notes,source,last_updated
```

- `keep_in_english = yes` → never translate; `translation` is blank.
- `context` disambiguates homographs (e.g. `Table` → `表` for UI vs `テーブル` for a database).
- `source` ∈ `style-guide` · `branded-terms` · `mined-tm` · `mined-articles` · `retrospective:PR#N`.
  Rows sourced from the style guide / branded terms are the trusted baseline; `mined-*` rows are
  auto-extracted and flagged for human vetting; `retrospective:*` rows were learned from corrections.
- `last_updated` = ISO date.

## How the pieces work together

1. **Translate deterministically.** The `localize` skill loads `glossary/<lang>.csv` and applies
   every matching term exactly — keep-in-English terms untouched, translated terms rendered per the
   glossary.
2. **Check deterministically.** `scripts/check-glossary.py <english> <translated> <lang>` reports any
   glossary term whose rule the translation appears to break. The skill runs this and fixes findings.
3. **Snapshot.** Right after writing each localized file (every language), the skill copies it into
   `retrospective/.snapshots/<sha>/<lang>/` — the record of what the AI produced before human review.
4. **Learn.** After human translators correct articles in a CAT tool and the corrected versions land
   as merged PRs, the `localization-retrospective` skill (Step 0 of `localize`) diffs merged-vs-snapshot,
   extracts term-level corrections, and writes them back into the glossaries as `retrospective:PR#N`
   rows — a self-improving translation memory.

## Regenerating the glossaries

```bash
python3 scripts/build-localization-glossary.py          # rebuild all four CSVs
python3 scripts/build-localization-glossary.py --report # also print the JA TM mining report
```

The builder regenerates `style-guide` / `branded-terms` / `mined-tm` rows from the style guide, the
branded-terms CSV, and the XTM TM. It **preserves** `retrospective:*` and `manual*` rows, so the
learning-loop entries are never lost on a rebuild.
