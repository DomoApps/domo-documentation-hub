# Phase 3b cluster: Dan-Brinton__3

**Owning PM:** Dan Brinton
**Files in this cluster:** 3  |  **Gaps:** 3

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360042934594.mdx`
*DomoStats - Activity Log App* — area: Projects & Tasks / DomoStats

### Gap rank 157 (Medium, score 55.2) — Projects & Tasks field limitations and Tags in DomoStats
- **What's missing:** Document the actual fields available on Projects (no start date) and Tasks (no start/estimation/priority), and that Tags aren't included in the Tasks DomoStats dataset, so users can plan ETL workarounds. Field additions are feature requests.
- **Suggested location:** Update the Projects & Tasks documentation to enumerate available fields and explicitly note the absences (no start date, no estimation/priority; Tags not in the Tasks DomoStats dataset) so users can plan ETL workarounds. Adding the fields is a feature request.

---

## `s/article/360043427513.mdx`
*Change Your Password* — area: User Management / Buzz

### Gap rank 290 (Medium, score 46.0) — Re-sending user invitation / password emails (Buzz dependency, Domo Everywhere)
- **What's missing:** Documentation should clarify how to (re)trigger invitation/password emails, the dependency on Buzz, and alternatives when Buzz isn't available (Forgot Password flow, admin password reset) - especially for Domo Everywhere instances.
- **Suggested location:** Update the user-management / invitation article (start from s/article/360043427513.mdx and the admin user-management docs) to document how to (re)trigger invitation/password emails, the Buzz dependency, and the alternatives when Buzz isn't available on a Domo Everywhere instance (user Forgot Password flow, admin password reset). Optionally note the POST /api/content/v1/avatar workaround surfaced in the profile-image thread.

- **Other referenced articles:** s/article/000005875.mdx

---

## `s/article/360043439293.mdx`
*DomoStats - DataSets and DataFlows* — area: Magic ETL (scheduling / DomoStats)

### Gap rank 254 (Medium, score 48.4) — Identifying ETL trigger type (schedule vs data-update) and trigger-based-not-conditional behavior
- **What's missing:** Document how to identify ETL trigger type via DomoStats (Dataflow History execution type, Dataflows With Input Datasources) and the dataflows API, and clarify that ETL execution is trigger-based not conditional (a filtered dataset view still triggers on every refresh).
- **Suggested location:** Clarify in s/article/000005216.mdx (Advanced DataFlow Triggering) that execution is trigger-based not conditional (a filtered view still triggers every refresh), and add to 360043439293 (DomoStats - DataSets and DataFlows) how to read execution/trigger type.

- **Other referenced articles:** s/article/000005216.mdx

---
