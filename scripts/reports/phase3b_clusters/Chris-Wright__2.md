# Phase 3b cluster: Chris-Wright__2

**Owning PM:** Chris Wright
**Files in this cluster:** 5  |  **Gaps:** 5

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360042924434.mdx`
*Comparative Gauge* — area: Charting & Analyzer

### Gap rank 213 (Medium, score 51.1) — Gauge / Multi-Value / Comparison card percent-change calculation and display
- **What's missing:** Document how Comparative Gauge / Multi-Value / Comparison cards compute % change (no divide-by-zero handling), how to display ratio-style values, why blank cards occur, and the 2-color limit on multi-value cards.
- **Suggested location:** Add % change formula / divide-by-zero / blank-from-aggregation / color-limit notes to the relevant gauge/multi-value/comparison chart-type article(s) under Charting. Outside the core Beast Mode/Variables scope of this bucket.

---

## `s/article/360042924594.mdx`
*Grouped and Stacked Bar with Line Chart* — area: Charting & Analyzer

### Gap rank 306 (Low, score 44.1) — Grouped + stacked / multi-level bar charts and trellis grouping
- **What's missing:** Documentation of how to approximate group+stack visualizations using trellis categories or combined beast-mode dimensions, and which chart types support trellis vs not (e.g., trellis unavailable on bullet charts).
- **Suggested location:** Add a note to the relevant bar-chart-type article(s) and/or a Trellis/charting reference clarifying how to approximate group+stack with trellis categories or concatenated Beast Mode dimensions, and which chart types support trellis (e.g., not bullet charts).

---

## `s/article/360042933054.mdx`
*Printing a Visualization Card* — area: Charting & Analyzer

### Gap rank 354 (Low, score 37.4) — Printing/exporting wide Mega Table cards (all columns on one page)
- **What's missing:** Documentation needed on Mega Table print/export behavior and workarounds: 'Allow Text to Wrap' to reduce column overflow, the Domo Google Sheets Add-On as a non-Excel export path, and limits on defining a print area.
- **Suggested location:** Update s/article/360042933054.mdx (Printing a Visualization Card): add a note that wide Mega Tables may split columns across print pages and that 'Allow text to wrap' / narrower 'Set column widths' / 'Hide columns' (linking to 360042925374 Properties for Tables) reduce overflow, and mention the Google Sheets Add-On (360043437913) as a non-Excel export path.

- **Other referenced articles:** s/article/360042925374.mdx, s/article/360043437913.mdx

---

## `s/article/360043428053.mdx`
*Stacked Bar with Line Chart* — area: Charting & Analyzer

### Gap rank 219 (Medium, score 50.5) — Combo / dual-axis bar+line chart configuration (Series on left scale, same/second scale)
- **What's missing:** Documentation on the 'Series on left scale' chart property (how the number controls how many measures show as lines vs bars), enabling dual/right-axis for selected series, putting bar and line on the same scale, Excel-style combo charts with mixed scales, and why switching a stacked bar to YOY/bar+line drops the series breakdown.
- **Suggested location:** Update the bar+line chart-type articles (e.g. s/article/360043428053.mdx) or the Chart Properties reference (s/article/360042925374.mdx) to explain the 'Series on left scale' property: how the number sets how many measures render as lines vs bars, how to push selected series to a right/second axis, and how to align bar and line on the same scale.

- **Other referenced articles:** s/article/360043429153.mdx, s/article/360042924594.mdx

---

## `s/article/360043428733.mdx`
*Sorting the Data in Your Chart* — area: Charting & Analyzer

### Gap rank 194 (Medium, score 52.3) — RANK / Top N within partition and Top N + Others in tables and grouped charts
- **What's missing:** Documentation on: why Top N / Limit Rows applies after the series split in grouped bar charts (ranks per-series instead of overall), the RANK() OVER(ORDER BY SUM(...)) workaround placed in Sorting/Filter, the Sort on Totals + Maximum Items chart properties for nested bars, that Domo doesn't support Top-N-within-partition natively (pre-process in ETL), and that RANK subtotals don't aggregate correctly in pivots.
- **Suggested location:** Update s/article/360043428733.mdx (Sorting the Data in Your Chart) or a Beast Mode samples article to document: Top N/Limit Rows applies after the series split in grouped charts, the RANK() OVER(ORDER BY SUM()) sort/filter workaround, Maximum Items + Sort on Totals for nested bars, and that Top-N-within-partition must be pre-computed in ETL.

- **Other referenced articles:** s/article/360043430133.mdx

---
