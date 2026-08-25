# Phase 3b cluster: Phil-Fuchs__3

**Owning PM:** Phil Fuchs
**Files in this cluster:** 5  |  **Gaps:** 7

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360042925474.mdx`
*Beast Mode Manager* — area: Dashboards - Admin / Management

### Gap rank 135 (Medium, score 57.4) — Moving sub-dashboards between parents and detaching from a parent
- **What's missing:** Step-by-step (Admin > Dashboards > select > Edit > Move Dashboard > choose location/Top Level > permissions) and an explanation of what the 'Merge permissions' vs other permission options do during a dashboard move.
- **Suggested location:** Update the dashboard/page admin-management article to add the Move Dashboard step-by-step (including detaching to Top Level) and define the permission options ('Merge permissions' vs alternatives) presented during a move.

### Gap rank 296 (Medium, score 45.5) — Beast Mode Manager / DomoStats governance gaps (data type, dates, bulk select/transfer, save-to-dataset restriction, shared-edit warning)
- **What's missing:** Mostly feature requests. Documentable: Beast Mode data type can be retrieved via the JSON connector endpoint (GET /api/query/v1/functions/template/{beastmode}); clarify current Beast Mode Manager capabilities, bulk limits (100), and save-to-dataset performance implications.
- **Suggested location:** Note in Beast Mode Manager (s/article/360042925474.mdx) and/or the Governance connector docs which Beast Mode metadata is available (data type via the JSON connector endpoint) and current limits; the rest are feature requests.

---

## `s/article/360042926154.mdx`
*Best Practices for Managing DataSets* — area: Connectors / Dataset management

### Gap rank 125 (Medium, score 58.5) — Duplicate Dataset and dataset history revert (now shipped) discoverability
- **What's missing:** Documentation of the now-available 'Duplicate Dataset' feature (three-dot menu) for cloning connector settings, and the dataset history 'revert to this point' capability that restores prior connector settings.
- **Suggested location:** Update a dataset-management article (e.g. s/article/360042926154.mdx) or add a short how-to documenting the Duplicate Dataset action (three-dot menu) and the dataset history 'revert to this point' capability for restoring prior connector settings.

- **Other referenced articles:** s/article/6814561223959.mdx

---

## `s/article/360042935354.mdx`
*Best Practices for Sharing Content in Domo* — area: Datasets / Permissions & Roles

### Gap rank 293 (Medium, score 45.8) — Dataset sharing gated by recipient role/grants (can't view shared dataset; add admin to all datasets)
- **What's missing:** Document that dataset sharing is gated by the recipient's role grants (ability to access Data Center / view datasets), and how 'Manage all DataSets' or other grants affect visibility regardless of explicit sharing.
- **Suggested location:** Add a troubleshooting note to the dataset-sharing documentation: sharing a dataset does not grant visibility unless the recipient's role includes the grants to access the Data Center / view datasets (e.g. Manage all DataSets). Explain the sharing-vs-role interaction.

---

## `s/article/360043428293.mdx`
*Combine DataSets Using DataFusion (Deprecated)* — area: Datasets / Data Fusion

### Gap rank 198 (Medium, score 52.1) — Blend/Data Fusion removed — replacement and migration guidance
- **What's missing:** Document the deprecation/removal of Blend/Data Fusion, the replacement (Dataset Views/Magic ETL), and how to migrate existing fusions that feed downstream ETLs.
- **Suggested location:** Add a clear deprecation/migration note to s/article/360043428293.mdx (Combine DataSets Using DataFusion (Deprecated)): what replaced it (Dataset Views/Magic ETL) and how to migrate fusions that feed downstream ETLs without breaking them.

- **Other referenced articles:** s/article/360043428333.mdx

---

## `s/article/360046074774.mdx`
*Manage DataSet Views* — area: Dataset Views / SQL Editor

### Gap rank 271 (Medium, score 47.1) — Can't Save View / unhelpful Views Explorer SQL errors (UNION not working)
- **What's missing:** Documentation should cover Views Explorer SQL Editor constraints and troubleshooting: avoid SELECT *, use named fields, use UNION ALL vs UNION, supported syntax limits, and that you cannot switch back to the GUI builder (incl. Beast Mode creation) once you use the SQL Editor.
- **Suggested location:** Update s/article/360046074774.mdx (Manage DataSet Views): add a SQL Editor troubleshooting/limitations subsection — common causes of the generic 'Unable to save'/'issue during processing' error, prefer named columns over SELECT *, UNION vs UNION ALL, and the one-directional switch to the SQL Editor (after which Beast Modes must be created in SQL).

### Gap rank 347 (Low, score 39.2) — Selecting a subset of columns for a View / one-way SQL Editor switch
- **What's missing:** Document the recommended workflow for keeping a small subset of columns in a View (select-all-delete then add back), and clearly document that the SQL Editor / GUI switch in Views is one-directional and that Beast Modes must then be created in SQL.
- **Suggested location:** Update s/article/360046074774.mdx (Manage DataSet Views): add a tip for trimming wide datasets to a small subset of columns (select all + delete, then re-add the few you want) and reinforce the one-directional GUI->SQL Editor switch (shared with the SQL-errors topic). The remove-column mechanics are already documented.

---
