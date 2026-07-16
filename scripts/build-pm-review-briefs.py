#!/usr/bin/env python3
"""
Build per-PM review briefs for KB restructure PM meetings.

Reads:
  - Article-PM-Ownership-Reference.mdx  (PM → feature → article mapping)
  - _gaps_with_support.json              (community forum gap analysis)

Outputs one .md file per PM in pm-review-briefs/.

Each brief has four sections:
  1. Content reorganization — how the PM's features map to the new pillars
  2. AI-generated articles — Phase 3a synthesis articles needing PM fact-check
  3. Gap articles — items requiring a dedicated info-gathering meeting
  4. Support gap integration changes — what changed in response to Audit + Forum analysis

Usage:
  python3 scripts/build-pm-review-briefs.py
"""

import json
import re
import os
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
OWNERSHIP_FILE = REPO_ROOT / "Article-PM-Ownership-Reference.mdx"
GAPS_FILE = REPO_ROOT / "_gaps_with_support.json"
OUTPUT_DIR = REPO_ROOT / "pm-review-briefs"


# ─────────────────────────────────────────────────────────────────────────────
# FEATURE → NEW PILLAR MAPPING
# Source: RESTRUCTURE-IA-SPEC.md
# (ia-spec.json was gitignored; this is the canonical feature-level mapping)
# ─────────────────────────────────────────────────────────────────────────────

FEATURE_PILLAR = {
    "Accessibility":                        "Pillar 9: Administer & Govern",
    "Admin":                                "Pillar 9: Administer & Govern",
    "AI Services":                          "Pillar 8: AI & Data Science",
    "Alerts, NLG, Smart Alerts/Insights":   "Pillar 7: Share & Collaborate",
    "App Dev Framework":                    "Pillar 6: Build Apps & Automate",
    "App Studio":                           "Pillar 6: Build Apps & Automate",
    "AppStore":                             "Pillar 6: Build Apps & Automate",
    "Approvals":                            "Pillar 6: Build Apps & Automate",
    "Attribute Based Access Control (ABAC)":"Pillar 9: Administer & Govern",
    "Auto ML":                              "Pillar 4: Prepare & Transform Data",
    "Beast Mode":                           "Pillar 5: Analyze & Visualize",
    "Bricks/Templates":                     "Pillar 6: Build Apps & Automate",
    "Buzz":                                 "Pillar 7: Share & Collaborate",
    "CLI":                                  "Pillar 10: Develop & Integrate",
    "Cloud Amplifier":                      "Pillar 2: Connect & Bring In Data",
    "Combined Schema":                      "Pillar 4: Prepare & Transform Data",
    "Connectors 1.0":                       "Pillar 2: Connect & Bring In Data",
    "Consumption":                          "Pillar 9: Administer & Govern",
    "Data Center":                          "Pillar 3: Manage Data",
    "Data Flows":                           "Pillar 4: Prepare & Transform Data",
    "Data Views":                           "Pillar 3: Manage Data",
    "DataSets":                             "Pillar 3: Manage Data",
    "Doc Cards":                            "Pillar 5: Analyze & Visualize",
    "Documents-Filesets":                   "Pillar 8: AI & Data Science",
    "Domo Everywhere":                      "Pillar 7: Share & Collaborate",
    "DomoStats":                            "Pillar 8: AI & Data Science",
    "Education":                            "Pillar 1: Getting Started",
    "Export to CSV":                        "Pillar 5: Analyze & Visualize",
    "Federated":                            "Pillar 2: Connect & Bring In Data",
    "Freemium":                             "Pillar 1: Getting Started",
    "Fusions":                              "Archive — DataFusion deprecated (retiring in Phase 4)",
    "Goals":                                "Pillar 9: Administer & Govern",
    "Governance Toolkit":                   "Pillar 9: Administer & Govern",
    "Jupyter Notebooks":                    "Pillar 8: AI & Data Science",
    "Magic ETL":                            "Pillar 4: Prepare & Transform Data",
    "Mobile - iOS":                         "Pillar 1: Getting Started",
    "MS Office Plugins / Addins":           "Pillar 7: Share & Collaborate",
    "MS Office Plugins/Addins":             "Pillar 7: Share & Collaborate",
    "Onboarding":                           "Pillar 1: Getting Started",
    "Period over Period":                   "Pillar 5: Analyze & Visualize",
    "Profile":                              "Pillar 9: Administer & Govern",
    "Projects & Tasks":                     "Pillar 7: Share & Collaborate [D2: may → Archive if feature deprecated]",
    "Publication Groups":                   "Pillar 7: Share & Collaborate",
    "Sandbox":                              "Pillar 9: Administer & Govern",
    "Single Sign-On":                       "Pillar 9: Administer & Govern",
    "Slideshows":                           "Pillar 7: Share & Collaborate",
    "Third Party Connectors":               "Pillar 2: Connect & Bring In Data",
    "Workbench":                            "Pillar 2: Connect & Bring In Data",
    "Worksheets":                           "Pillar 5: Analyze & Visualize",
    "Charting":                             "Pillar 5: Analyze & Visualize",
    "Analyzer":                             "Pillar 5: Analyze & Visualize",
    "Application Security":                 "Pillar 9: Administer & Govern (no PM assigned)",
    "Release Management":                   "Release Notes (no content PM)",
}

# Navigation changes that need calling out explicitly in the brief
STRUCTURAL_NOTES = {
    "Tasleema Lallmamode": [
        "**CDW merge:** Cloud Data Warehouses (104 articles) are no longer a top-level section — they are now a sub-group inside the Connector Library. Writeback Connectors (55 articles) are similarly integrated into the library alongside read connectors rather than living in a standalone section.",
        "**Workbench consolidation:** Workbench 4 (37 articles) is moving to Archive (D1 confirmed). Workbench 5.1 gets a clearly-labeled Legacy sub-group.",
        "**Defunct-service connectors (111):** Articles for services that no longer exist (LinkedIn API v1, Pinterest, StumbleUpon, etc.) are Phase 4 retirement candidates.",
    ],
    "Andrea Henderson": [
        "**DataFusion retirement:** All 11 DataFusion articles are being archived in Phase 4. A `DataFusion-Migration-Guide.mdx` needs to be written (pointing users to Magic ETL equivalents) before or alongside the archival.",
        "**Old Magic ETL tile articles (15):** 15 articles about the old Magic ETL tile interface are being archived. 1 article (`Create a Recursive/Snapshot Old Magic ETL DataFlow`) is explicitly kept.",
    ],
    "Khushboo": [
        "**CourseBuilder (16 articles):** Support KB Audit flags CourseBuilder as retired/removed from Domo Appstore. Pending D10: confirm with you whether to archive all 16 before Phase 7 nav rebuild.",
    ],
    "Chris Wright": [
        "**'Build Your First Dashboard' (D4):** This tutorial currently lives in Getting Started. It should move to Analyze & Visualize > Dashboards & Pages. Confirm before moving.",
    ],
    "Jordan Jensen": [
        "**DataSet Management split (D9):** Some DataSet Management articles currently in Prepare & Transform will move to the new Manage Data pillar (Pillar 3). The split: pipeline-oriented articles stay in Pillar 4; governance/lifecycle articles move to Pillar 3. Resolve before Phase 7.",
    ],
    "Dan Brinton": [
        "**'Introduction to Domo' (D5):** The existing 000005874 article overlaps with the new 'What is Domo?' synthesis article. Decision needed: keep as deep-dive companion, or retire once new article ships?",
        "**'What is an Alert?' new article:** An alert concept article is being synthesized and added to the Alerts section. The existing Alerts Overview article may become secondary.",
    ],
    "Phil Fuchs": [
        "**DataFusion/Fusions:** Fusions (DataFusion) articles are being archived in Phase 4. If any Beast Mode or Combined Schema articles reference DataFusion, they'll need updating.",
        "**Data Views (D9):** Data Views articles may shift between Pillar 3 (Manage Data) and Pillar 4 (Prepare & Transform Data) depending on D9 resolution.",
        "**Window function filter limitation workaround (Beast-Mode-Window-Functions.mdx):** The new window functions article notes that Beast Mode window function columns cannot be used as chart filters due to order-of-operations. A workaround exists but is not yet confirmed. Please confirm the recommended approach (e.g., materialize the calculation in Magic ETL before bringing into Analyzer, restructure logic to avoid post-aggregation filtering, or other). The FAQ accordion in the article has a `[pm-input]` placeholder — provide the confirmed steps and we'll replace it.",
        "**Review new article: 'Use Window Functions in Beast Mode' (s/article/Beast-Mode-Window-Functions.mdx):** Published 2026-07-15 as the #1 Critical gap from forum analysis. Covers RANK/DENSE_RANK, LAG/LEAD, SUM(SUM(x)) OVER running totals, Top N + Others. Please review for accuracy and completeness before the article is widely promoted.",
    ],
    "Mamta Bolaki": [
        "**Domo Everywhere positioning:** Domo Everywhere content lives in Pillar 7 (Share & Collaborate) with its own sub-section. The embed framing (public vs. private, SSO + PDP interaction) should be consistent across all Domo Everywhere articles.",
    ],
    "Ryan Despain": [
        "**Projects & Tasks (D2):** 10 articles currently in Share & Collaborate. If the feature is being phased out in favor of Workflows, these may belong in Archive. Confirm status.",
        "**PDP (Personalized Data Permissions):** PDP articles are in Administer & Govern (Pillar 9). The Governance Toolkit sits in the same pillar.",
    ],
    "Ken Boyer": [
        "**Develop & Integrate (Pillar 10):** Currently only 5 articles — severely thin. This pillar cannot tell a story until Phase 3a content is written. The pillar may largely function as an entry ramp to the Developer Portal (developer.domo.com).",
        "**D6 scope question:** Confirm: should Develop & Integrate be KB how-tos, or primarily a link-out to developer.domo.com?",
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 3a — SYNTHESIZABLE ARTICLES → OWNING PM
# ─────────────────────────────────────────────────────────────────────────────

PHASE3A_ARTICLES = [
    # (filename, title, pillar, owning_pm, synthesize_from, key_claims_to_verify)
    ("What-is-Domo.mdx",
     "What is Domo?", "Pillar 1", "Dan Brinton",
     "000005874, Getting Started role guides",
     "Core value proposition, platform overview, key use cases — verify nothing is outdated or overpromised"),
    ("Getting-Started-for-Admins.mdx",
     "Getting Started for Admins", "Pillar 1", "Dan Brinton",
     "Admin how-tos, roles/grants articles",
     "Admin onboarding path, key first tasks (user setup, SSO, security), grant scopes"),
    ("Getting-Started-for-App-Builders.mdx",
     "Getting Started for App Builders", "Pillar 1", "Khushboo",
     "App Studio / Workflows overview articles",
     "App builder journey, recommended starting tools, prerequisites, App Studio vs DDX scope"),
    ("Getting-Started-for-Developers.mdx",
     "Getting Started for Developers", "Pillar 1", "Ken Boyer",
     "API articles, MCP article, Access Tokens",
     "Developer entry points, API auth methods, available SDKs, MCP integration availability"),
    ("What-is-a-DataSet.mdx",
     "What is a DataSet?", "Pillar 4", "Jordan Jensen",
     "Connector how-tos, ETL input tile articles",
     "DataSet definition, dataset types, lifecycle states, update methods — especially the 'archived' state"),
    ("What-is-Magic-ETL.mdx",
     "What is Magic ETL?", "Pillar 4", "Andrea Henderson",
     "Magic ETL overview articles",
     "Magic ETL capabilities, when to use vs SQL DataFlows, 400k preview row limit"),
    ("What-is-a-DataFlow.mdx",
     "What is a DataFlow?", "Pillar 4", "Andrea Henderson",
     "DataFlow articles",
     "DataFlow types (SQL, Python, R), when to use each vs Magic ETL"),
    ("Prepare-and-Transform-Overview.mdx",
     "Prepare & Transform Data Overview", "Pillar 4", "Andrea Henderson",
     "All ETL / DataFlow / DataSet articles",
     "Full data prep toolbox, positioning of each tool, credit/consumption model accuracy"),
    ("What-is-a-Card.mdx",
     "What is a Card?", "Pillar 5", "Chris Wright",
     "Analyzer articles",
     "Card types, Analyzer overview, card lifecycle, card vs dashboard distinction"),
    ("What-is-a-Dashboard.mdx",
     "What is a Dashboard?", "Pillar 5", "Chris Wright",
     "Dashboard articles",
     "Dashboard types, filter behavior, card organization, page vs app distinction"),
    ("What-is-Beast-Mode.mdx",
     "What is Beast Mode?", "Pillar 5", "Phil Fuchs",
     "Beast Mode FAQs, functions reference",
     "Beast Mode definition, when to use vs Magic ETL, aggregation rules, filter limitations"),
    ("Analyze-and-Visualize-Overview.mdx",
     "Analyze & Visualize Overview", "Pillar 5", "Chris Wright",
     "All Analyzer / chart / dashboard articles",
     "Complete analysis toolbox overview, chart recommendation guidance"),
    ("What-is-an-Alert.mdx",
     "What is an Alert?", "Pillar 7", "Dan Brinton",
     "Alerts Overview, alert articles",
     "Alert types, trigger conditions, Smart Alerts / NLG behavior, notification routing"),
    ("What-is-a-Connector.mdx",
     "What is a Connector?", "Pillar 2", "Tasleema Lallmamode",
     "General Connector Info (12 articles)",
     "Connector concept, OAuth vs API key auth, scheduling, update methods"),
    ("Connect-and-Bring-In-Data-Overview.mdx",
     "Connect & Bring In Data Overview", "Pillar 2", "Tasleema Lallmamode",
     "All connector / Workbench articles",
     "Read + write framing accuracy, Cloud Amplifier as recommended CDW path, connector types"),
    ("Manage-Data-Overview.mdx",
     "Manage Data Overview", "Pillar 3", "Jordan Jensen",
     "DataSet articles, Data Center context",
     "Data Center navigation, dataset discovery, lifecycle, sharing — verify current UI state"),
    ("What-is-the-Data-Center.mdx",
     "What is the Data Center?", "Pillar 3", "Jordan Jensen",
     "DataSet management articles, connector how-tos",
     "Data Center UI, dataset cards, status indicators — verify current UI state"),
    ("Find-and-Manage-Your-DataSets.mdx",
     "Find and Manage Your DataSets", "Pillar 3", "Jordan Jensen",
     "DataSet management, sharing, workspace/favorites articles",
     "Search/filter/favorite/share datasets — verify current Data Center UI"),
    ("What-is-Domo-AI.mdx",
     "What is Domo AI?", "Pillar 8", "Ken Boyer",
     "Domo AI FAQ, AI Playground, AI articles",
     "AI Chat capabilities, AI Playground, available AI models, what's GA vs Beta"),
    ("AI-and-Data-Science-Overview.mdx",
     "AI & Data Science Overview", "Pillar 8", "Ken Boyer",
     "All AI / DomoStats / Jupyter articles",
     "Full AI toolbox: AI Chat, AutoML, Jupyter, DomoStats — verify current feature availability"),
    ("What-is-App-Studio.mdx",
     "What is App Studio?", "Pillar 6", "Khushboo",
     "App Studio Overview articles",
     "App Studio capabilities, no-code vs pro-code boundary, Code Engine integration"),
    ("Build-Apps-and-Automate-Overview.mdx",
     "Build Apps & Automate Overview", "Pillar 6", "Khushboo",
     "App Studio, Workflows, Code Engine articles",
     "Full app-building toolbox overview, App Studio vs Workflows use cases"),
    ("What-is-Workbench.mdx",
     "What is Workbench?", "Pillar 2", "Tasleema Lallmamode",
     "Workbench 5.2 overview, Workbench Enterprise",
     "Workbench capabilities, read + write paths, current version support status"),
    ("Share-and-Collaborate-Overview.mdx",
     "Share & Collaborate Overview", "Pillar 7", "Dan Brinton",
     "Sharing / Buzz / Publications / Embed articles",
     "All sharing mechanisms, publication groups vs Domo Everywhere scope distinction"),
    ("Domo-User-Roles.mdx",
     "Domo User Roles and What They Can Do", "Pillar 9", "Dan Brinton",
     "Roles / grants articles",
     "System roles, custom roles, grant scopes — verify completeness of role list"),
    ("Security-and-Permissions-Overview.mdx",
     "Security & Permissions Overview", "Pillar 9", "Dan Brinton",
     "PDP, OAuth, security settings articles",
     "PDP, SSO, IP allowlist, access tokens, session management — verify current security model"),
    ("Administer-and-Govern-Overview.mdx",
     "Administer & Govern Overview", "Pillar 9", "Dan Brinton",
     "All admin articles",
     "Full admin toolbox overview — verify nothing major is missing from hub"),
    ("Domo-Sandbox-Overview.mdx",
     "Domo Sandbox Overview", "Pillar 9", "Mamta Bolaki",
     "Sandbox article, Linked Repositories",
     "Sandbox capabilities, promotion workflow, environment types, linked repo feature"),
    ("Develop-and-Integrate-Overview.mdx",
     "Develop & Integrate Overview", "Pillar 10", "Ken Boyer",
     "Existing 5 API articles",
     "Developer entry points, API vs SDK, auth options, MCP integration"),
]

# PM Input articles — need a dedicated meeting; can't be synthesized without PM sign-off
PHASE3A_PM_ARTICLES = [
    # (filename, title, owning_pm, what_pm_must_provide)
    ("How-Data-Flows-Through-Domo.mdx",
     "How Data Flows Through Domo",
     "Andrea Henderson",
     "Canonical end-to-end pipeline narrative; confirm how connect → prepare → analyze → share → govern is described; sign off on framing"),
    ("Choosing-the-Right-Data-Prep-Tool.mdx",
     "Choosing the Right Data Prep Tool",
     "Andrea Henderson",
     "Positioning: when to use Magic ETL vs SQL DataFlow vs Python/R vs Data Models; official recommendation matrix"),
    ("Understanding-DataSet-Joins.mdx",
     "Understanding DataSet Joins & Relationships",
     "Phil Fuchs",
     "Decision guidance: when to use ETL joins vs Data Models vs DataFlows; join semantics and performance tradeoffs"),
    ("Domo-for-Mobile-Overview.mdx",
     "Domo for Mobile Overview",
     "Chris Wright",
     "Confirm current iOS app feature scope: what can/can't be done vs web; roadmap awareness; any known limitations to document"),
]


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 3a-FORUM — NEW ARTICLES FROM FORUM GAP ANALYSIS → OWNING PM
# ─────────────────────────────────────────────────────────────────────────────

FORUM_NEW_CRITICAL = [
    # (rank, filename, topic_summary, owning_pm, fact_check_needed)
    (1,  "Beast-Mode-Window-Functions.mdx",
         "RANK/DENSE_RANK, LAG/LEAD, SUM(SUM(x)) OVER running totals, Top N + Others; 'can't filter by window function' limitation and workarounds",
         "Phil Fuchs",
         "Confirm window function behavior; verify 'filter limitation' is still accurate and not a known roadmap item; review worked examples"),
    (6,  "Workflows-Write-Data-Back.mdx",
         "Append / Multiline Append / AppDB write from Workflows; dynamic row handling",
         "Ryan Despain",
         "Confirm Append vs Multiline Append semantics; AppDB write path; any limits on dynamic rows"),
    (7,  "Activity-Log-Event-Reference.mdx",
         "All Activity Log event types defined: VIEWED vs EXPORTED vs DOWNLOADED; DomoStats field mapping",
         "Dan Brinton",
         "Verify the full event type list is current; confirm DomoStats field names and mapping; check for any recently added event types"),
    (9,  "Restore-a-Deleted-Dashboard.mdx",
         "No self-service restore; contact support path; prevention via snapshot/copy",
         "Chris Wright",
         "Confirm no self-service restore exists; verify current support escalation path; check if Admin tools added recovery options"),
    (11, "Beast-Mode-for-Spreadsheet-Users.mdx",
         "IF→CASE, SUMIF→SUM(CASE), VLOOKUP→ETL join translation guide; no stacked IF, no volatile functions",
         "Phil Fuchs",
         "Verify translation examples are accurate; confirm 'no stacked IF' limitation; review function mapping completeness"),
]

FORUM_NEW_HIGH = [
    # (rank, filename, topic_summary, owning_pm)
    (13,  "Workflows-Package-Administration.mdx",
          "Domo Users / DataSet package functions: assign roles, manage owners, set attributes via Workflows",
          "Ryan Despain"),
    (14,  "Dataset-Column-Rename-Impact.mdx",
          "Renaming a dataset/dataflow column silently breaks card filters, sorts, and downstream references — safe rename procedure",
          "Jordan Jensen"),
    (17,  "Embed-Domo-in-Third-Party-Platforms.mdx",
          "Confluence, NetSuite, HubSpot, SharePoint, Salesforce embed methods and iframe constraints",
          "Mamta Bolaki"),
    (21,  "Filter-Funnel-and-PDP-Shield-Icons.mdx",
          "Hiding/showing the filter funnel and PDP shield on cards; page-variable behavior; Admin setting",
          "Ryan Despain"),
    (22,  "Filtering-on-Null-and-Empty-Values.mdx",
          "NULL vs empty string; IS NULL filter; NOT IN behavior; Beast Mode IFNULL workarounds",
          "Phil Fuchs"),
    (25,  "Card-Refresh-Timing-After-Dataset-Update.mdx",
          "How long cards take to reflect dataset changes; cache warm-up; force-refresh approach",
          "Chris Wright"),
    (26,  "DomoStats-vs-Governance-Datasets-Connector.mdx",
          "When to use DomoStats connector vs Domo Governance Datasets connector; field-level reference; deprecation status",
          "Dan Brinton"),
    (27,  "Trigger-Workbench-from-External-Scripts.mdx",
          "`wb.exe` CLI command syntax; triggering a Workbench job from Task Scheduler or CI scripts",
          "Tasleema Lallmamode"),
    (28,  "Embedded-Dashboard-Unfiltered-Data-Flash.mdx",
          "Why embedded/public-share dashboards briefly show unfiltered data on load; SSO and PDP timing fix",
          "Mamta Bolaki"),
    (32,  "Connecting-Unsupported-Data-Sources.mdx",
          "No native connector options: JSON No Code, HTTP connector, SFTP, Workbench ODBC, custom connector builder",
          "Tasleema Lallmamode"),
    (33,  "Zero-Fill-Missing-Date-Gaps-in-Charts.mdx",
          "Date densification in Magic ETL; zero-filling time series; empty pivot rows; calendar join pattern",
          "Andrea Henderson"),
    (44,  "Dataset-Archived-Lifecycle-State.mdx",
          "What the 'archived/not accessed' state means; how it blocks AI Readiness lineage; how to reactivate",
          "Jordan Jensen"),
    (47,  "Troubleshoot-Cards-Not-Updating.mdx",
          "Cards showing stale data after dataset refresh; color rules not applying; cache and permission causes",
          "Chris Wright"),
    (49,  "Period-over-Period-Calculations.mdx",
          "Prev week / prev month / prior year / year-boundary calculations in Beast Mode and Magic ETL; worked examples",
          "Phil Fuchs"),
    (50,  "Write-Data-from-Pro-Code-Apps-to-AppDB.mdx",
          "Writing back to AppDB collections from DDX Bricks / Pro-Code apps; sync to dataset; schema requirements",
          "Khushboo"),
    (55,  "Incremental-Ingestion-and-Lastvalue.mdx",
          "`lastvalue` parameter default, behavior, and edge cases; late-arriving and deleted source record handling",
          "Tasleema Lallmamode"),
    (56,  "Dataset-Column-Character-Limits.mdx",
          "~1,024 char text column limit; truncation of base64 images, JSON payloads, LLM output; workarounds",
          "Jordan Jensen"),
    (57,  "Pivot-Table-Census-Calendar-Join.mdx",
          "Date-range / calendar join pattern for length-of-visit / census modeling",
          "Andrea Henderson"),
    (61,  "Plot-Two-Date-Columns-on-One-Axis.mdx",
          "Data reshaping in Magic ETL to plot two date columns on a shared time axis",
          "Andrea Henderson"),
    (62,  "Data-Allocation-Split-Credit-in-ETL.mdx",
          "Reproducing proportional allocation / split-credit mapping in Magic ETL",
          "Andrea Henderson"),
    (64,  "Request-Access-Behavior.mdx",
          "How 'Request Access' and 'Request More Access' buttons work; who receives the request; admin configuration",
          "Dan Brinton"),
    (66,  "Troubleshoot-Office-PowerPoint-Add-In.mdx",
          "Connection failures, authentication errors, stale refresh; installation prerequisites",
          "Khushboo"),
    (69,  "Dashboard-Editor-Unresponsive-Multi-Select-Filter.mdx",
          "Dashboard editor hangs caused by misconfigured multi-select filter card; diagnosis and fix",
          "Chris Wright"),
    (71,  "Drill-to-Final-Data-Security.mdx",
          "What 'Drill to Final Data' exposes; detecting it is enabled; securing the master dataset",
          "Ryan Despain"),
    (77,  "Time-Interval-Bucketing-and-Dedup.mdx",
          "Assigning records to time buckets; deduplication within a window; Beast Mode vs Magic ETL approach",
          "Phil Fuchs"),
    (81,  "Schedule-Enterprise-Dataset-Copy.mdx",
          "Configuring a specific run time for Enterprise Dataset Copy jobs (not just 'run now')",
          "Jordan Jensen"),
    (82,  "Manage-Dataset-Error-Alerts.mdx",
          "Turning off / bulk-removing 'Error Loading Data' alerts after archiving or deleting datasets",
          "Jordan Jensen"),
    (83,  "Host-Images-for-Domo-Apps.mdx",
          "data-files URL pattern for storing and referencing internal images in Domo Apps and ETL",
          "Khushboo"),
    (84,  "GA4-BigQuery-Daily-Table-Nested-Data.mdx",
          "GA4 connector daily-table sprawl; unnesting `event_params`; BigQuery date-partitioned table approach",
          "Tasleema Lallmamode"),
    (86,  "Find-Domo-Version-and-Tool-Versions.mdx",
          "Where to find the Domo instance build number; Workbench version; plugin / add-in version",
          "Dan Brinton"),
    (89,  "Retrieve-Dataset-Source-Query-via-API.mdx",
          "API call to get the underlying connection/query for a dataset; connector metadata endpoints",
          "Ken Boyer"),
    (91,  "Remove-Bad-Rows-from-a-Dataset.mdx",
          "CLI full-replace artifact cleanup; removing a single erroneous row; append-mode dataset corrections",
          "Jordan Jensen"),
    (99,  "Domo-API-Changelog.mdx",
          "No published changelog for Domo APIs; versioning policy; how to track changes via DomoStats/release notes",
          "Ken Boyer"),
    (100, "App-Studio-Performance-with-Large-Datasets.mdx",
          "Load time causes; dataset size thresholds; optimization patterns (pre-aggregation, DataSet Views)",
          "Khushboo"),
    (103, "ETL-Credits-and-Consumption-Model.mdx",
          "Legacy ETL vs consumption credits; what counts as a 'manual run' vs 'significant change'; billing implications",
          "Andrea Henderson"),
    (107, "Multi-Language-Dashboards.mdx",
          "Dynamic language switching on dashboards; localization patterns; Beast Mode locale functions",
          "Chris Wright"),
    (109, "Custom-Card-Visuals-with-HTML-and-Bricks.mdx",
          "HTML card techniques; DDX Brick custom visuals; profile pictures, ERP-style detail panels",
          "Khushboo"),
]


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 3b-FORUM — CRITICAL UPDATE TARGETS (7 items)
# ─────────────────────────────────────────────────────────────────────────────

FORUM_UPDATE_CRITICAL = [
    # (rank, area, addition_needed, owning_pm, fact_check_needed)
    (2,  "Magic ETL troubleshooting",
         "Editor-level failure diagnostics: save failures, validate error, blank canvas bug",
         "Andrea Henderson",
         "Verify current error messages are accurate; confirm blank-canvas bug status (fixed or still present?)"),
    (3,  "Magic ETL troubleshooting",
         "'Preview vs Run' discrepancy FAQ; 'Not Runnable' error causes",
         "Andrea Henderson",
         "Confirm known causes of Preview vs Run differences; verify 'Not Runnable' error trigger conditions"),
    (4,  "App Studio card management",
         "Orphan card recovery procedure; delete-app-with-cards warning",
         "Khushboo",
         "Confirm orphan card recovery steps; verify what happens when you delete an app that contains cards"),
    (5,  "Beast Mode date functions",
         "YTD/MTD/rolling N months patterns with worked examples",
         "Phil Fuchs",
         "Verify date function examples are correct; confirm fiscal year behavior; review period boundary edge cases"),
    (8,  "Magic ETL preview documentation",
         "Explicit 400k row preview limit; run-to-here and sample tile workarounds",
         "Andrea Henderson",
         "Confirm 400k row limit is still accurate; verify run-to-here and sample tile work as described"),
    (10, "Beast Mode reference",
         "Aggregation context; grouping requirement; SUM(SUM(x)) pattern for subtotals",
         "Phil Fuchs",
         "Verify aggregation examples; confirm SUM(SUM(x)) subtotal pattern behavior"),
    (12, "Workflows forms/tasks",
         "Task Center setup; queue configuration; native approval flow patterns",
         "Ryan Despain",
         "Verify Task Center setup steps; confirm queue config options; review approval flow pattern accuracy"),
]


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 4 — RETIREMENTS AND URGENT FIXES
# ─────────────────────────────────────────────────────────────────────────────

PHASE4_RETIREMENTS = [
    # (batch, pm, count, action, notes)
    ("Workbench 4 articles", "Tasleema Lallmamode", 37, "Archive",
     "D1 confirmed. 37 EOL articles for an end-of-life product version."),
    ("DataFusion articles", "Andrea Henderson", 11, "Archive",
     "DataFusion discontinued. 6 Deprecate + 5 Mark as Legacy. Must add `DataFusion-Migration-Guide.mdx` pointing users to Magic ETL equivalents before or alongside archival."),
    ("Old Magic ETL tile articles", "Andrea Henderson", 15, "Archive (1 Keep)",
     "15 articles to Archive. Exception: `Create a Recursive/Snapshot Old Magic ETL DataFlow` — keep this one."),
    ("Defunct-service connectors", "Tasleema Lallmamode", 111, "Archive / remove from nav",
     "111 verified dead-service articles (LinkedIn API v1, Pinterest, StumbleUpon, Simply Measured, IBM Coremetrics, GetThere, Moz, Snowflake Writeback, DCM via Google Cloud Storage, etc.)."),
    ("CourseBuilder articles", "Khushboo", 16, "Archive (pending D10)",
     "Support Audit flags CourseBuilder as retired from Domo Appstore. 16 articles (3 Deprecate, 5 Legacy, 4 Needs Review, 4 pending). Confirm with PM; archive all 16 if confirmed retired."),
]

PHASE4_URGENT_FIXES = [
    # (area, pm, urgency_note)
    ("Snowflake Connector + Snowflake Unload V2", "Tasleema Lallmamode",
     "URGENT — FIX NOW. Snowflake retired key-pair/password authentication November 2025. These articles actively mislead customers who are actively failing connections. Fix with `update-kb-article` before Phase 4 begins."),
]


# ─────────────────────────────────────────────────────────────────────────────
# domo_area → PM keyword mapping (for forum gap assignment)
# ─────────────────────────────────────────────────────────────────────────────

# Ordered list of (keyword, pm) — checked in order; first match wins.
# More specific phrases first.
AREA_PM_RULES = [
    ("Domo Everywhere",         "Mamta Bolaki"),
    ("Private Embed",           "Mamta Bolaki"),
    ("Public Embed",            "Mamta Bolaki"),
    ("Embed",                   "Mamta Bolaki"),
    ("Sandbox",                 "Mamta Bolaki"),
    ("Governance Toolkit",      "Ryan Despain"),
    ("PDP",                     "Ryan Despain"),
    ("Personalized Data",       "Ryan Despain"),
    ("Workflows",               "Ryan Despain"),
    ("Workflow",                "Ryan Despain"),
    ("Approvals",               "Ryan Despain"),
    ("Projects & Tasks",        "Ryan Despain"),
    ("Beast Mode",              "Phil Fuchs"),
    ("beast mode",              "Phil Fuchs"),
    ("Period over Period",      "Phil Fuchs"),
    ("Combined Schema",         "Phil Fuchs"),
    ("Data View",               "Phil Fuchs"),
    ("Fusions",                 "Phil Fuchs"),
    ("Magic ETL",               "Andrea Henderson"),
    ("magic etl",               "Andrea Henderson"),
    ("SQL DataFlow",            "Andrea Henderson"),
    ("DataFlow",                "Andrea Henderson"),
    ("Data Flow",               "Andrea Henderson"),
    ("Auto ML",                 "Andrea Henderson"),
    ("Cloud Amplifier",         "Jordan Jensen"),
    ("Federated",               "Jordan Jensen"),
    ("AppStore",                "Jordan Jensen"),
    ("DataSet",                 "Jordan Jensen"),
    ("Dataset",                 "Jordan Jensen"),
    ("Data Center",             "Jordan Jensen"),
    ("Workbench",               "Tasleema Lallmamode"),
    ("workbench",               "Tasleema Lallmamode"),
    ("Third Party Connector",   "Tasleema Lallmamode"),
    ("Connector",               "Tasleema Lallmamode"),
    ("connector",               "Tasleema Lallmamode"),
    ("Activity Log",            "Dan Brinton"),
    ("DomoStats",               "Dan Brinton"),
    ("Smart Alerts",            "Dan Brinton"),
    ("Alerts",                  "Dan Brinton"),
    ("Alert",                   "Dan Brinton"),
    ("NLG",                     "Dan Brinton"),
    ("Buzz",                    "Dan Brinton"),
    ("Goals",                   "Dan Brinton"),
    ("SSO",                     "Dan Brinton"),
    ("Single Sign-On",          "Dan Brinton"),
    ("ABAC",                    "Dan Brinton"),
    ("Admin",                   "Dan Brinton"),
    ("admin",                   "Dan Brinton"),
    ("Governance & Security",   "Dan Brinton"),
    ("Content Organization",    "Dan Brinton"),
    ("Navigation",              "Dan Brinton"),
    ("User Management",         "Dan Brinton"),
    ("App Studio",              "Khushboo"),
    ("app studio",              "Khushboo"),
    ("Pro-code",                "Khushboo"),
    ("DDX",                     "Khushboo"),
    ("AppDB",                   "Khushboo"),
    ("Bricks",                  "Khushboo"),
    ("Code Engine",             "Khushboo"),
    ("Office",                  "Khushboo"),
    ("Add-in",                  "Khushboo"),
    ("Plugin",                  "Khushboo"),
    ("Publication",             "Khushboo"),
    ("Jupyter",                 "Ken Boyer"),
    ("Domo AI",                 "Ken Boyer"),
    ("AI Service",              "Ken Boyer"),
    ("CLI",                     "Ken Boyer"),
    ("Fileset",                 "Ken Boyer"),
    ("Unstructured",            "Ken Boyer"),
    ("MCP",                     "Ken Boyer"),
    ("API",                     "Ken Boyer"),
    ("Dashboard",               "Chris Wright"),
    ("Dashboards",              "Chris Wright"),
    ("dashboard",               "Chris Wright"),
    ("Charting",                "Chris Wright"),
    ("Analyzer",                "Chris Wright"),
    ("Chart",                   "Chris Wright"),
    ("Export",                  "Chris Wright"),
    ("Reporting",               "Chris Wright"),
    ("Slideshow",               "Chris Wright"),
    ("Worksheet",               "Chris Wright"),
    ("Doc Cards",               "Chris Wright"),
    ("Mobile",                  "Chris Wright"),
    ("AI",                      "Ken Boyer"),
]


def area_to_pm(domo_area: str) -> str:
    """Map a domo_area string to the most likely PM name."""
    if not domo_area:
        return "Unknown"
    for keyword, pm in AREA_PM_RULES:
        if keyword in domo_area:
            return pm
    return "Unknown"


# ─────────────────────────────────────────────────────────────────────────────
# PARSING
# ─────────────────────────────────────────────────────────────────────────────

def load_ownership_reference(path: Path) -> dict:
    """
    Parse Article-PM-Ownership-Reference.mdx markdown table.
    Returns: {pm_name: {"features": set(), "articles": [(feature, title, filename)]}}
    """
    index = defaultdict(lambda: {"features": set(), "articles": []})
    if not path.exists():
        print(f"  WARNING: {path} not found — ownership data will be empty")
        return index

    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Match pipe-table rows: | Feature | Title | Filename | PM |
    row_pattern = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", re.MULTILINE)
    for match in row_pattern.finditer(content):
        feature, title, filename, pm = (c.strip() for c in match.groups())
        # Skip header rows and separator rows
        if feature.lower() in ("feature", "---", "") or "---" in feature:
            continue
        if not pm or pm.lower() == "pm" or "---" in pm:
            continue
        # Strip markdown links from title/filename
        title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)
        filename = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", filename)
        pm = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", pm).strip()
        if pm and feature and filename:
            index[pm]["features"].add(feature)
            index[pm]["articles"].append((feature, title, filename))

    return index


def load_forum_gaps(path: Path) -> list:
    """Load _gaps_with_support.json. Returns list of gap dicts."""
    if not path.exists():
        print(f"  WARNING: {path} not found — forum gap data will be empty")
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("gaps", [])


# ─────────────────────────────────────────────────────────────────────────────
# BRIEF GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def generate_brief(pm_name: str, pm_ownership: dict, all_gaps: list) -> str:
    """Generate a markdown review brief for one PM."""
    features = sorted(pm_ownership.get("features", set()))
    articles = pm_ownership.get("articles", [])
    article_count = len(articles)

    # Count articles per feature
    feature_counts = defaultdict(int)
    for feat, _, _ in articles:
        feature_counts[feat] += 1

    lines = []

    # ── Header ────────────────────────────────────────────────────────────────
    lines += [
        f"# PM Review Brief: {pm_name}",
        "",
        f"**Prepared for:** KB Restructure PM Review Meeting",
        f"**Features owned:** {', '.join(features) if features else '(none mapped)'}",
        f"**Total articles in your area:** {article_count}",
        "",
        "> This document is your meeting guide. It shows how your content is being reorganized,",
        "> which AI-generated articles need your fact-check, which articles need a dedicated",
        "> info-gathering meeting before they can be written, and what changes are being made",
        "> to your content area in response to Support KB Audit and community forum gap findings.",
        "",
        "---",
        "",
    ]

    # ── Section 1: Content Reorganization ─────────────────────────────────────
    lines += [
        "## 1. How Your Content Is Being Reorganized",
        "",
        "The KB is moving from a flat feature encyclopedia to a story-driven structure organized",
        "around **11 pillars** (user workflows). The table below shows where each of your feature",
        "areas lands in the new structure.",
        "",
        "| Feature | Articles | New Location |",
        "|---------|----------|--------------|",
    ]
    for feat in sorted(feature_counts.keys()):
        count = feature_counts[feat]
        pillar = FEATURE_PILLAR.get(feat, f"TBD — not yet mapped")
        lines.append(f"| {feat} | {count} | {pillar} |")

    lines += [""]

    # Structural notes for this PM
    notes = STRUCTURAL_NOTES.get(pm_name, [])
    if notes:
        lines += ["### Notable Navigation Changes", ""]
        for note in notes:
            lines += [f"- {note}", ""]

    lines += ["---", ""]

    # ── Section 2: AI-Generated Articles to Fact-Check ────────────────────────
    pm_phase3a = [(fn, title, pillar, synth, claims)
                  for fn, title, pillar, pm, synth, claims in PHASE3A_ARTICLES
                  if pm == pm_name]

    lines += [
        "## 2. AI-Generated Articles — Your Fact-Check Required",
        "",
    ]

    if pm_phase3a:
        lines += [
            "These articles will be synthesized by AI from existing KB content in Phase 3a.",
            "**They need your review before publishing.** Please read the draft and verify the",
            "key claims listed — especially anything about product behavior, limitations, or",
            "recommended patterns.",
            "",
            "| # | Article | Synthesized From | Key Claims to Verify |",
            "|---|---------|------------------|---------------------|",
        ]
        for i, (fn, title, pillar, synth, claims) in enumerate(pm_phase3a, 1):
            lines.append(f"| {i} | `{fn}` ({pillar}) | {synth} | {claims} |")
        lines += [""]
    else:
        lines += [
            "_No Phase 3a synthesized articles are assigned to your feature area._",
            "",
        ]

    lines += ["---", ""]

    # ── Section 3: Gap Articles — Meeting Required ─────────────────────────────
    pm_input = [(fn, title, what) for fn, title, pm, what in PHASE3A_PM_ARTICLES if pm == pm_name]
    pm_forum_critical_new = [(r, fn, summary, fc) for r, fn, summary, pm, fc in FORUM_NEW_CRITICAL if pm == pm_name]
    pm_forum_high_new = [(r, fn, summary) for r, fn, summary, pm in FORUM_NEW_HIGH if pm == pm_name]

    lines += [
        "## 3. Gap Articles — Information-Gathering Meeting Required",
        "",
        "These articles **cannot be written without your input**. A short dedicated meeting",
        "(30 min each, or async written response) is needed before work can begin.",
        "",
    ]

    has_gaps = pm_input or pm_forum_critical_new or pm_forum_high_new

    if pm_input:
        lines += [
            "### 3a. PM Input Articles (from original restructure plan)",
            "",
            "| Article | What You Need to Provide |",
            "|---------|--------------------------|",
        ]
        for fn, title, what in pm_input:
            lines.append(f"| `{fn}` — *{title}* | {what} |")
        lines += [""]

    if pm_forum_critical_new:
        lines += [
            "### 3b. Critical Forum-Gap New Articles",
            "",
            "These topics were the most-requested missing knowledge in the community forums",
            "(Critical priority). Each needs a new article and your input to ensure accuracy.",
            "",
            "| Rank | Filename | Topic | Fact-Check Info Needed From You |",
            "|------|----------|-------|--------------------------------|",
        ]
        for rank, fn, summary, fc in pm_forum_critical_new:
            lines.append(f"| {rank} | `{fn}` | {summary} | {fc} |")
        lines += [""]

    if pm_forum_high_new:
        lines += [
            "### 3c. High Priority Forum-Gap New Articles",
            "",
            "These topics were High-priority missing knowledge in the community forums.",
            "AI can draft these from existing documentation, but your review is needed",
            "before publishing.",
            "",
            "| Rank | Filename | Topic |",
            "|------|----------|-------|",
        ]
        for rank, fn, summary in pm_forum_high_new:
            lines.append(f"| {rank} | `{fn}` | {summary} |")
        lines += [""]

    if not has_gaps:
        lines += [
            "_No dedicated info-gathering articles are currently assigned to your area._",
            "",
        ]

    lines += ["---", ""]

    # ── Section 4: Support Gap Integration Changes ─────────────────────────────
    pm_retirements = [(batch, count, action, notes)
                      for batch, pm, count, action, notes in PHASE4_RETIREMENTS
                      if pm == pm_name]
    pm_urgent = [(area, note) for area, pm, note in PHASE4_URGENT_FIXES if pm == pm_name]
    pm_crit_updates = [(rank, area, addition, fc)
                       for rank, area, addition, pm, fc in FORUM_UPDATE_CRITICAL
                       if pm == pm_name]

    # Forum High update gaps assigned to this PM (from JSON)
    pm_forum_high_updates = [
        g for g in all_gaps
        if g.get("recommendation") == "update"
        and g.get("priority") in ("High",)
        and area_to_pm(g.get("domo_area", "")) == pm_name
    ]
    pm_forum_high_updates.sort(key=lambda g: g.get("rank", 9999))

    lines += [
        "## 4. Changes Flagged by Support Gap Integrations",
        "",
        "Two gap-fill analyses have been integrated into the restructure plan. This section",
        "shows what changes are planned in your content area and what fact-check input reduces",
        "hallucination risk in the updated articles.",
        "",
    ]

    # 4a: Support KB Audit
    lines += ["### 4a. Support KB Audit Findings (Phase 4)", ""]

    if pm_urgent:
        lines += ["**URGENT — Fix before Phase 4:**", ""]
        for area, note in pm_urgent:
            lines += [f"> **{area}**", f"> {note}", ""]

    if pm_retirements:
        lines += [
            "**Retirement batches in your area (Phase 4 execution plan):**",
            "",
            "| Batch | Count | Action | Notes |",
            "|-------|-------|--------|-------|",
        ]
        for batch, count, action, notes in pm_retirements:
            lines.append(f"| {batch} | {count} | {action} | {notes} |")
        lines += [""]
    elif not pm_urgent:
        lines += ["_No Support KB Audit retirements are currently assigned to your area._", ""]

    # 4b: Forum update targets
    lines += ["### 4b. Community Forum Gap Analysis — Update Targets", ""]

    if pm_crit_updates:
        lines += [
            "**Critical update targets** (address alongside or immediately after Phase 3a):",
            "",
            "| Rank | Article Area | Addition Needed | Fact-Check Info Needed |",
            "|------|-------------|-----------------|------------------------|",
        ]
        for rank, area, addition, fc in pm_crit_updates:
            lines.append(f"| {rank} | {area} | {addition} | {fc} |")
        lines += [""]

    if pm_forum_high_updates:
        lines += [
            f"**High priority update targets** ({len(pm_forum_high_updates)} articles in your area):",
            "",
            "| Rank | Score | Topic | Affected Area | Specific Addition Needed |",
            "|------|-------|-------|---------------|--------------------------|",
        ]
        for g in pm_forum_high_updates[:20]:  # cap at 20 to keep brief readable
            rank = g.get("rank", "?")
            score = g.get("score", 0)
            topic = g.get("topic", "")[:80]
            area = g.get("domo_area", "")[:40]
            gap_detail = g.get("gap_detail", "")[:100]
            lines.append(f"| {rank} | {score:.1f} | {topic} | {area} | {gap_detail} |")
        if len(pm_forum_high_updates) > 20:
            lines += ["", f"_...and {len(pm_forum_high_updates) - 20} more. See `_gaps_with_support.json` for full list._"]
        lines += [""]
    else:
        lines += ["_No High-priority forum update targets mapped to your area._", ""]

    if not pm_crit_updates and not pm_forum_high_updates and not pm_retirements and not pm_urgent:
        lines += ["_No support gap integration changes are flagged for your area at this time._", ""]

    lines += ["---", ""]

    # ── Quick Actions Summary ─────────────────────────────────────────────────
    lines += [
        "## Quick Actions Summary",
        "",
        "A prioritized list of everything this document is asking of you:",
        "",
        "| # | Action | Type | Est. Effort |",
        "|---|--------|------|------------|",
    ]

    action_num = 1

    # Urgent fixes first
    for area, note in pm_urgent:
        lines.append(f"| {action_num} | Fix `{area}` auth/accuracy issue | **URGENT fix** | 1–2 hrs |")
        action_num += 1

    # Retirement decisions
    for batch, count, action, _ in pm_retirements:
        if "pending" in action.lower():
            lines.append(f"| {action_num} | Confirm: {batch} ({count} articles) — retire or keep? | Decision | 15 min |")
            action_num += 1

    # Phase 3a fact-checks
    for fn, title, _, _, _ in pm_phase3a[:5]:  # top 5 only in summary
        lines.append(f"| {action_num} | Read and fact-check `{fn}` | Fact-check | 30–45 min |")
        action_num += 1
    if len(pm_phase3a) > 5:
        lines.append(f"| {action_num} | Read and fact-check remaining {len(pm_phase3a) - 5} Phase 3a articles | Fact-check | ~30 min each |")
        action_num += 1

    # PM input articles
    for fn, title, _ in pm_input:
        lines.append(f"| {action_num} | Provide input for `{fn}` | Info meeting | 30 min |")
        action_num += 1

    # Critical new articles
    for rank, fn, _, fc in pm_forum_critical_new:
        lines.append(f"| {action_num} | Review/validate `{fn}` (Rank {rank} community request) | Fact-check | 20–30 min |")
        action_num += 1

    # Critical update validations
    for rank, area, addition, _ in pm_crit_updates:
        lines.append(f"| {action_num} | Validate additions to: {area} (Rank {rank}) | Review | 20 min |")
        action_num += 1

    # Open decisions
    for note in notes:
        if "[D" in note:
            d_match = re.search(r"\[D(\d+)", note)
            d_num = d_match.group(0) if d_match else ""
            lines.append(f"| {action_num} | Decision needed {d_num}: see Section 1 notes | Decision | 10 min |")
            action_num += 1

    lines += ["", "---", "", f"_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-IA-SPEC.md, _gaps_with_support.json, and RESTRUCTURE-PROGRESS.md._", ""]

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("Loading data...")
    ownership = load_ownership_reference(OWNERSHIP_FILE)
    gaps = load_forum_gaps(GAPS_FILE)
    print(f"  Ownership reference: {sum(len(v['articles']) for v in ownership.values())} articles across {len(ownership)} PMs")
    print(f"  Forum gaps: {len(gaps)} gaps loaded")

    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"\nGenerating briefs in {OUTPUT_DIR.relative_to(REPO_ROOT)}/...")

    # All PMs — union of ownership reference + hardcoded PM lists
    all_pms_from_data = set(ownership.keys())
    all_pms_hardcoded = set()
    for _, _, _, pm, _, _ in PHASE3A_ARTICLES:
        all_pms_hardcoded.add(pm)
    for _, _, pm, _ in PHASE3A_PM_ARTICLES:
        all_pms_hardcoded.add(pm)
    for _, _, _, pm, _ in FORUM_NEW_CRITICAL:
        all_pms_hardcoded.add(pm)
    all_pms = sorted(all_pms_from_data | all_pms_hardcoded)

    for pm_name in all_pms:
        pm_data = ownership.get(pm_name, {"features": set(), "articles": []})
        brief = generate_brief(pm_name, pm_data, gaps)
        safe_name = pm_name.replace(" ", "-").replace("/", "-").replace("(", "").replace(")", "")
        out_path = OUTPUT_DIR / f"{safe_name}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(brief)
        article_count = len(pm_data["articles"])
        print(f"  ✓ {out_path.name}  ({article_count} articles)")

    print(f"\nDone — {len(all_pms)} briefs written to pm-review-briefs/")


if __name__ == "__main__":
    main()
