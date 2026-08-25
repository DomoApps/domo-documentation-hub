# Phase 3b cluster: Andrea-Henderson__1

**Owning PM:** Andrea Henderson
**Files in this cluster:** 5  |  **Gaps:** 5

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005901.mdx`
*Magic ETL Tiles: Disable Tiles* — area: Magic ETL

### Gap rank 164 (Medium, score 54.9) — Magic ETL development/testing: disable/comment-out tiles, run-to-here, single-output runs
- **What's missing:** Mostly feature requests, but the newly shipping beta/GA features (disable/comment-out tiles, Run to Here, recover changes, undo/redo, search) need documentation. Disable Tiles has shipped and is documented; Run to Here / single-output runs are not yet covered.
- **Suggested location:** The disable-tiles request is already documented (000005901). As Run to Here, single-tile preview, and run-specific-outputs go GA, add them as sibling Magic ETL KB articles in s/article/ and reference in the relevant release-notes article. Update 000005901 to cross-link related run-control features.

---

## `s/article/360043427933.mdx`
*Join DataSets by Adding a Unique Key Column* — area: Datasets / Dataflows / Migration

### Gap rank 181 (Medium, score 53.4) — Copying/replicating an entire dataset lineage (dev vs prod) and bulk source swapping
- **What's missing:** Document how to copy datasets/dataflows and swap data sources to replicate a lineage for dev/prod, and supported approaches for bulk re-mapping content to new datasets (incl. migrating to Cloud Amplifier/new providers).
- **Suggested location:** Extend s/article/360042923134.mdx (Copying a DataFlow) or add a migration how-to covering lineage replication for dev/prod and bulk source swapping (CLI and the relevant remap approaches). Nav under DataFlow Management.

- **Other referenced articles:** s/article/360042923134.mdx, s/article/360043437733.mdx

---

## `s/article/360043437753.mdx`
*Data Assembler Usage Guidelines (Legacy)* — area: Data Assembler

### Gap rank 279 (Medium, score 46.8) — Data Assembler: how to access and edit jobs
- **What's missing:** Document how to access Data Assembler (via its app/page + token), how to edit an existing job's settings, and how to create a new one.
- **Suggested location:** Add (or new article for) how to access Data Assembler (app/page + token), edit an existing job, and create a new job, to accompany s/article/360043437753.mdx (Data Assembler Usage Guidelines (Legacy)). Note legacy status.

---

## `s/article/360044258533.mdx`
*Writing Formulas in Magic ETL* — area: Datasets / ETL

### Gap rank 308 (Low, score 44.1) — Updating a single cell/value in a dataset (datasets are immutable to direct edits)
- **What's missing:** Document that datasets can't be directly cell-edited and the supported pattern to change a value (Magic ETL formula + CASE, or DataSet Forms).
- **Suggested location:** Add a short note (datasets aren't directly cell-editable; change values via a Magic ETL formula + CASE or DataSet Forms) to s/article/000005946.mdx (DataSet Fields) or Best Practices for Managing DataSets, linking the formula-tile article.

- **Other referenced articles:** s/article/000005946.mdx

---

## `s/article/4404652354583.mdx`
*DataFlows Disabled Due to Extended Inactivity* — area: Datasets / DataFlow / Administration

### Gap rank 252 (Medium, score 48.6) — Dataset/dataflow lifecycle: auto-deactivation, deletion permissions, output-dataset coupling, version recovery [JP]
- **What's missing:** Mostly feature requests, but documentable behaviors: when/why datasets auto-deactivate and how to reactivate, who can delete datasets and the ownership/share requirement, the impact of deleting an ETL output dataset, and support's workarounds (e.g. periodically opening a card to keep input datasets active).
- **Suggested location:** Extend s/article/4404652354583.mdx (DataFlows Disabled Due to Extended Inactivity) to cover input-dataset auto-deactivation and reactivation steps; document deletion permissions/ownership requirements and the consequence of deleting an ETL output dataset (cross-link DataSet Backup for recovery). Feature-request leaning; document current behaviors.

- **Other referenced articles:** s/article/4415792998935.mdx

---
