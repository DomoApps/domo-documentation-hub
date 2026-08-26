# KB Restructure Progress Tracker

This file is the canonical source of truth for where we are in the KB restructure.
Update it at the end of every work session. Future Claude sessions should read this
file at the start of any restructure work to orient themselves before doing anything.

**Plan document:** `KB-RESTRUCTURE-PLAN.md`
**Disposition log:** `RESTRUCTURE-MANIFEST.md` — running record of what happened to every article; updated throughout all phases; Phase 9 converts it to the final audit report
**Last updated:** 2026-08-26 (Phase 3b general **15 Medium `rec=new` net-new triaged + cleared**: coverage research → 4 written & in nav [299, 114, 118, 159], 5 confirmed DEFER→PM briefs [127, 142, 146, 209, 244], 2 flagged OUT-OF-SCOPE/portal [144, 161]. 4 others [117/139/152/172] were already written 2026-08-04.)

---

## Current Status

**Active phase:** Phase 3b general — forum-gap pass COMPLETE → remaining 3b work: structural intro/prereq pass + 15 Medium `rec=new` net-new articles; or advance to Phase 4
**Blocked on:** 8 human decisions (see Phase 2 Decision Required table in `RESTRUCTURE-IA-SPEC.md`)

### ▶ Where we left off (2026-08-26) — pick up here next session

**▶▶ RESUME TOMORROW — read this first.**
- **State:** branch `update/fullRestructure`. Forum-gap pass committed+pushed through `0ff8bda5`. The 2026-08-26 net-new work (4 new articles + docs.json + manifest/tracker edits) is **NOT yet committed** — working tree has uncommitted changes. Commit before starting new work.
- **Just finished:** Triaged and cleared the **15 Medium `rec=new` net-new articles**. Coverage-researched all 15 (4 parallel agents): **4 written + in nav** (`Handle-Source-Schema-Drift-in-Connectors` 299 clean; `Dynamic-Dropdowns-in-Table-Cards` 114 → 1 `[pm-input]` Chris Wright; `Editor-Dataset-Access-Scope` 118 → 2 `[pm-input]` Phil Fuchs; `Extract-Data-from-PDFs-with-Domo-AI` 159 → 2 `[pm-input]` Ken Boyer). **5 confirmed DEFER** (127, 142, 146, 209, 244) stay in the manifest deferred table. **2 DROPPED as out-of-scope** (144, 161 — Developer Portal; restructure does not touch `portal/`). (117/139/152/172 were already written 2026-08-04.) Gates run: fact-check (all 19 internal links resolve; claims verified) + style; screenshots omitted (self-sufficient text — no source-screenshot pull).
- **First action tomorrow:** commit the uncommitted net-new work, then decide the next chunk (options below), then go.
  1. **Structural intro/prereq sweep (~200 articles)** — the remaining Phase 3b general item: add a concept intro (from `excerpt`) + prerequisites to articles lacking them. Fuzzy target; consider script-assisting the "which articles lack an intro" detection first. NO interlinking (that's Phase 5).
  2. **Net-new leftover:** gap 148 (App Studio card-actions) — not part of the 15; verify still wanted.
  3. **Advance to Phase 4** (Consolidation & Retirement) — retirement batches are pre-scoped (Workbench 4, DataFusion, old Magic ETL tiles, defunct connectors, CourseBuilder); see Phase 4 section + Support KB Audit.
- **How the forum-gap pass was run (reuse this rig for the structural sweep):** `scripts/reports/phase3b_build_clusters.py` clusters gaps by PM into `scripts/reports/phase3b_clusters/*.md`; `_AGENT-INSTRUCTIONS.md` is the shared agent prompt; launch parallel general-purpose agents (one per cluster, ≤5 files / ≤9 gaps, collision-free); verify each wave with `scripts/reports/check_tag_balance.py` + the stray-marker/`[pm-input]`-format greps; commit per wave. Full recipe in `_WAVE-STATUS.md`.

---

**Phase 3b general FORUM-GAP PASS is COMPLETE.** All 236 Medium/Low `rec=update` community-forum gaps triaged via 5 waves of parallel sub-agents (35 PM clusters + 4 re-route clusters = 39 agent tasks). Full per-wave/per-cluster detail in `RESTRUCTURE-MANIFEST.md` › Phase 3b general; live tracking in `scripts/reports/phase3b_clusters/_WAVE-STATUS.md`.

- **~134 distinct articles updated**, **~172 new `[pm-input]` markers** (auto-flow to owning PMs' Phase 4.5 briefs — this is the main yield).
- **27 gaps deferred** as out-of-scope (portal/-only targets or dead targets) — logged in `scripts/reports/phase3b_clusters/_DEFERRED.md`.
- **~18 gaps were mislinked in the source data** (`existing_related_articles` pointed at the wrong article) — all caught by agents (skipped rather than mis-edited) and re-homed in Wave 5. Agents also caught ~4 factually false gap claims (not asserted) and fixed 3 pre-existing article bugs.
- Every wave verified: docs.json untouched, no new files, 0 stray TODO/FIXME, all `[pm-input]` markers well-formed, all JSX block tags balanced. Committed per wave (`b628279c`, `12e53470`, `295b05b3`, `75f5a0f4`, `2f15cfbf`). Not pushed.

**NEXT (remaining Phase 3b general, not started):**
1. **Structural intro/prerequisites upgrade pass (~200 articles)** — the mechanical sweep: add a concept intro (from `excerpt`) + prerequisites to articles lacking them. Separate from forum gaps. (NOTE: interlinking/Next Steps/Related is Phase 5, not here.)
2. ~~**15 Medium `rec=new` net-new articles**~~ — **DONE 2026-08-26.** Triaged: 4 written (299, 114, 118, 159), 5 DEFER→PM briefs (127, 142, 146, 209, 244), 2 DROPPED as out-of-scope/portal (144, 161), 4 already-written earlier (117/139/152/172). See `RESTRUCTURE-MANIFEST.md` written + deferred tables.
3. **Net-new backlog from the forum pass:** gap 148 (App Studio card-actions article), gap 303 (portal Forms rich text — out of scope).

Or advance to **Phase 4** (Consolidation & Retirement). All 266 Medium/Low forum gaps have now been consumed by the 3b pass.

**Also open (non-blocking):** rank-146 `Domo-Certification-Exam-Logistics.mdx` has no roster PM — needs a human ownership decision before Phase 4.5. (Gaps 144 and 161 were dropped 2026-08-26 as out-of-scope Developer Portal topics.)

---

**Phase 3a quality gates:** ✅ Complete 2026-07-15 — all 3 gates passed on all 31 articles; 15+ factual fixes, 30 screenshots added, see `RESTRUCTURE-MANIFEST.md`
**Snowflake urgent fix:** ✅ Complete 2026-07-15 — 7 Snowflake connector articles updated (retirement language, `<Note>` → `<Warning>`, migration section rewritten); PM: Tasleema Lallmamode; see Phase 3b section in `RESTRUCTURE-MANIFEST.md`
**Phase 3a-Forum:** ✅ Writing pass complete (2026-08-04) — all 57 scored net-new gaps triaged: **14 written**, **43 deferred** to PM briefs (undocumented mechanics; logged in `RESTRUCTURE-MANIFEST.md` › Deferred to PM Briefs, one row per gap with PM + what the PM must supply). Written: 5 Critical, 5 High (ranks 26, 32, 49, 50, 89), 4 Medium (ranks 117, 139, 152, 172). The 43 deferred become `[pm-input]` items in the Phase 4.5 PM briefs.

**Standing rule — pending articles:** Any article that cannot be completed without PM or human context (missing feature details, unclear positioning, unconfirmed scope) is automatically added as a `[pm-input]` item in the relevant PM's Phase 4.5 meeting brief. It is never tracked as a blocker to the current phase. Write what can be written from existing KB content; note the gap in the PM brief.
**Phase 1/2 re-run:** Complete 2026-07-14 on branch `update/fullRestructure`
**Phase 3a core:** ✅ Complete 2026-07-14 — all 29 synthesizable articles written and in docs.json

---

## Phase Completion

| Phase | Status | Notes |
|-------|--------|-------|
| **1: Audit & Inventory** | ✅ Complete (re-run 2026-07-14) | 1,832 articles; 2 orphaned; 842 merge candidates (23 exact); see updated findings below |
| **2: IA Design** | ✅ Complete (re-run 2026-07-14) | 11 pillars in `docs.json` KB tab; 1,832 articles assigned; see Phase 2 outputs below |
| **3a: Net-New Articles (~29)** | ✅ Complete (2026-07-14) | 29 articles written; all registered in docs.json; MCP group fixed |
| **3a-PM: PM Input Articles (4)** | ➡️ Moved to Phase 4.5 PM briefs | [pm-input] items in per-PM meeting briefs; see PM Input section below |
| **3a-Forum: Forum-Driven New Articles (~57)** | ✅ Writing pass complete (2026-08-04) | All 57 triaged: 14 written, 43 deferred to PM briefs (undocumented mechanics). See Forum Gap Analysis section + `RESTRUCTURE-MANIFEST.md` |
| **3b: Article Upgrades (~200)** | 🔄 Forum-gap portion + 15 Medium net-new COMPLETE | Medium/Low forum gaps done (5 waves, ~134 articles, ~172 `[pm-input]`). 15 Medium `rec=new` triaged 2026-08-26 (4 written, 5 defer, 2 out-of-scope). Remaining: structural intro/prereq sweep (~200) |
| **3b-Forum: Forum-Driven Article Updates (Critical+High, ~68)** | ✅ Complete (2026-08-20) | All 68 done: Critical 7 (committed), High 61 (10 parallel agents, 2 waves). 45 files, ~84 total `[pm-input]` across the phase. Ranks 42/93 re-routed to correct homes. |
| **3c: Main Branch Content Sync** | 🔄 Sync #1 complete (2026-08-20); sync #2 pre-merge | Sync #1: 15 new + 68 edits + 12 portal + 72 images + 1 snippet from main; 5 conflicts resolved; 1 deletion mirrored; 1 case-rename; 14 new articles into nav (1 deprecated held). Sync #2 uses the numeric-ID parity system. |
| **4: Consolidation, Retirement & Archive** | 🔲 Not started | Duplicates, lifecycle classification; see Product Lifecycle Standards below |
| **4.5: PM Review System** | 🔧 Built — run after Phase 4 | Script ready: `scripts/build-pm-review-briefs.py`; generates per-PM task checklists + meeting briefs |
| **4.6: Lifecycle Status Application** | 🔲 Not started | Bulk-add `status: "active"` to all articles; apply PM-confirmed non-Active states; move Legacy/Sunset to Archive group; remove Retired from nav |
| **5: Interlinking** | 🔲 Not started | Next Steps + Related Articles bulk pass — runs after PM sign-off |
| **6: Slug Rename + Redirects + Localization** | 🔲 Not started | Enhanced: CSV map, localized file rename, docs.json redirects, internal link updates |
| **7: Nav Rebuild** | 🔲 Not started | Rebuild docs.json nav groups after Phase 6 slug changes |
| **8: Style Guide & Template Update** | 🔲 Not started | Update `Domo-KB-Style-Guide.mdx` + `New-Article-Template.mdx` for new standards |
| **9: Restructure Artifacts Cleanup** | 🔲 Not started | Move all planning/analysis artifacts to `restructure/` folder; generate final disposition report from `RESTRUCTURE-MANIFEST.md` |

---

## Quality Gates — Required for Every Net-New or Significantly Updated Article

Every article written or meaningfully updated during Phases 3a, 3a-Forum, 3b, 3b-Forum, and 4 must pass all three gates **in order** before it is considered done. Do not skip or reorder.

### Gate 1 — Fact-Check (runs first)

Verify claims against source KB articles. The goal is to catch hallucinations and ensure nothing was misrepresented when synthesizing from existing content.

**Checklist:**
- Read each source article the new article was synthesized from (listed in RESTRUCTURE-MANIFEST.md `source_articles` column)
- Verify every named feature, capability, and limitation against the source
- Verify every grant name matches its canonical wording (search existing articles: `grep -rn "Grant Name —" s/article/`)
- Verify every internal link resolves to a real file (`ls s/article/<slug>.mdx`)
- Flag any claim that cannot be verified as `{/* FACT-CHECK: [claim] — could not verify against source */}`

### Gate 2 — Screenshot Audit (runs second)

Screenshots are first-class content. Walls of text are not acceptable. Every article must make its best effort to include applicable screenshots from source material.

**Checklist:**
- Read all source articles and collect every `<img>` or `<Frame>` reference
- For each screenshot: does it illustrate something covered in the new article?
  - **Yes → include it**, wrapped in `<Frame>`, with original alt text preserved
  - **Maybe → include it speculatively**; human reviewer decides whether to keep it
  - **No → omit it** (no TODO markers; clean articles only)
- For overview/hub articles: include at minimum one screenshot of the feature's main UI
- For how-to articles: include all applicable step screenshots from source material
- Do not leave `{/* TODO: screenshot */}` or similar markers in article files — either include it or don't; human reviewers can add screenshots during manual verification
- For split articles (one source → multiple targets): assign each screenshot to exactly one target article in RESTRUCTURE-MANIFEST.md; do not leave any screenshot unassigned

### Gate 3 — Style Guide Review (runs last)

Structural and formatting compliance check against `Domo-KB-Style-Guide.mdx`.

**Checklist:**
- `title:` and `excerpt:` both present in frontmatter
- Intro section is H2, succinct, uses "This article explains/covers…" format
- Horizontal rule (`---`) follows the Intro section
- `## Required Grants` section present (if feature requires grants); uses exact format from style guide
- Task/action headings use imperative mood (no gerund form); topic/category labels may use noun phrases
- All headings use Title Case (Chicago 18th: all prepositions lowercase regardless of length)
- FAQ section uses `<AccordionGroup>` + `<Accordion title="...">` format; located at bottom
- All callout labels are bolded: `**Note:**`, `**Warning:**`, `**Tip:**`
- All internal links use root-relative format `/s/article/slug` (no `.mdx` extension)
- All block-level screenshots wrapped in `<Frame>`

### Decomposition Record (for splits only)

When a large source article is split into multiple new articles, create a decomposition record in RESTRUCTURE-MANIFEST.md for the source article. Before the source article is deleted or archived, every section in its decomposition record must be marked as addressed in a specific target article. No source article may be removed until its decomposition record is 100% complete.

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

## Product Lifecycle Standards

These standards replace the previous Archive/Legacy two-state system. They apply throughout Phases 3–4 and must be reflected in Phase 8 (Style Guide update).

### Five lifecycle states

| State | What it means | File fate | Nav fate | YAML | Visual indicator |
|-------|--------------|-----------|----------|------|-----------------|
| **Active** | Current, fully supported. Receives updates and bug fixes. | File kept | Normal position in KB nav | `status: "active"` | None — this is the default, implicit state |
| **Deprecated** | Still functional but officially discouraged. Users should migrate to a replacement. | File kept | Stays in its **normal pillar group** (not archived) | `status: "deprecated"`, `tag: "Deprecated"` | `<DeprecatedNote />` callout just below title, before intro |
| **Legacy** | Deeply integrated old technology kept alive solely for critical backwards compatibility. No active development. | File kept | Moved to **Archive group** at bottom of KB tab | `status: "legacy"`, `tag: "Legacy"` | `<LegacyNote />` callout just below title, before intro |
| **Sunset** | Official end-of-life countdown in progress. EOL date announced. Support drops on a known date. | File kept | Moved to **Archive group** at bottom of KB tab | `status: "sunset"`, `tag: "Sunset"`, `sunset_date: "YYYY-MM-DD"` | `<SunsetNote />` callout just below title, before intro |
| **Retired** | Completely removed or shut down. Feature no longer runs or accepts traffic. | File kept | **Not in nav at all** — exists in repo for reference only | `status: "retired"` | None — article is unpublished |

**Deleted** is a separate disposition (not a lifecycle state) for articles whose content has been fully absorbed into other articles. Deleted files are removed from the repo and nav entirely. See Key Rule below.

**Key rule:** If an article's content is used elsewhere in any form — merged into another article, its information rewritten into a new article — the original file is **deleted**, not given a lifecycle status. Lifecycle states are only for articles whose content still serves readers in its current form.

### YAML frontmatter spec

The `status` field is the canonical lifecycle identifier used by restructure tooling (PM review script, task tracker, disposition report). The `tag` field is a native Mintlify frontmatter property that renders a visible label next to the article title in the sidebar — it accepts any string.

**Active article** (explicit; may be omitted — active is the implicit default):
```yaml
---
title: "Article Title"
status: "active"
---
```

**Deprecated article** (stays in normal nav, visible "Deprecated" sidebar label, warning callout):
```yaml
---
title: "Article Title"
status: "deprecated"
tag: "Deprecated"
---
```

**Legacy article** (Archive group, visible "Legacy" sidebar label, warning callout):
```yaml
---
title: "Article Title"
status: "legacy"
tag: "Legacy"
---
```

**Sunset article** (Archive group, visible "Sunset" sidebar label, warning callout, EOL date):
```yaml
---
title: "Article Title"
status: "sunset"
tag: "Sunset"
sunset_date: "2026-12-31"
---
```

**Retired article** (not in nav; metadata only; no callout needed):
```yaml
---
title: "Article Title"
status: "retired"
---
```

### Snippets to create at Phase 4 execution time

All three follow the `snippets/BetaNote.mdx` pattern. Import at the top of the MDX file, use as a standalone component just below the YAML frontmatter block and before the `## Intro` section. For partial-article deprecation/legacy/sunset (where only one section is affected), place the callout as the first element under the relevant section heading instead.

- `snippets/DeprecatedNote.mdx` — renders a `<Warning>` callout: "**Deprecated:** This feature is officially deprecated. It remains functional but is no longer recommended. Please migrate to [replacement link] to avoid disruption when this feature is removed."
- `snippets/LegacyNote.mdx` — renders a `<Warning>` callout: "**Legacy:** This article describes a feature that is no longer actively maintained. It remains functional for backwards compatibility only. For the current approach, see [replacement link]."
- `snippets/SunsetNote.mdx` — renders a `<Warning>` callout: "**Sunset:** This feature is scheduled for end of life on [sunset_date]. Support and updates have ended. Please migrate to [replacement link] before that date."

All three accept an optional `replacement` prop (a URL or article path) used to generate the "see [replacement link]" anchor. When no replacement exists yet, the prop is omitted and the sentence is dropped from the callout.

### Determining lifecycle state — PM confirmation required

Lifecycle state beyond **Active** requires PM sign-off. During Phase 4 and Phase 4.5, articles in a PM's area that are candidates for Deprecated/Legacy/Sunset/Retired designation will appear in their PM review brief as decision items. PM must confirm:

| State being assigned | PM must confirm |
|----------------------|----------------|
| Deprecated | Feature is still functional; a recommended replacement exists; migration timeline or guidance is available |
| Legacy | Feature still exists in Domo; it is not actively developed/maintained; no planned removal date; a successor approach exists |
| Sunset | Feature has an announced EOL date; support has ended or is ending; migration path exists |
| Retired | Feature is completely gone from Domo — no longer runs, no longer accessible to customers |

The PM review brief script (`scripts/build-pm-review-briefs.py`) should be updated before Phase 4.5 to include a "Lifecycle Candidates" section per PM, surfacing articles from the Support KB Audit flagged for any non-Active state.

The task checklist type tags for Phase 4.5 expand to:
- `[deprecated]` — article marked Deprecated; PM must confirm replacement exists
- `[legacy]` — article marked Legacy; PM must confirm feature still runs, no removal date
- `[sunset]` — article marked Sunset; PM must provide EOL date
- `[retired]` — article marked Retired; PM must confirm feature is gone from product

### Applying lifecycle states to existing retirement batches (Phase 4 guidance)

| Batch | Default state | Rationale |
|-------|---------------|-----------|
| Workbench 4 articles (37) | **Legacy** | WB4 still installed at some sites; WB5 is the replacement; no announced removal date |
| DataFusion articles (11) | **Retired** | DataFusion was discontinued and removed from the product |
| Old Magic ETL tile articles (15) | **Retired** | Old tile interface fully replaced; no longer accessible |
| Defunct-service connectors (111) | **Retired** | Underlying third-party services no longer exist |
| CourseBuilder articles (16) | **Retired** (pending D10 confirmation) | Audit flags as removed from Domo AppStore; confirm with PM |

These assignments are defaults for Phase 4 planning. PM sign-off in Phase 4.5 may change any individual article's state.

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
- [ ] [pm-input] `Choose-the-Right-Data-Prep-Tool.mdx` — need: ETL vs DataFlow vs SQL positioning
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

**Note (2026-08-18):** Phase 3a-Forum data is no longer hardcoded in the script. `build-pm-review-briefs.py` now reads the **`RESTRUCTURE-MANIFEST.md`** Phase 3a-Forum *written* and *deferred* tables as its source of truth, and scans `s/article/*.mdx` for embedded `{/* [pm-input] … */}` markers to build the per-PM checkpoint (3d) list. To change which forum articles a PM sees, edit the manifest tables — not the script. Only the non-forum data (`PHASE3A_ARTICLES`, `PHASE3A_PM_ARTICLES`, `FORUM_UPDATE_CRITICAL`, `PHASE4_*`, `MANIFEST_PM_INPUT_FLAGS`) remains in-script. The script prints an **UNASSIGNED** warning for any manifest forum row whose PM cell matches no roster PM (currently rank 146 `Domo-Certification-Exam-Logistics.mdx` — "Domo University / Enablement", no product PM; needs a human ownership decision before Phase 4.5).

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

## Phase 3a — Complete ✅ (2026-07-14)

All 29 synthesizable articles were written and registered in docs.json. MCP articles were also extracted from the Domo AI group into their own sibling MCP group.

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

## PM Input Required (Phase 4.5 PM Brief Items)

These 4 articles need PM input before they can be written. They are **not blocking Phase 3a-Forum** — they will appear as `[pm-input]` items in the per-PM Phase 4.5 meeting briefs so they can be addressed during PM review meetings.

In addition, the items below were flagged during article writing and need specific PM answers before the articles can be finalized.

| Article | What PM needs to provide | PM |
|---------|--------------------------|-----|
| `How-Data-Flows-Through-Domo.mdx` | Canonical end-to-end pipeline narrative; sign off on how connect → prepare → analyze → share → govern is described | TBD |
| `Choose-the-Right-Data-Prep-Tool.mdx` | Positioning: when to use Magic ETL vs SQL DataFlow vs Python/R vs Data Models | Andrea Henderson |
| `Understand-DataSet-Joins-and-Relationships.mdx` | Decision guidance: when to use ETL joins vs Data Models vs DataFlows | Phil Fuchs / Andrea Henderson |
| `Domo-for-Mobile-Overview.mdx` | Confirm current mobile feature scope before writing overview | TBD |
| `Beast-Mode-Window-Functions.mdx` | Confirm the supported workaround for filtering on window function results (options: materialize in Magic ETL, restructure logic to avoid post-aggregation filter, other?) — replace FAQ placeholder once confirmed | Phil Fuchs |
| `Beast-Mode-Window-Functions.mdx` | Awareness: new article published covering RANK/DENSE_RANK, LAG/LEAD, running totals, Top N + Others — request review for accuracy and completeness | Phil Fuchs |
| Getting Started articles (all 4 role variants) | Confirm correct eLearning course URLs per role — all 4 articles currently link to the same `data-consumer-training` URL which is likely wrong for Admins, App Builders, Developers | Education team / PM TBD |
| `Workflows-Write-Data-Back.mdx` | Confirm exact write-back action names and configuration steps (append / multiline-append): how values + delimiters are entered, how a list of rows maps to the write action, how to create a new DataSet as the target — replace the `[pm-input]` block with a step-by-step section | Ryan Despain |
| `Activity-Log-Event-Reference.mdx` | Provide the complete enumerated Activity Log event glossary with precise definitions (VIEWED vs EXPORTED vs DOWNLOADED, Shared/Added/Access Granted, FILE/FILE_REVISION/ACTIVITY_LOG_CSV object types); confirm canonical **View Activity Logs** grant wording | Dan Brinton |
| `Restore-a-Deleted-Dashboard.mdx` | Confirm the backup retention window for deleted dashboards and the exact Support recovery path; confirm card-fate behavior when a dashboard is deleted | Dan Brinton |

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
| 1 | `Beast-Mode-Window-Functions.mdx` | ✅ **Done 2026-07-15** — RANK/DENSE_RANK, LAG/LEAD, SUM(SUM(x)) OVER running totals, Top N + Others; filter limitation noted; PM brief item logged for Phil Fuchs |
| 6 | `Workflows-Write-Data-Back.mdx` | ✅ **Done 2026-08-04** — DataSet vs AppDB destination, append vs replace, credit-efficient batching, dynamic rows; `[pm-input]` Ryan Despain for exact action config |
| 7 | `Activity-Log-Event-Reference.mdx` | ✅ **Done 2026-08-04** — entry structure, Type/Event/Object model, card-view semantics, analysis over time; `[pm-input]` Dan Brinton for full event glossary |
| 9 | `Restore-a-Deleted-Dashboard.mdx` | ✅ **Done 2026-08-04** — no self-service restore, Support recovery path, parent-deletes-subpages, prevention; `[pm-input]` Dan Brinton for retention window |
| 11 | `Beast-Mode-for-Spreadsheet-Users.mdx` | ✅ **Done 2026-08-04** — IF→CASE, SUMIF/COUNTIF→SUM(CASE), VLOOKUP→ETL join, no-stacking guidance |

#### High new (37 articles)

| Rank | Suggested filename | Topic summary |
|------|--------------------|---------------|
| 13 | `Workflows-Package-Administration.mdx` | Domo Users / DataSet package functions: assign roles, manage owners, set attributes via Workflows |
| 14 | `Dataset-Column-Rename-Impact.mdx` | Renaming a dataset/dataflow column silently breaks card filters, sorts, and downstream references — safe rename procedure |
| 17 | `Embed-Domo-in-Third-Party-Platforms.mdx` | Confluence, NetSuite, HubSpot, SharePoint, Salesforce embed methods and iframe constraints |
| 21 | `Filter-Funnel-and-PDP-Shield-Icons.mdx` | Hiding/showing the filter funnel and PDP shield on cards; page-variable behavior; Admin setting |
| 22 | `Filter-Null-and-Empty-Values.mdx` | NULL vs empty string; IS NULL / IS NOT NULL filter; NOT IN behavior; Beast Mode IFNULL workarounds |
| 25 | `Card-Refresh-Timing-After-Dataset-Update.mdx` | How long cards take to reflect dataset changes; cache warm-up; force-refresh approach |
| 26 | `DomoStats-vs-Governance-Datasets-Connector.mdx` | When to use DomoStats connector vs Domo Governance Datasets connector; field-level reference; deprecation status |
| 27 | `Trigger-Workbench-from-External-Scripts.mdx` | `wb.exe` CLI command syntax; triggering a Workbench job from Task Scheduler or CI scripts |
| 28 | `Embedded-Dashboard-Unfiltered-Data-Flash.mdx` | Why embedded/public-share dashboards briefly show unfiltered data on load; SSO and PDP timing fix |
| 32 | `Connect-Unsupported-Data-Sources.mdx` | No native connector options: JSON No Code, HTTP connector, SFTP, Workbench ODBC, custom connector builder |
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
| 139 | `Choose-How-to-Share-Outside-Domo.mdx` | Decision guide: embed types vs publication groups vs Domo Everywhere vs scheduled reports |
| 142 | `Choose-a-Cloud-Data-Warehouse.mdx` | CDW comparison for Domo; Cloud Amplifier cost/credit consumption guide |
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

## Phase 3c — Main Branch Content Sync

**Runs after:** Phase 3b and 3b-Forum (all article writing complete)
**Runs before:** Phase 4 (retirement/archive decisions)

The restructure branch (`update/fullRestructure`) has been diverging from `main` for months. During that time, new articles have been published and existing articles have been updated on `main`. Phase 3c ensures the restructure does not lose that new content — while preserving every rewrite, reorganization, and structural improvement made in the restructure branch.

**This is NOT a merge.** Do not run `git merge main`. Merging main back in would overwrite restructure rewrites with original pre-restructure versions. The goal is to surgically apply the new *content* without restoring old *structure*.

### Step-by-step procedure

**1. Find the divergence point**
```bash
git merge-base update/fullRestructure main
```
This gives the commit SHA where the branches last shared history. Call it `<BASE>`.

**2. List all files changed on main since divergence**
```bash
git log <BASE>..main --name-only --pretty=format: -- s/article/ s/topic/ | sort -u | grep '\.mdx$'
```
This lists every article file that has been added or modified on main after the branch cut.

**3. Categorize each changed file**

For each file in the list, determine which category it falls into:

| Category | Condition | Action |
|----------|-----------|--------|
| **New article** | File exists on `main` but not in the restructure branch | Cherry-pick the new file into `s/article/` and register it in `docs.json` under the appropriate pillar (use the same IA-spec pillar assignment logic from Phase 2) |
| **Content update to an unrewritten article** | File exists in both branches; the restructure branch version is essentially the same as the pre-restructure version | Directly apply the main-branch version — no restructure rewrite conflicts |
| **Content update to a rewritten article** | File exists in both; the restructure branch has a significant rewrite | Manually review the main-branch diff (`git diff <BASE>..main -- <file>`) and incorporate only the factual changes (new steps, corrected info, added features) into the rewritten version |
| **Structural change only** | File was reorganized or renamed on main but not content-updated | Skip — restructure nav and slugs take precedence |

**4. Commands to inspect each file's diff**
```bash
# See what changed on main for a specific file:
git diff <BASE>..main -- s/article/FileName.mdx

# See the current main version:
git show main:s/article/FileName.mdx

# Cherry-pick a net-new file from main:
git checkout main -- s/article/NewFile.mdx
```

**5. Register new articles in docs.json**
For each net-new article cherry-picked from main, use the `add-to-nav` skill to place it in the correct pillar group. Do not add it to the old flat nav structure — place it in the restructure's 11-pillar IA.

**6. Update the RESTRUCTURE-MANIFEST.md**
Log each synced file with disposition `main-sync` so the Phase 9 audit can account for it.

### What to watch for

- Articles on `main` may have been added with numeric filenames (e.g., `000042925394.mdx`). These should be cherry-picked as-is now and renamed during Phase 6 along with everything else.
- New articles on `main` that fall into a Phase 3a/3b topic area (gap already addressed by the restructure) should be reviewed: if the restructure's new article already covers the content, the main-branch article is a duplicate candidate for Phase 4 consolidation.
- If `docs.json` on `main` has nav changes: extract only the new article registrations (not the nav structure), since the restructure's nav structure is the one being built.

### Two-sync strategy + parity system (decided 2026-08-20)

Main keeps moving while the restructure runs, so Phase 3c happens **twice**:

- **Sync #1 — now (2026-08-20).** Clear the accumulated backlog while filenames on both branches still match (numeric IDs), so reconciliation is filename-based and conflicts are minimal.
- **Sync #2 — immediately before the final merge**, per decision. By then Phase 6 will have **renamed most files** (numeric ID → human slug), so filename-based matching no longer works. Sync #2 relies on the **parity system** below.

**Parity system (for sync #2, post-rename):** the immutable key is the **numeric KB article ID** (today's filename stem; `main` never renames, so it uses this ID forever). Two sources translate an ID to its current restructure location and disposition:

1. **Frontmatter ID stamp — HARD DEPENDENCY, must run BEFORE Phase 6.** Before any file is renamed, stamp each article's original numeric ID into its frontmatter (e.g. `legacy_id: "000005874"`). The filename stem *is* the ID, so this is a trivial deterministic bulk pass. After this, identity lives *inside* the file and survives any rename — a grep finds "which file is 000005874" regardless of its new slug. **If Phase 6 renames files without this stamp first, the parity system breaks.** Add this as a Phase 6 prerequisite step.
2. **Manifest disposition map.** `RESTRUCTURE-MANIFEST.md` records every article's fate (renamed / merged / split / archived / deleted) with source→target. Generate a machine-readable map from it to *route* each main change, not just locate it.

**Sync #2 procedure:** `git diff <sync#1-point>..origin/main` → main's changed/added/deleted files by numeric ID → resolve each via frontmatter ID + manifest map → renamed/kept = 3-way apply; merged/split = route to target(s) + human review; archived/deleted = surface for human call; main-added = import + nav. Delta is only what main changed since sync #1, so it stays small.

### Sync #1 execution log (2026-08-20)

Divergence base: `a4dd80c2` (2026-07-14). Main delta since: 432 commits; **87 `s/article`** (15 new, ~68 clean edits, 2 conflicts, 1 delete, 1 case-rename), 16 `portal`, 80 `images/kb`, 1 `snippets`, `docs.json`.
- **2 true conflicts** (main + restructure both changed): `000005179.mdx` (Manage Workflows — edited in High batch), `360043437093.mdx` → 3-way merge.
- **1 delete** `000005946.mdx`; **1 case-rename** `Microsoft-Sharepoint-Connector` → `Microsoft-SharePoint-Connector` (macOS case-collision hazard — handle with `git mv`/explicit checkout).
- 15 new articles need import + nav placement in the 11-pillar IA.

---

## Phase 4 — Inputs and Pre-Work

Phase 4 has not started, but the Support KB Audit (`KB Audit Results.csv`, completed 2026-04-28) provides a confirmed retirement hit list that should be used directly as the Phase 4 execution plan for several categories. Do not re-run agent retirement analysis for these — the Audit already did it.

For lifecycle state definitions and YAML/callout specs, see **Product Lifecycle Standards** above.

**Confirmed retirement batches ready for Phase 4:**

| Batch | Count | Lifecycle State | Action |
|-------|-------|-----------------|--------|
| Workbench 4 articles | 37 (118 total Workbench articles flagged in Audit) | **Legacy** | Move to Archive group; add `<LegacyNote />`; D1 confirmed |
| DataFusion articles | 11 | **Retired** | Remove from nav; metadata only; no callout |
| Old Magic ETL tile articles | 15 to retire + 1 Keep | **Retired** | Remove from nav; keep 1 (`Create a Recursive/Snapshot Old Magic ETL DataFlow`) |
| Defunct-service connectors | 111 confirmed dead-service articles (verified via Audit summaries) | **Retired** | Remove from Connector Library nav |
| Release notes pre-2022 (all languages) | Large volume (all locales) | **Retired** | Remove from nav; collapse into Archive group in Phase 7 |
| CourseBuilder articles | 16 (pending D10 PM confirmation) | **Retired** (pending) | Remove from nav if PM confirms retired (D10) |

**Urgent pre-Phase 4 fix:** `Snowflake Connector` and `Snowflake Unload V2 Connector` documents key-pair/password auth that Snowflake retired November 2025. Customers are actively failing. Fix these now with `update-kb-article` before Phase 4 starts.

See `Support KB Audit Shared GAP Analysis.md` (repo root) for the full analysis and per-item rationale.

---

## Phase 4.6 — Lifecycle Status Application

**Runs after:** Phase 4.5 (all PM lifecycle confirmations received)
**Runs before:** Phase 5 (interlinking requires stable article states)

With PM sign-off complete, this phase stamps every article with its confirmed lifecycle status and puts the nav in the correct state for the lifecycle system.

### Step 1 — Bulk-add `status: "active"` to all articles without a status field

Every article in `s/article/` that does not already have a `status:` field in its frontmatter gets `status: "active"` added. This is a mechanical find-and-update pass — no content changes.

```bash
# Find articles missing a status field
grep -rL "^status:" s/article/*.mdx
```

For each file in that list, insert `status: "active"` into the frontmatter directly below `excerpt:`. A script is the right tool here — do not manually edit 1,800+ files.

### Step 2 — Apply PM-confirmed non-Active states

Using the completed `RESTRUCTURE-TASKS.md` checklist (all `[deprecated]`, `[legacy]`, `[sunset]`, `[retired]` items checked off by PMs), apply the confirmed lifecycle state to each article:

**For each Deprecated article:**
1. Add `status: "deprecated"` and `tag: "Deprecated"` to frontmatter
2. Add `import { DeprecatedNote } from '/snippets/DeprecatedNote.mdx';` below the frontmatter
3. Place `<DeprecatedNote replacement="..." />` as the first body element (before `## Intro`)
4. Article stays in its current nav group — no docs.json move needed

**For each Legacy article:**
1. Add `status: "legacy"` and `tag: "Legacy"` to frontmatter
2. Add `import { LegacyNote } from '/snippets/LegacyNote.mdx';` below the frontmatter
3. Place `<LegacyNote replacement="..." />` as the first body element
4. Move the article's entry in `docs.json` from its current pillar group to the Archive group at the bottom of the KB tab

**For each Sunset article:**
1. Add `status: "sunset"`, `tag: "Sunset"`, and `sunset_date: "YYYY-MM-DD"` to frontmatter
2. Add `import { SunsetNote } from '/snippets/SunsetNote.mdx';` below the frontmatter
3. Place `<SunsetNote date="Month DD, YYYY" replacement="..." />` as the first body element
4. Move the article's entry in `docs.json` to the Archive group

**For each Retired article:**
1. Add `status: "retired"` to frontmatter
2. Remove the article's entry from `docs.json` nav entirely — the file stays in the repo
3. No callout needed

### Step 3 — Verify Archive group structure in docs.json

After all moves, confirm the Archive group at the bottom of the KB tab contains exactly the Legacy and Sunset articles (and only those). Retired articles should have no nav entry. Deprecated articles should appear in their pillar groups.

### Step 4 — Update RESTRUCTURE-MANIFEST.md

For every article whose status changed in this phase, update its disposition record to reflect its final lifecycle state.

---

## Phase 5 — Interlinking

**Runs after:** Phase 4.6 (all lifecycle states applied and nav updated)

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
- Verify Archive group is at the bottom of the KB tab containing only Legacy- and Sunset-state articles
- Verify Legacy articles have `tag: "Legacy"` and Sunset articles have `tag: "Sunset"` sidebar labels
- Verify Deprecated articles have `tag: "Deprecated"` and remain in their normal pillar group (not in Archive)
- Verify Retired articles have `status: "retired"` and are absent from docs.json nav entirely
- Verify all Phase 3a stub files have been replaced with real content
- Verify localized tab structures mirror the English KB structure

---

## Phase 8 — Style Guide & Template Update

**Runs after:** Phase 7

Update `Domo-KB-Style-Guide.mdx` and `New-Article-Template.mdx` to reflect every structural standard introduced by this restructure.

**`Domo-KB-Style-Guide.mdx` — expected additions:**
- **Product Lifecycle States** — the five states (Active, Deprecated, Legacy, Sunset, Retired), full YAML spec for each, when to use each state, snippet usage for DeprecatedNote/LegacyNote/SunsetNote, nav placement rules (Deprecated stays in pillar; Legacy/Sunset move to Archive group; Retired not in nav), and PM sign-off requirements
- **Wheel-and-spoke product group structure** — standard pattern: one Overview/hub article + How-To articles + Reference articles (optional) + FAQ (in Accordion at bottom of hub); typical article counts per product group
- **Pillar hub articles** — what they are, when a new product area needs one, how they link to product group articles
- **New article types added by this restructure** — "What is X?" overview articles, pillar hub articles, getting-started-for-role articles; what makes each distinct
- **AI callout pattern** — when to add `<Tip>**Try it with AI:**...`; links to AI & Data Science pillar articles
- **Cross-pillar linking conventions** — KB ↔ Developer Portal cross-links; how to reference portal articles from KB

**`New-Article-Template.mdx` — expected additions:**
- Optional `status:` YAML field with all five lifecycle values documented in a comment block
- All three lifecycle snippet imports (DeprecatedNote, LegacyNote, SunsetNote) commented out at the top — uncomment the applicable one when needed
- Minor: verify existing template structure still matches the updated style guide

Run a diff of the current template against the style guide after Phase 7 to confirm exactly what needs updating — do not over-engineer this step.

**`CLAUDE.md` — review and update:**
CLAUDE.md is the AI-facing project instructions. After the restructure is complete, it references file paths, nav structure, and workflows that will have changed. Review and update:
- File path references (e.g., `s/article/` numeric IDs now have slug equivalents; new Phase 3a hub article slugs added)
- Architecture section — update to reflect the pillar-based navigation structure in docs.json and the addition of hub articles in `s/article/`
- Navigation section — update to reflect that docs.json now uses pillar groups rather than the old flat KB structure
- Any script references that have moved (if `scripts/output/` contents are now under `restructure/`)
- Add guidance on the five product lifecycle states and when to use each
- Remove references to planning files that have moved to `restructure/`

CLAUDE.md stays at the repo root (not moved to `restructure/`) — it must be at root to be picked up by Claude Code.

---

## Phase 9 — Restructure Artifacts Cleanup

**Final phase — runs after Phase 8**

### Step 9.1 — Generate Final Disposition Report

Before moving any files, generate the **Article Disposition Report** from `RESTRUCTURE-MANIFEST.md`. This is the audit document used to verify that every article in the pre-restructure KB has been accounted for — nothing dropped, nothing accidentally deleted.

The report should list every article (pre-restructure + net-new) with:
- **Filename** and **Title**
- **Disposition**: `new` | `same-regrouped` | `updated` | `split` | `merged-into` | `main-sync` | `deprecated` | `legacy` | `sunset` | `retired` | `deleted`
- **Source articles** (for new/updated articles: what they were synthesized from)
- **Target articles** (for split/merged: where the content went)
- **Screenshot status**: `included` | `todo-markers-left` | `n/a`
- **Notes**: any PM-flagged items, fact-check TODOs, or open questions

Run a final human audit against this report before calling the restructure complete. Only after the audit is signed off should artifacts move to `restructure/`.

### Step 9.2 — Move Artifacts to `restructure/`

Move all planning and analysis artifacts generated during the restructure into a single folder named `restructure/` at the repo root. These files are not documentation — they are project records. Keeping them at the repo root clutters the working directory.

**Files to move to `restructure/`:**
- `KB-RESTRUCTURE-PLAN.md`
- `RESTRUCTURE-PROGRESS.md`
- `RESTRUCTURE-IA-SPEC.md`
- `RESTRUCTURE-MANIFEST.md`
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
| 2026-07-14 | Archive vs Legacy vs Deleted distinction defined | Three explicit categories for content removal: (1) Deleted — restructured into other content, file removed; (2) Archived — genuinely retired, no living successor, file kept in Archive nav group with `archived: true` + `<ArchivedNote />`; (3) Legacy — feature still functional but unmaintained, file stays in pillar with `legacy: true` + `tag: "Legacy"` + `<LegacyNote />`. PM sign-off required for Legacy marking. **Superseded 2026-07-16 — see five-state lifecycle system.** |
| 2026-07-14 | Legacy frontmatter approach confirmed | Mintlify native `tag:` frontmatter field renders a visible sidebar label — use `tag: "Legacy"` for legacy articles and `tag: "Archived"` for archived articles. Custom fields `legacy: true` / `archived: true` serve tooling. `<LegacyNote />` and `<ArchivedNote />` snippets (to build at Phase 4 time) provide body-level callouts. Do NOT use `deprecated: true` for Legacy articles — "deprecated" implies a removal date which Legacy explicitly does not. **Superseded 2026-07-16 — see five-state lifecycle system.** |
| 2026-07-14 | Phase 6 (Slug Rename) significantly enhanced | Original plan was: rename files, rebuild nav. New plan adds 4 sub-steps: (6.1) generate slug-rename-map.csv; (6.3) rename localized files (ja/de/es/fr) to English slug for exact filename parity; (6.5) add permanent 308 redirects to docs.json for all renamed paths; (6.6) update all internal links in the repo using the CSV mapping. |
| 2026-07-14 | Phase 8 (Style Guide + Template + CLAUDE.md) added | Final human-facing standards update: Domo-KB-Style-Guide.mdx gets Archive/Legacy standards, wheel-and-spoke product group structure, pillar hub article guidance, AI callout pattern, and cross-pillar linking conventions. New-Article-Template.mdx gets legacy/archived YAML fields. CLAUDE.md gets full review and update to reflect the restructured repo — stays at root (not moved to restructure/). |
| 2026-07-14 | Phase 9 (Restructure Artifacts Cleanup) added | All planning/analysis/tracking artifacts (KB-RESTRUCTURE-PLAN.md, RESTRUCTURE-PROGRESS.md, RESTRUCTURE-IA-SPEC.md, RESTRUCTURE-TASKS.md, slug-rename-map.csv, ownership reference, audit/gap files, pm-review-briefs/, scripts/output/) move to restructure/ folder at repo root after Phase 8. Keeps live documentation directory clean post-restructure. |
| 2026-07-14 | RESTRUCTURE-TASKS.md granular checklist system defined | Generated at Phase 4.5 by updated build-pm-review-briefs.py. Organized Pillar → Product Group → discrete tasks with type tags: [new-article], [update], [archive], [legacy], [deleted], [pm-input], [decision], [fact-check]. This is the working document for PM meetings and post-PM execution — query it at any time for remaining tasks by pillar, PM, or type. **Updated 2026-07-16 — task tags expand to include [deprecated], [sunset], [retired] per five-state lifecycle system.** |
| 2026-07-14 | Restructure scope confirmed: s/article/ only; portal/ is out of scope | Phase 3a article paths corrected from portal/ subdirectories to s/article/. The portal/ directory (Developer Portal) is entirely out of scope for this restructure — no new portal/ files, no portal/ nav changes. The only portal/ work is Phase 5 interlinking, which adds links FROM s/article/ how-tos TO existing portal/ pages. Phase 8 CLAUDE.md review language updated to remove incorrect portal/ references. Phases 1 and 2 were unaffected (already scoped to s/article/ throughout). |
| 2026-07-14 | D9 resolved — Manage Data pillar populated | 31 DataSet Management articles split: 20 → Manage Data (3 in "Data Center" group: Data Center Layout, Using the Data Warehouse, Understanding Connector Options; 17 in "DataSet Lifecycle" group: ownership, sharing, health, lifecycle how-tos). 5 pipeline articles stay in Prepare & Transform (DataSet Update Methods, DataFusion ×2, Enterprise Stacker, Advanced Tools Launch Center). 1 (PDP) → Administer & Govern > Governance. 2 developer tools (CLI, ODBC) → Develop & Integrate > APIs & SDKs. 1 (Migrate from Federated to Cloud) → Connect & Bring In Data > Cloud Data Warehouses. 2 visualization articles → Analyze & Visualize > Analyzer. `scripts/build_ia_spec.py` OVERRIDES section updated; Phase 2 re-run confirms 1,832/1,832 articles assigned. |
| 2026-07-16 | Five-state product lifecycle system replaces two-state Archive/Legacy | Previous system had only Archived and Legacy. New system: Active (metadata only, default), Deprecated (stays in normal nav, `tag: "Deprecated"`, `<DeprecatedNote />`), Legacy (Archive group, `tag: "Legacy"`, `<LegacyNote />`), Sunset (Archive group, `tag: "Sunset"`, `sunset_date:`, `<SunsetNote />`), Retired (not in nav, `status: "retired"`, no callout). All five use a canonical `status:` YAML field; Deprecated/Legacy/Sunset also get Mintlify `tag:` for sidebar labels and a snippet callout just below the title. Retired articles exist in repo but are unpublished. |
| 2026-07-16 | Phase 3c (Main Branch Content Sync) added | New phase runs after 3b/3b-Forum, before Phase 4. Purpose: find all new articles and content updates merged to main after the restructure branch diverged, and apply the new content without reverting restructure rewrites. Procedure: git merge-base to find divergence point; git log to list changed files; categorize each as net-new, unrewritten update, or rewritten-article update; cherry-pick or manually merge accordingly. Not a git merge. |
| 2026-07-16 | Workbench 4 reclassified: Archive → Legacy | Under the new lifecycle system, Workbench 4 maps to Legacy (still installed at some sites, WB5 is the replacement, no announced removal date). Will move to Archive group in nav with `<LegacyNote />` and `tag: "Legacy"`. |
| 2026-07-16 | DataFusion, old Magic ETL tile articles, defunct connectors reclassified: Archive → Retired | These features/services are completely gone — DataFusion discontinued, old tile UI replaced, third-party services shut down. Under the new lifecycle system they are Retired: `status: "retired"`, removed from nav entirely, no callout. |
| 2026-07-16 | Phase 4.6 (Lifecycle Status Application) added | New phase between 4.5 and 5. Bulk-adds `status: "active"` to every article without a status field; applies PM-confirmed Deprecated/Legacy/Sunset/Retired states (frontmatter + snippet imports + callout placement + docs.json nav moves); verifies Archive group contains only Legacy and Sunset articles. Must complete before Phase 5 so interlinking does not add Next Steps/Related links to articles that are about to be moved or removed from nav. |
| 2026-08-18 | PM-brief script refactored to read the manifest as source of truth | Pre-3b audit found the hardcoded `FORUM_NEW_CRITICAL`/`FORUM_NEW_HIGH`/`ARTICLE_CHECKPOINTS` in `build-pm-review-briefs.py` had drifted from `RESTRUCTURE-MANIFEST.md`: 11 Medium deferred gaps were absent entirely, 5 written articles were mis-framed as "cannot be written without input," `Find-Which-Dashboard` was missing, and `Restore-a-Deleted-Dashboard` was routed to the wrong PM (Chris Wright vs. Dan Brinton). Fix: deleted the hardcoded forum blocks; the script now parses the manifest's Phase 3a-Forum written table (→ Section 3b fact-check) and deferred table (→ Section 3c needs-input), and scans `s/article/*.mdx` for embedded `[pm-input]` markers (→ Section 3d checkpoints). Result verified: 14 written + 43 deferred parsed, 6 markers found, rank-146 orphan surfaced. Section 3 re-framed to separate "drafted, fact-check" from "cannot be written yet." |
