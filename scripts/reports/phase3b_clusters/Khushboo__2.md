# Phase 3b cluster: Khushboo__2

**Owning PM:** Khushboo
**Files in this cluster:** 1  |  **Gaps:** 11

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/000005295.mdx`
** — area: App Studio / Editable & Linked Tables (beta)

### Gap rank 140 (Medium, score 56.9) — App Studio editable/linked tables: permissions and column controls (beta)
- **What's missing:** Document the permission requirements for editing data in editable/linked table cells (which grants are actually required - the permission-requires-Edit-Cards coupling) and current capabilities/limitations of linked tables. Column-control items are feature requests.
- **Suggested location:** Update s/article/000005295.mdx (or a dedicated Editable/Linked Tables article) to document the grants required to edit data in editable/linked table cells (incl. the Edit Cards requirement) and current linked-table column capabilities/limitations. Column-type/validation items are feature requests.

### Gap rank 143 (Medium, score 56.7) — App Studio 'last updated' on cards and dynamic text patterns
- **What's missing:** Document patterns for displaying a 'last updated' value on a card: storing it as a dataset field and surfacing via Smart Text in a notebook card, dynamic text box, or summary number with CONCAT.
- **Suggested location:** Update s/article/000005295.mdx (Add Text with a Notebook Card) with a short dynamic-text pattern for showing a 'last updated' value (dataset field + Smart Text / CONCAT summary number).

### Gap rank 177 (Medium, score 53.6) — App Studio filter UX patterns (too many filter cards, bulk-add, tabbed filters, legend display)
- **What's missing:** Document layout best practices for many filters (tabbed filter containers, Controls menu vs filter cards tradeoffs), the manual multi-step process to add filter cards (no bulk add), and that on-page legend visibility isn't independently controllable.
- **Suggested location:** Update s/article/000005295.mdx with a filter-layout best-practices note (tabbed filter container pattern, Controls vs filter cards). Mostly feature requests (bulk add, legend display).

- **Other referenced articles:** portal/embed/embed-in-sites-and-apps/filtering-options.mdx

### Gap rank 242 (Medium, score 49.1) — App Studio open-a-form-as-popup from text/image elements and filter context in popups
- **What's missing:** Document current behavior: only Button components can open a form popup (text/image cannot; button icons limited to Domo defaults), the Brick/Pro-Code workaround, and that filter selections aren't passed into a popup-opened form (vs inline form).
- **Suggested location:** Update s/article/000005171.mdx and/or s/article/000005295.mdx (Add a Button / Forms): document opening a form as a popup via a Button, that only Buttons (not text/image) can do this with default icons, and that filter selections aren't passed into the popup form (vs inline).

- **Other referenced articles:** s/article/000005171.mdx

### Gap rank 243 (Medium, score 49.0) — App Studio app organization: folders, tags, descriptions, title length, home page layout
- **What's missing:** Primarily feature requests. Doc-actionable: clarify current App Studio home organization options (favorites, alphabetical by title), the ~20-character title truncation, and document the folder-structure feature once released.
- **Suggested location:** Update s/article/000005295.mdx (Apps Home section): note the current organization options and limits; document the folder feature when it releases. Mostly feature-request, but current-state limitation note is documentable.

### Gap rank 253 (Medium, score 48.4) — App Studio / dashboard version control, undo-redo, and stuck full-screen mode
- **What's missing:** Document where undo/redo is available in App Studio today (shipped in the App Studio enhancements beta), that Sandbox provides versioning/rollback for App Studio apps and how to use it, and the fix for being stuck in full-screen/wide mode (clear cache, close sessions).
- **Suggested location:** Cross-link s/article/4403367344023.mdx (Sandbox App Studio repository) from s/article/000005295.mdx as the version-control/rollback path, and add a brief troubleshooting note for stuck full-screen (clear cache/close sessions). Undo/redo is already documented.

- **Other referenced articles:** s/article/4403367344023.mdx

### Gap rank 257 (Medium, score 48.1) — App Studio navigation behavior: hide menu/nav bar, secondary nav, mobile parity
- **What's missing:** Mostly feature requests. Document current options for hiding navigation/menu in apps and Domo Everywhere embeds, the known nav-shift/flash-on-load behavior, and how mobile vs. desktop navigation settings currently differ.
- **Suggested location:** Update s/article/000005295.mdx (App Studio Overview) and/or s/article/360043437993.mdx (Embed Content Outside of Domo) to document current options for suppressing system/Domo navigation in embedded apps, note the known logo nav-shift/flash-on-load behavior, and clarify how mobile vs desktop navigation/filter settings currently differ. Keep the remaining items framed as feature requests.

### Gap rank 259 (Medium, score 47.8) — App Studio navigation bar: Home button, nav buttons, custom icons, browser tabs
- **What's missing:** Mostly feature requests. Doc-actionable: document current nav-bar behavior - the Home button can be disabled but not relabeled, nav-bar buttons should use icons (text buttons appear invisible until hovered), how to exit an app, and that only built-in icons are available (no custom icon upload).
- **Suggested location:** Update s/article/000005295.mdx (Main Navigation / Custom Navigation sections): add notes that the Home button can be hidden but not relabeled, that nav buttons should use icons (text-only buttons appear invisible until hovered), and that only built-in icons are available. Mostly feature-request (custom icons 981 views).

### Gap rank 281 (Medium, score 46.6) — App Studio Homepage shows misleading 'Last Updated' for apps
- **What's missing:** Document what the App Studio 'Last Updated' timestamp reflects (app/layout edit time, not dataset refresh) and whether/how it can be hidden.
- **Suggested location:** Update s/article/000005295.mdx (Details/Apps Home): add a short note clarifying that the app 'Last Updated' timestamp reflects when the app/layout was edited, not when underlying data refreshed. Cheap, high-value clarification.

### Gap rank 288 (Medium, score 46.1) — App Studio formatting tables to fit card width with text wrapping
- **What's missing:** Document how to configure table cards in App Studio to fit card width and wrap text on resize (responsive table sizing settings).
- **Suggested location:** Update s/article/000005681.mdx or the Format Table Columns section of s/article/000005295.mdx with how to fit table columns to card width and enable text wrapping on resize.

- **Other referenced articles:** s/article/000005681.mdx

### Gap rank 355 (Low, score 37.0) — Filter View as a button action in App Studio (apply a saved filter view) + Clear Filters button behavior
- **What's missing:** Feature request for a 'select Filter View' button action; documentable now: where Filter Views live (Controls menu) and how the Clear Filters button action works/why it may not appear or function.
- **Suggested location:** Update s/article/000005295.mdx (Add a Button > Actions): document the Clear Filters button action and any conditions where it doesn't appear/work. The 'apply a saved Filter View' action is a feature request.

---
