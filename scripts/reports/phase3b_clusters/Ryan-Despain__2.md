# Phase 3b cluster: Ryan-Despain__2

**Owning PM:** Ryan Despain
**Files in this cluster:** 4  |  **Gaps:** 8

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005105.mdx`
*DataSet Watchdog* — area: Governance & Security

### Gap rank 205 (Medium, score 51.5) — Dataset Watchdog: configuration limits, frequency, and log retention
- **What's missing:** Document Dataset Watchdog behavior/limits: execution-log retention/display limits, why jobs run on particular hours, that UI-created jobs run hourly with no frequency control, and alert-spam considerations.
- **Suggested location:** Update s/article/000005105.mdx (DataSet Watchdog) with a behavior/limits section: UI-created jobs run hourly with no configurable frequency, execution-log retention/display limits, scheduling-hour behavior, and alert-frequency considerations.

### Gap rank 210 (Medium, score 51.2) — Dataset Watchdog custom query examples and limitations
- **What's missing:** Documentation should provide concrete custom-query examples for Dataset Watchdog, state the SQL dialect (MySQL syntax, backtick comments), single-dataset limitations, and constraints of the SQL prompt. Users explicitly call out the existing support article (000005105) lacks examples.
- **Suggested location:** Update s/article/000005105.mdx (DataSet Watchdog): add a 'Custom Query examples' section with 2-3 concrete queries (e.g. row-level condition, comparing two column values), state the SQL dialect/syntax (MySQL-style, backtick handling), the single-dataset/columns-must-exist constraint, and what a matching row triggers.

---

## `s/article/000005865.mdx`
*Build an AI Agent Task in Workflows* — area: Domo AI Agents / Workflows / Filesets

### Gap rank 126 (Medium, score 58.4) — AI Academy AI Agent / Image-to-Text workflows: passing Form file attachments, Filesets limitation, and agent errors
- **What's missing:** Document how to pass a file/attachment from a Form into an AI Agent, the attachment variable types, that Filesets-enabled instances change attachment behavior, how images display in Task Center, and troubleshooting AI Agent / Image-to-Text 'Internal Server Error' (model selection / AI Service Layer settings, prompt parameter config). Update the Image-to-Text tutorial pattern to reflect post-tutorial UI changes.
- **Suggested location:** Update s/article/000005865.mdx (Build an AI Agent Task) and s/article/000005369.mdx (AI Service Layer Integration) with: passing a Form File attachment into an agent, Filesets-enabled attachment-type behavior, image display in Task Center, and Internal Server Error troubleshooting (model/AI Service Layer settings, prompt params). Cross-link the Forms attachment section (000005171).

- **Other referenced articles:** s/article/000005369.mdx, s/article/000005171.mdx

### Gap rank 216 (Medium, score 50.6) — AI Academy episode follow-along: building an AI Agent / Marketing Agent (output mapping errors)
- **What's missing:** Needs documented, reproducible guidance for the AI Agent Task tutorial: how to configure output parameters/prompt so results map to outputs reliably, why results are inconsistent, and a place to access the prompts/sample datasets shared in the live-session chat (currently lost from recordings).
- **Suggested location:** Update s/article/000005865.mdx (Build an AI Agent Task in Workflows). Add a troubleshooting subsection: 'My agent drafts content but doesn't populate output parameters' covering how to write output (and child-property) descriptions so values map reliably, how to use the test panel to confirm outputs, and why results can vary with input values/prompt phrasing. The ephemeral AI Academy assets (prompts/sample files) are a training-content distribution issue rather than a KB doc gap.

- **Other referenced articles:** s/article/000005853.mdx, s/article/000005720.mdx

---

## `s/article/4415800746391.mdx`
*PDP Automation* — area: Governance & Security

### Gap rank 128 (Medium, score 58.1) — PDP Automation configuration with managed/custom attributes
- **What's missing:** PDP Automation policy value format against managed attributes (domo.policy.managed_<attribute>), that the Value column must hold the attribute key, key casing must match, and how to assign one user multiple values of the same attribute. Users say they 'missed it in the documentation.'
- **Suggested location:** Update s/article/4415800746391.mdx (PDP Automation): add an explicit note that attribute key casing must match, a worked example for assigning one user multiple values of the same attribute, and clarify custom/non-system attribute resolution. The base managed-attribute value syntax is already documented.

### Gap rank 343 (Low, score 39.4) — PDP Automation supporting column policies, not just row policies
- **What's missing:** Feature request, but documentation should clarify the current scope/limitation of PDP automation (row-level only; column masks manual).
- **Suggested location:** Add a one-line scope/limitation note to the PDP Automation article (s/article/4415800746391.mdx): PDP automation applies to row policies only; column masking must be configured manually per dataset. Column-policy automation is a feature request.

---

## `s/article/6305057013527.mdx`
*User Management* — area: Governance & Security

### Gap rank 190 (Medium, score 52.6) — Creating users without invite emails and bulk credential updates
- **What's missing:** How to create users without invite emails (CLI create-user without -i true, or admin 'Send invite email' toggle), whether bulk password/credential updates are possible, and how to suppress product release notifications for embedded users.
- **Suggested location:** Update the User Management article to document creating users without invite emails (the admin 'Send invite email' toggle and the CLI create-user -i flag), clarify whether bulk password/credential updates are supported, and how to suppress product release notifications for embedded users.

- **Other referenced articles:** s/article/360043437733.mdx

### Gap rank 298 (Medium, score 45.2) — Suspending/deactivating user accounts instead of deleting
- **What's missing:** Whether a true suspend/reactivate exists and the recommended workaround: convert to Social user and/or transfer owned objects to a temporary holding group, then re-transfer on return. This account-lifecycle pattern isn't documented.
- **Suggested location:** Update the User Management article (s/article/6305057013527.mdx) to address temporary deactivation: clarify there's no true suspend/reactivate, and document the recommended workaround (convert to Social user and/or transfer owned objects to a temporary holding group, then re-transfer on return; note DataFlows are the hard case).

---
