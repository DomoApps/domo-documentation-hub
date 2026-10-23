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
around **12 pillars** (user workflows). The table below shows where each of your feature
areas lands in the new structure.

| Feature | Articles | New Location |
|---------|----------|--------------|
| Analyzer | 24 | Pillar 5: Analyze & Visualize |
| Charting | 173 | Pillar 5: Analyze & Visualize |
| Doc Cards | 12 | Pillar 5: Analyze & Visualize |
| Export to CSV | 5 | Pillar 5: Analyze & Visualize |
| Mobile - iOS | 6 | Pillar 1: Getting Started |
| Slideshows | 2 | Pillar 7: Distribute |
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

- [ ] **`4529227357975.mdx`**
  confirm the exact Date range Smart Text behavior when a card is not directly filtered (for example, whether it inherits a dashboard-level date filter or falls back to the card's saved range). Synthesized from community forum reports; needs confirmation.

- [ ] **`4529227357975.mdx`**
  confirm the recommended Beast Mode + Variable recipe for surfacing literal filtered start/end date values in a card title (e.g., which functions capture the applied date filter bounds). Synthesized from community forum reports; needs confirmation.

- [ ] **`7903767835031.mdx`**
  confirm the Smart Text card-title behavior for variables: does a variable token in a card title render only when a non-default value is selected (falling back to static text at the default value), and is that the intended behavior? Synthesized from community forum reports; needs confirmation.

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
| 14 | **Open placeholder in `360043437813.mdx`:** confirm where the per-card Excel export row-limit setting lives (e | **Answer required** | 15–30 min |
| 15 | **Open placeholder in `360043437813.mdx`:** confirm why the export row-limit setting is unavailable on certain card or view  | **Answer required** | 15–30 min |
| 16 | **Open placeholder in `360043437813.mdx`:** confirm how the "Warning: Not all the data is shown" / red header state maps to  | **Answer required** | 15–30 min |
| 17 | **Open placeholder in `360043437813.mdx`:** confirm whether column width or frozen-pane behavior can be controlled for Pivot | **Answer required** | 15–30 min |
| 18 | **Open placeholder in `360043437813.mdx`:** confirm the exact PowerPoint file format produced by card and dashboard export ( | **Answer required** | 15–30 min |
| 19 | **Open placeholder in `4529227357975.mdx`:** confirm the exact Date range Smart Text behavior when a card is not directly fil | **Answer required** | 15–30 min |
| 20 | **Open placeholder in `4529227357975.mdx`:** confirm the recommended Beast Mode + Variable recipe for surfacing literal filte | **Answer required** | 15–30 min |
| 21 | **Open placeholder in `7903767835031.mdx`:** confirm the Smart Text card-title behavior for variables: does a variable token  | **Answer required** | 15–30 min |
| 22 | **Open placeholder in `Use-Worksheets.mdx`:** confirm the recommended decision criteria between Worksheets, Projects & Tasks,  | **Answer required** | 15–30 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
