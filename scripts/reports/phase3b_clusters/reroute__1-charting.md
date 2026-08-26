# Phase 3b RE-ROUTE cluster: reroute__1-charting

These gaps were correctly skipped by earlier waves because the gap data mislinked them. Each is re-homed to its correct article below. Some target files were already edited in an earlier wave — read current state first and add ONLY the new gap's content.

Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links).

---

## `s/article/360043429793.mdx`
**Marker PM for this file:** Chris Wright

### Gap rank 115 (Medium, score 59.7) — Chart display limits and discoverability (scrollable bars, top-N + Other, data-label overlap, donut center total, dynamic headers)
- **Routing note:** Was mislinked to the Tables-properties article. This is 'Properties Available for Most Charts' — add Maximum Items top-N + rotate/overlap data labels + Trellis parts here; pie-specific Maximum Items/'Other'/donut-center goes to 360042925314.
- **What's missing:** Document Chart Properties options: Maximum Items (top-N with 'Other' bar and hiding it), data-label rotate/overlap settings, Hover Legend Position=Inside for donut center totals, Trellis categories for pseudo-scroll, and that dynamic column headers aren't natively supported (pivot-longer workaround).
- **Original suggested location:** Add task-oriented examples to s/article/360042925374.mdx (Chart Properties): top-N via Maximum Items with the 'Other' bar (and hiding it), data-label rotate/overlap, Hover Legend Position=Inside for donut center totals, and that native bars don't scroll (use Trellis or the App Store horizontal-bar Brick). Note dynamic column headers need a pivot-longer ETL workaround.

### Gap rank 120 (Medium, score 58.9) — Date-axis / time-scale behavior (forced datetime, Graph By, incomplete months, trellis fiscal)
- **Routing note:** Was mislinked to Tables. Add time-scale (Category Scale X) + Trellis date-settings content here.
- **What's missing:** Documentation on: dashboard/card time-scale setting (Default vs Day) and 'Never use time scale'; why DATE fields get coerced to datetime and using DATE()/DATE_FORMAT to force date; how Graph By interacts with filtering (wrong-date results); filtering out the incomplete current month (ELSE 0 creates spurious points vs NULL); a vertical line between actual and forecast; Trellis/Tiered Date Settings limits with custom fiscal calendars and on bullet charts.
- **Original suggested location:** Update s/article/360042925374.mdx (Chart Properties) date/time-scale section (or a dedicated date-axis troubleshooting article) to cover: time-scale Default vs Day and 'Never use time scale'; DATE coercion to datetime and DATE()/DATE_FORMAT fix; Graph By + filtering wrong-date behavior; filtering the incomplete current month (NULL vs 0); Trellis/Tiered Date Settings limits with fiscal calendars and bullet charts.

### Gap rank 178 (Medium, score 53.6) — Goal/target lines, scale markers, and average lines on charts
- **Routing note:** Was mislinked to Tables. Add Y-axis Goal / Scale Marker (static + dynamic goal line) content here.
- **What's missing:** Documentation of: Y-axis Goal setting vs Scale Marker for static goals, Beast Mode approach for a dynamic per-row/variable goal line, why a calculated average line won't render when a series is configured, projecting toward a variable target line, and multiple actual-vs-target progress bars with dynamic color.
- **Original suggested location:** Update the Chart Properties reference (s/article/360042925374.mdx) or relevant value-scale property article to clarify: Y-axis Goal vs Scale Marker for static goal lines, Beast Mode for a dynamic/variable goal line, and the documented gotcha that an average line won't render once a series is added.

---

## `s/article/360042925314.mdx`
**Marker PM for this file:** Chris Wright

### Gap rank 115 (Medium, score 59.7) — Chart display limits and discoverability (scrollable bars, top-N + Other, data-label overlap, donut center total, dynamic headers)
- **Routing note:** Pie-specific portion only: Maximum Items + 'Other' bucketing, donut center total via Legend Position=Inside.
- **What's missing:** Document Chart Properties options: Maximum Items (top-N with 'Other' bar and hiding it), data-label rotate/overlap settings, Hover Legend Position=Inside for donut center totals, Trellis categories for pseudo-scroll, and that dynamic column headers aren't natively supported (pivot-longer workaround).
- **Original suggested location:** Add task-oriented examples to s/article/360042925374.mdx (Chart Properties): top-N via Maximum Items with the 'Other' bar (and hiding it), data-label rotate/overlap, Hover Legend Position=Inside for donut center totals, and that native bars don't scroll (use Trellis or the App Store horizontal-bar Brick). Note dynamic column headers need a pivot-longer ETL workaround.

---

## `s/article/360043429473.mdx`
**Marker PM for this file:** Chris Wright

### Gap rank 323 (Low, score 42.6) — Pivot table expand/collapse breaks with HTML-link Beast Mode columns
- **Routing note:** Pivot Table chart-type article (was pointed at the aggregated-Beast-Mode article 000005559). Add the HTML-link-column expand/collapse limitation note here.
- **What's missing:** Document that Pivot Tables don't support HTML-link content and this breaks expand/collapse for affected columns.
- **Original suggested location:** Add a one-line limitation note to the Pivot Table chart-type article (Charting bucket) that HTML-link content isn't supported and breaks expand/collapse. Peripheral to Beast Mode/Variables.

---

## `s/article/360043437813.mdx`
**Marker PM for this file:** Chris Wright

### Gap rank 356 (Low, score 36.8) — Excel export formatting of pivot tables (column width, frozen panes)
- **Routing note:** Export Visualization Cards (was pointed at the Tables-properties article). Add pivot Excel-export column-width / frozen-panes guidance. NOTE: this file already got gaps 256/360 in Wave 2 — read current state, add only the 356 content.
- **What's missing:** Documentation should clarify whether column width or frozen-pane behavior can be controlled for pivot-table Excel exports (workarounds: 'Allow text to wrap', export as CSV) and document any limitations.
- **Original suggested location:** Update s/article/360043437813.mdx (Export Visualization Cards) with a note on pivot-table Excel-export formatting: that exported column widths/frozen panes are not directly controllable, and the practical workarounds ('Allow text to wrap' / 'Set column widths' in Properties for Tables 360042925374, or export as CSV).

---

## `s/article/360043428253.mdx`
**Marker PM for this file:** Chris Wright

### Gap rank 135 (Medium, score 57.4) — Moving sub-dashboards between parents and detaching from a parent
- **Routing note:** Manage Dashboards (was pointed at Beast Mode Manager). Add move/detach sub-dashboard between parents / to Top Level. NOTE: already got gap 334 in Wave 2 — add only 135 content.
- **What's missing:** Step-by-step (Admin > Dashboards > select > Edit > Move Dashboard > choose location/Top Level > permissions) and an explanation of what the 'Merge permissions' vs other permission options do during a dashboard move.
- **Original suggested location:** Update the dashboard/page admin-management article to add the Move Dashboard step-by-step (including detaching to Top Level) and define the permission options ('Merge permissions' vs alternatives) presented during a move.

---
