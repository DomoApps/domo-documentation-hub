# PM Review Brief: Andrea Henderson

**Prepared for:** KB Restructure PM Review Meeting
**Features owned:** Auto ML, Data Flows, Magic ETL
**Total articles in your area:** 84

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
| Auto ML | 3 | Pillar 4: Prepare & Transform Data |
| Data Flows | 28 | Pillar 4: Prepare & Transform Data |
| Magic ETL | 53 | Pillar 4: Prepare & Transform Data |

### Notable Navigation Changes

- **DataFusion retirement:** The 4 EN DataFusion articles are staged for Retired in Phase 4.6. Replacement SHIPPED: `DataFusion-Migration-Guide.mdx` (points users to Magic ETL equivalents) — please fact-check it for accuracy.

- **Old Magic ETL tile articles (7):** 7 EN old-tile-interface articles staged for Retired. 1 article (`360043428113` Create a Recursive/Snapshot Old Magic ETL DataFlow) is explicitly kept.

---

## 2. AI-Generated Articles — Your Fact-Check Required

These articles will be synthesized by AI from existing KB content in Phase 3a.
**They need your review before publishing.** Please read the draft and verify the
key claims listed — especially anything about product behavior, limitations, or
recommended patterns.

| # | Article | Synthesized From | Key Claims to Verify |
|---|---------|------------------|---------------------|
| 1 | `What-is-Magic-ETL.mdx` (Pillar 4) | Magic ETL overview articles | Magic ETL capabilities, when to use vs SQL DataFlows, 400k preview row limit |
| 2 | `What-is-a-DataFlow.mdx` (Pillar 4) | DataFlow articles | DataFlow types (SQL, Python, R), when to use each vs Magic ETL |
| 3 | `Prepare-and-Transform-Overview.mdx` (Pillar 4) | All ETL / DataFlow / DataSet articles | Full data prep toolbox, positioning of each tool, credit/consumption model accuracy |

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
| `How-Data-Flows-Through-Domo.mdx` — *How Data Flows Through Domo* | Canonical end-to-end pipeline narrative; confirm how connect → prepare → analyze → share → govern is described; sign off on framing |
| `Choosing-the-Right-Data-Prep-Tool.mdx` — *Choosing the Right Data Prep Tool* | Positioning: when to use Magic ETL vs SQL DataFlow vs Python/R vs Data Models; official recommendation matrix |

### 3b. Forum-Gap Articles Already Drafted — Fact-Check Required

These articles have been **written** in response to the highest-demand community
forum gaps. Please read each draft and verify accuracy. A ⚠️ flag means the draft
also contains an open `[pm-input]` placeholder — see Section 3d for the exact ask.

| Rank | Article | What Was Synthesized / What to Verify |
|------|---------|---------------------------------------|
| 117 | `Split-Multi-Value-Fields-into-Rows.mdx` — *Split a Delimited Field into Multiple Rows in Magic ETL* | Synthesized from 360045402873 (Text tile) + 360044951294 (Unpivot); two-step Split Column → Dynamic Unpivot recipe |
| 299 | `Handle-Source-Schema-Drift-in-Connectors.mdx` — *Handle Changing Source Headers and Date Formats in Magic ETL* ⚠️ | Synthesized from 000005809 (FUZZY_PARSE_DATE), 000005408 (SFTP Generate Header Row / Start Row Scheme), 360044876874 (Select Columns tile). No `[pm-input]` — fully synthesizable (was rank-299 DEFER, promoted to written after 2026-08-26 coverage research) |

### 3c. Forum-Gap Articles Awaiting Your Input — Cannot Be Written Yet

These forum gaps **cannot be written without your input** — the KB has no source
material and the mechanics are Domo-proprietary. A short dedicated meeting (or an
async written answer) is needed before drafting can begin.

| Rank | Intended Article | What You Need to Supply |
|------|------------------|-------------------------|
| 57 | `Pivot-Table-Census-Calendar-Join.mdx` | How to build a date-spine DataSet, the BETWEEN-join tile config in Magic ETL, DATE_FORMAT month grouping, default end-date handling for open intervals |
| 61 | `Plot-Two-Date-Columns-on-One-Axis.mdx` | Magic ETL steps to unpivot/union two date columns into one shared column (which tiles), Analyzer line+bar combo-chart setup on the reshaped output |
| 62 | `Data-Allocation-Split-Credit-in-ETL.mdx` | How to structure an allocation/split table with effective-date ranges, the Join-tile fan-out config, the value × split % calculation step |
| 77 | `Time-Interval-Bucketing-and-Dedup.mdx` | The dedup recipe (window-count vs Group By + Join tile), the decision rule for moving from Beast Mode to Magic ETL, the 6-hour bucket approach |

### 3d. Open Article Placeholders — Your Answer Required

The items below are open `[pm-input]` placeholders where specific information from
you is needed before the content can be finalized. Each is a checkbox — check it
off once you've provided the answer.

- [ ] **`000005150.mdx`**
  confirm the exact preview row-sampling limit per input (reported in the community as roughly 400,000 rows) so it can be stated precisely here, and confirm the filtered-DataSet-View-as-input workaround is the recommended testing approach.

- [ ] **`000005541.mdx`**
  confirm the exact behavior when an existing Replace/Append DataSet is switched to Partition (community reports that pre-existing rows are retained under a null/empty partition and that row counts double). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005741.mdx`**
  confirm the exact reason an AI Forecasting DataFlow can succeed in Preview but fail on a full run (community reports point to Preview processing only a subset of rows while the full run encounters nulls/inconsistent formatting across the complete dataset). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005809.mdx`**
  confirm that the Magic ETL SQL tile does not support recursive CTEs and that recursive/row-dependent calculations are unsupported across Magic ETL. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005809.mdx`**
  confirm SQL-tile handling of temporary tables (for example, CREATE TEMP TABLE) and of non-recursive WITH/CTE clauses, and confirm that Magic ETL does not expose the SQL that a DataFlow generates (the SQL action is translated into a graph of simpler Magic ETL actions, not the reverse). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005901.mdx`**
  confirm the current names and behavior of Magic ETL run-control features beyond Run to Here (for example, single-tile preview and running specific outputs), so they can be documented or cross-linked here. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042922974.mdx`**
  confirm whether Magic ETL DataFlows expose the same privacy lock and whether their edit access is derived from input-DataSet sharing in the same way. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042923134.mdx`**
  confirm the supported approach for bulk re-mapping many pieces of content to new DataSets at once (swapping a whole lineage's sources in one step rather than DataFlow by DataFlow) and for migrating an existing lineage's inputs to Cloud Amplifier or a new data provider. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042923174.mdx`**
  confirm the Required Grants for changing DataFlow ownership; no Required Grants section exists.

- [ ] **`360042923174.mdx`**
  confirm two current-state facts reported in the community: (1) the exact scope of the DataFlow Sharing modal (what access sharing grants a non-owner and what it does not), and (2) that a non-owner who adds an output DataSet to a DataFlow is not automatically granted ownership or permissions on that new output. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043427653.mdx`**
  confirm the Larger Grid details: the April 8, 2025 default cutoff, that the switch recommendation appears only to owners of older DataFlows, that Ignore dismisses permanently while the X dismisses only for the session, and the exact location of the grid lines and mini-map settings. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043427653.mdx`**
  confirm the exact control used to leave the full-screen Magic ETL editor without running (community reports describe a Cancel option that returns to Domo while preserving already-saved work) and its label/behavior. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043427953.mdx`**
  confirm the complete list of conditions that produce a "Not Runnable" error and the exact resolution steps. The triggers above are representative, synthesized from community forum reports, and need confirmation.

- [ ] **`360043427953.mdx`**
  confirm whether run status reflects all outputs finishing indexing or only the first, and the recommended way for a user to tell when every output has finished.

- [ ] **`360043427953.mdx`**
  confirm the exact meaning and resolution of the "Saved but Incomplete" status, that disconnected/orphan tiles block execution and how the UI flags them (orange warning icon), and the precise wording and cause of the engine-level errors ("Query runtime limit exceeded" and the data export failure). Synthesized from community forum reports; needs confirmation.

- [ ] **`360043427953.mdx`**
  confirm that the "output DataSet deleted" error indicates the user is not the output owner (rather than an actual deletion), how output-DataSet ownership relates to DataFlow edit/run access, and the Start-button-unavailable behavior on the Overview tab. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043427953.mdx`**
  confirm the recommended patterns for one-time historical corrections in append pipelines (Jupyter dataframe replace, API update, temporary corrective DataFlow). Synthesized from community forum reports; needs confirmation.

- [ ] **`360043437753.mdx`**
  document how to open Data Assembler and create a new job (the app or page entry point and any required access token). Synthesized from community forum reports; needs confirmation.

- [ ] **`360043437753.mdx`**
  document how to access and edit an existing Data Assembler job's settings (where the job list lives and which settings can be changed). Synthesized from community forum reports; needs confirmation.

- [ ] **`360044258533.mdx`**
  confirm whether DataSet Forms (interactive data entry that writes back to a DataSet) is a supported way for end users to change individual DataSet values, and the correct feature name and article to reference. Synthesized from community forum reports; needs confirmation.

- [ ] **`360044258533.mdx`**
  confirm the supported pattern for intentionally failing a DataFlow when the input returns zero rows (e.g. a Group By count row feeding an ERROR formula). synthesized from community forum reports; needs confirmation.

- [ ] **`360044289573.mdx`**
  confirm the exact default-time-zone behavior of NOW()/CURRENT_TIME()/CURRENT_TIMESTAMP() (community reports they return UTC) and the exact support status of CONVERT_TZ() across contexts (Beast Mode, Magic ETL, SQL DataFlow, connector SQL), since the community received conflicting answers. Synthesized from community forum reports; needs confirmation.

- [ ] **`360044289573.mdx`**
  confirm Beast Mode's exact ROUND() rounding mode for equidistant values so the ETL-vs-Beast-Mode difference can be stated precisely. Synthesized from community forum reports; needs confirmation.

- [ ] **`360044289573.mdx`**
  confirm the ETL-vs-Beast-Mode difference for HOUR() on elapsed-time strings over 24 hours (community reports that '170:15' errors in Magic ETL but returns 170 in Beast Mode). Synthesized from community forum reports; needs confirmation.

- [ ] **`360044289573.mdx`**
  confirm whether STR_TO_DATE() reliably parses the short month-name token %b (community reports needing to map to full month names and use %M as a workaround). Synthesized from community forum reports; needs confirmation.

- [ ] **`360044876094.mdx`**
  confirm whether GROUP_CONCAT(DISTINCT ...) is supported inside a Group By tile formula. The Supported Functions reference notes DISTINCT/ORDER BY are not supported in Magic ETL v2, while the SQL Expressions reference lists [DISTINCT]. synthesized from community forum reports and conflicting repo references; needs confirmation.

- [ ] **`360044876194.mdx`**
  confirm the current enforcement status of Relationship Type constraints. Community reports describe a period where the asymmetric constraints (One-to-Many / Many-to-One) were reversed and enforcement was paused. synthesized from community forum reports; needs confirmation.

- [ ] **`360044876614.mdx`**
  confirm the date-picker calendar shortcut in the Filter Rows tile: clicking the month/year header to jump to a month, year, and decade selection view. Synthesized from community forum reports; needs confirmation.

- [ ] **`360045485833.mdx`**
  confirm the exact current outbound-network limitation of the Magic ETL Python/R scripting tiles (whether external API calls are fully blocked, unreliable, or environment-dependent) before publishing. Synthesized from community forum reports; needs confirmation.

- [ ] **`360047787514.mdx`**
  confirm the current status of these editor issues (which are fixed vs. still present in the current release) and the confirmed fix for the dark pop-up text and formula-editor scrolling issues. Synthesized from recurring community forum reports (2025–2026): the save-failure, Group By validate-button, and cut-text fixes come from forum resolutions; the pop-up-text and formula-scroll rows use a safe generic fix pending your confirmation.

- [ ] **`360057087393.mdx`**
  confirm the CLI workaround community members reference for remapping a Magic ETL output to an existing DataSet ID (reported as list-dataflow / update-dataflow commands in the Domo CLI). These commands are not currently documented in the Domo CLI article, so confirm the exact command names, parameters, and whether this is supported before documenting or linking a procedure. Synthesized from community forum reports; needs confirmation.

- [ ] **`4404652354583.mdx`**
  confirm the exact steps to re-enable a DataFlow that was auto-disabled for inactivity (where the enable control lives and whether a manual run is required afterward). Synthesized from community forum reports; needs confirmation.

- [ ] **`What-is-Magic-ETL.mdx`**
  confirm the exact behavior when a Magic ETL DataFlow references a cloud-connector (e.g., Cloud Amplifier) DataSet whose connection is broken or unavailable: the specific error text and whether it appears when opening versus running the DataFlow. Synthesized from community forum reports; needs confirmation.

---

## 4. Changes Flagged by Support Gap Integrations

Two gap-fill analyses have been integrated into the restructure plan. This section
shows what changes are planned in your content area and what fact-check input reduces
hallucination risk in the updated articles.

### 4a. Support KB Audit Findings (Phase 4)

**Retirement batches in your area (Phase 4 execution plan):**

| Batch | Count | Action | Notes |
|-------|-------|--------|-------|
| DataFusion articles | 4 | → Retired (staged for 4.6) | DataFusion discontinued. 4 EN articles. Replacement SHIPPED: `DataFusion-Migration-Guide.mdx` (Magic ETL equivalents) — please also fact-check that guide for accuracy. Confirm Retired: feature gone from product. |
| Old Magic ETL tile articles | 7 | → Retired (1 Keep; staged for 4.6) | 7 EN tile-interface articles → Retired. KEEP exception: `360043428113` (Create a Recursive/Snapshot Old Magic ETL DataFlow). Confirm the old tile UI is fully replaced/inaccessible. |

### 4b. Community Forum Gap Analysis — Update Targets

**Critical update targets** (address alongside or immediately after Phase 3a):

| Rank | Article Area | Addition Needed | Fact-Check Info Needed |
|------|-------------|-----------------|------------------------|
| 2 | Magic ETL troubleshooting | Editor-level failure diagnostics: save failures, validate error, blank canvas bug | Verify current error messages are accurate; confirm blank-canvas bug status (fixed or still present?) |
| 3 | Magic ETL troubleshooting | 'Preview vs Run' discrepancy FAQ; 'Not Runnable' error causes | Confirm known causes of Preview vs Run differences; verify 'Not Runnable' error trigger conditions |
| 8 | Magic ETL preview documentation | Explicit 400k row preview limit; run-to-here and sample tile workarounds | Confirm 400k row limit is still accurate; verify run-to-here and sample tile work as described |

**High priority update targets** (9 articles in your area):

| Rank | Score | Topic | Affected Area | Specific Addition Needed |
|------|-------|-------|---------------|--------------------------|
| 18 | 72.8 | Viewing/charting DataFlow schedules (no native list of triggers/schedules) | SQL DataFlows / DomoStats / Governance | Document how to obtain dataflow schedule/trigger info (currently only via the undocumented /api/data |
| 20 | 72.3 | Constrained join (Relationship Type) feature and reversed-constraint advisory in | Magic ETL (Join Data tile) | Document the Relationship Type / constrained-join feature: what each constraint enforces, the known  |
| 23 | 71.9 | Magic ETL error/warning diagnostics: disconnected tiles, orange warning icon, 'S | Magic ETL (errors / warnings) | Explain why a dataflow can preview but fail ('Saved but Incomplete'), that disconnected tiles block  |
| 24 | 71.7 | Editing/correcting historical data in append-based ETLs; misleading output-owner | Magic ETL (output datasets / ownership) | Document patterns for correcting historical data without breaking an append pipeline (Jupyter/datafr |
| 31 | 69.6 | Larger Grid recommendation pop-up: behavior and permanent dismissal | Magic ETL (DataFlow settings) | Document the Larger Grid change: DataFlows created after 04/08/2025 default to Larger Grid; older on |
| 35 | 69.4 | Recursive / row-dependent calculations in Magic ETL (forecasts, running products | Magic ETL (limitations / patterns) | Document that Magic ETL cannot perform recursive/row-referential calculations and the non-recursive  |
| 51 | 66.6 | Intentionally failing a Magic ETL on bad/empty input (data sanity checks via ERR | Magic ETL (validation) | How-to: use the ERROR function in a formula to intentionally fail a dataflow for validation/sanity c |
| 101 | 61.2 | Aggregation context in Magic ETL formula tiles (Group By required, division of s | Magic ETL (Group By / formula tiles) | Clarify that formula tiles operate row-by-row and cannot aggregate; SUM/AVG belong in the Group By t |
| 106 | 60.7 | Joins in Magic ETL: missing fields, type-mismatched keys, left-outer dropping ro | Magic ETL (Join Data tile) | Document join gotchas: a column won't appear in the join field list if dropped by upstream Select Co |

---

## Quick Actions Summary

A prioritized list of everything this document is asking of you:

| # | Action | Type | Est. Effort |
|---|--------|------|------------|
| 1 | Read and fact-check `What-is-Magic-ETL.mdx` | Fact-check | 30–45 min |
| 2 | Read and fact-check `What-is-a-DataFlow.mdx` | Fact-check | 30–45 min |
| 3 | Read and fact-check `Prepare-and-Transform-Overview.mdx` | Fact-check | 30–45 min |
| 4 | Provide input for `How-Data-Flows-Through-Domo.mdx` | Info meeting | 30 min |
| 5 | Provide input for `Choosing-the-Right-Data-Prep-Tool.mdx` | Info meeting | 30 min |
| 6 | Fact-check `Split-Multi-Value-Fields-into-Rows.mdx` (Rank 117 community request) | Fact-check | 20–30 min |
| 7 | Fact-check `Handle-Source-Schema-Drift-in-Connectors.mdx` (Rank 299 community request) | Fact-check | 20–30 min |
| 8 | Supply info to write `Pivot-Table-Census-Calendar-Join.mdx` (Rank 57) | Info meeting | 30 min |
| 9 | Supply info to write `Plot-Two-Date-Columns-on-One-Axis.mdx` (Rank 61) | Info meeting | 30 min |
| 10 | Supply info to write `Data-Allocation-Split-Credit-in-ETL.mdx` (Rank 62) | Info meeting | 30 min |
| 11 | Supply info to write `Time-Interval-Bucketing-and-Dedup.mdx` (Rank 77) | Info meeting | 30 min |
| 12 | **Open placeholder in `000005150.mdx`:** confirm the exact preview row-sampling limit per input (reported in the communit | **Answer required** | 15–30 min |
| 13 | **Open placeholder in `000005541.mdx`:** confirm the exact behavior when an existing Replace/Append DataSet is switched t | **Answer required** | 15–30 min |
| 14 | **Open placeholder in `000005741.mdx`:** confirm the exact reason an AI Forecasting DataFlow can succeed in Preview but f | **Answer required** | 15–30 min |
| 15 | **Open placeholder in `000005809.mdx`:** confirm that the Magic ETL SQL tile does not support recursive CTEs and that rec | **Answer required** | 15–30 min |
| 16 | **Open placeholder in `000005809.mdx`:** confirm SQL-tile handling of temporary tables (for example, CREATE TEMP TABLE) a | **Answer required** | 15–30 min |
| 17 | **Open placeholder in `000005901.mdx`:** confirm the current names and behavior of Magic ETL run-control features beyond  | **Answer required** | 15–30 min |
| 18 | **Open placeholder in `360042922974.mdx`:** confirm whether Magic ETL DataFlows expose the same privacy lock and whether the | **Answer required** | 15–30 min |
| 19 | **Open placeholder in `360042923134.mdx`:** confirm the supported approach for bulk re-mapping many pieces of content to new | **Answer required** | 15–30 min |
| 20 | **Open placeholder in `360042923174.mdx`:** confirm the Required Grants for changing DataFlow ownership; no Required Grants  | **Answer required** | 15–30 min |
| 21 | **Open placeholder in `360042923174.mdx`:** confirm two current-state facts reported in the community: (1) the exact scope o | **Answer required** | 15–30 min |
| 22 | **Open placeholder in `360043427653.mdx`:** confirm the Larger Grid details: the April 8, 2025 default cutoff, that the swit | **Answer required** | 15–30 min |
| 23 | **Open placeholder in `360043427653.mdx`:** confirm the exact control used to leave the full-screen Magic ETL editor without | **Answer required** | 15–30 min |
| 24 | **Open placeholder in `360043427953.mdx`:** confirm the complete list of conditions that produce a "Not Runnable" error and  | **Answer required** | 15–30 min |
| 25 | **Open placeholder in `360043427953.mdx`:** confirm whether run status reflects all outputs finishing indexing or only the f | **Answer required** | 15–30 min |
| 26 | **Open placeholder in `360043427953.mdx`:** confirm the exact meaning and resolution of the "Saved but Incomplete" status, t | **Answer required** | 15–30 min |
| 27 | **Open placeholder in `360043427953.mdx`:** confirm that the "output DataSet deleted" error indicates the user is not the ou | **Answer required** | 15–30 min |
| 28 | **Open placeholder in `360043427953.mdx`:** confirm the recommended patterns for one-time historical corrections in append p | **Answer required** | 15–30 min |
| 29 | **Open placeholder in `360043437753.mdx`:** document how to open Data Assembler and create a new job (the app or page entry  | **Answer required** | 15–30 min |
| 30 | **Open placeholder in `360043437753.mdx`:** document how to access and edit an existing Data Assembler job's settings (where | **Answer required** | 15–30 min |
| 31 | **Open placeholder in `360044258533.mdx`:** confirm whether DataSet Forms (interactive data entry that writes back to a Data | **Answer required** | 15–30 min |
| 32 | **Open placeholder in `360044258533.mdx`:** confirm the supported pattern for intentionally failing a DataFlow when the inpu | **Answer required** | 15–30 min |
| 33 | **Open placeholder in `360044289573.mdx`:** confirm the exact default-time-zone behavior of NOW()/CURRENT_TIME()/CURRENT_TIM | **Answer required** | 15–30 min |
| 34 | **Open placeholder in `360044289573.mdx`:** confirm Beast Mode's exact ROUND() rounding mode for equidistant values so the E | **Answer required** | 15–30 min |
| 35 | **Open placeholder in `360044289573.mdx`:** confirm the ETL-vs-Beast-Mode difference for HOUR() on elapsed-time strings over | **Answer required** | 15–30 min |
| 36 | **Open placeholder in `360044289573.mdx`:** confirm whether STR_TO_DATE() reliably parses the short month-name token %b (com | **Answer required** | 15–30 min |
| 37 | **Open placeholder in `360044876094.mdx`:** confirm whether GROUP_CONCAT(DISTINCT  | **Answer required** | 15–30 min |
| 38 | **Open placeholder in `360044876194.mdx`:** confirm the current enforcement status of Relationship Type constraints | **Answer required** | 15–30 min |
| 39 | **Open placeholder in `360044876614.mdx`:** confirm the date-picker calendar shortcut in the Filter Rows tile: clicking the  | **Answer required** | 15–30 min |
| 40 | **Open placeholder in `360045485833.mdx`:** confirm the exact current outbound-network limitation of the Magic ETL Python/R  | **Answer required** | 15–30 min |
| 41 | **Open placeholder in `360047787514.mdx`:** confirm the current status of these editor issues (which are fixed vs | **Answer required** | 15–30 min |
| 42 | **Open placeholder in `360057087393.mdx`:** confirm the CLI workaround community members reference for remapping a Magic ETL | **Answer required** | 15–30 min |
| 43 | **Open placeholder in `4404652354583.mdx`:** confirm the exact steps to re-enable a DataFlow that was auto-disabled for inact | **Answer required** | 15–30 min |
| 44 | **Open placeholder in `What-is-Magic-ETL.mdx`:** confirm the exact behavior when a Magic ETL DataFlow references a cloud-connecto | **Answer required** | 15–30 min |
| 45 | Validate additions to: Magic ETL troubleshooting (Rank 2) | Review | 20 min |
| 46 | Validate additions to: Magic ETL troubleshooting (Rank 3) | Review | 20 min |
| 47 | Validate additions to: Magic ETL preview documentation (Rank 8) | Review | 20 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
