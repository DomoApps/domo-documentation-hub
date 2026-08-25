# Phase 3b cluster: Ryan-Despain__1

**Owning PM:** Ryan Despain
**Files in this cluster:** 4  |  **Gaps:** 9

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005171.mdx`
*Forms* — area: App Studio / Forms

### Gap rank 129 (Medium, score 57.9) — App Studio Forms: restricting/validating date inputs (lock out weekends/holidays)
- **What's missing:** Document that App Studio Form date inputs cannot be constrained to exclude specific dates (weekends/holidays) and the Pro-Code Editor workaround.
- **Suggested location:** Update s/article/000005171.mdx (Date/Time question type): add a limitation note that date inputs can't exclude specific dates (weekends/holidays) and mention the Pro-Code Editor workaround.

### Gap rank 183 (Medium, score 53.2) — App Studio Forms: dropdown options from a dataset, editing existing records, custom thank-you, shared output dataset
- **What's missing:** Docs should cover: (1) configuring a form select field to source options from a dataset column (answer exists but users couldn't find it), (2) whether/how form responses can capture the current app filter/slicer context, (3) that forms create new rows only (no edit-in-place today) and the editable-tables roadmap, and (4) whether multiple forms can target the same storing dataset (behavior reportedly changed).
- **Suggested location:** Update s/article/000005171.mdx (Forms): the dataset-defined dropdown and cascading-filter pieces already exist (make them more discoverable), and add explicit notes that forms insert new rows only (no edit-in-place; point to editable/linked tables), and clarify multiple-forms-to-one-output-dataset behavior.

### Gap rank 264 (Medium, score 47.5) — App Studio Forms: dataset sharing requirement, submission errors, and 'Error loading form'
- **What's missing:** Documentation does not clearly state that the underlying form/output dataset must be shared with all participant users for forms to load and accept submissions. Users explicitly note 'Documentation claims this is unnecessary' and 'I can't find anything in KB.' Need a troubleshooting section for 'Error loading form' and 'Failed to submit form' that calls out dataset-sharing requirements and how to diagnose via browser network inspection.
- **Suggested location:** Update s/article/000005171.mdx (Forms): correct/clarify the sharing statement and add a troubleshooting subsection covering 'Error loading form' and 'Failed to submit form' that calls out the dataset-sharing requirement for participants and a browser-network-inspection diagnosis tip.

- **Other referenced articles:** s/article/000005295.mdx

### Gap rank 342 (Low, score 39.4) — App Studio Forms: dataset visibility, filtering choices, sorting, branching
- **What's missing:** Mostly feature requests. Documentation should cover how Forms bind to datasets (dataset-defined fields), current sorting/filtering behavior of Form choices, and the workaround of building pre-filtered datasets to limit choices.
- **Suggested location:** Update s/article/000005171.mdx (Define List Options): note the workaround of building a pre-filtered/sorted dataset to control choice options and ordering. Branching and dataset-governance views are feature requests.

### Gap rank 348 (Low, score 38.9) — Legacy Form Builder vs App Studio Forms confusion and Form Builder instability
- **What's missing:** Docs need to clarify the relationship/differences between the older Form Builder + Form Viewer and the newer App Studio Forms, including which is recommended, why Form Builder forms may vanish, and the 'Form not found' error. The user reports the existing Form Builder instructions don't work end-to-end.
- **Suggested location:** Update s/article/000005171.mdx (or the Advanced Forms overview): add a short note disambiguating legacy Form Builder + Form Viewer from current App Studio/Advanced Forms, state the recommended path, and note the 'Form not found'/disappearing-form failure mode.

- **Other referenced articles:** portal/Forms/Advanced-Forms/overview.mdx

---

## `s/article/000005172.mdx`
*Monitor Queues in Task Center* — area: App Studio / Queues (Task Center)

### Gap rank 186 (Medium, score 53.2) — App Studio Queues: white-screen on add, filters reset on app update, and filtering
- **What's missing:** Document Queue component behavior and known issues: the white-screen/React loop on add, that app publish/update reinitializes app state and resets in-queue filter selections (and how to mitigate via personalization), and how to filter queues by assignee/task within an app (Task Center dataset card approach and its limitations).
- **Suggested location:** Update s/article/000005172.mdx (Monitor Queues in Task Center) with an App Studio Queue component section covering filtering options and a known-issues/behavior note (state reset on app publish, white-screen mitigation). Alternatively add to the App Studio components docs.

---

## `s/article/000005173.mdx`
*Code Engine* — area: Code Engine / Workflows

### Gap rank 241 (Medium, score 49.4) — Code Engine method/library reference (dataset, credential, third-party API methods)
- **What's missing:** Need a full reference for Code Engine library methods (dataset functions like GetMetadata/CreateDatasetTag, credential access, third-party API calls) with signatures and examples. Also surfaced: tag manipulation overwrites all tags (no extend/remove), and a shared read-only service account appears in the Accounts panel but not in the dropdown selection.
- **Suggested location:** Expand portal/Automate-Actions/Code-Engine/javascript-libraries.mdx into a full method reference (dataset functions incl. GetMetadata/tag functions with the all-tags-overwrite limitation, credential/getAccount access, sendRequest patterns for product APIs) with signatures + examples. Add credential/account dropdown-visibility notes to limitations-and-troubleshooting.mdx.

- **Other referenced articles:** portal/Automate-Actions/Code-Engine/javascript-libraries.mdx, portal/Automate-Actions/Code-Engine/common-use-cases.mdx

---

## `s/article/4415826269335.mdx`
*Virtual DataSets* — area: Dataset Views

### Gap rank 231 (Medium, score 49.8) — Dataset Views joining limitations across source types / Cloud Amplifier
- **What's missing:** Documentation needs to clearly state which datasets/views can and cannot be joined: that Cloud Amplifier (Snowflake cloud) datasets can only join other same-type datasets in Views, that materialized vs non-materialized behave differently, and that UNION across views/sources is unsupported.
- **Suggested location:** Update the Dataset Views documentation: add a limitations note stating that Views can only join datasets of the same underlying type (e.g. Cloud Amplifier/Snowflake datasets join only other Snowflake datasets), that published/virtual datasets can't be joined, and that UNION across sources is unsupported.

- **Other referenced articles:** s/article/360045402273.mdx

### Gap rank 261 (Medium, score 47.7) — Federated data / cross-instance virtual datasets: understanding, federating PROD-to-UAT, troubleshooting
- **What's missing:** Document the cross-instance Virtual Dataset / federation workflow (Admin > Governance Toolkit, Publish), how the source-to-subscriber relationship works, how to identify the source, when to use Virtual Datasets vs a secondary Workbench, and troubleshooting when data stops (incl. instance-separation scenarios and create failures).
- **Suggested location:** Update s/article/4415826269335.mdx (Virtual DataSets) with a 'understanding and troubleshooting cross-instance federation' section: identifying the source instance, PROD-to-UAT federation, Virtual Datasets vs second Workbench, and what to check when data stops or a Virtual Dataset won't create.

- **Other referenced articles:** s/article/360045120554.mdx, s/article/000005675.mdx

---
