# PM Review Brief: Chris Wright

**Prepared for:** KB Restructure PM Review Meeting
**Features owned:** Analyzer, Charting, Doc Cards, Export to CSV, Mobile - iOS, Slideshows, Worksheets
**Total articles in your area:** 223

> This document is your meeting guide. It shows how your content is being reorganized,
> which AI-generated articles need your fact-check, which articles need a dedicated
> info-gathering meeting before they can be written, and what changes are being made
> to your content area in response to Support KB Audit and community forum gap findings.

---

## 1. How Your Content Is Being Reorganized

The KB is moving from a flat feature encyclopedia to a story-driven structure organized
around **11 pillars** (user workflows). The table below shows where each of your feature
areas lands in the new structure.

| Feature | Articles | New Location |
|---------|----------|--------------|
| Analyzer | 24 | Pillar 5: Analyze & Visualize |
| Charting | 173 | Pillar 5: Analyze & Visualize |
| Doc Cards | 12 | Pillar 5: Analyze & Visualize |
| Export to CSV | 5 | Pillar 5: Analyze & Visualize |
| Mobile - iOS | 6 | Pillar 1: Getting Started |
| Slideshows | 2 | Pillar 7: Share & Collaborate |
| Worksheets | 1 | Pillar 5: Analyze & Visualize |

### Notable Navigation Changes

- **'Build Your First Dashboard' (D4):** This tutorial currently lives in Getting Started. It should move to Analyze & Visualize > Dashboards & Pages. Confirm before moving.

---

## 2. AI-Generated Articles — Your Fact-Check Required

These articles will be synthesized by AI from existing KB content in Phase 3a.
**They need your review before publishing.** Please read the draft and verify the
key claims listed — especially anything about product behavior, limitations, or
recommended patterns.

| # | Article | Synthesized From | Key Claims to Verify |
|---|---------|------------------|---------------------|
| 1 | `What-is-a-Card.mdx` (Pillar 5) | Analyzer articles | Card types, Analyzer overview, card lifecycle, card vs dashboard distinction |
| 2 | `What-is-a-Dashboard.mdx` (Pillar 5) | Dashboard articles | Dashboard types, filter behavior, card organization, page vs app distinction |
| 3 | `Analyze-and-Visualize-Overview.mdx` (Pillar 5) | All Analyzer / chart / dashboard articles | Complete analysis toolbox overview, chart recommendation guidance |

---

## 3. New Forum-Gap Articles and Open Placeholders

New articles in your area from the community-forum gap analysis (and the original
restructure plan). Some are **already drafted and need your fact-check**; others
**cannot be written until you supply information**. The two are separated below so
it's clear which is which.

### 3a. PM Input Articles (from original restructure plan)

Not yet written — each needs a short info-gathering conversation before drafting.

| Article | What You Need to Provide |
|---------|--------------------------|
| `Domo-for-Mobile-Overview.mdx` — *Domo for Mobile Overview* | Confirm current iOS app feature scope: what can/can't be done vs web; roadmap awareness; any known limitations to document |

### 3b. Forum-Gap Articles Already Drafted — Fact-Check Required

These articles have been **written** in response to the highest-demand community
forum gaps. Please read each draft and verify accuracy. A ⚠️ flag means the draft
also contains an open `[pm-input]` placeholder — see Section 3d for the exact ask.

| Rank | Article | What Was Synthesized / What to Verify |
|------|---------|---------------------------------------|
| 114 | `Dynamic-Dropdowns-in-Table-Cards.mdx` — *Add In-Cell Controls or Write-Back to a Table Card* ⚠️ | Synthesized from 360043429573 (Table Charts) + pointers to 000005681, 4423762260375, 000005353, Workflows-Write-Data-Back. 1× `[pm-input]` Chris Wright: confirm the negative capability boundary (no in-cell dropdowns/write-back on standard table cards) |
| 172 | `Export-Domo-Data-to-Reports.mdx` — *Build Formatted and Static Reports from Domo Data* | Synthesized from 360043437813 (export) + 000005829 (Report Builder) + 360043437913 (Google Sheets); options-and-limits overview |

### 3c. Forum-Gap Articles Awaiting Your Input — Cannot Be Written Yet

These forum gaps **cannot be written without your input** — the KB has no source
material and the mechanics are Domo-proprietary. A short dedicated meeting (or an
async written answer) is needed before drafting can begin.

| Rank | Intended Article | What You Need to Supply |
|------|------------------|-------------------------|
| 21 | `Filter-Funnel-and-PDP-Shield-Icons.mdx` | Classic-dashboard + App Studio toggle paths/labels for filter and PDP icons, page-variable filter-icon behavior, whether PDP shield is a separate control |
| 22 | `Filter-Null-and-Empty-Values.mdx` | Analyzer filter behavior for null vs empty (IN, NOT IN, equals, is empty), whether NOT IN excludes nulls and if intended, the Beast Mode ISNULL/CASE workaround |
| 47 | `Troubleshoot-Cards-Not-Updating.mdx` | "Change Dataset" verification flow, dataset re-indexing latency, color-rule precedence (card vs dataset), filter/Beast Mode differences that make a card look stale |
| 71 | `Drill-to-Final-Data-Security.mdx` | "Drill to Final Data" toggle default state + security implication, `api/content/v1/cards` detection fields + auth, instance-wide audit, copy-to-embed behavior (distinct from drill-path prevention) |
| 107 | `Multi-Language-Dashboards.mdx` | Confirm a variable-driven CASE language switch renders as live switchable text, the AI Text Generation Magic ETL tile workflow, translated-label data-prep steps |
| 109 | `Custom-Card-Visuals-with-HTML-and-Bricks.mdx` | HTML/CONCAT recipes + hyperlink pitfalls, avatar endpoint support (`/api/content/v1/avatar/...`), table-with-bars via Flex/Faceted bar, in-cell dropdown via bricks confirmation |
| 244 | `Dataset-Level-Date-and-Fiscal-Calendar-Defaults.mdx` | Whether dataset-level date-range/fiscal-calendar defaults exist and how they flow to cards; the normal-vs-drill-path missing-field highlighting behavior |

### 3d. Open Article Placeholders — Your Answer Required

The items below are open `[pm-input]` placeholders where specific information from
you is needed before the content can be finalized. Each is a checkbox — check it
off once you've provided the answer.

- [ ] **`360042923914.mdx`**
  confirm multi-select Page Filters combine selected values with OR logic (no native AND option within a single column), and that the recommended workarounds are separate filters on different columns or a Beast Mode indicator column. synthesized from community forum reports; needs confirmation.

- [ ] **`360042923914.mdx`**
  confirm whether sharing a dashboard URL or bookmark with a specific Filter View applied reliably targets that view for the recipient (a workaround for the lack of per-user or per-group Filter View sharing). Synthesized from community forum reports; needs confirmation.

- [ ] **`360042923914.mdx`**
  confirm (1) whether a Beast Mode calculation created only in Analyzer on a single card is unavailable as a Page Filter column unless it is saved to the DataSet, and (2) the reported limit that a table card can be controlled by only one Page Filter at a time. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042923914.mdx`**
  confirm the current behavior and label of the per-card "Change Filter Exceptions" / "Allow global date" setting (whether an individual card can be exempted from a global date filter, and how), and whether, with interaction filters on, clicking a chart element now also self-filters the clicked card (a reported release-behavior change). Synthesized from community forum reports; needs confirmation.

- [ ] **`360042923914.mdx`**
  confirm the reported behavior change that a dashboard's date selector now requires "Allow global date filters" to be enabled to filter cards, when it previously worked without it. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042923914.mdx`**
  confirm whether a manual start/end date-entry range picker and a period-over-period configuration surfaced as a dashboard-level control are available natively, and document the recommended variable/App (Brick) approach for a custom start/end date-range control if one is supported. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042924034.mdx`**
  confirm whether card save comments and version-history entries surface in any Governance or DomoStats dataset for querying. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042924034.mdx`**
  confirm the exact rule Domo uses to auto-select the default date field on a new card, the precise steps to change the card's active date field when the DataSet has more than one date column, and that dataset owners cannot currently set a preferred default date field (open feature request). Synthesized from community forum reports; needs confirmation.

- [ ] **`360042924034.mdx`**
  forum gap (rank 93) asks for documentation of which card types support HTML/rich formatting (Notebook/Brick/App vs plain Text cards), summary-number font behavior, and Notebook card export limitations. This belongs in the dedicated Notebook Card articles (/s/article/360043430233 Adding a Notebook Card and /s/article/360042925654 Editing a Notebook Card), not in this Analyzer interface reference. Confirm the card-type formatting support and Notebook export behavior before documenting. synthesized from community forum reports; needs confirmation.

- [ ] **`360042924054.mdx`**
  confirm the Required Grants for opening Analyzer; no Required Grants section exists.

- [ ] **`360042924094.mdx`**
  confirm the following drill behaviors reported in the community forum: (1) on a table/grid drill, clicking a value cell behaves differently from clicking a category label and can produce an error; (2) a single card cannot both drill in place and apply a dashboard-wide filter, so the workaround is to split it into two cards; (3) there is no bulk action to copy a drill path from one card to many. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042924454.mdx`**
  confirm the exact precedence between a static SVG fill, the card color rules, and the chart's "No Data" color for a matched-but-unvalued region (does "No Data" override an SVG static fill, or vice versa?). Synthesized from community forum reports; needs confirmation.

- [ ] **`360042924594.mdx`**
  confirm the current list of chart types that do not support trellis categories (community reports cite bullet charts specifically). Synthesized from community forum reports; needs confirmation.

- [ ] **`360042925314.mdx`**
  confirm the exact control that pins the Hover Legend / total value inside the center of a Donut chart (reported as Legend Position = Inside), and whether it displays persistently or only on hover. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042932994.mdx`**
  confirm whether Domo offers a bulk or spreadsheet-based sharing option for granting access to many users or groups at once, and where it lives. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042932994.mdx`**
  confirm there is no UI option to auto-generate a shareable link for a filtered page or card view (reported as a feature request in the community forum). Synthesized from community forum reports; needs confirmation.

- [ ] **`360042934414.mdx`**
  confirm the Required Grants for company pages; no Required Grants section exists.

- [ ] **`360043428053.mdx`**
  confirm the exact behavior when converting a stacked bar chart to a YOY or bar+line combination chart (whether the stacked series breakdown is dropped, re-roled, or collapsed to a single bar). Synthesized from community forum reports; needs confirmation.

- [ ] **`360043428593.mdx`**
  confirm the Required Grants for deleting Cards from Domo; no Required Grants section exists.

- [ ] **`360043428613.mdx`**
  confirm the Required Grants for restricting Card edit capability; no Required Grants section exists.

- [ ] **`360043428713.mdx`**
  confirm the total/grand-total row behavior for tables and Pivot Tables: whether a total mirrors each column's own aggregation (for example, an averaged column producing an average of averages in the total) and the exact Beast Mode FIXED expression recommended to produce a summed total over an averaged column (reported as SUM(AVG(...) FIXED())). Synthesized from community forum reports; needs confirmation.

- [ ] **`360043428733.mdx`**
  confirm two community-reported specifics: (1) that a Top N / row limit applied to a grouped bar chart takes effect after the series split, so it ranks per-series rather than across the whole chart; and (2) the exact RANK() OVER(ORDER BY SUM(...)) Beast Mode sort/filter workaround, given that existing KB states Beast Mode does not support window functions. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043428813.mdx`**
  confirm the following synthesized limitations/workarounds: (1) a color rule cannot reference another column's value; (2) there is no native per-row heatmap and the recommended workaround is ETL normalization (and/or an HTML-table Beast Mode with CONCAT + inline color, or emoji/unicode indicators); (3) drill-path color follow-through requires the colored column to be present in the drill view. synthesized from community forum reports; needs confirmation.

- [ ] **`360043429293.mdx`**
  confirm which options (Divide value by/abbreviation, target, color, % display) apply to each gauge variant, and that showing value + target + % requires a multi-value gauge rather than the Single Value gauge. Multiple targets and Beast Mode-driven dynamic gauge color are not currently supported (feature requests). synthesized from community forum reports; needs confirmation.

- [ ] **`360043429473.mdx`**
  confirm that Pivot Tables do not support HTML-link content and that including an HTML-link (e.g., Beast Mode `<a>`) column breaks the expand/collapse behavior for the affected columns. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043429473.mdx`**
  confirm the following synthesized limitations: (1) measures in the Values region cannot be displayed as rows (values are columns only); (2) Beast Mode cannot produce new calculated pivot total/subtotal rows; (3) dynamic (unknown-column) pivoting requires a MySQL DataFlow or R/Python scripting tile rather than the native Magic ETL Pivot tile; (4) whether there is a supported way to hide empty columns in a Pivot Table. synthesized from community forum reports; needs confirmation.

- [ ] **`360043429473.mdx`**
  confirm and document the exact recipe for TTM/annualized financial columns in a Pivot Table (the Magic ETL month-index calculation and the Beast Mode expression that maps rows into trailing-twelve-month or annualized buckets). Synthesized from community forum reports; needs confirmation.

- [ ] **`360043429573.mdx`**
  a forum thread (rank 74) reports Domo staff confirming that HTML Tables are legacy/being phased out in favor of Mega, Pivot, and Flex tables. Confirm whether HTML Tables carry an official legacy/retirement status and whether it should be stated here. Also confirm period-over-period column configuration guidance for Flex Tables (belongs in /s/article/360043429073 Flex Table, not this article). synthesized from community forum reports; needs confirmation.

- [ ] **`360043429793.mdx`**
  confirm the recommended way to display more categories than fit on a native (non-scrolling) bar chart, including the exact App Store horizontal-bar Brick to use. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043429793.mdx`**
  confirm the supported ETL pattern (pivot-longer / unpivot) for driving dynamic column headers in a chart, and whether any native chart setting exists. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043429793.mdx`**
  confirm and document the following date-axis behaviors reported by community users: (1) the dashboard/card time-scale control (Default vs. Day) and how it relates to Never Use Time Scale; (2) why DATE fields are coerced to datetime on the axis and using DATE()/DATE_FORMAT in Beast Mode to force a pure date; (3) how Graph By interacts with filtering to produce wrong-date results; (4) filtering out the incomplete current month, and why an ELSE 0 in Beast Mode creates spurious zero points versus returning NULL; (5) adding a vertical divider line between actual and forecast data; (6) Tiered/Trellis Date Settings limits with custom fiscal calendars and on bullet charts. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043429793.mdx`**
  confirm the supported approach for a dynamic/per-row goal or target line built with Beast Mode (including projecting toward a variable target and rendering multiple actual-vs-target progress bars with dynamic color), and document the reported gotcha that a Calculated Line average will not render once an additional series is configured on the chart. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043430233.mdx`**
  confirm the current formatting-support matrix across card types (Notebook toolbar-only vs. Text plain vs. Bricks/App full HTML/CSS/JS vs. Image), that a Notebook Card does not accept hand-written HTML, and the exact behavior in which the body Font Size Picker does not restyle a dynamic Summary Number. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043430233.mdx`**
  confirm Notebook Card export behavior: whether a Notebook Card can be exported (PDF/PowerPoint/image) the way chart cards can, and any current limitation or enablement step. Reported as a forum gap; export-enable may be a feature request — needs confirmation.

- [ ] **`360043437813.mdx`**
  confirm where the per-card Excel export row-limit setting lives (e.g., Chart/Table Properties), its default and maximum values, and how a user raises it. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043437813.mdx`**
  confirm why the export row-limit setting is unavailable on certain card or view types, such as drill-through views. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043437813.mdx`**
  confirm how the "Warning: Not all the data is shown" / red header state maps to export completeness — that is, whether an export of that card contains all of the underlying data or only the portion the card displays. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043437813.mdx`**
  confirm whether column width or frozen-pane behavior can be controlled for Pivot Table Excel exports, and document any supported setting or the definitive limitation. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043437813.mdx`**
  confirm the exact PowerPoint file format produced by card and dashboard export (e.g., legacy .ppt vs. .pptx), so IT-policy-restricted users know before exporting. Synthesized from community forum reports; needs confirmation.

- [ ] **`4409575159191.mdx`**
  confirm the following limitations reported in the community forum: (1) the company-wide default landing page (set in Company Settings) applies only to the desktop web app and is not honored on mobile; (2) setting an App Studio app as a landing page and setting a workspace/App Studio home as a landing page are not currently supported (open feature requests). Synthesized from community forum reports; needs confirmation.

- [ ] **`4529227357975.mdx`**
  confirm the exact Date range Smart Text behavior when a card is not directly filtered (for example, whether it inherits a dashboard-level date filter or falls back to the card's saved range). Synthesized from community forum reports; needs confirmation.

- [ ] **`4529227357975.mdx`**
  confirm the recommended Beast Mode + Variable recipe for surfacing literal filtered start/end date values in a card title (e.g., which functions capture the applied date filter bounds). Synthesized from community forum reports; needs confirmation.

- [ ] **`7903767835031.mdx`**
  confirm the Smart Text card-title behavior for variables: does a variable token in a card title render only when a non-default value is selected (falling back to static text at the default value), and is that the intended behavior? Synthesized from community forum reports; needs confirmation.

- [ ] **`Dynamic-Dropdowns-in-Table-Cards.mdx`**
  confirm the capability boundary for this article: that a standard Analyzer table card supports only display, drill, and action-link behavior and does NOT support interactive in-cell input controls (dropdowns, editable cells) or write-back, and that App Framework / Bricks / a writeback connector is the required path for in-cell interactivity. State the boundary explicitly once confirmed.

- [ ] **`Use-Worksheets.mdx`**
  confirm the recommended decision criteria between Worksheets, Projects & Tasks, and App Studio editable tables for task-list / editable-tracker / CRM-style workflows, including: whether Projects & Tasks items can be powered by or tied to a DataSet, the current state of editable table components in App Studio (including Edit-in-Place for table components), and which option to recommend for each use case. Synthesized from community forum reports; needs confirmation.

---

## 4. Changes Flagged by Support Gap Integrations

Two gap-fill analyses have been integrated into the restructure plan. This section
shows what changes are planned in your content area and what fact-check input reduces
hallucination risk in the updated articles.

### 4a. Support KB Audit Findings (Phase 4)

_No Support KB Audit retirements are currently assigned to your area._

### 4b. Community Forum Gap Analysis — Update Targets

**High priority update targets** (9 articles in your area):

| Rank | Score | Topic | Affected Area | Specific Addition Needed |
|------|-------|-------|---------------|--------------------------|
| 16 | 73.5 | Period-over-period / Year-over-year comparison patterns and percent-change | Charting & Analyzer | A canonical PoP/YoY guide: why hardcoding YEAR()='2025' in Beast Modes breaks the native Choose Date |
| 54 | 66.2 | Analyzer / card feature requests with documentable current limits (filters, form | Analyzer | These are product feature requests. A few imply documentable current limitations (e.g. tooltip-field |
| 60 | 65.2 | Pivot table layout limitations and capabilities (values as rows/columns, totals, | Analyzer / Pivot Table | Largely feature requests, but documentation should cover what IS available today and key limitations |
| 68 | 64.6 | Conditional / cross-column color formatting, color-rule scope and per-card manag | Charting & Analyzer | Document the limitation (color rules can't reference another column and operate per-column not per-r |
| 70 | 64.5 | Multi-select filter AND logic vs OR logic | Dashboards - Filters | Documentation should state that multi-select filters use OR logic with no native AND option, and doc |
| 74 | 64.4 | HTML vs Mega vs Flex table card comparison and HTML-card legacy status | Charting & Analyzer / Tables | A comparison/decision guide of HTML vs Mega vs Flex (features, limits, color coding, scroll, sorting |
| 75 | 64.4 | Exporting dashboards/reports to PDF/PPT/Excel and scheduled-report feature gaps  | Dashboards / Scheduled Reports (Export & | Mostly feature requests, but documentable behaviors/limits: scheduled-report card attachments are CS |
| 85 | 62.8 | Gauge chart configuration and limitations (abbreviation, multi-value, targets, c | Charting & Analyzer / Gauges | Documentation of gauge options that exist (Divide value by > None to stop abbreviation; multi-value  |
| 93 | 61.9 | Text / Notebook card capabilities and formatting (HTML support, summary-number f | Charting & Analyzer / Text & Notebook Ca | Documentation clarifying which card types support HTML/rich formatting (notebook/brick/app/image vs  |

---

## Quick Actions Summary

A prioritized list of everything this document is asking of you:

| # | Action | Type | Est. Effort |
|---|--------|------|------------|
| 1 | Read and fact-check `What-is-a-Card.mdx` | Fact-check | 30–45 min |
| 2 | Read and fact-check `What-is-a-Dashboard.mdx` | Fact-check | 30–45 min |
| 3 | Read and fact-check `Analyze-and-Visualize-Overview.mdx` | Fact-check | 30–45 min |
| 4 | Provide input for `Domo-for-Mobile-Overview.mdx` | Info meeting | 30 min |
| 5 | Fact-check `Dynamic-Dropdowns-in-Table-Cards.mdx` (Rank 114 community request) | Fact-check | 20–30 min |
| 6 | Fact-check `Export-Domo-Data-to-Reports.mdx` (Rank 172 community request) | Fact-check | 20–30 min |
| 7 | Supply info to write `Filter-Funnel-and-PDP-Shield-Icons.mdx` (Rank 21) | Info meeting | 30 min |
| 8 | Supply info to write `Filter-Null-and-Empty-Values.mdx` (Rank 22) | Info meeting | 30 min |
| 9 | Supply info to write `Troubleshoot-Cards-Not-Updating.mdx` (Rank 47) | Info meeting | 30 min |
| 10 | Supply info to write `Drill-to-Final-Data-Security.mdx` (Rank 71) | Info meeting | 30 min |
| 11 | Supply info to write `Multi-Language-Dashboards.mdx` (Rank 107) | Info meeting | 30 min |
| 12 | Supply info to write `Custom-Card-Visuals-with-HTML-and-Bricks.mdx` (Rank 109) | Info meeting | 30 min |
| 13 | Supply info to write `Dataset-Level-Date-and-Fiscal-Calendar-Defaults.mdx` (Rank 244) | Info meeting | 30 min |
| 14 | **Open placeholder in `360042923914.mdx`:** confirm multi-select Page Filters combine selected values with OR logic (no nati | **Answer required** | 15–30 min |
| 15 | **Open placeholder in `360042923914.mdx`:** confirm whether sharing a dashboard URL or bookmark with a specific Filter View  | **Answer required** | 15–30 min |
| 16 | **Open placeholder in `360042923914.mdx`:** confirm (1) whether a Beast Mode calculation created only in Analyzer on a singl | **Answer required** | 15–30 min |
| 17 | **Open placeholder in `360042923914.mdx`:** confirm the current behavior and label of the per-card "Change Filter Exceptions | **Answer required** | 15–30 min |
| 18 | **Open placeholder in `360042923914.mdx`:** confirm the reported behavior change that a dashboard's date selector now requir | **Answer required** | 15–30 min |
| 19 | **Open placeholder in `360042923914.mdx`:** confirm whether a manual start/end date-entry range picker and a period-over-per | **Answer required** | 15–30 min |
| 20 | **Open placeholder in `360042924034.mdx`:** confirm whether card save comments and version-history entries surface in any Go | **Answer required** | 15–30 min |
| 21 | **Open placeholder in `360042924034.mdx`:** confirm the exact rule Domo uses to auto-select the default date field on a new  | **Answer required** | 15–30 min |
| 22 | **Open placeholder in `360042924034.mdx`:** forum gap (rank 93) asks for documentation of which card types support HTML/rich | **Answer required** | 15–30 min |
| 23 | **Open placeholder in `360042924054.mdx`:** confirm the Required Grants for opening Analyzer; no Required Grants section exi | **Answer required** | 15–30 min |
| 24 | **Open placeholder in `360042924094.mdx`:** confirm the following drill behaviors reported in the community forum: (1) on a  | **Answer required** | 15–30 min |
| 25 | **Open placeholder in `360042924454.mdx`:** confirm the exact precedence between a static SVG fill, the card color rules, an | **Answer required** | 15–30 min |
| 26 | **Open placeholder in `360042924594.mdx`:** confirm the current list of chart types that do not support trellis categories ( | **Answer required** | 15–30 min |
| 27 | **Open placeholder in `360042925314.mdx`:** confirm the exact control that pins the Hover Legend / total value inside the ce | **Answer required** | 15–30 min |
| 28 | **Open placeholder in `360042932994.mdx`:** confirm whether Domo offers a bulk or spreadsheet-based sharing option for grant | **Answer required** | 15–30 min |
| 29 | **Open placeholder in `360042932994.mdx`:** confirm there is no UI option to auto-generate a shareable link for a filtered p | **Answer required** | 15–30 min |
| 30 | **Open placeholder in `360042934414.mdx`:** confirm the Required Grants for company pages; no Required Grants section exists | **Answer required** | 15–30 min |
| 31 | **Open placeholder in `360043428053.mdx`:** confirm the exact behavior when converting a stacked bar chart to a YOY or bar+l | **Answer required** | 15–30 min |
| 32 | **Open placeholder in `360043428593.mdx`:** confirm the Required Grants for deleting Cards from Domo; no Required Grants sec | **Answer required** | 15–30 min |
| 33 | **Open placeholder in `360043428613.mdx`:** confirm the Required Grants for restricting Card edit capability; no Required Gr | **Answer required** | 15–30 min |
| 34 | **Open placeholder in `360043428713.mdx`:** confirm the total/grand-total row behavior for tables and Pivot Tables: whether  | **Answer required** | 15–30 min |
| 35 | **Open placeholder in `360043428733.mdx`:** confirm two community-reported specifics: (1) that a Top N / row limit applied t | **Answer required** | 15–30 min |
| 36 | **Open placeholder in `360043428813.mdx`:** confirm the following synthesized limitations/workarounds: (1) a color rule cann | **Answer required** | 15–30 min |
| 37 | **Open placeholder in `360043429293.mdx`:** confirm which options (Divide value by/abbreviation, target, color, % display) a | **Answer required** | 15–30 min |
| 38 | **Open placeholder in `360043429473.mdx`:** confirm that Pivot Tables do not support HTML-link content and that including an | **Answer required** | 15–30 min |
| 39 | **Open placeholder in `360043429473.mdx`:** confirm the following synthesized limitations: (1) measures in the Values region | **Answer required** | 15–30 min |
| 40 | **Open placeholder in `360043429473.mdx`:** confirm and document the exact recipe for TTM/annualized financial columns in a  | **Answer required** | 15–30 min |
| 41 | **Open placeholder in `360043429573.mdx`:** a forum thread (rank 74) reports Domo staff confirming that HTML Tables are lega | **Answer required** | 15–30 min |
| 42 | **Open placeholder in `360043429793.mdx`:** confirm the recommended way to display more categories than fit on a native (non | **Answer required** | 15–30 min |
| 43 | **Open placeholder in `360043429793.mdx`:** confirm the supported ETL pattern (pivot-longer / unpivot) for driving dynamic c | **Answer required** | 15–30 min |
| 44 | **Open placeholder in `360043429793.mdx`:** confirm and document the following date-axis behaviors reported by community use | **Answer required** | 15–30 min |
| 45 | **Open placeholder in `360043429793.mdx`:** confirm the supported approach for a dynamic/per-row goal or target line built w | **Answer required** | 15–30 min |
| 46 | **Open placeholder in `360043430233.mdx`:** confirm the current formatting-support matrix across card types (Notebook toolba | **Answer required** | 15–30 min |
| 47 | **Open placeholder in `360043430233.mdx`:** confirm Notebook Card export behavior: whether a Notebook Card can be exported ( | **Answer required** | 15–30 min |
| 48 | **Open placeholder in `360043437813.mdx`:** confirm where the per-card Excel export row-limit setting lives (e | **Answer required** | 15–30 min |
| 49 | **Open placeholder in `360043437813.mdx`:** confirm why the export row-limit setting is unavailable on certain card or view  | **Answer required** | 15–30 min |
| 50 | **Open placeholder in `360043437813.mdx`:** confirm how the "Warning: Not all the data is shown" / red header state maps to  | **Answer required** | 15–30 min |
| 51 | **Open placeholder in `360043437813.mdx`:** confirm whether column width or frozen-pane behavior can be controlled for Pivot | **Answer required** | 15–30 min |
| 52 | **Open placeholder in `360043437813.mdx`:** confirm the exact PowerPoint file format produced by card and dashboard export ( | **Answer required** | 15–30 min |
| 53 | **Open placeholder in `4409575159191.mdx`:** confirm the following limitations reported in the community forum: (1) the compa | **Answer required** | 15–30 min |
| 54 | **Open placeholder in `4529227357975.mdx`:** confirm the exact Date range Smart Text behavior when a card is not directly fil | **Answer required** | 15–30 min |
| 55 | **Open placeholder in `4529227357975.mdx`:** confirm the recommended Beast Mode + Variable recipe for surfacing literal filte | **Answer required** | 15–30 min |
| 56 | **Open placeholder in `7903767835031.mdx`:** confirm the Smart Text card-title behavior for variables: does a variable token  | **Answer required** | 15–30 min |
| 57 | **Open placeholder in `Dynamic-Dropdowns-in-Table-Cards.mdx`:** confirm the capability boundary for this article: that a standard Analyzer table | **Answer required** | 15–30 min |
| 58 | **Open placeholder in `Use-Worksheets.mdx`:** confirm the recommended decision criteria between Worksheets, Projects & Tasks,  | **Answer required** | 15–30 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
