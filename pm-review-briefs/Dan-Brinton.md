# PM Review Brief: Dan Brinton

**Prepared for:** KB Restructure PM Review Meeting
**Features owned:** Admin, Alerts, NLG, Smart Alerts/Insights, Attribute Based Access Control (ABAC), Buzz, Consumption, DomoStats, Goals, Profile, Single Sign-On
**Total articles in your area:** 70

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
| Admin | 23 | Pillar 9: Administer & Govern |
| Alerts, NLG, Smart Alerts/Insights | 7 | Pillar 7: Share & Collaborate |
| Attribute Based Access Control (ABAC) | 4 | Pillar 9: Administer & Govern |
| Buzz | 11 | Pillar 7: Share & Collaborate |
| Consumption | 2 | Pillar 9: Administer & Govern |
| DomoStats | 5 | Pillar 8: AI & Data Science |
| Goals | 5 | Pillar 9: Administer & Govern |
| Profile | 8 | Pillar 9: Administer & Govern |
| Single Sign-On | 5 | Pillar 9: Administer & Govern |

### Notable Navigation Changes

- **'Introduction to Domo' (D5):** The existing 000005874 article overlaps with the new 'What is Domo?' synthesis article. Decision needed: keep as deep-dive companion, or retire once new article ships?

- **'What is an Alert?' new article:** An alert concept article is being synthesized and added to the Alerts section. The existing Alerts Overview article may become secondary.

---

## 2. AI-Generated Articles — Your Fact-Check Required

These articles will be synthesized by AI from existing KB content in Phase 3a.
**They need your review before publishing.** Please read the draft and verify the
key claims listed — especially anything about product behavior, limitations, or
recommended patterns.

| # | Article | Synthesized From | Key Claims to Verify |
|---|---------|------------------|---------------------|
| 1 | `What-is-Domo.mdx` (Pillar 1) | 000005874, Getting Started role guides | Core value proposition, platform overview, key use cases — verify nothing is outdated or overpromised |
| 2 | `Getting-Started-for-Admins.mdx` (Pillar 1) | Admin how-tos, roles/grants articles | Admin onboarding path, key first tasks (user setup, SSO, security), grant scopes |
| 3 | `What-is-an-Alert.mdx` (Pillar 7) | Alerts Overview, alert articles | Alert types, trigger conditions, Smart Alerts / NLG behavior, notification routing |
| 4 | `Share-and-Collaborate-Overview.mdx` (Pillar 7) | Sharing / Buzz / Publications / Embed articles | All sharing mechanisms, publication groups vs Domo Everywhere scope distinction |
| 5 | `Domo-User-Roles.mdx` (Pillar 9) | Roles / grants articles | System roles, custom roles, grant scopes — verify completeness of role list |
| 6 | `Security-and-Permissions-Overview.mdx` (Pillar 9) | PDP, OAuth, security settings articles | PDP, SSO, IP allowlist, access tokens, session management — verify current security model |
| 7 | `Administer-and-Govern-Overview.mdx` (Pillar 9) | All admin articles | Full admin toolbox overview — verify nothing major is missing from hub |

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
| 7 | `Activity-Log-Event-Reference.mdx` — *Activity Log Event Reference* ⚠️ | Synthesized from 360042934574 (admin Activity Log) + 360042934594 (DomoStats app) + portal Activity Log API. `[pm-input]` Dan Brinton: full enumerated event glossary (VIEWED/EXPORTED/DOWNLOADED, FILE/FILE_REVISION/ACTIVITY_LOG_CSV) + canonical View Activity Logs grant wording |
| 9 | `Restore-a-Deleted-Dashboard.mdx` — *Restore a Deleted Dashboard* ⚠️ | No source article — current-state FAQ. `[pm-input]` Dan Brinton: confirm backup retention window + Support recovery path |
| 26 | `DomoStats-vs-Governance-Datasets-Connector.mdx` — *Compare the DomoStats and Domo Governance Datasets Connectors* | Synthesized from 360043433813 + 360056318074; report-by-report comparison + service-account Activity Log caveat. Omitted unverifiable deprecation/scheduling claims |
| 152 | `Find-Which-Dashboard-a-Card-Lives-On.mdx` — *Find Which Dashboard a Card Lives On* ⚠️ | Synthesized from 360056318074 (Governance connector Cards/Pages reports). Classic dashboards only; `[pm-input]` Tasleema Lallmamode for App Studio lineage |

### 3c. Forum-Gap Articles Awaiting Your Input — Cannot Be Written Yet

These forum gaps **cannot be written without your input** — the KB has no source
material and the mechanics are Domo-proprietary. A short dedicated meeting (or an
async written answer) is needed before drafting can begin.

| Rank | Intended Article | What You Need to Supply |
|------|------------------|-------------------------|
| 82 | `Manage-Dataset-Error-Alerts.mdx` | How data-load-failure ("Error Loading Data") notifications are generated and why system-managed, per-dataset disable path, bulk-suppression options and official status |
| 99 | `Domo-API-Changelog.mdx` | The versioning convention (if any), whether/where breaking changes are announced, deprecation timeline policy, any existing changelog content |
| 103 | `ETL-Credits-and-Consumption-Model.mdx` | Definition of a "manual run" vs scheduled, the "significant change" threshold that voids legacy ETL consumption status, a citable authoritative source |
| 127 | `Alert-on-Stuck-Dataset-Refresh.mdx` | Confirm a DataSet alert on the DomoStats last-run field to detect a stuck refresh + the exact condition; the Workflow timer-trigger + Run Connector action to run sub-daily |

### 3d. Open Article Placeholders — Your Answer Required

The items below are open `[pm-input]` placeholders where specific information from
you is needed before the content can be finalized. Each is a checkbox — check it
off once you've provided the answer.

- [ ] **`000005326.mdx`**
  Confirm how Magic ETL credit consumption relates to processed row counts (for example, a runaway many-to-many join that generates very large row counts), how to cancel an in-progress DataFlow or ETL execution, and whether any automatic protections stop runaway runs. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005492.mdx`**
  Confirm the behavior when Data Refresh Permissions is enabled: whether only full admins can set advanced or sub-hourly refresh schedules regardless of a user's assigned policy, and exactly how a policy's frequency limit interacts with a non-admin user's role. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042925994.mdx`**
  Confirm the exact prerequisites and failure conditions for Alert-triggered Task creation: the Project role/membership the Alert owner needs (owner vs. member) to add Tasks, and the specific reasons a Task can silently fail to be created when an Alert fires. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042925994.mdx`**
  Confirm how numeric column formatting and exponential/scientific display affect threshold evaluation — specifically whether the Alert evaluates the underlying stored numeric value rather than the formatted or exponentially displayed value. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042925994.mdx`**
  Confirm how an attached Scheduled/Triggered Report resolves the actual triggered value versus the "Current alert value" placeholder in the report body. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042934294.mdx`**
  Confirm which objects support group ownership versus individual ownership only—specifically whether datasets can be group-owned while DataFlows cannot—and confirm that a content certification request goes to an individual owner only (group members and admins can't approve on the group's behalf), along with any co-owner workaround. Certification-specific behavior belongs in Certify Cards and DataSets (/s/article/360043430613). Synthesized from community forum reports; needs confirmation.

- [ ] **`360042934294.mdx`**
  Confirm the following dynamic-group criteria behaviors: (1) that leaving a criterion blank or set to a space produces a group that includes every user in the instance; (2) that a user's role and email address are not available as native membership criteria, so the custom Managed attribute workaround above is the supported way to group by role. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042934454.mdx`**
  confirm the Required Grants for adding and managing user licenses; no Required Grants section exists.

- [ ] **`360042934594.mdx`**
  Confirm the precise meaning of the Activity Log action and object values, specifically DOWNLOADED vs. EXPORTED and the FILE, FILE_REVISION, and ACTIVITY_LOG_CSV object types, plus the full list of fields available in each DomoStats DataSet. synthesized from community forum reports; needs confirmation.

- [ ] **`360042934594.mdx`**
  Confirm exactly how the card-footer view count is calculated and the time window it covers, so it can be reconciled against Activity Log card-view events. synthesized from community forum reports; needs confirmation.

- [ ] **`360043427513.mdx`**
  Confirm whether invitation and password-reset email delivery depends on Buzz being enabled, and what the supported alternative is for (re)triggering these emails on Domo Everywhere instances where Buzz is unavailable. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043438133.mdx`**
  confirm the Required Grants for enabling SSO with Okta; no Required Grants section exists.

- [ ] **`360043438213.mdx`**
  confirm which certificate's expiration affects SAML auth-request signing (the "Information your IdP may need" certificate) and the exact remediation the customer must perform (for example, regenerate the certificate in Domo and re-upload it to the IdP). Synthesized from community forum reports; needs confirmation.

- [ ] **`360043438953.mdx`**
  Confirm the exact names of the account-management/account-sharing grants, that the default Admin role does not include them (so a custom role is required), and the precise condition that produces the "Sharing restricted by the system" (HTTP 403) error. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043438973.mdx`**
  Confirm whether Domo hides menus and features that a user's role lacks the grants for, or whether those entry points stay visible and only deny the action on use. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043438973.mdx`**
  Confirm which grants the default Admin system role includes and excludes, and confirm that only the default Admin role (not a custom role with equivalent grants) can view all Domo Support tickets for the instance—and, if so, which grant or role property controls that. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043438973.mdx`**
  Confirm any role or grant visibility conferred by the Assign Users to a Role grant beyond assigning allowlisted roles (community reports that it exposes full role and grant visibility). Synthesized from community forum reports; needs confirmation.

- [ ] **`360043438973.mdx`**
  Confirm the implicit or coupled grant requirements for common actions, such as which grant is required to share pages and which grants Governance Toolkit access requires. Note: App Studio Report Builder is governed by the "Edit Report (Report Builder)" grant per /s/article/000005829, which appears to conflict with the community report that Report Builder requires "Edit Pages" plus "Edit Apps"—reconcile before documenting. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043438973.mdx`**
  Confirm the policy for how newly released grants are applied to existing custom roles at release: whether they are enabled or disabled by default and whether an admin must opt in. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043439293.mdx`**
  Confirm the supported way to obtain DataFlow trigger type and schedule for reporting, and whether a documented endpoint or connector-based workaround should be recommended here. synthesized from community forum reports; needs confirmation.

- [ ] **`360043439313.mdx`**
  confirm the exact field-level gaps in the DomoStats Projects and Tasks datasets: which fields are absent from the Tasks dataset (e.g., start date, priority, estimation) and that Tags are not included in the Tasks dataset. Synthesized from community forum reports; needs confirmation.

- [ ] **`Activity-Log-Event-Reference.mdx`**
  confirm the canonical description wording for the View Activity Logs grant; the description above was authored for this article because no existing article defines it in the standard grant format.

- [ ] **`Activity-Log-Event-Reference.mdx`**
  provide the complete enumerated list of Activity Log event types with a precise one-line definition of each, including the semantic distinctions users ask about: VIEWED vs. EXPORTED vs. DOWNLOADED, the Shared / Added / Access Granted distinctions, and the FILE / FILE_REVISION / ACTIVITY_LOG_CSV object types. Replace the representative table above with the confirmed glossary.

- [ ] **`Restore-a-Deleted-Dashboard.mdx`**
  confirm the backup retention window (how far back a deleted dashboard can be recovered from a backup) and the exact recovery path Support follows. Replace the "not guaranteed" language with the confirmed retention window once known.

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
| 19 | 72.3 | DomoStats action/object meanings (Download vs Export, FILE/FILE_REVISION) and fi | DomoStats | Document the meaning of DomoStats Activity Log actions/objects (DOWNLOADED vs EXPORTED, FILE/FILE_RE |
| 45 | 67.7 | Card view-count discrepancies (card footer vs Activity Log Viewed) | Activity Log / Card metrics | Document precisely how the card view count (footer) is calculated and over what period vs how the Ac |
| 79 | 63.5 | Restricting dataset/card access including from admins; PDP column masking; unsha | Governance & Security | Document that the Admin role cannot be restricted by PDP (requires a custom 'Admin Lite'-style role) |

---

## Quick Actions Summary

A prioritized list of everything this document is asking of you:

| # | Action | Type | Est. Effort |
|---|--------|------|------------|
| 1 | Read and fact-check `What-is-Domo.mdx` | Fact-check | 30–45 min |
| 2 | Read and fact-check `Getting-Started-for-Admins.mdx` | Fact-check | 30–45 min |
| 3 | Read and fact-check `What-is-an-Alert.mdx` | Fact-check | 30–45 min |
| 4 | Read and fact-check `Share-and-Collaborate-Overview.mdx` | Fact-check | 30–45 min |
| 5 | Read and fact-check `Domo-User-Roles.mdx` | Fact-check | 30–45 min |
| 6 | Read and fact-check remaining 2 Phase 3a articles | Fact-check | ~30 min each |
| 7 | Fact-check `Activity-Log-Event-Reference.mdx` (Rank 7 community request) | Fact-check | 20–30 min |
| 8 | Fact-check `Restore-a-Deleted-Dashboard.mdx` (Rank 9 community request) | Fact-check | 20–30 min |
| 9 | Fact-check `DomoStats-vs-Governance-Datasets-Connector.mdx` (Rank 26 community request) | Fact-check | 20–30 min |
| 10 | Fact-check `Find-Which-Dashboard-a-Card-Lives-On.mdx` (Rank 152 community request) | Fact-check | 20–30 min |
| 11 | Supply info to write `Manage-Dataset-Error-Alerts.mdx` (Rank 82) | Info meeting | 30 min |
| 12 | Supply info to write `Domo-API-Changelog.mdx` (Rank 99) | Info meeting | 30 min |
| 13 | Supply info to write `ETL-Credits-and-Consumption-Model.mdx` (Rank 103) | Info meeting | 30 min |
| 14 | Supply info to write `Alert-on-Stuck-Dataset-Refresh.mdx` (Rank 127) | Info meeting | 30 min |
| 15 | **Open placeholder in `000005326.mdx`:** Confirm how Magic ETL credit consumption relates to processed row counts (for ex | **Answer required** | 15–30 min |
| 16 | **Open placeholder in `000005492.mdx`:** Confirm the behavior when Data Refresh Permissions is enabled: whether only full | **Answer required** | 15–30 min |
| 17 | **Open placeholder in `360042925994.mdx`:** Confirm the exact prerequisites and failure conditions for Alert-triggered Task  | **Answer required** | 15–30 min |
| 18 | **Open placeholder in `360042925994.mdx`:** Confirm how numeric column formatting and exponential/scientific display affect  | **Answer required** | 15–30 min |
| 19 | **Open placeholder in `360042925994.mdx`:** Confirm how an attached Scheduled/Triggered Report resolves the actual triggered | **Answer required** | 15–30 min |
| 20 | **Open placeholder in `360042934294.mdx`:** Confirm which objects support group ownership versus individual ownership only—s | **Answer required** | 15–30 min |
| 21 | **Open placeholder in `360042934294.mdx`:** Confirm the following dynamic-group criteria behaviors: (1) that leaving a crite | **Answer required** | 15–30 min |
| 22 | **Open placeholder in `360042934454.mdx`:** confirm the Required Grants for adding and managing user licenses; no Required G | **Answer required** | 15–30 min |
| 23 | **Open placeholder in `360042934594.mdx`:** Confirm the precise meaning of the Activity Log action and object values, specif | **Answer required** | 15–30 min |
| 24 | **Open placeholder in `360042934594.mdx`:** Confirm exactly how the card-footer view count is calculated and the time window | **Answer required** | 15–30 min |
| 25 | **Open placeholder in `360043427513.mdx`:** Confirm whether invitation and password-reset email delivery depends on Buzz bei | **Answer required** | 15–30 min |
| 26 | **Open placeholder in `360043438133.mdx`:** confirm the Required Grants for enabling SSO with Okta; no Required Grants secti | **Answer required** | 15–30 min |
| 27 | **Open placeholder in `360043438213.mdx`:** confirm which certificate's expiration affects SAML auth-request signing (the "I | **Answer required** | 15–30 min |
| 28 | **Open placeholder in `360043438953.mdx`:** Confirm the exact names of the account-management/account-sharing grants, that t | **Answer required** | 15–30 min |
| 29 | **Open placeholder in `360043438973.mdx`:** Confirm whether Domo hides menus and features that a user's role lacks the grant | **Answer required** | 15–30 min |
| 30 | **Open placeholder in `360043438973.mdx`:** Confirm which grants the default Admin system role includes and excludes, and co | **Answer required** | 15–30 min |
| 31 | **Open placeholder in `360043438973.mdx`:** Confirm any role or grant visibility conferred by the Assign Users to a Role gra | **Answer required** | 15–30 min |
| 32 | **Open placeholder in `360043438973.mdx`:** Confirm the implicit or coupled grant requirements for common actions, such as w | **Answer required** | 15–30 min |
| 33 | **Open placeholder in `360043438973.mdx`:** Confirm the policy for how newly released grants are applied to existing custom  | **Answer required** | 15–30 min |
| 34 | **Open placeholder in `360043439293.mdx`:** Confirm the supported way to obtain DataFlow trigger type and schedule for repor | **Answer required** | 15–30 min |
| 35 | **Open placeholder in `360043439313.mdx`:** confirm the exact field-level gaps in the DomoStats Projects and Tasks datasets: | **Answer required** | 15–30 min |
| 36 | **Open placeholder in `Activity-Log-Event-Reference.mdx`:** confirm the canonical description wording for the View Activity Logs grant; the  | **Answer required** | 15–30 min |
| 37 | **Open placeholder in `Activity-Log-Event-Reference.mdx`:** provide the complete enumerated list of Activity Log event types with a precise  | **Answer required** | 15–30 min |
| 38 | **Open placeholder in `Restore-a-Deleted-Dashboard.mdx`:** confirm the backup retention window (how far back a deleted dashboard can be rec | **Answer required** | 15–30 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
