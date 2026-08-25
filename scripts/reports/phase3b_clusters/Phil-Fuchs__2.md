# Phase 3b cluster: Phil-Fuchs__2

**Owning PM:** Phil Fuchs
**Files in this cluster:** 4  |  **Gaps:** 9

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360043428693.mdx`
*Understanding Chart Data* — area: Charting & Analyzer / Data Types

### Gap rank 317 (Low, score 43.1) — Float/numeric ID columns treated as measures in filters/analyzer
- **What's missing:** Documentation explaining why numeric (float) columns are treated as measures vs dimensions in Analyzer/quick filters, and how to convert an ID to a dimension (string) so it filters as discrete values.
- **Suggested location:** Add a short note to s/article/360043428693.mdx (Understanding Chart Data) or a quick-filter article: numeric (float) columns are treated as measures, so their quick filter shows a range/aggregation; cast an ID to string in Magic ETL to make it a dimension that filters as discrete values.

---

## `s/article/360043429933.mdx`
*Beast Mode Functions Reference Guide* — area: Beast Mode / Calculations

### Gap rank 130 (Medium, score 57.9) — Beast Mode number-formatting function (NUMBER_FORMAT / TO_CHAR) and formatting numbers in concatenated strings
- **What's missing:** Feature request. Until shipped, document the verbose Beast Mode patterns for thousands separators / currency / percent / abbreviation within concatenated strings.
- **Suggested location:** Add a 'formatting numbers inside strings' recipe section to a Sample Transforms article (e.g. s/article/360043430113.mdx Miscellaneous or s/article/360042925514.mdx Mathematical): comma/currency/percent formatting and abbreviation patterns for concatenated values.

- **Other referenced articles:** s/article/360043430113.mdx

### Gap rank 154 (Medium, score 55.7) — Beast Mode date/time difference calculations (DATEDIFF, TIMESTAMPDIFF, UNIX_TIMESTAMP, business days/hours)
- **What's missing:** Needs a recipe set: DATEDIFF unit behavior and why summing duplicates (use MIN/MAX), hour/minute durations via TIMESTAMPDIFF or UNIX_TIMESTAMP subtraction, formatting durations to HH:MM, business days excluding weekends, business-hours exclusion, and 'end of next day' timestamp construction. Note TIMESTAMPDIFF is not in the Functions Reference.
- **Suggested location:** Add a 'duration / elapsed-time recipes' section to s/article/360042925494.mdx (Date Transforms) or the FAQ: HH:MM formatting via SEC_TO_TIME/TIME_TO_SEC, decimal-hours via UNIX_TIMESTAMP subtraction, business-days/business-hours, and the MIN/MAX trick to avoid summing duplicated DATEDIFF. Add TIMESTAMPDIFF to the Functions Reference if supported.

- **Other referenced articles:** s/article/360043430053.mdx, s/article/360042925494.mdx

### Gap rank 155 (Medium, score 55.5) — Beast Mode IN-list / expression size limit (large value lists)
- **What's missing:** State any practical limit on Beast Mode IN-list / expression length and recommend alternatives (ETL join against a lookup dataset, splitting into OR'd statements) for large value lists.
- **Suggested location:** Add a note to the IN-operator description in the Functions Reference (s/article/360043429933.mdx) or Troubleshooting about large-list practical limits and the ETL-lookup alternative.

### Gap rank 176 (Medium, score 53.7) — WEEKOFYEAR / week numbering does not follow ISO-8601 and differs between Magic ETL and Beast Mode
- **What's missing:** Document WEEKOFYEAR/WEEK/YEARWEEK behavior, the mode parameter and what each mode does, default week start (Sunday), how it differs from ISO-8601, and the noted Magic ETL vs Beast Mode discrepancy.
- **Suggested location:** Add WEEKOFYEAR to the Functions Reference (s/article/360043429933.mdx) with a note on default Sunday week start, the WEEK/YEARWEEK mode parameter, ISO-8601 non-alignment, and the Magic ETL vs Beast Mode difference.

- **Other referenced articles:** s/article/360043430133.mdx

### Gap rank 246 (Medium, score 48.9) — Beast Mode ABS() with FIXED BY aggregation (absolute-value totals per group)
- **What's missing:** Document combining ABS() with SUM() and FIXED BY for a correct absolute-value total per group (e.g. ABS(SUM(budget - actual) FIXED (by category))) and clarify current ABS semantics (behavior reportedly changed mid-2025).
- **Suggested location:** Add an ABS-with-FIXED-BY worked example to s/article/4408174643607.mdx (FIXED Functions) or the Mathematical Transforms sample, clarifying per-group absolute-value totals.

- **Other referenced articles:** s/article/4408174643607.mdx

### Gap rank 326 (Low, score 42.1) — What SQL dialect Beast Mode / Domo uses
- **What's missing:** A prominent, easy-to-find statement that Beast Mode uses a MySQL-like dialect (and which functions are supported) to prevent repeated questions.
- **Suggested location:** Add a one-line statement to the top of the Functions Reference (s/article/360043429933.mdx) naming the MySQL-like dialect Beast Mode is based on.

- **Other referenced articles:** s/article/360043429953.mdx

---

## `s/article/360043430053.mdx`
*Beast Mode FAQs* — area: Beast Mode / Calculations

### Gap rank 192 (Medium, score 52.5) — Beast Mode division returning 0 / wrong value (aggregate before dividing)
- **What's missing:** Document clearly that division should wrap numerator and denominator in SUM() (SUM(a)/SUM(b)) rather than SUM(a/b) or a/b, why row-level division produces wrong aggregates, and the need for backticks plus percent formatting on the result.
- **Suggested location:** Add a short 'ratios and division' entry to Beast Mode FAQs (s/article/360043430053.mdx) and/or the Mathematical Transforms sample (s/article/360042925514.mdx): SUM(a)/SUM(b) pattern, why row-level division is wrong, plus formatting/backticks.

- **Other referenced articles:** s/article/000005559.mdx

---

## `s/article/360043437733.mdx`
*Domo CLI (Command Line Interface) Tool* — area: CLI / DomoStats / Datasets

### Gap rank 250 (Medium, score 48.6) — CLI activity logging and CLI/API dataset upsert-key removal on schema update
- **What's missing:** Explain how CLI actions appear in the Activity Log (and that they aren't distinctly tagged), how to manage/preserve upsert keys for CLI/API datasets, and the known behavior that a schema update can drop the upsert key without warning.
- **Suggested location:** Update the Domo CLI article (s/article/360043437733.mdx) with a behavior note: a schema/table update can silently drop the upsert key on CLI/API datasets (and how to preserve it), and how CLI actions surface in the Activity Log (not distinctly tagged). The separate-CLI-audit ask is a feature request.

---
