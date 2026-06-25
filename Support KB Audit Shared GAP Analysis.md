# Support KB Audit — Shared Gap Analysis

**Decision summary:** The Support team's KB Audit and the active KB Restructure initiative share a meaningful overlap in retirement/archival work — Workbench 4, DataFusion, old Magic ETL tiles, ~100+ deprecated connectors, and old release notes — which should be executed once during Restructure Phase 4 using the Audit as the authoritative hit list, rather than twice as separate efforts. The Audit's remaining work (API reference quality fixes, connector content accuracy, localized article retirement, screenshot refresh) falls outside the Restructure's scope and will become a separate follow-on project once the Restructure's nav rebuild is complete. One item is urgent regardless of either initiative: Snowflake connector articles documenting a now-retired authentication method should be updated immediately, as customers attempting new connections today will fail.

**Prepared:** 2026-06-25
**Inputs:**
- `KB Audit Results.csv` — Support team audit of 3,680 articles (completed 2026-04-28); identifies update/deprecation/legacy disposition per article
- `KB-RESTRUCTURE-PLAN.md`, `RESTRUCTURE-IA-SPEC.md`, `RESTRUCTURE-PROGRESS.md` — Active 7-phase KB restructure; Phases 1–2 complete, Phase 3a (net-new article creation) is next

**Purpose:** Determine which gap work is shared between the two initiatives (done once, not twice) and which work belongs exclusively to one initiative, so effort is not duplicated and each project has a clean scope boundary.

---

## At a Glance: The Two Initiatives

| Dimension | Support KB Audit | KB Restructure |
|-----------|-----------------|----------------|
| Scale | 3,680 articles audited | 1,819 articles in-scope |
| Primary question | "Is this existing article accurate and self-service-ready?" | "Does the KB tell a coherent story, and what's missing?" |
| Overlap with repo | Heavy on Developer Portal API reference and localized content | KB-only (`s/article/`, `s/topic/`, `portal/`) |
| Gap type found | Content accuracy, deprecated content, broken examples, outdated screenshots | Missing article types, flat navigation, no conceptual framing, no interlinking |
| Disposition categories | Keep / Needs Review / Deprecate / Mark as Legacy | Write / Move / Archive / Upgrade / Rename |
| Volume flagged for action | 1,461 articles need some action (936 Needs Review, 748 Deprecate, 713 Mark as Legacy, 301 confirmed stale updates) | ~1,100 articles need structural changes; ~29 new articles to write |

---

## Executive Summary

The two initiatives are addressing fundamentally different dimensions of the same problem: the Restructure asks *"where is the content and can users find it?"*; the Audit asks *"is the content that exists actually correct?"* They are complementary, not redundant — but they share a meaningful overlap in the retirement/archival work.

**The Venn diagram in one paragraph:** Both initiatives independently identified that Workbench 4, DataFusion, Old Magic ETL tiles, numerous deprecated connector articles, and old localized release notes need to be retired or archived. That retirement work — approximately 500–600 article-level actions — is the primary shared zone, and it should be executed *once* during the Restructure's Phase 4 (Consolidation & Retirement), using the Audit data as the authoritative hit list for what to retire and why. Doing this work twice would be wasteful; doing it out of order (Audit-first, then Restructure-second) risks retiring articles the Restructure is actively reorganizing.

**What the Audit adds that the Restructure doesn't cover:** A large body of content-accuracy work — broken API code examples, outdated connector authentication procedures, stale screenshots, and incorrect UI paths — that has nothing to do with navigation or information architecture. This work, approximately 500+ high-priority article-level fixes, is a separate post-restructure project. It also surfaced that localized content (~1,145 articles across Japanese, German, Spanish, French) needs significant deprecation work; the Restructure doesn't touch localization.

**What the Restructure addresses that the Audit doesn't:** The entire missing-article layer. The Audit is an accuracy audit of existing content; it has no mechanism for identifying articles that don't exist yet. The Restructure's ~29 new conceptual and hub articles, the navigation rebuild, role-based Getting Started guides, slug rename, and cross-linking work are entirely outside the Audit's scope.

---

## Section 1 — Shared Gaps (Address Once, During Restructure Phase 4)

These gaps appear in both initiatives. The Audit supplies the specific hit list; the Restructure supplies the execution framework. Retire/archive these in **Restructure Phase 4** so the nav rebuild in Phase 7 starts clean.

### 1.1 Workbench 4 Retirement

**Restructure:** Decision D1 — Archive Workbench 4 (37 articles; EOL product). Recommendation: Archive. Not yet executed.

**Audit:** 188 total Workbench articles audited. 83 flagged **Mark as Legacy**, 35 flagged **Deprecate** (118 total retirement-flagged). The majority of these are Workbench 4 and Workbench 5.1 articles. Many summaries note: *"Customers cannot self-serve because the article provides instructions for an end-of-support product without linking to the current version."*

**Action for Restructure Phase 4:** Use Audit's Workbench deprecation/legacy list as the definitive execution plan for D1. The Audit has already done the article-by-article analysis; the Restructure provides the destination (Archive nav group). These are the same 37+ articles.

---

### 1.2 DataFusion Deprecation

**Restructure:** DataFusion is a deprecated feature. Phase 4 retirement work would catch it; it is not called out by name in the plan but appears in merge-candidate analysis.

**Audit:** 11 DataFusion articles identified — 6 flagged **Deprecate**, 5 flagged **Mark as Legacy**. Key finding: *"DataFusionパフォーマンス推奨: Customers cannot self-serve because the article provides optimization guidance for DataFusion, a deprecated feature."* The English-language articles (`Combine DataSets Using DataFusion (Deprecated)`, `Edit a DataFusion`, `DataFlow and DataFusion Troubleshooting and FAQs`) are all flagged.

**Action for Restructure Phase 4:** Retire all 11 DataFusion articles to Archive. The Audit confirms this is safe — no customers can self-serve with current DataFusion content anyway.

---

### 1.3 Deprecated Connector Articles

**Restructure:** Phase 4 Consolidation — retire connectors where `tag: "Deprecated"` is set, and any connectors whose excerpt describes a feature no longer in the product.

**Audit:** 337 Data Connection articles flagged **Deprecate**, 498 flagged **Mark as Legacy** (835 total retirement-flagged connector articles). Specific examples of confirmed-dead connectors:
- LinkedIn Connector (LinkedIn API v1, disabled May 2019)
- Pinterest Connector (disabled March 2018)
- StumbleUpon Connector (service shut down 2018)
- Simply Measured Connector (acquired and shut down 2017)
- Salesforce Desk Connector (discontinued 2017)
- IBM Digital Analytics/Coremetrics Connector (IBM discontinued)
- Adobe Analytics Advanced Legacy Connector (explicitly deprecated; new datasets blocked)
- Snowflake Writeback Connector (fully deprecated by October 1, 2025)
- DCM via Google Cloud Storage (OAuth deprecated by Google; connector unavailable)
- GetThere Connector (UI unavailable; contact support only)

**Action for Restructure Phase 4:** The Audit is the authoritative deprecation list for the connector library. Its summaries provide the *reason* for each retirement — useful for writing the Archive group description and for any redirect copy. Do not run a separate deprecation analysis; use Audit data directly.

**Important scope note:** The Audit also flags 498 connectors as "Mark as Legacy" rather than full deprecation. These are connectors that still work but whose documentation is outdated. This population should be assessed during Restructure Phase 4 as merge-candidates or flagged for Phase 3b article upgrades — they are not Archive candidates, but they need updating.

---

### 1.4 Old Magic ETL Tiles

**Restructure:** Phase 1 catalog found `retire-candidate` classification. Phase 4 legacy cleanup is planned.

**Audit:** 16 articles explicitly titled "Old Magic ETL" or referencing legacy Magic ETL tiles are in the audit. Of these, 15 are flagged Deprecate or Mark as Legacy; 1 (`Create a Recursive/Snapshot Old Magic ETL DataFlow`) is flagged **Keep** and should not be archived. The remaining 72 Magic ETL articles in the audit split as: 10 Deprecate, 20 Mark as Legacy, 23 Needs Review. The clear pattern: articles about the "old" Magic ETL tile interface are legacy; articles about new Magic ETL features (Snowflake Pass-Through SQL, AI tiles) are current but may have beta-status confusion.

**Action for Restructure Phase 4:** Retire the 16 old Magic ETL tile articles to Archive. For the 20 "Mark as Legacy" Magic ETL articles, use Phase 3b article upgrade agents to add a prominent "This article covers the legacy Magic ETL interface. [Link to current]" callout rather than full retirement.

---

### 1.5 Release Notes Archival

**Restructure:** Plan specifies collapsing pre-2022 release notes to an archive group in Phase 7 nav rebuild. Pre-2022 articles = low priority for primary nav.

**Audit:** Large volume of localized release notes flagged for **Deprecate** or **Mark as Legacy** — 2015–2023 release notes in German, Spanish, French, and Japanese, with assessments like *"historical release notes document that only announces features without providing actionable guidance."* English release notes from 2018–2021 also flagged.

**Action for Restructure Phase 7:** Nav rebuild moves pre-2022 release notes (all languages) into the collapsed Archive nav group. The Audit confirms this is user-neutral — these articles have negligible self-service value for current customers.

---

### 1.6 Missing Conceptual Framing Causing "Can't Self-Serve" Failures

**Restructure:** Phase 3a creates ~29 new "What is X?" and hub articles specifically because users land on how-to articles with no conceptual context.

**Audit:** The most common customer failure pattern in Audit summaries is: *"Customers cannot self-serve because the article assumes familiarity with [feature] but provides no definition or context."* This appears in Data Transformation (Magic ETL, DataFlow), Visualization (Analyzer, Beast Mode), Administration (SSO setup, PDP), and AI articles. The Audit identifies this as a *content quality problem*; the Restructure's Phase 3a directly solves it.

**Action:** The Restructure's new conceptual articles — `What-is-Magic-ETL.mdx`, `What-is-a-DataFlow.mdx`, `What-is-Beast-Mode.mdx`, `What-is-Domo-AI.mdx`, etc. — are the structural fix for the Audit's most common failure mode. No separate Audit project needed for this. **Once Phase 3a articles are published and added to nav, this failure pattern should drop measurably in support ticket volume.**

---

### 1.7 Cloud Amplifier / Data Warehouse Terminology and Navigation Confusion

**Restructure:** The Connect & Bring In Data pillar restructure establishes Cloud Amplifier as the recommended path for CDW connections and adds a Cloud Data Warehouses Overview hub article.

**Audit:** 12 Data Warehouse articles flagged as needing review, with consistent issue: *"The article references 'Cloud Amplifier' terminology and UI paths like 'Data Warehouse' and 'Add new cloud' that may no longer match the current interface."* Specific articles: `Cloud Integrations (Cloud Amplifier) Troubleshooting`, `Domo on Amazon Redshift`, `Add Databricks Tables to Domo`, `Migrate from Federated to Cloud Amplifier`, `Non-queryable DataSets`.

**Action:** Restructure's Cloud Data Warehouses Overview hub article (Phase 3a, priority item in Connect pillar) addresses the navigation layer. The specific content accuracy fixes in these 12 articles (screenshot updates, correct UI paths) are **Audit-only work** to be executed after the hub article establishes correct terminology — so the Audit's content fixes for these articles should wait until the Restructure's CDW hub is published.

---

### 1.8 AI Article Beta/GA Status Clarification

**Restructure:** Phase 3a creates `What-is-Domo-AI.mdx` and `AI-and-Data-Science-Overview.mdx`. The IA spec notes AI articles need conceptual framing.

**Audit:** 29 AI & Machine Learning articles flagged (High priority), with the predominant issue: *"Beta designation is unexplained. Customers cannot confidently self-serve because it is unclear whether this feature is production-ready."* Specific articles: Sentiment Analysis Beta, Targeted Sentiment Analysis Beta, AI Service Layer articles in multiple languages, Magic ETL Data Science Tiles (flagged Critical: navigation stub with no content).

**Action:** The new AI hub article (Phase 3a) establishes the canonical GA vs. Beta status map. After the hub publishes, the individual AI articles should be updated to reference the hub for status context — this is Phase 3b upgrade work. The API-specific AI articles (in the Developer Portal) require separate Audit follow-up regardless of Restructure status.

---

## Section 2 — Gaps Unique to the Support Audit (Post-Restructure Project)

These gaps were identified by the Audit but are **not addressed by the Restructure initiative**. They constitute the scope of a separate post-restructure content-accuracy project.

### 2.1 API Reference Article Quality Fixes (Developer Portal — 340 articles, 91 Needs Review)

The Audit reviewed 340 Developer Portal API reference articles. 91 are flagged Needs Review with substantive gaps:

- **Missing response schemas:** AppDB API (Create Document, List Documents, Query Document, Bulk Delete Documents), Dataset streaming endpoints (Stream Get, Stream Create), Files API endpoints — all marked "response body is not documented"
- **Broken/malformed code examples:** `Create Export` endpoint has malformed JSON with escaped quotes that would cause API calls to fail if copied directly; `Upload CSV Part` contains the extraneous phrase "Jae and Oleksii, why hello, it is the way" (literal copy-paste artifact)
- **Unverified authentication methods:** Files API articles (Copy/Move, Delete, Download, Get/Update Permissions, Upload) all note authentication as "Assumed based on similar APIs" — 7 articles with unverified auth headers
- **HTTP method contradictions:** `Update a Beast Mode` simultaneously labels the endpoint as both PUT and POST
- **Missing prerequisite sections:** AI Service Layer endpoints (Text-to-SQL, Sentiment Analysis, Targeted Sentiment Analysis) lack explanation of how to obtain Developer Tokens or enable the feature

**Why this is not Restructure work:** These are content accuracy problems in the Developer Portal's auto-generated and hand-authored API reference, not KB navigation or information architecture problems. They require product engineering or developer relations to verify live API behavior, then a technical writer to update the spec. The Restructure plan explicitly does not include API reference quality work.

**Post-Restructure project scope:** ~91 API reference articles requiring engineering verification and content fixes. Critical priority: malformed JSON (`Create Export`), extraneous text (`Upload CSV Part`), and unverified auth headers across Files API endpoints.

---

### 2.2 Individual Connector Content Accuracy (not just retirement)

Beyond the deprecated connectors (Section 1.3), the Audit identified a large population of *working* connectors with content accuracy problems that the Restructure won't fix:

- **Deprecated authentication still documented as current:** Multiple connectors where the credential flow described is no longer valid (Google Ads OAuth vs. current auth; Snowflake key-pair authentication retiring November 2025)
- **Copy-paste errors between connectors:** SmartDB connector (credentials pane references Xero OAuth and Spotify), RealPage connector (conflates RealPage and Intacct), Adobe Sign connector (references Google Ads OAuth)
- **Broken external prerequisite links:** Azure Data Lake Gen2 OAuth (truncated Microsoft API docs link), Qualtrics Upsert (Qualtrics UI path outdated), Xero Custom (missing Client ID/Secret instructions)
- **Snowflake auth deprecation urgency:** Multiple Snowflake connector articles (Snowflake Connector, Snowflake Unload V2, Snowflake Writeback) document authentication methods Snowflake is retiring in November 2025 — this may already be past deadline and causing active customer failures

**Why this is not Restructure work:** The Restructure adds a hub article and organizes connectors alphabetically; it does not audit or fix the content of individual connector how-to articles. Connector content accuracy requires connector-by-connector verification against live product behavior.

**Post-Restructure project scope:** An estimated 200–300 connector articles requiring content accuracy review. The Snowflake auth deprecation items are urgent and should be addressed immediately, even before the Restructure completes.

---

### 2.3 Localized Article Deprecation and Retirement (~1,145 articles)

The Audit identified hundreds of localized articles (Japanese, German, Spanish, French) for Deprecate or Mark as Legacy. Major patterns:
- Old release notes in every language (2017–2023) flagged for deprecation
- Legacy feature articles (DataFusion, old Magic ETL, deprecated apps) in each language that mirror the English retirement list
- Localized connector articles for deprecated connectors

**Why this is not Restructure work:** The Restructure initiative is English-KB-only. Localization maintenance requires a coordinated process with the localization team or localization vendor — it is not a navigation/IA project.

**Post-Restructure project scope:** A dedicated localization audit and retirement project. The Audit provides the per-article disposition for each language; the project is execution, not re-analysis.

---

### 2.4 Screenshot Currency and Broken Image References

The Audit identified a pervasive pattern across hundreds of articles: **outdated screenshots or broken image references** causing customer self-service failures. Concentrated areas:

- **Data Warehouse articles:** Multiple articles referencing "Data Warehouse" nav path (now renamed); icons and screenshots no longer match current UI
- **Administration articles:** SSO configuration articles (Google, Okta, Azure Active Directory) with screenshots from older UI versions
- **Data Transformation:** SQL DataFlow creation articles where "Magic Transform toolbar" path screenshots are obsolete
- **Connector articles at scale:** Hundreds of connectors where Credentials Pane screenshots are outdated

**Why this is not Restructure work:** The Restructure adds new articles and reorganizes navigation. Systematic screenshot refreshes across existing articles are a content maintenance project requiring screenshot tooling, product access, and writer bandwidth — separate from the structural IA work.

**Post-Restructure project scope:** A screenshot-refresh sprint, potentially using a systematic comparison of live product UI against article screenshots. High priority: Data Warehouse articles, SSO configuration articles, and Data Transformation articles with broken icon references.

---

### 2.5 CourseBuilder Retirement

The Audit flags CourseBuilder as a **retired tool no longer available in Domo**, with Critical priority:
- `Understanding the CourseBuilder Layout` — *"CourseBuilder is a retired/legacy tool no longer available. The article contains only placeholder references to screenshots."*
- `Importing Files into Your CourseBuilder App Project` — *"The referenced graphic is missing and the entire instructional content is absent."*
- `Installing CourseBuilder`, `Previewing and Exporting Your CourseBuilder App` — both Mark as Legacy

**Why this is partially Restructure work:** The Restructure IA spec places CourseBuilder under Build Apps & Automate. If the feature is retired, all 16 articles should move to Archive instead. This is a **fast decision** that should be made before Phase 7 nav rebuild.

**Immediate action:** Confirm with PM that CourseBuilder is retired. If confirmed, move all 16 articles to the Archive group during Phase 4 — this costs nothing extra and cleans the Build Apps & Automate pillar before nav rebuild.

---

### 2.6 Buzz Desktop / Buzz Web Disambiguation

The Audit flags the "Use Buzz" article as High priority Needs Review: *"The contradictory deprecation notice at the top alongside extensive feature documentation for Buzz web creates confusion about which Buzz product customers should use."*

**Why this is Audit-only work:** The Restructure creates a Share & Collaborate hub article but does not update existing Buzz articles. Adding a one-sentence scope statement ("This article covers Buzz in the Domo web app. If you were using the Buzz Desktop app, that has been discontinued.") is a quick `update-kb-article` fix that can be done as part of Audit follow-up.

---

### 2.7 Geocoder App Removal Notice

The Audit flags multiple Geocoder App articles as High priority: *"The Geocoder App has been removed from the Domo Appstore. Instructions are non-actionable for new customers."*

**Why this is Audit-only work:** The Restructure IA puts Geocoder under Premium Apps, which is flagged for PM currency audit (D3 decision) but not scheduled for rewriting. The fix is simple: add a banner note to each Geocoder article explaining the app has been removed and directing users to alternative geocoding solutions (custom apps or partner solutions).

---

## Section 3 — Gaps Unique to the Restructure (Not Covered by Audit)

These are the Restructure's core deliverables. The Support Audit has no mechanism to identify missing articles or navigation problems, so none of this appears in the Audit data.

### 3.1 Net-New Conceptual and Hub Articles (~29 articles)

The Audit is an accuracy audit — it can only evaluate articles that exist. It cannot identify:
- `What-is-Domo.mdx`, `What-is-a-DataSet.mdx`, `What-is-Magic-ETL.mdx`, `What-is-a-DataFlow.mdx`, `What-is-a-Card.mdx`, `What-is-a-Dashboard.mdx`, `What-is-Beast-Mode.mdx`, `What-is-App-Studio.mdx`, `What-is-an-Alert.mdx`, `What-is-a-Connector.mdx`, `What-is-Domo-AI.mdx`, `What-is-Workbench.mdx`
- Section hub articles for all 12 pillars
- Role-based Getting Started guides (Admin, App Builder, Developer)
- Data Center and Manage Data overview articles
- Sandbox and Promotion Overview

These ~29 articles fill the conceptual layer that currently does not exist in the KB. They are entirely Restructure work.

---

### 3.2 Navigation Collapse (335 Groups → 12 Pillars)

The nav rebuild is purely Restructure territory. The Audit evaluates article content; it has no awareness that 335 nav groups cause discoverability failure. The entire Phase 7 nav rebuild — new `docs.json`, pillar structure, hub-and-spoke layout — is Restructure-only scope.

---

### 3.3 KB ↔ Developer Portal Cross-Linking (Phase 5.5)

The systematic bidirectional linking between KB how-to articles and Developer Portal API reference pages is a Restructure deliverable (Phase 5.5). The Audit found that some API articles lack prerequisites (developers can't find the KB how-to for enabling the feature); the Restructure's cross-linking work addresses this from the KB side. These are complementary but the execution is Restructure-owned.

---

### 3.4 URL Slug Rename (Phase 6)

Renaming 1,575 numeric-ID filenames to human-readable slugs is a Restructure Phase 6 deliverable. The Audit references articles by URL — many of its URLs use the current numeric paths (e.g., `000005874.mdx`). The Audit's dispositions remain valid after rename; no re-audit needed. But the rename itself is Restructure-only.

---

### 3.5 Systematic Interlinking / Next Steps (Phase 5)

Adding `## Next Steps` and `## Related Articles` sections to ~200+ articles is Restructure Phase 5 work. The Audit noted that customers "cannot find related articles" as a contributing factor in some failures, but the fix is the Restructure's interlinking pass.

---

### 3.6 AI as First Option Callouts

Adding `<Tip>**Try it with AI:**</Tip>` callouts to hub articles and key how-tos, pointing to GA AI features, is a Restructure cross-cutting principle. The Audit doesn't address this pattern.

---

### 3.7 PM-Gated Narrative Articles (4 articles)

`How-Data-Flows-Through-Domo.mdx`, `Choosing-the-Right-Data-Prep-Tool.mdx`, `Understanding-DataSet-Joins-and-Relationships.mdx`, `Domo-for-Mobile-Overview.mdx` — all require PM input before writing. Pure Restructure scope.

---

## Section 4 — Execution Recommendations

### Integrate Immediately Into Restructure Phase 4

The following Audit findings should be incorporated into the Restructure Phase 4 execution plan **before that phase begins**. The Audit has already done the analysis; the Restructure provides the execution framework:

| Item | Audit finding | Restructure action |
|------|--------------|-------------------|
| Workbench 4 retirement | 118 Workbench articles flagged Deprecate/Legacy | Confirms D1: Archive. Use Audit list as execution plan. |
| DataFusion deprecation | 11 articles flagged Deprecate/Legacy | Add to Phase 4 retirement batch |
| Old Magic ETL tiles | 15 articles flagged Deprecate/Legacy; 1 (`Create a Recursive/Snapshot Old Magic ETL DataFlow`) flagged Keep — do not archive | Add 15 to Phase 4 Archive batch |
| Deprecated connectors (dead services) | 111 confirmed dead-service connector articles (verified via Audit summaries) | Phase 4 retirement execution list |
| Legacy release notes (all languages) | Flagged for deprecation | Phase 7: move pre-2022 to collapsed Archive nav group |
| CourseBuilder retirement | 16 articles (3 Deprecate, 5 Legacy, 4 Needs Review, 4 pending) | Fast D-decision: if PM confirms retired, add all 16 to Phase 4 Archive |

### Snowflake Auth Deprecation — Treat as Urgent, Pre-Restructure Fix

Multiple Snowflake connector articles document a key-pair / password authentication method that Snowflake deprecated by November 2025. This is past-tense — customers trying to use these articles for new connections are already failing. **This should be addressed immediately, not waiting for Restructure Phase 4.** Use `update-kb-article` on the affected Snowflake connector articles (Snowflake Connector, Snowflake Unload V2) to add a prominent notice that the documented auth method is retired and link to the current setup path.

### Post-Restructure Project Definition

Once the Restructure's Phase 7 nav rebuild is complete, the remaining Audit work becomes a well-scoped second project with these work streams:

1. **API reference quality sprint** (~91 Developer Portal articles; owned by dev relations / technical writers with API access)
2. **Connector content accuracy sprint** (~200–300 connector articles; requires live connector testing or product team verification)
3. **Screenshot refresh sprint** (high-priority: Data Warehouse, SSO config, Data Transformation articles)
4. **Localization retirement project** (~1,145 localized articles; requires localization team coordination)
5. **Remaining legacy cleanup** (Geocoder app notice, Buzz disambiguation, smaller Audit-flagged fixes)

---

## Appendix — Audit Statistics Summary

| Metric | Count |
|--------|-------|
| Total articles audited | 3,680 |
| Confirmed needs update | 301 |
| Possibly needs update | 2,069 |
| Deprecate | 748 |
| Mark as Legacy | 713 |
| Needs Review | 936 |
| Keep (no action) | 621 |
| Critical priority | 160 |
| High priority | 930 |
| **Total requiring action (Critical + High)** | **1,090** |

| Category | Articles audited |
|----------|-----------------|
| Data Connection (connectors + Workbench) | 1,803 |
| Visualization and Apps | 683 |
| Domo APIs (Developer Portal) | 340 |
| Data Transformation | 223 |
| Administration and Governance | 222 |
| Orchestration and Automation | 137 |
| Domo Everywhere | 81 |
| Uncategorized | 73 |
| AI & Machine Learning | 62 |
| Data Warehouse | 45 |
