# Phase 3b cluster: Chris-Wright__1

**Owning PM:** Chris Wright
**Files in this cluster:** 5  |  **Gaps:** 7

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360042924034.mdx`
*Analyzer Layout* — area: Analyzer

### Gap rank 171 (Medium, score 54.4) — Card version history and Save-and-Comment storage / restore
- **What's missing:** Documentation of where card save comments live (Card Details > History) and whether they're queryable in DomoStats/Governance datasets, plus clarification that card History only shows a snapshot image and does not support version restore.
- **Suggested location:** Update s/article/360042923934.mdx (Card Details View Layout) to add a short subsection on the History tab: that it stores Save-and-Comment notes with a snapshot image, that there is no version-restore capability, and whether the comments surface in any Governance/DomoStats dataset. Cross-link from Analyzer Layout.

- **Other referenced articles:** s/article/360042923934.mdx

### Gap rank 335 (Low, score 41.1) — Default date field auto-selection on new cards (deprecated field shows no data)
- **What's missing:** Document how Domo chooses the default date field on a card, how to change the card's active date field, and that dataset owners cannot currently set a preferred default date field.
- **Suggested location:** Add a short note to s/article/360042924034.mdx (Analyzer Layout) or the date-filter article: how Domo selects the default date field on a new card, how to change the card's active date field, and that there's no dataset-owner preferred-default setting today.

---

## `s/article/360042924094.mdx`
*Add a Drill Path to Your Chart* — area: Analyzer / Dashboards / Drill Path

### Gap rank 132 (Medium, score 57.8) — Drill-down behavior, cross-card filtering, drill-path reuse and management
- **What's missing:** Document what drill interactions are/aren't supported: drilling does not cross-filter other cards; drill-in-place targets must be rebuilt (can't pick an existing card); value-cell vs category-label click behavior on table drills (and the error it can produce); the per-card 'prevent drilling to final data grid view' setting (no dashboard-level bulk option); no bulk copy of drill paths; no native drillable-card indicator.
- **Suggested location:** Update s/article/360042924094.mdx (Add a Drill Path to Your Chart) and s/article/360042923994.mdx (Drilling into Data) to add a 'Drill behavior and limitations' section: drilling does not cross-filter other cards; drill-in-place rebuilds rather than reusing an existing card; value-cell vs category-label click on table drills; per-card 'prevent drilling to final data grid view'; no bulk copy of drill paths.

- **Other referenced articles:** s/article/360042923994.mdx

### Gap rank 196 (Medium, score 52.1) — Drill paths: how to build, in-place drill + filter, visual cues, blocking drill-to-dataset
- **What's missing:** Documentation should: point to a drill-path how-to, clarify that a single card can't both drill-in-place and apply a global filter (split into two cards), suggest visual-cue conventions for drillable cards, and document the 'Edit Drill Path > Prevent Drilling to final data' setting.
- **Suggested location:** Update s/article/360042924094.mdx (Add a Drill Path to Your Chart): add notes that a single card cannot both drill-in-place and apply a dashboard-wide filter (split into two cards), and add a best-practice tip on signaling a drillable card (title hint/icon convention). The how-to, 'Drill in place', prevent-drilling, and drill-to-dataset are already documented.

- **Other referenced articles:** s/article/360042923994.mdx

---

## `s/article/360043429293.mdx`
*Single Value Gauge* — area: Analyzer / Chart types

### Gap rank 338 (Low, score 40.3) — Goal-vs-actual progress visualization options (chart-type selection)
- **What's missing:** Which panel/gauge chart types fit goal-vs-actual: thermometer, progress panel, waffle, range gauge, radial progress — a comparison/guidance doc on choosing among them for target tracking.
- **Suggested location:** Add a 'choosing a goal-vs-actual visualization' comparison (thermometer, progress panel, waffle, range gauge, radial progress) to the gauge/panel chart article or a chart-types overview. Overlaps with the goal/target-lines topic; could be one combined section.

---

## `s/article/4409575159191.mdx`
*Setting User-Specific Landing Pages* — area: App Studio / Mobile / Admin

### Gap rank 263 (Medium, score 47.6) — Landing pages: App Studio app / dashboard as landing on desktop vs mobile vs workspace
- **What's missing:** Documentable current-state limitation: the company default landing page (including an app) applies only to the desktop web app, not mobile; per-user app landing pages aren't supported.
- **Suggested location:** Update s/article/4409575159191.mdx to state the documentable limitations: landing pages accept a Dashboard or Card (not an App Studio app) and the company default landing page applies to desktop only, not mobile. Setting an app as landing / workspace-home landing remain feature requests.

---

## `s/article/Use-Worksheets.mdx`
*Use Worksheets* — area: App Studio / Editable Data / Worksheets / Projects & Tasks

### Gap rank 235 (Medium, score 49.6) — Building task-list / editable-data / CRM-style workflows in Domo (Worksheets, Projects & Tasks, editable tables)
- **What's missing:** Document the options and tradeoffs for editable/work-list use cases: Domo Worksheets, Projects & Tasks (and whether tasks can be powered by/tied to a dataset), editable-data features, and the roadmap for editable tables in App Studio (incl. Edit-in-Place for table components). Users explicitly hunt for the right feature.
- **Suggested location:** Add a decision/comparison section (likely a new short overview-style KB article in s/article/ or in the App Studio portal area) that maps work-list/editable-tracker use cases to Worksheets vs Projects & Tasks vs editable table components, cross-linking Use-Worksheets.mdx and the Projects & Tasks articles. Update those articles with 'when to use' framing.

- **Other referenced articles:** s/article/000005502.mdx

---
