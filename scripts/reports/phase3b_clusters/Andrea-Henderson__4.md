# Phase 3b cluster: Andrea-Henderson__4

**Owning PM:** Andrea Henderson
**Files in this cluster:** 5  |  **Gaps:** 7

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005541.mdx`
*DataSet Update Methods in Magic ETL* — area: Magic ETL / Dataset Update Methods

### Gap rank 174 (Medium, score 54.1) — Partition update method behavior in Magic ETL (row doubling, single-column key, retroactivity)
- **What's missing:** Explain (1) converting an existing Replace dataset to Partition leaves original data under a null key and doubles rows (start fresh); (2) Partition supports only one partition column (concatenate columns upstream into one key); (3) Magic ETL does not retroactively reprocess existing partitions when upstream formulas change.
- **Suggested location:** Add a Partition gotchas/notes section to s/article/000005541.mdx (DataSet Update Methods in Magic ETL): the Replace-to-Partition doubling and null-key behavior (start from a fresh dataset), single-partition-column limit with the upstream-concatenation workaround, and that existing partitions are not retroactively reprocessed on formula changes.

---

## `s/article/360042922974.mdx`
*Restrict Access to a SQL DataFlow* — area: SQL DataFlows / Governance

### Gap rank 182 (Medium, score 53.3) — Restricting/securing access to DataFlows (dataflow privacy lock)
- **What's missing:** Document that dataflow permissions derive from input-dataset sharing (no per-dataflow edit permission) and the existence/use of the 'Dataflow privacy' lock that restricts a dataflow to owners/admins.
- **Suggested location:** Confirm/expand s/article/360042922974.mdx (Restrict Access to a SQL DataFlow) to explicitly state permissions derive from input-dataset sharing and document the 'Dataflow privacy' lock; extend coverage to Magic ETL dataflows if applicable.

---

## `s/article/360042923014.mdx`
*Optimizing a SQL DataFlow* — area: SQL DataFlows

### Gap rank 197 (Medium, score 52.1) — SQL DataFlow performance optimization and Explain SQL availability
- **What's missing:** Document SQL DataFlow performance best practices (filter early, split transforms, avoid large cross joins, indexing limits, convert to Magic ETL) and when/why 'Explain SQL' is available vs greyed out (reportedly limited to certain engines like Redshift).
- **Suggested location:** Add an 'Explain SQL availability' note (engine-dependent, e.g. greyed out except certain engines) to s/article/360042923014.mdx (Optimizing a SQL DataFlow); confirm filter-early/convert-to-Magic-ETL guidance is present.

---

## `s/article/360044289573.mdx`
*Supported Functions in Magic ETL Reference Guide* — area: Magic ETL / Beast Mode (functions)

### Gap rank 204 (Medium, score 51.6) — ROUND() and STR_TO_DATE behavior differences between Magic ETL and Beast Mode
- **What's missing:** Note ROUND() rounding-mode differences between ETL and Beast Mode and STR_TO_DATE format-token support/limitations (e.g., %b workaround via mapping to full month + %M). Also includes a JP-reported Magic-ETL-vs-Beast-Mode HOUR() difference for >24h elapsed-time strings (e.g. '170:15' errors in ETL but returns 170 in Beast Mode; workaround: split string, hours*60+minutes).
- **Suggested location:** Add behavior notes to s/article/360044289573.mdx (Supported Functions in Magic ETL) for ROUND() rounding mode, HOUR() on >24h elapsed-time text (with split-string workaround), and STR_TO_DATE token limits — even though the unify requests are feature ideas, the differences are documentable gotchas.

### Gap rank 265 (Medium, score 47.5) — Counting category occurrences and distance/geo calculations (Beast Mode vs Magic ETL)
- **What's missing:** Show counting category occurrences (category to rows + to values with COUNT, or count bar chart) and document that distance/geo math (haversine) isn't available in Beast Mode but works in Magic ETL formula tiles.
- **Suggested location:** Note Beast-Mode-vs-Magic-ETL function availability (geo/distance math available in ETL formula tiles, not Beast Mode) in the function reference guides, and add a count-occurrences example. Could fold into the bucketing/counting how-to.

- **Other referenced articles:** s/article/360043429933.mdx

### Gap rank 272 (Medium, score 47.1) — Timezone handling in date/time functions (NOW/CURRENT_TIME return UTC; CONVERT_TZ support)
- **What's missing:** Document that built-in date/time functions return UTC, how to convert to local time, and the exact support status of CONVERT_TZ across contexts (Beast Mode, Magic ETL, SQL dataflow, connector SQL) — community got conflicting answers even though it works.
- **Suggested location:** Add a UTC/timezone note to the function reference guides (360044289573, 360043429933): NOW/CURRENT_TIME/CURRENT_TIMESTAMP return UTC, how to convert to local time, and the exact CONVERT_TZ support status by context.

- **Other referenced articles:** s/article/360043429933.mdx

---

## `s/article/360045485833.mdx`
*Magic ETL Tiles: Scripting* — area: Magic ETL Python tile / Jupyter Workspaces

### Gap rank 212 (Medium, score 51.2) — Calling external APIs / geocoding from Magic ETL Python tile vs Jupyter Workspaces
- **What's missing:** Document the Python tile's network/outbound-request limitations (cannot reliably call external APIs) and that Jupyter Workspaces is the supported place for API-driven enrichment like geocoding. Also note the security risk of pasting API keys into error output.
- **Suggested location:** Add a Note to the Magic ETL scripting-tile docs (s/article/360045485833.mdx or 4422644650519.mdx) stating the Python/R scripting tiles' outbound-network limitation for external API calls, and recommend Jupyter Workspaces for API-driven enrichment (geocoding). Confirm the exact current limitation with engineering before publishing.

- **Other referenced articles:** s/article/4422644650519.mdx

---
