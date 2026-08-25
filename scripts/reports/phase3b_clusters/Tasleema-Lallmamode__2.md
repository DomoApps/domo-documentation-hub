# Phase 3b cluster: Tasleema-Lallmamode__2

**Owning PM:** Tasleema Lallmamode
**Files in this cluster:** 5  |  **Gaps:** 5

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005677.mdx`
*SharePoint Online Writeback Connector* — area: Connectors / Microsoft integration

### Gap rank 187 (Medium, score 52.8) — SharePoint / Microsoft Office connectors (Writeback config, lookup fields, Excel as a source)
- **What's missing:** Guidance on: SharePoint Writeback prerequisites and 'Your DataSet could not be created' troubleshooting (folders must pre-exist, naming, Azure app permissions); that the standard SharePoint connector returns lookup IDs not display values and the workaround; and that the Office Add-in is Domo-to-Excel only, with supported ways to bring Excel into Domo.
- **Suggested location:** Update the SharePoint Writeback connector article with 'DataSet could not be created' troubleshooting; update the SharePoint connector article with the lookup-ID-vs-display-value note; add an FAQ clarifying Office Add-in directionality and Excel-into-Domo options.

- **Other referenced articles:** s/article/000005503.mdx, s/article/000005146.mdx

---

## `s/article/360042929914.mdx`
*Pinterest Connector* — area: Connectors / Email connector

### Gap rank 193 (Medium, score 52.5) — Email connector: subject/attachment regex, CSV encoding, sender identification
- **What's missing:** Need documentation on: how subject/attachment-name regex actually works (it filters allow/deny, does NOT extract capture groups into columns), correct regex patterns to avoid dropping all rows, CSV vs CSV-UTF-8 encoding requirements, and the lack of any 'from' sender record. Sender tracking is also a feature request.
- **Suggested location:** Update the Email connector article: clarify that subject/attachment regex filters (allow/deny) and does not extract capture groups into columns, give safe regex examples, document the CSV vs CSV-UTF-8 encoding requirement, and note that the sender address is not captured (feature request).

---

## `s/article/360042931914.mdx`
*CSV SFTP Push Connector* — area: Connectors / File-based ingestion

### Gap rank 255 (Medium, score 48.2) — SFTP connector troubleshooting (directory read failures, SSH keys, GPG encryption)
- **What's missing:** Documentation on SFTP connector requirements/limitations: which SSH key types/formats Domo supports, any folder-count limits when listing directories, and whether GPG/PGP encryption is supported for SFTP Writeback (currently not built in; users resort to Jupyter or AWS).
- **Suggested location:** Update the SFTP connector article(s): document supported SSH key types/formats, any directory-listing limits, and that GPG/PGP encryption is not built in for SFTP Writeback (with the Jupyter/AWS workaround).

---

## `s/article/360052105454.mdx`
*JSON No Code OAuth Connector* — area: Connectors / JSON No Code

### Gap rank 151 (Medium, score 56.3) — JSON No Code connector limitations: JWT auth and pagination
- **What's missing:** Documentation should clarify which auth flows the JSON No Code connector supports (it does NOT handle JWT login/refresh), and provide a pagination guide covering supported methods (page-based vs next-token/cursor) with config examples and troubleshooting for hangs. JWT support is partly a feature request.
- **Suggested location:** Update the JSON No Code / JSON No Code OAuth connector article(s): add a 'Supported authentication' note (JWT login/refresh not supported) and a pagination section covering page-based vs next-token/cursor with examples and hang troubleshooting.

---

## `s/article/360052122294.mdx`
*About Partition Connectors* — area: Connectors / Dataset update modes

### Gap rank 240 (Medium, score 49.4) — Connector update methods: Append vs Replace vs Merge, partition behavior, detecting deletes
- **What's missing:** Clear documentation of connector update/import methods and edge cases: how Append handles schema/column changes and same-key updates, what Replace/Merge/partition (e.g. Snowflake Key Pair Partition 'Append') actually do, and how to detect hard-deleted source records. Partition update-option naming is confusing enough to require support calls.
- **Suggested location:** Update 'About Partition Connectors' (s/article/360052122294.mdx) and/or the Connector FAQs: add a clear reference for Append/Replace/Merge/partition behavior incl. schema/column changes, same-key updates, partition 'Append' semantics, and how to detect hard-deletes.

- **Other referenced articles:** s/article/360042926294.mdx

---
