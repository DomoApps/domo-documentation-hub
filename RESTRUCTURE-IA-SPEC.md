# KB Information Architecture Spec

**Status:** Phase 2 complete — updated with workshop feedback (2026-06-17); ready for Phase 3 (content creation) and Phase 7 (nav rebuild)
**Generated from:** `scripts/build_ia_spec.py` + `scripts/output/ia-spec.json`
**Article mapping:** `scripts/output/ia-mapping.json` (every article → new pillar/group/sub_group)

This document defines the target structure for the Domo KB after restructuring.
`[NEW]` = article to be written. `[DECISION]` = requires human/PM sign-off before acting.
Counts in parentheses are existing articles moving to that location.

---

## Summary

| Pillar | Existing articles | New articles needed | Priority |
|--------|-------------------|---------------------|----------|
| Getting Started | 34 | 5 (3 role-based + 2 concept) | 🔴 Critical |
| Connect & Bring In Data | 1,050 | 4 (hub + 3 concept) | 🟡 Medium |
| Manage Data | 0–31 (pending D9) | 3 (hub + 2 concept) | 🔴 Critical |
| Prepare & Transform Data | 101 (or ~70 pending D9) | 4 (hub + 3 concept) | 🔴 Critical |
| Analyze & Visualize | 230 | 4 (hub + 3 concept) | 🔴 Critical |
| Build Apps & Automate | 106 | 3 (hub + 2 concept) | 🟡 Medium |
| Share & Collaborate | 51 | 2 (hub + 1 concept) | 🟡 Medium |
| AI & Data Science | 41 | 3 (hub + 2 concept) | 🟡 Medium |
| Administer & Govern | 72 | 3 (hub + 2 concept) | 🟡 Medium |
| Develop & Integrate | 5 | 4 (hub + 3 concept) | 🟠 High — severely thin |
| Release Notes | 65 | 0 | — |
| Archive | 64 | 0 | — |

---

## Pillar 1: Getting Started

**Story:** A new user's first hour in Domo — what is it, how do I log in, and where do I start based on my role.

```
Getting Started
├── [NEW] What is Domo?                               ← synthesize from 000005874 + role guides
├── [NEW] How Data Flows Through Domo                 ← [DECISION: PM input required]
├── By Role (2 existing + 3 new)
│   ├── Getting Started for Data Consumers            ← existing
│   ├── Getting Started for Data Engineers            ← existing
│   ├── [NEW] Getting Started for Admins              ← synthesize from admin how-tos
│   ├── [NEW] Getting Started for App Builders        ← synthesize from App Studio/Workflows
│   └── [NEW] Getting Started for Developers          ← synthesize from API articles
├── Key Resources (12)
│   ├── Introduction to Domo                          ← 000005874 (may be superseded by new "What is Domo?")
│   ├── First 5 Things to Do in Domo
│   ├── Domo Platform Tour
│   ├── Domo Glossary
│   ├── Domo Video Library
│   ├── Getting Help
│   ├── Standard Domo Support
│   ├── System Requirements
│   └── [+ 4 more]
├── Domo Mobile (6)
│   ├── [NEW - implied] What is the Domo Mobile App?
│   ├── Customize Domo Mobile App
│   ├── Editing a Dashboard's Mobile Layout
│   └── [+ 3 more]
├── Domo Free (4)
│   ├── Domo Free Overview
│   ├── Freemium Overview
│   └── [+ 2 more]
└── QuickStart Apps (10)         ← pre-built app tutorials for specific tools
    ├── Facebook (Business) QuickStart App
    ├── Hubspot QuickStart App
    └── [+ 8 more]
```

**[DECISION]** "Introduction to Domo" (000005874) currently serves as the main overview. Once the new "What is Domo?" article is written, determine whether to retire/merge 000005874 or keep it as a companion deep-dive.

---

## Pillar 2: Connect & Bring In Data

**Story:** You have data somewhere else. Here's how to get it into Domo — and, where needed, how to write data back to source systems — from the simplest connector to on-premises systems and cloud warehouses.

```
Connect & Bring In Data
├── [NEW] Overview: Connecting Your Data to Domo     ← hub article (establishes read + write framing)
├── [NEW] What is a Connector?                        ← synthesize from General Connector Info
├── [NEW] Getting Started: Connect Your First DataSet ← synthesize from connector setup articles
├── [NEW] How Connectors Work                         ← synthesize from General Connector Info (12)
│   (OAuth, credentials, scheduling, update methods)
├── Connector Library — Reference (976)               ← CDW + A-Z + Writeback merged; reference section
│   ├── [NEW] Connector Library Overview              ← hub article; introduces Cloud Amplifier for CDWs;
│   │                                                    "most commonly used connectors" curated highlight
│   ├── Cloud Data Warehouses (104)                   ← CDW sub-groups promoted within the library
│   │   ├── [NEW] Cloud Data Warehouses Overview      ← Cloud Amplifier as #1 recommended path for all CDWs;
│   │   │                                                introduces read + write framing for CDWs
│   │   ├── Snowflake (26)
│   │   │   ├── [NEW] Connect to Snowflake            ← read: Cloud Amplifier preferred; write: Cloud Amplifier
│   │   │   │                                            write path; fallback: existing Snowflake connectors
│   │   │   └── [existing 26 articles]
│   │   ├── Google BigQuery (11)
│   │   ├── Azure (17)
│   │   ├── Amazon Redshift/Athena (13)
│   │   ├── Databricks (5)
│   │   ├── MySQL (10)
│   │   ├── Oracle (9)
│   │   ├── PostgreSQL (8)
│   │   └── Dremio (1)
│   ├── Connectors A-B (130)
│   ├── Connectors C-F (119)
│   ├── Connectors G-K (122)
│   ├── Connectors L-P (176)
│   ├── Connectors Q-S (144)
│   ├── Connectors T-Z & # (102)
│   ├── Writeback Connectors (55)                     ← integrated into library; no longer a top-level section
│   └── Files & APIs (24)
└── Workbench (62)
    ├── [NEW] What is Workbench?                      ← synthesize from Workbench 5.2 overview;
    │                                                    covers both read and writeback capabilities
    ├── Workbench Enterprise (current)
    ├── Workbench 5 (current)
    └── Workbench 5.1 (Legacy) (12)                  ← collapsed group, clearly labeled legacy
```

**Note on Writeback Connectors:** The 55 writeback connector articles are no longer a standalone top-level section. CDW-specific write paths (Cloud Amplifier writeback) are documented within each CDW's sub-group overview. Standard writeback connectors are integrated into the alphabetical Connector Library groups alongside read connectors. Workbench writeback is covered in the Workbench section.

**[DECISION]** Workbench 4 (37 articles) is in Archive. Confirm: should it be completely removed from primary nav, or kept in a Legacy group? Recommend: Archive — these are 5+ year old articles for an EOL product.

**[DECISION]** "Files & APIs" is a sub-group of the connector library containing 24 articles. These are HTTP-based and file-upload connectors (SFTP, XML, JSON, etc.). Confirm they stay in Connector Library vs. getting their own section.

---

## Pillar 3: Manage Data

**Story:** You've connected your data. Now find it, understand it, and put it to work — navigate the Data Center, discover what's available, manage dataset health, and share data with the right people.

```
Manage Data
├── [NEW] Overview: Manage Your Data in Domo         ← hub article
├── [NEW] What is the Data Center?                    ← synthesize from connector + DataSet articles
│   (data list view, dataset cards, status indicators)
├── [NEW] Find and Manage Your DataSets               ← how to search, filter, favorite, share datasets
├── DataSet Management (31)                           ← [DECISION D9: some articles may stay in Pillar 4]
│   ├── DataSet Update Methods
│   ├── Export DataSets
│   ├── DataSet Backup
│   ├── Virtual DataSets
│   └── [remaining DataSet management how-tos]
└── [articles covering Data Center navigation, dataset lifecycle, workspaces/favorites — TBD pending D9]
```

**[DECISION D9]** Which existing DataSet Management articles (currently in Prepare & Transform Data) belong in Manage Data vs. staying in Prepare & Transform? Pipeline-oriented articles (update methods, virtual datasets) likely stay in Prepare & Transform; governance-adjacent articles (backup, sharing, lifecycle) likely move here. Resolve before Phase 7 nav rebuild.

---

## Pillar 4: Prepare & Transform Data

**Story:** Your data is in Domo. Now you need to clean it, join it, transform it, and shape it for analysis.

```
Prepare & Transform Data
├── [NEW] Overview: Preparing Your Data in Domo      ← hub article
├── [NEW] What is a DataSet?                          ← synthesize from connector + ETL articles
├── [NEW] Choosing the Right Data Prep Tool           ← [DECISION: PM input required]
│   (when to use Magic ETL vs DataFlows vs SQL vs Python)
├── Magic ETL (43)
│   ├── [NEW] What is Magic ETL?                      ← synthesize from ETL articles
│   ├── [NEW] Getting Started with Magic ETL          ← synthesize from ETL how-tos
│   ├── Magic ETL Tiles Reference
│   ├── Data Selection in Magic ETL
│   ├── Magic ETL on Snowflake                        ← Cloud Amplifier pattern
│   ├── Magic ETL AI
│   └── [remaining ETL how-tos]
├── DataFlows (26)
│   ├── [NEW] What is a DataFlow?                     ← synthesize from DataFlow articles
│   ├── Create and Manage DataFlows
│   ├── SQL DataFlows
│   └── [remaining DataFlow how-tos]
├── DataSet Management (31)
│   ├── DataSet Update Methods
│   ├── Export DataSets
│   ├── DataSet Backup
│   ├── Virtual DataSets
│   └── [remaining DataSet management how-tos]
└── Data Models (1 + needs expansion)
    ├── [NEW] What is a Data Model?                   ← synthesize from existing 1 article
    └── Create and Use Data Models (Beta)             ← existing 1 article
```

**[DECISION]** Data Models currently has only 1 article (Beta feature). Does this section need more articles written, or should it stay minimal until the feature ships? Recommend: Keep as a small section that grows as the feature matures.

---

## Pillar 5: Analyze & Visualize

**Story:** Your data is clean and ready. Now let's turn it into insights — cards, charts, dashboards, and calculations.

```
Analyze & Visualize
├── [NEW] Overview: Analyze & Visualize in Domo      ← hub article
├── [NEW] What is a Card?                             ← synthesize from Analyzer articles
├── [NEW] What is a Dashboard?                        ← synthesize from dashboard articles
├── Cards (33)                                        ← building individual visualization cards
│   ├── [NEW] Getting Started: Build Your First Card  ← synthesize; "Build Your First Dashboard"
│   │                                                    tutorial already exists (Getting Started)
│   ├── Analyzer Overview
│   ├── Analyzer Layout
│   ├── Powering a Card with Data
│   ├── Save a Visualization Card
│   ├── Card Building FAQs
│   └── [remaining card how-tos and references]
├── Chart Types — Reference (143)                     ← reference library; not a story section
│   ├── [NEW] Chart Types Overview / How to Choose    ← upgrade existing "Best Practices for Choosing
│   │                                                    Chart Types" into the hub article
│   ├── Line Charts
│   ├── Bar Charts
│   ├── Pie-Type Charts
│   ├── Map Charts
│   └── [remaining chart type articles]
├── Beast Mode (18)
│   ├── [NEW] What is Beast Mode?                     ← synthesize from FAQs + functions reference
│   ├── Create a Beast Mode Calculation
│   ├── Beast Mode Functions Reference
│   ├── Beast Mode FAQs
│   ├── Sample Beast Mode Calculations (5 sub-articles)
│   └── Troubleshooting Beast Mode
└── Dashboards & Pages (36)
    ├── [NEW] Getting Started: Build Your First Dashboard  ← already exists in Getting Started;
    │                                                          MOVE here (it's misplaced)
    ├── Manage Dashboards
    ├── Page Filters and Filter Views
    ├── Dashboard Optimization Best Practices
    ├── Top 10 Dashboard Design Best Practices
    └── [remaining dashboard articles]
```

**[DECISION]** "Build Your First Dashboard | Tutorial" currently lives in Getting Started. It should move to Analyze & Visualize > Dashboards & Pages, and Getting Started should link to it. Confirm before moving.

---

## Pillar 6: Build Apps & Automate

**Story:** You understand your data. Now let's build experiences on top of it — apps, workflows, and automations that help your whole organization act on insights.

```
Build Apps & Automate
├── [NEW] Overview: Build Apps & Automate             ← hub article
├── [NEW] What is App Studio?                         ← synthesize from App Studio Overview + articles
├── App Studio (11)
│   ├── App Studio | Overview                         ← existing (may become the "What is App Studio?")
│   ├── Build Domo Apps with the Pro-code Editor
│   ├── Design with App Studio Themes
│   ├── Create and Customize App Components
│   ├── Explore Data with Table Elements
│   ├── Deliver Reports with Report Builder
│   ├── Wire an App
│   └── [remaining App Studio how-tos]
├── Workflows (13)
│   ├── [NEW] What is Workflows?                      ← Workflows | Overview already exists
│   │         (may just promote existing overview)
│   ├── Workflows | Overview                          ← existing overview
│   ├── Create a Workflow
│   ├── Manage Workflows
│   ├── Build an AI Agent Task in Workflows
│   ├── Forms
│   └── [remaining Workflow how-tos]
├── Code Engine (1)
│   └── Code Engine                                   ← single article; section grows over time
├── Appstore (3)
│   ├── [NEW] Appstore Overview                       ← synthesize from existing 3
│   ├── Deploy, Request, and Remove Apps
│   ├── Manage Subscriptions
│   └── List on the Appstore
├── Asset Library (2)
│   ├── Asset Library
│   └── Asset Manager
├── CourseBuilder (12)
│   ├── Why Use CourseBuilder?                        ← serves as overview
│   ├── Installing CourseBuilder
│   └── [remaining CourseBuilder articles]
└── Premium Apps (65)                                 ← pre-built dashboard apps from Appstore
    ├── [NEW] Premium Apps Overview                   ← brief hub explaining what these are
    ├── Flex Map v2
    ├── Geocoder
    ├── Inline Editing
    ├── Campaigns App
    └── [remaining named apps — ~60 individual app how-tos]
```

**[DECISION]** Premium Apps (65 articles) are old-era "dashboard apps" from the early Appstore — Salesforce, Marketo, Fitbit, etc. Many may be outdated or unmaintained. Before Phase 3b upgrades, someone should audit which of these apps are still available and supported. Recommend: Flag the list for PM review before spending time upgrading these articles.

---

## Pillar 7: Share & Collaborate

**Story:** You've built your insights. Now get them in front of the right people — share dashboards, set up alerts, collaborate in Buzz, and publish to external audiences.

```
Share & Collaborate
├── [NEW] Overview: Share & Collaborate               ← hub article
├── Sharing (10)
│   ├── Sharing and Removing Access to Cards/Dashboards
│   ├── Certify Cards and DataSets
│   ├── Control Access to Cards and Dashboards
│   └── [remaining sharing how-tos]
├── Alerts (7)
│   ├── [NEW] What is an Alert?                       ← synthesize from Alerts Overview + articles
│   ├── Alerts Overview                               ← existing (promote to concept article)
│   ├── Create an Alert for a Card
│   ├── Create an Alert for a DataSet
│   ├── Manage Your Alerts
│   └── [remaining alert articles]
├── Buzz (8)
│   ├── Use Buzz
│   ├── Configuring Notifications for a Buzz Conversation
│   ├── Importing an Email Thread into Buzz
│   ├── Adding a Bot to Buzz
│   └── [remaining Buzz articles]
├── Publications (4)
│   ├── Setting Up Publication Groups
│   ├── Publish Content to a Subscriber Instance
│   ├── Slideshow Publications Page Layout
│   └── Sharing Content Using Slideshows
├── Export & Embed (8)
│   ├── Embed Content Outside of Domo
│   ├── Exporting Dashboards to PDF or PowerPoint
│   ├── Export Visualization Cards
│   ├── Exporting Embedded Content
│   └── [remaining export articles]
├── Domo Add-ins (3)
│   ├── Domo Add-ins for Microsoft Office 365 | User Guide
│   ├── Manual Installation Guide
│   └── Manual Installation for Enterprise
├── Projects & Tasks (10)
│   ├── Creating a Project
│   ├── Creating and Assigning Project Tasks
│   └── [remaining P&T articles]
└── Notifications & Reports (1)
    └── Scheduled Reports
```

**[DECISION]** Projects & Tasks is a legacy feature (pre-Workflows era). Are these articles current? If the feature is being phased out in favor of Workflows, these may belong in Archive.

---

## Pillar 8: AI & Data Science

**Story:** Go beyond standard charts — use AI to generate insights, run machine learning models, write Python and R in Jupyter, and build AI agents.

```
AI & Data Science
├── [NEW] Overview: AI & Data Science in Domo         ← hub article
├── [NEW] What is Domo AI?                            ← synthesize from Domo AI FAQ + AI articles
├── Domo AI (27)
│   ├── Domo AI FAQ
│   ├── AI Chat articles
│   ├── Magic ETL AI
│   ├── AI Playground
│   ├── AI Adapters (Databricks, OpenAI, Bedrock)
│   ├── MCP Integration
│   └── [remaining AI articles]
├── AutoML (1)
│   └── Train and Deploy Models with AutoML           ← single article; needs expansion
├── Jupyter Workspaces (5)
│   ├── Jupyter articles
│   └── Jupyter Troubleshooting Guide
├── DomoStats (7)
│   ├── DomoStats Overview                            ← serves as hub
│   ├── DomoStats Connector
│   ├── DomoStats - Activity Log App
│   └── [remaining DomoStats reports]
└── Unstructured Data (1)
    └── Use FileSets to Gather Information from Unstructured Data
```

---

## Pillar 9: Administer & Govern

**Story:** You're responsible for the Domo instance. Here's how to manage users, set up security, govern data quality, and keep the platform running smoothly.

```
Administer & Govern
├── [NEW] Overview: Administer & Govern               ← hub article
├── [NEW] Security & Permissions Overview             ← synthesize from PDP, roles, access articles
├── Users & Roles (13)
│   ├── [NEW] Domo User Roles and What They Can Do    ← synthesize from roles/grants articles
│   ├── Manage Users
│   ├── Custom Roles
│   ├── System Roles
│   ├── PDP (Personalized Data Permissions)
│   └── [remaining user/role articles]
├── Security & Access (9)
│   ├── OAuth / SSO Configuration
│   ├── Troubleshoot Single Sign-On Using SAML
│   ├── Allowlist IP Addresses
│   ├── Session Management
│   ├── Access Tokens (Beta)
│   └── [remaining security articles]
├── Governance (3)
│   ├── Content Governance Hub
│   ├── DataSet Watchdog
│   └── Enterprise Data Copy
├── Instance Settings (39)
│   ├── Admin Settings
│   ├── Tag Management
│   ├── Brand Kit
│   ├── Schema Management
│   ├── Group Management
│   ├── Credit Monitoring
│   ├── Observability Metrics
│   └── [remaining instance settings]
├── Sandbox & Environments (1)
│   ├── [NEW] Domo Sandbox & Promotion Overview       ← synthesize from Sandbox article
│   └── Domo Sandbox: Linked Repositories
└── Goals (5)
    ├── Getting Started With Goals                    ← existing tutorial
    ├── Configuring Goals Settings
    ├── Accessing Goals Data
    ├── Enhancing Your Goals
    └── Managing Your Goals and Metrics
```

**[DECISION]** "Instance Settings" has 39 articles — it's a catch-all for admin-level how-tos that don't fit elsewhere. Consider whether this should be broken into sub-groups (Billing & Credits, Notifications, Profile Settings, etc.) in the nav. For now, keep flat; revisit if UX testing shows users can't find things.

---

## Pillar 10: Develop & Integrate

**Story:** You want to build on top of Domo programmatically — call the REST API, use SDKs, integrate via MCP, or build custom apps.

**Current state: 5 articles. Severely thin. This pillar cannot tell a story until Phase 3a content is written.**

```
Develop & Integrate
├── [NEW] Overview: Develop & Integrate               ← hub article
├── [NEW] Getting Started with the Domo API           ← synthesize from existing API articles
├── APIs & SDKs (5)
│   ├── [existing 5 API/SDK articles]
│   └── [NEW] Domo REST API Reference hub             ← links to developer.domo.com
├── [NEW] Authentication Overview                     ← synthesize from access token + OAuth articles
└── [NEW] MCP Integration                             ← Connect-AI-Tools-to-Domo-Using-MCP.mdx
                                                         exists in Connect but should move here
```

**Note:** The Domo developer documentation may live primarily at developer.domo.com (the Developer Portal tab in docs.json). This pillar may largely function as an entry ramp to that portal, with a small number of KB articles for common how-tos. Confirm scope with the developer relations or API team.

---

## Pillar 11: Release Notes

```
Release Notes
├── Current Release Notes
├── 2025-2026 Archives
└── Pre-2025 Archives (collapsed)
    ├── 2023-2024
    ├── 2021-2022
    └── 2015-2020
```

---

## Pillar 12: Archive (not in primary nav)

The Archive pillar holds deprecated/legacy content that is removed from primary navigation but not deleted. It should be linked from a single "Legacy & Archived Content" page at the bottom of the KB.

```
Archive (64 articles)
├── Legacy Workbench (37)            ← Workbench 4 articles
├── Deprecated Features (25)         ← various deprecated product features
├── Legacy Magic ETL (1)
└── Legacy Products (1)              ← PopChart contact page
```

---

## Human Decisions Required Before Phase 3

| # | Decision | Recommendation | Who |
|---|----------|----------------|-----|
| D1 | Keep or retire Workbench 4 articles (37)? | Archive — EOL product | You |
| D2 | Keep or archive Projects & Tasks (10 articles)? | Check if feature still active | You / PM |
| D3 | Audit Premium Apps (65 articles) for currency | Many may be outdated apps | You / PM |
| D4 | "Build Your First Dashboard" — move from Getting Started to Analyze & Visualize? | Yes — move it | You |
| D5 | "Introduction to Domo" (000005874) — keep alongside new "What is Domo?" or retire? | Keep as deep-dive companion | You |
| D6 | Confirm Develop & Integrate scope — KB how-tos vs. link-out to developer.domo.com? | Clarify with dev relations | You / Dev PM |
| D7 | Data Models section (1 article, Beta) — expand or hold? | Hold until feature ships | You / PM |
| D8 | Instance Settings (39) — sub-group further or keep flat? | Keep flat for now | You |
| D9 | Which DataSet Management articles move from Prepare & Transform to Manage Data? | Pipeline articles stay; governance/lifecycle articles move | You / PM |

---

## New Articles to Write (Phase 3a — synthesizable from existing content)

Listed in priority order. All synthesizable without PM input unless marked [PM].

| Priority | Article | Synthesize from |
|----------|---------|-----------------|
| 1 | `What-is-Domo.mdx` | 000005874, Getting Started role guides |
| 2 | `Getting-Started-for-Admins.mdx` | Admin how-tos, roles/grants articles |
| 3 | `Getting-Started-for-App-Builders.mdx` | App Studio Overview, Workflows overview |
| 4 | `Getting-Started-for-Developers.mdx` | API articles, MCP article, Access Tokens |
| 5 | `What-is-a-DataSet.mdx` | Connector how-tos, Magic ETL input tile articles |
| 6 | `What-is-Magic-ETL.mdx` | Magic ETL overview articles |
| 7 | `What-is-a-DataFlow.mdx` | DataFlow articles |
| 8 | `Prepare-and-Transform-Data-Overview.mdx` | All ETL/DataFlow/DataSet articles (hub) |
| 9 | `What-is-a-Card.mdx` | Analyzer articles |
| 10 | `What-is-a-Dashboard.mdx` | Dashboard articles |
| 11 | `What-is-Beast-Mode.mdx` | Beast Mode FAQs, functions reference |
| 12 | `Analyze-and-Visualize-Overview.mdx` | All Analyzer/chart/dashboard articles (hub) |
| 13 | `What-is-an-Alert.mdx` | Alerts Overview, alert articles |
| 14 | `What-is-a-Connector.mdx` | General Connector Info (12 articles) |
| 15 | `Connect-and-Bring-In-Data-Overview.mdx` | All connector/Workbench articles (hub); frames read + write directions |
| 16 | `Manage-Data-Overview.mdx` | DataSet articles, Data Center articles (hub) |
| 17 | `What-is-the-Data-Center.mdx` | Connector how-tos (implicit Data Center context), DataSet management articles |
| 18 | `Find-and-Manage-Your-DataSets.mdx` | DataSet management, sharing, workspace/favorites articles |
| 19 | `What-is-Domo-AI.mdx` | Domo AI FAQ, AI Playground, AI articles |
| 20 | `AI-and-Data-Science-Overview.mdx` | All AI/DomoStats/Jupyter articles (hub) |
| 21 | `What-is-App-Studio.mdx` | App Studio Overview (may just reframe it) |
| 22 | `Build-Apps-and-Automate-Overview.mdx` | App Studio, Workflows, Code Engine articles (hub) |
| 23 | `What-is-Workbench.mdx` | Workbench 5.2 overview, Workbench Enterprise |
| 24 | `Share-and-Collaborate-Overview.mdx` | Sharing, Buzz, Publications, Embed articles (hub) |
| 25 | `Domo-User-Roles-and-What-They-Can-Do.mdx` | Roles/grants articles |
| 26 | `Security-and-Permissions-Overview.mdx` | PDP, access rights, OAuth, security settings |
| 27 | `Administer-and-Govern-Overview.mdx` | Admin articles (hub) |
| 28 | `Domo-Sandbox-and-Promotion-Overview.mdx` | Sandbox article, Linked Repositories |
| 29 | `Develop-and-Integrate-Overview.mdx` | Existing 5 API articles (hub) |
| PM | `How-Data-Flows-Through-Domo.mdx` | [PM: needs canonical pipeline narrative] |
| PM | `Choosing-the-Right-Data-Prep-Tool.mdx` | [PM: ETL vs DataFlow vs SQL positioning] |
| PM | `Understanding-DataSet-Joins-and-Relationships.mdx` | [PM: decision guidance needed] |
| PM | `Domo-for-Mobile-Overview.mdx` | [PM: confirm current mobile feature scope] |
