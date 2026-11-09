# PM Review Brief: Ken Boyer

**Prepared for:** KB Restructure PM Review Meeting
**Features owned:** AI Chat, AI Services, CLI, Documents-Filesets, Jupyter Notebooks
**Total articles in your area:** 56

> This document is your meeting guide. It shows how your content is being reorganized,
> which AI-generated articles need your fact-check, which articles need a dedicated
> info-gathering meeting before they can be written, and what changes are being made
> to your content area in response to Support KB Audit and community forum gap findings.

---

## 1. How Your Content Is Being Reorganized

The KB is moving from a flat feature encyclopedia to a story-driven structure organized
around **12 pillars** (user workflows). The table below shows where each of your feature
areas lands in the new structure.

| Feature | Articles | New Location |
|---------|----------|--------------|
| AI Chat | 1 | TBD — not yet mapped |
| AI Services | 41 | Pillar 9: AI & Data Science |
| CLI | 1 | Pillar 11: Develop & Integrate |
| Documents-Filesets | 8 | Pillar 9: AI & Data Science |
| Jupyter Notebooks | 5 | Pillar 9: AI & Data Science |

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

- [ ] **`000005849.mdx`**
  Confirm the FileSets file-download URL format and the exact steps to reference a FileSet image URL in App Studio image/gallery components (the referencing fix was reported in the community forum but is not yet documented). Synthesized from community forum reports; needs confirmation.

- [ ] **`36004740075.mdx`**
  Confirm the current write_dataframe type-handling behavior reported by users since 2023–2024: boolean columns landing as empty integer columns and Python date/datetime columns not writing correctly. Confirm whether astype(str) plus a downstream ETL input-type fix is the recommended workaround or whether a fix has shipped. Synthesized from community forum reports; needs confirmation.

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
| 5 | Fact-check `Extract-Data-from-PDFs-with-Domo-AI.mdx` (Rank 159 community request) | Fact-check | 20–30 min |
| 6 | Supply info to write `AI-Chat-API-Session-ID.mdx` (Rank 144) | Info meeting | 30 min |
| 7 | Supply info to write `Private-Embed-Token-Validation-Errors.mdx` (Rank 161) | Info meeting | 30 min |
| 8 | **Open placeholder in `000005539.mdx`:** Confirm the exact in-chat workaround for reading an AI Chat v1 chart's inferred  | **Answer required** | 15–30 min |
| 9 | **Open placeholder in `000005849.mdx`:** Confirm the FileSets file-download URL format and the exact steps to reference a | **Answer required** | 15–30 min |
| 10 | **Open placeholder in `36004740075.mdx`:** Confirm the current write_dataframe type-handling behavior reported by users sin | **Answer required** | 15–30 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
