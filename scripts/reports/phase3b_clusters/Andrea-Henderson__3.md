# Phase 3b cluster: Andrea-Henderson__3

**Owning PM:** Andrea Henderson
**Files in this cluster:** 5  |  **Gaps:** 7

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005741.mdx`
*Magic ETL Tiles: AI Services* — area: Magic ETL / AI Forecasting

### Gap rank 283 (Medium, score 46.6) — Universal AI Forecasting enablement and Magic ETL AI Forecasting tile failures
- **What's missing:** Document that Universal Forecasting is gated (button won't appear unless enabled by account team), and AI Forecasting tile data requirements/troubleshooting (preview works on a subset but full run fails due to nulls/data consistency/formatting).
- **Suggested location:** Update s/article/000005741.mdx (Magic ETL Tiles: AI Services): add an enablement note (Universal Forecasting is limited release, requires account-team enablement, otherwise the tile/button is unavailable) and a troubleshooting subsection on common run failures (nulls, inconsistent formatting) vs. successful previews.

---

## `s/article/360042923174.mdx`
*Changing the Owner of a DataFlow* — area: Magic ETL (ownership / collaboration)

### Gap rank 208 (Medium, score 51.3) — Magic ETL collaboration: group ownership and concurrent-edit locking (current-state facts)
- **What's missing:** Mostly feature requests, but documentable current-state facts: ETL ownership is single-user (no group ownership), ownership-transfer limitations, the DataFlow Sharing modal scope, and that non-owners who add an output aren't granted permissions on it.
- **Suggested location:** Add current-state limitations to s/article/360042923174.mdx (Changing the Owner of a DataFlow): single-user ownership (no group ownership), transfer limits, sharing-modal scope, and that a non-owner who adds an output isn't granted permission on it. (Feature-request heavy; document the facts.)

---

## `s/article/360042923234.mdx`
*Data Cleaning Operations Using SQL and Magic ETL DataFlows* — area: Magic ETL (data cleaning / type conversion)

### Gap rank 203 (Medium, score 51.6) — Handling nulls/empty strings and currency/type conversion in Magic ETL
- **What's missing:** Document reliable null/empty-to-zero recipes (COALESCE(NULLIF(TRIM(col),''),0) or Value Mapper) and why CASE sometimes fails, plus that Alter Columns can't cast strings with $, commas, or parentheses to numeric — strip them first (REPLACE; convert () to minus sign).
- **Suggested location:** Extend s/article/360042923234.mdx (Data Cleaning Operations) with concrete recipes: null/empty-to-zero via COALESCE(NULLIF(TRIM())) or Value Mapper, and stripping $/commas/parentheses before Alter Columns numeric casts (convert () to minus).

---

## `s/article/360043427653.mdx`
*Editing a Magic ETL DataFlow* — area: Magic ETL (search)

### Gap rank 258 (Medium, score 47.9) — Magic ETL search enhancements (search/replace, wildcard, tile-type, modified-vs-passthrough)
- **What's missing:** Primarily feature requests building on the shipped ETL search. Documentation action: when enhancements ship, document the search capabilities and scope (what is/isn't matched).
- **Suggested location:** Document the current ETL search scope (what fields/where it matches) in s/article/360043427653.mdx (Editing a Magic ETL DataFlow), and expand as enhancements ship. Feature-request heavy; document current capabilities now.

### Gap rank 310 (Low, score 43.5) — Exiting a full-screen Magic ETL without running it (Cancel/Save behavior)
- **What's missing:** Document that Save (without run) then Cancel returns you to Domo while preserving work; the exit path is non-obvious.
- **Suggested location:** Add a short note to s/article/360043427653.mdx (Editing a Magic ETL DataFlow) that Cancel (after optionally Save) exits the full-screen editor and returns to Domo while preserving work.

---

## `s/article/360057087393.mdx`
*Creating a Recursive/Snapshot DataFlow in Magic ETL* — area: Magic ETL (output datasets)

### Gap rank 191 (Medium, score 52.6) — Magic ETL output dataset targeting (point output to existing dataset, recursive-ETL exception, CLI remap)
- **What's missing:** State the rules: an output can equal an input only in a recursive ETL; you cannot natively point output to an arbitrary existing dataset; and the CLI list-dataflow/update-dataflow workaround remaps an output to an existing dataset ID. Users ask for a CLI doc link.
- **Suggested location:** Add a note to s/article/360057087393.mdx and/or 360043437733 stating the output-targeting rules (recursive-only output=input, no native arbitrary-existing-dataset target) and document/link the CLI update-dataflow remap procedure.

- **Other referenced articles:** s/article/360043437733.mdx

### Gap rank 332 (Low, score 41.4) — Snapshotting / historical datasets (recursive dataflow vs Dataset Copy append)
- **What's missing:** Document snapshot approaches and when to use each: Dataset Copy with APPEND (auto BATCH_LAST_RUN timestamp) vs recursive dataflow vs date-spine/calendar-join, and how to union current + historical.
- **Suggested location:** Add a 'choosing a snapshot approach' comparison to s/article/360057087393.mdx (Creating a Recursive/Snapshot DataFlow): recursive vs Dataset Copy APPEND (BATCH_LAST_RUN) vs date-spine, and how to keep current + historical together.

- **Other referenced articles:** s/article/360043428073.mdx

---
