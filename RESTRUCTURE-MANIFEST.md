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

### Phase 3b-Forum — Critical Update Targets (Complete — 2026-08-20)

Priority `rec=update` gaps from the community forum analysis. Text written self-sufficiently; no screenshot TODO markers (clean-article policy). Uncertain product mechanics logged as embedded `[pm-input]` markers, which surface automatically in the owning PM's Phase 4.5 brief (Section 3d) via the article scan.

**Andrea Henderson — Magic ETL cluster (ranks 2, 3, 8):**

| Filename | Title | Disposition | Gap Rank/Score | Change | `[pm-input]` |
|----------|-------|-------------|----------------|--------|--------------|
| `360047787514.mdx` | Behavior Changes and Feature Updates in Magic ETL | updated | #2 / 83.8 | Added **Editor Known Issues and Quick Fixes** section: save-failure fixes (close other tab; remove/re-add inputs), Group By validate-button error is display-only, cut-text reopen fix, dark pop-up text and formula-editor scroll rows with safe generic fixes | Andrea — confirm current status of the five issues (fixed vs. present) + confirmed fix for pop-up-text and formula-scroll rows |
| `360043427953.mdx` | DataFlow and DataFusion Troubleshooting and FAQs | updated | #3 / 82.4 | Added three FAQ entries under DataFlows: preview-vs-full-run discrepancies (sampling, nulls, JSON/text splits, time zone), "Not Runnable" error causes, multi-output "Successful"-but-not-indexed behavior. Cross-links to `000005150#preview-and-testing-limits` and `360047787514#notable-behavior-changes` | Andrea — confirm full "Not Runnable" trigger list + whether run status reflects all outputs indexing or only the first |
| `000005150.mdx` | Data Selection in Magic ETL | updated | #8 / 77.5 | Added **Preview and Testing Limits** section: preview samples each input rather than the full DataSet; use a filtered DataSet View as input to test. Links to `360046074774` (Manage DataSet Views). Home for rank 8 in place of the 15-line stub `360043427653` (per plan) | Andrea — confirm exact preview row-sampling limit (~400k reported) + that the filtered-view workaround is recommended |

**Phil Fuchs — Beast Mode cluster (ranks 5, 10):**

| Filename | Title | Disposition | Gap Rank/Score | Change | `[pm-input]` |
|----------|-------|-------------|----------------|--------|--------------|
| `360043430133.mdx` | Sample Beast Mode Calculations: Period-over-Period Transforms | updated | #5 / 79.0 | Added **Rolling and Cumulative N-Month Totals** (trailing-window `CASE`+`SUM` pattern; true rolling/cumulative *series* needs a DataFlow because Beast Mode has no cross-row window functions; links the FAQ rolling-average example) and **Best Practice: A Month or Date Filter Can Break YTD Calculations** (a date filter strips history before aggregation; use a date-range/variable control or pre-aggregate in Magic ETL). Added a leap-year `<Note>` after the MTD table (align MTD-LY on `DAYOFMONTH`, not `DAYOFYEAR`; handle Feb 29). | Phil — confirm whether a native window-function capability / dedicated window-functions article is planned to link for the rolling/cumulative-series case |
| `000005559.mdx` | Use Non-aggregated Columns in Aggregated Beast Modes | updated | #10 / 76.1 | Added **Understand the "Aggregated and Non-aggregated Columns" Warning** section (non-blocking warning vs. blocking error; when safe to ignore vs. duplicate-row risk; resolution paths) and reframed the Support-only intro. | Phil — confirm exact current warning wording and that it is non-blocking (still saves/renders) |
| `360043430153.mdx` | Troubleshooting Beast Mode Calculations | updated (cross-link) | #10 / 76.1 | Added a short **"Aggregated and Non-aggregated Columns" Warning** entry linking to `000005559` for the full treatment | — |
| `360043430053.mdx` | Beast Mode FAQs | updated (cross-link) | #10 / 76.1 | Added a FAQ entry on the warning, cross-linking `000005559` | — |

**Khushboo — App Studio (rank 4):**

| Filename | Title | Disposition | Gap Rank/Score | Change | `[pm-input]` |
|----------|-------|-------------|----------------|--------|--------------|
| `000005295.mdx` | App Studio \| Overview | updated | #4 / 79.6 | Added **Manage Cards behind an App** section: orphan behavior on app delete, App pages absent from the card Move/Copy menu + info panel, **Delete Orphaned Cards** (`More > Admin > Cards` + grant requirement), and **Locate Orphaned Cards with the Governance Connector**. Existing orphan `<Warning>` reused, not duplicated. | Khushboo (4) — (1) no combined app+cards delete; (2) App pages absent from Move/Copy & card info panel; (3) exact Admin > Cards delete action + App-page filter; (4) whether the Governance Datasets connector maps cards to App Studio pages |

**Ryan Despain — Workflows (rank 12):**

| Filename | Title | Disposition | Gap Rank/Score | Change | `[pm-input]` |
|----------|-------|-------------|----------------|--------|--------------|
| `000005171.mdx` | Forms | updated | #12 / 75.4 | Added **Add Links or HTML to Question Text** subsection, a group-task **History-tab** identifier `<Note>`, and a **Review and Approve Form Submissions** section (Task Center review; App Studio read-only table + Brick write-back; bulk approve; secure public PII form Bricks). | Ryan (4) — link/HTML rendering in questions; read-only-table + Brick write-back pattern; native bulk-approval availability; securing public PII form Bricks |
| `000005172.mdx` | Monitor Queues in Task Center | updated | #12 / 75.4 | Added **Resolve "Assignee Does Not Have Update Content Access to Queue"** (grant Update Content access), **Customize Task List Columns**, and a turn-off-default-task-email `<Note>`. | Ryan (3) — default-email governance; exact error string + resolution; Task List column-customization mechanics |

**Critical batch complete (2026-08-20):** all 7 Critical `rec=update` forum gaps are done — ranks 2, 3, 8 (Andrea, committed `ed05fac9`); rank 4 (Khushboo); ranks 5, 10 (Phil Fuchs); rank 12 (Ryan Despain). 13 `[pm-input]` markers embedded across 7 articles (Phil 2, Khushboo 4, Ryan 7) → auto-flow to the owning PMs' Phase 4.5 briefs. Next: Phase 3b-Forum High targets (61 `rec=update`, ranked list in `RESTRUCTURE-PROGRESS.md`).

---

### Phase 3b-Forum — High Update Targets (Complete — 2026-08-20)

All 61 High `rec=update` forum gaps closed via 10 parallel subagents in 2 waves, clustered by PM; one file per agent (no write collisions); cross-links consolidated in a main-session follow-up pass. **45 files updated** (39 `s/article` + 6 `portal` docs), **71 new `[pm-input]` markers**. No screenshots added (clean-article policy; no applicable source shots). Two ranks (42, 93) were re-routed to their correct home articles after agents found the scored target mismatched. Change detail by rank was sourced from `_gaps_with_support.json`.

**Phil Fuchs — Beast Mode / PoP / PDP / Variables:**

| Filename | Ranks | Change | `[pm-input]` |
|----------|-------|--------|--------------|
| `7903767835031.mdx` | 29, 78, 87 | Variable scope (which cards a variable affects), reference value in labels/text, build a variable-driven toggle | 2 |
| `4408174643607.mdx` | 38 | FIXED share-of-total use case + Tips/Common Pitfalls (filter-shrinks-denominator; FIXED must sit inside an aggregate) | 1 |
| `360042925474.mdx` | 34 | Merged Beast Modes when moving a card to a new DataSet | 1 |
| `360042925494.mdx` | 39 | STR_TO_DATE/DATE_FORMAT mask matching; custom week start/week-ending label; BM-vs-ETL availability. **Fixed pre-existing stale link** (specifier article → `360043429953`) | 0 |
| `360043430053.mdx` | 73, 80 | FAQs: sum/aggregate a boolean column; AVG-of-CASE lower-than-expected. Updated "percent of total" answer to add FIXED | 1 |
| `360043430153.mdx` | 30, 67 | Troubleshooting: column-does-not-exist, COUNT vs SUM of CASE, CASE evaluation order, syntax checklist, HTML-encoded chars | 1 |
| `360042924834.mdx` | 16 | PoP card limitations + Beast Mode alternatives (don't hardcode `YEAR()`) | 0 |
| `360042934614.mdx` | 79 | PDP-does-not-restrict-Admins Warning; auto-share-on-enable flagged | 1 |

**Andrea Henderson — Magic ETL / AutoML:**

| Filename | Ranks | Change | `[pm-input]` |
|----------|-------|--------|--------------|
| `360044258533.mdx` | 51, 101 | Aggregate in a Group By tile (not Formula tile) ratios/order; Fail-a-DataFlow-on-bad-input (`ERROR()`) validation | 1 |
| `360044876094.mdx` | 52 | GROUP_CONCAT string combine (null-skip, SEPARATOR) | 1 |
| `360044876194.mdx` | 20, 106 | Relationship Type definition table; Troubleshoot a Join | 1 |
| `360043427653.mdx` | 31 | Larger Grid and canvas display options | 1 |
| `000005809.mdx` | 35 | Recursion / recursive-CTE not supported + workarounds | 1 |
| `360043427953.mdx` | 23, 24 | Saved-but-Incomplete status, disconnected tile, engine errors; output-DataSet-deleted, historical correction in append | 3 |

**Chris Wright — Charting / Analyzer:**

| Filename | Ranks | Change | `[pm-input]` |
|----------|-------|--------|--------------|
| `360042923914.mdx` | 70 | Multi-select page filters use OR logic (workarounds) | 1 |
| `360042924034.mdx` | 93 | Re-routed: tracking marker only — content added to Notebook Card articles (target mismatch) | 1 |
| `360042925374.mdx` | 54 | Row display limits note | 0 |
| `360043428813.mdx` | 68 | Color Rules Limitations and Workarounds | 1 |
| `360043429293.mdx` | 85 | Gauge: stop abbreviation; value+target+% needs a multi-value gauge | 1 |
| `360043429473.mdx` | 60 | Pivot Table Limitations and Workarounds | 1 |
| `360043429573.mdx` | 74 | "Which Table Type Should I Use?" decision guide | 1 |
| `360043430233.mdx` | 93 (re-route home) | Formatting Support and Limitations (card-type matrix, summary-number font, export) | 2 |

**Ryan Despain — Workflows / Governance Toolkit / Projects & Tasks:**

| Filename | Ranks | Change | `[pm-input]` |
|----------|-------|--------|--------------|
| `000005171.mdx` | 53 | Multi-select answers stored in one delimited cell + split workaround | 1 |
| `000005179.mdx` | 43, 65 | Pass app context into a workflow; Trigger limitations | 2 |
| `000005797.mdx` | 48 (+65) | Send Email and Notification Functions; end-a-single-branch note | 5 |
| `000005865.mdx` | 92 | AI Agent best practices (knowledge vs query results; model selection) | 1 |
| `360043437773.mdx` | 75 | Scheduled Reports Current Limitations | 1 |
| `6814561223959.mdx` | 15 | Data Types, Leading Zeros, and Views | 2 |
| `360042925874.mdx` | 42 (re-route home) | Create or Update Tasks Programmatically (no native Workflows action; Code Engine + API) | 1 |

**Khushboo — App Studio:**

| Filename | Ranks | Change | `[pm-input]` |
|----------|-------|--------|--------------|
| `000005295.mdx` | 40, 63, 72, 76, 94, 97, 110 | Share an App (app-level only); Design the Mobile Layout; Known Editor Behaviors; Filter Behavior and Limitations; Tabs Tips and Limitations | 15 |
| `000005829.mdx` | 46 | Report Builder FAQs (recipient filters, frequencies, PDF/PPT export, change propagation) | 2 |

**Tasleema Lallmamode — Connectors:**

| Filename | Ranks | Change | `[pm-input]` |
|----------|-------|--------|--------------|
| `360042926294.mdx` | 36, 41, 59, 102 | MFA auth; zero-row Replace no-wipe; spreadsheet upload failures; Box Excel-date-as-number | 4 |
| `360042929154.mdx` | 108 | Adobe 1.4 (Deprecated) → recreate-on-v2 migration note (kept minimal) | 1 |
| `360042932974.mdx` | 37 | Federated unfiltered/materialization query FAQ | 1 |

**Cross-product (per-file PM):**

| Filename | Ranks | PM | Change | `[pm-input]` |
|----------|-------|----|--------|--------------|
| `360042934594.mdx` | 19, 45 | Dan Brinton | Activity Log actions/objects; card-view reconcile | 2 |
| `360043439293.mdx` | 18 | Dan Brinton | DataFlow trigger/schedule not exposed | 1 |
| `360045120554.mdx` | 105 | Mamta Bolaki | Dataset names/descriptions/visibility for subscribers | 1 |
| `4403367344023.mdx` | 95 | Mamta Bolaki | Sandbox Best Practices | 1 |
| `000005561.mdx` | 88, 104 | Ken Boyer | AI Readiness: synonym-save FAQ; subscriber metadata carryover | 2 |
| `Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx` | 90 | Jordan Jensen | Manual refresh; move DataSet View across CA connections | 2 |

**Embed / Developer docs (`portal/`, owner TBD):**

| Filename | Ranks | Change | `[pm-input]` |
|----------|-------|--------|--------------|
| `workflow-appdb-sync.mdx` | 96 | AppDB sync mechanics, force-sync, troubleshooting, PUT vs POST | 1 |
| `programmatic-filtering.mdx` | 98 | Programmatic filters vs client-side pfilters (security); PDP inheritance | 1 |
| `url-parameters-in-embedded-content.mdx` | 58, 98 | Passing filters/params into App Studio Bricks; pfilter security Warning | 1 |
| `filtering-options.mdx` | 58 | Filters and bricks in App Studio | 0 |
| `hitting-a-workflow.mdx` | 58 | Public embed cannot trigger workflows | 1 |
| `domo-js-v5.mdx` | 58 | `filterContainer()` empty-array clearing difference (App State) | 1 |

**Cross-links added in the main-session follow-up pass:**
- `360042925494.mdx` — fixed stale specifier link (`360043430153` → `360043429953`)
- `360042923154.mdx` — reciprocal Tip linking the `360044258533` data-validation section

**Deferred secondary / other-file items (optional enhancements — each rank's PRIMARY target is addressed; logged for a later pass):**
- rank 54 → tooltip-field cap + average-line-with-series in general chart-properties/chart-type articles
- rank 60 → dynamic-pivot ETL guidance in `360044951294` (Magic ETL Pivot tile)
- rank 74 → Flex Table period-over-period config in `360043429073`
- rank 79 → "Unshare App does not unshare cards" in App Studio sharing (`000005295`)
- rank 16 → additional filter-respecting PoP Beast Mode samples in `360043430133`
- rank 65 → Workflow Start Form Brick (`000005372`) refresh; rank 75 → Dashboard export note (`360043437893`, SharePoint/auth images); rank 92 → summarize-and-email how-to content in `000005369`
- rank 108 → consolidated connector-retirements article (net-new) + `360042929174` / SharePoint / Facebook pages; rank 41 → SQL Server zero-row behavior; rank 59/102 → dedicated file-upload & Box connector articles
- rank 96 → reciprocal link on the AppDB-API doc

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
