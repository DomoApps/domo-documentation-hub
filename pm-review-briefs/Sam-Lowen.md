# PM Review Brief: Sam Lowen

**Prepared for:** KB Restructure PM Review Meeting
**Features owned:** Cloud Amplifier, DataSets, Federated
**Total articles in your area:** 22

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
| Cloud Amplifier | 18 | Pillar 2: Connect & Integrate Data |
| DataSets | 3 | Pillar 3: Manage Data |
| Federated | 1 | Pillar 2: Connect & Integrate Data |

---

## 2. AI-Generated Articles — Your Fact-Check Required

These articles will be synthesized by AI from existing KB content in Phase 3a.
**They need your review before publishing.** Please read the draft and verify the
key claims listed — especially anything about product behavior, limitations, or
recommended patterns.

| # | Article | Synthesized From | Key Claims to Verify |
|---|---------|------------------|---------------------|
| 1 | `Find-and-Manage-Your-DataSets.mdx` (Pillar 3) | DataSet management, sharing, workspace/favorites articles | Search/filter/favorite/share datasets — verify current Data Center UI |

---

## 3. New Forum-Gap Articles and Open Placeholders

New articles in your area from the community-forum gap analysis (and the original
restructure plan). Some are **already drafted and need your fact-check**; others
**cannot be written until you supply information**. The two are separated below so
it's clear which is which.

### 3d. Open Article Placeholders — Your Answer Required

The items below are open `[pm-input]` placeholders where specific information from
you is needed before the content can be finalized. Each is a checkbox — check it
off once you've provided the answer.

- [ ] **`4412849158167.mdx`**
  Confirm the exact date-handling impact of the en-US-only limitation for Cloud Amplifier (Databricks) and the recommended workaround (ETL reformatting reported as high-overhead); confirm full locale support is a tracked feature request. Synthesized from community forum reports; needs confirmation.

- [ ] **`Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`**
  Confirm the manual-refresh control for a Cloud Amplifier integration (reported as a "Sync with Cloud" button): its exact label and location, and confirm that it refreshes all tables in the integration rather than a single DataSet. synthesized from community forum reports; needs confirmation.

- [ ] **`Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`**
  Confirm that a DataSet View built on a Cloud Amplifier connection cannot be remapped to a different Cloud Amplifier connection (unlike standard connectors, which is useful for DEV/PROD moves), and that remapping support is a tracked feature request. synthesized from community forum reports; needs confirmation.

- [ ] **`Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`**
  Confirm whether the DataSet History tab is intentionally absent (or hidden) for Cloud Integration (Cloud Amplifier) DataSets, and whether full run-history metadata support is a tracked feature request. Synthesized from community forum reports; needs confirmation.

- [ ] **`Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`**
  Confirm whether a dedicated control to pause or cap per-card queries against a live Cloud Amplifier source (beyond caching/TTL) exists or is a tracked feature request. Synthesized from community forum reports; needs confirmation.

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
| 15 | 74.1 | File import data types: leading zeros and type changes on import/view | Datasets / Connectors / Views | Document which file-upload connector supports the 'keep leading zeros' option (newer 'CONNECT DATA > |
| 37 | 69.0 | Federated (on-prem SQL) dataset preemptive full-scan query behavior | Datasets / Federated | Document federated dataset query/materialization behavior, whether the unfiltered preemptive query c |
| 90 | 62.1 | Cloud Amplifier data freshness, caching, sync behavior, and view remapping | Cloud Integrations / Cloud Amplifier | Need clear documentation defining Data Freshness vs Data Caching (purpose, difference, behavior), th |

---

## Quick Actions Summary

A prioritized list of everything this document is asking of you:

| # | Action | Type | Est. Effort |
|---|--------|------|------------|
| 1 | Read and fact-check `Find-and-Manage-Your-DataSets.mdx` | Fact-check | 30–45 min |
| 2 | **Open placeholder in `4412849158167.mdx`:** Confirm the exact date-handling impact of the en-US-only limitation for Cloud Am | **Answer required** | 15–30 min |
| 3 | **Open placeholder in `Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`:** Confirm the manual-refresh control for a Cloud Amplifier integration (reported a | **Answer required** | 15–30 min |
| 4 | **Open placeholder in `Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`:** Confirm that a DataSet View built on a Cloud Amplifier connection cannot be rema | **Answer required** | 15–30 min |
| 5 | **Open placeholder in `Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`:** Confirm whether the DataSet History tab is intentionally absent (or hidden) for  | **Answer required** | 15–30 min |
| 6 | **Open placeholder in `Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`:** Confirm whether a dedicated control to pause or cap per-card queries against a l | **Answer required** | 15–30 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
