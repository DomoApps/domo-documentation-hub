---
title: "KB Restructure Article Disposition Manifest"
excerpt: "Running log of what happened to every article during the KB restructure. Updated throughout all phases. Phase 9 converts this to the final audit report."
---

# KB Restructure Article Disposition Manifest

**Purpose:** Track the disposition of every article touched during the restructure so that nothing is accidentally dropped, deleted without a trace, or left unaccounted for. This file is updated as work happens — not reconstructed at the end.

**Source of truth for Phase 9 audit.** No article may be deleted or archived without a row in this manifest.

**Last updated:** 2026-07-15

---

## Disposition Types

| Code | Meaning |
|------|---------|
| `new` | Net-new article created; did not previously exist |
| `same-regrouped` | Existing article unchanged in content; moved to a new nav group |
| `updated` | Existing article with material content changes |
| `split` | Source article broken into multiple new articles; original to be deleted or archived |
| `merged-into` | Article's content merged into another article; original to be deleted or archived |
| `archived` | Article retained but moved to Archive nav group; `archived: true` frontmatter added |
| `legacy` | Article retained in its pillar; `legacy: true` + `tag: "Legacy"` added; PM sign-off required |
| `deleted` | Article removed; its content exists elsewhere (merged or rewritten into another article) |

---

## Screenshot Status Codes

| Code | Meaning |
|------|---------|
| `included` | All applicable source screenshots identified and included |
| `todo-markers` | _(deprecated — do not use; omit screenshot rather than leaving a marker)_ |
| `n/a` | Article has no applicable screenshots (conceptual-only content, or net-new with no source screenshots) |
| `pending` | Screenshot audit not yet run on this article |

---

## Phase 3a — Net-New Articles (Complete 2026-07-14)

All 31 articles below are net-new (`new` disposition). Written in the main session; registered in `docs.json`. Source articles are the existing KB articles each new article was synthesized from or linked to. Screenshot audit status reflects whether Gate 2 has been run.

| Filename | Title | Disposition | Source Articles (synthesized from) | Screenshot Status | Notes |
|----------|-------|-------------|-------------------------------------|-------------------|-------|
| `What-is-Domo.mdx` | What Is Domo? | new | `000005874.mdx`, role guide articles | included | 1 screenshot (dashboard UI) |
| `Getting-Started-for-Admins.mdx` | Getting Started for Admins | new | Admin how-to articles | included | 1 screenshot (Admin tab) |
| `Getting-Started-for-App-Builders.mdx` | Getting Started for App Builders | new | App Studio/Workflows overview articles | included | 1 screenshot (App Studio interface) |
| `Getting-Started-for-Data-Consumers.mdx` | Getting Started for Data Consumers | new | Consumer-facing how-to articles | included | 1 screenshot (dashboard UI); typo fix applied |
| `Getting-Started-for-Data-Engineers.mdx` | Getting Started for Data Engineers | new | Data engineering how-to articles | included | 1 screenshot (Data Center UI); heading fix applied |
| `Getting-Started-for-Developers.mdx` | Getting Started for Developers | new | API articles, Access Tokens | included | 1 screenshot (App Studio interface) |
| `What-is-a-DataSet.mdx` | What Is a DataSet? | new | Connector + ETL articles, Data Center source | included | 1 screenshot (Data Center UI) |
| `What-is-Magic-ETL.mdx` | What Is Magic ETL? | new | Magic ETL overview articles | included | 1 screenshot (ETL canvas) |
| `What-is-a-DataFlow.mdx` | What Is a DataFlow? | new | DataFlow articles | included | 1 screenshot (DataFlow type selection) |
| `Prepare-and-Transform-Overview.mdx` | Prepare and Transform Overview | new | All ETL/DataFlow articles | included | 1 screenshot (ETL canvas) |
| `What-is-a-Card.mdx` | What Is a Card? | new | Analyzer articles | included | 1 screenshot (Analyzer interface); link text fix applied |
| `What-is-a-Dashboard.mdx` | What Is a Dashboard? | new | Dashboard articles | included | 1 screenshot (dashboard view); link fixes applied |
| `What-is-Beast-Mode.mdx` | What Is Beast Mode? | new | Beast Mode FAQ + functions reference | included | 1 screenshot (Beast Mode editor); hallucinated FAQ entry removed |
| `Analyze-and-Visualize-Overview.mdx` | Analyze and Visualize Overview | new | All analyzer/chart articles | included | 1 screenshot (Analyzer interface); duplicate link removed |
| `What-is-an-Alert.mdx` | What Is an Alert? | new | Alerts Overview + alert articles | included | 1 screenshot (Alert Me card option); wrong grant removed |
| `Share-and-Collaborate-Overview.mdx` | Share and Collaborate Overview | new | Sharing/Buzz/Publications articles | included | 1 screenshot (Scheduled Reports nav); grant fix applied |
| `What-is-a-Connector.mdx` | What Is a Connector? | n/a | General Connector Info (12 articles) | n/a | No applicable hero screenshot in source articles; FAQ Merge/Upsert fix applied |
| `Connect-and-Bring-In-Data-Overview.mdx` | Connect and Bring In Data Overview | new | All connector articles | included | 1 screenshot (Cloud Integrations panel); Azure name fix applied |
| `What-is-Workbench.mdx` | What Is Workbench? | new | Workbench 5.2 overview articles | included | 1 screenshot (Workbench Home tab) |
| `Manage-Data-Overview.mdx` | Manage Data Overview | new | DataSet articles, Data Center context | included | 1 screenshot (DataSets list view) |
| `What-is-the-Data-Center.mdx` | What Is the Data Center? | new | DataSet management articles | included | 1 screenshot (Data Center main view) |
| `Find-and-Manage-Your-DataSets.mdx` | Find and Manage Your DataSets | new | DataSet management, sharing, workspace articles | included | 1 screenshot (Data Center view); grant description fix applied |
| `What-is-Domo-AI.mdx` | What Is Domo AI? | new | Domo AI FAQ + AI articles | included | 1 screenshot (AI Chat UI) |
| `AI-and-Data-Science-Overview.mdx` | AI and Data Science Overview | new | All AI/DomoStats/Jupyter articles | included | 1 screenshot (AI Chat UI) |
| `What-is-App-Studio.mdx` | What Is App Studio? | new | App Studio overview articles | included | 1 screenshot (App Studio editor); grants corrected to "Edit App (App Studio)" |
| `Build-Apps-and-Automate-Overview.mdx` | Build Apps and Automate Overview | new | App Studio/Workflows/Code Engine articles | included | 1 screenshot (App Studio editor); App Studio + Code Engine grants corrected |
| `Domo-Sandbox-Overview.mdx` | Domo Sandbox Overview | new | Sandbox article | included | 1 screenshot (My Repositories tab); grants completely rewritten |
| `Domo-User-Roles.mdx` | Domo User Roles | new | Roles/grants articles | included | 1 screenshot (Roles grid tab); "Manage All Roles" grant name fixed |
| `Security-and-Permissions-Overview.mdx` | Security and Permissions Overview | new | PDP, OAuth, security articles | included | 1 screenshot (PDP policy types); grant + PDP + CGH description fixes applied |
| `Administer-and-Govern-Overview.mdx` | Administer and Govern Overview | new | All admin articles | included | 1 screenshot (CGH content summary); "Manage All Roles" + CGH description fixes applied |
| `Develop-and-Integrate-Overview.mdx` | Develop and Integrate Overview | new | Existing API articles | included | 1 screenshot (CLI tool) |

---

## Phase 3a — Quality Gate Status

| Gate | Status | Notes |
|------|--------|-------|
| Gate 1: Fact-Check | ✅ Complete 2026-07-15 | 15+ factual errors fixed across 31 articles; see summary below |
| Gate 2: Screenshot Audit | ✅ Complete 2026-07-15 | Screenshots added to 28 of 31 articles; 3 had no applicable source screenshots |
| Gate 3: Style Guide Review | ✅ Complete 2026-07-15 | Heading audit (5 fixes) + structural pass (callouts, links, frontmatter, FAQ) — all clean |

### Phase 3a Fact-Check Summary (2026-07-15)

**Systemic errors fixed across multiple articles:**
- "Manage Roles" → "**Manage All Roles**" — wrong grant name in 3 articles (User Roles, Security, Admin+Govern)
- "Can Create DataSets" misattributed as required grant for Publication Groups and DataSet alerts — corrected in Share & Collaborate and Alerts
- App Studio grant "Create Pages and Apps" + "Edit Pages" → single grant "**Edit App (App Studio)**" — fixed in App Studio + Build Apps & Automate
- Content Governance Hub described as "governance health dashboard" when it is actually an archiving tool — fixed in Security and Admin+Govern

**Per-article fixes:**
- `What-is-Domo.mdx` — FAQ security answer said "two layers" (correct: three)
- `Getting-Started-for-Data-Consumers.mdx` — typo "learniing" fixed
- `What-is-a-Card.mdx` — wrong link anchor text for Chart Types article
- `What-is-a-Dashboard.mdx` — Scheduled Reports link pointed to wrong article; duplicate link consolidated
- `What-is-Beast-Mode.mdx` — removed fabricated "certified calculation" feature from FAQ
- `Analyze-and-Visualize-Overview.mdx` — duplicate/misattributed Chart Types link removed
- `What-is-an-Alert.mdx` — removed "Can Create DataSets" grant (not required for DataSet alerts)
- `What-is-a-Connector.mdx` — Merge/Upsert update method missing from FAQ; added
- `Connect-and-Bring-In-Data-Overview.mdx` — "Azure Synapse" → "Azure SQL Database"
- `Domo-Sandbox-Overview.mdx` — grants completely wrong; replaced with correct Administer Sandbox + Manage Repositories
- `Security-and-Permissions-Overview.mdx` — PDP description missing column-level policies
- `Build-Apps-and-Automate-Overview.mdx` — Code Engine grant "Manage All Company Settings" → "Manage Code Engine Packages"
- `Find-and-Manage-Your-DataSets.mdx` — Can Create DataSets description inaccurate

**PM input flag (add to Phase 4.5 briefs):**
- All Getting Started articles (Admins, App Builders, Data Engineers, Developers) link to the same eLearning course URL (`data-consumer-training`) — likely incorrect for non-consumer roles. Needs PM/Education team to confirm correct course URLs per role.

---

## Phase 3a-Forum — Net-New Articles (In Progress — 2026-07-15)

| Filename | Title | Disposition | PM | Gap Rank/Score | Screenshot Status | Quality Gates | Notes |
|----------|-------|-------------|----|----------------|-------------------|---------------|-------|
| `Beast-Mode-Window-Functions.mdx` | Use Window Functions in Beast Mode | new | Phil Fuchs | #1 / 93.0 | n/a (no applicable source screenshots) | ✅ All gates 2026-07-15 | Filter limitation FAQ has `[pm-input]` placeholder — Phil Fuchs to confirm workaround |
| `Beast-Mode-for-Spreadsheet-Users.mdx` | Translate Spreadsheet Formulas to Beast Mode | new | Phil Fuchs | #11 / 75.8 | included (Beast Mode editor) | ✅ All gates 2026-08-04 | Synthesized from 360043430073 (Basic Transforms) + 360043430053 (Beast Mode FAQs); IF→CASE, SUMIF/COUNTIF→SUM(CASE), VLOOKUP→ETL join, no-stacking guidance |
| `Restore-a-Deleted-Dashboard.mdx` | Restore a Deleted Dashboard | new | Dan Brinton | #9 / 76.2 | n/a (no-native-solution FAQ; no source article) | ✅ All gates 2026-08-04 | No source article — current-state FAQ. `[pm-input]` Dan Brinton: confirm backup retention window + Support recovery path |
| `Activity-Log-Event-Reference.mdx` | Activity Log Event Reference | new | Dan Brinton | #7 / 78.1 | included (Activity Log page) | ✅ All gates 2026-08-04 | Synthesized from 360042934574 (admin Activity Log) + 360042934594 (DomoStats app) + portal Activity Log API. `[pm-input]` Dan Brinton: full enumerated event glossary (VIEWED/EXPORTED/DOWNLOADED, FILE/FILE_REVISION/ACTIVITY_LOG_CSV) + canonical View Activity Logs grant wording |
| `Workflows-Write-Data-Back.mdx` | Write Data Back to a DataSet from Workflows | new | Ryan Despain | #6 / 78.3 | n/a (write-back UI undocumented in source) | ✅ All gates 2026-08-04 | Synthesized from 000005797 (Workflows Reference — read side only). Conceptual/decision guidance written; `[pm-input]` Ryan Despain: exact append/multiline-append action names + config steps |
| `DomoStats-vs-Governance-Datasets-Connector.mdx` | Compare the DomoStats and Domo Governance Datasets Connectors | new | Dan Brinton | #26 / n/a | n/a | ✅ All gates 2026-08-04 | Synthesized from 360043433813 + 360056318074; report-by-report comparison + service-account Activity Log caveat. Omitted unverifiable deprecation/scheduling claims |
| `Connect-Unsupported-Data-Sources.mdx` | Connect Data When No Native Connector Exists | new | Tasleema Lallmamode | #32 / n/a | n/a | ✅ All gates 2026-08-04 | Decision hub synthesized from 360042926294; links to JSON No Code, Workbench, Jupyter, custom connector |
| `Period-over-Period-Calculations.mdx` | Compare Periods over Time in Beast Mode and DataFlows | new | Phil Fuchs | #49 / n/a | included (offset-join logic table) | ✅ All gates 2026-08-04 | Synthesized from 360042923094 + 360042925494; prior-period flags, offset-join snapshot, rolling avg. Omitted unverifiable YEARWEEK/LAG year-boundary pitfalls |
| `Write-Data-from-Pro-Code-Apps-to-AppDB.mdx` | Write Data from an App to an AppDB Collection | new | Khushboo (App Dev Framework) | #50 / n/a | n/a | ✅ All gates 2026-08-04 | Synthesized from portal AppDB-API + manifest guides; links to Developer Portal reference. Omitted unverifiable bug narratives (new-collection-per-session, "Submitting" stuck state) |
| `Retrieve-Dataset-Source-Query-via-API.mdx` | Retrieve a Dataset's Source Query with the API | new | Ken Boyer (CLI/APIs) | #89 / n/a | n/a | ✅ All gates 2026-08-04 | Synthesized from portal Datasets API + overview; metadata→streamId→stream configuration→query chain. Links to Developer Portal reference |
| `Split-Multi-Value-Fields-into-Rows.mdx` | Split a Delimited Field into Multiple Rows in Magic ETL | new | Andrea Henderson | #117 / n/a | included (Split Column + Dynamic Unpivot) | ✅ All gates 2026-08-04 | Synthesized from 360045402873 (Text tile) + 360044951294 (Unpivot); two-step Split Column → Dynamic Unpivot recipe |
| `Choose-How-to-Share-Outside-Domo.mdx` | Choose How to Share Content Outside Domo | new | Mamta Bolaki | #139 / n/a | n/a (decision matrix) | ✅ All gates 2026-08-04 | Synthesized from 360043437993 + portal embed guides; public/private-embed/Publish/Edit-Experience decision matrix. Omitted unverifiable single-SSO-provider limit |
| `Find-Which-Dashboard-a-Card-Lives-On.mdx` | Find Which Dashboard a Card Lives On | new | Dan Brinton | #152 / n/a | n/a | ✅ All gates 2026-08-04 | Synthesized from 360056318074 (Governance connector Cards/Pages reports). Classic dashboards only; `[pm-input]` Tasleema Lallmamode for App Studio lineage |
| `Export-Domo-Data-to-Reports.mdx` | Build Formatted and Static Reports from Domo Data | new | Chris Wright | #172 / n/a | n/a | ✅ All gates 2026-08-04 | Synthesized from 360043437813 (export) + 000005829 (Report Builder) + 360043437913 (Google Sheets); options-and-limits overview |

### Phase 3a-Forum — Deferred to PM Briefs (net-new NOT written; KB lacks source material)

Per the "defer thin ones" rule (2026-08-04): these gaps cannot be written into a substantially complete article without inventing Domo-proprietary mechanics. Logged as pure `[pm-input]` items for the PM briefs; no file written.

| Rank | Intended filename | PM | What the PM must supply |
|------|-------------------|----|-----------------------|
| 13 | `Workflows-Package-Administration.mdx` | Ryan Despain | Domo Users / DataSet package function signatures + params, ID-type requirements, createUser attribute limits, group-support status/version, executor-context permission rule |
| 14 | `Dataset-Column-Rename-Impact.mdx` | Phil Fuchs | Whether cards/filters/sorts bind to column name (case-sensitive?), that rename breaks refs silently, ETL/DataFlow ref breakage, whether a stable Column ID exists, the safe-rename workflow |
| 17 | `Embed-Domo-in-Third-Party-Platforms.mdx` | Mamta Bolaki | Per-platform embed pattern + steps + limits for Confluence, NetSuite, HubSpot, SharePoint (esp. Confluence sandboxed-iframe selector/filter limitation); secure client ID/secret handling |
| 21 | `Filter-Funnel-and-PDP-Shield-Icons.mdx` | Chris Wright | Classic-dashboard + App Studio toggle paths/labels for filter and PDP icons, page-variable filter-icon behavior, whether PDP shield is a separate control |
| 22 | `Filter-Null-and-Empty-Values.mdx` | Chris Wright | Analyzer filter behavior for null vs empty (IN, NOT IN, equals, is empty), whether NOT IN excludes nulls and if intended, the Beast Mode ISNULL/CASE workaround |
| 25 | `Card-Refresh-Timing-After-Dataset-Update.mdx` | Phil Fuchs | Confirm cards have no settable refresh interval, dataset-update→index→display latency, the refresh API endpoint, any card cache/last-updated behavior |
| 27 | `Trigger-Workbench-from-External-Scripts.mdx` | Tasleema Lallmamode | Full `wb.exe` command/parameter reference, how to trigger a job/group from an external script, same-server requirement, referenceable job/group IDs |
| 28 | `Embedded-Dashboard-Unfiltered-Data-Flash.mdx` | Mamta Bolaki | Embed load-sequence/permissions timing that briefly shows unfiltered data, generating-user permission dependency, mitigation, mobile rendering parity |
| 33 | `Zero-Fill-Missing-Date-Gaps-in-Charts.mdx` | Phil Fuchs | Magic ETL date-spine/cross-join recipe (which tiles), rendering a continuous date axis in Analyzer, retaining empty pivot rows |
| 44 | `Dataset-Archived-Lifecycle-State.mdx` | Ryan Despain | Definition/trigger of the archived / "not accessed" state, inactivity threshold, how to detect via DomoStats/Activity Log, AI-readiness/lineage interaction |
| 47 | `Troubleshoot-Cards-Not-Updating.mdx` | Chris Wright | "Change Dataset" verification flow, dataset re-indexing latency, color-rule precedence (card vs dataset), filter/Beast Mode differences that make a card look stale |
| 55 | `Incremental-Ingestion-and-Lastvalue.mdx` | Tasleema Lallmamode | `lastvalue` parameter syntax + required default value, cause/fix of "last value is missing" error, incremental vs full-replace handling of late updates and deletes |
| 56 | `Dataset-Column-Character-Limits.mdx` | Phil Fuchs | Confirm text-column character limit (~1,024) and whether fixed, truncation-on-upload behavior, whether columns can be widened/deleted self-service, `set-dataset-column-width` CLI syntax |
| 57 | `Pivot-Table-Census-Calendar-Join.mdx` | Andrea Henderson | How to build a date-spine DataSet, the BETWEEN-join tile config in Magic ETL, DATE_FORMAT month grouping, default end-date handling for open intervals |
| 61 | `Plot-Two-Date-Columns-on-One-Axis.mdx` | Andrea Henderson | Magic ETL steps to unpivot/union two date columns into one shared column (which tiles), Analyzer line+bar combo-chart setup on the reshaped output |
| 62 | `Data-Allocation-Split-Credit-in-ETL.mdx` | Andrea Henderson | How to structure an allocation/split table with effective-date ranges, the Join-tile fan-out config, the value × split % calculation step |
| 64 | `Request-Access-Behavior.mdx` | Phil Fuchs | What Request Access / Request More Access do (Buzz message and/or owner emails), Buzz-disabled behavior, where owners see/manage requests, per-card/role controls |
| 66 | `Troubleshoot-Office-PowerPoint-Add-In.mdx` | Khushboo | "Content couldn't be loaded" trigger + fix, re-authentication path, 0-rows condition (Date column / Excel-table requirement), Office version deps, legacy-plugin deprecation timeline |
| 69 | `Dashboard-Editor-Unresponsive-Multi-Select-Filter.mdx` | Khushboo | Confirm multi-select filter card as a reproducible cause, the isolate-by-removing-cards flow as supported, Domo-side fix vs browser-side mitigation |
| 71 | `Drill-to-Final-Data-Security.mdx` | Chris Wright | "Drill to Final Data" toggle default state + security implication, `api/content/v1/cards` detection fields + auth, instance-wide audit, copy-to-embed behavior (distinct from drill-path prevention) |
| 77 | `Time-Interval-Bucketing-and-Dedup.mdx` | Phil Fuchs / Andrea Henderson | The dedup recipe (window-count vs Group By + Join tile), the decision rule for moving from Beast Mode to Magic ETL, the 6-hour bucket approach |
| 81 | `Schedule-Enterprise-Dataset-Copy.mdx` | Ryan Despain | Enterprise Data Copy native scheduling / specific-time options, the Dataset Copy connector's Advanced-tab time capability, the supported API/workflow trigger pattern |
| 82 | `Manage-Dataset-Error-Alerts.mdx` | Dan Brinton | How data-load-failure ("Error Loading Data") notifications are generated and why system-managed, per-dataset disable path, bulk-suppression options and official status |
| 83 | `Host-Images-for-Domo-Apps.mdx` | Khushboo | The `data-files` endpoint contract, how a FILE_ID is minted, beta Files feature scope/status, auth/size/type limits, internal-vs-external (S3/Azure/GCS) storage criteria |
| 84 | `GA4-BigQuery-Daily-Table-Nested-Data.mdx` | Tasleema Lallmamode | Recommended BigQuery connector variant, wildcard-view / `_TABLE_SUFFIX` SQL, Magic ETL `UNNEST(event_params)` steps, GA4-UI reconciliation methodology |
| 86 | `Find-Domo-Version-and-Tool-Versions.mdx` | Tasleema Lallmamode | Confirm no user-facing platform version, `/admin/tooldownloads` page description + URL + required grant, Workbench/plugin independent versioning |
| 91 | `Remove-Bad-Rows-from-a-Dataset.mdx` | Phil Fuchs | Confirm no single-row delete + the republish/full-replace workaround, the CLI full-replace escaping conditions that create a malformed row, whether Workbench avoids it |
| 99 | `Domo-API-Changelog.mdx` | Dan Brinton (route to dev-platform owner) | The versioning convention (if any), whether/where breaking changes are announced, deprecation timeline policy, any existing changelog content |
| 100 | `App-Studio-Performance-with-Large-Datasets.mdx` | Khushboo | Filter-card load impact (group-by/aggregate behavior), why unfiltered raw card data is slow, dataset/view design recommendations and size thresholds |
| 103 | `ETL-Credits-and-Consumption-Model.mdx` | Dan Brinton | Definition of a "manual run" vs scheduled, the "significant change" threshold that voids legacy ETL consumption status, a citable authoritative source |
| 107 | `Multi-Language-Dashboards.mdx` | Phil Fuchs / Chris Wright | Confirm a variable-driven CASE language switch renders as live switchable text, the AI Text Generation Magic ETL tile workflow, translated-label data-prep steps |
| 109 | `Custom-Card-Visuals-with-HTML-and-Bricks.mdx` | Khushboo / Chris Wright | HTML/CONCAT recipes + hyperlink pitfalls, avatar endpoint support (`/api/content/v1/avatar/...`), table-with-bars via Flex/Faceted bar, in-cell dropdown via bricks confirmation |
| 114 | `Dynamic-Dropdowns-in-Table-Cards.mdx` | Chris Wright | Confirm table cards support display + Action links only (no interactive dropdowns/write-back), the supported in-card control path (custom app vs Bricks vs writeback), cost considerations |
| 118 | `Editor-Dataset-Access-Scope.mdx` | Phil Fuchs | How dataset access is implicitly granted when a card/dashboard is shared with an Editor, Editor vs Participant dataset visibility, drill/"Go To Dataset" control, PDP/column-masking interplay, recommended patterns |
| 127 | `Alert-on-Stuck-Dataset-Refresh.mdx` | Dan Brinton | Confirm a DataSet alert on the DomoStats last-run field to detect a stuck refresh + the exact condition; the Workflow timer-trigger + Run Connector action to run sub-daily |
| 142 | `Choose-a-Cloud-Data-Warehouse.mdx` | Jordan Jensen | Credit model (pushdown vs materialization), sizing guidance for small datasets, which Domo features force materialization and consume ingestion credits (PDP, View Data Explorer, alerts, scheduled emails) |
| 144 | `AI-Chat-API-Session-ID.mdx` | Ken Boyer | Ask Chat endpoint path/method, how to obtain the Domo-generated session ID, the required call sequence, the client-UUID→HTTP 200 canned-refusal behavior, auth/prereqs |
| 146 | `Domo-Certification-Exam-Logistics.mdx` | Domo University / Enablement (no listed PM) | Exam duration, single-sitting requirement, online vs proctored format, three-step structure, hands-on requirements, whether the KB hosts content or points to Domo University |
| 159 | `Extract-Data-from-PDFs-with-Domo-AI.mdx` | Ken Boyer | How PDFs (not just images) are ingested/converted, batch processing from S3/SFTP, Magic ETL AI tile or Brick exposure, structured-vs-scanned-PDF limits + source-prep guidance |
| 161 | `Private-Embed-Token-Validation-Errors.mdx` | Mamta Bolaki | Why a valid embedToken still 302-redirects to login, client ID/secret + authorized-domains interaction, token regeneration after a domain change, why the auto-submit form lands on the default post-login page |
| 209 | `Workspaces-and-Folder-Organization.mdx` | Khushboo | How to create folders/sub-folders for apps/dashboards/data sources, grid vs list views, required grant/role, the grid-vs-list sub-folder visibility difference |
| 244 | `Dataset-Level-Date-and-Fiscal-Calendar-Defaults.mdx` | Chris Wright | Whether dataset-level date-range/fiscal-calendar defaults exist and how they flow to cards; the normal-vs-drill-path missing-field highlighting behavior |
| 299 | `Handle-Source-Schema-Drift-in-Connectors.mdx` | Andrea Henderson | Connector "import without headers" + assign-by-position downstream in ETL; `FUZZY_PARSE_DATE` syntax in a Magic ETL formula tile; connector behavior when source columns are added/removed/renamed |

---

## Phase 3b — Updated Articles (In Progress)

Articles updated here may have been done out-of-order (before Phase 3b officially starts) when urgency required it.

### Snowflake Urgent Fix (2026-07-15) — out-of-order; done before Phase 3b opened

Snowflake discontinued username/password authentication in November 2025. All 7 articles below had stale future-tense language ("will be retired") and a `<Note>` that should be a `<Warning>`. PM: Tasleema Lallmamode.

**Changes applied to all 7:**
1. `<Note>` → `<Warning>` with updated past-tense retirement language
2. Migration section heading renamed to "Migrate Your Snowflake DataSets" with updated body
3. Prerequisite bullet updated to note auth method is no longer accepted
4. "When should I use this connector?" FAQ entry replaced with retired-connector redirect
5. `excerpt:` updated to reflect retired status

| Filename | Title | Disposition |
|----------|-------|-------------|
| `360042931814.mdx` | Snowflake Connector | updated |
| `360042931834.mdx` | Snowflake Unload V2 Connector | updated |
| `360043436313.mdx` | Snowflake Unload Connector | updated |
| `360043437093.mdx` | Snowflake Writeback Connector | updated |
| `360061691114.mdx` | Snowflake High Bandwidth With Advanced Partitions Connector | updated |
| `360057013754.mdx` | Snowflake Partition Connector | updated |
| `360058757134.mdx` | Snowflake Managed Unload Connector | updated |

---

## Phase 4 — Archived / Legacy / Deleted Articles (Not Started)

Rows will be added here as articles are retired. No article may be deleted or archived without an entry here.

**Known batches pending Phase 4 (pre-logged):**

| Source Filename | Title | Planned Disposition | Notes |
|-----------------|-------|---------------------|-------|
| Workbench 4 articles (37) | Various | `archived` | D1 confirmed; add rows when Phase 4 executes |
| DataFusion articles (11) | Various | `archived` | Confirmed discontinued |
| Old Magic ETL tile articles (15) | Various | `archived` | 1 article to keep (`Create a Recursive/Snapshot Old Magic ETL DataFlow`) |
| Defunct-service connectors (111) | Various | `archived` | Verified via Support KB Audit |
| CourseBuilder articles (16) | Various | `archived` (pending D10) | Awaiting PM confirmation |

---

## Orphaned Articles (Phase 1 Finding)

| Filename | Title | Status | Notes |
|----------|-------|--------|-------|
| `000005849.mdx` | Use FileSets to Gather Information from Unstructured Data | Orphaned — not in nav | Add to nav when appropriate |
| `Access-Tokens.mdx` | Access Tokens | Orphaned intentionally — Beta feature | Add to nav when feature ships |
