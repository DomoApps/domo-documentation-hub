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
