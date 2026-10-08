# PM Review Brief: Jordan Jensen

**Prepared for:** KB Restructure PM Review Meeting
**Features owned:** AppStore, Cloud Amplifier, DataSets, Education, Federated, Onboarding
**Total articles in your area:** 124

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
| AppStore | 78 | Pillar 6: Build Apps & Automate |
| Cloud Amplifier | 18 | Pillar 2: Connect & Integrate Data |
| DataSets | 3 | Pillar 3: Manage Data |
| Education | 13 | Pillar 1: Getting Started |
| Federated | 1 | Pillar 2: Connect & Integrate Data |
| Onboarding | 11 | Pillar 1: Getting Started |

### Notable Navigation Changes

- **DataSet Management split (D9):** Some DataSet Management articles currently in Prepare & Transform will move to the new Manage Data pillar (Pillar 3). The split: pipeline-oriented articles stay in Pillar 4; governance/lifecycle articles move to Pillar 3. Resolve before Phase 7.

---

## 2. AI-Generated Articles — Your Fact-Check Required

These articles will be synthesized by AI from existing KB content in Phase 3a.
**They need your review before publishing.** Please read the draft and verify the
key claims listed — especially anything about product behavior, limitations, or
recommended patterns.

| # | Article | Synthesized From | Key Claims to Verify |
|---|---------|------------------|---------------------|
| 1 | `What-is-a-DataSet.mdx` (Pillar 4) | Connector how-tos, ETL input tile articles | DataSet definition, dataset types, lifecycle states, update methods — especially the 'archived' state |
| 2 | `Manage-Data-Overview.mdx` (Pillar 3) | DataSet articles, Data Center context | Data Center navigation, dataset discovery, lifecycle, sharing — verify current UI state |
| 3 | `What-is-the-Data-Center.mdx` (Pillar 3) | DataSet management articles, connector how-tos | Data Center UI, dataset cards, status indicators — verify current UI state |
| 4 | `Find-and-Manage-Your-DataSets.mdx` (Pillar 3) | DataSet management, sharing, workspace/favorites articles | Search/filter/favorite/share datasets — verify current Data Center UI |

---

## 3. New Forum-Gap Articles and Open Placeholders

New articles in your area from the community-forum gap analysis (and the original
restructure plan). Some are **already drafted and need your fact-check**; others
**cannot be written until you supply information**. The two are separated below so
it's clear which is which.

### 3c. Forum-Gap Articles Awaiting Your Input — Cannot Be Written Yet

These forum gaps **cannot be written without your input** — the KB has no source
material and the mechanics are Domo-proprietary. A short dedicated meeting (or an
async written answer) is needed before drafting can begin.

| Rank | Intended Article | What You Need to Supply |
|------|------------------|-------------------------|
| 142 | `Choose-a-Cloud-Data-Warehouse.mdx` | Credit model (pushdown vs materialization), sizing guidance for small datasets, which Domo features force materialization and consume ingestion credits (PDP, View Data Explorer, alerts, scheduled emails) |
| 146 | `Domo-Certification-Exam-Logistics.mdx` | Exam duration, single-sitting requirement, online vs proctored format, three-step structure, hands-on requirements, whether the KB hosts content or points to Domo University |

### 3d. Open Article Placeholders — Your Answer Required

The items below are open `[pm-input]` placeholders where specific information from
you is needed before the content can be finalized. Each is a checkbox — check it
off once you've provided the answer.

- [ ] **`000005900.mdx`**
  Confirm whether admins can set a default navigation layout or admin-managed pinned sections for a group (default-by-group / admin-managed sections), or whether pinning and personalization remain per-user only today. Synthesized from community forum reports; needs confirmation.

- [ ] **`1500000406641.mdx`**
  Confirm that pydomo has no native upsert-key command and document the schema-based Python SDK approach (reported as marking a column as an upsert key via a schema-upsert.json definition): the exact field/flag and where it is set. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042935714.mdx`**
  Confirm whether the editable design can be retrieved or downloaded from an app that has already been published to Domo, or whether editing requires the original exported app project folder. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042935714.mdx`**
  Confirm the distinction between the download-design (export) output format and the format the CourseBuilder desktop app expects on import. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043438473.mdx`**
  some users report that YouTube videos added by ID do not display in the published CourseBuilder app even when the provider and ID are set correctly; confirm whether this is a known issue and the supported workaround. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043440393.mdx`**
  Confirm the correct Publish-to-Domo sequence in CourseBuilder that resolves the blank-screen / missing-login-prompt symptom on macOS. Synthesized from community forum reports; needs confirmation.

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

- [ ] **`Getting Started role articles — eLearning course URLs`**
  All Getting Started role articles (Admins, App Builders, Data Engineers, Developers) currently link to the same `data-consumer-training` eLearning course URL, which is likely wrong for non-consumer roles. Confirm the correct course URL for each role (coordinate with the Education / Domo University team).

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
| 1 | Read and fact-check `What-is-a-DataSet.mdx` | Fact-check | 30–45 min |
| 2 | Read and fact-check `Manage-Data-Overview.mdx` | Fact-check | 30–45 min |
| 3 | Read and fact-check `What-is-the-Data-Center.mdx` | Fact-check | 30–45 min |
| 4 | Read and fact-check `Find-and-Manage-Your-DataSets.mdx` | Fact-check | 30–45 min |
| 5 | Supply info to write `Choose-a-Cloud-Data-Warehouse.mdx` (Rank 142) | Info meeting | 30 min |
| 6 | Supply info to write `Domo-Certification-Exam-Logistics.mdx` (Rank 146) | Info meeting | 30 min |
| 7 | **Open placeholder in `000005900.mdx`:** Confirm whether admins can set a default navigation layout or admin-managed pinn | **Answer required** | 15–30 min |
| 8 | **Open placeholder in `1500000406641.mdx`:** Confirm that pydomo has no native upsert-key command and document the schema-bas | **Answer required** | 15–30 min |
| 9 | **Open placeholder in `360042935714.mdx`:** Confirm whether the editable design can be retrieved or downloaded from an app t | **Answer required** | 15–30 min |
| 10 | **Open placeholder in `360042935714.mdx`:** Confirm the distinction between the download-design (export) output format and t | **Answer required** | 15–30 min |
| 11 | **Open placeholder in `360043438473.mdx`:** some users report that YouTube videos added by ID do not display in the publishe | **Answer required** | 15–30 min |
| 12 | **Open placeholder in `360043440393.mdx`:** Confirm the correct Publish-to-Domo sequence in CourseBuilder that resolves the  | **Answer required** | 15–30 min |
| 13 | **Open placeholder in `4412849158167.mdx`:** Confirm the exact date-handling impact of the en-US-only limitation for Cloud Am | **Answer required** | 15–30 min |
| 14 | **Open placeholder in `Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`:** Confirm the manual-refresh control for a Cloud Amplifier integration (reported a | **Answer required** | 15–30 min |
| 15 | **Open placeholder in `Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`:** Confirm that a DataSet View built on a Cloud Amplifier connection cannot be rema | **Answer required** | 15–30 min |
| 16 | **Open placeholder in `Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`:** Confirm whether the DataSet History tab is intentionally absent (or hidden) for  | **Answer required** | 15–30 min |
| 17 | **Open placeholder in `Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`:** Confirm whether a dedicated control to pause or cap per-card queries against a l | **Answer required** | 15–30 min |
| 18 | **Open placeholder in `Getting Started role articles — eLearning course URLs`:** All Getting Started role articles (Admins, App Builders, Data Engineers, Develop | **Answer required** | 15–30 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
