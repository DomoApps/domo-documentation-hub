# PM Review Brief: Phil Fuchs

**Prepared for:** KB Restructure PM Review Meeting
**Features owned:** Beast Mode, Combined Schema, Data Center, Data Views, Fusions, Period over Period
**Total articles in your area:** 54

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
| Beast Mode | 18 | Pillar 5: Analyze & Visualize |
| Combined Schema | 1 | Pillar 4: Prepare & Transform Data |
| Data Center | 28 | Pillar 3: Manage Data |
| Data Views | 2 | Pillar 3: Manage Data |
| Fusions | 3 | Archive — DataFusion deprecated (retiring in Phase 4) |
| Period over Period | 2 | Pillar 5: Analyze & Visualize |

### Notable Navigation Changes

- **DataFusion/Fusions:** Fusions (DataFusion) articles are being archived in Phase 4. If any Beast Mode or Combined Schema articles reference DataFusion, they'll need updating.

- **Data Views (D9):** Data Views articles may shift between Pillar 3 (Manage Data) and Pillar 4 (Prepare & Transform Data) depending on D9 resolution.

---

## 2. AI-Generated Articles — Your Fact-Check Required

These articles will be synthesized by AI from existing KB content in Phase 3a.
**They need your review before publishing.** Please read the draft and verify the
key claims listed — especially anything about product behavior, limitations, or
recommended patterns.

| # | Article | Synthesized From | Key Claims to Verify |
|---|---------|------------------|---------------------|
| 1 | `What-is-Beast-Mode.mdx` (Pillar 5) | Beast Mode FAQs, functions reference | Beast Mode definition, when to use vs Magic ETL, aggregation rules, filter limitations |

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
| `Understanding-DataSet-Joins.mdx` — *Understanding DataSet Joins & Relationships* | Decision guidance: when to use ETL joins vs Data Models vs DataFlows; join semantics and performance tradeoffs |

### 3b. Forum-Gap Articles Already Drafted — Fact-Check Required

These articles have been **written** in response to the highest-demand community
forum gaps. Please read each draft and verify accuracy. A ⚠️ flag means the draft
also contains an open `[pm-input]` placeholder — see Section 3d for the exact ask.

| Rank | Article | What Was Synthesized / What to Verify |
|------|---------|---------------------------------------|
| 1 | `Beast-Mode-Window-Functions.mdx` — *Use Window Functions in Beast Mode* ⚠️ | Filter limitation FAQ has `[pm-input]` placeholder — Phil Fuchs to confirm workaround |
| 11 | `Beast-Mode-for-Spreadsheet-Users.mdx` — *Translate Spreadsheet Formulas to Beast Mode* | Synthesized from 360043430073 (Basic Transforms) + 360043430053 (Beast Mode FAQs); IF→CASE, SUMIF/COUNTIF→SUM(CASE), VLOOKUP→ETL join, no-stacking guidance |
| 49 | `Period-over-Period-Calculations.mdx` — *Compare Periods over Time in Beast Mode and DataFlows* | Synthesized from 360042923094 + 360042925494; prior-period flags, offset-join snapshot, rolling avg. Omitted unverifiable YEARWEEK/LAG year-boundary pitfalls |
| 118 | `Editor-Dataset-Access-Scope.mdx` — *Understand Dataset Access from Shared Cards and Dashboards* ⚠️ | Synthesized from 360042932994 + 360042935354 + 360042934614 + 360042924094 + 360042922974. 2× `[pm-input]` Phil Fuchs: Editor edit-vs-view scope on the implicit grant; whether a "Go To DataSet" card control exists |

### 3c. Forum-Gap Articles Awaiting Your Input — Cannot Be Written Yet

These forum gaps **cannot be written without your input** — the KB has no source
material and the mechanics are Domo-proprietary. A short dedicated meeting (or an
async written answer) is needed before drafting can begin.

| Rank | Intended Article | What You Need to Supply |
|------|------------------|-------------------------|
| 14 | `Dataset-Column-Rename-Impact.mdx` | Whether cards/filters/sorts bind to column name (case-sensitive?), that rename breaks refs silently, ETL/DataFlow ref breakage, whether a stable Column ID exists, the safe-rename workflow |
| 25 | `Card-Refresh-Timing-After-Dataset-Update.mdx` | Confirm cards have no settable refresh interval, dataset-update→index→display latency, the refresh API endpoint, any card cache/last-updated behavior |
| 33 | `Zero-Fill-Missing-Date-Gaps-in-Charts.mdx` | Magic ETL date-spine/cross-join recipe (which tiles), rendering a continuous date axis in Analyzer, retaining empty pivot rows |
| 56 | `Dataset-Column-Character-Limits.mdx` | Confirm text-column character limit (~1,024) and whether fixed, truncation-on-upload behavior, whether columns can be widened/deleted self-service, `set-dataset-column-width` CLI syntax |
| 64 | `Request-Access-Behavior.mdx` | What Request Access / Request More Access do (Buzz message and/or owner emails), Buzz-disabled behavior, where owners see/manage requests, per-card/role controls |
| 77 | `Time-Interval-Bucketing-and-Dedup.mdx` | The dedup recipe (window-count vs Group By + Join tile), the decision rule for moving from Beast Mode to Magic ETL, the 6-hour bucket approach |
| 91 | `Remove-Bad-Rows-from-a-Dataset.mdx` | Confirm no single-row delete + the republish/full-replace workaround, the CLI full-replace escaping conditions that create a malformed row, whether Workbench avoids it |
| 107 | `Multi-Language-Dashboards.mdx` | Confirm a variable-driven CASE language switch renders as live switchable text, the AI Text Generation Magic ETL tile workflow, translated-label data-prep steps |

### 3d. Open Article Placeholders — Your Answer Required

The items below are open `[pm-input]` placeholders where specific information from
you is needed before the content can be finalized. Each is a checkbox — check it
off once you've provided the answer.

- [ ] **`000005559.mdx`**
  confirm the exact current wording of the editor warning and that it is non-blocking (the Beast Mode still saves and the card still renders). Synthesized from recurring community forum reports where users read the message as a blocking error; wording and behavior need confirmation against the current release.

- [ ] **`360042925474.mdx`**
  confirm how Beast Mode metadata (specifically the data type) can be retrieved programmatically for governance reporting, reported to be the JSON connector endpoint GET /api/query/v1/functions/template/{beastmode}. Confirm the exact endpoint/path and which Governance connector or API exposes it. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042925474.mdx`**
  confirm the exact behavior when a card is moved/switched to a new DataSet: the "Merged from <datasource>" naming applied to carried-over Beast Modes, how this interacts with "save calculation to DataSet," and whether the merge/auto-rename can be prevented or managed. Provenance: synthesized from community forum reports; needs confirmation.

- [ ] **`360042926154.mdx`**
  confirm the now-shipped DataSet management options for this: (1) the "Duplicate DataSet" action (reported to be in the DataSet's three-dot menu) and exactly what it clones (schema only, or connector settings/scheduling); (2) the DataSet history "revert to this point" capability and whether it restores prior connector settings. Note: Schema Management's Clone explicitly does not copy connector settings or scheduling, so confirm how Duplicate DataSet differs. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042926194.mdx`**
  confirm the Required Grants for deleting DataSets; no Required Grants section exists.

- [ ] **`360042926214.mdx`**
  confirm the Required Grants for executing DataSets; no Required Grants section exists.

- [ ] **`360042934614.mdx`**
  Confirm the reported behavior that adding a user or group to a PDP policy (and/or enabling PDP on a DataSet) automatically grants those members access to the DataSet (auto-share). If confirmed, document the exact behavior here. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042934614.mdx`**
  Confirm whether PDP row and column policies are enforced across all the ways an App Studio app reads a PDP-controlled DataSet (for example, app variables, filters, and any direct DataSet queries), and document any App Studio-specific exceptions. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043429933.mdx`**
  confirm current ABS() semantics with aggregated / FIXED expressions; community reports indicate the behavior changed mid-2025. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043429933.mdx`**
  confirm the practical maximum length / value count for a Beast Mode IN-list (or overall expression), if one is enforced. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043429933.mdx`**
  confirm whether Beast Mode supports a thousands-separator / grouping function (such as MySQL FORMAT()) for inserting commas into numbers inside concatenated strings, and the exact supported syntax. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043429933.mdx`**
  confirm (1) the default week-start / mode for WEEK, YEARWEEK, and WEEKOFYEAR in Beast Mode and whether WEEKOFYEAR follows ISO-8601, and (2) the reported week-numbering discrepancy between Magic ETL and Beast Mode. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043430053.mdx`**
  confirm whether TIMESTAMPDIFF is supported in Beast Mode (it is not currently in the Functions Reference), and the recommended pattern for excluding business hours (not just weekend days) from an elapsed-time calculation. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043430053.mdx`**
  Confirm whether SUM() on a natively boolean-typed column (not a string) counts the true values directly in Beast Mode (i.e., whether Domo treats a boolean true as 1). Synthesized from community forum reports; needs confirmation.

- [ ] **`360043430133.mdx`**
  confirm whether a native window-function capability, or a dedicated window-functions KB article, is planned for Beast Mode; if so, link it here for the rolling/cumulative-series case. Synthesized from recurring community requests for rolling 12-month and running-total calculations; the "no window functions in Beast Mode" limitation is confirmed by the Beast Mode FAQs rolling-average answer.

- [ ] **`360043430153.mdx`**
  Confirm the reported table-cell vs. chart-tooltip rendering discrepancy for HTML-encoded characters, and that a card-level Beast Mode REPLACE may correct the value in table cells but not in chart tooltips (so normalizing in Magic ETL is the recommended fix). Synthesized from community forum reports; needs confirmation.

- [ ] **`360043437733.mdx`**
  confirm (1) the exact mechanism by which a schema/table update drops the upsert key on CLI/API DataSets and the supported way to preserve or re-apply it, and (2) how CLI actions are represented in the Activity Log (community reports indicate they are attributed to the authenticated user but not distinctly tagged as CLI). A separate CLI-specific audit log is a feature request. Synthesized from community forum reports; needs confirmation.

- [ ] **`360046074774.mdx`**
  confirm the precise same-type join rule for Views across storage types (Cloud Amplifier/Snowflake vs. standard Adrenaline DataSets), whether materialized and non-materialized Views behave differently for these joins, and the exact set of source combinations that are unsupported for join and for UNION. Synthesized from community forum reports; needs confirmation.

- [ ] **`360046074774.mdx`**
  confirm the SQL Editor switch is one-directional: that once a View uses the SQL Editor you cannot return to the visual Views Explorer builder for that View, and that calculated/Beast Mode columns must then be created in SQL. Also confirm the specific conditions that trigger the generic "Unable to save"/"issue during processing" error. Synthesized from community forum reports; needs confirmation.

- [ ] **`4408174643607.mdx`**
  confirm the recommended FIXED pattern for replacing COUNT(DISTINCT ...) / cross-row distinct aggregation, and whether it is officially supported. Provenance: synthesized from community forum reports; needs confirmation.

- [ ] **`7903767835031.mdx`**
  confirm whether variable logic must be removed from a Beast Mode before its associated control can be removed, and the exact behavior/error path when promoting an app that uses variables from dev to prod. Provenance: synthesized from community forum reports; needs confirmation.

- [ ] **`7903767835031.mdx`**
  confirm the current scope for surfacing a variable's selected value as dynamic text: which card elements (title, axis labels, legends, column headers) can reference it today, and whether formatting can follow the selected metric. Provenance: synthesized from community forum reports; needs confirmation.

- [ ] **`Beast-Mode-Window-Functions.mdx`**
  confirm the supported workaround for filtering on window function results. Options likely include materializing the calculation in Magic ETL before bringing into Analyzer, or restructuring logic to avoid the post-aggregation filter. Add workaround steps here and remove this note.

- [ ] **`Editor-Dataset-Access-Scope.mdx`**
  confirm the exact dataset-access scope an Editor receives from a shared card: does the implicit grant give the Editor edit/build access to the underlying DataSet, or view access only? Document the precise scope once confirmed.

- [ ] **`Editor-Dataset-Access-Scope.mdx`**
  confirm whether a viewer-facing "Go To DataSet" control exists on shared cards and, if so, which roles/grants expose it and how to disable it. No current KB article documents such a control; add a section once confirmed.

---

## 4. Changes Flagged by Support Gap Integrations

Two gap-fill analyses have been integrated into the restructure plan. This section
shows what changes are planned in your content area and what fact-check input reduces
hallucination risk in the updated articles.

### 4a. Support KB Audit Findings (Phase 4)

_No Support KB Audit retirements are currently assigned to your area._

### 4b. Community Forum Gap Analysis — Update Targets

**Critical update targets** (address alongside or immediately after Phase 3a):

| Rank | Article Area | Addition Needed | Fact-Check Info Needed |
|------|-------------|-----------------|------------------------|
| 5 | Beast Mode date functions | YTD/MTD/rolling N months patterns with worked examples | Verify date function examples are correct; confirm fiscal year behavior; review period boundary edge cases |
| 10 | Beast Mode reference | Aggregation context; grouping requirement; SUM(SUM(x)) pattern for subtotals | Verify aggregation examples; confirm SUM(SUM(x)) subtotal pattern behavior |

**High priority update targets** (10 articles in your area):

| Rank | Score | Topic | Affected Area | Specific Addition Needed |
|------|-------|-------|---------------|--------------------------|
| 30 | 69.6 | Apostrophe / HTML-encoded character rendering differs between table cells and ch | Dashboards / Beast Mode - Data quality | Document the table-vs-tooltip rendering discrepancy for HTML-encoded characters, the Magic ETL REPLA |
| 34 | 69.4 | Merged Beast Modes when moving cards to a new dataset | Beast Mode / Dataset management | Document how Beast Mode merging works when a card is moved/switched to a new dataset, the 'Merged fr |
| 38 | 68.7 | FIXED functions and filter interaction (share-of-total, % of revenue, market sha | Beast Mode / Calculations | Clearer FIXED examples for share-of-total scenarios: SUM(SUM(x)) FIXED(BY ...), why filtering out a  |
| 39 | 68.7 | Date parsing and formatting in Magic ETL / Beast Mode (STR_TO_DATE, DATE_FORMAT, | Magic ETL / Beast Mode (date functions) | Consolidated, example-rich reference: STR_TO_DATE/DATE_FORMAT masks must exactly match the source st |
| 52 | 66.5 | Distinct/conditional aggregation and GROUP_CONCAT (Magic ETL Group By vs Beast M | Magic ETL / Beast Mode (aggregation) | Clarify aggregation rules: Beast Mode cannot do cross-row distinct sums; the supported approach is t |
| 67 | 64.6 | Beast Mode CASE/COUNT syntax errors and 'a column does not exist' confusion | Beast Mode / Calculations | A consolidated syntax-troubleshooting reference: quote string literals so they aren't treated as col |
| 73 | 64.4 | Summing a boolean (true/false) column in Beast Mode | Beast Mode / Calculations | Short how-to: when SUM(`bool`) works, how booleans imported as strings behave, and MAX(CASE WHEN ... |
| 78 | 63.7 | Variable scope and control-propagation behavior (cross-dataset carry-over, uniqu | Beast Mode / Variables | Authoritative documentation of variable scope (instance-wide/global vs per-card/per-dataset effect), |
| 80 | 63.3 | Beast Mode AVG skewed by CASE...ELSE 0 (return NULL when averaging flagged/disti | Beast Mode / Calculations | A short best-practice note that ELSE 0 in a CASE breaks AVG (zeros are counted) and to omit the ELSE |
| 87 | 62.7 | Variable-driven toggles and dynamic number-format switching (MTD/YTD toggle, cur | Beast Mode / Variables | How-to on variable-driven toggles: CASE statements referencing a variable, applying the Beast Mode a |

---

## Quick Actions Summary

A prioritized list of everything this document is asking of you:

| # | Action | Type | Est. Effort |
|---|--------|------|------------|
| 1 | Read and fact-check `What-is-Beast-Mode.mdx` | Fact-check | 30–45 min |
| 2 | Provide input for `Understanding-DataSet-Joins.mdx` | Info meeting | 30 min |
| 3 | Fact-check `Beast-Mode-Window-Functions.mdx` (Rank 1 community request) | Fact-check | 20–30 min |
| 4 | Fact-check `Beast-Mode-for-Spreadsheet-Users.mdx` (Rank 11 community request) | Fact-check | 20–30 min |
| 5 | Fact-check `Period-over-Period-Calculations.mdx` (Rank 49 community request) | Fact-check | 20–30 min |
| 6 | Fact-check `Editor-Dataset-Access-Scope.mdx` (Rank 118 community request) | Fact-check | 20–30 min |
| 7 | Supply info to write `Dataset-Column-Rename-Impact.mdx` (Rank 14) | Info meeting | 30 min |
| 8 | Supply info to write `Card-Refresh-Timing-After-Dataset-Update.mdx` (Rank 25) | Info meeting | 30 min |
| 9 | Supply info to write `Zero-Fill-Missing-Date-Gaps-in-Charts.mdx` (Rank 33) | Info meeting | 30 min |
| 10 | Supply info to write `Dataset-Column-Character-Limits.mdx` (Rank 56) | Info meeting | 30 min |
| 11 | Supply info to write `Request-Access-Behavior.mdx` (Rank 64) | Info meeting | 30 min |
| 12 | Supply info to write `Time-Interval-Bucketing-and-Dedup.mdx` (Rank 77) | Info meeting | 30 min |
| 13 | Supply info to write `Remove-Bad-Rows-from-a-Dataset.mdx` (Rank 91) | Info meeting | 30 min |
| 14 | Supply info to write `Multi-Language-Dashboards.mdx` (Rank 107) | Info meeting | 30 min |
| 15 | **Open placeholder in `000005559.mdx`:** confirm the exact current wording of the editor warning and that it is non-block | **Answer required** | 15–30 min |
| 16 | **Open placeholder in `360042925474.mdx`:** confirm how Beast Mode metadata (specifically the data type) can be retrieved pr | **Answer required** | 15–30 min |
| 17 | **Open placeholder in `360042925474.mdx`:** confirm the exact behavior when a card is moved/switched to a new DataSet: the " | **Answer required** | 15–30 min |
| 18 | **Open placeholder in `360042926154.mdx`:** confirm the now-shipped DataSet management options for this: (1) the "Duplicate  | **Answer required** | 15–30 min |
| 19 | **Open placeholder in `360042926194.mdx`:** confirm the Required Grants for deleting DataSets; no Required Grants section ex | **Answer required** | 15–30 min |
| 20 | **Open placeholder in `360042926214.mdx`:** confirm the Required Grants for executing DataSets; no Required Grants section e | **Answer required** | 15–30 min |
| 21 | **Open placeholder in `360042934614.mdx`:** Confirm the reported behavior that adding a user or group to a PDP policy (and/o | **Answer required** | 15–30 min |
| 22 | **Open placeholder in `360042934614.mdx`:** Confirm whether PDP row and column policies are enforced across all the ways an  | **Answer required** | 15–30 min |
| 23 | **Open placeholder in `360043429933.mdx`:** confirm current ABS() semantics with aggregated / FIXED expressions; community r | **Answer required** | 15–30 min |
| 24 | **Open placeholder in `360043429933.mdx`:** confirm the practical maximum length / value count for a Beast Mode IN-list (or  | **Answer required** | 15–30 min |
| 25 | **Open placeholder in `360043429933.mdx`:** confirm whether Beast Mode supports a thousands-separator / grouping function (s | **Answer required** | 15–30 min |
| 26 | **Open placeholder in `360043429933.mdx`:** confirm (1) the default week-start / mode for WEEK, YEARWEEK, and WEEKOFYEAR in  | **Answer required** | 15–30 min |
| 27 | **Open placeholder in `360043430053.mdx`:** confirm whether TIMESTAMPDIFF is supported in Beast Mode (it is not currently in | **Answer required** | 15–30 min |
| 28 | **Open placeholder in `360043430053.mdx`:** Confirm whether SUM() on a natively boolean-typed column (not a string) counts t | **Answer required** | 15–30 min |
| 29 | **Open placeholder in `360043430133.mdx`:** confirm whether a native window-function capability, or a dedicated window-funct | **Answer required** | 15–30 min |
| 30 | **Open placeholder in `360043430153.mdx`:** Confirm the reported table-cell vs | **Answer required** | 15–30 min |
| 31 | **Open placeholder in `360043437733.mdx`:** confirm (1) the exact mechanism by which a schema/table update drops the upsert  | **Answer required** | 15–30 min |
| 32 | **Open placeholder in `360046074774.mdx`:** confirm the precise same-type join rule for Views across storage types (Cloud Am | **Answer required** | 15–30 min |
| 33 | **Open placeholder in `360046074774.mdx`:** confirm the SQL Editor switch is one-directional: that once a View uses the SQL  | **Answer required** | 15–30 min |
| 34 | **Open placeholder in `4408174643607.mdx`:** confirm the recommended FIXED pattern for replacing COUNT(DISTINCT  | **Answer required** | 15–30 min |
| 35 | **Open placeholder in `7903767835031.mdx`:** confirm whether variable logic must be removed from a Beast Mode before its asso | **Answer required** | 15–30 min |
| 36 | **Open placeholder in `7903767835031.mdx`:** confirm the current scope for surfacing a variable's selected value as dynamic t | **Answer required** | 15–30 min |
| 37 | **Open placeholder in `Beast-Mode-Window-Functions.mdx`:** confirm the supported workaround for filtering on window function results | **Answer required** | 15–30 min |
| 38 | **Open placeholder in `Editor-Dataset-Access-Scope.mdx`:** confirm the exact dataset-access scope an Editor receives from a shared card: do | **Answer required** | 15–30 min |
| 39 | **Open placeholder in `Editor-Dataset-Access-Scope.mdx`:** confirm whether a viewer-facing "Go To DataSet" control exists on shared cards a | **Answer required** | 15–30 min |
| 40 | Validate additions to: Beast Mode date functions (Rank 5) | Review | 20 min |
| 41 | Validate additions to: Beast Mode reference (Rank 10) | Review | 20 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
