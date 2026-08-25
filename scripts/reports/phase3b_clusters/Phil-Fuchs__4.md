# Phase 3b cluster: Phil-Fuchs__4

**Owning PM:** Phil Fuchs
**Files in this cluster:** 2  |  **Gaps:** 3

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360042925434.mdx`
*Bucketing Data Using Beast Mode* — area: Magic ETL / Beast Mode

### Gap rank 289 (Medium, score 46.1) — Reclassifying/grouping similar values and combining datasets of differing granularity
- **What's missing:** Document CASE-based value reclassification, joining/aggregating datasets of differing granularity, and the recommended Views-for-aggregation-then-ETL-for-join workflow to keep ETL inputs small.
- **Suggested location:** Add a 'combining datasets of differing granularity' recipe (aggregate the finer set with a Dataset View, then join in Magic ETL) to s/article/4405337525783.mdx (Data Fundamentals) or a new how-to; cross-link CASE reclassification.

- **Other referenced articles:** s/article/4405337525783.mdx

---

## `s/article/360042934614.mdx`
*Personalized Data Permissions (PDP)* — area: Security - PDP

### Gap rank 202 (Medium, score 51.7) — PDP not applying / admins and page owners bypassing PDP; App Studio scope
- **What's missing:** Prominently state that Admins, DataSet owners/co-owners, and users with Manage DataSet grant bypass row/column PDP (see everything), clarify default 'all data' behavior when a user isn't in any policy, and explicitly document whether/how PDP applies to App Studio apps.
- **Suggested location:** Update s/article/360042934614.mdx: add a prominent troubleshooting/FAQ callout that Admins, owners/co-owners, and Manage DataSet users bypass PDP (a common 'PDP not working' cause), and add an explicit statement of whether/how PDP applies to App Studio apps.

### Gap rank 223 (Medium, score 50.3) — Hidden whitespace/carriage returns breaking PDP matching
- **What's missing:** Document that invisible/trailing characters (carriage returns, leading/trailing whitespace) can break PDP matching and how to detect/clean them (e.g. via ETL TRIM); the Data tab does not surface these.
- **Suggested location:** Add a short troubleshooting note to the PDP article (s/article/360042934614.mdx): invisible/trailing characters (carriage returns, leading/trailing spaces) can prevent PDP value matches; clean them with an ETL TRIM. Note the Data tab doesn't reveal them.

---
