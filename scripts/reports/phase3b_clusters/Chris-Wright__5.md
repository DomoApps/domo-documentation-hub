# Phase 3b cluster: Chris-Wright__5

**Owning PM:** Chris Wright
**Files in this cluster:** 1  |  **Gaps:** 4

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360042925374.mdx`
*Properties for Tables* — area: Dashboards / Chart properties

### Gap rank 115 (Medium, score 59.7) — Chart display limits and discoverability (scrollable bars, top-N + Other, data-label overlap, donut center total, dynamic headers)
- **What's missing:** Document Chart Properties options: Maximum Items (top-N with 'Other' bar and hiding it), data-label rotate/overlap settings, Hover Legend Position=Inside for donut center totals, Trellis categories for pseudo-scroll, and that dynamic column headers aren't natively supported (pivot-longer workaround).
- **Suggested location:** Add task-oriented examples to s/article/360042925374.mdx (Chart Properties): top-N via Maximum Items with the 'Other' bar (and hiding it), data-label rotate/overlap, Hover Legend Position=Inside for donut center totals, and that native bars don't scroll (use Trellis or the App Store horizontal-bar Brick). Note dynamic column headers need a pivot-longer ETL workaround.

- **Other referenced articles:** s/article/360042925314.mdx

### Gap rank 120 (Medium, score 58.9) — Date-axis / time-scale behavior (forced datetime, Graph By, incomplete months, trellis fiscal)
- **What's missing:** Documentation on: dashboard/card time-scale setting (Default vs Day) and 'Never use time scale'; why DATE fields get coerced to datetime and using DATE()/DATE_FORMAT to force date; how Graph By interacts with filtering (wrong-date results); filtering out the incomplete current month (ELSE 0 creates spurious points vs NULL); a vertical line between actual and forecast; Trellis/Tiered Date Settings limits with custom fiscal calendars and on bullet charts.
- **Suggested location:** Update s/article/360042925374.mdx (Chart Properties) date/time-scale section (or a dedicated date-axis troubleshooting article) to cover: time-scale Default vs Day and 'Never use time scale'; DATE coercion to datetime and DATE()/DATE_FORMAT fix; Graph By + filtering wrong-date behavior; filtering the incomplete current month (NULL vs 0); Trellis/Tiered Date Settings limits with fiscal calendars and bullet charts.

- **Other referenced articles:** s/article/360043428733.mdx

### Gap rank 178 (Medium, score 53.6) — Goal/target lines, scale markers, and average lines on charts
- **What's missing:** Documentation of: Y-axis Goal setting vs Scale Marker for static goals, Beast Mode approach for a dynamic per-row/variable goal line, why a calculated average line won't render when a series is configured, projecting toward a variable target line, and multiple actual-vs-target progress bars with dynamic color.
- **Suggested location:** Update the Chart Properties reference (s/article/360042925374.mdx) or relevant value-scale property article to clarify: Y-axis Goal vs Scale Marker for static goal lines, Beast Mode for a dynamic/variable goal line, and the documented gotcha that an average line won't render once a series is added.

### Gap rank 356 (Low, score 36.8) — Excel export formatting of pivot tables (column width, frozen panes)
- **What's missing:** Documentation should clarify whether column width or frozen-pane behavior can be controlled for pivot-table Excel exports (workarounds: 'Allow text to wrap', export as CSV) and document any limitations.
- **Suggested location:** Update s/article/360043437813.mdx (Export Visualization Cards) with a note on pivot-table Excel-export formatting: that exported column widths/frozen panes are not directly controllable, and the practical workarounds ('Allow text to wrap' / 'Set column widths' in Properties for Tables 360042925374, or export as CSV).

- **Other referenced articles:** s/article/360043437813.mdx

---
