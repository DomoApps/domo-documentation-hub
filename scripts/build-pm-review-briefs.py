#!/usr/bin/env python3
"""
Build per-PM review briefs for KB restructure PM meetings.

Reads:
  - Article-PM-Ownership-Reference.mdx  (PM → feature → article mapping)
  - _gaps_with_support.json              (community forum gap analysis)
  - RESTRUCTURE-MANIFEST.md              (canonical Phase 3a-Forum written +
                                          deferred article tables — source of truth)
  - s/article/*.mdx                      (scanned for embedded [pm-input] markers)

Outputs one .md file per PM in pm-review-briefs/.

The Phase 3a-Forum data (which new articles were written vs. deferred, and which
drafted articles still carry open [pm-input] placeholders) is NOT hardcoded here —
it is parsed from RESTRUCTURE-MANIFEST.md and the article files themselves so the
briefs can never drift from the manifest. See parse_manifest_forum_* below.

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
MANIFEST_FILE = REPO_ROOT / "RESTRUCTURE-MANIFEST.md"
ARTICLE_DIR = REPO_ROOT / "s" / "article"
OUTPUT_DIR = REPO_ROOT / "pm-review-briefs"

# Features excluded from PM briefs entirely — their articles are outside
# the scope of the restructure and require no PM review action.
EXCLUDED_FEATURES = {
    "Release Management",  # Historical release notes — not restructured
}


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
        "**Workbench consolidation:** Workbench 4 (36 EN articles) → Legacy (D1 confirmed); moves to the Archive group with a `<LegacyNote/>` in Phase 4.6. Workbench 5.1 gets a clearly-labeled Legacy sub-group.",
        "**Connector merges DONE (2026-08-28):** 14 exact-title duplicate connectors were merged/deleted — keeper kept, unique fields folded in, nav entries and inbound links fixed. See RESTRUCTURE-MANIFEST.md › Connector Merges.",
        "**8 title-collisions were NOT duplicates (deferred, need retitling):** distinct connectors sharing a title — Documents-surface (SFTP, Amazon S3, GitHub), variants (WordPress self-hosted, Magento OAuth, Kendra query). For **LinkedIn** and **Google Ads**, the *current* connector was retained on review; the *deprecated* generation (LinkedIn V1, legacy AdWords) is now a Retired candidate.",
        "**Defunct-service connectors:** 12 named dead-service articles + the Deprecate superset (185 EN) are Retired candidates (staged for 4.6) — confirm the true dead set.",
    ],
    "Andrea Henderson": [
        "**DataFusion retirement:** The 4 EN DataFusion articles are staged for Retired in Phase 4.6. Replacement SHIPPED: `DataFusion-Migration-Guide.mdx` (points users to Magic ETL equivalents) — please fact-check it for accuracy.",
        "**Old Magic ETL tile articles (7):** 7 EN old-tile-interface articles staged for Retired. 1 article (`360043428113` Create a Recursive/Snapshot Old Magic ETL DataFlow) is explicitly kept.",
    ],
    "Khushboo": [
        "**CourseBuilder (9 EN articles):** Support KB Audit flags CourseBuilder as retired/removed from Domo Appstore. Staged for Retired in Phase 4.6. Pending D10: confirm CourseBuilder is gone from the product before the nav rebuild.",
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
# MANIFEST PM-INPUT FLAGS — cross-cutting items with no article marker
#
# Open [pm-input] questions embedded in article files are picked up automatically
# by scan_article_pm_inputs() (below). This constant is ONLY for manifest-recorded
# PM-input flags that are NOT tied to a single article's inline marker and therefore
# cannot be scanned — e.g. a link issue spanning several files.
#
# Source: RESTRUCTURE-MANIFEST.md › Phase 3a › "PM input flag (add to Phase 4.5 briefs)"
# Format: {pm_name: [(scope_label, ask), ...]}
# ─────────────────────────────────────────────────────────────────────────────

MANIFEST_PM_INPUT_FLAGS = {
    # Getting Started role articles all link to the same `data-consumer-training`
    # eLearning URL. No single article carries a [pm-input] marker for this, so it
    # is tracked here. Routed to Jordan Jensen, who owns Education + Onboarding.
    "Jordan Jensen": [
        (
            "Getting Started role articles — eLearning course URLs",
            "All Getting Started role articles (Admins, App Builders, Data Engineers, "
            "Developers) currently link to the same `data-consumer-training` eLearning "
            "course URL, which is likely wrong for non-consumer roles. Confirm the correct "
            "course URL for each role (coordinate with the Education / Domo University team).",
        ),
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
# PHASE 3a-FORUM — NEW ARTICLES FROM FORUM GAP ANALYSIS
#
# The written vs. deferred split is NOT hardcoded. It is parsed at run time from
# RESTRUCTURE-MANIFEST.md by parse_manifest_forum_written() (the "Net-New Articles"
# table — articles already drafted, needing fact-check) and
# parse_manifest_forum_deferred() (the "Deferred to PM Briefs" table — articles that
# cannot be written without PM input). This guarantees the briefs match the manifest.
# ─────────────────────────────────────────────────────────────────────────────


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
    # Status 2026-08-28: classified + STAGED for Phase 4.6 (status stamping + nav
    # moves happen after PM sign-off). Counts are verified English s/article/ files.
    ("Workbench 4 articles", "Tasleema Lallmamode", 36, "→ Legacy (staged for 4.6)",
     "D1 confirmed. 36 EN articles for an end-of-life product version. Confirm Legacy: feature still runs at some sites, WB5 is the replacement, no announced removal date."),
    ("DataFusion articles", "Andrea Henderson", 4, "→ Retired (staged for 4.6)",
     "DataFusion discontinued. 4 EN articles. Replacement SHIPPED: `DataFusion-Migration-Guide.mdx` (Magic ETL equivalents) — please also fact-check that guide for accuracy. Confirm Retired: feature gone from product."),
    ("Old Magic ETL tile articles", "Andrea Henderson", 7, "→ Retired (1 Keep; staged for 4.6)",
     "7 EN tile-interface articles → Retired. KEEP exception: `360043428113` (Create a Recursive/Snapshot Old Magic ETL DataFlow). Confirm the old tile UI is fully replaced/inaccessible."),
    ("Defunct-service connectors", "Tasleema Lallmamode", "12 named + superset", "→ Retired (staged for 4.6)",
     "12 verified dead-service articles named (LinkedIn API v1, Pinterest x2, StumbleUpon, Simply Measured, Salesforce Desk, IBM Coremetrics, GetThere, Moz, Adobe Analytics Adv Legacy, DCM via GCS, Azure Data Lake Store) + legacy Google Ads/AdWords reroute. The Category=Data Connection + Deprecate superset (185 EN) is attached for you to confirm which are truly dead."),
    ("CourseBuilder articles", "Khushboo", 9, "→ Retired (pending D10; staged for 4.6)",
     "Support Audit flags CourseBuilder as retired from Domo Appstore. 9 EN articles. D10: confirm CourseBuilder is gone from the product; retire all if confirmed."),
]

PHASE4_URGENT_FIXES = [
    # (area, pm, urgency_note)
    ("Snowflake Connector + Snowflake Unload V2", "Tasleema Lallmamode",
     "DONE (Phase 3b, 2026-07-15). Snowflake retired key-pair/password auth Nov 2025; 7 Snowflake connector articles were updated (retirement language, Warning callouts, migration-section rewrite). Flagged here for your awareness/verification."),
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

    # Replace escaped pipes (\|) in cell content with a placeholder so the
    # column-splitting regex treats them as literal characters, not separators.
    PIPE_PLACEHOLDER = "\x00PIPE\x00"
    content = content.replace(r"\|", PIPE_PLACEHOLDER)

    # Match pipe-table rows: | Feature | Title | Filename | PM |
    row_pattern = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", re.MULTILINE)
    for match in row_pattern.finditer(content):
        feature, title, filename, pm = (
            c.strip().replace(PIPE_PLACEHOLDER, "|") for c in match.groups()
        )
        # Skip header rows and separator rows
        if feature.lower() in ("feature", "---", "") or "---" in feature:
            continue
        if not pm or pm.lower() == "pm" or "---" in pm:
            continue
        # Skip features excluded from the restructure scope
        if feature in EXCLUDED_FEATURES:
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


def _extract_table_rows(text: str, start_marker: str, end_marker: str, expected_cols: int) -> list:
    """
    Return the data rows of the first pipe table between start_marker and
    end_marker. Header and separator rows are dropped. Each row is normalized
    to exactly `expected_cols` cells: extra cells (e.g. a stray '|' inside a
    note) are merged back into the last column; short rows are skipped.
    """
    start = text.find(start_marker)
    if start == -1:
        return []
    search_from = start + len(start_marker)
    end = text.find(end_marker, search_from) if end_marker else -1
    if end == -1:
        end = len(text)
    segment = text[start:end]

    rows = []
    for line in segment.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        # Separator row (all dashes)?
        if all(set(c) <= {"-", ":"} and c for c in cells):
            continue
        if len(cells) < expected_cols:
            continue
        if len(cells) > expected_cols:
            head = cells[: expected_cols - 1]
            tail = " | ".join(cells[expected_cols - 1:])
            cells = head + [tail]
        rows.append(cells)
    return rows


def _rank_from(text: str) -> int:
    """Pull a leading rank number out of strings like '#26 / n/a' or '26'."""
    m = re.search(r"\d+", text or "")
    return int(m.group(0)) if m else 9999


def parse_manifest_forum_written(manifest_text: str) -> list:
    """
    Parse the 'Phase 3a-Forum — Net-New Articles' table (articles already
    drafted). Returns list of dicts:
      {rank, filename, title, pm, notes, has_pm_input}
    These need PM fact-check, NOT creation.
    """
    rows = _extract_table_rows(
        manifest_text,
        "## Phase 3a-Forum — Net-New Articles",
        "### Phase 3a-Forum — Deferred to PM Briefs",
        expected_cols=8,
    )
    out = []
    for cells in rows:
        filename, title, disposition, pm, rank_score, _screens, _gates, notes = cells[:8]
        if filename.lower() in ("filename", ""):
            continue
        filename = filename.strip("`")
        out.append({
            "rank": _rank_from(rank_score),
            "filename": filename,
            "title": title,
            "pm": pm,
            "notes": notes,
            "has_pm_input": "[pm-input]" in notes,
        })
    return out


def parse_manifest_forum_deferred(manifest_text: str) -> list:
    """
    Parse the 'Phase 3a-Forum — Deferred to PM Briefs' table (articles NOT
    written — the KB lacks source material). Returns list of dicts:
      {rank, filename, pm, what}
    These cannot be written without PM input.
    """
    rows = _extract_table_rows(
        manifest_text,
        "### Phase 3a-Forum — Deferred to PM Briefs",
        "\n---\n",
        expected_cols=4,
    )
    out = []
    for cells in rows:
        rank, filename, pm, what = cells[:4]
        if rank.lower() in ("rank", ""):
            continue
        out.append({
            "rank": _rank_from(rank),
            "filename": filename.strip("`"),
            "pm": pm,
            "what": what,
        })
    return out


# Matches a whole embedded pm-input comment: {/* [pm-input] Name — ask... */}
_PM_INPUT_RE = re.compile(r"\{/\*\s*\[pm-input\]\s*(.*?)\*/\}", re.DOTALL)
# Splits "Name — ask" (em-dash or colon separator) into (name, ask).
_PM_INPUT_SPLIT = re.compile(r"\s*(.+?)\s*[—:]\s*(.*)", re.DOTALL)


def scan_article_pm_inputs(article_dir: Path) -> list:
    """
    Scan every article .mdx for embedded {/* [pm-input] Name — ask */} markers.
    Returns list of dicts: {filename, pm, ask}. This is the authoritative source
    for open placeholders in drafted articles — it can never drift from the files.
    """
    out = []
    if not article_dir.exists():
        print(f"  WARNING: {article_dir} not found — article pm-input scan skipped")
        return out
    for path in sorted(article_dir.glob("*.mdx")):
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if "[pm-input]" not in content:
            continue
        for m in _PM_INPUT_RE.finditer(content):
            inner = m.group(1).strip()
            sm = _PM_INPUT_SPLIT.match(inner)
            if not sm:
                continue
            pm = sm.group(1).strip()
            ask = re.sub(r"\s+", " ", sm.group(2)).strip()
            out.append({"filename": path.name, "pm": pm, "ask": ask})
    return out


def pm_cell_matches(cell: str, pm_name: str) -> bool:
    """
    True if pm_name is named in a manifest PM cell. Handles parenthetical
    suffixes ('Ken Boyer (CLI/APIs)') and shared cells ('Phil Fuchs / Andrea
    Henderson') by stripping '(...)' and splitting on '/'.
    """
    cleaned = re.sub(r"\([^)]*\)", "", cell)
    parts = [p.strip() for p in cleaned.split("/")]
    return pm_name in parts


# ─────────────────────────────────────────────────────────────────────────────
# BRIEF GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def generate_brief(pm_name: str, pm_ownership: dict, all_gaps: list, forum: dict) -> str:
    """Generate a markdown review brief for one PM.

    `forum` carries the manifest-derived Phase 3a-Forum data:
      {"written": [...], "deferred": [...], "checkpoints": [...]}
    """
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

    # ── Section 3: New Forum-Gap Articles + Open Placeholders ──────────────────
    pm_input = [(fn, title, what) for fn, title, pm, what in PHASE3A_PM_ARTICLES if pm == pm_name]
    # Written forum articles (drafted; need fact-check) — matched on manifest PM cell.
    pm_forum_written = sorted(
        [w for w in forum["written"] if pm_cell_matches(w["pm"], pm_name)],
        key=lambda w: w["rank"],
    )
    # Deferred forum articles (not written; need PM input to begin).
    pm_forum_deferred = sorted(
        [d for d in forum["deferred"] if pm_cell_matches(d["pm"], pm_name)],
        key=lambda d: d["rank"],
    )
    # Open [pm-input] placeholders: embedded article markers (scanned) + manifest flags.
    pm_checkpoints = [(c["filename"], c["ask"]) for c in forum["checkpoints"]
                      if c["pm"] == pm_name]
    pm_checkpoints += [(scope, ask) for scope, ask in MANIFEST_PM_INPUT_FLAGS.get(pm_name, [])]

    lines += [
        "## 3. New Forum-Gap Articles and Open Placeholders",
        "",
        "New articles in your area from the community-forum gap analysis (and the original",
        "restructure plan). Some are **already drafted and need your fact-check**; others",
        "**cannot be written until you supply information**. The two are separated below so",
        "it's clear which is which.",
        "",
    ]

    has_gaps = pm_input or pm_forum_written or pm_forum_deferred or pm_checkpoints

    if pm_input:
        lines += [
            "### 3a. PM Input Articles (from original restructure plan)",
            "",
            "Not yet written — each needs a short info-gathering conversation before drafting.",
            "",
            "| Article | What You Need to Provide |",
            "|---------|--------------------------|",
        ]
        for fn, title, what in pm_input:
            lines.append(f"| `{fn}` — *{title}* | {what} |")
        lines += [""]

    if pm_forum_written:
        lines += [
            "### 3b. Forum-Gap Articles Already Drafted — Fact-Check Required",
            "",
            "These articles have been **written** in response to the highest-demand community",
            "forum gaps. Please read each draft and verify accuracy. A ⚠️ flag means the draft",
            "also contains an open `[pm-input]` placeholder — see Section 3d for the exact ask.",
            "",
            "| Rank | Article | What Was Synthesized / What to Verify |",
            "|------|---------|---------------------------------------|",
        ]
        for w in pm_forum_written:
            flag = " ⚠️" if w["has_pm_input"] else ""
            title = w["title"] or w["filename"]
            lines.append(f"| {w['rank']} | `{w['filename']}` — *{title}*{flag} | {w['notes']} |")
        lines += [""]

    if pm_forum_deferred:
        lines += [
            "### 3c. Forum-Gap Articles Awaiting Your Input — Cannot Be Written Yet",
            "",
            "These forum gaps **cannot be written without your input** — the KB has no source",
            "material and the mechanics are Domo-proprietary. A short dedicated meeting (or an",
            "async written answer) is needed before drafting can begin.",
            "",
            "| Rank | Intended Article | What You Need to Supply |",
            "|------|------------------|-------------------------|",
        ]
        for d in pm_forum_deferred:
            lines.append(f"| {d['rank']} | `{d['filename']}` | {d['what']} |")
        lines += [""]

    if not has_gaps:
        lines += [
            "_No new forum-gap articles are currently assigned to your area._",
            "",
        ]

    if pm_checkpoints:
        lines += [
            "### 3d. Open Article Placeholders — Your Answer Required",
            "",
            "The items below are open `[pm-input]` placeholders where specific information from",
            "you is needed before the content can be finalized. Each is a checkbox — check it",
            "off once you've provided the answer.",
            "",
        ]
        for fn, ask in pm_checkpoints:
            lines += [
                f"- [ ] **`{fn}`**",
                f"  {ask}",
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

    # PM input articles (original plan — not written)
    for fn, title, _ in pm_input:
        lines.append(f"| {action_num} | Provide input for `{fn}` | Info meeting | 30 min |")
        action_num += 1

    # Written forum articles needing fact-check
    for w in pm_forum_written:
        lines.append(f"| {action_num} | Fact-check `{w['filename']}` (Rank {w['rank']} community request) | Fact-check | 20–30 min |")
        action_num += 1

    # Deferred forum articles needing PM input to begin
    for d in pm_forum_deferred:
        lines.append(f"| {action_num} | Supply info to write `{d['filename']}` (Rank {d['rank']}) | Info meeting | 30 min |")
        action_num += 1

    # Open article placeholders (inline [pm-input] checkpoints + manifest flags)
    for fn, ask in pm_checkpoints:
        short_ask = ask.split(".")[0][:80]
        lines.append(f"| {action_num} | **Open placeholder in `{fn}`:** {short_ask} | **Answer required** | 15–30 min |")
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

    lines += ["", "---", "", f"_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._", ""]

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("Loading data...")
    ownership = load_ownership_reference(OWNERSHIP_FILE)
    gaps = load_forum_gaps(GAPS_FILE)
    manifest_text = MANIFEST_FILE.read_text(encoding="utf-8") if MANIFEST_FILE.exists() else ""
    if not manifest_text:
        print(f"  WARNING: {MANIFEST_FILE} not found — forum written/deferred tables will be empty")

    forum = {
        "written": parse_manifest_forum_written(manifest_text),
        "deferred": parse_manifest_forum_deferred(manifest_text),
        "checkpoints": scan_article_pm_inputs(ARTICLE_DIR),
    }

    print(f"  Ownership reference: {sum(len(v['articles']) for v in ownership.values())} articles across {len(ownership)} PMs")
    print(f"  Forum gaps: {len(gaps)} gaps loaded")
    print(f"  Manifest forum tables: {len(forum['written'])} written, {len(forum['deferred'])} deferred")
    print(f"  Embedded [pm-input] markers: {len(forum['checkpoints'])} found in s/article/")

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Roster of PMs we generate a brief for — union of ownership reference,
    # hardcoded Phase 3a lists, manifest PM-input flags, and scanned markers.
    roster = set(ownership.keys())
    for _, _, _, pm, _, _ in PHASE3A_ARTICLES:
        roster.add(pm)
    for _, _, pm, _ in PHASE3A_PM_ARTICLES:
        roster.add(pm)
    roster.update(MANIFEST_PM_INPUT_FLAGS.keys())
    for c in forum["checkpoints"]:
        roster.add(c["pm"])

    # Orphan detection: manifest forum rows whose PM cell matches no roster PM
    # (e.g. "Domo University / Enablement (no listed PM)"). These would silently
    # vanish from every brief, so surface them loudly.
    orphans = []
    for w in forum["written"]:
        if not any(pm_cell_matches(w["pm"], pm) for pm in roster):
            orphans.append(("written", w["rank"], w["filename"], w["pm"]))
    for d in forum["deferred"]:
        if not any(pm_cell_matches(d["pm"], pm) for pm in roster):
            orphans.append(("deferred", d["rank"], d["filename"], d["pm"]))

    all_pms = sorted(roster)
    print(f"\nGenerating briefs in {OUTPUT_DIR.relative_to(REPO_ROOT)}/...")

    for pm_name in all_pms:
        pm_data = ownership.get(pm_name, {"features": set(), "articles": []})
        brief = generate_brief(pm_name, pm_data, gaps, forum)
        safe_name = pm_name.replace(" ", "-").replace("/", "-").replace("(", "").replace(")", "")
        out_path = OUTPUT_DIR / f"{safe_name}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(brief)
        article_count = len(pm_data["articles"])
        print(f"  ✓ {out_path.name}  ({article_count} articles)")

    print(f"\nDone — {len(all_pms)} briefs written to pm-review-briefs/")

    if orphans:
        print("\n  ⚠️  UNASSIGNED forum items — no roster PM matched, will NOT appear in any brief:")
        for kind, rank, fn, pm in sorted(orphans, key=lambda o: o[1]):
            print(f"      [{kind}] Rank {rank}  {fn}  — PM cell: '{pm}'")
        print("      Fix the PM in RESTRUCTURE-MANIFEST.md or add them to the roster.")


if __name__ == "__main__":
    main()
