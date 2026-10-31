# Domo KB Restructure Plan

## Vision

Transform the Domo KB from a feature encyclopedia into a narrative-driven product story — one that meets users where they are (new, intermediate, advanced, admin, developer) and guides them along a clear path to competency and mastery.

**The core problem in one sentence:** We have ~1,819 articles, ~70% of which are task-oriented how-to guides, and almost none of which explain what Domo is, how its pieces fit together, or where a user should go next.

**The solution:** Apply the Diátaxis framework as the taxonomy backbone, restructure navigation from 335 groups to 12 pillars, create ~30 missing "glue" articles (conceptual overviews, tutorials, section hubs), and implement systematic interlinking that creates actual reading paths.

---

## Research Foundations

### The Diátaxis Framework

The strongest evidence-backed framework for structuring a SaaS KB organizes content around **user-need states**, not product features:

| Type | User state | Question it answers | We currently have |
|------|-----------|---------------------|-------------------|
| **Tutorial** | Learning | "Walk me through X for the first time" | ~5 |
| **How-To Guide** | Doing | "How do I accomplish X?" | ~1,280 (~70%) |
| **Reference** | Looking up | "What does X mean/do?" | ~270 (~15%) |
| **Explanation** | Understanding | "Why does X work this way?" | ~20 |

**The key insight:** We are massively overweight on How-To and nearly missing Tutorials and Explanation entirely. Users who don't yet understand the conceptual model of Domo can't find or effectively use our how-to guides.

A critical Diátaxis principle: Tutorials and how-to guides serve structurally distinct purposes and must be kept separate. Tutorials serve users in **learning mode** (acquiring a skill). How-to guides serve users in **working mode** (applying a skill to a real task). Conflating them is a documented cause of documentation failure.

### Progressive Disclosure

Leading SaaS KBs (Stripe, Atlassian, Intercom, Figma) all use progressive disclosure: start with the simplest version of the truth, surface basics prominently, and link to technical depth for users who need it. Articles lead with a 1–2 sentence plain-language explanation, give the default procedure, then offer "Advanced" or "Learn more" sections for depth. This is the structural device that bridges beginner → advanced without cluttering either experience.

### Topic Clusters

Hub-and-spoke: each major product area gets one Overview/hub article that links out to tutorials, how-to guides, reference, and advanced material — rather than a flat list of disconnected articles. This is how Atlassian, HubSpot, and Notion all structure their help centers.

### Role-Based Entry Points

Different users have different jobs to be done. A data consumer's first question is "how do I find the dashboard my manager shared?" A data engineer's first question is "how do I connect our database?" Separate role-based entry points (Getting Started guides) are essential, and the best-practice implementation (used by Notion, Figma, Intercom) presents these as role cards on the homepage.

---

## The Domo Story Arc

The KB should tell this story in order, for each user role:

```
What is Domo? → First Login → Integrate Data → Manage Data → Prepare & Transform Data →
Analyze & Visualize → Share & Act → Build & Automate →
Govern & Administer → Go Deeper (AI, Dev, Advanced)
```

Every section of the KB should have a clear place in this arc, and users should always be able to see where they are and where to go next.

---

## Cross-Cutting Principle: AI as First Option

### Long-Term Vision

The eventual goal is to position AI as the *first-recommended path* for completing tasks across every product area at every level of documentation — surfacing AI Chat, the AI Playground, MCP integrations, Workflows automation, and agent-based approaches as the preferred method wherever Domo AI can accomplish what a user is trying to do.

This vision is not fully implementable in this restructure cycle. Domo's AI capabilities are not yet consistently mature enough across all product areas to make AI the default first option in every how-to guide. Attempting it now would introduce inconsistent guidance and risk sending users down paths that don't yet work reliably at scale. **The AI & Data Science pillar therefore remains its own standalone pillar for this restructure and must not be dissolved into other sections.**

### What We Can Do Now

Within the current restructure, actively surface AI-first options in other pillars wherever existing AI & Data Science content already supports it. The signal for "do this now" is simple: if an AI feature for that task already exists and is GA, surface it.

**Pattern for the callout** (add to hub articles and key how-to guides during Phase 3a and Phase 5):

```mdx
<Tip>**Try it with AI:** [AI Chat](/s/article/000005539) can answer questions about your data directly. See [AI & Data Science](/s/article/AI-and-Data-Science-Overview) for the full toolkit.</Tip>
```

**Current AI surface points by pillar:**

| Pillar | AI feature to surface | Where to add it |
|--------|-----------------------|-----------------|
| Prepare & Transform Data | Magic ETL AI (AI-assisted tile config); AI-assisted SQL in DataSet Views | Hub article + Magic ETL how-tos |
| Analyze & Visualize | Beast Mode AI Assistant; AI Chat on dashboards | Hub article + Beast Mode articles + Card Building how-tos |
| Build Apps & Automate | Workflows AI agent tasks; Code Engine + AI Service Layer API | Hub article + Workflows overview |
| Share & Collaborate | AI Chat surfaced from dashboards | Hub article |
| Develop & Integrate | AI Service Layer API; MCP connector (`Connect-AI-Tools-to-Domo-Using-MCP.mdx`) | Hub article + API overview |
| Administer & Govern | AI Readiness (DataSet prep for AI); AI governance settings | Hub article + DataSet management how-tos |
| Connect & Integrate Data | AI-assisted connector troubleshooting (where available) | Hub article only — don't force it |

**Rules for this phase:**
- Only add an AI callout if the feature is GA and the KB article for it already exists in the AI & Data Science pillar.
- Do not add placeholder callouts for capabilities that aren't available or that only exist as Alpha/Beta with restricted access — link to the existing article which will carry the access caveat.
- Do not restructure existing how-to content around the AI path. Add the callout, then continue the existing procedural steps.

### Forward-Looking Requirement for New Hub Articles

When writing new hub articles in Phase 3a, include a brief "AI-powered approaches" card group or callout section at the end of the hub where relevant AI features exist. This primes the structure for full AI-first documentation in a future pass without requiring the current restructure to solve it completely.

---

## Current State (Audit Summary)

- **1,819 articles** in `s/article/`, **126 topic pages** in `s/topic/`
- **66% opaque Zendesk IDs** (e.g. `360042925394.mdx`) — not human-readable; the `excerpt` frontmatter field provides the semantic description for these
- **335 navigation groups** in `docs.json` — ~22× too many for good discoverability
- **4 role-based getting-started articles** — needs to expand to at least 5–6 (add Admin, App Builder, Developer)
- **0 "What is X?" concept articles** for any core product area (DataSet, Magic ETL, DataFlow, Card, Dashboard, Beast Mode, App Studio, Alert, Connector)
- **Article type distribution:** ~70% How-To, ~15% Reference, ~8% Best Practices, ~5% Hub/Overview, ~2% FAQ
- **~800+ connector articles** — well-populated but need a hub page, a "how connectors work" overview, and category-level organization instead of pure A-Z
- **90+ Workbench 4/5/Enterprise articles** for legacy versions cluttering the nav with version sprawl

---

## Progress Tracking

**Progress file:** `RESTRUCTURE-PROGRESS.md` (repo root)

This file is the single source of truth for where restructure work stands across sessions. Every Claude session working on the restructure should:

1. **Read `RESTRUCTURE-PROGRESS.md` first** to orient — it shows which phase is active, what's complete, key findings, and the next concrete steps
2. **Update it at the end of every session** — mark completed tasks, add findings to the Decision Log, update "Next Steps" for the next session
3. Never assume context from prior sessions — read the progress file, read the relevant `scripts/output/` artifacts, then act

The progress file tracks: phase status, output file locations and stats, per-phase findings, PM-blocked items, and a decision log.

---

## Available Skills for Execution

The repo includes Claude skills that should be used for all article creation and navigation work. These are not optional shortcuts — they encode the style guide, template, and Mintlify conventions automatically.

| Skill | When to use |
|-------|-------------|
| `new-kb-article` | Writing any new procedural how-to or tutorial article from scratch or by synthesizing content from existing articles |
| `new-overview-article` | Writing section hub articles ("Analyze & Visualize Overview") and "What is X?" conceptual articles — handles the title-collision check and link-cluster structure specific to overview-type content |
| `update-kb-article` | Editing, restructuring, or adding sections to any existing article — renames, content edits, step updates, adding Next Steps/Related Articles, merging two articles |
| `add-to-nav` | Adding any new or moved article to `docs.json` — never hand-edit nav for new articles |

**Rule of thumb:** If you're touching an existing file → `update-kb-article`. If you're creating a net-new explanation or hub page → `new-overview-article`. If you're creating a net-new how-to or tutorial → `new-kb-article`. After any new file → `add-to-nav`.

---

## Phase 1: Audit & Inventory (Script-Driven)

**Goal:** Build a machine-readable catalog of all content before touching anything.

### 1.1 Extract Article Catalog

Write a script that reads all frontmatter and outputs a JSON catalog:

```bash
# scripts/build-catalog.js
# Output: scripts/output/catalog.json
# Schema per article:
# {
#   filename, title, excerpt, tags,
#   approx_line_count, is_slug_based,
#   current_nav_group  (cross-referenced from docs.json)
# }
```

**Note:** Use `excerpt` as the human-readable description for all numeric-ID articles. 1,818 of 1,819 articles have an `excerpt` field.

### 1.2 Classify Articles by Diátaxis Type

**Agent task:** Feed the catalog to a classification agent that assigns each article to:

```
tutorial | howto | reference | explanation | connector | release-notes | retire-candidate
```

Classification heuristics (from title + excerpt):
- Title contains "Connector" and excerpt says "Use the X Connector to import..." → `connector`
- Title contains a year and "release notes" → `release-notes`
- Title starts with "Use" or "Create" or "Add" or "Configure" → `howto`
- Title starts with "Overview" or "Introduction" or "What is" → `explanation`
- Title contains "Reference" or "Properties" or "Functions" → `reference`
- Title starts with "Getting Started" → `tutorial`

**Output:** `scripts/output/catalog-classified.json`

### 1.3 Find Orphans & Near-Duplicates

**Script:** Cross-reference all article filenames against `docs.json` → output list of articles not appearing anywhere in nav (orphaned articles).

**Agent task:** Cluster articles by excerpt semantic similarity → flag pairs/groups likely covering the same topic that should be merged.

**Output:** `scripts/output/orphans.json`, `scripts/output/merge-candidates.json`

### 1.4 Gap Analysis

**Agent task:** Using the classified catalog, identify per-product-area gaps:
- Product areas with no `explanation` article (the "What is X?" gap)
- Product areas with no `tutorial` article (the "Getting Started with X" gap)
- Product areas with only one article (likely incomplete coverage)
- Product areas with 50+ articles that may need sub-organization

**Output:** `scripts/output/gap-analysis.json` — prioritized list of missing articles to create

---

## Phase 2: Information Architecture Redesign

**Goal:** Collapse 335 nav groups into 12 content pillars, each with a defined hub-and-spoke structure.

### 2.1 The 12 Pillars

| # | Pillar | Current groups (approx.) | Approx. current articles |
|---|--------|--------------------------|--------------------------|
| 1 | Getting Started | 1 | 10 → expand to ~25 |
| 2 | Core Concepts | 0 | 0 → create ~15 |
| 3 | Connect & Integrate Data | 60+ | ~900 (connectors + Workbench) |
| 4 | Manage Data | 0 | 0 → create ~3 + pull from Prepare & Transform (pending D9) |
| 5 | Prepare & Transform Data | 8 | ~80 (or ~50 pending D9) |
| 6 | Analyze & Visualize | 25 | ~200 |
| 7 | Build Cards & Dashboards | 15 | ~100 |
| 8 | Build Apps & Automate | 20 | ~80 |
| 9 | Share & Collaborate | 10 | ~40 |
| 10 | AI & Data Science | 15 | ~50 |
| 11 | Administer & Govern | 30 | ~150 |
| 12 | Develop & Integrate | 20 | ~80 |
| — | Release Notes | 10 | all release notes |

### 2.2 Section Structure Template

Every pillar follows this hub-and-spoke pattern in the nav. The hub article is the group's **root page**, not a child: selecting the group title opens the hub. See [7.1](#71-nav-authoring) for how this is encoded in `docs.json`.

```
[Pillar Name]                      ← group root: Overview hub article, new or rewrite
├── What is [X]?                   ← explanation article, new
├── Getting Started with [X]       ← tutorial, new or upgrade
├── Key Concepts                   ← 3–8 explanation articles
├── How-To Guides
│   ├── [Task cluster 1]
│   │   ├── [How-to 1]
│   │   └── [How-to 2]
│   └── [Task cluster 2]
├── Reference
│   ├── [Properties/Settings reference]
│   └── [Functions/Commands reference]
└── Advanced
    ├── [Admin-level feature]
    └── [Integration pattern]
```

### 2.3 Special Handling: Connector Articles (~900 articles)

Connectors are a reference library — they don't need full story treatment per article but need a proper hub and category organization.

**Proposed structure for "Connect & Integrate Data":**

```
Connect & Integrate Data                          ← root: Connecting Your Data to Domo hub (frames read + write)
├── Getting Started: Connect Your First DataSet   ← new tutorial
├── How Connectors Work (OAuth, scheduling, etc.) ← root: What is a Connector? (new explanation)
└── Connector Library — Reference                 ← root: Connector Library Overview; "most commonly used" curated list
    ├── Cloud Data Warehouses                     ← CDW sub-groups promoted within the library; root: Cloud Data Warehouses Overview (Cloud Amplifier as #1 for all CDWs)
    │   ├── Snowflake (hub → existing articles)   ← read + write framing; Cloud Amplifier first
    │   ├── Google BigQuery
    │   ├── Databricks
    │   └── Amazon Redshift/Athena
    ├── Connectors A-B
    ├── Connectors C-F
    │   ... (alphabetical)
    ├── Writeback Connectors                      ← integrated into library; not a top-level section
    └── Files & APIs
```

**Key structural decisions from workshop (2026-06-17):**
- Cloud Data Warehouses and the Connector Library are one section, not two. CDWs are connectors.
- Writeback Connectors are not a standalone section. CDW writeback is in each CDW's sub-group; standard writeback connectors appear alphabetically in the library alongside read connectors.
- "Data Providers" terminology replaced with "Connectors" throughout.
- Connector Library stays alphabetical. No use-case grouping for the main list.
- Each article in the alphabetical groups is placed and sorted by its **title**, and the title is the connector name with no lead-in prose ("Adobe Analytics Data Warehouse", not "Connecting to Adobe Analytics Data Warehouse"). In the last group, titles that start with a number sort after the letters.

### 2.3a Read/Write Framing Convention

**This applies to all articles in the Connect & Integrate Data pillar.**

The pillar covers both directions of data movement. Authors must treat read and write as a pair — not as separate concerns, with write as an afterthought.

**Convention:** The pillar overview article and every technology section (Cloud Amplifier/CDW, Connectors, Workbench) must explicitly address both its read path (bringing data into Domo) and its write path (writing data back to source systems) before linking to detailed how-tos. Section overview articles should answer both "How do I get data from X into Domo?" and "How do I write data back to X from Domo?" in sequence.

**Why:** Without this framing, writeback documentation becomes invisible. Users who land in the CDW section or Connector Library looking to write data back have no way to discover that capability unless the section overviews introduce both directions upfront.

### 2.4 Workbench Rationalization

Current: 3 separate Workbench sections (Enterprise, 5, 4) with ~90 articles.

Proposed: One "Workbench" section with:
- Current version content prominently first
- Legacy version content clearly labeled under a "Legacy Versions" collapsible group
- `What-is-Workbench` as the group root, with a "Which version do I have?" decision article as the first child

This collapses ~3 nav sections and removes ~35 Workbench 4 articles from primary nav visibility.

---

## Phase 3: Content Creation (The Missing Glue)

**Goal:** Fill the ~30-article gap in conceptual and hub content. The strong preference is to **synthesize from existing how-to content** rather than write from scratch — our procedural articles already contain most of the conceptual raw material, just buried in intros and context paragraphs. Writing net-new articles from existing content keeps the KB internally consistent, respects what writers have already built, and avoids introducing factual drift.

### Content Creation Strategy

**Default approach — synthesize from existing how-tos:**

Most "What is X?" and hub articles can be built by:
1. Identifying the 3–8 best existing how-to articles on the topic
2. Extracting their opening/context paragraphs, which usually define the feature
3. Synthesizing those into a coherent explanation-type article in the new format
4. Adding the hub's card/link structure pointing back to those source articles

This is agent-assistable: an agent can read a set of existing articles, extract definitional content, and draft the new article; a human reviews and publishes via the `new-overview-article` or `new-kb-article` skill.

**Exception — genuinely new content needed from PM:**

Some articles require product-level narrative that isn't derivable from existing how-tos — positioning calls, end-to-end pipeline framing, "when to use which tool" decision guidance. These require PM input before writing can start. See [PM Input Required](#pm-input-required) below.

**Important execution note:** Net-new articles must be authored in the main session (not sub-agents) due to the sub-agent write-block on creating new files. All new articles use the `new-kb-article` or `new-overview-article` skill and must be added to nav with `add-to-nav` immediately after creation.

---

### 3.1 Net-New Articles — Synthesizable from Existing Content

These ~26 articles can be drafted by reading existing how-tos and reformatting the conceptual content into the new article type. No PM input required to start; PM review recommended before publishing.

**Tier 1 — Story entry points (write first; everything else links to these):**

| # | Article | Skill | Primary source articles to synthesize from |
|---|---------|-------|--------------------------------------------|
| 1 | `What-is-Domo.mdx` | `new-overview-article` | `000005874` (Intro to Domo), Getting Started for Data Consumers, Getting Started for Data Engineers |
| 2 | `Getting-Started-for-Admins.mdx` | `new-kb-article` | Existing admin how-tos: user management, roles/grants, governance, security settings |
| 3 | `Getting-Started-for-App-Builders.mdx` | `new-kb-article` | `000005295` (App Studio Overview), Wire an App, Workflows overview |
| 4 | `Getting-Started-for-Developers.mdx` | `new-kb-article` | API authentication, Access Tokens, MCP article, Code Engine overview |

**Tier 2 — Core concept articles (synthesize from the many how-tos that assume this knowledge):**

| # | Article | Skill | Primary source articles to synthesize from |
|---|---------|-------|--------------------------------------------|
| 5 | `What-is-a-DataSet.mdx` | `new-overview-article` | Connector how-tos (all define DataSets implicitly), Magic ETL input tile articles |
| 6 | `What-is-Magic-ETL.mdx` | `new-overview-article` | Magic ETL overview articles, Data Selection in Magic ETL, Magic ETL tiles reference |
| 7 | `What-is-a-DataFlow.mdx` | `new-overview-article` | DataFlow creation and management articles, Advanced DataFlow Triggering |
| 8 | `What-is-a-Card.mdx` | `new-overview-article` | Analyzer Overview, existing card-type intro paragraphs |
| 9 | `What-is-a-Dashboard.mdx` | `new-overview-article` | Dashboard/page management articles |
| 10 | `What-is-Beast-Mode.mdx` | `new-overview-article` | Beast Mode FAQs, Beast Mode functions reference intro sections |
| 11 | `What-is-App-Studio.mdx` | `new-overview-article` | `000005295` (App Studio Overview) — primarily a reformat of this into a true explanation |
| 12 | `What-is-an-Alert.mdx` | `new-overview-article` | Alert creation articles, Alert Center article |
| 13 | `What-is-a-Connector.mdx` | `new-overview-article` | General Connector Information section articles |
| 14 | `What-is-Domo-AI.mdx` | `new-overview-article` | Domo AI FAQ, AI Playground, Magic ETL AI, AI Chat articles |
| 15 | `What-is-Workbench.mdx` | `new-overview-article` | Workbench 5.2 overview article, Workbench Enterprise articles |

**Tier 3 — Section hub articles (curate links + write brief intro; one per pillar):**

All 8 hub articles use the `new-overview-article` skill, which is designed exactly for this pattern. Source material is the set of existing articles that will nest under each hub. Each hub becomes its pillar's group `root` (see [7.1](#71-nav-authoring)), not a child page.

| # | Article | Source content |
|---|---------|---------------|
| 16 | `Connect-and-Integrate-Data-Overview.mdx` | All connector, Workbench, and writeback articles |
| 17 | `Prepare-and-Transform-Data-Overview.mdx` | Magic ETL, DataFlows, Data Models, DataSet unions articles |
| 18 | `Analyze-and-Visualize-Overview.mdx` | Analyzer, chart types, Beast Mode, KPI card articles |
| 19 | `Build-Apps-and-Automate-Overview.mdx` | App Studio, Workflows, Forms, Code Engine articles |
| 20 | `Share-and-Collaborate-Overview.mdx` | Sharing, Publications, Buzz, embed articles |
| 21 | `AI-and-Data-Science-Overview.mdx` | Domo AI, DomoStats, Jupyter, AutoML articles |
| 22 | `Administer-and-Govern-Overview.mdx` | Admin settings, Governance Toolkit, roles, security articles |
| 23 | `Develop-and-Integrate-Overview.mdx` | REST API, SDKs, MCP, CLI, Code Engine articles |

**Tier 4 — Structural upgrade articles (synthesizable, no PM input needed):**

| # | Article | Skill | Source articles |
|---|---------|-------|----------------|
| 24 | `Domo-User-Roles-and-What-They-Can-Do.mdx` | `new-overview-article` | Roles/grants articles, custom roles, system roles |
| 25 | `Security-and-Permissions-Overview.mdx` | `new-overview-article` | PDP, access rights, OAuth, security settings articles |
| 26 | `Domo-Sandbox-and-Promotion-Overview.mdx` | `new-overview-article` | Sandbox article(s), linked repository article |

---

### 3.2 PM Input Required

These articles require product-level narrative that isn't reliably derivable from existing how-to content — they involve positioning calls, end-to-end pipeline framing, or "when to use which tool" guidance that a PM must own.

**Before writing any of these, get PM sign-off on the core narrative/decision framework. Do not draft from assumptions.**

| # | Article | What PM needs to provide |
|---|---------|--------------------------|
| P1 | `How-Data-Flows-Through-Domo.mdx` | The canonical end-to-end pipeline narrative (Connect → Prepare → Analyze → Share → Govern). This is a strategic framing document — PMs need to bless how the pipeline is described, especially for edge cases like real-time ingestion, writeback flows, and Cloud Amplifier. |
| P2 | `Choosing-the-Right-Data-Prep-Tool.mdx` | When to use Magic ETL vs SQL DataFlow vs Python/R scripting vs Data Models. This is a product positioning call — engineering teams have opinions but PM owns the recommended path for each use case. |
| P3 | `Understanding-DataSet-Joins-and-Relationships.mdx` | The "when to use ETL joins vs Data Models vs DataFlows" decision guidance. The technical content is synthesizable; the _recommendation_ requires PM/product input on intended use-case boundaries. |
| P4 | `Domo-for-Mobile-Overview.mdx` | Existing mobile articles may be thin or out of date. PM needed to confirm current mobile feature scope before writing an overview that will set user expectations. |

---

### 3.3 Article Structure Upgrade (Bulk Edit — `update-kb-article`)

~200 existing articles need structural upgrades via the `update-kb-article` skill, not full rewrites. Specifically, every article that currently lacks:

- A 1–2 sentence concept intro ("What it is and why you'd use it") at the very top
- A "Prerequisites" section where implicit dependencies exist
- A "Next Steps" section at the bottom with 2–4 forward links
- A "Related Articles" section with 3–5 lateral links

**Agent task (parallelizable in batches of 50):**
1. Read article content
2. Check if concept intro is present in first paragraph; if not, generate one from the `excerpt` field
3. Identify logical next steps from topic + Domo product structure
4. Append structured `## Next Steps` and `## Related Articles` sections
5. Write changes via Edit (not Write — articles already exist)

---

## Phase 3c: Main Branch Content Sync

**Goal:** Bring new articles and factual updates that landed on `main` after the branch cut into the restructure branch — without reverting any restructure rewrite. This is **NOT** a `git merge` of main (that would restore pre-restructure structure).

**Two syncs, by design:**
- **Sync #1 — during the content phases**, while filenames on both branches still match numeric IDs, so reconciliation is filename-based and conflicts are minimal. (Executed 2026-08-20; see `RESTRUCTURE-PROGRESS.md` › Phase 3c and `RESTRUCTURE-MANIFEST.md` › Phase 3c.)
- **Sync #2 — immediately before the final merge**, after Phase 6 has renamed most files to slugs. Because filenames no longer match, sync #2 depends on the parity system below.

**Parity system (for sync #2, post-rename).** The immutable key is the **numeric KB article ID** — `main` never renames, so it uses this ID forever. Two sources translate an ID to its current restructure location and disposition:
1. **Frontmatter ID stamp** — see **Phase 6.0**. HARD DEPENDENCY: the stamp must run *before* Phase 6 renames anything, or the parity system breaks. Once stamped, identity lives inside the file and survives any rename.
2. **Disposition map from `RESTRUCTURE-MANIFEST.md`** — every article's fate (renamed / merged / split / archived / deleted, source→target) routes each `main` change to the right target(s).

**Sync #2 procedure:** `git diff <sync#1-point>..origin/main` → resolve each changed numeric ID via the frontmatter stamp + manifest map → **renamed/kept** = 3-way apply to the new file; **merged/split** = route to target(s) + human review; **archived/deleted** = surface for a human call; **main-added** = import + place in nav. The delta is only what `main` changed since sync #1, so it stays small and fast.

Full step-by-step procedure and the sync #1 execution log live in `RESTRUCTURE-PROGRESS.md` › Phase 3c.

---

## Phase 4: Consolidation & Retirement

**Goal:** Reduce noise; merge overlapping content; archive legacy material.

### 4.1 Merge Candidates

**High-confidence (script-detectable by excerpt similarity):**
- Workbench articles where content is >80% identical across versions → merge with version callout sections
- Connector articles that have separate "Setup" and "Advanced Setup" variants for the same connector → combine with progressive disclosure
- Release notes 2015–2019 → collapse to one summary article per year; remove from primary nav

**Needs human judgment:**
- Article pairs where excerpt similarity is high but use-cases may legitimately differ
- Beta articles that are positioned to replace existing stable articles (decide: replace or merge with callout)

### 4.2 Retirement Candidates

**Script-detectable:**
- Articles with <100 words (stubs with no real content)
- Articles where `tag: "Deprecated"` is set in frontmatter
- Legacy release notes pre-2022 (move to archive nav group, remove from main nav)

**Agent-detectable:**
- Articles whose excerpt describes a feature no longer in the product
- Articles fully superseded by a newer article on the same topic (identified by the merge-candidates analysis in Phase 1.3)

**Support KB Audit — confirmed retirement list (use as Phase 4 execution input):**

The Support team's audit of 3,680 articles (completed 2026-04-28, `KB Audit Results.csv`) provides a per-article deprecation/legacy verdict for content the restructure would otherwise need to re-analyze from scratch. Use this data directly as the Phase 4 execution list for these categories:

| Category | Audit finding | Phase 4 action |
|----------|--------------|----------------|
| Workbench 4 articles (37) | 118 of 188 total Workbench articles flagged Deprecate or Mark as Legacy | Archive — confirms D1 |
| DataFusion articles (11) | 6 Deprecate, 5 Mark as Legacy — all flagged; feature confirmed discontinued | Archive all 11 |
| Old Magic ETL tile articles (15) | 15 flagged Mark as Legacy or Deprecate — legacy tile interface, not current ETL UI. 1 article (`Create a Recursive/Snapshot Old Magic ETL DataFlow`) is flagged Keep — do not archive. | Archive 15; keep 1 |
| Defunct-service connectors (111 confirmed) | 111 connector articles where the Audit summary confirms the underlying service no longer exists or the connector is entirely non-functional. Named examples confirmed dead: LinkedIn Connector (API v1 disabled 2019), Pinterest Connector (disabled 2018), StumbleUpon (shut down 2018), Simply Measured (shut down 2017), Salesforce Desk (discontinued 2017), IBM Digital Analytics/Coremetrics (discontinued by IBM), Snowflake Writeback (deprecated Oct 2025), Adobe Analytics Advanced Legacy (new datasets blocked), DCM via Google Cloud Storage (OAuth deprecated by Google). Note: not all LinkedIn/Pinterest connector articles are dead — LinkedIn Ads and LinkedIn V2 connectors are active; the original LinkedIn Connector (v1) is the dead one. | Archive or remove from primary nav |
| CourseBuilder articles (16) | 3 Deprecate, 5 Mark as Legacy, 4 Needs Review, 4 still flagged for evaluation — tool confirmed retired from Domo Appstore | Confirm with PM → Archive all 16 (see D10 in `RESTRUCTURE-IA-SPEC.md`) |
| Release notes pre-2022 (all languages) | Confirmed negligible self-service value; flagged across all locales | Move to collapsed Archive nav group in Phase 7 |

> **Urgent — fix before Phase 4 begins:** Snowflake connector articles (`Snowflake Connector`, `Snowflake Unload V2 Connector`) document key-pair/password authentication that Snowflake retired November 2025. Customers attempting new connections today are actively failing. Use `update-kb-article` on these two articles immediately to add a deprecation notice and link to the current Cloud Amplifier / OAuth setup path. Do not wait for Phase 4.

---

## Phase 5: Interlinking & Pathways

**Goal:** Make every article part of a navigable network rather than a dead end.

### 5.1 "Next Steps" Systematic Addition

**Agent task (batch, all articles):** For every article, identify 2–4 logical follow-on articles and add a `## Next Steps` section at the bottom.

Follow-on logic by article type:
- Connector setup article → next steps: "Prepare your DataSet in Magic ETL" + "Create your first Card"
- Concept explanation → next steps: relevant getting-started tutorial + the primary how-to
- How-to guide → next steps: related how-tos + "Going deeper" reference article
- Tutorial → next steps: first practical how-to + key reference article

### 5.2 Related Pages (Mintlify native feature)

Replace the hand-written `## Related Articles` markdown sections with Mintlify's native [Related Pages](https://www.mintlify.com/docs/organize/related-pages) feature. Mintlify renders a "Related topics" block for us; it supports an **automatic** mode (suggestions generated from the content search index by page title) and per-page **manual overrides** via the `related` frontmatter field, and the manual definitions take precedence over the auto suggestions wherever we set them. Ultimately we want curated relations where we've chosen them and sensible auto-fill everywhere else, with no hand-maintained markdown to keep in sync.

Three steps:

1. **Remove the existing `## Related Articles` sections.** ~40 articles currently carry a hand-written `## Related Articles` heading (from Phase 3b upgrades / legacy content); none use the `related:` frontmatter field yet. Bulk pass to strip these sections so the native feature is the single source of related links and nothing renders twice.

2. **Define relations with the `related` frontmatter field.** For as many pages as practical, set explicit relations in frontmatter — an array of root-relative KB paths (and, where useful, Developer Portal paths or external URLs), optionally as `Title: /path` objects to control the label. The excerpt-level term-overlap script keeps its original job of generating candidate lists; the agent validates them and writes the chosen 3–5 into `related:` instead of a markdown section. Use `related: false` to suppress the block on pages where related links aren't wanted (e.g. hub/overview pages that already cluster links). Example:
   ```yaml
   related:
     - /s/article/What-is-Magic-ETL
     - Create a DataFlow: /s/article/What-is-a-DataFlow
     - /s/article/Beast-Mode-Window-Functions
   ```

   **Use `s/topic/` to find page relationships.** The legacy Salesforce topic pages in `s/topic/` (~115 `.mdx` files) are human-curated clusters: each one groups a set of related articles and sub-topics (e.g. "Connect Data to Domo" → Cloud Data Warehouses, On-premises Systems, Data Providers A–Z, …). They are excluded from the restructure nav, but as a *relationship signal* they are high-value — they encode editorial judgment about which articles belong together that the excerpt-level term-overlap script can't infer. When curating `related:` relations (and the `## Next Steps` logic in 5.1), you can and should mine `s/topic/` for candidate clusters: resolve each topic's listed members (legacy IDs/slugs → current articles via the `legacy_id` frontmatter stamp from Phase 6.0 and the manifest map), then validate and promote the still-relevant pairings into `related:`.

3. **Enable automatic mode in Mintlify.** Turn on Related Pages in the Mintlify dashboard (General → "Related topics" → Show related topics; choose automatic mode, display limit default 5 / max 10). Automatic mode then covers every article — even those we didn't curate — while our frontmatter `related` definitions override the auto suggestions wherever present.

4. **Delete `s/topic/` once relationship mining is complete.** `s/topic/` is legacy grouping-page content that the restructure does not carry forward (it is already excluded from the new IA — see Phase 2). Its only remaining value is as the relationship source in step 2. Once that mining pass is done and the relations have been promoted into `related:` frontmatter, **delete the entire `s/topic/` directory** (and remove any `s/topic/*` references from `docs.json` and the localized `{de,es,fr,ja}/s/topic/` mirrors). Do this as the closing action of 5.2 — not before — because the directory is the input the earlier steps depend on. Log the deletion in `RESTRUCTURE-MANIFEST.md`.

**Implementation notes:**
- The dashboard toggle is a one-time Mintlify admin action — **dashboard-only**, with no `docs.json` key, CLI, or public API to set it — so it must be done by hand in app.mintlify.com (General → "Related topics"). Route it to the KB Administrator. Note the `related:` frontmatter is **inert until that toggle is on**: it customizes the block but does not enable the feature, so no related links (curated or automatic) render until the switch is flipped.
- `related:` paths are internal links, so Phase 6 (slug rename + internal-link updates) must rewrite them alongside body links.
- This supersedes the per-article `## Related Articles` sections called for in Phase 3b and the Phase 5 Interlinking Agent. `## Next Steps` (5.1) is unaffected — it stays an in-article section.

### 5.3 Role Pathway Cards on Section Hubs

Every section hub article includes a role-selector `<CardGroup>` block near the top:

```mdx
<CardGroup cols={3}>
  <Card title="I'm new to this" href="/s/article/Getting-Started-with-X">
    Start with the basics
  </Card>
  <Card title="I know the basics" href="#how-to-guides">
    Jump to How-To Guides
  </Card>
  <Card title="I need advanced config" href="#advanced">
    Advanced options
  </Card>
</CardGroup>
```

### 5.4 "You Are Here" Context Breadcrumbs

For every deeply-nested article, add a one-line context statement at the top identifying where the article sits in the product story. Currently absent for all articles, and disorienting for users who land on an article from search.

Example at the top of a Beast Mode article:
```
This article is part of **Analyze & Visualize → Beast Mode**. New to Beast Mode? [Start here.](/s/article/What-is-Beast-Mode)
```

### 5.5 KB ↔ Developer Portal Cross-Linking

**Goal:** Make the KB and Developer Portal function as a unified documentation network rather than two parallel but disconnected systems. A user should be able to move fluidly from a KB how-to into the developer-level depth the portal offers, and vice versa — the portal already does the vice-versa half in ~45 places.

**Context — how the portal currently links to the KB:**

The Developer Portal (`portal/` directory) already references KB articles in at least these areas:

| Portal area | KB articles already linked |
|-------------|---------------------------|
| Authentication & API access | Access Token management, client revocation |
| Connectors & Cloud Amplifier | Cloud Amplifier (4412849158167), Workbench, Jupyter |
| Code Engine | Code Engine functions reference (000005173) |
| Workflows | Create a Workflow (000005331), Workflows overview (000005108) |
| AI services | AI Chat (000005539), AI Playground (000005236), AI Models (000005502), Beast Mode AI (000005304), Forecasting (000005567) |
| Jupyter Workspaces | Jupyter User Guide, Jupyter Troubleshooting, Jupyter + GitHub |
| DataSets / Governance | DataSet management, PDP policies, access token revocation |
| Embed | Embed how-tos |
| App Studio / Apps | App Studio how-tos (000005295, 000005331) |

These portal→KB links are the highest-priority targets for adding the reverse KB→Portal link: users already in those KB articles are the most likely audience for developer-level depth.

**Interlinking priorities by pillar:**

| KB Pillar | Primary Developer Portal targets | Link direction note |
|-----------|----------------------------------|---------------------|
| Connect & Integrate Data | `portal/Connectors/` — Custom Connectors, Writeback Connectors, API Connections, Federated Queries | KB connector setup articles → Portal for API/programmatic data ingestion |
| Prepare & Transform Data | `portal/data-science/scripting-tiles`, `portal/data-science/jupyter` | KB DataFlow and ETL articles → Portal for scripting-based prep |
| Analyze & Visualize | `portal/API-Reference/Product-APIs/` — Cards API, Beast Modes API | KB card/Beast Mode articles → Portal for programmatic card management |
| Build Apps & Automate | `portal/Apps/`, `portal/Automate-Actions/` — App Framework, Workflows API | KB App Studio + Workflows articles → Portal for pro-code and API-driven automation |
| AI & Data Science | `portal/data-science/`, `portal/API-Reference/app-framework-apis/AI-Service-Layer-API` | KB AI articles → Portal for AI Service Layer API, scripting-based ML, AutoML |
| Administer & Govern | `portal/Governance/` — PDP, content management, data management APIs | KB PDP and governance articles → Portal for API-driven governance automation |
| Develop & Integrate | All `portal/API-Reference/` sections | This pillar is the primary bridge; every new article should link to the corresponding Portal API reference |

**How to execute (agent task, Phase 5):**

1. Read each portal file that already links to KB articles (identified by `grep -r "s/article" portal/ --include="*.mdx" -l`).
2. For each portal→KB link found, extract the KB article path and the portal page path.
3. Output `scripts/output/portal-kb-crosslinks.json` — a bidirectional map: `{kb_article, portal_page, portal_section_title}`.
4. For each KB article in the map, add a developer callout near the Related Articles section using this pattern:

```mdx
<Note>**For developers:** This feature is also accessible via the Domo API. See [Resource Name](/portal/path) in the Developer Portal for programmatic access and API reference.</Note>
```

5. For Develop & Integrate hub and sub-articles (Phase 3a), make portal links primary, not secondary — the portal is this pillar's source of truth for reference content.

**Output:** `scripts/output/portal-kb-crosslinks.json`

### 5.6 Normalize legacy KB full-URL links to root-relative paths

Many migrated articles link to KB content with the **legacy absolute host** instead of a root-relative path — ~1,550 `https://domo-support.domo.com/s/article/...` links today, plus smaller counts on other retired KB hosts (`knowledge.domo.com`, `domohelp.domo.com`, `wiki.domo.com`). These bypass in-site navigation (Mintlify treats them as external links — no client-side nav), rot if the legacy host is ever retired, and dodge the Phase 6 slug/redirect machinery. Convert each legacy KB URL to its root-relative equivalent:

- `https?://domo-support.domo.com/s/article/<ID>[?query][#anchor]` → `/s/article/<ID>` (keep any `#anchor`; drop tracking query params)
- `https?://domo-support.domo.com/s/topic/<sf-id>/<slug>` → the current `/s/topic/<file>` (a lookup, not mechanical — the legacy path carries a Salesforce topic ID; resolve by slug)
- bare `.../s/` or `.../` (KB home) → the KB landing path
- same treatment for the other retired KB hosts wherever the target resolves to a current article

**Scope guard — do NOT relativize genuinely external Domo hosts:** `developer.domo.com`, `community-forums.domo.com`, `university.domo.com` / `learndomo.domo.com`, `embed.domo.com`, `oauth.domo.com`, `app.domo.com`, `www.domo.com` (marketing), `*.domo.com` customer instances, etc. Only hosts serving the SAME content now published on this Mintlify site become relative. When a legacy URL's target can't be resolved to a current article (merged/retired/deleted in Phase 4), flag it for review rather than guess.

**Ordering:** run this as a Phase 5 pre-pass, before 5.1–5.2. Because it leaves `/s/article/<numeric-ID>` paths behind, Phase 6.6 then rewrites those IDs to final slugs automatically — no special-casing. Script-generated, agent/spot-checked; log converted/flagged counts per host in `RESTRUCTURE-MANIFEST.md`.

**Output:** edited article files + a per-host conversion/flag report

---

## Phase 6: Rename to Slugs (Migration Script)

**Goal:** Replace 1,575 opaque ID-based filenames with human-readable slugs derived from the `title` field.

### 6.0 Prerequisite — Stamp Numeric IDs into Frontmatter (REQUIRED before any rename)

**Before renaming a single file**, stamp each article's original numeric KB ID into its frontmatter (e.g. `legacy_id: "000005874"`). The current filename stem *is* the ID, so this is a deterministic bulk pass over `s/article/`.

This is a **hard dependency for the second main-branch sync (Phase 3c, sync #2)**. `main` never renames its files, so after this rename `main`'s changes can only be matched to our renamed files by the numeric ID. If the ID lives *only* in the filename, renaming destroys the one key that links a `main` change to its restructure counterpart. With the ID in frontmatter, identity survives the rename and a grep resolves any numeric ID to its current slug file. **Do not run the rename script until this pass is complete and committed.** See Phase 3c for the full parity system.

### 6.1 Rename Script

```python
# scripts/rename-to-slugs.py
# 1. Read all articles, extract title from frontmatter
# 2. Slugify: lowercase, spaces → hyphens, strip special chars
# 3. Check for collisions (append -2, -3 suffix if needed)
# 4. Build rename mapping: {old_path: new_path}
# 5. Output: scripts/output/rename-mapping.json (dry run by default)
# 6. With --execute flag: git mv each file
```

### 6.2 Update Internal Links

**Script:** Read `rename-mapping.json`, find all occurrences of old paths (by filename) in all `.mdx` files and `docs.json`, replace with new slug paths. In `docs.json` this covers group `root` values as well as `pages` entries, and the override map in `scripts/group_roots.json` must be rewritten the same way.

### 6.3 Generate Redirect Map

Output a `redirects.json` (or Mintlify-compatible redirect config entries) mapping every old numeric ID to its new slug. This preserves existing bookmarks, external links, and any SEO value accrued on old URLs. **Every entry must set `"permanent": true`** (308, not the 307 that `permanent: false` produces) — set it explicitly rather than relying on the platform default. See `RESTRUCTURE-PROGRESS.md` § 6.5 for the exact entry shape and the validation requirement.

### 6.4 Execution Order

1. Run rename script in dry-run mode → review `rename-mapping.json`
2. Human reviews mapping for odd slugs or collisions
3. Execute renames (`--execute` flag)
4. Run link-updater script
5. Run nav validator (Phase 7)
6. Commit as a single atomic commit with message: "migrate: rename articles from ID-based to slug-based filenames"

### 6.5 GitHub Actions for Ongoing Automation

After the slug rename completes, the following GitHub Actions keep the documentation system healthy automatically on every PR and push. Implement these alongside the rename so the slug-based system stays consistent from day one.

**Pre-implementation audit:** Before building these, run a quick audit of `.github/workflows/` — existing actions (`case-collision-check.yml`, `mint-preview.yml`, `sync-api-docs.yml`, `sync-video-library.yml`) already cover case collisions and OpenAPI sync. New actions should not duplicate these.

| Action | Trigger | What it does |
|--------|---------|--------------|
| **Nav validator** | PR, push to `main` | Runs `scripts/validate-nav.js`; fails the PR if any `docs.json` page or `root` ref points to a missing file, if any article in `s/article/` has no nav entry, or if the root rules in 7.2 are broken | Extends the Phase 7 validator |
| **Orphan detector** | PR, push to `main` | Flags any new `.mdx` file in `s/article/` not referenced in `docs.json` — catches articles added without a nav entry | New: `scripts/check-orphans.js` |
| **Slug linter** | PR only | Checks that new article filenames follow the slug convention (lowercase, hyphens only, no special characters) — prevents regression to numeric IDs | New: `scripts/lint-slugs.js` or a remark lint rule |
| **Numeric-ID ref checker** | PR, push to `main` | After Phase 6, greps all `.mdx` files and `docs.json` for any remaining `s/article/[0-9]` references — enforces migration completeness as new articles are added | New: simple grep action |
| **Redirect integrity check** | PR, push to `main` | Validates every entry in `redirects.json` points to a real slug — catches cases where a slug is later changed without updating the redirect map | Extend nav validator or new script |
| **Stale internal link reporter** | Weekly `schedule` | Scans all internal links across `.mdx` files and `docs.json`; opens a GitHub Issue listing broken refs | New script; weekly cron |

**Priority order for implementation:**
1. Nav validator — highest priority; prevents broken site deployments
2. Orphan detector — prevents nav drift as articles are added
3. Numeric-ID ref checker — enforces the migration stays clean
4. Slug linter — guards filename convention going forward
5. Redirect integrity check — SEO and bookmark protection
6. Stale link reporter — maintenance, lowest urgency

**Note for non-technical contributors:** These actions run silently in the background. A failing check blocks a PR from merging. If your PR is blocked, a technical contributor can resolve the specific validation error — it usually means a file was added or renamed without updating `docs.json`, which is a one-line fix.

---

## Phase 7: Navigation Rebuild

**Goal:** Rebuild `docs.json` to implement the 12-pillar IA, validate all references, and eliminate orphans.

### 7.1 Nav Authoring

New `docs.json` navigation authored to match the Phase 2 structure. Each group's hub article is set as the group's Mintlify [`root`](https://www.mintlify.com/docs/organize/navigation#root-page) page: selecting the group title opens the hub, so the hub is not repeated as a child.

**Rules:**
- A group with an Overview or "What is X?" hub sets `"root"` to it, and the hub is **not** also listed in `pages`. Listing it in both makes it appear twice.
- `"root"` comes directly after `"group"`.
- Every **top-level** group (pillar) with a root also sets `"expanded": true` directly after `"root"`, so its sub-groups show by default. Nested groups set `root` only, never `expanded`.
- Groups with no hub article stay rootless and keep their pages as plain children.
- Groups inside the Archive pillar are not rooted. The Archive pillar itself is.
- A group must keep at least one child page alongside its root.

Example:

```json
{
  "group": "Prepare & Transform Data",
  "root": "s/article/Prepare-and-Transform-Overview",
  "expanded": true,
  "pages": [
    {
      "group": "Magic ETL",
      "root": "s/article/What-is-Magic-ETL",
      "pages": [
        "s/article/Magic-ETL-Getting-Started",
        "s/article/Magic-ETL-Tiles-Reference",
        ...
      ]
    }
  ]
}
```

**Tooling:** on the Knowledge Base tab, `scripts/apply_group_roots.py` proposes and applies roots: dry-run by default, `--apply` to write `docs.json`. Decisions and `null` overrides live in `scripts/group_roots.json`, which wins over the script's auto-proposal. The Developer Portal tab follows the same rules but is maintained by hand. Localized tabs (`ja`, `fr`, `de`, `es`) mirror the English roots in Phase 6.

**OpenAPI sync caveat:** when a Product APIs spec re-syncs, `sync-api-docs.yml` replaces that whole group with endpoint-only pages, which drops the group's `root` and its overview page. Re-add them after each sync.

### 7.2 Validation Script

```bash
# scripts/validate-nav.js
# 1. Parse docs.json, extract all page references, including group "root" values
# 2. Check each reference resolves to a real file
# 3. Check each file in s/article/ appears at least once in nav (as a page or a root)
# 4. Check root rules: no root page also listed in its group's pages, every
#    rooted group keeps at least one child page, expanded only on top-level groups
# 5. Report: broken references, orphaned articles, root-rule violations
# Exit code 1 if any errors (integrate with CI/pre-commit hook)
```

### 7.3 Orphan Handling

Articles not appearing in nav after rebuild: add to a `_uncategorized` holding group for human triage — determine if each should be placed in a pillar, merged with another article, or retired.

---

## Agent Execution Specifications

### Phase 1 Catalog Builder

- **Input:** All `.mdx` files in `s/article/`
- **Tool:** Bash (grep frontmatter), Read (sample articles)
- **Output:** `scripts/output/catalog.json`
- **Parallelism:** Grep is synchronous; single-pass

### Phase 1 Classification Agent

- **Input:** `catalog.json` (title + excerpt per article)
- **Tool:** Agent reading catalog in batches
- **Output:** `catalog-classified.json` with `type` field added per article
- **Parallelism:** Can classify in batches of 100 articles per agent call

### Phase 1 Gap Analysis Agent

- **Input:** `catalog-classified.json`
- **Tool:** Agent reasoning over the classified catalog
- **Output:** `gap-analysis.json` — list of `{product_area, missing_types, priority}`
- **Parallelism:** Single agent, sequential

### Phase 3b Article Upgrade Agent

- **Input:** Article path + catalog entry
- **Tool:** Read article, Edit to add sections
- **Output:** Edited article file
- **Parallelism:** Batches of 25–50 articles; Edit tool (not Write)
- **Constraint:** Agents can Edit existing files; cannot Write new files — net-new articles must be authored in main session

### Phase 5 Interlinking Agent

- **Input:** Article + catalog entries for topic-adjacent articles
- **Tool:** Read article, Edit to add the `## Next Steps` section (5.1) and the `related:` frontmatter field (5.2); strip any existing `## Related Articles` section
- **Output:** Edited article
- **Parallelism:** Batches of 25–50; Edit tool

### Phase 7 Nav Validator

- **Input:** `docs.json` + `s/article/` directory listing
- **Tool:** Bash (find, grep), Read (parse docs.json)
- **Output:** Validation report to stdout; exit 1 on errors

---

## Execution Roadmap

| Phase | Executor | Estimated effort | Output artifacts |
|-------|----------|-----------------|------------------|
| 1: Audit & Inventory | Script + Agent | 1–2 days | `catalog.json`, `catalog-classified.json`, `gap-analysis.json`, `merge-candidates.json` |
| 2: IA Design | Human + Agent | 2–3 days | New nav spec document, section structure definitions |
| 3a: Net-New Articles (~26 synthesizable) | Human (main session) via `new-kb-article` / `new-overview-article` + `add-to-nav` | 2–3 weeks | ~26 new `.mdx` files |
| 3a-PM: PM Input Articles (4) | PM provides narrative → Human writes | Async; unblock in parallel | 4 new `.mdx` files |
| 3b: Article Upgrades (~200) | Agent (batch) via `update-kb-article` | 2–3 days | ~200 articles upgraded with intros + next steps |
| 3c: Main Branch Content Sync (runs twice) | Human + Agent | Sync #1: ~1 day; sync #2: pre-merge | Synced new/updated articles; numeric-ID parity (frontmatter stamp + manifest map) |
| 4: Consolidation & Retirement | Human + Agent | 1 week | Merged/retired articles, merge decision log |
| 5: Interlinking | Agent (batch) | 2–3 days | Next Steps + Related Articles on all articles |
| 6: Rename to Slugs | Script + human review | 1–2 days | Renamed files, `rename-mapping.json`, `redirects.json` |
| 7: Nav Rebuild | Agent + Human | 2–3 days | New `docs.json`, validation passing |

**Total estimate:** 6–8 weeks for full execution. Phases 3a (content creation) and 3b/5 (bulk agent edits) can run in parallel after Phase 1 completes. Phase 6 (rename) should run after Phase 3a to avoid renaming files that are being actively written.

---

## Key Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Broken internal links after rename | Link-updater script (rewrites `pages`, `root`, and `scripts/group_roots.json`) + post-rename nav validation |
| Group roots dropped by the OpenAPI sync | Re-add the root and overview page after each Product APIs spec sync; the nav validator flags a rooted group that lost its root file |
| Existing SEO / bookmarks broken by rename | Redirects map generated before rename executes; maintained in Mintlify config |
| Connector articles too numerous to individually maintain | Templated structure; consider a connector article generator script for new connectors |
| Net-new articles don't match style guide | All new articles authored via `new-kb-article` or `new-overview-article` skill (encodes style guide automatically) + human review before merge |
| Merges accidentally lose unique content | Merge agents diff source articles first; human reviews all merge decisions |
| Sub-agents can't Write new files | Net-new articles authored in main session; agents only use Edit on existing files |
| Workbench legacy content removed too aggressively | Legacy articles archived (not deleted) in a collapsible nav group; removals are additive nav moves, not file deletions |
| Phase 2 IA design assumptions wrong | Run Phase 1 audit first; IA design is informed by actual content distribution, not assumptions |
