# KB Restructure Progress Tracker

This file is the canonical source of truth for where we are in the KB restructure.
Update it at the end of every work session. Future Claude sessions should read this
file at the start of any restructure work to orient themselves before doing anything.

**Plan document:** `KB-RESTRUCTURE-PLAN.md`
**Last updated:** 2026-07-14

---

## Current Status

**Active phase:** Phase 3a — Net-New Articles (synthesizable)
**Blocked on:** 8 human decisions (see Phase 2 Decision Required table in `RESTRUCTURE-IA-SPEC.md`)
**Phase 1/2 re-run:** Complete 2026-07-14 on branch `update/fullRestructure`

---

## Phase Completion

| Phase | Status | Notes |
|-------|--------|-------|
| **1: Audit & Inventory** | ✅ Complete (re-run 2026-07-14) | 1,832 articles; 2 orphaned; 842 merge candidates (23 exact); see updated findings below |
| **2: IA Design** | ✅ Complete (re-run 2026-07-14) | 11 pillars in `docs.json` KB tab; 1,832 articles assigned; see Phase 2 outputs below |
| **3a: Net-New Articles (~26)** | 🔲 Not started | Synthesizable from existing content; see article list below |
| **3a-PM: PM Input Articles (4)** | 🔲 Blocked — awaiting PM | See PM Input section below |
| **3a-Forum: Forum-Driven New Articles (~57)** | 🔲 Not started | Community forum gaps; see Forum Gap Analysis section below |
| **3b: Article Upgrades (~200)** | 🔲 Not started | Bulk agent edit pass |
| **3b-Forum: Forum-Driven Article Updates (Critical+High, ~68)** | 🔲 Not started | Priority targets for Phase 3b bulk agent pass |
| **4: Consolidation, Retirement & Archive** | 🔲 Not started | Duplicates, true archival, legacy marking; see Archive/Legacy Standards below |
| **4.5: PM Review System** | 🔧 Built — run after Phase 4 | Script ready: `scripts/build-pm-review-briefs.py`; generates per-PM task checklists + meeting briefs |
| **5: Interlinking** | 🔲 Not started | Next Steps + Related Articles bulk pass — runs after PM sign-off |
| **6: Slug Rename + Redirects + Localization** | 🔲 Not started | Enhanced: CSV map, localized file rename, docs.json redirects, internal link updates |
| **7: Nav Rebuild** | 🔲 Not started | Rebuild docs.json nav groups after Phase 6 slug changes |
| **8: Style Guide & Template Update** | 🔲 Not started | Update `Domo-KB-Style-Guide.mdx` + `New-Article-Template.mdx` for new standards |
| **9: Restructure Artifacts Cleanup** | 🔲 Not started | Move all planning/analysis artifacts to `restructure/` folder |

---

## Phase 1 Outputs (Complete — re-run 2026-07-14)

All files are in `scripts/output/` (gitignored; must re-run scripts before Phase 3):

| File | Description | Key stats |
|------|-------------|-----------|
| `catalog.json` | Master article inventory | 1,832 articles; 2 missing excerpt |
| `catalog-classified.json` | Inventory + Diátaxis type per article | See distribution below |
| `orphans.json` | Articles not appearing in docs.json nav | 2 articles |
| `merge-candidates.json` | Near-duplicate title pairs (Jaccard ≥ 0.55) | 842 pairs; 23 exact (1.00) |
| `gap-analysis.json` | Missing tutorial/explanation coverage per pillar | 6 of 10 pillars missing tutorials |

### Classification Distribution

| Type | Count | Notes |
|------|-------|-------|
| connector | 977 | ~53% of all content |
| howto | 570 | ~31% — the main article bulk |
| explanation | 71 | conceptual/overview articles |
| reference | 69 | properties tables, function lists, etc. |
| release-notes | 65 | current + archived |
| retire-candidate | 62 | legacy/deprecated content |
| tutorial | 18 | severely underweight — target: 30+ |

### Key Phase 1 Findings

**Orphaned articles (2):**
- `000005849.mdx` — "Use FileSets to Gather Information from Unstructured Data"
- `Access-Tokens.mdx` — "Access Tokens" (Beta feature — add to nav when feature ships)

**Duplicate connectors (22 exact-title pairs — Phase 4 merge targets):**
- Pattern A: Same title, same nav group, different line counts → stub coexists with full article; keep longer, retire shorter
- Pattern B: Same title, different nav groups → nav placement error; one copy in wrong section
- Notable examples: Amazon S3 (43 vs 121 lines), PostgreSQL (41 vs 185 lines), Adaptive Insights (63 vs 642 lines)

**Gap analysis — pillars missing tutorials (highest priority for Phase 3a):**
- **Connect & Bring In Data** — 1,057 articles, 0 tutorials (largest gap)
- **Prepare & Transform Data** — 75 articles, 0 tutorials (was 109; 34 articles reclassified to Manage Data + other pillars via D9)
- **Manage Data** — 20 articles, 0 tutorials (new pillar, populated by D9 resolution)
- **Administer & Govern** — 73 articles, 0 tutorials
- **Share & Collaborate** — 51 articles, 0 tutorials
- **Develop & Integrate** — 7 articles, 0 tutorials, 0 explanations (still underdocumented; gained CLI + ODBC from D9)
- **Other** — 64 articles, 0 tutorials (catch-all bucket needing categorization)

---

## Phase 2 — Complete (re-run 2026-07-14; D9 resolved 2026-07-14)

All 1,832 articles assigned to 11 pillars + Archive. Full spec in `RESTRUCTURE-IA-SPEC.md`.

**Note:** Phase 2 will be re-run after Phase 1 completes on this branch. See "Phase 2 Redo Approach" below.

**Outputs (re-run 2026-07-14):**
- `scripts/output/ia-spec.json` — every article → `{pillar, group, sub_group}`
- `scripts/output/ia-mapping.json` — article filename → `{pillar, group, sub_group}`
- `docs.json` — KB tab rebuilt with 11 pillar groups (1,832 page refs; up from 1,772)
- `scripts/build_docs_nav.py` — new script; reads `ia-mapping.json` + `catalog.json`, rebuilds KB tab in-place; preserves Developer Portal, Release Notes, and all localized tabs
- `RESTRUCTURE-IA-SPEC.md` — human-readable nav spec with full hierarchy, new articles to write, and 8 open decisions

**Nav structure:** 11 pillars as top-level groups inside the single **Knowledge Base** tab. Each pillar contains its groups as nested sub-groups. Archive appended last. `s/topic/` files excluded (not relevant to restructure). Developer Portal and Release Notes tabs, and all localized tabs (ja/fr/de/es), untouched.

**Article count:** 1,832 in `s/article/` (up from 1,819 at original Phase 1 — 13 new articles added since).

---

## Archive / Legacy Standards

These standards apply throughout Phases 3–4 and must be reflected in Phase 8 (Style Guide update).

### Three categories of "removal"

| Category | What it means | File fate | Nav fate | YAML | Visual indicator |
|----------|--------------|-----------|----------|------|-----------------|
| **Deleted** | Article is restructured into other content — its info lives elsewhere (merged, rewritten, split) | File deleted | Removed from nav | — | — |
| **Archived** | Content is genuinely retired: feature removed, content truly unnecessary AND its info is not used elsewhere, PM or Audit confirmed | File kept | Moved to "Archive" group at bottom of KB tab | `archived: true` | `<ArchivedNote />` callout at top of article |
| **Legacy** | Feature still exists and is functional but is no longer actively maintained; superseded by a newer approach | File kept | Stays in its pillar group with `(Legacy)` sidebar tag | `legacy: true`, `tag: "Legacy"` | `<LegacyNote />` callout at top of article |

**Key rule:** If an article's content is used elsewhere in any form — merged into another article, its information rewritten into a new article — the original file is **deleted**, not archived. Archive is reserved for content with no living successor.

### YAML frontmatter spec

**Archived article:**
```yaml
---
title: "Article Title"
archived: true
tag: "Archived"
---
```

**Legacy article:**
```yaml
---
title: "Article Title"
legacy: true
tag: "Legacy"
---
```

The `tag` field is a native Mintlify frontmatter property that renders a visible label next to the article title in the sidebar. The `archived` and `legacy` fields are custom metadata used by restructure tooling (PM review script, task tracker).

### Snippets to create at Phase 4 execution time

- `snippets/LegacyNote.mdx` — renders a `<Warning>` callout: "**Legacy:** This article describes a feature that is no longer actively maintained. It remains functional but may not reflect current best practices. For the current approach, see [replacement link]."
- `snippets/ArchivedNote.mdx` — renders a `<Warning>` callout: "**Archived:** This content has been retired and may no longer reflect current product behavior. It is preserved for historical reference only."

Both follow the existing `snippets/BetaNote.mdx` pattern (import at top of MDX, use as `<LegacyNote />` or `<ArchivedNote />`).

### Determining archive vs legacy — PM confirmation required

Legacy marking requires PM sign-off. During Phase 4 and Phase 4.5, articles in a PM's area that are candidates for Legacy designation will appear in their PM review brief as a decision item. PM must confirm:
- Feature still exists in Domo
- Feature is not being actively developed/maintained
- The feature has a recommended successor (which the LegacyNote should link to)

The PM review brief script (`scripts/build-pm-review-briefs.py`) should be updated before Phase 4.5 to include a "Legacy Candidates" section per PM, surfacing articles from the Support KB Audit that were flagged as potential legacy but not yet confirmed.

**7 decisions need human sign-off before Phase 7 (nav rebuild):**
| # | Decision |
|---|----------|
| D1 | Workbench 4 articles (37) — Archive or keep? |
| D2 | Projects & Tasks (10) — still active feature or archive? |
| D3 | Premium Apps (65) — audit currency before upgrading |
| D4 | "Build Your First Dashboard" — move from Getting Started to Analyze & Visualize? |
| D5 | "Introduction to Domo" (000005874) — keep alongside new "What is Domo?" or retire? |
| D6 | Develop & Integrate scope — KB how-tos vs. link-out to developer.domo.com? |
| D7 | Data Models (1 article, Beta) — expand or hold until feature ships? |
| D8 | Instance Settings (39) — sub-group further or keep flat? |
| ~~D9~~ | ~~DataSet Management split~~ — **Resolved 2026-07-14.** 20 governance/lifecycle articles → Manage Data (3 Data Center, 17 DataSet Lifecycle). 5 pipeline articles stay in Prepare & Transform. PDP → Administer & Govern. Domo CLI + ODBC → Develop & Integrate. Analyzer/Chart articles → Analyze & Visualize. See decision log. |

These decisions don't block Phase 3a article writing — they only block the nav rebuild in Phase 7.

---

## Phase 4.5 — PM Review System

**Status:** Built — run after Phase 4 is complete, before Phase 5 begins
**Script:** `scripts/build-pm-review-briefs.py`
**Output:** `pm-review-briefs/<PM-Name>.md` + `RESTRUCTURE-TASKS.md` — generated on demand

Phase 4.5 is the human sign-off gate. All content work (Phases 3a–4) is complete before this runs. PMs review every change made to their product area and either sign off, provide fact-check corrections, or schedule follow-up meetings for remaining information gaps. No interlinking, renaming, or nav rebuild happens until this phase is complete.

### What the system generates

Run the script after Phase 4 to produce two outputs:

**1. Per-PM meeting brief** (`pm-review-briefs/<PM-Name>.md`) — one file per PM covering:
- Content reorganization: every feature → new pillar assignment + article count + structural nav changes
- All Phase 3a/3a-Forum/3b/3b-Forum changes in their area (new articles written, articles updated) with fact-check prompts
- All Phase 4 archival and legacy marking actions in their area requiring sign-off
- Pending items: PM-input articles still needing information, outstanding D1–D10 decisions
- Legacy candidates: articles flagged as potential legacy needing PM yes/no confirmation
- Support gap integration summary: Audit retirements + forum update targets executed in their area

**2. Granular task checklist** (`RESTRUCTURE-TASKS.md`) — the working checklist for post-PM-review execution, organized:
```
Pillar → Product Group → [ ] Individual task
```
Each task is one discrete change with a type tag:
- `[new-article]` — new article written; needs fact-check
- `[update]` — existing article updated; needs PM review if significant
- `[archive]` — article archived; needs PM sign-off
- `[legacy]` — article marked legacy; needs PM confirmation
- `[deleted]` — article deleted (content moved elsewhere); PM awareness only
- `[pm-input]` — article pending PM information before it can be written
- `[decision]` — open D1–D10 architectural decision needing resolution
- `[fact-check]` — specific claim in a written article needs PM verification

Example checklist entries:
```markdown
## Pillar 4: Prepare & Transform Data
### Magic ETL (Andrea Henderson)
- [ ] [fact-check] `What-is-Magic-ETL.mdx` — verify: capabilities, 400k preview limit, vs SQL DataFlows
- [ ] [new-article] `Beast-Mode-Window-Functions.mdx` — verify: window function behavior, filter limitation still accurate?
- [ ] [update] Magic ETL troubleshooting: editor-level failures added — verify: error messages current?
- [ ] [archive] Old Magic ETL tile articles (15) — sign-off required
- [ ] [pm-input] `Choosing-the-Right-Data-Prep-Tool.mdx` — need: ETL vs DataFlow vs SQL positioning
- [ ] [legacy] DataFusion articles (11) — confirm: DataFusion fully replaced by Magic ETL?
```

This checklist is the working document for PM meetings. Query it at any time: "what's left for Connectors?", "how many tasks remain for Phil Fuchs?", etc.

### When to run

```bash
# After Phase 4 is complete:
python3 scripts/build-pm-review-briefs.py
# Also generates RESTRUCTURE-TASKS.md (update script before running to reflect completed work)
```

Before running, update the script's hardcoded phase data to reflect what was actually completed vs. planned in Phases 3–4. The brief and task list should show real completed changes, not plans.

### PM roster

| PM | Features | GitHub Login | Status |
|----|----------|-------------|--------|
| Andrea Henderson | Auto ML, Data Flows, Magic ETL | @ahenderson-domo | ✅ Confirmed |
| Beth Saenz | Accessibility | — | Unconfirmed |
| Chris Wright | Analyzer, Charting, Doc Cards, Export to CSV, Mobile - iOS, Slideshows, Worksheets | — | Unconfirmed |
| Dan Brinton | Admin, Alerts/NLG/Smart Alerts, ABAC, Buzz, Consumption, DomoStats, Goals, Profile, SSO | @OriginalDanB | ✅ Confirmed |
| Jordan Jensen | AppStore, Cloud Amplifier, DataSets, Education, Federated, Onboarding | @mnwhitepine | ✅ Confirmed |
| Ken Boyer | AI Services, CLI, Documents-Filesets, Jupyter Notebooks | @bikene1 | ✅ Confirmed |
| Khushboo | App Dev Framework, App Studio, Bricks/Templates, MS Office Plugins/Addins, Publication Groups | — | Unconfirmed |
| Mamta Bolaki | Domo Everywhere, Sandbox | @mamtabolaki-gif | ✅ Confirmed |
| Mark Adams | Freemium | — | Unconfirmed |
| Phil Fuchs | Beast Mode, Combined Schema, Data Center, Data Views, Fusions, Period over Period | @phil-fuchs-domo | ✅ Confirmed |
| Ryan Despain | Approvals, Governance Toolkit, Projects & Tasks, Workflows | @RyanDespain | ✅ Confirmed |
| Tasleema Lallmamode | Connectors 1.0, Third Party Connectors, Workbench | — | Unconfirmed |

*GitHub logins source: `.github/CODEOWNERS`*

---

## Phase 3a — Next Steps (Start Here Next Session)

Write the ~26 new articles that can be synthesized from existing KB content. All require the `new-kb-article` or `new-overview-article` skill. Net-new files must be written in the **main session** (sub-agents cannot Write new files).

**Priority order for Phase 3a:**

| Priority | Filename | Synthesize from | Skill |
|----------|---------|-----------------|-------|
| 1 | `s/article/What-is-Domo.mdx` | 000005874 + role guides | `new-overview-article` |
| 2 | `s/article/Getting-Started-for-Admins.mdx` | Admin how-tos | `new-kb-article` |
| 3 | `s/article/Getting-Started-for-App-Builders.mdx` | App Studio/Workflows overview | `new-kb-article` |
| 4 | `s/article/Getting-Started-for-Developers.mdx` | API articles, Access Tokens | `new-kb-article` |
| 5 | `s/article/What-is-a-DataSet.mdx` | Connector + ETL articles | `new-overview-article` |
| 6 | `s/article/What-is-Magic-ETL.mdx` | Magic ETL overview articles | `new-overview-article` |
| 7 | `s/article/What-is-a-DataFlow.mdx` | DataFlow articles | `new-overview-article` |
| 8 | `s/article/Prepare-and-Transform-Overview.mdx` | All ETL/DataFlow articles | `new-overview-article` |
| 9 | `s/article/What-is-a-Card.mdx` | Analyzer articles | `new-overview-article` |
| 10 | `s/article/What-is-a-Dashboard.mdx` | Dashboard articles | `new-overview-article` |
| 11 | `s/article/What-is-Beast-Mode.mdx` | Beast Mode FAQ + functions ref | `new-overview-article` |
| 12 | `s/article/Analyze-and-Visualize-Overview.mdx` | All analyzer/chart articles | `new-overview-article` |
| 13 | `s/article/What-is-an-Alert.mdx` | Alerts Overview + alert articles | `new-overview-article` |
| 14 | `s/article/What-is-a-Connector.mdx` | General Connector Info (12 articles) | `new-overview-article` |
| 15 | `s/article/Connect-and-Bring-In-Data-Overview.mdx` | All connector articles; frames read + write | `new-overview-article` |
| 16 | `s/article/Manage-Data-Overview.mdx` | DataSet articles, Data Center context | `new-overview-article` |
| 17 | `s/article/What-is-the-Data-Center.mdx` | DataSet management articles | `new-overview-article` |
| 18 | `s/article/Find-and-Manage-Your-DataSets.mdx` | DataSet management, sharing, workspace articles | `new-kb-article` |
| 19 | `s/article/What-is-Domo-AI.mdx` | Domo AI FAQ + AI articles | `new-overview-article` |
| 20 | `s/article/AI-and-Data-Science-Overview.mdx` | All AI/DomoStats/Jupyter articles | `new-overview-article` |
| 21 | `s/article/What-is-App-Studio.mdx` | App Studio Overview | `new-overview-article` |
| 22 | `s/article/Build-Apps-and-Automate-Overview.mdx` | App Studio/Workflows/Code Engine | `new-overview-article` |
| 23 | `s/article/What-is-Workbench.mdx` | Workbench 5.2 overview | `new-overview-article` |
| 24 | `s/article/Share-and-Collaborate-Overview.mdx` | Sharing/Buzz/Publications articles | `new-overview-article` |
| 25 | `s/article/Domo-User-Roles.mdx` | Roles/grants articles | `new-overview-article` |
| 26 | `s/article/Security-and-Permissions-Overview.mdx` | PDP, OAuth, security articles | `new-overview-article` |
| 27 | `s/article/Administer-and-Govern-Overview.mdx` | All admin articles | `new-overview-article` |
| 28 | `s/article/Domo-Sandbox-Overview.mdx` | Sandbox article | `new-overview-article` |
| 29 | `s/article/Develop-and-Integrate-Overview.mdx` | Existing 5 API articles | `new-overview-article` |

**Scope note:** All Phase 3a articles go in `s/article/`. The `portal/` directory is entirely out of scope for this restructure — it is Developer Portal content with its own structure and audience. The only portal/ work in this restructure is Phase 5 interlinking, which adds links *from* `s/article/` how-tos *to* existing `portal/` reference pages (no new portal/ files, no portal/ nav changes).

---

## PM Input Required (Blocking Phase 3a-PM)

These 4 articles cannot be written without PM input. Track separately from main Phase 3a work.

| Article | What PM needs to provide | Status |
|---------|--------------------------|--------|
| `How-Data-Flows-Through-Domo.mdx` | Canonical end-to-end pipeline narrative; sign off on how connect → prepare → analyze → share → govern is described | ⏳ Not requested |
| `Choosing-the-Right-Data-Prep-Tool.mdx` | Positioning: when to use Magic ETL vs SQL DataFlow vs Python/R vs Data Models | ⏳ Not requested |
| `Understanding-DataSet-Joins-and-Relationships.mdx` | Decision guidance: when to use ETL joins vs Data Models vs DataFlows | ⏳ Not requested |
| `Domo-for-Mobile-Overview.mdx` | Confirm current mobile feature scope before writing overview | ⏳ Not requested |

---

## Community Forum Gap Analysis — Phase 3a/3b Input

**Source:** `_gaps_with_support.json` (repo root)
**What it is:** 5,452 community forum records (1,756 threads, 2019–2026) analyzed to identify topics underdocumented or entirely missing in the KB. Topics already well-covered were excluded before scoring. All 361 gaps were validated against actual repo content.
**Totals:** 361 gaps — 12 Critical, 98 High, 192 Medium, 59 Low — scored by demand + impact + recency.
**Recommendations:** 57 net-new articles (`rec=new`); 304 updates to existing articles (`rec=update`).

This is a different dataset from the Support KB Audit already integrated below. The Audit identifies accuracy problems in existing content; the forum analysis identifies knowledge gaps where users cannot find what they need. They are complementary.

**How this integrates into the restructure:**
- Critical/High `rec=new` gaps → **Phase 3a-Forum**: additional net-new articles to write
- Critical `rec=update` and High `rec=update` gaps → **Phase 3b-Forum**: priority targets for the article upgrade agent pass
- Medium/Low gaps → Phase 3b bulk agent pass input; reference `_gaps_with_support.json` directly for the full scored list

**Already addressed — do not duplicate:**

| Gap | How already handled |
|-----|---------------------|
| Gap #116 — Snowflake username/password auth retirement (Medium, update) | Covered by "Urgent pre-Phase 4 fix" in Phase 4 section below |
| Gap #198 — DataFusion removed, replacement guidance (Medium, update) | DataFusion articles are being archived (Phase 4), but the forum analysis surfaces a need for a migration note pointing users to Magic ETL replacements. **Add a brief `DataFusion-Migration-Guide.mdx` alongside Phase 4 archival.** |
| General "no conceptual context" failures | Phase 3a structural articles (`What-is-X.mdx`, hub articles) address the broad framing gap; the forum gaps go deeper into specific technical questions the structural articles won't cover |

---

### Critical Gaps (12 total)

Address Critical `rec=update` items during Phase 3b alongside or immediately after Phase 3a structural articles. Critical `rec=new` items are in the Phase 3a-Forum article list below.

| Rank | Score | Area | Topic | Rec | Phase 3 action |
|------|-------|------|-------|-----|----------------|
| 1 | 93.0 | Beast Mode | Window functions (RANK, LAG, running totals, Top N) and the filter limitation | **new** | `Beast-Mode-Window-Functions.mdx` — example-driven reference; RANK/DENSE_RANK, LAG/LEAD, SUM(SUM(x)) OVER, Top N + Others, "can't filter by window function" workarounds |
| 2 | 83.8 | Magic ETL | Editor UI failures: save failures, validate error, blank-canvas bug | update | Update Magic ETL troubleshooting article — add editor-level failure diagnostics separate from execution failures |
| 3 | 82.4 | Magic ETL | Preview vs run discrepancies; "Not Runnable"; silent multi-output non-updates | update | Update Magic ETL troubleshooting article — add "Preview vs Run" FAQ with known causes |
| 4 | 79.6 | App Studio | Managing cards in App Studio: Move/Copy menu, delete app + cards, orphan recovery | update | Update App Studio card management article — add orphan card recovery, delete-app-with-cards warning |
| 5 | 79.0 | Beast Mode | Date comparisons and cumulative Beast Modes (YTD/MTD/MoM/YoY/WoW, rolling N months) | update | Update Beast Mode date functions article — add YTD/MTD/rolling patterns section with worked examples |
| 6 | 78.3 | Workflows | Writing data back to datasets (Append / Multiline Append, dynamic rows, AppDB) | **new** | `Workflows-Write-Data-Back.mdx` — Append, Multiline Append, AppDB write from Workflows |
| 7 | 78.1 | Admin / Governance | Activity Log action/event definitions (VIEWED, EXPORTED, DOWNLOADED, etc.) | **new** | `Activity-Log-Event-Reference.mdx` — enumerated glossary of all event types; DomoStats mapping |
| 8 | 77.5 | Magic ETL | Preview row limit (~400k); limited preview/testing visibility | update | Update Magic ETL preview article — document 400k row limit explicitly; add run-to-here workaround |
| 9 | 76.2 | Dashboards | Restoring a deleted dashboard/page | **new** | `Restore-a-Deleted-Dashboard.mdx` — FAQ: no self-service restore; contact support path; prevention |
| 10 | 76.1 | Beast Mode | Mixing aggregated and non-aggregated columns (grouping errors, subtotals) | update | Update Beast Mode reference article — add aggregation context section; SUM(SUM(x)) pattern |
| 11 | 75.8 | Beast Mode | Replicating Excel/Google Sheets logic in Beast Mode (IF→CASE, SUMIF→SUM(CASE), etc.) | **new** | `Beast-Mode-for-Spreadsheet-Users.mdx` — translation guide from spreadsheet formulas to Beast Mode |
| 12 | 75.4 | Workflows | Building forms, tasks, queues, and the Task Center (native review/approval flows) | update | Update Workflows forms/tasks article — add Task Center setup, queue config, approval flow patterns |

---

### Phase 3a-Forum: Net-New Articles (Critical + High Priority)

42 articles with no KB coverage, ranked Critical or High. Write in the main session using `new-kb-article` or `new-overview-article` skill. For full gap detail (affected articles, suggested location, forum + support signal), look up by rank in `_gaps_with_support.json`.

#### Critical new (5 articles)

| Rank | Suggested filename | Topic summary |
|------|--------------------|---------------|
| 1 | `Beast-Mode-Window-Functions.mdx` | RANK/DENSE_RANK, LAG/LEAD, SUM(SUM(x)) OVER running totals, Top N + Others; "can't filter by window function" limitation and workarounds |
| 6 | `Workflows-Write-Data-Back.mdx` | Append / Multiline Append / AppDB write from Workflows; dynamic row handling |
| 7 | `Activity-Log-Event-Reference.mdx` | All Activity Log event types defined; VIEWED vs EXPORTED vs DOWNLOADED; DomoStats field mapping |
| 9 | `Restore-a-Deleted-Dashboard.mdx` | No self-service restore; contact support path; prevention via snapshot/copy |
| 11 | `Beast-Mode-for-Spreadsheet-Users.mdx` | IF→CASE, SUMIF→SUM(CASE), VLOOKUP→ETL join; no stacked IF, no volatile functions |

#### High new (37 articles)

| Rank | Suggested filename | Topic summary |
|------|--------------------|---------------|
| 13 | `Workflows-Package-Administration.mdx` | Domo Users / DataSet package functions: assign roles, manage owners, set attributes via Workflows |
| 14 | `Dataset-Column-Rename-Impact.mdx` | Renaming a dataset/dataflow column silently breaks card filters, sorts, and downstream references — safe rename procedure |
| 17 | `Embed-Domo-in-Third-Party-Platforms.mdx` | Confluence, NetSuite, HubSpot, SharePoint, Salesforce embed methods and iframe constraints |
| 21 | `Filter-Funnel-and-PDP-Shield-Icons.mdx` | Hiding/showing the filter funnel and PDP shield on cards; page-variable behavior; Admin setting |
| 22 | `Filtering-on-Null-and-Empty-Values.mdx` | NULL vs empty string; IS NULL / IS NOT NULL filter; NOT IN behavior; Beast Mode IFNULL workarounds |
| 25 | `Card-Refresh-Timing-After-Dataset-Update.mdx` | How long cards take to reflect dataset changes; cache warm-up; force-refresh approach |
| 26 | `DomoStats-vs-Governance-Datasets-Connector.mdx` | When to use DomoStats connector vs Domo Governance Datasets connector; field-level reference; deprecation status |
| 27 | `Trigger-Workbench-from-External-Scripts.mdx` | `wb.exe` CLI command syntax; triggering a Workbench job from Task Scheduler or CI scripts |
| 28 | `Embedded-Dashboard-Unfiltered-Data-Flash.mdx` | Why embedded/public-share dashboards briefly show unfiltered data on load; SSO and PDP timing fix |
| 32 | `Connecting-Unsupported-Data-Sources.mdx` | No native connector options: JSON No Code, HTTP connector, SFTP, Workbench ODBC, custom connector builder |
| 33 | `Zero-Fill-Missing-Date-Gaps-in-Charts.mdx` | Date densification in Magic ETL; zero-filling time series; empty pivot rows; calendar join pattern |
| 44 | `Dataset-Archived-Lifecycle-State.mdx` | What the "archived/not accessed" state means; how it blocks AI Readiness lineage; how to reactivate |
| 47 | `Troubleshoot-Cards-Not-Updating.mdx` | Cards showing stale data after dataset refresh; color rules not applying; cache and permission causes |
| 49 | `Period-over-Period-Calculations.mdx` | Prev week / prev month / prior year / year-boundary calculations in Beast Mode and Magic ETL; worked examples |
| 50 | `Write-Data-from-Pro-Code-Apps-to-AppDB.mdx` | Writing back to AppDB collections from DDX Bricks / Pro-Code apps; sync to dataset; schema requirements |
| 55 | `Incremental-Ingestion-and-Lastvalue.mdx` | `lastvalue` parameter default, behavior, and edge cases; late-arriving and deleted source record handling |
| 56 | `Dataset-Column-Character-Limits.mdx` | ~1,024 char text column limit; truncation of base64 images, JSON payloads, LLM output; workarounds |
| 57 | `Pivot-Table-Census-Calendar-Join.mdx` | Date-range / calendar join pattern for length-of-visit / census modeling |
| 61 | `Plot-Two-Date-Columns-on-One-Axis.mdx` | Data reshaping in Magic ETL to plot two date columns on a shared time axis |
| 62 | `Data-Allocation-Split-Credit-in-ETL.mdx` | Reproducing proportional allocation / split-credit mapping in Magic ETL |
| 64 | `Request-Access-Behavior.mdx` | How "Request Access" and "Request More Access" buttons work; who receives the request; admin configuration |
| 66 | `Troubleshoot-Office-PowerPoint-Add-In.mdx` | Connection failures, authentication errors, stale refresh; installation prerequisites |
| 69 | `Dashboard-Editor-Unresponsive-Multi-Select-Filter.mdx` | Dashboard editor hangs caused by misconfigured multi-select filter card; diagnosis and fix |
| 71 | `Drill-to-Final-Data-Security.mdx` | What "Drill to Final Data" exposes; detecting it is enabled; securing the master dataset |
| 77 | `Time-Interval-Bucketing-and-Dedup.mdx` | Assigning records to time buckets; deduplication within a window; Beast Mode vs Magic ETL approach |
| 81 | `Schedule-Enterprise-Dataset-Copy.mdx` | Configuring a specific run time for Enterprise Dataset Copy jobs (not just "run now") |
| 82 | `Manage-Dataset-Error-Alerts.mdx` | Turning off / bulk-removing "Error Loading Data" alerts after archiving or deleting datasets |
| 83 | `Host-Images-for-Domo-Apps.mdx` | data-files URL pattern for storing and referencing internal images in Domo Apps and ETL |
| 84 | `GA4-BigQuery-Daily-Table-Nested-Data.mdx` | GA4 connector daily-table sprawl; unnesting `event_params`; BigQuery date-partitioned table approach |
| 86 | `Find-Domo-Version-and-Tool-Versions.mdx` | Where to find the Domo instance build number; Workbench version; plugin/add-in version |
| 89 | `Retrieve-Dataset-Source-Query-via-API.mdx` | API call to get the underlying connection/query for a dataset; connector metadata endpoints |
| 91 | `Remove-Bad-Rows-from-a-Dataset.mdx` | CLI full-replace artifact cleanup; removing a single erroneous row; append-mode dataset corrections |
| 99 | `Domo-API-Changelog.mdx` | No published changelog for Domo APIs; versioning policy; how to track changes (DomoStats, release notes) |
| 100 | `App-Studio-Performance-with-Large-Datasets.mdx` | Load time causes; dataset size thresholds; optimization patterns (pre-aggregation, DataSet Views) |
| 103 | `ETL-Credits-and-Consumption-Model.mdx` | Legacy ETL vs consumption credits; what counts as a "manual run" vs "significant change"; billing implications |
| 107 | `Multi-Language-Dashboards.mdx` | Dynamic language switching on dashboards; localization patterns; Beast Mode locale functions |
| 109 | `Custom-Card-Visuals-with-HTML-and-Bricks.mdx` | HTML card techniques; DDX Brick custom visuals; profile pictures, ERP-style detail panels |

---

### Phase 3b-Forum: Priority Update Targets (Critical + High `rec=update`)

68 gaps where existing articles need material additions. These are priority inputs for the Phase 3b bulk article upgrade agent pass. Full detail (affected article paths, specific gap description, suggested additions) is in `_gaps_with_support.json` — look up by rank.

**Critical update targets (7 — address alongside or immediately after Phase 3a structural articles):**

| Rank | Affected article area | Specific addition needed |
|------|-----------------------|--------------------------|
| 2 | Magic ETL troubleshooting | Editor-level failure diagnostics (save failures, validate error, blank canvas) |
| 3 | Magic ETL troubleshooting | "Preview vs Run" discrepancy FAQ section; "Not Runnable" error causes |
| 4 | App Studio card management | Orphan card recovery; delete-app-with-cards warning and procedure |
| 5 | Beast Mode date functions | YTD/MTD/rolling N months patterns with worked examples |
| 8 | Magic ETL preview documentation | Explicit 400k row limit; run-to-here and sample tile workarounds |
| 10 | Beast Mode reference | Aggregation context; grouping requirement; SUM(SUM(x)) pattern for subtotals |
| 12 | Workflows forms/tasks | Task Center setup; queue configuration; native approval flow patterns |

**High update targets (61) — ranked list for Phase 3b agent pass:**

Full rank list: 15, 16, 18, 19, 20, 23, 24, 29, 30, 31, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 48, 51, 52, 53, 54, 58, 59, 60, 63, 65, 67, 68, 70, 72, 73, 74, 75, 76, 78, 79, 80, 85, 87, 88, 90, 92, 93, 94, 95, 96, 97, 98, 101, 102, 104, 105, 106, 108, 110

Grouped by product area for batching the Phase 3b agent pass:

| Area | Ranks |
|------|-------|
| Magic ETL (join behavior, errors, output, validation, date functions, group-by) | 20, 23, 24, 35, 36, 39, 51, 52, 101, 106 |
| Beast Mode (FIXED, CASE/COUNT, aggregation, AVG, variables, formatting, dates) | 29, 30, 34, 38, 52, 67, 68, 73, 78, 80, 87, 88 |
| App Studio (mobile layout, Report Builder, forms, filters, editor, tabs, sharing) | 40, 43, 46, 53, 54, 58, 63, 65, 72, 76, 94, 97, 98, 110 |
| Charting & Analyzer (PoP, null filter, date axis, color rules, pivot, tables) | 16, 60, 68, 74, 85, 93 |
| Governance & Security (PDP, DomoStats, activity log, roles, sandbox, CDW) | 18, 19, 36, 45, 79, 90, 95, 96 |
| Workflows (triggers, App Studio write-back, notifications, AI agents) | 42, 43, 48, 65, 92 |
| Dashboards (filters, drill paths, export, scheduling, smart text) | 70, 75 |
| Connectors (auth, ingestion behavior, error messages, incremental, CDW) | 36, 37, 41, 102, 105, 108 |
| APIs / Developer (AppDB sync, PDP embed, token types, onDataUpdate) | 96, 98 |

---

### Medium/Low Gaps (266 total)

Medium gaps include 15 `rec=new` and 192 `rec=update`. Low gaps are all 59 `rec=update`. These are Phase 3b general bulk-pass inputs. The full scored list with suggested locations and related articles is in `_gaps_with_support.json`.

**Medium new articles (15)** — add to Phase 3a-Forum backlog after Critical + High new articles are complete:

| Rank | Suggested filename | Topic summary |
|------|--------------------|---------------|
| 114 | `Dynamic-Dropdowns-in-Table-Cards.mdx` | In-cell dropdown controls and write-back in Analyzer table cards |
| 117 | `Split-Multi-Value-Fields-into-Rows.mdx` | Comma-separated / multi-value field expansion in Magic ETL |
| 118 | `Editor-Dataset-Access-Scope.mdx` | What datasets Editors can see: cards/dashboards shared vs direct dataset sharing |
| 127 | `Alert-on-Stuck-Dataset-Refresh.mdx` | Alerting when a dataset stops refreshing; DomoStats refresh frequency monitoring |
| 139 | `Choosing-How-to-Share-Outside-Domo.mdx` | Decision guide: embed types vs publication groups vs Domo Everywhere vs scheduled reports |
| 142 | `Choosing-a-Cloud-Data-Warehouse.mdx` | CDW comparison for Domo; Cloud Amplifier cost/credit consumption guide |
| 144 | `AI-Chat-API-Session-ID.mdx` | Ask Chat / AI API requires a Domo-generated session ID — how to obtain and use it |
| 146 | `Domo-Certification-Exam-Logistics.mdx` | Domo Professional Certification: registration, exam format, retake policy |
| 152 | `Find-Which-Dashboard-a-Card-Lives-On.mdx` | Card-to-page/app lineage via Governance Toolkit / DomoStats |
| 159 | `Extract-Data-from-PDFs-with-Domo-AI.mdx` | Image-to-Text / PDF table extraction with Domo AI |
| 161 | `Private-Embed-Token-Validation-Errors.mdx` | Private Embed token validation failures; redirect-to-login causes and fixes |
| 172 | `Export-Domo-Data-to-Reports.mdx` | Formatted report-style exports (Excel, PDF, static output); options and limitations |
| 209 | `Workspaces-and-Folder-Organization.mdx` | Organizing apps, dashboards, and data sources with folders/Workspaces |
| 244 | `Dataset-Level-Date-and-Fiscal-Calendar-Defaults.mdx` | Setting dataset-level date range field and fiscal calendar; overriding card-level settings |
| 299 | `Handle-Source-Schema-Drift-in-Connectors.mdx` | When source adds/removes/renames columns; connector behavior; ETL schema adaptation |

---

## Phase 4 — Inputs and Pre-Work

Phase 4 has not started, but the Support KB Audit (`KB Audit Results.csv`, completed 2026-04-28) provides a confirmed retirement hit list that should be used directly as the Phase 4 execution plan for several categories. Do not re-run agent retirement analysis for these — the Audit already did it.

**Confirmed retirement batches ready for Phase 4:**

| Batch | Count | Action |
|-------|-------|--------|
| Workbench 4 articles | 37 (118 total Workbench articles flagged in Audit) | Archive — D1 confirmed |
| DataFusion articles | 11 (6 Deprecate, 5 Mark as Legacy) | Archive |
| Old Magic ETL tile articles | 15 to Archive + 1 Keep (`Create a Recursive/Snapshot Old Magic ETL DataFlow`) | Archive 15; keep 1 |
| Defunct-service connectors | 111 confirmed dead-service articles (verified via Audit summaries) | Archive / remove from Connector Library nav |
| Release notes pre-2022 (all languages) | Large volume (all locales) | Move to collapsed Archive group in Phase 7 |
| CourseBuilder articles | 16 (pending D10 PM confirmation) | Archive if PM confirms retired |

**Urgent pre-Phase 4 fix:** `Snowflake Connector` and `Snowflake Unload V2 Connector` documents key-pair/password auth that Snowflake retired November 2025. Customers are actively failing. Fix these now with `update-kb-article` before Phase 4 starts.

See `Support KB Audit Shared GAP Analysis.md` (repo root) for the full analysis and per-item rationale.

---

---

## Phase 5 — Interlinking

**Runs after:** Phase 4.5 (PM sign-off complete)

Bulk agent pass to add **Next Steps** and **Related Articles** sections to every article in the restructured KB. This phase cannot run before PM review because article titles and paths must be stable — content still being updated during PM review would produce stale links.

**Scope:**
- Every article in Pillars 1–10 gets a `## Next Steps` section pointing to logical follow-on articles
- Every article gets a `## Related Articles` section pointing to sibling articles in the same product group
- Cross-pillar links added where a KB how-to touches a portal/developer equivalent
- AI callout (`<Tip>**Try it with AI:**...`) added to applicable how-tos where a GA AI feature exists for the same task (see Cross-Cutting Concerns in `RESTRUCTURE-IA-SPEC.md`)

---

## Phase 6 — Slug Rename + Redirects + Localization

**Runs after:** Phase 5

Enhanced from original plan. Full sub-step sequence:

### 6.1 Generate rename CSV
Script reads all `s/article/` and `s/topic/` files and outputs `slug-rename-map.csv` (repo root):
```
original_filename,new_slug,article_title
000005874.mdx,What-is-Domo.mdx,What is Domo?
000042925394.mdx,Connect-to-Snowflake.mdx,Connect to Snowflake
...
```

### 6.2 Rename English article files
Apply all renames in `slug-rename-map.csv` to `s/article/` and `s/topic/`. Run in a single script pass to avoid partial-rename conflicts.

### 6.3 Rename localized files to match English slugs
The `ja/`, `de/`, `es/`, `fr/` directories use the same numeric filename scheme as English. Use `slug-rename-map.csv` to find matching localized files and rename them to the English slug. This creates exact filename parity across all languages — prerequisite for any future localization automation.

### 6.4 Update docs.json nav references
Replace all old numeric paths in docs.json with new slug paths. Run after 6.2/6.3 so the nav and files are in sync.

### 6.5 Add redirects to docs.json
For every renamed file, add a permanent (308) redirect entry to `docs.json`:
```json
"redirects": [
  { "source": "/s/article/000005874", "destination": "/s/article/What-is-Domo" },
  ...
]
```
Mintlify applies redirects at request time — goes live on next deploy. Preserves SEO and prevents broken external links.

### 6.6 Update all internal links in the repository
Grep all `.mdx` files for old numeric path strings. Use `slug-rename-map.csv` to replace each with the new slug path. This covers:
- Inline links in article bodies
- `existing_related_articles` references (if any remain in frontmatter)
- Any portal/ articles that link to s/article/ numeric paths

---

## Phase 7 — Nav Rebuild

**Runs after:** Phase 6 (all slugs stable and redirects in place)

Final rebuild of the `docs.json` Knowledge Base tab with correct slug-based paths. At this point, Phase 2's IA-spec-driven nav is already in place (pillar groups, etc.) — Phase 7 verifies integrity and cleans up any remaining issues.

**Checklist:**
- Run `mintlify broken-links` CLI — fix any remaining broken refs
- Verify Archive group is at the bottom of the KB tab
- Verify Legacy-tagged articles appear with `tag: "Legacy"` sidebar labels
- Verify all Phase 3a stub files have been replaced with real content
- Verify localized tab structures mirror the English KB structure

---

## Phase 8 — Style Guide & Template Update

**Runs after:** Phase 7

Update `Domo-KB-Style-Guide.mdx` and `New-Article-Template.mdx` to reflect every structural standard introduced by this restructure.

**`Domo-KB-Style-Guide.mdx` — expected additions:**
- **Archive vs Legacy vs Deleted** — the three categories, YAML spec, when to use each, LegacyNote/ArchivedNote snippet usage
- **Wheel-and-spoke product group structure** — standard pattern: one Overview/hub article + How-To articles + Reference articles (optional) + FAQ (in Accordion at bottom of hub); typical article counts per product group
- **Pillar hub articles** — what they are, when a new product area needs one, how they link to product group articles
- **New article types added by this restructure** — "What is X?" overview articles, pillar hub articles, getting-started-for-role articles; what makes each distinct
- **AI callout pattern** — when to add `<Tip>**Try it with AI:**...`; links to AI & Data Science pillar articles
- **Cross-pillar linking conventions** — KB ↔ Developer Portal cross-links; how to reference portal articles from KB

**`New-Article-Template.mdx` — expected additions:**
- Optional YAML fields for legacy/archived articles (`legacy: true`, `archived: true`, `tag: "Legacy"/"Archived"`)
- LegacyNote/ArchivedNote import/usage example (commented out — uncomment when applicable)
- Minor: verify existing template structure still matches the updated style guide

Run a diff of the current template against the style guide after Phase 7 to confirm exactly what needs updating — do not over-engineer this step.

**`CLAUDE.md` — review and update:**
CLAUDE.md is the AI-facing project instructions. After the restructure is complete, it references file paths, nav structure, and workflows that will have changed. Review and update:
- File path references (e.g., `s/article/` numeric IDs now have slug equivalents; new Phase 3a hub article slugs added)
- Architecture section — update to reflect the pillar-based navigation structure in docs.json and the addition of hub articles in `s/article/`
- Navigation section — update to reflect that docs.json now uses pillar groups rather than the old flat KB structure
- Any script references that have moved (if `scripts/output/` contents are now under `restructure/`)
- Add guidance on Archive vs Legacy article handling for future contributors
- Remove references to planning files that have moved to `restructure/`

CLAUDE.md stays at the repo root (not moved to `restructure/`) — it must be at root to be picked up by Claude Code.

---

## Phase 9 — Restructure Artifacts Cleanup

**Final phase — runs after Phase 8**

Move all planning and analysis artifacts generated during the restructure into a single folder named `restructure/` at the repo root. These files are not documentation — they are project records. Keeping them at the repo root clutters the working directory.

**Files to move to `restructure/`:**
- `KB-RESTRUCTURE-PLAN.md`
- `RESTRUCTURE-PROGRESS.md`
- `RESTRUCTURE-IA-SPEC.md`
- `RESTRUCTURE-TASKS.md` (generated at Phase 4.5)
- `slug-rename-map.csv` (generated at Phase 6)
- `Article-PM-Ownership-Reference.mdx`
- `Support KB Audit Shared GAP Analysis.md`
- `_gaps_with_support.json`
- `KB Audit Results.csv`
- `Feature - Owning Squad, PM, Eng, UX.csv`
- `pm-review-briefs/` directory (entire folder)
- `scripts/output/` JSON artifacts (catalog, ia-spec, ia-mapping, etc.)

**Files NOT moved:**
- `Domo-KB-Style-Guide.mdx` — stays at root; it's a live writer-facing reference
- `New-Article-Template.mdx` — stays at root; it's a live writer tool
- `snippets/` — stays; active MDX components
- `scripts/` — stays; active tooling

After moving, update `CLAUDE.md` to reflect the new location of these files (the Claude project instructions reference some of them by root-relative path).

---

## Scripts Reference

All restructure scripts live in `scripts/`. Run from repo root with `python3`.

| Script | Phase | Purpose |
|--------|-------|---------|
| `scripts/build_catalog.py` | 1.1 | Build `catalog.json` from all article frontmatter |
| `scripts/classify_catalog.py` | 1.2 | Classify articles by Diátaxis type (heuristics + optional API) |
| `scripts/apply_manual_classifications.py` | 1.2 | Apply hand-reviewed classifications for ambiguous articles |
| `scripts/find_duplicates_and_gaps.py` | 1.3–1.4 | Find orphans, near-duplicates, and per-pillar content gaps |
| `scripts/build_ia_spec.py` | 2 | Assign all 1,832 articles to 11 pillars; outputs `ia-spec.json` + `ia-mapping.json` |
| `scripts/build_docs_nav.py` | 2 | Rebuild KB tab in `docs.json` with 11-pillar groups from `ia-mapping.json`; preserves all other tabs |
| `scripts/build-pm-review-briefs.py` | 4.5 | Generate per-PM meeting briefs + `RESTRUCTURE-TASKS.md` checklist; run right before PM review meetings |

**To rebuild catalog from scratch** (if articles have changed since last run):
```bash
python3 scripts/build_catalog.py
python3 scripts/classify_catalog.py --api-limit 0
python3 scripts/apply_manual_classifications.py
python3 scripts/find_duplicates_and_gaps.py
```

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-06-10 | Use Diátaxis as taxonomy backbone | Best evidence-based framework; widely adopted by Canonical, Stripe, Atlassian |
| 2026-06-10 | Synthesize new articles from existing how-to content where possible | Keep KB internally consistent; avoid factual drift from writing from scratch |
| 2026-06-10 | Keep connector articles in A-Z library; add hub + category sub-groups | Too many connectors (971) to individually story-ize; reference library pattern is appropriate |
| 2026-06-10 | 22 exact-title duplicate connectors → keep longer article, retire shorter stub | Confirmed by line count comparison; Pattern A duplicates only |
| 2026-06-10 | Access-Tokens.mdx orphaned intentionally | Beta feature not yet in nav; add to nav when feature ships |
| 2026-06-10 | Phase 2 IA: 11 pillars + Archive (not 12) | Release Notes and Archive are navigational necessities but not content pillars in the story sense |
| 2026-06-10 | Goals → Administer & Govern | Goals is an org-level feature managed by admins; fits governance pattern |
| 2026-06-10 | Publications → Share & Collaborate | Slideshows and publication groups are sharing mechanisms, not app-building |
| 2026-06-10 | Projects & Tasks → Share & Collaborate (pending D2) | Collaboration feature; may move to Archive if feature is deprecated |
| 2026-06-10 | Workbench 4 → Archive (pending D1 human sign-off) | EOL product; 37 legacy articles; not surfaced in primary nav |
| 2026-06-10 | Connector library keeps A-Z structure | 971 connectors too many to story-ize; reference library + hub article is correct pattern |
| 2026-06-10 | DomoStats → AI & Data Science (override) | DomoStats is an analytics/data-science tool, not an admin tool despite admin overlap |
| 2026-06-17 | Cloud Data Warehouses merged into Connector Library | CDWs are connectors; separate top-level section created false structural split (workshop feedback: Leema Lallmamode) |
| 2026-06-17 | Writeback Connectors integrated into context, not standalone | CDW writeback lives in each CDW sub-group; standard writeback connectors appear alphabetically in the library (workshop feedback) |
| 2026-06-17 | "Data Providers" renamed to "Connectors" in all nav groups | Non-standard industry term; no competitor KB uses it (workshop feedback) |
| 2026-06-17 | Manage Data added as Pillar 3 | Missing link between Connect and Prepare: Data Center navigation, dataset discovery, lifecycle, sharing not covered anywhere (workshop feedback) |
| 2026-06-17 | Read/write framing convention added to Connect pillar | Authors must treat read + write as a pair in all Connect section overviews; prevents writeback from being invisible (workshop feedback) |
| 2026-06-25 | D1 confirmed: Workbench 4 → Archive | Support KB Audit confirms 118 of 188 Workbench articles flagged for Deprecate/Legacy; 37 Workbench 4 articles confirmed for Archive in Phase 4 |
| 2026-06-25 | DataFusion → Archive (all 11 articles) | Support KB Audit confirms DataFusion is discontinued; all 11 DataFusion articles flagged Deprecate or Legacy — add to Phase 4 retirement batch |
| 2026-06-25 | Old Magic ETL tile articles → Archive (15 articles; 1 Keep) | Support KB Audit flags 15 old Magic ETL tile interface articles for Archive; 1 (`Create a Recursive/Snapshot Old Magic ETL DataFlow`) is Keep-flagged — do not archive |
| 2026-06-25 | Defunct-service connectors → Archive (111 confirmed) | 111 connector articles verified via Audit summaries confirming the underlying service no longer exists; use Audit list as Phase 4 execution plan |
| 2026-06-25 | D10 added: CourseBuilder — pending PM confirmation | Support KB Audit flags CourseBuilder as retired/removed from Domo Appstore; 16 articles (not 4 — initial count missed localized articles); confirm with PM before Phase 7 — Archive if confirmed |
| 2026-06-25 | Snowflake auth deprecation flagged as urgent pre-Phase fix | Snowflake retired key-pair/password auth November 2025; Snowflake Connector and Snowflake Unload V2 articles are actively misleading customers; fix with update-kb-article before Phase 4 begins |
| 2026-06-25 | Support KB Audit integrated into Restructure phases | Gap analysis (`Support KB Audit Shared GAP Analysis.md`) cross-referenced Audit against Restructure plan; shared retirement work merged into Phase 4; Audit-only work (API reference quality, connector content accuracy, localization retirement, screenshot refresh) scoped as separate post-restructure project |
| 2026-07-14 | Community forum gap analysis (`_gaps_with_support.json`) integrated as Phase 3a/3b input | 5,452 forum records → 361 scored gaps; 57 net-new articles and 304 article updates identified. Cross-diffed against existing restructure plan: no Critical/High gaps were already addressed (only Snowflake auth fix and DataFusion archival had partial overlap). Two new phases added to tracking: 3a-Forum (~57 new articles) and 3b-Forum (~68 Critical+High update targets). Medium/Low gaps are Phase 3b bulk input. |
| 2026-07-14 | DataFusion Phase 4 archival must include migration guidance article | Forum gap analysis (rank 198) confirms users actively searching for ETL replacement guidance after DataFusion removal. Phase 4 archival should add `DataFusion-Migration-Guide.mdx` pointing users to Magic ETL equivalents before or alongside archiving the 11 DataFusion articles. |
| 2026-07-14 | PM Review System built as Phase 2.5 | `scripts/build-pm-review-briefs.py` generates per-PM meeting briefs from IA spec + forum gap data + ownership reference. Run right before PM review meetings (not now). Section 4 of each brief covers both Audit gap-fill changes and forum update targets in that PM's area — executed changes should be updated in the script's hardcoded phase data so the brief reflects reality when run. |
| 2026-07-14 | Phase 2.5 (PM Review System) moved to Phase 4.5 | PM review now runs AFTER Phases 3a–4 (all content work complete) rather than before Phase 3a. PMs review actual completed changes, not plans. This makes the review actionable: fact-checks, sign-offs, and legacy confirmations all happen against real written/updated articles. |
| 2026-07-14 | Archive vs Legacy vs Deleted distinction defined | Three explicit categories for content removal: (1) Deleted — restructured into other content, file removed; (2) Archived — genuinely retired, no living successor, file kept in Archive nav group with `archived: true` + `<ArchivedNote />`; (3) Legacy — feature still functional but unmaintained, file stays in pillar with `legacy: true` + `tag: "Legacy"` + `<LegacyNote />`. PM sign-off required for Legacy marking. |
| 2026-07-14 | Legacy frontmatter approach confirmed | Mintlify native `tag:` frontmatter field renders a visible sidebar label — use `tag: "Legacy"` for legacy articles and `tag: "Archived"` for archived articles. Custom fields `legacy: true` / `archived: true` serve tooling. `<LegacyNote />` and `<ArchivedNote />` snippets (to build at Phase 4 time) provide body-level callouts. Do NOT use `deprecated: true` for Legacy articles — "deprecated" implies a removal date which Legacy explicitly does not. |
| 2026-07-14 | Phase 6 (Slug Rename) significantly enhanced | Original plan was: rename files, rebuild nav. New plan adds 4 sub-steps: (6.1) generate slug-rename-map.csv; (6.3) rename localized files (ja/de/es/fr) to English slug for exact filename parity; (6.5) add permanent 308 redirects to docs.json for all renamed paths; (6.6) update all internal links in the repo using the CSV mapping. |
| 2026-07-14 | Phase 8 (Style Guide + Template + CLAUDE.md) added | Final human-facing standards update: Domo-KB-Style-Guide.mdx gets Archive/Legacy standards, wheel-and-spoke product group structure, pillar hub article guidance, AI callout pattern, and cross-pillar linking conventions. New-Article-Template.mdx gets legacy/archived YAML fields. CLAUDE.md gets full review and update to reflect the restructured repo — stays at root (not moved to restructure/). |
| 2026-07-14 | Phase 9 (Restructure Artifacts Cleanup) added | All planning/analysis/tracking artifacts (KB-RESTRUCTURE-PLAN.md, RESTRUCTURE-PROGRESS.md, RESTRUCTURE-IA-SPEC.md, RESTRUCTURE-TASKS.md, slug-rename-map.csv, ownership reference, audit/gap files, pm-review-briefs/, scripts/output/) move to restructure/ folder at repo root after Phase 8. Keeps live documentation directory clean post-restructure. |
| 2026-07-14 | RESTRUCTURE-TASKS.md granular checklist system defined | Generated at Phase 4.5 by updated build-pm-review-briefs.py. Organized Pillar → Product Group → discrete tasks with type tags: [new-article], [update], [archive], [legacy], [deleted], [pm-input], [decision], [fact-check]. This is the working document for PM meetings and post-PM execution — query it at any time for remaining tasks by pillar, PM, or type. |
| 2026-07-14 | Restructure scope confirmed: s/article/ only; portal/ is out of scope | Phase 3a article paths corrected from portal/ subdirectories to s/article/. The portal/ directory (Developer Portal) is entirely out of scope for this restructure — no new portal/ files, no portal/ nav changes. The only portal/ work is Phase 5 interlinking, which adds links FROM s/article/ how-tos TO existing portal/ pages. Phase 8 CLAUDE.md review language updated to remove incorrect portal/ references. Phases 1 and 2 were unaffected (already scoped to s/article/ throughout). |
| 2026-07-14 | D9 resolved — Manage Data pillar populated | 31 DataSet Management articles split: 20 → Manage Data (3 in "Data Center" group: Data Center Layout, Using the Data Warehouse, Understanding Connector Options; 17 in "DataSet Lifecycle" group: ownership, sharing, health, lifecycle how-tos). 5 pipeline articles stay in Prepare & Transform (DataSet Update Methods, DataFusion ×2, Enterprise Stacker, Advanced Tools Launch Center). 1 (PDP) → Administer & Govern > Governance. 2 developer tools (CLI, ODBC) → Develop & Integrate > APIs & SDKs. 1 (Migrate from Federated to Cloud) → Connect & Bring In Data > Cloud Data Warehouses. 2 visualization articles → Analyze & Visualize > Analyzer. `scripts/build_ia_spec.py` OVERRIDES section updated; Phase 2 re-run confirms 1,832/1,832 articles assigned. |
