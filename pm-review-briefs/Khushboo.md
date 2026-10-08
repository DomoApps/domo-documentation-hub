# PM Review Brief: Khushboo

**Prepared for:** KB Restructure PM Review Meeting
**Features owned:** App Dev Framework, App Studio, Bricks/Templates, MS Office Plugins / Addins, Publication Groups
**Total articles in your area:** 32

> This document is your meeting guide. It shows how your content is being reorganized,
> which AI-generated articles need your fact-check, which articles need a dedicated
> info-gathering meeting before they can be written, and what changes are being made
> to your content area in response to Support KB Audit and community forum gap findings.

---

## 1. How Your Content Is Being Reorganized

The KB is moving from a flat feature encyclopedia to a story-driven structure organized
around **11 pillars** (user workflows). The table below shows where each of your feature
areas lands in the new structure.

| Feature | Articles | New Location |
|---------|----------|--------------|
| App Dev Framework | 5 | Pillar 6: Build Apps & Automate |
| App Studio | 14 | Pillar 6: Build Apps & Automate |
| Bricks/Templates | 3 | Pillar 6: Build Apps & Automate |
| MS Office Plugins / Addins | 8 | Pillar 7: Share & Collaborate |
| Publication Groups | 2 | Pillar 7: Share & Collaborate |

### Notable Navigation Changes

- **CourseBuilder (9 EN articles):** Support KB Audit flags CourseBuilder as retired/removed from Domo Appstore. Staged for Retired in Phase 4.6. Pending D10: confirm CourseBuilder is gone from the product before the nav rebuild.

---

## 2. AI-Generated Articles — Your Fact-Check Required

These articles will be synthesized by AI from existing KB content in Phase 3a.
**They need your review before publishing.** Please read the draft and verify the
key claims listed — especially anything about product behavior, limitations, or
recommended patterns.

| # | Article | Synthesized From | Key Claims to Verify |
|---|---------|------------------|---------------------|
| 1 | `Getting-Started-for-App-Builders.mdx` (Pillar 1) | App Studio / Workflows overview articles | App builder journey, recommended starting tools, prerequisites, App Studio vs DDX scope |
| 2 | `What-is-App-Studio.mdx` (Pillar 6) | App Studio Overview articles | App Studio capabilities, no-code vs pro-code boundary, Code Engine integration |
| 3 | `Build-Apps-and-Automate-Overview.mdx` (Pillar 6) | App Studio, Workflows, Code Engine articles | Full app-building toolbox overview, App Studio vs Workflows use cases |

---

## 3. New Forum-Gap Articles and Open Placeholders

New articles in your area from the community-forum gap analysis (and the original
restructure plan). Some are **already drafted and need your fact-check**; others
**cannot be written until you supply information**. The two are separated below so
it's clear which is which.

### 3b. Forum-Gap Articles Already Drafted — Fact-Check Required

These articles have been **written** in response to the highest-demand community
forum gaps. Please read each draft and verify accuracy. A ⚠️ flag means the draft
also contains an open `[pm-input]` placeholder — see Section 3d for the exact ask.

| Rank | Article | What Was Synthesized / What to Verify |
|------|---------|---------------------------------------|
| 50 | `Write-Data-from-Pro-Code-Apps-to-AppDB.mdx` — *Write Data from an App to an AppDB Collection* | Synthesized from portal AppDB-API + manifest guides; links to Developer Portal reference. Omitted unverifiable bug narratives (new-collection-per-session, "Submitting" stuck state) |

### 3c. Forum-Gap Articles Awaiting Your Input — Cannot Be Written Yet

These forum gaps **cannot be written without your input** — the KB has no source
material and the mechanics are Domo-proprietary. A short dedicated meeting (or an
async written answer) is needed before drafting can begin.

| Rank | Intended Article | What You Need to Supply |
|------|------------------|-------------------------|
| 66 | `Troubleshoot-Office-PowerPoint-Add-In.mdx` | "Content couldn't be loaded" trigger + fix, re-authentication path, 0-rows condition (Date column / Excel-table requirement), Office version deps, legacy-plugin deprecation timeline |
| 69 | `Dashboard-Editor-Unresponsive-Multi-Select-Filter.mdx` | Confirm multi-select filter card as a reproducible cause, the isolate-by-removing-cards flow as supported, Domo-side fix vs browser-side mitigation |
| 83 | `Host-Images-for-Domo-Apps.mdx` | The `data-files` endpoint contract, how a FILE_ID is minted, beta Files feature scope/status, auth/size/type limits, internal-vs-external (S3/Azure/GCS) storage criteria |
| 100 | `App-Studio-Performance-with-Large-Datasets.mdx` | Filter-card load impact (group-by/aggregate behavior), why unfiltered raw card data is slow, dataset/view design recommendations and size thresholds |
| 109 | `Custom-Card-Visuals-with-HTML-and-Bricks.mdx` | HTML/CONCAT recipes + hyperlink pitfalls, avatar endpoint support (`/api/content/v1/avatar/...`), table-with-bars via Flex/Faceted bar, in-cell dropdown via bricks confirmation |
| 209 | `Workspaces-and-Folder-Organization.mdx` | How to create folders/sub-folders for apps/dashboards/data sources, grid vs list views, required grant/role, the grid-vs-list sub-folder visibility difference |

### 3d. Open Article Placeholders — Your Answer Required

The items below are open `[pm-input]` placeholders where specific information from
you is needed before the content can be finalized. Each is a checkbox — check it
off once you've provided the answer.

- [ ] **`000005143.mdx`**
  confirm the current state of relative date filtering for add-in imported content (available vs. roadmap) and how it differs from in-Domo relative date filters. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005143.mdx`**
  confirm the Excel re-import-in-place limitation vs. the legacy Office plug-in (what is and isn't supported when refreshing or replacing an already-imported DataSet in Excel, and the recommended workaround). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005143.mdx`**
  confirm whether Google Slides or other Google Workspace integration is planned. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005143.mdx`**
  confirm PowerPoint dashboard-import layout behavior vs. the legacy plug-in: whether each imported card is placed on its own slide, and how slide order and template are determined. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the current Apps Home organization options (alphabetical-by-title ordering, favorites, no folder/tag grouping), the exact app-title truncation length in the tile view (community reports cite roughly 20 characters), and that the "Last Updated" timestamp reflects app/layout edit time rather than dataset refresh (and whether it can be hidden). Document the folder-structure feature here once it releases. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm that App Studio sharing is app-level only (no per-page or per-group page visibility, and no per-page PDP), and that the recommended workaround is separate apps per audience. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm that the App Studio mobile layout is independent of the desktop layout (element position, size, and visibility can be set separately per view) and that desktop edits do not overwrite the mobile layout. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the per-tab card-sizing behavior on mobile: whether resizing a card in one tab propagates that size to cards in other tabs, and the supported way to give a card a different size on a specific tab. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm how tab and page order is determined on mobile (whether it follows the desktop Order tab) and whether there is a known issue in which mobile tab order can differ from desktop. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm there is no prompt or option to delete an app's underlying cards at the same time as the app (the cards always remain as orphans in the instance). Synthesized from a high-demand community forum thread; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm that App Studio app pages do not appear in a card's Move or Copy menu or in the card info panel, so a card cannot be traced to its parent app page through those menus. Synthesized from community forum reports; corroborates an open question in "Find Which Dashboard a Card Lives On"; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the exact way to delete cards from More > Admin > Cards (the menu path/label, for example an Edit > Delete action) and whether a filter or column exists to isolate the cards that belonged to a specific (or deleted) App Studio app page. The bulk "Add to dashboards" action is documented; the delete action and an App-page filter are not yet verified. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm whether the Domo Governance Datasets connector (or a Governance Toolkit / card lineage feature) is the recommended way to locate App Studio orphaned cards, and whether its reports actually map cards to App Studio app pages rather than only classic dashboards. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the interaction between the app-level background (App theme) and a page-level background (Format Page): that a page background paints over the app background and there is no transparency option to let the app background show through. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the conditional-formatting "Apply to" blank-column-list behavior when editing a card inside App Studio, and that the supported workaround is to edit the card on a traditional dashboard in Analyzer. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the current concurrent-editing behavior in App Studio: whether multiple users can safely edit the same app (or different pages of the same app) at once, and what happens to conflicting changes when each person saves. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm that rebuilding a page is the recommended recovery step for a corrupted App Studio page layout, and whether a support-assisted repair path exists. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm that Domo Sandbox is the supported versioning/rollback path for App Studio apps and the basic commit/restore steps, and confirm the resolution for an app stuck in full-screen/wide mode (clear cache, close other sessions). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm that a card's Filter Exceptions "Allow filtering" setting is all-or-nothing (there is no way to allow only specific filter columns to affect one card while ignoring others). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the reported behavior in which a filter selection persists visually in Controls but does not apply to cards, and the correct resolution. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm whether and how an app owner can limit which columns appear in Controls > Add Filter for viewers (for example, through a Filter Options setting or a per-DataSet configuration). Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the supported method for a dynamic/relative default date filter in App Studio (Filter Views with a relative range, and any Beast Mode approach), and the reported limitation that a dropdown filter card cannot supply a relative default date. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm that on-page filter controls must be added one at a time (no bulk-add action) and that grouping them in a Tabs or layout container is the recommended pattern for many-filter pages. The bulk-add action and independent on-page legend-visibility control are feature requests. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the current App Studio navigation behaviors: that text-only nav buttons appear invisible until hovered (icons recommended), that the Home button can be hidden but not relabeled or repointed, that only built-in icons are available (no custom icon upload), the exact controls for hiding app vs. system/Domo navigation in embedded apps and Domo Everywhere, the known logo/nav shift or flash-on-load behavior, and how mobile vs. desktop navigation and filter settings currently differ. Remaining requests (custom icon upload, secondary nav) are feature requests. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the tab nesting/save behavior (improperly nested components causing save failures) and the shared-height behavior with the Spacer workaround, including that the spacer workaround does not carry over to mobile. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the current limitations that a tab layout cannot be copied to another tab and that no navigation action (Page Drill or button) can deep-link to a specific tab within a page. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm that App Studio has no accordion/collapsible-section element today and that tabs or additional pages are the recommended alternative for long pages. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm that only Button components (not text or image elements) can open a Form as a pop-up, that button icons are limited to the built-in Domo set, and that page filter selections are not passed into a popup-opened form (whereas an inline form receives them). The Brick/Pro-Code workaround for a pop-up from other elements needs confirmation. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the supported settings for fitting table columns to card width and wrapping cell text on resize (responsive/auto-fit column sizing and a text-wrap toggle) in App Studio table cards. Only manual column resizing by dragging the header edge is documented today. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005295.mdx`**
  confirm the exact permission required to edit data in Editable/Linked Table cells within a published App Studio app (community reports indicate the viewer also needs the Edit Cards grant, coupling table-cell editing to card-edit permission), and document the current Linked Tables column capabilities and limitations. Column-type and cell-validation controls are feature requests. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005543.mdx`**
  confirm whether App Studio app themes override per-card color settings such as heatmaps and conditional formatting, whether an individual card can be made theme-independent, the supported workaround to preserve a card's own colors, and which theme setting controls the background of an expanded (pop-out) card view. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005543.mdx`**
  confirm which Brand Kit branding elements (beyond the built-in fonts) carry into App Studio automatically, and whether App Studio theme styling supports background transparency or custom CSS. Synthesized from community forum reports; needs confirmation.

- [ ] **`000005829.mdx`**
  confirm the current output/export formats for Report Builder reports (emailed snapshots) and whether PDF, PowerPoint, or A3 file export is supported or planned. synthesized from community forum reports; needs confirmation.

- [ ] **`000005829.mdx`**
  confirm which app changes do and do not propagate to an existing report automatically (layout, theme, added cards) versus data refreshing on each scheduled send. synthesized from community forum reports; needs confirmation.

- [ ] **`000005864.mdx`**
  confirm that a Filter List component sources its selectable values from the first DataSet alphabetically when a page contains multiple DataSets, and the supported workarounds (renaming a DataSet with a leading space so it sorts first, or unioning the DataSets into one). Synthesized from community forum reports; needs confirmation.

---

## 4. Changes Flagged by Support Gap Integrations

Two gap-fill analyses have been integrated into the restructure plan. This section
shows what changes are planned in your content area and what fact-check input reduces
hallucination risk in the updated articles.

### 4a. Support KB Audit Findings (Phase 4)

**Retirement batches in your area (Phase 4 execution plan):**

| Batch | Count | Action | Notes |
|-------|-------|--------|-------|
| CourseBuilder articles | 9 | → Retired (pending D10; staged for 4.6) | Support Audit flags CourseBuilder as retired from Domo Appstore. 9 EN articles. D10: confirm CourseBuilder is gone from the product; retire all if confirmed. |

### 4b. Community Forum Gap Analysis — Update Targets

**Critical update targets** (address alongside or immediately after Phase 3a):

| Rank | Article Area | Addition Needed | Fact-Check Info Needed |
|------|-------------|-----------------|------------------------|
| 4 | App Studio card management | Orphan card recovery procedure; delete-app-with-cards warning | Confirm orphan card recovery steps; verify what happens when you delete an app that contains cards |

**High priority update targets** (9 articles in your area):

| Rank | Score | Topic | Affected Area | Specific Addition Needed |
|------|-------|-------|---------------|--------------------------|
| 40 | 68.5 | App Studio mobile layout: independent mobile view, elongated charts, tab order | App Studio / Mobile | Document how the App Studio mobile layout works as an independent layout from desktop, how to adjust |
| 46 | 67.7 | App Studio Report Builder: capabilities, scheduling, export formats, filters, th | App Studio / Report Builder | Document Report Builder capabilities and limitations: how to rename a report (About > name), support |
| 53 | 66.3 | App Studio Forms: multi-select output stored as comma-separated single row | App Studio / Forms | Need documentation of the actual output behavior of multi-select form fields (one row, comma-separat |
| 63 | 64.9 | App Studio editor UX bugs and quirks (save behavior, background image override,  | App Studio / Editor | Document known editor behaviors and the editor-vs-Analyzer card editing introduced recently: save-ex |
| 72 | 64.4 | App Studio filter control: per-card scoping, persistence, exceptions, field sele | App Studio / Filters & Controls | Document filter mechanics in depth: persistent page filters, Filter Exceptions 'Allow Filtering' all |
| 76 | 64.2 | App Studio multi-user concurrent editing | App Studio / Collaboration | Document the current concurrent-editing capability and its limits (e.g., multiple users editing diff |
| 94 | 61.8 | App Studio Tabs: save errors, mobile stretching, shared height, layout copying,  | App Studio / Layout (Tabs) | Document Tabs gotchas: properly nesting components inside a tab (visual vs technical nesting causing |
| 97 | 61.6 | App Studio page-level / component-level access control (cannot share or hide ind | App Studio / Sharing & Permissions | Predominantly a feature request (page-level permissions don't exist). Doc-actionable: clearly docume |
| 110 | 60.0 | App Studio collapsible/accordion sections and broader dashboard layout/navigatio | App Studio / Layout (feature request) | Document that App Studio has no accordion/collapsible-section element today and the recommended alte |

---

## Quick Actions Summary

A prioritized list of everything this document is asking of you:

| # | Action | Type | Est. Effort |
|---|--------|------|------------|
| 1 | Confirm: CourseBuilder articles (9 articles) — retire or keep? | Decision | 15 min |
| 2 | Read and fact-check `Getting-Started-for-App-Builders.mdx` | Fact-check | 30–45 min |
| 3 | Read and fact-check `What-is-App-Studio.mdx` | Fact-check | 30–45 min |
| 4 | Read and fact-check `Build-Apps-and-Automate-Overview.mdx` | Fact-check | 30–45 min |
| 5 | Fact-check `Write-Data-from-Pro-Code-Apps-to-AppDB.mdx` (Rank 50 community request) | Fact-check | 20–30 min |
| 6 | Supply info to write `Troubleshoot-Office-PowerPoint-Add-In.mdx` (Rank 66) | Info meeting | 30 min |
| 7 | Supply info to write `Dashboard-Editor-Unresponsive-Multi-Select-Filter.mdx` (Rank 69) | Info meeting | 30 min |
| 8 | Supply info to write `Host-Images-for-Domo-Apps.mdx` (Rank 83) | Info meeting | 30 min |
| 9 | Supply info to write `App-Studio-Performance-with-Large-Datasets.mdx` (Rank 100) | Info meeting | 30 min |
| 10 | Supply info to write `Custom-Card-Visuals-with-HTML-and-Bricks.mdx` (Rank 109) | Info meeting | 30 min |
| 11 | Supply info to write `Workspaces-and-Folder-Organization.mdx` (Rank 209) | Info meeting | 30 min |
| 12 | **Open placeholder in `000005143.mdx`:** confirm the current state of relative date filtering for add-in imported content | **Answer required** | 15–30 min |
| 13 | **Open placeholder in `000005143.mdx`:** confirm the Excel re-import-in-place limitation vs | **Answer required** | 15–30 min |
| 14 | **Open placeholder in `000005143.mdx`:** confirm whether Google Slides or other Google Workspace integration is planned | **Answer required** | 15–30 min |
| 15 | **Open placeholder in `000005143.mdx`:** confirm PowerPoint dashboard-import layout behavior vs | **Answer required** | 15–30 min |
| 16 | **Open placeholder in `000005295.mdx`:** confirm the current Apps Home organization options (alphabetical-by-title orderi | **Answer required** | 15–30 min |
| 17 | **Open placeholder in `000005295.mdx`:** confirm that App Studio sharing is app-level only (no per-page or per-group page | **Answer required** | 15–30 min |
| 18 | **Open placeholder in `000005295.mdx`:** confirm that the App Studio mobile layout is independent of the desktop layout ( | **Answer required** | 15–30 min |
| 19 | **Open placeholder in `000005295.mdx`:** confirm the per-tab card-sizing behavior on mobile: whether resizing a card in o | **Answer required** | 15–30 min |
| 20 | **Open placeholder in `000005295.mdx`:** confirm how tab and page order is determined on mobile (whether it follows the d | **Answer required** | 15–30 min |
| 21 | **Open placeholder in `000005295.mdx`:** confirm there is no prompt or option to delete an app's underlying cards at the  | **Answer required** | 15–30 min |
| 22 | **Open placeholder in `000005295.mdx`:** confirm that App Studio app pages do not appear in a card's Move or Copy menu or | **Answer required** | 15–30 min |
| 23 | **Open placeholder in `000005295.mdx`:** confirm the exact way to delete cards from More > Admin > Cards (the menu path/l | **Answer required** | 15–30 min |
| 24 | **Open placeholder in `000005295.mdx`:** confirm whether the Domo Governance Datasets connector (or a Governance Toolkit  | **Answer required** | 15–30 min |
| 25 | **Open placeholder in `000005295.mdx`:** confirm the interaction between the app-level background (App theme) and a page- | **Answer required** | 15–30 min |
| 26 | **Open placeholder in `000005295.mdx`:** confirm the conditional-formatting "Apply to" blank-column-list behavior when ed | **Answer required** | 15–30 min |
| 27 | **Open placeholder in `000005295.mdx`:** confirm the current concurrent-editing behavior in App Studio: whether multiple  | **Answer required** | 15–30 min |
| 28 | **Open placeholder in `000005295.mdx`:** confirm that rebuilding a page is the recommended recovery step for a corrupted  | **Answer required** | 15–30 min |
| 29 | **Open placeholder in `000005295.mdx`:** confirm that Domo Sandbox is the supported versioning/rollback path for App Stud | **Answer required** | 15–30 min |
| 30 | **Open placeholder in `000005295.mdx`:** confirm that a card's Filter Exceptions "Allow filtering" setting is all-or-noth | **Answer required** | 15–30 min |
| 31 | **Open placeholder in `000005295.mdx`:** confirm the reported behavior in which a filter selection persists visually in C | **Answer required** | 15–30 min |
| 32 | **Open placeholder in `000005295.mdx`:** confirm whether and how an app owner can limit which columns appear in Controls  | **Answer required** | 15–30 min |
| 33 | **Open placeholder in `000005295.mdx`:** confirm the supported method for a dynamic/relative default date filter in App S | **Answer required** | 15–30 min |
| 34 | **Open placeholder in `000005295.mdx`:** confirm that on-page filter controls must be added one at a time (no bulk-add ac | **Answer required** | 15–30 min |
| 35 | **Open placeholder in `000005295.mdx`:** confirm the current App Studio navigation behaviors: that text-only nav buttons  | **Answer required** | 15–30 min |
| 36 | **Open placeholder in `000005295.mdx`:** confirm the tab nesting/save behavior (improperly nested components causing save | **Answer required** | 15–30 min |
| 37 | **Open placeholder in `000005295.mdx`:** confirm the current limitations that a tab layout cannot be copied to another ta | **Answer required** | 15–30 min |
| 38 | **Open placeholder in `000005295.mdx`:** confirm that App Studio has no accordion/collapsible-section element today and t | **Answer required** | 15–30 min |
| 39 | **Open placeholder in `000005295.mdx`:** confirm that only Button components (not text or image elements) can open a Form | **Answer required** | 15–30 min |
| 40 | **Open placeholder in `000005295.mdx`:** confirm the supported settings for fitting table columns to card width and wrapp | **Answer required** | 15–30 min |
| 41 | **Open placeholder in `000005295.mdx`:** confirm the exact permission required to edit data in Editable/Linked Table cell | **Answer required** | 15–30 min |
| 42 | **Open placeholder in `000005543.mdx`:** confirm whether App Studio app themes override per-card color settings such as h | **Answer required** | 15–30 min |
| 43 | **Open placeholder in `000005543.mdx`:** confirm which Brand Kit branding elements (beyond the built-in fonts) carry into | **Answer required** | 15–30 min |
| 44 | **Open placeholder in `000005829.mdx`:** confirm the current output/export formats for Report Builder reports (emailed sn | **Answer required** | 15–30 min |
| 45 | **Open placeholder in `000005829.mdx`:** confirm which app changes do and do not propagate to an existing report automati | **Answer required** | 15–30 min |
| 46 | **Open placeholder in `000005864.mdx`:** confirm that a Filter List component sources its selectable values from the firs | **Answer required** | 15–30 min |
| 47 | Validate additions to: App Studio card management (Rank 4) | Review | 20 min |

---

_Generated by `scripts/build-pm-review-briefs.py` from RESTRUCTURE-MANIFEST.md (Phase 3a-Forum written + deferred tables), Article-PM-Ownership-Reference.mdx, _gaps_with_support.json, and s/article/ [pm-input] markers._
