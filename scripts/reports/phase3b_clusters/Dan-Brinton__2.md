# Phase 3b cluster: Dan-Brinton__2

**Owning PM:** Dan Brinton
**Files in this cluster:** 5  |  **Gaps:** 7

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005241.mdx`
*SCIM (System for Cross-domain Identity Management) in Domo* — area: Governance & Security

### Gap rank 200 (Medium, score 51.8) — SSO / SCIM onboarding and IdP SSL certificate expiration handling
- **What's missing:** Practical SCIM onboarding walkthrough (KB exists but users want more), and clear guidance on 'Information your IdP may need' vs 'Information from your IdP' certificates — which certificate expirations affect SAML auth-request signing and what the customer must do (OIDC and non-signing SAML unaffected).
- **Suggested location:** Update the SSO configuration article to add an explicit section on the two certificates ('Information your IdP may need' vs 'from your IdP'), which expiration affects SAML auth-request signing, and what the customer must do (OIDC and non-signing SAML unaffected). Optionally expand the SCIM article with a fuller onboarding walkthrough.

- **Other referenced articles:** s/article/360042934374.mdx

---

## `s/article/000005326.mdx`
*Credit Monitoring* — area: Magic ETL (consumption / runtime)

### Gap rank 226 (Medium, score 50.2) — Magic ETL credit/runtime overage from runaway joins and long runs
- **What's missing:** Document how ETL credit consumption is driven by row counts (a bad join generating billions of rows), how to estimate/limit it, how to cancel runaway executions, and any existing protections.
- **Suggested location:** Add ETL consumption-driver guidance (row counts, runaway many-to-many joins, how to cancel an in-progress run) to s/article/000005326.mdx (Credit Monitoring) or a Magic ETL performance/cost article.

- **Other referenced articles:** s/article/4405156517527.mdx

---

## `s/article/000005492.mdx`
*Data Refresh Permissions* — area: Governance / Data Refresh Permissions

### Gap rank 162 (Medium, score 55.0) — Data Refresh Permissions: frequency floors and admin-only advanced schedules
- **What's missing:** Document available frequency floors (No restrictions / 15 min / 30 min / Hourly / Daily; no Manual), that non-admins cannot set advanced/sub-hourly schedules when the setting is on regardless of policy, and the policy-vs-role interaction.
- **Suggested location:** Update s/article/000005492.mdx to add: there is no 'Manual' frequency floor (Daily is the least frequent), and when Data Refresh Permissions is enabled only full admins can set advanced/sub-hourly schedules regardless of a user's policy. Clarify policy-vs-role interaction.

---

## `s/article/360042934294.mdx`
*Create and Manage Groups* — area: Governance & Security

### Gap rank 156 (Medium, score 55.5) — Dynamic groups: membership criteria, attributes not appearing, all-instance groups, role-based
- **What's missing:** How dynamic group Membership Criteria work: why custom/managed attributes don't show up (must be defined on people), that a blank/space criterion creates an all-instance group, lack of LIKE/contains logic, that email/role aren't native attributes, and the custom-managed-attribute workaround to group by role.
- **Suggested location:** Update s/article/360042934294.mdx (Create and Manage User Groups) with a 'Dynamic group membership criteria' deep-dive: which attributes appear and why, the blank-criterion = all-users behavior, no contains/LIKE matching, email/role not being native attributes, and the managed-attribute workaround for role-based groups.

### Gap rank 175 (Medium, score 53.8) — Group ownership limitations (dataflows, certification submission)
- **What's missing:** Document the scope of group ownership: datasets support it, dataflows do not, and certification requests go only to an individual owner (group members/admins can't approve). Note workarounds (group as co-owner) and current limits.
- **Suggested location:** Add a current-state limitations note to s/article/360043430613.mdx (Certify Cards and DataSets) and/or group docs: group ownership applies to datasets not dataflows, and certification submission requires an individual owner. (Two threads are ideas; the limitation is documentable now.)

- **Other referenced articles:** s/article/360043430613.mdx

---

## `s/article/360043438973.mdx`
*Manage User Roles and Grants* — area: Governance & Security (Roles & Grants / Navigation)

### Gap rank 168 (Medium, score 54.5) — Domo does not hide features/menus users lack permission for; default Admin role grant gaps
- **What's missing:** Feature requests, but documentable: that Domo does not hide menus for features a user lacks grants for, which grants the default Admin role does/doesn't include, why only the default Admin role can view all Support tickets, and that 'Assign Users to a Role' exposes full role/grant visibility.
- **Suggested location:** Update the Managing Custom Roles / roles-and-grants documentation to add documentable current-state facts: Domo does not hide menus/features a user lacks grants for; which grants the default Admin role includes/excludes; only the default Admin role can view all Support tickets; the 'Assign Users to a Role' grant exposes full role visibility. The hide-features and decoupling asks stay feature requests.

### Gap rank 321 (Low, score 42.7) — Custom roles / grant granularity (decoupling share from edit, per-tool grants, default-disabled)
- **What's missing:** Primarily feature requests. Documentable today: which implicit/coupled grants are required for actions (sharing pages requires Manage All Pages; Report Builder requires Edit Pages AND Edit Apps; Governance Toolkit requires broad admin grants), and how new grants are applied to existing custom roles on release.
- **Suggested location:** Update Managing Custom Roles (s/article/360043438973.mdx) to document implicit grant dependencies for common actions and the policy for how newly released grants are applied to existing custom roles. Decoupling/per-tool grants remain feature requests.

---
