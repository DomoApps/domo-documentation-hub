# Phase 3b cluster: Chris-Wright__3

**Owning PM:** Chris Wright
**Files in this cluster:** 2  |  **Gaps:** 8

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360042924454.mdx`
*Custom Charts* — area: Charting & Analyzer / Maps

### Gap rank 222 (Medium, score 50.3) — Custom SVG / map charts (static fills, non-geo points, geography-level mismatch)
- **What's missing:** Documentation on: setting static fill in SVG (data-name vs id tags, editing fill before upload), how Domo matches SVG element IDs/data-name to dataset fields, 'No Data' coloring conflicts, representing a non-geographic value on a geo map (substitute province via Beast Mode), and geography-level mismatch (county data on a state map).
- **Suggested location:** Update s/article/360042924454.mdx (Custom Charts) with a 'Working with SVG element IDs and static fills' subsection: how Domo matches id/data-name to dataset fields, setting a static fill before upload, avoiding 'No Data' coloring conflicts, and the Beast Mode substitute-region trick for non-geographic points and geography-level mismatch.

- **Other referenced articles:** s/article/360043428933.mdx

---

## `s/article/7903767835031.mdx`
** — area: Charting & Analyzer / Filters

### Gap rank 123 (Medium, score 58.8) — Single-control multi-value selection / 'All' option in slicers and selectors (variable + Beast Mode pattern)
- **What's missing:** Documentation on building an 'All' / combined option using a Variable (Pills/Radio control) plus a Beast Mode filter (CASE WHEN Variable='All' THEN 'Include'...), saving the include/exclude filter to each card rather than as a slicer; and splitting/unpivoting delimited multi-value columns (Split Column + Dynamic Unpivot) so slicers show individual values. Native Select All in filters is a feature request.
- **Suggested location:** Add a worked example to s/article/7903767835031.mdx (Variables | Overview) or s/article/360043429313.mdx (Slicer/Selector Cards): building an 'All' option via a Variable + CASE WHEN Beast Mode include/exclude filter saved to each card. Document delimited-multi-value Split Column + Dynamic Unpivot in an ETL article. Note native Select All is a feature request.

- **Other referenced articles:** s/article/360043429313.mdx

### Gap rank 138 (Medium, score 57.2) — Reordering variable values / dynamic (dataset-driven) variable values
- **What's missing:** Feature request. Documentable current state: variable values can't be reordered (must remove and re-add) and are static (not dataset-driven).
- **Suggested location:** Add a brief current-state note to s/article/7903767835031.mdx: variable control values are static and entered manually (not populated from a dataset) and can't be reordered without re-creating them; the variable-driven series-switch (set Y-axis/series by variable value) is a documentable technique.

### Gap rank 150 (Medium, score 56.3) — Populating variable control options from a dataset field
- **What's missing:** How to dynamically populate variable control values from a dataset; currently the only path is a Workflows/CodeEngine distinct-list workaround.
- **Suggested location:** Add a current-state note + the Workflows/CodeEngine distinct-list workaround to s/article/7903767835031.mdx for populating variable options from a dataset.

### Gap rank 180 (Medium, score 53.4) — Date-type variable default to current date / dynamic defaults (and default to max available date)
- **What's missing:** Whether/how a date variable default can be dynamic (currently no documented way; highest-voted Variables idea), plus the 'Month to Date' saved date-picker for dynamic current-month defaults and the Magic ETL MAX(date) flag approach for 'up to max available date'.
- **Suggested location:** Add a note to s/article/7903767835031.mdx that date variable defaults are static (no dynamic 'today' default at present) and document the date-filter 'Month to Date' saved-default and Magic ETL MAX(date) flag workarounds for dynamic-to-latest defaults.

### Gap rank 195 (Medium, score 52.3) — Card titles after platform update / Smart Text titles not rendering
- **What's missing:** Document how to set/override card title font color (especially on dark backgrounds), explain the hover-text-vs-title duplication, and clarify Smart Text variable behavior in titles — notably that a variable only renders in the title when a non-default value is selected.
- **Suggested location:** Update s/article/7903767835031.mdx (Variables | Overview) or a Smart Text article to document that a variable renders in a card title only when a non-default value is selected. Add card-title font-color/dark-background guidance to a card-styling or Chart Properties article. The styling regression itself is a release item, not a doc gap.

### Gap rank 233 (Medium, score 49.6) — Fiscal calendar as a switchable variable
- **What's missing:** Whether fiscal/standard calendar can be exposed as a variable and how to build the workaround (custom calendar fields in dataflows + variable switching).
- **Suggested location:** Add a workaround note (custom calendar fields in a dataflow + variable-driven CASE to switch) to s/article/7903767835031.mdx or a fiscal-calendar article. Feature request otherwise.

### Gap rank 260 (Medium, score 47.7) — Variable management/governance (Variable Manager, sorting, formatting controls)
- **What's missing:** Where to find/manage all variables in an instance, whether DomoStats Variables datasets cover this, and how to sort/format variable controls.
- **Suggested location:** Make the 'where to view/manage all variables' guidance (Beast Mode Editor Variables tab + DomoStats Variables reports) more discoverable in s/article/7903767835031.mdx, and note current limits (no dedicated Manager UI, no control sorting/formatting). Otherwise feature request.

- **Other referenced articles:** s/article/360042925474.mdx

---
