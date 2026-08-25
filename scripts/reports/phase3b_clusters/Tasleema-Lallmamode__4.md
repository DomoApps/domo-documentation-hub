# Phase 3b cluster: Tasleema-Lallmamode__4

**Owning PM:** Tasleema Lallmamode
**Files in this cluster:** 5  |  **Gaps:** 9

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360042932974.mdx`
*Manage Your Federated Data Connection* — area: Governance / Data Access / Connectors

### Gap rank 316 (Low, score 43.2) — PDP / OAuth / Federated account configuration usability
- **What's missing:** Mostly feature requests for UI/usability. Documentable adjacent: how PDP policies are configured (manual per-attribute selection) and how OAuth/Federated OAuth (e.g. Snowflake) accounts are configured including role/warehouse fields.
- **Suggested location:** Low-priority. Ensure current PDP and OAuth/Federated account configuration behavior (per-attribute selection, role/warehouse fields) is documented; the UI usability asks are feature requests to track.

---

## `s/article/360043433813.mdx`
*DomoStats Connector* — area: Governance & Security

### Gap rank 113 (Medium, score 59.8) — Which DomoStats/Governance dataset for X (cards owners, tags, AI readiness, activity log description)
- **What's missing:** An up-to-date catalog/mapping of DomoStats & Governance datasets to the data they contain, noting deprecations (Cards / Cards and Datasets deprecated -> use Card Permissions + People), the Dataset Tags report, AI Readiness Report / AI Readiness Details Report, and where the activity-log Description field is surfaced (it's not in the DomoStats Activity Log).
- **Suggested location:** Update s/article/360043433813.mdx (DomoStats Connector): flag the legacy Cards / Cards and Datasets report as deprecated and point card-owner lookups to Card Permissions + People; add a note that the activity-log Description field is not available in the DomoStats Activity Log report (and where, if anywhere, it is surfaced). Optionally add a short 'find the right report for a field' lookup table to s/article/DomoStats-Overview.mdx.

- **Other referenced articles:** s/article/DomoStats-Overview.mdx, s/article/000005851.mdx

### Gap rank 291 (Medium, score 45.9) — DomoStats scheduling limits (basic only, no advanced/hourly)
- **What's missing:** Document that DomoStats only supports basic scheduling (vs advanced on Domo Governance), and the workaround of triggering refreshes via a Workflow timer trigger or external API/Lambda.
- **Suggested location:** Update s/article/360043433813.mdx (DomoStats Connector): add a note that DomoStats supports only basic scheduling (Domo Governance supports advanced), and the workaround of triggering refresh via a Workflow timer or API.

### Gap rank 319 (Low, score 42.8) — DomoStats / Governance reports coverage gaps (cloud engine column, connector config audit, app access)
- **What's missing:** Partly documentable: the DomoStats Datasets report now includes engine columns (Domo/Snowflake/Databricks) and the integration used - should be documented. The Activity Log gap for connector config/schedule changes and lack of an App-access report are feature requests.
- **Suggested location:** Update s/article/360043433813.mdx (DomoStats Connector) to document the engine/cloud-provider columns now on the Datasets report. Track the Activity Log connector-config audit and App-access report as feature requests.

### Gap rank 350 (Low, score 38.8) — Activity log / tracking coverage limits (PPT add-in refresh, Snowflake query tagging, card-on-page views)
- **What's missing:** Mostly feature requests. Documentable: what the Activity Log / DomoStats does and does not capture (e.g. card view events lack page context), and approximation approaches (timestamp-based joins on card-load/page-view events).
- **Suggested location:** Update the DomoStats/Activity Log docs with a note on what activity is and isn't captured (e.g. card view events lack page context) and the timestamp-join approximation for card-on-page. Track PPT-refresh tracking and Snowflake query tagging as feature requests.

---

## `s/article/360043437333.mdx`
*Setting Notifications in Workbench 5* — area: Workbench / Administration

### Gap rank 357 (Low, score 36.3) — Workbench server reauthorization frequency and error-notification visibility
- **What's missing:** Documentation of Workbench server authorization lifetime/renewal behavior and where job error-notification recipients are surfaced. Primarily enhancement requests.
- **Suggested location:** Optionally document Workbench server authorization lifetime/renewal behavior in the Workbench admin docs. Exposing notification recipients in DomoStats and longer auth duration are feature requests to track.

---

## `s/article/360056318074.mdx`
*Domo Governance Datasets Connector* — area: Governance & Security (DomoStats / DomoGovernance)

### Gap rank 238 (Medium, score 49.5) — DomoStats / governance reporting gaps after Domo Governance deprecation
- **What's missing:** Mostly feature requests, but a migration-mapping doc is warranted: which deprecated Domo Governance datasets/fields map to current DomoStats reports, and which have no equivalent.
- **Suggested location:** Add a migration-mapping section to the Domo Governance Datasets Connector article (s/article/360056318074.mdx): which deprecated Domo Governance datasets/fields (PDP policy metadata, dataflow locked/restricted flag) map to current DomoStats/Governance datasets and which have no equivalent. The new field additions are feature requests.

- **Other referenced articles:** s/article/360042934594.mdx

### Gap rank 280 (Medium, score 46.7) — Auditing dashboard/page viewer access and exporting group membership
- **What's missing:** How to obtain viewer-level page access and group-membership data via the Governance Datasets Connector ('Pages and Users', 'Users and Groups' datasets; requires an access token). A how-to mapping these needs to the connector is the gap.
- **Suggested location:** Add task-oriented examples to the Domo Governance Datasets Connector article (s/article/360056318074.mdx): 'List viewers with access to a dashboard' (Pages and Users) and 'Export group membership' (Users and Groups), including the access-token requirement. Reduces these recurring governance-reporting questions.

---

## `s/article/360062446514.mdx`
*Workbench Partition Support* — area: Workbench / Data ingestion

### Gap rank 201 (Medium, score 51.7) — Workbench append + periodic replace / partitioning strategy for large incremental loads
- **What's missing:** Best-practice guidance on combining APPEND/REPLACE/UPSERT/partitioning for large incremental loads, schema warnings during method switches, and that partitioning is Workbench-only (not Magic ETL).
- **Suggested location:** Update s/article/360062446514.mdx (Workbench Partition Support) or add a Workbench ingestion best-practices section: how to combine APPEND/REPLACE/UPSERT/partition for large incremental loads, schema warnings on method switches, and that partitioning is Workbench-only.

---
