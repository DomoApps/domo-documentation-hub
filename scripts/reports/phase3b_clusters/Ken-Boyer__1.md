# Phase 3b cluster: Ken-Boyer__1

**Owning PM:** Ken Boyer
**Files in this cluster:** 4  |  **Gaps:** 8

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005539.mdx`
*Use AI Chat* — area: Domo AI Chat / Roles

### Gap rank 225 (Medium, score 50.2) — Enabling AI Chat: where the icon lives, roles/grants, and per-user control
- **What's missing:** Document how to enable AI Chat (the AI Chat grant in Admin > Roles > Grid, icon location in new left navigation), prerequisites (AI Service Layer settings, AI readiness), whether it's consumption-model-only, and that per-user/group control requires custom roles (default roles can't be edited).
- **Suggested location:** Update s/article/000005539.mdx (Use AI Chat). Expand 'Required Grants' / 'Access AI Chat' with: a troubleshooting note for a missing AI Chat icon (verify the Use AI Chat grant + AI Service Layer enabled), and an explicit statement that to grant AI Chat to only specific users/groups you must create a custom role (link to the custom-roles article, e.g. s/article/360042922974.mdx) because default roles cannot be edited. Note current state that per-dashboard/per-app scoping of AI Chat is not available.

- **Other referenced articles:** s/article/000005561.mdx

### Gap rank 245 (Medium, score 49.0) — Saving AI Chat-generated charts/graphs to a card or dashboard
- **What's missing:** Document current AI Chat limitation (cannot save a generated chart as a card), the workarounds (Show Chart Controls to infer config then build in Analyzer; AI Content Builder Agent), and how to access the AI Content Builder Agent (Apps dropdown).
- **Suggested location:** Update s/article/000005539.mdx (Use AI Chat). Add a short subsection or FAQ entry: 'Can I save a chart from AI Chat as a card?' stating the current limitation and listing the workarounds (copy as image, use Show Chart Controls to read the inferred config and rebuild in Analyzer, or use the AI Content Builder Agent — and where to find it in the Apps dropdown).

---

## `s/article/000005849.mdx`
*Use FileSets to Gather Information from Unstructured Data* — area: App Studio / FileSets & Images

### Gap rank 147 (Medium, score 56.4) — Using images in App Studio: uploading files, FileSets URLs, and referencing in apps
- **What's missing:** How-to documentation for uploading images at scale, the FileSets file-download URL format, and how to reference those URLs so images render in App Studio components (a recent fix was mentioned but undocumented).
- **Suggested location:** Update s/article/000005849.mdx (FileSets): reconcile the roadmap note with current capability, document the file-download URL pattern, and how to reference image URLs in App Studio image/gallery components. Cross-link from s/article/000005864.mdx (App Components).

- **Other referenced articles:** s/article/000005864.mdx

---

## `s/article/36004740075.mdx`
** — area: Developer / Domo Jupyter

### Gap rank 322 (Low, score 42.7) — Domo Jupyter: account access errors when 'access unencrypted credentials' unchecked
- **What's missing:** Document that Jupyter credential access requires the connector advanced option 'Allow authorized users to access unencrypted credentials', that this option is hidden under 'show advanced options', and that a 404 from get_account_property_value can mean this rather than a missing account.
- **Suggested location:** Add a troubleshooting entry to s/article/7440921035671.mdx (Jupyter Troubleshooting Guide) and/or the account-credentials section of s/article/36004740075.mdx: get_account_property_value 404 can mean the connector's 'Allow authorized users to access unencrypted credentials' advanced option is unchecked (hidden under 'show advanced options'), not a missing account.

- **Other referenced articles:** s/article/7440921035671.mdx

### Gap rank 328 (Low, score 42.0) — Jupyter Workspaces: writing data types (boolean/date) to Domo datasets
- **What's missing:** Document type-handling quirks of domojupyter.write_dataframe: boolean columns landing as empty integer columns, the known Python date/datetime issue, and recommended coercion patterns (astype(str)) or downstream ETL input-type fixes. Users note this has persisted since 2023-2024.
- **Suggested location:** Add a write_dataframe data-type-handling note to s/article/36004740075.mdx (or the troubleshooting guide): boolean columns can land as empty integer columns, known date/datetime quirks, and the astype(str)/ETL input-type coercion workarounds. This is partly a long-standing bug; document the workaround as current state.

- **Other referenced articles:** s/article/7440921035671.mdx

### Gap rank 349 (Low, score 38.9) — Update R version and Jupyter workspace search/backup quality-of-life requests
- **What's missing:** Feature requests, not doc gaps. Documentable: the current R version (4.1) and supported kernels/packages, how in-workspace os.walk search works for finding code strings, and the lack of backup (deletion is permanent) so users plan accordingly.
- **Suggested location:** Add documentable current-state facts to s/article/36004740075.mdx: the current R version and supported kernels/packages, an in-workspace code-search pattern (os.walk), and a Warning that deleting a workspace is permanent (no backup). The R-upgrade, cross-workspace search, and backup API remain product feature requests.

---

## `s/article/7440921035671.mdx`
*Jupyter Troubleshooting Guide* — area: Jupyter Workspaces (errors / provisioning)

### Gap rank 206 (Medium, score 51.4) — Jupyter Workspaces: datasource-id resolution failures and enablement/access
- **What's missing:** Document how to troubleshoot 'Input dataset with id ... not found' / datasource-id resolution errors in Jupyter Workspaces, how to add/verify datasets in a workspace, the account/permission requirements for workspace access, and the process to request Jupyter Workspaces enablement (including non-standard/student instances).
- **Suggested location:** Add troubleshooting entries to s/article/7440921035671.mdx (Jupyter Troubleshooting Guide): datasource-id resolution errors ('Input dataset with id ... not found') and how to add/verify datasets in a workspace; and document the enablement-request path (incl. student/non-standard instances) in s/article/36004740075.mdx.

- **Other referenced articles:** s/article/36004740075.mdx

### Gap rank 313 (Low, score 43.3) — Jupyter Workspaces: scheduled .ipynb / 'Edit in Jupyter' button opens blank / wrong code
- **What's missing:** Document how scheduled .ipynb files link to their source .py in a workspace, what happens when the source is renamed/deleted, and how to locate/repair the code behind a failing scheduled job (the 'Edit in Jupyter' button behavior and limitations).
- **Suggested location:** Expand the 'Scheduled Execution Failures' section of s/article/7440921035671.mdx to explain how a scheduled .ipynb links to its source file, what 'Edit in Jupyter' does when the source is renamed/deleted (blank screen), and how to locate/repair the code (recent_executions). Partly a UX bug; document current behavior and confirm fix status.

- **Other referenced articles:** s/article/36004740075.mdx

---
