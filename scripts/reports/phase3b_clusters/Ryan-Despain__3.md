# Phase 3b cluster: Ryan-Despain__3

**Owning PM:** Ryan Despain
**Files in this cluster:** 4  |  **Gaps:** 9

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005179.mdx`
*Manage Workflows* — area: Workflows / Execution & monitoring

### Gap rank 119 (Medium, score 59.2) — Workflows: execution context, monitoring, credits, Get Executor, and the 1000-pass limit
- **What's missing:** Documentation of Workflow execution behavior and monitoring beyond the executions list: how Get Executor works, where to see credit consumption per execution/step, the 1000-runs-through-a-shape limit (raisable via support), failure/completion notification options (and who receives them), and the DomoStats Workflows dataset for building execution-info bricks.
- **Suggested location:** Update s/article/000005179.mdx (Manage Workflows) to add: Get Executor function semantics, per-execution/step credit visibility, failure/completion notification configuration and recipients, and the DomoStats Workflows dataset (for building execution-info bricks). Add the 1000-runs-through-a-shape limit (and that it can be raised via support) to portal/Automate-Actions/Workflows/troubleshooting.mdx.

- **Other referenced articles:** portal/Automate-Actions/Workflows/troubleshooting.mdx

---

## `s/article/000005331.mdx`
*Create a Workflow* — area: Workflows / Editor

### Gap rank 199 (Medium, score 51.9) — Workflows editor UI/usability: moving/copying shapes, reference guide, 'shapes need to be connected' error, porting
- **What's missing:** A reference guide for Workflow editor shapes and UI actions (copy/paste, drag), explanation of the 'shapes need to be connected' error, that workflows can't be ported across instances (must rebuild), and copying code from a Code Engine function.
- **Suggested location:** Update s/article/000005331.mdx (Create a Workflow) with an editor-actions section (moving/copying shapes and the parameter-blanking caveat) and a validation note explaining the 'All shapes need to be connected' error; add an explicit statement that workflows can't be ported across instances. Add copying code from a Code Engine function to s/article/000005173.mdx.

- **Other referenced articles:** s/article/000005797.mdx

---

## `s/article/000005797.mdx`
** — area: Workflows / Code Engine

### Gap rank 165 (Medium, score 54.8) — Workflows + Code Engine: account binding, metadata/tags, web crawler, remote instance, nullable objects
- **What's missing:** Documentation of Code Engine constraints in Workflows: account inputs are statically bound at compile time (no runtime account switching), Get Metadata tag-access limitations, the account 'external use' setting for remote-instance/external calls, web crawler auth, and object/child-property nullability.
- **Suggested location:** Update portal/Automate-Actions/Code-Engine/limitations-and-troubleshooting.mdx to document: static account binding (no runtime account switching across subscriber sites), Get Metadata tag-access limitation, the account 'external use' setting (required for remote-instance/external calls), web-crawler auth, and nullable child object properties. Add the external-use prerequisite to start-a-remote-workflow.mdx.

- **Other referenced articles:** portal/Automate-Actions/Code-Engine/limitations-and-troubleshooting.mdx, portal/Partner-Developers/Guides/start-a-remote-workflow.mdx

### Gap rank 302 (Medium, score 45.0) — Workflows: getting current date/time and duration handling
- **What's missing:** Documentation for obtaining current date/time inside a workflow and the duration data type format (ISO 8601, e.g. P3D/PT2H) required by the Wait/timer functions. 'System variables' are noted as on the roadmap.
- **Suggested location:** Update s/article/000005797.mdx (Workflows | Reference) Data Types section to add the ISO 8601 duration format (e.g. P3D, PT2H) for setting duration values used by Wait/timer functions, and add a short pattern for obtaining current date/time inside a workflow (Query Table CURDATE/CURTIME or execution metadata). Note system variables are on the roadmap.

---

## `s/article/360043437773.mdx`
*Scheduled Reports* — area: Reporting / Scheduled Reports

### Gap rank 145 (Medium, score 56.6) — Redesigned Scheduled Reports / Report Builder interface: empty Reports view, missing editing, theming, multi-card, link removal
- **What's missing:** Document the new Reports/Report Builder experience: why the default Reports view is blank and the dropdown (dashboard vs card) needed to see reports, where editing moved, that Report Builder emails use default theme / pull alternating row colors and require recreating the report after a theme change, how to include multiple cards in one scheduled email, and how to send a CSV without a card link.
- **Suggested location:** Update s/article/360043437773.mdx (Scheduled Reports): add an explicit note that the redesigned Reports/Admin Reports view can appear empty until you select a report type (dashboard vs card) in the navigation dropdown, and confirm where editing now lives. The Report Builder theming/alternating-row behavior and multi-card composition are already covered in 000005829 (cross-link). The 'send CSV without a link back' question maps to the card CSV attachment in 360043437773.

- **Other referenced articles:** s/article/000005829.mdx

### Gap rank 230 (Medium, score 50.0) — Scheduled Reports vs Workflows for recurring emails of dataset lists
- **What's missing:** Guidance on when to use a Scheduled Report (card-based) vs a Workflow for recurring emails, including sending to external (non-Domo) recipients and using a query result as the email body.
- **Suggested location:** Add a 'Scheduled Reports vs Workflows for recurring emails' decision note to s/article/360043437773.mdx (Scheduled Reports) and cross-link from the Workflows email function docs, covering external (non-Domo) recipients and using a query result as the email body (which also belongs in the Send Email gap above).

### Gap rank 266 (Medium, score 47.5) — Scheduled reports limit and offline/cached dashboard viewing
- **What's missing:** Documentation should state any limit on scheduled reports per dashboard and behavior when many are scheduled at the same time (UI not rendering them), and clarify that offline viewing isn't natively supported (mobile-app caching / browser-extension workarounds).
- **Suggested location:** Update s/article/360043437773.mdx (Scheduled Reports): add a note on any practical limit to the number of scheduled reports and behavior/UI when many are scheduled at the same time. Offline dashboard viewing has no related article - if pursued, add a short FAQ entry to a Dashboards/Mobile article (e.g. Get Started with Dashboards 360043428553) clarifying offline viewing is not natively supported.

### Gap rank 269 (Medium, score 47.2) — Managing other users' scheduled reports as an admin
- **What's missing:** Document the admin Scheduled Reports management page (More > Admin > Scheduled Reports): how to view, edit, cancel, and recreate scheduled reports for other users.
- **Suggested location:** Update s/article/360043437773.mdx (Scheduled Reports) to add an admin section on viewing/editing/canceling/recreating other users' scheduled reports via More > Admin > Scheduled Reports.

### Gap rank 336 (Low, score 41.0) — Scheduled report / alert delivery to Microsoft Teams renders broken
- **What's missing:** Primarily a product gap, but documentation should note the limitation/known issue with Teams report rendering vs Slack, and any supported delivery options. Also a separate request to toggle attachment on/off when editing an existing scheduled report.
- **Suggested location:** Update s/article/360043437773.mdx (Scheduled Reports) and/or the relevant Alerts article: add a known-issue/limitation note that scheduled reports and alerts may not render fully in Microsoft Teams (only header/footer) compared with Slack, and clarify supported delivery destinations. Also note whether the CSV attachment can be toggled on/off when editing an existing scheduled report.

---
