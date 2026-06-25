# KB Restructure Progress Tracker

This file is the canonical source of truth for where we are in the KB restructure.
Update it at the end of every work session. Future Claude sessions should read this
file at the start of any restructure work to orient themselves before doing anything.

**Plan document:** `KB-RESTRUCTURE-PLAN.md`
**Last updated:** 2026-06-17

---

## Current Status

**Active phase:** Phase 3a — Net-New Articles (synthesizable)
**Blocked on:** 8 human decisions (see Phase 2 Decision Required table in `RESTRUCTURE-IA-SPEC.md`)

---

## Phase Completion

| Phase | Status | Notes |
|-------|--------|-------|
| **1: Audit & Inventory** | ✅ Complete | All outputs written to `scripts/output/` |
| **2: IA Design** | ✅ Complete | See `RESTRUCTURE-IA-SPEC.md`; 8 decisions need human sign-off |
| **3a: Net-New Articles (~26)** | 🔲 Not started | Synthesizable from existing content; see article list below |
| **3a-PM: PM Input Articles (4)** | 🔲 Blocked — awaiting PM | See PM Input section below |
| **3b: Article Upgrades (~200)** | 🔲 Not started | Bulk agent edit pass |
| **4: Consolidation & Retirement** | 🔲 Not started | Address duplicates + legacy content |
| **5: Interlinking** | 🔲 Not started | Next Steps + Related Articles bulk pass |
| **6: Rename to Slugs** | 🔲 Not started | Script-driven; run after Phase 3a |
| **7: Nav Rebuild** | 🔲 Not started | Rebuild docs.json after Phase 6 |

---

## Phase 1 Outputs (Complete)

All files are in `scripts/output/`:

| File | Description | Key stats |
|------|-------------|-----------|
| `catalog.json` | Master article inventory | 1,819 articles; 1 missing excerpt |
| `catalog-classified.json` | Inventory + Diátaxis type per article | See distribution below |
| `orphans.json` | Articles not appearing in docs.json nav | 2 articles |
| `merge-candidates.json` | Near-duplicate title pairs (Jaccard ≥ 0.55) | 838 pairs; 22 exact (1.00) |
| `gap-analysis.json` | Missing tutorial/explanation coverage per pillar | 6 of 10 pillars missing tutorials |

### Classification Distribution

| Type | Count | Notes |
|------|-------|-------|
| connector | 971 | ~53% of all content |
| howto | 564 | ~31% — the main article bulk |
| explanation | 70 | conceptual/overview articles |
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
- **Connect & Bring In Data** — 1,064 articles, 0 tutorials (largest gap)
- **Prepare & Transform Data** — 109 articles, 0 tutorials
- **Administer & Govern** — 70 articles, 0 tutorials
- **Share & Collaborate** — 15 articles, 0 tutorials
- **Develop & Integrate** — 3 articles, 0 tutorials, 0 explanations (severely underdocumented)
- **Other** — 64 articles, 0 tutorials (catch-all bucket needing categorization)

---

## Phase 2 — Complete

All 1,819 articles assigned to 11 pillars + Archive. Full spec in `RESTRUCTURE-IA-SPEC.md`.

**Outputs:**
- `scripts/output/ia-spec.json` — every article → `{pillar, group, sub_group}`
- `scripts/output/ia-mapping.json` — pillar → list of articles
- `RESTRUCTURE-IA-SPEC.md` — human-readable nav spec with full hierarchy, new articles to write, and 8 open decisions

**8 decisions need human sign-off before Phase 7 (nav rebuild):**
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
| D9 | Which DataSet Management articles (currently in Prepare & Transform) move to new Manage Data pillar? |

These decisions don't block Phase 3a article writing — they only block the nav rebuild in Phase 7.

---

## Phase 3a — Next Steps (Start Here Next Session)

Write the ~26 new articles that can be synthesized from existing KB content. All require the `new-kb-article` or `new-overview-article` skill. Net-new files must be written in the **main session** (sub-agents cannot Write new files).

**Priority order for Phase 3a:**

| Priority | Filename | Synthesize from | Skill |
|----------|---------|-----------------|-------|
| 1 | `portal/getting-started/What-is-Domo.mdx` | 000005874 + role guides | `new-overview-article` |
| 2 | `portal/getting-started/Getting-Started-for-Admins.mdx` | Admin how-tos | `new-kb-article` |
| 3 | `portal/getting-started/Getting-Started-for-App-Builders.mdx` | App Studio/Workflows overview | `new-kb-article` |
| 4 | `portal/getting-started/Getting-Started-for-Developers.mdx` | API articles, Access Tokens | `new-kb-article` |
| 5 | `portal/prepare-transform/What-is-a-DataSet.mdx` | Connector + ETL articles | `new-overview-article` |
| 6 | `portal/prepare-transform/What-is-Magic-ETL.mdx` | Magic ETL overview articles | `new-overview-article` |
| 7 | `portal/prepare-transform/What-is-a-DataFlow.mdx` | DataFlow articles | `new-overview-article` |
| 8 | `portal/prepare-transform/Prepare-and-Transform-Overview.mdx` | All ETL/DataFlow articles | `new-overview-article` |
| 9 | `portal/analyze-visualize/What-is-a-Card.mdx` | Analyzer articles | `new-overview-article` |
| 10 | `portal/analyze-visualize/What-is-a-Dashboard.mdx` | Dashboard articles | `new-overview-article` |
| 11 | `portal/analyze-visualize/What-is-Beast-Mode.mdx` | Beast Mode FAQ + functions ref | `new-overview-article` |
| 12 | `portal/analyze-visualize/Analyze-and-Visualize-Overview.mdx` | All analyzer/chart articles | `new-overview-article` |
| 13 | `portal/share-collaborate/What-is-an-Alert.mdx` | Alerts Overview + alert articles | `new-overview-article` |
| 14 | `portal/connect/What-is-a-Connector.mdx` | General Connector Info (12 articles) | `new-overview-article` |
| 15 | `portal/connect/Connect-and-Bring-In-Data-Overview.mdx` | All connector articles; frames read + write | `new-overview-article` |
| 16 | `portal/manage-data/Manage-Data-Overview.mdx` | DataSet articles, Data Center context | `new-overview-article` |
| 17 | `portal/manage-data/What-is-the-Data-Center.mdx` | DataSet management articles | `new-overview-article` |
| 18 | `portal/manage-data/Find-and-Manage-Your-DataSets.mdx` | DataSet management, sharing, workspace articles | `new-kb-article` |
| 19 | `portal/ai-data-science/What-is-Domo-AI.mdx` | Domo AI FAQ + AI articles | `new-overview-article` |
| 20 | `portal/ai-data-science/AI-and-Data-Science-Overview.mdx` | All AI/DomoStats/Jupyter articles | `new-overview-article` |
| 21 | `portal/build-automate/What-is-App-Studio.mdx` | App Studio Overview | `new-overview-article` |
| 22 | `portal/build-automate/Build-Apps-and-Automate-Overview.mdx` | App Studio/Workflows/Code Engine | `new-overview-article` |
| 23 | `portal/connect/What-is-Workbench.mdx` | Workbench 5.2 overview | `new-overview-article` |
| 24 | `portal/share-collaborate/Share-and-Collaborate-Overview.mdx` | Sharing/Buzz/Publications articles | `new-overview-article` |
| 25 | `portal/administer-govern/Domo-User-Roles.mdx` | Roles/grants articles | `new-overview-article` |
| 26 | `portal/administer-govern/Security-and-Permissions-Overview.mdx` | PDP, OAuth, security articles | `new-overview-article` |
| 27 | `portal/administer-govern/Administer-and-Govern-Overview.mdx` | All admin articles | `new-overview-article` |
| 28 | `portal/administer-govern/Domo-Sandbox-Overview.mdx` | Sandbox article | `new-overview-article` |
| 29 | `portal/develop-integrate/Develop-and-Integrate-Overview.mdx` | Existing 5 API articles | `new-overview-article` |

**Note on file paths:** The `portal/` sub-paths above are proposed — they don't exist yet. They'll be created when Phase 3a articles are written. Confirm directory structure before first write.

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

## Scripts Reference

All restructure scripts live in `scripts/`. Run from repo root with `python3`.

| Script | Phase | Purpose |
|--------|-------|---------|
| `scripts/build_catalog.py` | 1.1 | Build `catalog.json` from all article frontmatter |
| `scripts/classify_catalog.py` | 1.2 | Classify articles by Diátaxis type (heuristics + optional API) |
| `scripts/apply_manual_classifications.py` | 1.2 | Apply hand-reviewed classifications for ambiguous articles |
| `scripts/find_duplicates_and_gaps.py` | 1.3–1.4 | Find orphans, near-duplicates, and per-pillar content gaps |
| `scripts/build_ia_spec.py` | 2 | Assign all 1,819 articles to 11 pillars; outputs `ia-spec.json` + `ia-mapping.json` |

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
