# Phase 3b RE-ROUTE cluster: reroute__2-data-etl

These gaps were correctly skipped by earlier waves because the gap data mislinked them. Each is re-homed to its correct article below. Some target files were already edited in an earlier wave — read current state first and add ONLY the new gap's content.

Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links).

---

## `s/article/360042923134.mdx`
**Marker PM for this file:** Andrea Henderson

### Gap rank 181 (Medium, score 53.4) — Copying/replicating an entire dataset lineage (dev vs prod) and bulk source swapping
- **Routing note:** Copying a DataFlow (was pointed at the unique-key-join article). Add dataset/dataflow lineage replication for dev/prod + bulk source swapping.
- **What's missing:** Document how to copy datasets/dataflows and swap data sources to replicate a lineage for dev/prod, and supported approaches for bulk re-mapping content to new datasets (incl. migrating to Cloud Amplifier/new providers).
- **Original suggested location:** Extend s/article/360042923134.mdx (Copying a DataFlow) or add a migration how-to covering lineage replication for dev/prod and bulk source swapping (CLI and the relevant remap approaches). Nav under DataFlow Management.

---

## `s/article/4405337525783.mdx`
**Marker PM for this file:** Andrea Henderson

### Gap rank 289 (Medium, score 46.1) — Reclassifying/grouping similar values and combining datasets of differing granularity
- **Routing note:** Data Fundamentals — join/differing-granularity HALF ONLY (the CASE reclassification half was already done in 360042925434). Add: aggregate finer set with a DataSet View, then join in Magic ETL.
- **What's missing:** Document CASE-based value reclassification, joining/aggregating datasets of differing granularity, and the recommended Views-for-aggregation-then-ETL-for-join workflow to keep ETL inputs small.
- **Original suggested location:** Add a 'combining datasets of differing granularity' recipe (aggregate the finer set with a Dataset View, then join in Magic ETL) to s/article/4405337525783.mdx (Data Fundamentals) or a new how-to; cross-link CASE reclassification.

---

## `s/article/What-is-Magic-ETL.mdx`
**Marker PM for this file:** Andrea Henderson

### Gap rank 339 (Low, score 39.8) — Magic ETL access prerequisites and cloud-connector dependency errors
- **Routing note:** Magic ETL overview (was pointed at Create a Beast Mode Calculation). Add access-prerequisites note (role/grants) + referenced-cloud-connector-dataset dependency error.
- **What's missing:** Documentation of Magic ETL access prerequisites (role/grants required) and that errors can stem from a referenced cloud-connector dataset, plus whether a cloud account is required to use Magic ETL.
- **Original suggested location:** Update the Magic ETL overview/getting-started article with an access-prerequisites note (required role/grants) and a troubleshooting note that a referenced cloud-connector dataset can cause open errors.

---

## `s/article/360046074774.mdx`
**Marker PM for this file:** Phil Fuchs

### Gap rank 231 (Medium, score 49.8) — Dataset Views joining limitations across source types / Cloud Amplifier
- **Routing note:** Manage DataSet Views (was pointed at the Virtual DataSets article). Add Dataset Views join/blend limitations (same-type join, UNION, Cloud Amplifier). NOTE: already got gaps 271/347 in Wave 3 — add only 231 content.
- **What's missing:** Documentation needs to clearly state which datasets/views can and cannot be joined: that Cloud Amplifier (Snowflake cloud) datasets can only join other same-type datasets in Views, that materialized vs non-materialized behave differently, and that UNION across views/sources is unsupported.
- **Original suggested location:** Update the Dataset Views documentation: add a limitations note stating that Views can only join datasets of the same underlying type (e.g. Cloud Amplifier/Snowflake datasets join only other Snowflake datasets), that published/virtual datasets can't be joined, and that UNION across sources is unsupported.

---

## `s/article/360043439313.mdx`
**Marker PM for this file:** Dan Brinton

### Gap rank 157 (Medium, score 55.2) — Projects & Tasks field limitations and Tags in DomoStats
- **Routing note:** DomoStats - Projects and Tasks (was pointed at the Activity Log app article). Add field limitations: no start date, no priority/estimation, Tags absent from Tasks dataset. Likely needs a [pm-input] for the unverifiable field-absence specifics.
- **What's missing:** Document the actual fields available on Projects (no start date) and Tasks (no start/estimation/priority), and that Tags aren't included in the Tasks DomoStats dataset, so users can plan ETL workarounds. Field additions are feature requests.
- **Original suggested location:** Update the Projects & Tasks documentation to enumerate available fields and explicitly note the absences (no start date, no estimation/priority; Tags not in the Tasks DomoStats dataset) so users can plan ETL workarounds. Adding the fields is a feature request.

---
