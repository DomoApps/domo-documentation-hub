# Phase 3b cluster: Chris-Wright__6

**Owning PM:** Chris Wright
**Files in this cluster:** 4  |  **Gaps:** 9

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360042923914.mdx`
*Page Filters and Filter Views on Dashboards* — area: Dashboards / Filters

### Gap rank 141 (Medium, score 56.8) — Dashboard filter behavior and limitations (legend click excludes, OR/contains, one-filter-per-table-card, filter-view priority)
- **What's missing:** Documentation of dashboard filter behaviors and limits with workarounds: why click-to-filter excludes the value (and how to invert); that page filters support only literal values (no contains/OR) plus the Beast Mode workaround; the one-filter-per-table-card limitation; that Filter Views key off the first card's dataset.
- **Suggested location:** Mostly feature requests but with stable documentable limits. Add a 'Filter behavior and limitations' note to s/article/360042923914.mdx: click-to-filter excludes (how to invert); page filters take literal values only (no contains/OR) with Beast Mode workaround; table cards control one filter at a time; Filter Views key off the first card's dataset.

### Gap rank 153 (Medium, score 55.8) — Page/card filter scoping, exceptions, and locked default selections
- **What's missing:** Documentation on: 'Change Filter Exceptions' / Allow global date per card; that you cannot make an arbitrary dataset column non-filterable (workaround: rename it in a Dataset View used by that card); that filter views can pre-select but not lock a value (no native required filter; Beast Mode default workaround); paired/page-level filters across two datasets with differently named key fields.
- **Suggested location:** Update s/article/360042923914.mdx (Page Filters and Filter Views on Dashboards) to add filter-scoping limitations and workarounds: Change Filter Exceptions / per-card global date; you cannot make a column non-filterable (rename in a Dataset View); filter views can pre-select but not lock a value; paired filters require matching field names (workaround for differently named keys).

### Gap rank 184 (Medium, score 53.2) — Date selector / global date filter not filtering cards
- **What's missing:** Document prerequisites for date-selector filters: the 'Allow global date filters' toggle must be enabled; date-range-hidden / filter-exception settings; filter and target cards must share an identically-named true-date-type column. Several threads show the 'turn on global date filters' fix that previously wasn't required.
- **Suggested location:** Update s/article/360042923914.mdx (Page Filters and Filter Views) with a 'Date selector not filtering cards' troubleshooting checklist: enable 'Allow global date filters', confirm filter exceptions, ensure filter and target cards share an identically named true-date-type column, and note the behavior change that now requires the global date toggle.

### Gap rank 237 (Medium, score 49.5) — Cross-dataset filtering and quick-filter scope
- **What's missing:** Documentation should explain that filter cards only act on their own dataset (cards must share an identically-named column or a merged view), that calculated fields used for filtering must exist at dataset level (not card level), and that there's no native way to apply a quick filter to many existing cards at once (page filter / Save As propagation workarounds).
- **Suggested location:** Update s/article/360042923914.mdx (Page Filters and Filter Views): add a 'How filters resolve across datasets' note — filter/page filters require an identically-named (or merged-view) column across cards, calculated fields used for filtering must exist at the dataset level, and there is no native bulk quick-filter-across-existing-cards (page filter / Save As propagation workarounds).

### Gap rank 276 (Medium, score 46.9) — Interaction-filter behavior change (clicked card now self-filters; page filters reset)
- **What's missing:** Clarify whether the clicked-card-self-filtering on interaction is intentional, document current interaction-filter behavior and any toggle.
- **Suggested location:** Once the intended behavior is confirmed, document current interaction-filter behavior (whether the clicked card self-filters and any toggle) in s/article/360042923914.mdx. Low views; primarily a release-behavior clarification.

### Gap rank 305 (Low, score 44.2) — Flexible date-range selection and period-over-period controls on dashboards
- **What's missing:** Feature requests, but documentable today: the current limits of card-level date selectors vs the global Dynamic Date Range Filter and page-level PoP config, and how to build flexible date-range selection using variables/Bricks (commenters share a custom date-range brick approach).
- **Suggested location:** Update s/article/360042923914.mdx (Page Filters and Filter Views on Dashboards): add a section clarifying the current limits of card-level date selectors vs the global Dynamic Date Range Filter and the page-level PoP configuration, and document the variable/Brick approach for a manual start/end custom date-range control as an interim workaround. Note PoP-as-dashboard-control and manual-entry range picker are not yet native.

---

## `s/article/360043428713.mdx`
*Applying DataSet Columns to Your Chart* — area: Dashboards / Tables / Pivot

### Gap rank 236 (Medium, score 49.5) — Table/pivot aggregation behavior (No Aggregation cascade, row-count discrepancy, average total row)
- **What's missing:** Document that No Aggregation is equivalent to adding the field to GROUP BY (cascades to all columns), how aggregation settings cause row-count discrepancies, and that the Total Row uses the same aggregation as the column (with the SUM(AVG() FIXED()) workaround for summed totals over averaged columns).
- **Suggested location:** Add an aggregation-behavior note to s/article/360043428713.mdx (Applying DataSet Columns to Your Chart) or the Table Charts article: No Aggregation == add to GROUP BY (cascades), how it changes row counts, and that the Total Row mirrors column aggregation (SUM(AVG() FIXED()) workaround for summed totals over averaged columns).

---

## `s/article/360043429473.mdx`
*Pivot Table* — area: Reporting / Pivot Tables

### Gap rank 270 (Medium, score 47.2) — Pivot table issues: 'multiple results' error, TTM/financial layouts, bulk value swaps
- **What's missing:** Document the cause of the pivot 'multiple results' warning (more than one record per row/column combo, often a FIXED Beast Mode or pill filter) and how to resolve it; provide a recipe for TTM/annualized financial columns via Magic ETL month-index; and clarify there is no native bulk edit to swap a value column across cards.
- **Suggested location:** Update s/article/360043429473.mdx (Pivot Table): expand the existing 'Multiple results' note with the broader cause (more than one record per row/column combination, often from an unaggregated/FIXED Beast Mode or pill filter) and resolution steps. TTM/annualized layouts are better suited to a Beast Mode/Magic ETL recipe (could be an FAQ addition); state plainly that there is no native bulk edit to swap a value column across multiple pivot cards.

---

## `s/article/360043439893.mdx`
** — area: Dashboards / Filters & Permissions

### Gap rank 185 (Medium, score 53.2) — Sharing filter views with specific users/groups (and sorting filter views)
- **What's missing:** Primarily a feature request. Documentation could clarify current filter-view sharing behavior and permissions (today: share with no one or everyone; sharing requires admin/Manage All Cards) and the URL/bookmark workaround for targeting a specific page-analyzer view.
- **Suggested location:** Update the filter-views documentation to clarify the current sharing model (you can share with everyone or no one; sharing requires admin / Manage All Cards & Pages) and the URL/bookmark workaround for targeting a specific analyzer view. Core ask (share with specific users/groups, sort views) stays a feature request.

---
