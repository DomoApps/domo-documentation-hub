# Phase 3b cluster: Tasleema-Lallmamode__5

**Owning PM:** Tasleema Lallmamode
**Files in this cluster:** 5  |  **Gaps:** 5

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005138.mdx`
*Workbench 5.2 Overview* — area: Workbench / Release notes

### Gap rank 228 (Medium, score 50.1) — Workbench release notes discoverability and version-change behavior
- **What's missing:** Where to find Workbench version release notes and what specific bug-fix changes mean (e.g. how Workbench writes null values to Domo). Release notes not discoverable in KB.
- **Suggested location:** Update s/article/000005138.mdx (Workbench 5.2 Overview): link the Workbench version release notes prominently and document notable behavior changes (e.g. null/blank handling). Improve discoverability of release notes across Workbench docs.

---

## `s/article/360042932734.mdx`
*Connecting to ODBC Data in Workbench 5* — area: Workbench / Data types

### Gap rank 173 (Medium, score 54.2) — Workbench data type precision limits (LONG/DOUBLE/DECIMAL) and setup/agent errors
- **What's missing:** Documented maximum precision/digit limits per Domo data type and guidance on handling high-precision numbers (store as string); resolving the 'No agents found matching computer name' error (delete-and-recreate-account workaround); ingesting unsupported sources like DB2 via the ODBC Connection Provider.
- **Suggested location:** Update Workbench docs: add a data-type precision reference table (LONG/DOUBLE/DECIMAL digit limits and store-as-string guidance), and add the 'No agents found matching computer name' error and its delete-and-recreate-account workaround to a Workbench troubleshooting article. DB2-via-ODBC is largely covered by the ODBC connector doc.

- **Other referenced articles:** s/article/360046864914.mdx

---

## `s/article/360046864914.mdx`
*Resolving Issues with Failing Jobs in Workbench 4* — area: Workbench / Errors

### Gap rank 232 (Medium, score 49.8) — Workbench-specific error messages without documented resolution
- **What's missing:** Troubleshooting docs for these specific Workbench errors, their causes, and fixes. Both threads point users to support with no documented answer.
- **Suggested location:** Update the Workbench troubleshooting article (s/article/360046864914.mdx or a Workbench 5 equivalent): add the 'Error converting value {null} to type System.Boolean' error and the success-but-empty-dataset scenario with causes/fixes.

---

## `s/article/360058762534.mdx`
*Simplified Server Migration in Workbench 5* — area: Workbench / Datasets

### Gap rank 295 (Medium, score 45.6) — Avoiding duplicate datasets on Workbench reinstall / pointing a job to an existing dataset
- **What's missing:** How to point a new Workbench job to an existing Domo dataset (avoid duplicate creation), and migrating/restoring jobs to a new machine. Behavior not documented.
- **Suggested location:** Update s/article/360058762534.mdx (Simplified Server Migration in Workbench 5) or the Workbench job docs: add a note on pointing a new job to an existing Domo dataset (Overview > Domo Details > Browse) to avoid duplicate dataset creation on reinstall.

- **Other referenced articles:** s/article/360044356293.mdx

---

## `s/article/4406022964375.mdx`
** — area: Workbench / Installation

### Gap rank 149 (Medium, score 56.4) — Workbench OS/permission requirements (Windows admin, no Mac support)
- **What's missing:** Clear documentation of Workbench OS/permission requirements (admin needed to install AND run, UAC elevation), removal of old non-admin workarounds, and lack of native Mac support.
- **Suggested location:** Update s/article/4406022964375.mdx (Workbench Install guide): correct/clarify that admin is required to install AND run, remove the outdated non-admin workaround, state no native Mac support, and point Mac/non-admin users to Workbench Enterprise (Docker).

- **Other referenced articles:** s/article/000005303.mdx

---
