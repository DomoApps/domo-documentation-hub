# PM Review Brief: Ryan Despain

**Prepared for:** KB Restructure PM Review Meeting
**Features owned:** Approvals, Governance Toolkit, Projects & Tasks, Workflows
**Total articles in your area:** 38

> This document is your meeting guide. It shows how your content is being reorganized,
> which AI-generated articles need your fact-check, which articles need a dedicated
> info-gathering meeting before they can be written, and what changes are being made
> to your content area in response to Support KB Audit and community forum gap findings.

---

## 1. How Your Content Is Being Reorganized

The KB is moving from a flat feature encyclopedia to a story-driven structure organized
around **11 pillars** (user workflows). The table below shows where each of your feature
areas lands in the new structure.

| Feature | Articles | New Location |
|---------|----------|--------------|
| Approvals | 2 | Pillar 6: Build Apps & Automate |
| Governance Toolkit | 12 | Pillar 9: Administer & Govern |
| Projects & Tasks | 10 | Pillar 7: Share & Collaborate [D2: may → Archive if feature deprecated] |
| Workflows | 14 | TBD — not yet mapped |

### Notable Navigation Changes

- **Projects & Tasks (D2):** 10 articles currently in Share & Collaborate. If the feature is being phased out in favor of Workflows, these may belong in Archive. Confirm status.

- **PDP (Personalized Data Permissions):** PDP articles are in Administer & Govern (Pillar 9). The Governance Toolkit sits in the same pillar.

---

## 2. AI-Generated Articles — Your Fact-Check Required

_No Phase 3a synthesized articles are assigned to your feature area._

---

## 3. New Forum-Gap Articles and Open Placeholders

New articles in your area from the community-forum gap analysis (and the original
restructure plan). Some are **already drafted and need your fact-check**; others
**cannot be written until you supply information**. The two are separated below so
it's clear which is which.

### 3b. Forum-Gap Articles Already Drafted — Fact-Check Required

These articles have been **written** in response to the highest-demand community
forum gaps. Please read each draft and verify accuracy. A ⚠️ flag means the draft
also contains an open `[pm-input]` placeholder — see Section 3d for the exact ask.

| Rank | Article | What Was Synthesized / What to Verify |
|------|---------|---------------------------------------|
| 6 | `Workflows-Write-Data-Back.mdx` — *Write Data Back to a DataSet from Workflows* ⚠️ | Synthesized from 000005797 (Workflows Reference — read side only). Conceptual/decision guidance written; `[pm-input]` Ryan Despain: exact append/multiline-append action names + config steps |

### 3c. Forum-Gap Articles Awaiting Your Input — Cannot Be Written Yet

These forum gaps **cannot be written without your input** — the KB has no source
material and the mechanics are Domo-proprietary. A short dedicated meeting (or an
async written answer) is needed before drafting can begin.

| Rank | Intended Article | What You Need to Supply |
|------|------------------|-------------------------|
| 13 | `Workflows-Package-Administration.mdx` | Domo Users / DataSet package function signatures + params, ID-type requirements, createUser attribute limits, group-support status/version, executor-context permission rule |
| 44 | `Dataset-Archived-Lifecycle-State.mdx` | Definition/trigger of the archived / "not accessed" state, inactivity threshold, how to detect via DomoStats/Activity Log, AI-readiness/lineage interaction |
| 81 | `Schedule-Enterprise-Dataset-Copy.mdx` | Enterprise Data Copy native scheduling / specific-time options, the Dataset Copy connector's Advanced-tab time capability, the supported API/workflow trigger pattern |

### 3d. Open Article Placeholders — Your Answer Required

The items below are open `[pm-input]` placeholders where specific information from
you is needed before the content can be finalized. Each is a checkbox — check it
off once you've provided the answer.

- [ ] **`000005105.mdx`**
  confirm the exact Custom Query format and SQL dialect for DataSet Watchdog: whether the query must be a full SELECT with a table reference (and what to use for the table name) or only a condition, the SQL dialect (community reports indicate MySQL-style syntax), and how comments and backticks are handled. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005105.mdx`**
  confirm the execution/metrics-log retention and display limits (how many past runs are kept and shown in a job's execution log) and the scheduling behavior that determines which hour of the day an hourly job runs. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005171.mdx`**
  confirm the current status of the legacy Form Builder/Form Viewer (deprecated vs. still supported), the recommended migration path from it to App Studio/Advanced Forms, and the cause of the "Form not found" error and reports of Form Builder forms disappearing. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005171.mdx`**
  confirm (1) whether editable/linked tables that allow in-place editing of form-backed rows are on the roadmap, and (2) the current behavior when two or more forms target the same output/response DataSet (whether this is supported and whether it recently changed). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005171.mdx`**
  confirm whether a clickable URL or raw HTML placed in form question text, a question description, or a Title/Description question renders as a live link or formatted content, or as literal text, and which question types (if any) support links. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005171.mdx`**
  confirm the exact storage format of multi-select Multiple Choice answers in the response DataSet (single row, all selections in one cell) and the delimiter used (comma vs. other). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005171.mdx`**
  confirm whether Form Date/Time inputs can constrain selectable dates (a min/max range, or excluding weekends/holidays), and whether the App Studio Pro-Code Editor provides a supported workaround to restrict date selection. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005171.mdx`**
  confirm whether a form submission can capture the current app page filter/slicer context (for example, writing the active filter values into the response DataSet), or whether filters only affect which options a question displays. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005171.mdx`**
  confirm the supported pattern for reviewing/approving form submissions in a table: that an App Studio table element is read only and that inline edit/approve/write-back requires a Brick (rather than a native table action). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005171.mdx`**
  confirm whether bulk approval of form submissions or tasks is supported natively, and if so where it lives (for example, multi-select in the Task Center task list) versus requiring a Brick-based approach. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005171.mdx`**
  confirm the recommended controls for securing a publicly embedded, PII-collecting form Brick (for example, embed token or domain restrictions, response DataSet access, and any Domo-side guardrails). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005171.mdx`**
  confirm whether the form's underlying response/output DataSet must be explicitly shared with all participant users for the form to load and accept submissions, or whether app/workflow sharing alone is sufficient (community reports conflict with the current "automatically shared" statement). Also confirm the exact error strings "Error loading form" and "Failed to submit form." Synthesized from community forum reports; needs confirmation.

- [ ] **`000005172.mdx`**
  confirm that the automatic email sent when a task is created or assigned is governed by the per-user Manage notifications email method (and/or the queue-level Admin Notification Setting), and that no separate always-on task-assignment email exists outside these controls. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005172.mdx`**
  confirm the exact error string ("Assignee does not have update content access to queue") and that granting the assignee Update Content access to the queue is the correct and complete resolution. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005172.mdx`**
  confirm whether Task List columns are customizable, the exact control or menu used to add or remove columns, the available columns (including form-field or Task Identifier columns), and whether the selection is saved per user or per queue. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005172.mdx`**
  confirm the supported way to surface and filter Task Center queues inside an App Studio app (the exact component or approach, e.g., an App Studio Queue component vs. a Task Center dataset-backed card), the available filtering options (for example, by assignee or by task), and these reported known issues and their mitigations: (1) a white screen / React render loop when adding the queue component, and (2) in-queue filter selections resetting when the app is published or updated (and whether personalization mitigates this). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005173.mdx`**
  provide/confirm canonical signatures and examples for the DataSet library functions (for example, GetMetadata and CreateDatasetTag), and confirm the tag behavior: whether setting tags overwrites all existing tags with no native extend/remove option, and the exact function or endpoint used. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005173.mdx`**
  confirm the visibility rule for accounts in the Code Engine account-input dropdown: specifically why a shared, read-only service account can appear in the Accounts panel but not be selectable in the function dropdown (for example, a required account-share permission level), and the recommended fix. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005179.mdx`**
  confirm the supported way to pass a clicked App Studio component/button value into a triggered workflow as an input, how to identify which component triggered the workflow, and the recommended webform-plus-PDP write-back-to-record pattern. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005179.mdx`**
  confirm (1) whether a DataSet/Alert trigger can be configured to fire only after all of a workflow's inputs have updated ("all-inputs-updated" pattern) or its documented limitation, and (2) the supported way to prevent a workflow from starting a new execution while a prior execution is still in progress (preventing simultaneous/concurrent runs). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005179.mdx`**
  confirm the exact name, inputs, and returned fields of the Get Executor function (which returns information about the person or system that started the current execution) and where it appears in the action menu. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005179.mdx`**
  confirm where per-execution and per-step credit consumption is surfaced (executions list, execution details, or a separate consumption view) and how it is calculated. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005179.mdx`**
  confirm how failure and completion notifications are configured for a workflow and who receives them (the workflow owner, the executor, or a configured recipient list). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005179.mdx`**
  confirm the name and availability of the DomoStats Workflows dataset used to report on workflow executions and to build execution-info bricks. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005331.mdx`**
  confirm whether the editor supports copy/paste or duplication of a configured shape (and the keyboard or menu action for it), and confirm the caveat that a copied shape's parameter mappings are blanked and must be re-configured in the copy. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005331.mdx`**
  confirm whether a workflow can be exported/imported or otherwise ported to another Domo instance, or whether it must be rebuilt manually in the target instance (its DataSets, accounts, and functions being instance-specific). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005797.mdx`**
  confirm the supported way to terminate a single parallel branch without ending the other active branches (for example, routing that branch to its own End step vs. an unsupported scenario). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005797.mdx`**
  confirm what the attachments field of the Send Email/Notification function expects (Domo Files API file IDs), whether attachments are passed as a List(Number) of file IDs, and how to attach multiple files. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005797.mdx`**
  confirm whether the email body supports HTML, and any limitation on rendering hyperlinks (href) in the delivered email. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005797.mdx`**
  confirm the sender/From and Reply-To behavior (whether these are governed by the global Brand Kit SMTP configuration and therefore not per-message) and whether a CC field is supported. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005797.mdx`**
  confirm the supported recipient inputs (single Person vs. Person List variable, plain email addresses for non-Domo-user recipients, and recipients sourced from a DataSet column) and how to map a query-result object so that dynamic body fields populate instead of returning null. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005797.mdx`**
  confirm the custom-value format for Duration values used by Wait and timer shapes (community reports indicate ISO 8601 duration strings such as P3D for three days and PT2H for two hours). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005797.mdx`**
  confirm the supported pattern for obtaining the current date/time inside a workflow (for example, a Query Table CURDATE()/CURTIME() query or execution metadata), and confirm that dedicated system variables for the current date/time are on the roadmap. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005865.mdx`**
  confirm the best practice for having an AI Agent produce chart or HTML output suitable for embedding in an email (for example, the summarize-a-dashboard-and-email pattern), and how to troubleshoot a "Forbidden" error when testing an agent (likely a sharing/permission or model-access issue). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005865.mdx`**
  document how to pass a File attachment from a Form into an AI Agent Task: the attachment/variable types the agent accepts, how Filesets-enabled instances change attachment behavior, how attached images display in Task Center, and how to troubleshoot the AI Agent / Image-to-Text "Internal Server Error" (model selection and AI Service Layer settings, prompt parameter configuration). The AI Service Layer model/settings detail belongs in /s/article/000005369 and the Forms attachment configuration in /s/article/000005171. Synthesized from community forum reports; needs confirmation.

- [ ] **`360042925874.mdx`**
  confirm there is no native Workflows action for Projects & Tasks and that the supported automation path is a Code Engine function calling the Projects & Tasks API; provide the specific API/endpoint (and Code Engine package, if one exists) to link here, and note whether a native action is planned. Synthesized from a high-interest community forum thread; needs confirmation.

- [ ] **`360043437773.mdx`**
  confirm these are not currently supported: reusable recipient distribution lists (recipients must be added individually as users/groups), bulk management of multiple scheduled reports at once, and a conditional "send only when data is available" option. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043437773.mdx`**
  confirm whether a scheduled report can be delivered as a CSV attachment only, with no card image or link back to Domo in the email body. Synthesized from community forum reports; needs confirmation.

- [ ] **`360043437773.mdx`**
  confirm whether there is a documented limit on the number of scheduled reports per dashboard (or per instance) and the expected UI behavior when many reports are scheduled to run simultaneously. Synthesized from community forum reports; needs confirmation.

- [ ] **`4415800746391.mdx`**
  confirm whether the attribute key entered in the `Value` column is case-sensitive (must match the Key exactly as defined on the Attributes page). Synthesized from community forum reports; needs confirmation.

- [ ] **`4415826269335.mdx`**
  confirm how to identify the source instance of a Virtual DataSet from the destination side (the exact UI indicator or DataSet detail), and confirm the recommended guidance for choosing Virtual DataSets vs. a second Workbench job. Synthesized from community forum reports; needs confirmation.

- [ ] **`4415826269335.mdx`**
  confirm the diagnostic steps and expected behavior for cross-instance scenarios where the source and destination are fully separated (instance separation), including what to check when data stops after a separation and any additional Virtual DataSet create-failure causes beyond token, grants, PDP, and materialization. Synthesized from community forum reports; needs confirmation.

- [ ] **`6305057013527.mdx`**
  confirm whether product release notifications can be suppressed for embedded users, and the supported setting or method for doing so. Synthesized from community forum reports; needs confirmation.

- [ ] **`6305057013527.mdx`**
  confirm the recommended account-lifecycle pattern for temporarily deactivating a user (for example, converting to a Social role and/or transferring owned objects to a temporary holding group, then re-transferring on return), and how DataFlow ownership should be handled in that pattern. Synthesized from community forum reports; needs confirmation.

- [ ] **`6814561223959.mdx`**
  confirm which file-upload path exposes a "keep leading zeros" option (reported to be the newer CONNECT DATA > FILE uploader vs. others). Synthesized from community forum reports; needs confirmation.

- [ ] **`6814561223959.mdx`**
  confirm the Dataset View type-inference behavior: that CAST/CONVERT in a View may not persist the intended type and the recommended workaround (for example, CONCAT an empty string to force text), and whether this is expected behavior or a known issue. Synthesized from community forum reports; needs confirmation.

- [ ] **`Workflows-Write-Data-Back.mdx`**
  confirm the exact action names and configuration steps for writing data back to a DataSet from Workflows (for example, the append and multiline-append actions), including how values and delimiters are entered, how a list of rows is mapped to the write action, and how to create a new DataSet as the write target. Add a step-by-step configuration section once the action details are confirmed.

---

## 4. Changes Flagged by Support Gap Integrations

Two gap-fill analyses have been integrated into the restructure plan. This section
shows what changes are planned in your content area and what fact-check input reduces
hallucination risk in the updated articles.

### 4a. Support KB Audit Findings (Phase 4)

_No Support KB Audit retirements are currently assigned to your area._

### 4b. Community Forum Gap Analysis — Update Targets

**Critical update targets** (address alongside or immediately after Phase 3a):

| Rank | Article Area | Addition Needed | Fact-Check Info Needed |
|------|-------------|-----------------|------------------------|
| 12 | Workflows forms/tasks | Task Center setup; queue configuration; native approval flow patterns | Verify Task Center setup steps; confirm queue config options; review approval flow pattern accuracy |

**High priority update targets** (5 articles in your area):

| Rank | Score | Topic | Affected Area | Specific Addition Needed |
|------|-------|-------|---------------|--------------------------|
| 42 | 68.2 | Workflows interacting with Projects & Tasks | Workflows / Projects & Tasks | Whether and how Workflows can create/update Projects & Tasks items, and the Code Engine approach to  |
| 43 | 68.1 | Workflows: write-back/edit interface embedded in App Studio dashboards (clicked- | Workflows / App Studio write-back | Patterns for embedded write-back in App Studio (webform + PDP, or passing clicked app-component valu |
| 48 | 67.6 | Workflows Send Email / Notification function: sender/reply-to, CC, attachments,  | Workflows / Notifications & Send Email | Reference docs for the Workflows Send Email function: what the attachments field expects (Domo Files |
| 65 | 64.8 | Workflows: triggers, alerts, and dataflow/execution control flow | Workflows / Triggers & control flow | Guidance on Workflow trigger mechanisms (alerts, buttons, dataset / all-inputs-updated, DDX bricks,  |
| 92 | 62.0 | Workflows + AI Agents: summarizing dashboards/datasets and choosing models | Workflows / Domo AI | Best practices for AI Agent steps in Workflows: add datasets as Agent knowledge vs passing query res |

---

## Quick Actions Summary

A prioritized list of everything this document is asking of you:

| # | Action | Type | Est. Effort |
|---|--------|------|------------|
| 1 | Fact-check `Workflows-Write-Data-Back.mdx` (Rank 6 community request) | Fact-check | 20–30 min |
| 2 | Supply info to write `Workflows-Package-Administration.mdx` (Rank 13) | Info meeting | 30 min |
| 3 | Supply info to write `Dataset-Archived-Lifecycle-State.mdx` (Rank 44) | Info meeting | 30 min |
| 4 | Supply info to write `Schedule-Enterprise-Dataset-Copy.mdx` (Rank 81) | Info meeting | 30 min |
| 5 | **Open placeholder in `000005105.mdx`:** confirm the exact Custom Query format and SQL dialect for DataSet Watchdog: whet | **Answer required** | 15–30 min |
| 6 | **Open placeholder in `000005105.mdx`:** confirm the execution/metrics-log retention and display limits (how many past ru | **Answer required** | 15–30 min |
| 7 | **Open placeholder in `000005171.mdx`:** confirm the current status of the legacy Form Builder/Form Viewer (deprecated vs | **Answer required** | 15–30 min |
| 8 | **Open placeholder in `000005171.mdx`:** confirm (1) whether editable/linked tables that allow in-place editing of form-b | **Answer required** | 15–30 min |
| 9 | **Open placeholder in `000005171.mdx`:** confirm whether a clickable URL or raw HTML placed in form question text, a ques | **Answer required** | 15–30 min |
| 10 | **Open placeholder in `000005171.mdx`:** confirm the exact storage format of multi-select Multiple Choice answers in the  | **Answer required** | 15–30 min |
| 11 | **Open placeholder in `000005171.mdx`:** confirm whether Form Date/Time inputs can constrain selectable dates (a min/max  | **Answer required** | 15–30 min |
| 12 | **Open placeholder in `000005171.mdx`:** confirm whether a form submission can capture the current app page filter/slicer | **Answer required** | 15–30 min |
| 13 | **Open placeholder in `000005171.mdx`:** confirm the supported pattern for reviewing/approving form submissions in a tabl | **Answer required** | 15–30 min |
| 14 | **Open placeholder in `000005171.mdx`:** confirm whether bulk approval of form submissions or tasks is supported natively | **Answer required** | 15–30 min |
| 15 | **Open placeholder in `000005171.mdx`:** confirm the recommended controls for securing a publicly embedded, PII-collectin | **Answer required** | 15–30 min |
| 16 | **Open placeholder in `000005171.mdx`:** confirm whether the form's underlying response/output DataSet must be explicitly | **Answer required** | 15–30 min |
| 17 | **Open placeholder in `000005172.mdx`:** confirm that the automatic email sent when a task is created or assigned is gove | **Answer required** | 15–30 min |
| 18 | **Open placeholder in `000005172.mdx`:** confirm the exact error string ("Assignee does not have update content access to | **Answer required** | 15–30 min |
| 19 | **Open placeholder in `000005172.mdx`:** confirm whether Task List columns are customizable, the exact control or menu us | **Answer required** | 15–30 min |
| 20 | **Open placeholder in `000005172.mdx`:** confirm the supported way to surface and filter Task Center queues inside an App | **Answer required** | 15–30 min |
| 21 | **Open placeholder in `000005173.mdx`:** provide/confirm canonical signatures and examples for the DataSet library functi | **Answer required** | 15–30 min |
| 22 | **Open placeholder in `000005173.mdx`:** confirm the visibility rule for accounts in the Code Engine account-input dropdo | **Answer required** | 15–30 min |
| 23 | **Open placeholder in `000005179.mdx`:** confirm the supported way to pass a clicked App Studio component/button value in | **Answer required** | 15–30 min |
| 24 | **Open placeholder in `000005179.mdx`:** confirm (1) whether a DataSet/Alert trigger can be configured to fire only after | **Answer required** | 15–30 min |
| 25 | **Open placeholder in `000005179.mdx`:** confirm the exact name, inputs, and returned fields of the Get Executor function | **Answer required** | 15–30 min |
| 26 | **Open placeholder in `000005179.mdx`:** confirm where per-execution and per-step credit consumption is surfaced (executi | **Answer required** | 15–30 min |
| 27 | **Open placeholder in `000005179.mdx`:** confirm how failure and completion notifications are configured for a workflow a | **Answer required** | 15–30 min |
| 28 | **Open placeholder in `000005179.mdx`:** confirm the name and availability of the DomoStats Workflows dataset used to rep | **Answer required** | 15–30 min |
| 29 | **Open placeholder in `000005331.mdx`:** confirm whether the editor supports copy/paste or duplication of a configured sh | **Answer required** | 15–30 min |
| 30 | **Open placeholder in `000005331.mdx`:** confirm whether a workflow can be exported/imported or otherwise ported to anoth | **Answer required** | 15–30 min |
| 31 | **Open placeholder in `000005797.mdx`:** confirm the supported way to terminate a single parallel branch without ending t | **Answer required** | 15–30 min |
| 32 | **Open placeholder in `000005797.mdx`:** confirm what the attachments field of the Send Email/Notification function expec | **Answer required** | 15–30 min |
| 33 | **Open placeholder in `000005797.mdx`:** confirm whether the email body supports HTML, and any limitation on rendering hy | **Answer required** | 15–30 min |
| 34 | **Open placeholder in `000005797.mdx`:** confirm the sender/From and Reply-To behavior (whether these are governed by the | **Answer required** | 15–30 min |
| 35 | **Open placeholder in `000005797.mdx`:** confirm the supported recipient inputs (single Person vs | **Answer required** | 15–30 min |
| 36 | **Open placeholder in `000005797.mdx`:** confirm the custom-value format for Duration values used by Wait and timer shape | **Answer required** | 15–30 min |
| 37 | **Open placeholder in `000005797.mdx`:** confirm the supported pattern for obtaining the current date/time inside a workf | **Answer required** | 15–30 min |
| 38 | **Open placeholder in `000005865.mdx`:** confirm the best practice for having an AI Agent produce chart or HTML output su | **Answer required** | 15–30 min |
| 39 | **Open placeholder in `000005865.mdx`:** document how to pass a File attachment from a Form into an AI Agent Task: the at | **Answer required** | 15–30 min |
| 40 | **Open placeholder in `360042925874.mdx`:** confirm there is no native Workflows action for Projects & Tasks and that the su | **Answer required** | 15–30 min |
| 41 | **Open placeholder in `360043437773.mdx`:** confirm these are not currently supported: reusable recipient distribution lists | **Answer required** | 15–30 min |
| 42 | **Open placeholder in `360043437773.mdx`:** confirm whether a scheduled report can be delivered as a CSV attachment only, wi | **Answer required** | 15–30 min |
| 43 | **Open placeholder in `360043437773.mdx`:** confirm whether there is a documented limit on the number of scheduled reports p | **Answer required** | 15–30 min |
| 44 | **Open placeholder in `4415800746391.mdx`:** confirm whether the attribute key entered in the `Value` column is case-sensitiv | **Answer required** | 15–30 min |
| 45 | **Open placeholder in `4415826269335.mdx`:** confirm how to identify the source instance of a Virtual DataSet from the destin | **Answer required** | 15–30 min |
| 46 | **Open placeholder in `4415826269335.mdx`:** confirm the diagnostic steps and expected behavior for cross-instance scenarios  | **Answer required** | 15–30 min |
| 47 | **Open placeholder in `6305057013527.mdx`:** confirm whether product release notifications can be suppressed for embedded use | **Answer required** | 15–30 min |
| 48 | **Open placeholder in `6305057013527.mdx`:** confirm the recommended account-lifecycle pattern for temporarily deactivating a | **Answer required** | 15–30 min |
| 49 | **Open placeholder in `6814561223959.mdx`:** confirm which file-upload path exposes a "keep leading zeros" option (reported t | **Answer required** | 15–30 min |
| 50 | **Open placeholder in `6814561223959.mdx`:** confirm the Dataset View type-inference behavior: that CAST/CONVERT in a View ma | **Answer required** | 15–30 min |
| 51 | **Open placeholder in `Workflows-Write-Data-Back.mdx`:** confirm the exact action names and configuration steps for writing data back to  | **Answer required** | 15–30 min |
| 52 | Validate additions to: Workflows forms/tasks (Rank 12) | Review | 20 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
