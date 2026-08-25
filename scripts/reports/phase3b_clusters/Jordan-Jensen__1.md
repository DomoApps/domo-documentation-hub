# Phase 3b cluster: Jordan-Jensen__1

**Owning PM:** Jordan Jensen
**Files in this cluster:** 5  |  **Gaps:** 6

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/1500000406641.mdx`
** — area: Datasets - APIs / CLI

### Gap rank 346 (Low, score 39.3) — Setting upsert / primary key on a dataset (CLI vs pydomo/Python SDK)
- **What's missing:** Documentation should explain how to define an upsert/primary key on a dataset: the CLI define-upsert command, that pydomo doesn't support upsert keys natively, and the schema-based approach (schema-upsert.json) in the Python SDK to mark a column as an upsert key.
- **Suggested location:** Surface the define-upsert / upsert-key guidance outside the Inline Editing app context — either add a general 'Define an upsert key on a dataset' KB article in s/article/ (under Datasets/API nav) or add a note to the DataSet Update Methods article (s/article/360043430733.mdx) covering CLI define-upsert, the schema-upsert.json SDK approach, and that pydomo lacks native upsert-key support.

- **Other referenced articles:** s/article/36004740075.mdx

---

## `s/article/360043440393.mdx`
*Previewing and Exporting Your CourseBuilder App* — area: App Studio

### Gap rank 307 (Low, score 44.1) — Course Builder publish/upload to Domo fails
- **What's missing:** Troubleshooting documentation for Course Builder's Publish-to-Domo flow (blank screen / missing login prompt), including macOS Gatekeeper open steps and the correct publish sequence.
- **Suggested location:** Update s/article/360043440393.mdx (Previewing and Exporting Your CourseBuilder App) to add the blank-screen/no-login-prompt symptom to the publish-troubleshooting Warning, with macOS Gatekeeper open steps and the correct publish sequence.

- **Other referenced articles:** s/article/360042935674.mdx

---

## `s/article/360058792094.mdx`
*How to Create a Date or DateTime Format Tag in Campaigns* — area: Connectors

### Gap rank 314 (Low, score 43.2) — Campaigns app: re-subscribing after unsubscribe
- **What's missing:** Documentation of how to re-subscribe a recipient who used a campaign unsubscribe link (e.g. manually removing them from the unsubscribers list), since the email-reply method does not work.
- **Suggested location:** Update or add to the Campaigns app documentation set: add a short FAQ/section on the unsubscribe list and how to re-subscribe a recipient (manual removal from the unsubscribers list), noting the email-reply method does not work.

---

## `s/article/4412849158167.mdx`
*Cloud Integrations Overview* — area: Cloud Amplifier / Databricks integration

### Gap rank 318 (Low, score 43.0) — Cloud Amplifier (Databricks) non-en-US locale support
- **What's missing:** Feature/limitation: documentation should state the en-US locale requirement/limitation for Cloud Amplifier (Databricks) and any date-handling workaround (ETL DataFlow noted as high-overhead).
- **Suggested location:** Add a limitations note to the Cloud Integrations / Databricks integration docs: Cloud Amplifier (Databricks) supports en-US locale only, with implications for date-typed data in non-US locales and a workaround. Full locale support is a feature request.

---

## `s/article/Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx`
*Configure Data Freshness and Caching in Cloud Integrations* — area: Cloud Integrations / Cloud Amplifier

### Gap rank 341 (Low, score 39.5) — Cloud Amplifier dataset/view metadata: run history, last-run date, row counts
- **What's missing:** Documentation should explain why Cloud Amplifier datasets lack a History tab / accurate last-run + row-count metadata, how to interpret freshness for live-cached datasets, and any current workarounds. Mostly logged as Ideas but reflects a genuine documentation gap on expected metadata behavior.
- **Suggested location:** Update the Cloud Integrations Overview (s/article/4412849158167.mdx) or the freshness/caching article with a 'metadata behavior' note: why CA datasets/views don't show run history, accurate last-run time, or row counts, and how to interpret freshness for live data. Note that full run-history support is a feature request.

### Gap rank 361 (Low, score 30.0) — Overview page card query consumption against Cloud Amplifier (Snowflake)
- **What's missing:** Feature request, but a documentable behavior: opening the Overview page triggers a query per saved card against the live cloud source. Document this consumption behavior and any guidance to limit it.
- **Suggested location:** Add a brief consumption note (to the freshness/caching article or a Cloud Amplifier cost-management doc): opening the Overview page issues a query per saved card against the cloud source, and caching mitigates repeat loads. The limit/pause control is a feature request.

---
