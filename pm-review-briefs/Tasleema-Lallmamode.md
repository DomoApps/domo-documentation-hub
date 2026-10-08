# PM Review Brief: Tasleema Lallmamode

**Prepared for:** KB Restructure PM Review Meeting
**Features owned:** Connectors 1.0, Third Party Connectors, Workbench
**Total articles in your area:** 1096

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
| Connectors 1.0 | 102 | Pillar 2: Connect & Integrate Data |
| Third Party Connectors | 895 | Pillar 2: Connect & Integrate Data |
| Workbench | 99 | Pillar 2: Connect & Integrate Data |

### Notable Navigation Changes

- **CDW merge:** Cloud Data Warehouses (104 articles) are no longer a top-level section — they are now a sub-group inside the Connector Library. Writeback Connectors (55 articles) are similarly integrated into the library alongside read connectors rather than living in a standalone section.

- **Workbench consolidation:** Workbench 4 (36 EN articles) → Legacy (D1 confirmed); moves to the Archive group with a `<LegacyNote/>` in Phase 4.6. Workbench 5.1 gets a clearly-labeled Legacy sub-group.

- **Connector merges DONE (2026-08-28):** 14 exact-title duplicate connectors were merged/deleted — keeper kept, unique fields folded in, nav entries and inbound links fixed. See RESTRUCTURE-MANIFEST.md › Connector Merges.

- **8 title-collisions were NOT duplicates (deferred, need retitling):** distinct connectors sharing a title — Documents-surface (SFTP, Amazon S3, GitHub), variants (WordPress self-hosted, Magento OAuth, Kendra query). For **LinkedIn** and **Google Ads**, the *current* connector was retained on review; the *deprecated* generation (LinkedIn V1, legacy AdWords) is now a Retired candidate.

- **Defunct-service connectors:** 12 named dead-service articles + the Deprecate superset (185 EN) are Retired candidates (staged for 4.6) — confirm the true dead set.

---

## 2. AI-Generated Articles — Your Fact-Check Required

These articles will be synthesized by AI from existing KB content in Phase 3a.
**They need your review before publishing.** Please read the draft and verify the
key claims listed — especially anything about product behavior, limitations, or
recommended patterns.

| # | Article | Synthesized From | Key Claims to Verify |
|---|---------|------------------|---------------------|
| 1 | `What-is-a-Connector.mdx` (Pillar 2) | General Connector Info (12 articles) | Connector concept, OAuth vs API key auth, scheduling, update methods |
| 2 | `Connect-and-Integrate-Data-Overview.mdx` (Pillar 2) | All connector / Workbench articles | Read + write framing accuracy, Cloud Amplifier as recommended CDW path, connector types |
| 3 | `What-is-Workbench.mdx` (Pillar 2) | Workbench 5.2 overview, Workbench Enterprise | Workbench capabilities, read + write paths, current version support status |

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
| 32 | `Connect-Unsupported-Data-Sources.mdx` — *Connect Data When No Native Connector Exists* | Decision hub synthesized from 360042926294; links to JSON No Code, Workbench, Jupyter, custom connector |

### 3c. Forum-Gap Articles Awaiting Your Input — Cannot Be Written Yet

These forum gaps **cannot be written without your input** — the KB has no source
material and the mechanics are Domo-proprietary. A short dedicated meeting (or an
async written answer) is needed before drafting can begin.

| Rank | Intended Article | What You Need to Supply |
|------|------------------|-------------------------|
| 27 | `Trigger-Workbench-from-External-Scripts.mdx` | Full `wb.exe` command/parameter reference, how to trigger a job/group from an external script, same-server requirement, referenceable job/group IDs |
| 55 | `Incremental-Ingestion-and-Lastvalue.mdx` | `lastvalue` parameter syntax + required default value, cause/fix of "last value is missing" error, incremental vs full-replace handling of late updates and deletes |
| 84 | `GA4-BigQuery-Daily-Table-Nested-Data.mdx` | Recommended BigQuery connector variant, wildcard-view / `_TABLE_SUFFIX` SQL, Magic ETL `UNNEST(event_params)` steps, GA4-UI reconciliation methodology |
| 86 | `Find-Domo-Version-and-Tool-Versions.mdx` | Confirm no user-facing platform version, `/admin/tooldownloads` page description + URL + required grant, Workbench/plugin independent versioning |

### 3d. Open Article Placeholders — Your Answer Required

The items below are open `[pm-input]` placeholders where specific information from
you is needed before the content can be finalized. Each is a checkbox — check it
off once you've provided the answer.

- [ ] **`000005138.mdx`**
  confirm the null/blank handling behavior change (how Workbench writes null vs. blank source values to a Domo DataSet, and in which version it changed) so it can be documented here. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005360.mdx`**
  confirm the exact JSON No Code UI field labels for cursor pagination: where the user specifies the token's location in the response (JSON path) and the "Add as a parameter" option that sends the token on the next request. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005677.mdx`**
  confirm the prerequisites behind the "Your DataSet could not be created" error: whether the target SharePoint folders must already exist (i.e., the connector does not create missing folders), any folder-naming restrictions, and the exact Azure app registration API permissions/roles the Writeback connector requires. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042926294.mdx`**
  confirm the recommended MFA guidance for connectors (service account vs. app password vs. OAuth) and whether any specific connectors can complete MFA directly. synthesized from community forum reports; needs confirmation.

- [ ] **`360042926294.mdx`**
  confirm the zero-row no-wipe behavior under Replace, and whether any connector (for example, SQL Server) exposes a setting analogous to Workbench's "clear dataset if query returns zero rows." synthesized from community forum reports; needs confirmation.

- [ ] **`360042926294.mdx`**
  confirm the supported spreadsheet formats for file upload, the .xlsm limitation and .xlsx workaround, and the exact wording/cause of the "File is not supported / use legacy connector" and "no data found" upload errors. synthesized from community forum reports; needs confirmation.

- [ ] **`360042926294.mdx`**
  confirm the Box connector Excel-date-to-numeric casting behavior and the exact recommended recovery (Excel serial-date epoch offset and the Magic ETL function to use). synthesized from community forum reports; needs confirmation.

- [ ] **`360042926294.mdx`**
  confirm the specific causes and recommended fixes for the generic connector messages "Domo is ready but…" and "Failed to execute import successfully." synthesized from community forum reports; needs confirmation.

- [ ] **`360042926294.mdx`**
  confirm the exact cause of "Indexing failed: Empty primary key" and the recommended fix (which merge/upsert key configuration triggers it and how to resolve empty key values). synthesized from community forum reports; needs confirmation.

- [ ] **`360042926294.mdx`**
  confirm OAuth token-expiry behavior (silent zero-row jobs vs. hard failure) and the exact re-authorization steps in the Accounts tab. synthesized from community forum reports; needs confirmation.

- [ ] **`360042926294.mdx`**
  confirm the exact Google Workspace Admin console path to trust/approve the Domo app (for example, Security > API controls > App access control) and which Google connectors it applies to. synthesized from community forum reports; needs confirmation.

- [ ] **`360042929154.mdx`**
  confirm that Adobe Analytics 1.4 DataSets cannot be auto-migrated and must be recreated on the v2 connector, and confirm the recreation steps and retirement timeline. synthesized from community forum reports; needs confirmation.

- [ ] **`360042930734.mdx`**
  confirm the exact columns/keys used to join Survey Response Choices to Survey Responses (for example, survey ID + question ID + choice/recode value). Synthesized from community forum reports; needs confirmation.

- [ ] **`360042931814.mdx`**
  confirm the full list of affected Snowflake connector variants (reported: Snowflake, Snowflake Unload, Snowflake Unload V2, Snowflake Managed Unload, Snowflake High Bandwidth, Snowflake Partition, Snowflake Writeback) and the recommended replacement (OAuth vs. Key Pair) for each. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042931914.mdx`**
  confirm that the CSV SFTP connectors do not support built-in GPG/PGP file-content encryption for SFTP writeback, and the recommended workaround (Jupyter/Domo Notebooks or AWS). Synthesized from community forum reports; needs confirmation.

- [ ] **`360042931954.mdx`**
  confirm whether capturing the sender ("from") address as a DataSet column is on the roadmap; forum users have requested it. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042932414.mdx`**
  provide the authoritative list of NetSuite record objects supported for writeback and the supported transform options, and confirm the status of the Case object and additional transform options (reported by forum users as feature requests). Synthesized from community forum reports; needs confirmation.

- [ ] **`360042932734.mdx`**
  confirm the maximum precision/digit limits for Domo's LONG, DOUBLE, and DECIMAL data types so the exact thresholds can be documented here. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042932974.mdx`**
  confirm the provider-specific connection fields required when configuring an OAuth / Federated OAuth account (for example, the Snowflake role and warehouse fields), and confirm how PDP policies are applied per attribute on Federated DataSets. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042932974.mdx`**
  confirm the preemptive unfiltered-query/materialization behavior for Federated DataSets, that it cannot be prevented, and how the cache TTL interacts with it. synthesized from community forum reports; needs confirmation.

- [ ] **`360042933494.mdx`**
  confirm the exact steps to remove a recipient who used an email unsubscribe link from the unsubscribers list so they can receive campaigns again (the Unsubscribes tab currently documents only Search, Export, and Refresh). Synthesized from community forum reports; needs confirmation.

- [ ] **`360043432333.mdx`**
  confirm whether the Salesforce Advanced connector offers any built-in option to return picklist display labels instead of API values. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043432333.mdx`**
  confirm the exact UI labels and behavior for the connector's REST vs. Bulk API data-selection tiles (community forum reports refer to a "Browse Object" / REST tile and a "Browse in Bulk" / Bulk API tile), including the row-volume threshold or limits that make Bulk the better choice. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043433453.mdx`**
  confirm whether an official NetSuite.com-to-NetSuite2.com table/column mapping reference exists that we can link to. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043433453.mdx`**
  confirm the exact date literal format SuiteAnalytics Connect / NetSuite2.com expects in WHERE clauses and provide a working example query. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043433453.mdx`**
  confirm that Upsert support has shipped for the SuiteAnalytics Connect connector and note any version/date or configuration requirement. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043433813.mdx`**
  confirm whether the DomoStats connector supports only basic scheduling (no advanced/hourly custom schedule) while the Domo Governance Datasets connector supports advanced scheduling, and confirm the supported refresh workaround (Workflows timer trigger vs. external API/Lambda). Synthesized from community forum reports; needs confirmation.

- [ ] **`360046864914.mdx`**
  confirm the recommended fix for the "Error converting value {null} to type System.Boolean" error (e.g., changing the column data type in Workbench vs. handling nulls in the query). Synthesized from community forum reports; needs confirmation.

- [ ] **`360046864914.mdx`**
  confirm the cause and the canonical fix for the "No agents found matching computer name" error (the delete-and-re-add-account workaround). Synthesized from community forum reports; needs confirmation.

- [ ] **`360052105454.mdx`**
  confirm which OAuth 2.0 grant types the JSON No Code OAuth connector supports and that JWT-bearer login/refresh is not supported (this is also tracked as a feature request). Synthesized from community forum reports; needs confirmation.

- [ ] **`360052105454.mdx`**
  confirm the exact stop conditions the JSON No Code OAuth connector uses for each paging method and the recommended fix when a paged run hangs or loops. Synthesized from community forum reports; needs confirmation.

- [ ] **`360052122294.mdx`**
  confirm the recommended, supported pattern for detecting hard-deleted source records with Append/Merge/Partition connectors (for example, a periodic full-key Replace DataSet compared in a DataFlow). Synthesized from community forum reports; needs confirmation.

- [ ] **`360056318074.mdx`**
  confirm the deprecation/support status of the Domo Governance Datasets connector relative to DomoStats, and confirm which Domo Governance fields have no DomoStats equivalent (community reports call out PDP policy metadata and the DataFlow locked/restricted flag). Synthesized from community forum reports; needs confirmation.

- [ ] **`4406022964375.mdx`**
  confirm whether the "Domo Workbench Users" group still lets non-admin users run Workbench, or whether administrative access is now required to both install and run Workbench (as stated under System Requirements). Community forum reports indicate the non-admin workaround may be outdated; needs confirmation before removing this note.

- [ ] **`Find-Which-Dashboard-a-Card-Lives-On.mdx`**
  the Governance connector reports cover classic pages and dashboards. Confirm how to trace a card to an App Studio app/page (whether an App Studio pages dataset exists) and document why App Studio pages are not shown in a card's info panel or Move/Copy menu. Add an App Studio section once confirmed.

---

## 4. Changes Flagged by Support Gap Integrations

Two gap-fill analyses have been integrated into the restructure plan. This section
shows what changes are planned in your content area and what fact-check input reduces
hallucination risk in the updated articles.

### 4a. Support KB Audit Findings (Phase 4)

**URGENT — Fix before Phase 4:**

> **Snowflake Connector + Snowflake Unload V2**
> DONE (Phase 3b, 2026-07-15). Snowflake retired key-pair/password auth Nov 2025; 7 Snowflake connector articles were updated (retirement language, Warning callouts, migration-section rewrite). Flagged here for your awareness/verification.

**Retirement batches in your area (Phase 4 execution plan):**

| Batch | Count | Action | Notes |
|-------|-------|--------|-------|
| Workbench 4 articles | 36 | → Legacy (staged for 4.6) | D1 confirmed. 36 EN articles for an end-of-life product version. Confirm Legacy: feature still runs at some sites, WB5 is the replacement, no announced removal date. |
| Defunct-service connectors | 12 named + superset | → Retired (staged for 4.6) | 12 verified dead-service articles named (LinkedIn API v1, Pinterest x2, StumbleUpon, Simply Measured, Salesforce Desk, IBM Coremetrics, GetThere, Moz, Adobe Analytics Adv Legacy, DCM via GCS, Azure Data Lake Store) + legacy Google Ads/AdWords reroute. The Category=Data Connection + Deprecate superset (185 EN) is attached for you to confirm which are truly dead. |

### 4b. Community Forum Gap Analysis — Update Targets

**High priority update targets** (4 articles in your area):

| Rank | Score | Topic | Affected Area | Specific Addition Needed |
|------|-------|-------|---------------|--------------------------|
| 36 | 69.2 | Connectors and MFA / app-password authentication | Connectors / Authentication | Need documentation on how Domo connectors handle MFA-protected source accounts: which connectors sup |
| 41 | 68.4 | Connector 'Replace'/zero-row behavior not wiping Domo dataset | Connectors / Data ingestion behavior | Document that Domo will not update/empty a dataset when a run returns no rows, the setting (analogou |
| 102 | 61.1 | Box connector converts Excel dates to numeric timestamps | Connectors (Box) / Data ingestion | Why the Box connector casts Excel dates to numeric timestamps and how to preserve/recover date typin |
| 108 | 60.5 | Connector authentication-method retirements (Adobe, Facebook, SharePoint) | Connectors / Third-party API deprecation | Customers need per-connector migration/recreation guides: which legacy connectors are affected, that |

---

## Quick Actions Summary

A prioritized list of everything this document is asking of you:

| # | Action | Type | Est. Effort |
|---|--------|------|------------|
| 1 | Fix `Snowflake Connector + Snowflake Unload V2` auth/accuracy issue | **URGENT fix** | 1–2 hrs |
| 2 | Read and fact-check `What-is-a-Connector.mdx` | Fact-check | 30–45 min |
| 3 | Read and fact-check `Connect-and-Integrate-Data-Overview.mdx` | Fact-check | 30–45 min |
| 4 | Read and fact-check `What-is-Workbench.mdx` | Fact-check | 30–45 min |
| 5 | Fact-check `Connect-Unsupported-Data-Sources.mdx` (Rank 32 community request) | Fact-check | 20–30 min |
| 6 | Supply info to write `Trigger-Workbench-from-External-Scripts.mdx` (Rank 27) | Info meeting | 30 min |
| 7 | Supply info to write `Incremental-Ingestion-and-Lastvalue.mdx` (Rank 55) | Info meeting | 30 min |
| 8 | Supply info to write `GA4-BigQuery-Daily-Table-Nested-Data.mdx` (Rank 84) | Info meeting | 30 min |
| 9 | Supply info to write `Find-Domo-Version-and-Tool-Versions.mdx` (Rank 86) | Info meeting | 30 min |
| 10 | **Open placeholder in `000005138.mdx`:** confirm the null/blank handling behavior change (how Workbench writes null vs | **Answer required** | 15–30 min |
| 11 | **Open placeholder in `000005360.mdx`:** confirm the exact JSON No Code UI field labels for cursor pagination: where the  | **Answer required** | 15–30 min |
| 12 | **Open placeholder in `000005677.mdx`:** confirm the prerequisites behind the "Your DataSet could not be created" error:  | **Answer required** | 15–30 min |
| 13 | **Open placeholder in `360042926294.mdx`:** confirm the recommended MFA guidance for connectors (service account vs | **Answer required** | 15–30 min |
| 14 | **Open placeholder in `360042926294.mdx`:** confirm the zero-row no-wipe behavior under Replace, and whether any connector ( | **Answer required** | 15–30 min |
| 15 | **Open placeholder in `360042926294.mdx`:** confirm the supported spreadsheet formats for file upload, the  | **Answer required** | 15–30 min |
| 16 | **Open placeholder in `360042926294.mdx`:** confirm the Box connector Excel-date-to-numeric casting behavior and the exact r | **Answer required** | 15–30 min |
| 17 | **Open placeholder in `360042926294.mdx`:** confirm the specific causes and recommended fixes for the generic connector mess | **Answer required** | 15–30 min |
| 18 | **Open placeholder in `360042926294.mdx`:** confirm the exact cause of "Indexing failed: Empty primary key" and the recommen | **Answer required** | 15–30 min |
| 19 | **Open placeholder in `360042926294.mdx`:** confirm OAuth token-expiry behavior (silent zero-row jobs vs | **Answer required** | 15–30 min |
| 20 | **Open placeholder in `360042926294.mdx`:** confirm the exact Google Workspace Admin console path to trust/approve the Domo  | **Answer required** | 15–30 min |
| 21 | **Open placeholder in `360042929154.mdx`:** confirm that Adobe Analytics 1 | **Answer required** | 15–30 min |
| 22 | **Open placeholder in `360042930734.mdx`:** confirm the exact columns/keys used to join Survey Response Choices to Survey Re | **Answer required** | 15–30 min |
| 23 | **Open placeholder in `360042931814.mdx`:** confirm the full list of affected Snowflake connector variants (reported: Snowfl | **Answer required** | 15–30 min |
| 24 | **Open placeholder in `360042931914.mdx`:** confirm that the CSV SFTP connectors do not support built-in GPG/PGP file-conten | **Answer required** | 15–30 min |
| 25 | **Open placeholder in `360042931954.mdx`:** confirm whether capturing the sender ("from") address as a DataSet column is on  | **Answer required** | 15–30 min |
| 26 | **Open placeholder in `360042932414.mdx`:** provide the authoritative list of NetSuite record objects supported for writebac | **Answer required** | 15–30 min |
| 27 | **Open placeholder in `360042932734.mdx`:** confirm the maximum precision/digit limits for Domo's LONG, DOUBLE, and DECIMAL  | **Answer required** | 15–30 min |
| 28 | **Open placeholder in `360042932974.mdx`:** confirm the provider-specific connection fields required when configuring an OAu | **Answer required** | 15–30 min |
| 29 | **Open placeholder in `360042932974.mdx`:** confirm the preemptive unfiltered-query/materialization behavior for Federated D | **Answer required** | 15–30 min |
| 30 | **Open placeholder in `360042933494.mdx`:** confirm the exact steps to remove a recipient who used an email unsubscribe link | **Answer required** | 15–30 min |
| 31 | **Open placeholder in `360043432333.mdx`:** confirm whether the Salesforce Advanced connector offers any built-in option to  | **Answer required** | 15–30 min |
| 32 | **Open placeholder in `360043432333.mdx`:** confirm the exact UI labels and behavior for the connector's REST vs | **Answer required** | 15–30 min |
| 33 | **Open placeholder in `360043433453.mdx`:** confirm whether an official NetSuite | **Answer required** | 15–30 min |
| 34 | **Open placeholder in `360043433453.mdx`:** confirm the exact date literal format SuiteAnalytics Connect / NetSuite2 | **Answer required** | 15–30 min |
| 35 | **Open placeholder in `360043433453.mdx`:** confirm that Upsert support has shipped for the SuiteAnalytics Connect connector | **Answer required** | 15–30 min |
| 36 | **Open placeholder in `360043433813.mdx`:** confirm whether the DomoStats connector supports only basic scheduling (no advan | **Answer required** | 15–30 min |
| 37 | **Open placeholder in `360046864914.mdx`:** confirm the recommended fix for the "Error converting value {null} to type Syste | **Answer required** | 15–30 min |
| 38 | **Open placeholder in `360046864914.mdx`:** confirm the cause and the canonical fix for the "No agents found matching comput | **Answer required** | 15–30 min |
| 39 | **Open placeholder in `360052105454.mdx`:** confirm which OAuth 2 | **Answer required** | 15–30 min |
| 40 | **Open placeholder in `360052105454.mdx`:** confirm the exact stop conditions the JSON No Code OAuth connector uses for each | **Answer required** | 15–30 min |
| 41 | **Open placeholder in `360052122294.mdx`:** confirm the recommended, supported pattern for detecting hard-deleted source rec | **Answer required** | 15–30 min |
| 42 | **Open placeholder in `360056318074.mdx`:** confirm the deprecation/support status of the Domo Governance Datasets connector | **Answer required** | 15–30 min |
| 43 | **Open placeholder in `4406022964375.mdx`:** confirm whether the "Domo Workbench Users" group still lets non-admin users run  | **Answer required** | 15–30 min |
| 44 | **Open placeholder in `Find-Which-Dashboard-a-Card-Lives-On.mdx`:** the Governance connector reports cover classic pages and dashboards | **Answer required** | 15–30 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
