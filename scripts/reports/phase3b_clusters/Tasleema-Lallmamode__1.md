# Phase 3b cluster: Tasleema-Lallmamode__1

**Owning PM:** Tasleema Lallmamode
**Files in this cluster:** 5  |  **Gaps:** 6

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005360.mdx`
*Connecting with the JSON No Code and JSON No Code OAuth connectors* — area: Connectors / Data Integration

### Gap rank 170 (Medium, score 54.5) — JSON No Code / OAuth connector for custom APIs (pagination, auth, bearer tokens)
- **What's missing:** Step-by-step guidance for the JSON No Code connector covering: configuring cursor-based pagination ('Get next page token from results', 'Add as a parameter'), authenticating with a bearer token / API key as a header parameter, and replicating a working Postman/curl GET request. Recommended fallback for unsupported APIs (Notion DB, Facebook Ads, Wistia, Meta Product Insights, Xero, Trade Desk).
- **Suggested location:** Update s/article/000005360.mdx with worked examples: a cursor/next-page-token pagination walkthrough, a bearer-token-as-header example, and a 'translate a working Postman/curl GET into JSON No Code' recipe. These are the exact recurring blockers.

- **Other referenced articles:** s/article/360043433473.mdx

---

## `s/article/360042926294.mdx`
*Connector FAQs and Troubleshooting* — area: Connectors / Data Integration

### Gap rank 134 (Medium, score 57.6) — Vague connector/dataflow error messages mapped to causes
- **What's missing:** Documentation mapping common generic connector errors to their real causes and fixes: 'Domo is ready but...', 'Failed to execute import successfully', 'Indexing failed: Empty primary key', 'schema has too many columns (max 1500)', plus how to retrieve the underlying API error (browser dev tools network tab).
- **Suggested location:** Update s/article/360042926294.mdx (Connector FAQs and Troubleshooting): expand the 'Troubleshooting Specific Errors' section with the common generic errors mapped to causes/fixes and a how-to for reading the underlying API error in the browser network tab.

### Gap rank 218 (Medium, score 50.6) — OAuth / API-credential auth on connectors blocked by MFA or Google Workspace app-access
- **What's missing:** A troubleshooting doc for connector authentication: using API credentials instead of username/password when MFA is enforced; the Google Workspace admin-console step to trust/approve the Domo app (same root cause as the prior Google Sheets fix); and configuring OAuth 2.0 refresh tokens so jobs don't silently return zero rows after the access token expires.
- **Suggested location:** Update s/article/360042926294.mdx (Connector FAQs and Troubleshooting) with three documentable fixes: use API credentials when the source enforces MFA; the Google Workspace admin-console step to trust/approve the Domo app; and OAuth token-expiry causing silent zero-row jobs and how to re-authorize. Root causes are external but the fixes are Domo-side documentable.

---

## `s/article/360042930734.mdx`
*Qualtrics Connector* — area: Connectors / Charting

### Gap rank 315 (Low, score 43.2) — Qualtrics connector: response labels vs values
- **What's missing:** Documentation note on the Qualtrics connector that response labels live in a separate 'Survey Response Choices' report which must be joined to 'Survey Responses' to chart by label.
- **Suggested location:** Update s/article/360042930734.mdx (Qualtrics Connector): add a note that response labels are in the 'Survey Response Choices' report and must be joined to 'Survey Responses' to chart by label.

---

## `s/article/7617841459223.mdx`
*Google Analytics 4 connector* — area: Connectors

### Gap rank 131 (Medium, score 57.9) — GA4 connector data not matching the GA4 platform (sampling / aggregation)
- **What's missing:** A GA4 connector troubleshooting note explaining that API data is sampled (so totals differ but directionality holds), and how to minimize discrepancies (match date format/grain to the platform, filter on the same properties/report types rather than aggregating granular data, reconcile unique metrics).
- **Suggested location:** Update s/article/7617841459223.mdx (Google Analytics 4 connector): add a 'Why my data doesn't match GA4' troubleshooting section covering sampling vs unsampling, matching date grain/format, filtering on the same report types/properties, and unique-metric aggregation behavior.

---

## `s/article/Databricks-Using-OAuth-M2M-Authentication-Connector.mdx`
*Databricks Using OAuth M2M Authentication Connector* — area: Connectors / Authentication

### Gap rank 337 (Low, score 40.6) — Service-principal / non-interactive OAuth for enterprise connectors (Databricks, etc.)
- **What's missing:** Largely a product feature request: connectors currently only support interactive user-based OAuth or PAT; users want service-principal auth (esp. Databricks/Azure). Documentation could clarify which auth methods each connector supports, but the core ask is a new capability.
- **Suggested location:** Documentable now: ensure the existing Databricks OAuth M2M connector article is discoverable and clearly positioned as the non-interactive/service-principal option; clarify supported auth methods on Databricks/Azure connector pages. The broader cross-connector service-principal support is a feature request to track.

---
