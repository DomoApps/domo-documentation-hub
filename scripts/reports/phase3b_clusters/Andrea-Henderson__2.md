# Phase 3b cluster: Andrea-Henderson__2

**Owning PM:** Andrea Henderson
**Files in this cluster:** 5  |  **Gaps:** 7

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005809.mdx`
** — area: Magic ETL (SQL tile)

### Gap rank 221 (Medium, score 50.4) — Magic ETL SQL tile supported functions and limitations (PERCENTILE_CONT, recursive CTEs, exposing SQL)
- **What's missing:** Surface/expand the SQL-tile supported-functions reference: explicitly list unsupported items (PERCENTILE_CONT, recursive CTEs, temp tables), explain CTE caveats, and document that Magic ETL does not expose generated SQL (the SQL action is translated into a graph of simpler actions, not the reverse).
- **Suggested location:** Add an explicit 'Unsupported in the SQL tile' list and a note that generated SQL is not exposed to s/article/000005809.mdx (SQL Expressions in Magic ETL); cross-link from the Supported Functions guide.

- **Other referenced articles:** s/article/360044289573.mdx

---

## `s/article/360042923414.mdx`
*Creating a Rank or Row Count* — area: Magic ETL (Rank & Window tile)

### Gap rank 251 (Medium, score 48.6) — Rank & Window tile partitioning (ties on latest date, sequential rank on change)
- **What's missing:** Document how to add columns to the partition to keep all ties (e.g., all plans on latest EFFDT), why a single row-number filter drops ties, and that ranking-on-change requires an explicit grouping/partition column (implied row order isn't enough).
- **Suggested location:** Extend s/article/360042923414.mdx (Creating a Rank or Row Count) with partition examples: keep all ties on a latest-date by partitioning, why row-number filters drop ties, and ranking-on-change with an explicit partition column.

---

## `s/article/360044876614.mdx`
*Magic ETL Tiles: Filter* — area: Magic ETL (Filter tile)

### Gap rank 249 (Medium, score 48.8) — Filtering on large value lists and removing future/past dates in Magic ETL
- **What's missing:** Document Filter-tile patterns: filtering against many values by joining a reference dataset (inner join to keep) vs Add Formula Rule with NOT IN, and the reliable date pattern DATE(field) < CURRENT_DATE().
- **Suggested location:** Add example patterns to s/article/360044296573.mdx (Writing a Filter Formula in Magic ETL): NOT IN for value lists, join-as-filter against a reference dataset, and DATE(field) comparisons for reliably removing future/past dates.

- **Other referenced articles:** s/article/360044296573.mdx

### Gap rank 286 (Medium, score 46.2) — Magic ETL date-filter calendar input (typing discarded; calendar shortcuts) [JP]
- **What's missing:** Note the calendar shortcut (click the month/year header to jump to month/year/decade lists) and the script-rule alternative for date filters.
- **Suggested location:** Add a tip to s/article/360044876614.mdx (Magic ETL Tiles: Filter): the calendar header-click shortcut for jumping to month/year/decade, and that the formula filter (360044296573) can compare dates directly.

- **Other referenced articles:** s/article/360044296573.mdx

---

## `s/article/360044951294.mdx`
*Magic ETL Tiles: Pivot* — area: Magic ETL (Pivot tile)

### Gap rank 188 (Medium, score 52.8) — Pivot tile behavior in Magic ETL (grain/row-identifier requirement, losing rows, dummy column)
- **What's missing:** Pivot tile docs should explain pre-aggregating to the post-pivot grain (Group By before Pivot) to avoid collapsed rows/shifted totals, why a row-identifier column is required and the add-a-constant-column workaround, and that post-pivot variance calcs follow the same aggregation rules.
- **Suggested location:** Add a 'Common pitfalls' section to s/article/360044951294.mdx (Magic ETL Tiles: Pivot): pre-aggregate to grain before pivoting, the row-identifier requirement and constant-column workaround, and why extra columns change totals.

### Gap rank 217 (Medium, score 50.6) — Reshaping wide/columnar data for charting (years/metrics as columns)
- **What's missing:** A how-to that explains the unpivot/reshape pattern (Magic ETL Dynamic Unpivot or cross-join) needed when years or metrics are stored as separate columns, and which native cards (pivot table) can consume wide data as-is. Recurring confusion: users expect to add multiple columns to one axis.
- **Suggested location:** Add a short how-to (or augment an existing Analyzer/charting KB article in s/article/) explaining: when years/metrics are separate columns you must unpivot first (link the Magic ETL Dynamic Unpivot tile docs), and that a pivot table card can consume wide data as-is. Low individual views but a recurring all-unanswered pattern.

- **Other referenced articles:** s/article/360047787514.mdx

---

## `s/article/4422644650519.mdx`
*Magic ETL Scripting Tile Environments* — area: Magic ETL (Python tile)

### Gap rank 309 (Low, score 43.6) — Python tile: dynamic pivoted-column output schema and Python environment/library availability
- **What's missing:** Document how the Python tile output schema works for dynamic columns ('Remove All Columns' vs manual + downstream Alter Columns), and the Python tile Environment selector — what each environment provides and which libraries are available.
- **Suggested location:** Expand s/article/4422644650519.mdx / 000005117 (Scripting Tile Environments) with per-environment library availability, and add to s/article/360045485833.mdx (Magic ETL Tiles: Scripting) how to output dynamically-generated columns ('Remove All Columns' + downstream Alter Columns).

- **Other referenced articles:** s/article/360045485833.mdx, s/article/000005117.mdx

---
