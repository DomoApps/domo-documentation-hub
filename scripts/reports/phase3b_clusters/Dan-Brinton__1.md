# Phase 3b cluster: Dan-Brinton__1

**Owning PM:** Dan Brinton
**Files in this cluster:** 5  |  **Gaps:** 6

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360042925814.mdx`
*Configuring Notification and Alert Settings* — area: App Studio / Sharing & Notifications

### Gap rank 294 (Medium, score 45.6) — App Studio sharing notifications also send SMS text messages
- **What's missing:** Document where to control SMS vs email notifications (profile > settings > Notifications tab > uncheck SMS column for the share event) so users can suppress texts when sharing apps/cards.
- **Suggested location:** Update s/article/360042925814.mdx (Configuring Notification and Alert Settings): add/clarify that sharing an app can trigger an SMS and how to uncheck the SMS column for that event. Optionally cross-link from the App Studio Distribute section.

---

## `s/article/360042925994.mdx`
*Create an Alert for a DataSet* — area: Alerts

### Gap rank 247 (Medium, score 48.9) — Dataset alert reliability: data-type/exponential handling, View datasets, and triggered-report values
- **What's missing:** Documentation that dataset alerts don't work on View datasets (must use dataflow-output datasets), how numeric display/exponential values affect alert logic, and how to get the actual triggered value into a report (placeholder vs Triggered Reports behavior).
- **Suggested location:** Update s/article/360042925994.mdx (Create an Alert for a DataSet): add a Limitations/Notes section stating alerts run on stored datasets and not on View datasets (use the dataflow-output dataset instead), how numeric formatting/exponential display vs underlying float affects threshold evaluation, and how attached Triggered Reports resolve the actual value vs the 'Current alert value' placeholder.

- **Other referenced articles:** s/article/360043430373.mdx

### Gap rank 345 (Low, score 39.3) — Creating Project tasks from card/dataset alerts
- **What's missing:** How-to/troubleshooting for configuring an alert to create a task in a project: prerequisites (project ownership, correct project selection), why task creation can silently fail, and known limitations. Currently undocumented enough that the answer was 'reach out to Domo Support.'
- **Suggested location:** Update the alert articles (s/article/360042925994.mdx and/or Create an Alert for a Visualization Card 360043430513.mdx): expand the Task action documentation with prerequisites (project ownership/membership, selecting a valid project), expected behavior when the alert fires, and a short troubleshooting note for when no task is created.

---

## `s/article/360042934234.mdx`
*Admin Settings* — area: Governance

### Gap rank 324 (Low, score 42.6) — Mobile/iPad session timeout logging users out
- **What's missing:** Documentation pointing to the mobile idle timeout / Session Settings that govern how often mobile users must re-authenticate, and how to adjust it.
- **Suggested location:** Update the Authentication / Session Settings admin article (s/article/360042934234.mdx) to explicitly document the mobile idle timeout setting, how it differs from desktop session timeout, and that lowering/raising it controls how often mobile/iPad users must re-authenticate.

---

## `s/article/360043430513.mdx`
*Create an Alert for a Visualization Card* — area: Alerts

### Gap rank 137 (Medium, score 57.3) — Setting up alerts: required alertable metric, filtered cards, multi-dimension/aggregate conditions, single-email behavior
- **What's missing:** A practical how-to covering: alerts require an alertable metric (Summary Number); how card/page filters interact with alerts; workarounds via beast-mode flag + row-count alert; multi-metric alert bodies require Workflows/Triggered Reports; and the limitation that dataset alerts send one email for all triggered rows (no per-row alert).
- **Suggested location:** Update s/article/360043430513.mdx (Create an Alert for a Visualization Card) to add an 'Alert condition patterns and limitations' section: beast-mode flag + Summary Number/row-count workaround for %-change and two-dimension comparisons, that filtered-card alerts can be honored or unfiltered, and pointer to Workflows/Triggered Reports for multi-metric bodies. Update s/article/360042925994.mdx to note the single-email-per-trigger behavior.

- **Other referenced articles:** s/article/360042925994.mdx, s/article/360043430373.mdx

---

## `s/article/360043438953.mdx`
** — area: Administration / Connectors / Roles & grants

### Gap rank 267 (Medium, score 47.4) — Account sharing / new Account-management grants ('Sharing restricted by the system')
- **What's missing:** Document the recently-introduced Account-management grants, that the default Admin role lacks them (must create a custom role to grant), and how to enable account sharing.
- **Suggested location:** Update the System Roles reference (s/article/360043438953.mdx) and/or the connector account-sharing docs: document the Account-management grants, that default Admin lacks them, the need for a custom role, and the 'Sharing restricted by the system' (403) symptom.

---
