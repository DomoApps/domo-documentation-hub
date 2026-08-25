# Phase 3b cluster: Phil-Fuchs__1

**Owning PM:** Phil Fuchs
**Files in this cluster:** 4  |  **Gaps:** 6

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005559.mdx`
*Use Non-aggregated Columns in Aggregated Beast Modes* — area: Analyzer (Pivot Table)

### Gap rank 323 (Low, score 42.6) — Pivot table expand/collapse breaks with HTML-link Beast Mode columns
- **What's missing:** Document that Pivot Tables don't support HTML-link content and this breaks expand/collapse for affected columns.
- **Suggested location:** Add a one-line limitation note to the Pivot Table chart-type article (Charting bucket) that HTML-link content isn't supported and breaks expand/collapse. Peripheral to Beast Mode/Variables.

---

## `s/article/360043429913.mdx`
*Create a Beast Mode Calculation* — area: Beast Mode / Calculations

### Gap rank 112 (Medium, score 59.8) — Beast Mode in Dataset View vs Analyzer (saved-to-dataset) — differences and when to use each
- **What's missing:** Clarify the two are largely identical in capability but differ in context (Views are row-level oriented, Analyzer is aggregation-oriented) and guidance on which to choose.
- **Suggested location:** Add a short 'where to create a Beast Mode (Dataset View vs Analyzer)' section to s/article/360043429913.mdx covering the row-level vs aggregation context and selection guidance.

- **Other referenced articles:** s/article/360042925474.mdx

### Gap rank 284 (Medium, score 46.4) — Net Income / calculated account-type rows in dataflow vs Beast Mode (quoting rules)
- **What's missing:** How-to for producing calculated rows like Net Income (Magic ETL vs Beast Mode + table totals) and Beast Mode quoting rules (single quotes for text, backticks for field names).
- **Suggested location:** Clarify Beast Mode quoting rules (single quotes = text literal, backticks = field name) in s/article/360043429913.mdx (Create a Beast Mode Calculation) / Beast Mode FAQs, and note adding calculated rows like Net Income via Magic ETL union vs a table Total row.

- **Other referenced articles:** s/article/360043430053.mdx

### Gap rank 339 (Low, score 39.8) — Magic ETL access prerequisites and cloud-connector dependency errors
- **What's missing:** Documentation of Magic ETL access prerequisites (role/grants required) and that errors can stem from a referenced cloud-connector dataset, plus whether a cloud account is required to use Magic ETL.
- **Suggested location:** Update the Magic ETL overview/getting-started article with an access-prerequisites note (required role/grants) and a troubleshooting note that a referenced cloud-connector dataset can cause open errors.

---

## `s/article/360043430133.mdx`
*Sample Beast Mode Calculations: Period-over-Period Transforms* — area: Beast Mode / Analyzer date settings

### Gap rank 133 (Medium, score 57.6) — NUMBER_FORMAT / 'Include Today?' (exclude today) date-range feature gaps
- **What's missing:** Feature request. Documentable workaround: a CASE-based 'Today/No' filter to exclude the current date from rolling ranges.
- **Suggested location:** Add a short 'exclude today from a rolling range' CASE recipe to s/article/360043430133.mdx or the Date Transforms sample. Feature request otherwise.

- **Other referenced articles:** s/article/360042925494.mdx

---

## `s/article/360043430733.mdx`
*DataSet Update Methods* — area: APIs

### Gap rank 224 (Medium, score 50.3) — DataSet API limitations: row-level updates, upserts, and append part-id errors
- **What's missing:** Documentation of DataSet API update semantics (no row-level update/delete; only Replace and Append), the recommended upsert workarounds (CLI partition-dataset and define-upsert, staging dataset + ETL), and how to avoid the consecutive part-id error when streaming large/multi-part uploads.
- **Suggested location:** Update s/article/360043430733.mdx (DataSet Update Methods) to state plainly that the public DataSet API supports only Replace and Append (no row-level update/delete) and point to upsert via CLI define-upsert / PARTITION. Add a troubleshooting note to the Stream API docs (portal/API-Reference/Domo-APIs/Stream-API.yaml) explaining the 'Too many non-consecutive part ids' error and the sequential part-id requirement.

- **Other referenced articles:** portal/API-Reference/Domo-APIs/Stream-API.yaml, portal/Apps/App-Framework/Guides/manifest.mdx

---
