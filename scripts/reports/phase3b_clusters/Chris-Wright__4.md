# Phase 3b cluster: Chris-Wright__4

**Owning PM:** Chris Wright
**Files in this cluster:** 4  |  **Gaps:** 6

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360042932994.mdx`
*Sharing and Removing Access to Cards and Dashboards* — area: Dashboards - Sharing / Permissions

### Gap rank 351 (Low, score 38.5) — Group access to dashboards intermittently failing (group vs individual share propagation)
- **What's missing:** Documentation should address group-vs-individual share propagation, the workaround (remove and re-share the page with the group), and the bulk 'upload spreadsheet' sharing approach.
- **Suggested location:** Update s/article/360042932994.mdx (Sharing and Removing Access to Cards and Dashboards): add a troubleshooting note that group-based access can occasionally fail to propagate to all members, with the workaround of removing and re-sharing the dashboard with the group, and reference the bulk spreadsheet sharing option if one exists.

---

## `s/article/360043428253.mdx`
*Manage Dashboards* — area: Dashboards - Navigation

### Gap rank 334 (Low, score 41.3) — Dashboard navigation aids: jump-to-section buttons, child-page TOC, manage-dashboards search/sort
- **What's missing:** Mostly feature requests, but the navigation-button workaround (text card with same-URL anchor link, or moving to App Studio with tabs) is documentable. The TOC card and Manage Dashboards search/sort are not native features.
- **Suggested location:** Update s/article/360043428253.mdx (Manage Dashboards) or a dashboard-building article to document the in-dashboard navigation-button workaround (text card with same-URL anchor link, or App Studio tabs). Note that Manage Dashboards search/sort and an auto-generated child-page TOC are not native features (feature requests).

---

## `s/article/360043437813.mdx`
*Export Visualization Cards* — area: Dashboards - Export

### Gap rank 256 (Medium, score 48.2) — Exporting cards to Excel/CSV - row limits, where to change them, and failures
- **What's missing:** Documentation should cover the Excel-export row-limit setting (defaults and how to raise it, where it lives), why it may be missing for some card/view types (e.g. drill-through views), how export limits count DataSet rows vs displayed pivot rows, and how the 'Warning: Not all the data is shown' message maps to export completeness.
- **Suggested location:** Update s/article/360043437813.mdx (Export Visualization Cards): add a section on the Excel-export row-limit setting - where it lives (Chart/Table Properties), the default and maximum, why it may be unavailable on certain views (e.g. drill-through), and clarify how the in-card 'Warning: Not all the data is shown / red header' relates to what actually exports. Cross-link from the Pivot Table article (360043429473).

- **Other referenced articles:** s/article/360043429473.mdx

### Gap rank 360 (Low, score 34.5) — Card-to-PowerPoint export file format (.ppt vs .pptx) and customization
- **What's missing:** Mostly feature requests, but documentation should state the current export file format (.ppt) and available export options so users know the limitation before hitting IT policy blocks.
- **Suggested location:** Update s/article/360043437813.mdx (Export Visualization Cards): add a Note stating the PowerPoint export file format produced (e.g. legacy .ppt) so IT-policy-restricted users know before exporting, and note that export layout/branding (disclaimers, logos) is not customizable. Mirror the note in 360043437893 if applicable.

- **Other referenced articles:** s/article/360043437893.mdx

---

## `s/article/4529227357975.mdx`
*Using Smart Text* — area: Dashboards - Smart Text

### Gap rank 220 (Medium, score 50.4) — Smart Text in titles to show literal filtered date ranges
- **What's missing:** Documentation should explain that Date range Smart Text outputs the named range label rather than literal date values, the limitations when a card isn't directly filtered, and how to combine with beast modes/variables to surface specific dates in a title.
- **Suggested location:** Update s/article/4529227357975.mdx (Using Smart Text): add a clarification/limitation note that Date range Smart Text renders the named range (e.g., 'This Week', 'All Time') rather than literal start/end dates, describe behavior when a card is not directly filtered, and add a tip on using a Variable + beast mode to display literal date values in the title.

### Gap rank 277 (Medium, score 46.9) — Smart text does not export / appear outside the card (Excel, scheduled reports, PowerPoint)
- **What's missing:** Document explicitly where smart text does and does not render (exports, scheduled reports, PowerPoint, search) and the workaround of putting the value into a dataset/calculated column or summary number, plus LISTAGG to surface multi-value filters.
- **Suggested location:** Update s/article/4529227357975.mdx (Using Smart Text): add a 'Where Smart Text appears' note/FAQ clarifying it renders only in the live card/dashboard/app view and does NOT carry into Excel/CSV exports, scheduled reports, or PowerPoint; document the workaround of surfacing the value via a Beast Mode/calculated column or summary number, and LISTAGG for multi-value filters.

- **Other referenced articles:** s/article/360043437813.mdx

---
