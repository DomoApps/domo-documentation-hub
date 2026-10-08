# PM Review Brief: Mamta Bolaki

**Prepared for:** KB Restructure PM Review Meeting
**Features owned:** Domo Everywhere, Sandbox
**Total articles in your area:** 11

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
| Domo Everywhere | 9 | Pillar 7: Share & Collaborate |
| Sandbox | 2 | Pillar 9: Administer & Govern |

### Notable Navigation Changes

- **Domo Everywhere positioning:** Domo Everywhere content lives in Pillar 7 (Share & Collaborate) with its own sub-section. The embed framing (public vs. private, SSO + PDP interaction) should be consistent across all Domo Everywhere articles.

---

## 2. AI-Generated Articles — Your Fact-Check Required

These articles will be synthesized by AI from existing KB content in Phase 3a.
**They need your review before publishing.** Please read the draft and verify the
key claims listed — especially anything about product behavior, limitations, or
recommended patterns.

| # | Article | Synthesized From | Key Claims to Verify |
|---|---------|------------------|---------------------|
| 1 | `Domo-Sandbox-Overview.mdx` (Pillar 9) | Sandbox article, Linked Repositories | Sandbox capabilities, promotion workflow, environment types, linked repo feature |

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
| 139 | `Choose-How-to-Share-Outside-Domo.mdx` — *Choose How to Share Content Outside Domo* | Synthesized from 360043437993 + portal embed guides; public/private-embed/Publish/Edit-Experience decision matrix. Omitted unverifiable single-SSO-provider limit |

### 3c. Forum-Gap Articles Awaiting Your Input — Cannot Be Written Yet

These forum gaps **cannot be written without your input** — the KB has no source
material and the mechanics are Domo-proprietary. A short dedicated meeting (or an
async written answer) is needed before drafting can begin.

| Rank | Intended Article | What You Need to Supply |
|------|------------------|-------------------------|
| 17 | `Embed-Domo-in-Third-Party-Platforms.mdx` | Per-platform embed pattern + steps + limits for Confluence, NetSuite, HubSpot, SharePoint (esp. Confluence sandboxed-iframe selector/filter limitation); secure client ID/secret handling |
| 28 | `Embedded-Dashboard-Unfiltered-Data-Flash.mdx` | Embed load-sequence/permissions timing that briefly shows unfiltered data, generating-user permission dependency, mitigation, mobile rendering parity |

### 3d. Open Article Placeholders — Your Answer Required

The items below are open `[pm-input]` placeholders where specific information from
you is needed before the content can be finalized. Each is a checkbox — check it
off once you've provided the answer.

- [ ] **`360043437993.mdx`**
  Confirm whether private embed IDs/codes are intentionally user-specific (per-user rather than a single universal code) for security and audit purposes, and document the supported way to programmatically monitor embedded-page health: the embed load sequence, the stack?parts endpoint, TOE codes, and the 401 authentication errors users hit when calling it. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043437993.mdx`**
  Confirm the exact wording and behavior of the "You are editing content embedded in N instances" warning, including how the instance count is calculated and whether it counts public embeds, private embeds, and published subscriber instances. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043437993.mdx`**
  Confirm the specific browser and version behind this Private Network Access change (reported as Chrome 142), the Domo-supported remediation (open-in-new-tab vs. access-control headers), and which Domo surfaces such as Data Explorer can and cannot be loaded in an iFrame. Synthesized from community forum reports; needs confirmation.

- [ ] **`360045120554.mdx`**
  Confirm whether a DataSet's name or description can be changed at publish time (so it appears differently to subscribers), and whether there is a supported way to hide superfluous DataSets from subscribers while still powering published content. synthesized from community forum reports; needs confirmation.

- [ ] **`4403367344023.mdx`**
  Confirm the recommended DEV/PROD promotion pattern; whether App Studio global and page filters are excluded from promotion and the manual workaround to recreate them in the destination instance; how to make aesthetic-only dashboard changes without cloning every card and Beast Mode; and the lifetime of the developer/access token used with Sandbox. synthesized from community forum reports; needs confirmation.

- [ ] **`4403367344023.mdx`**
  Confirm the exact generic error text users see (reported as an "invalid content entity" / dependency error) and whether the non-specific messaging is a known defect being tracked. Synthesized from community forum reports; needs confirmation.

---

## 4. Changes Flagged by Support Gap Integrations

Two gap-fill analyses have been integrated into the restructure plan. This section
shows what changes are planned in your content area and what fact-check input reduces
hallucination risk in the updated articles.

### 4a. Support KB Audit Findings (Phase 4)

_No Support KB Audit retirements are currently assigned to your area._

### 4b. Community Forum Gap Analysis — Update Targets

**High priority update targets** (4 articles in your area):

| Rank | Score | Topic | Affected Area | Specific Addition Needed |
|------|-------|-------|---------------|--------------------------|
| 58 | 65.7 | App Studio bricks, Pro-Code & public embed: passing filters/parameters and trigg | App Studio / Bricks & Pro-Code / Embed | Document: (1) how to pass app filters and pfilters into bricks/blank bricks and why pfilters in a br |
| 88 | 62.6 | AI Readiness changes not propagating to Domo Everywhere publications | Domo AI / Domo Everywhere | Document whether AI Readiness metadata propagates through Domo Everywhere publication/refresh, and h |
| 95 | 61.8 | Sandbox / repository deployment best practices (beast mode copies, repo structur | Governance & Security / Sandbox | Best-practice guidance for Sandbox repositories: aesthetic-only dashboard changes without cloning ev |
| 105 | 60.7 | Renaming/hiding datasets and custom messages in Domo Everywhere publishing | Domo Everywhere | Whether dataset names/descriptions can be changed at publish time, options to hide datasets from sub |

---

## Quick Actions Summary

A prioritized list of everything this document is asking of you:

| # | Action | Type | Est. Effort |
|---|--------|------|------------|
| 1 | Read and fact-check `Domo-Sandbox-Overview.mdx` | Fact-check | 30–45 min |
| 2 | Fact-check `Choose-How-to-Share-Outside-Domo.mdx` (Rank 139 community request) | Fact-check | 20–30 min |
| 3 | Supply info to write `Embed-Domo-in-Third-Party-Platforms.mdx` (Rank 17) | Info meeting | 30 min |
| 4 | Supply info to write `Embedded-Dashboard-Unfiltered-Data-Flash.mdx` (Rank 28) | Info meeting | 30 min |
| 5 | **Open placeholder in `360043437993.mdx`:** Confirm whether private embed IDs/codes are intentionally user-specific (per-use | **Answer required** | 15–30 min |
| 6 | **Open placeholder in `360043437993.mdx`:** Confirm the exact wording and behavior of the "You are editing content embedded  | **Answer required** | 15–30 min |
| 7 | **Open placeholder in `360043437993.mdx`:** Confirm the specific browser and version behind this Private Network Access chan | **Answer required** | 15–30 min |
| 8 | **Open placeholder in `360045120554.mdx`:** Confirm whether a DataSet's name or description can be changed at publish time ( | **Answer required** | 15–30 min |
| 9 | **Open placeholder in `4403367344023.mdx`:** Confirm the recommended DEV/PROD promotion pattern; whether App Studio global an | **Answer required** | 15–30 min |
| 10 | **Open placeholder in `4403367344023.mdx`:** Confirm the exact generic error text users see (reported as an "invalid content  | **Answer required** | 15–30 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
