# Phase 3b cluster: Tasleema-Lallmamode__3

**Owning PM:** Tasleema Lallmamode
**Files in this cluster:** 5  |  **Gaps:** 6

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005514.mdx`
*Salesforce Connector* — area: Connectors / Salesforce

### Gap rank 333 (Low, score 41.3) — Salesforce connector 2,000-row cap without unique ID
- **What's missing:** Document the Salesforce connector's 2,000-row limit for reports lacking a unique ID, that a unique ID column must be added (or a SOQL query built to replicate the report), and any other large-extract strategies.
- **Suggested location:** Update s/article/000005514.mdx (Salesforce Connector): add a note about the 2,000-row report limit when no unique ID column is present, and the workarounds (add a unique ID column, or build a SOQL query).

---

## `s/article/360042926274.mdx`
*Adding a DataSet Using a Connector* — area: Dataset Scheduling

### Gap rank 189 (Medium, score 52.6) — Dataset update scheduling: basic vs advanced, multiple schedules, retry behavior
- **What's missing:** Document: switching to Advanced disables Basic (and vice versa); advanced scheduling only supports intervals, not multiple distinct times/days; where retry-on-failure lives (Scheduling > Advanced > Error Handling > Do not retry) and that it's hidden when using a basic schedule.
- **Suggested location:** Update s/article/360042926274.mdx (Adding a DataSet Using a Connector) scheduling section: explicitly note that choosing Advanced disables Basic (and vice versa), that scheduling supports intervals rather than multiple discrete times/days, and reinforce where retry/error-handling lives. Multiple distinct schedules is a feature request — note as a current limitation.

---

## `s/article/360042931814.mdx`
*Snowflake Connector* — area: Connectors / Snowflake

### Gap rank 116 (Medium, score 59.7) — Snowflake username/password auth retirement and connector migration
- **What's missing:** Customers need a clear, step-by-step migration guide: full list of affected connectors (Snowflake, Snowflake Unload, Unload V2, Managed Unload, High Bandwidth, Partition, Writeback), how to migrate each to OAuth vs Key Pair, what happens after the deadline, and how to verify the new connection.
- **Suggested location:** Either expand the migration section in s/article/360042931814.mdx (Snowflake Connector) or add a dedicated 'Migrate Snowflake Connectors off Username/Password Authentication' KB article in the Connectors nav group, enumerating all affected connector variants, the OAuth-vs-Key-Pair decision, the cutover deadline, and verification steps.

- **Other referenced articles:** s/article/360042931854.mdx, s/article/360061552054.mdx

---

## `s/article/360043432333.mdx`
*Salesforce Advanced Connector* — area: Connectors / Salesforce

### Gap rank 331 (Low, score 41.5) — Salesforce connector behavior (REST vs Bulk API, picklist label vs API name)
- **What's missing:** Documentation explaining the Salesforce Advanced connector's REST vs Bulk API tiles (real-time/small-query limits vs high-volume), and whether/how to retrieve picklist label values instead of the API names the connector returns by default.
- **Suggested location:** Update s/article/360043432333.mdx (Salesforce Advanced Connector) with a short subsection comparing Browse Object (REST) vs Browse in Bulk (Bulk API) — when to use each, volume/limits — and clarify the picklist label-vs-API-name behavior (and the Column Name Styles option's scope).

---

## `s/article/360043433453.mdx`
*NetSuite SuiteAnalytics Connect Connector* — area: Connectors / NetSuite

### Gap rank 229 (Medium, score 50.0) — NetSuite2.com connector table discovery and Analytics Connect date filtering
- **What's missing:** Need documentation on: discovering available tables/columns in NetSuite2.com (SELECT * FROM OA_TABLES / OA_COLUMNS), any official NetSuite-to-NetSuite2 mapping, and how to write working date WHERE clauses in NetSuite Analytics Connect (must match instance date format; standard SQL YEAR()/EXTRACT/TO_DATE fail).
- **Suggested location:** Update the NetSuite SuiteAnalytics Connect connector articles: add a 'discovering tables/columns' tip (SELECT * FROM OA_TABLES / OA_COLUMNS) and a 'writing date filters' note that WHERE clauses must use the instance date format.

- **Other referenced articles:** s/article/000005906.mdx

### Gap rank 234 (Medium, score 49.6) — NetSuite SuiteAnalytics permission changes / migration to JDBC OAuth; UPSERT and writeback enhancements
- **What's missing:** Document the SuiteAnalytics permission requirement change and migration path to NetSuite JDBC OAuth; document the now-shipped UPSERT support on SuiteAnalytics Connect; provide a writeback object/transform support reference. Some items (Case object writeback, transform options) are feature requests.
- **Suggested location:** Update the NetSuite SuiteAnalytics Connect connector article with the permission-change advisory and migration path, plus the now-shipped UPSERT support. Update the NetSuite Writeback connector article with a supported-object/transform reference (note Case object/transform options are feature requests).

- **Other referenced articles:** s/article/360042932414.mdx

---
