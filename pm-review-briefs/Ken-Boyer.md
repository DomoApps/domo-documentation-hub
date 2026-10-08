# PM Review Brief: Ken Boyer

**Prepared for:** KB Restructure PM Review Meeting
**Features owned:** AI Services, CLI, Documents-Filesets, Jupyter Notebooks
**Total articles in your area:** 43

> This document is your meeting guide. It shows how your content is being reorganized,
> which AI-generated articles need your fact-check, which articles need a dedicated
> info-gathering meeting before they can be written, and what changes are being made
> to your content area in response to Support KB Audit and community forum gap findings.

---

## 1. How Your Content Is Being Reorganized

The KB is moving from a flat feature encyclopedia to a story-driven structure organized
around **11 pillars** (user workflows). The table below shows where each of your feature
areas lands in the new structure.

| Feature | Articles | New Location |
|---------|----------|--------------|
| AI Services | 29 | Pillar 8: AI & Data Science |
| CLI | 1 | Pillar 10: Develop & Integrate |
| Documents-Filesets | 8 | Pillar 8: AI & Data Science |
| Jupyter Notebooks | 5 | Pillar 8: AI & Data Science |

### Notable Navigation Changes

- **Develop & Integrate (Pillar 10):** Currently only 5 articles — severely thin. This pillar cannot tell a story until Phase 3a content is written. The pillar may largely function as an entry ramp to the Developer Portal (developer.domo.com).

- **D6 scope question:** Confirm: should Develop & Integrate be KB how-tos, or primarily a link-out to developer.domo.com?

---

## 2. AI-Generated Articles — Your Fact-Check Required

These articles will be synthesized by AI from existing KB content in Phase 3a.
**They need your review before publishing.** Please read the draft and verify the
key claims listed — especially anything about product behavior, limitations, or
recommended patterns.

| # | Article | Synthesized From | Key Claims to Verify |
|---|---------|------------------|---------------------|
| 1 | `Getting-Started-for-Developers.mdx` (Pillar 1) | API articles, MCP article, Access Tokens | Developer entry points, API auth methods, available SDKs, MCP integration availability |
| 2 | `What-is-Domo-AI.mdx` (Pillar 8) | Domo AI FAQ, AI Playground, AI articles | AI Chat capabilities, AI Playground, available AI models, what's GA vs Beta |
| 3 | `AI-and-Data-Science-Overview.mdx` (Pillar 8) | All AI / DomoStats / Jupyter articles | Full AI toolbox: AI Chat, AutoML, Jupyter, DomoStats — verify current feature availability |
| 4 | `Develop-and-Integrate-Overview.mdx` (Pillar 10) | Existing 5 API articles | Developer entry points, API vs SDK, auth options, MCP integration |

---

## 3. New Forum-Gap Articles and Open Placeholders

New articles in your area from the community-forum gap analysis (and the original
restructure plan). Some are **already drafted and need your fact-check**; others
**cannot be written until you supply information**. The two are separated below so
it's clear which is which.

### 3b. Forum-Gap Articles Already Drafted — Fact-Check Required

These articles have been **written** in response to the highest-demand community
forum gaps. Please read each draft and verify accuracy. A ⚠️ flag means the draft
also contains an open `[pm-input]` placeholder — see Section 3d for the exact ask.

| Rank | Article | What Was Synthesized / What to Verify |
|------|---------|---------------------------------------|
| 89 | `Retrieve-Dataset-Source-Query-via-API.mdx` — *Retrieve a Dataset's Source Query with the API* | Synthesized from portal Datasets API + overview; metadata→streamId→stream configuration→query chain. Links to Developer Portal reference |
| 159 | `Extract-Data-from-PDFs-with-Domo-AI.mdx` — *Extract Data from PDFs and Images with Domo AI* ⚠️ | Synthesized from 000005279 (Image-to-Text) + 000005369 (Workflows AI Service Layer) + 000005849 (FileSets). 2× `[pm-input]` Ken Boyer: Magic ETL AI-tile path + S3/SFTP batch pipeline; scanned-PDF / multi-column table extraction limits |

### 3c. Forum-Gap Articles Awaiting Your Input — Cannot Be Written Yet

These forum gaps **cannot be written without your input** — the KB has no source
material and the mechanics are Domo-proprietary. A short dedicated meeting (or an
async written answer) is needed before drafting can begin.

| Rank | Intended Article | What You Need to Supply |
|------|------------------|-------------------------|
| 144 | `AI-Chat-API-Session-ID.mdx` | Deferred to PM brief (re-homed from dropped, 2026-08-28): needs the Ask Chat / AI API session-ID sequence + client-UUID canned-refusal behavior. Ken (AI Services / APIs) to confirm KB-vs-Developer-Portal scope and supply the mechanics. |
| 161 | `Private-Embed-Token-Validation-Errors.mdx` | Deferred to PM brief (re-homed from dropped, 2026-08-28): valid-token 302-to-login causes, client ID/secret + authorized-domains, token regen after domain change. Ken (APIs) to confirm KB-vs-Developer-Portal scope and supply the mechanics. |

### 3d. Open Article Placeholders — Your Answer Required

The items below are open `[pm-input]` placeholders where specific information from
you is needed before the content can be finalized. Each is a checkbox — check it
off once you've provided the answer.

- [ ] **`000005539.mdx`**
  Confirm the exact in-chat workaround for reading an AI Chat v1 chart's inferred configuration (forum reports reference a "Show Chart Controls" option) and the exact path to launch the AI Content Builder Agent (forum reports reference the Apps dropdown). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005561.mdx`**
  Confirm the exact procedure to commit a synonym entry (for example, the keystroke that creates a synonym pill), whether there is a known limitation where Edit All drops changes when editing more than a few columns at once, and whether a Workflow-based approach for bulk AI Dictionary updates is supported. synthesized from community forum reports; needs confirmation.

- [ ] **`000005561.mdx`**
  Confirm whether AI Readiness / AI Dictionary metadata (DataSet context, synonyms, and column settings) propagates to a subscriber instance through a Domo Everywhere publication or refresh, and whether or how AI Chat must be separately enabled on the subscriber instance. synthesized from community forum reports; needs confirmation.

- [ ] **`000005849.mdx`**
  Confirm the FileSets file-download URL format and the exact steps to reference a FileSet image URL in App Studio image/gallery components (the referencing fix was reported in the community forum but is not yet documented). Synthesized from community forum reports; needs confirmation.

- [ ] **`36004740075.mdx`**
  Confirm the enablement-request process for non-standard or student instances, where Jupyter Workspaces may not be provisioned by default. Synthesized from community forum reports; needs confirmation.

- [ ] **`36004740075.mdx`**
  Confirm the current write_dataframe type-handling behavior reported by users since 2023–2024: boolean columns landing as empty integer columns and Python date/datetime columns not writing correctly. Confirm whether astype(str) plus a downstream ETL input-type fix is the recommended workaround or whether a fix has shipped. Synthesized from community forum reports; needs confirmation.

- [ ] **`36004740075.mdx`**
  Confirm the current R version shipped in Jupyter Workspaces (community reports cite R 4.1) and the list of supported/pre-installed kernels and packages. Synthesized from community forum reports; needs confirmation.

- [ ] **`Create-and-Use-Data-Models.mdx`**
  Confirm the deployment limitations reported for Data Models: models cannot be promoted through a repository or Sandbox and are not selectable in data-source mapping, so a model must be recreated manually in each development, test, and production environment. Deployment support is tracked as a feature request. Synthesized from community forum reports; needs confirmation.

- [ ] **`Create-and-Use-Data-Models.mdx`**
  Confirm the trigger conditions and any workaround for the "Bad Request" error affecting Data Models. Synthesized from community forum reports; needs confirmation.

- [ ] **`Create-and-Use-Data-Models.mdx`**
  Confirm the Analyzer date-field errors reported for Data Models (filter-by-date and summary number / Graph By) and document how to set up date fields in the model so they work in Analyzer. Synthesized from community forum reports; needs confirmation.

- [ ] **`Extract-Data-from-PDFs-with-Domo-AI.mdx`**
  confirm the remaining invocation paths so they can be documented: (1) whether Image-to-Text is available as a Magic ETL AI tile (the Magic ETL AI article documents only Text Generation, AI Forecasting, and Model Inference tiles — no Image-to-Text tile); (2) the supported end-to-end pattern for batch-processing PDFs pulled from S3 or SFTP through Image-to-Text. Add sections for each once confirmed.

- [ ] **`Extract-Data-from-PDFs-with-Domo-AI.mdx`**
  confirm and document the extraction limitations: whether scanned/flattened image-only PDFs and complex multi-column layouts extract cleanly as tables vs. plain text, and the recommended source-preparation guidance. Replace this section with the confirmed limits.

---

## 4. Changes Flagged by Support Gap Integrations

Two gap-fill analyses have been integrated into the restructure plan. This section
shows what changes are planned in your content area and what fact-check input reduces
hallucination risk in the updated articles.

### 4a. Support KB Audit Findings (Phase 4)

_No Support KB Audit retirements are currently assigned to your area._

### 4b. Community Forum Gap Analysis — Update Targets

**High priority update targets** (3 articles in your area):

| Rank | Score | Topic | Affected Area | Specific Addition Needed |
|------|-------|-------|---------------|--------------------------|
| 96 | 61.8 | AppDB collection-to-dataset sync: forcing sync, sync mode, and outages | APIs | Documentation on AppDB sync mechanics: syncEnabled in manifest, Scheduled vs API Update sync modes a |
| 98 | 61.5 | Programmatic / PDP filtering for embedded dashboards and per-user data | APIs | Documentation on secure per-user filtering for embeds: programmatic filters vs pfilters (and why pfi |
| 104 | 60.7 | AI Readiness / AI Dictionary not saving (synonyms, multiple edits) and Beast Mod | Domo AI / AI Readiness & Dictionary | Document the correct procedure to add/save synonyms and definitions in the AI Dictionary (and curren |

---

## Quick Actions Summary

A prioritized list of everything this document is asking of you:

| # | Action | Type | Est. Effort |
|---|--------|------|------------|
| 1 | Read and fact-check `Getting-Started-for-Developers.mdx` | Fact-check | 30–45 min |
| 2 | Read and fact-check `What-is-Domo-AI.mdx` | Fact-check | 30–45 min |
| 3 | Read and fact-check `AI-and-Data-Science-Overview.mdx` | Fact-check | 30–45 min |
| 4 | Read and fact-check `Develop-and-Integrate-Overview.mdx` | Fact-check | 30–45 min |
| 5 | Fact-check `Retrieve-Dataset-Source-Query-via-API.mdx` (Rank 89 community request) | Fact-check | 20–30 min |
| 6 | Fact-check `Extract-Data-from-PDFs-with-Domo-AI.mdx` (Rank 159 community request) | Fact-check | 20–30 min |
| 7 | Supply info to write `AI-Chat-API-Session-ID.mdx` (Rank 144) | Info meeting | 30 min |
| 8 | Supply info to write `Private-Embed-Token-Validation-Errors.mdx` (Rank 161) | Info meeting | 30 min |
| 9 | **Open placeholder in `000005539.mdx`:** Confirm the exact in-chat workaround for reading an AI Chat v1 chart's inferred  | **Answer required** | 15–30 min |
| 10 | **Open placeholder in `000005561.mdx`:** Confirm the exact procedure to commit a synonym entry (for example, the keystrok | **Answer required** | 15–30 min |
| 11 | **Open placeholder in `000005561.mdx`:** Confirm whether AI Readiness / AI Dictionary metadata (DataSet context, synonyms | **Answer required** | 15–30 min |
| 12 | **Open placeholder in `000005849.mdx`:** Confirm the FileSets file-download URL format and the exact steps to reference a | **Answer required** | 15–30 min |
| 13 | **Open placeholder in `36004740075.mdx`:** Confirm the enablement-request process for non-standard or student instances, wh | **Answer required** | 15–30 min |
| 14 | **Open placeholder in `36004740075.mdx`:** Confirm the current write_dataframe type-handling behavior reported by users sin | **Answer required** | 15–30 min |
| 15 | **Open placeholder in `36004740075.mdx`:** Confirm the current R version shipped in Jupyter Workspaces (community reports c | **Answer required** | 15–30 min |
| 16 | **Open placeholder in `Create-and-Use-Data-Models.mdx`:** Confirm the deployment limitations reported for Data Models: models cannot be pr | **Answer required** | 15–30 min |
| 17 | **Open placeholder in `Create-and-Use-Data-Models.mdx`:** Confirm the trigger conditions and any workaround for the "Bad Request" error af | **Answer required** | 15–30 min |
| 18 | **Open placeholder in `Create-and-Use-Data-Models.mdx`:** Confirm the Analyzer date-field errors reported for Data Models (filter-by-date  | **Answer required** | 15–30 min |
| 19 | **Open placeholder in `Extract-Data-from-PDFs-with-Domo-AI.mdx`:** confirm the remaining invocation paths so they can be documented: (1) whether Im | **Answer required** | 15–30 min |
| 20 | **Open placeholder in `Extract-Data-from-PDFs-with-Domo-AI.mdx`:** confirm and document the extraction limitations: whether scanned/flattened image | **Answer required** | 15–30 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
