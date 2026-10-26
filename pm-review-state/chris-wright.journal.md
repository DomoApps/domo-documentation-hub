# PM Review Journal — Chris Wright

_Generated 2026-10-20 by `pm_review.py journal`. Do not hand-edit._

## Chris Wright — review journal

**Branch:** `restructure/pm/chris-wright` · **Baseline:** `—`

### Sessions

- `s1-2026-10-19` (2026-10-19 → 2026-10-20) by chris-wright
  - items: fc-085c06faa1, fc-08f19eea0e, fc-6cb9a7d233, fc-be0e32624f, fc-c1e9cb05b5, pmi-018515a89b, pmi-15df09eab0, pmi-16ee786ad4, pmi-225a986c27, pmi-2526d9c1d3, pmi-303b99d73d, pmi-35922a92e4, pmi-3702dafae7, pmi-48c8e64451, pmi-52ca080d0c, pmi-54656f909c, pmi-61f63153fa, pmi-6751fa329d, pmi-6d8a348c99, pmi-7c2038f54e, pmi-812ec3004c, pmi-8bd7d6868a, pmi-92f12de6b4, pmi-9bbcde7e78, pmi-a4ad8400ba, pmi-a58494a4d1, pmi-ba2f4e9f83, pmi-bda58ec18c, pmi-c20e2f1385, pmi-cb436a95be, pmi-d04c47db4e, pmi-d0cf35bd5d, pmi-ee0364eb7f, pmi-fa8d8774b9
  - commits: 0e0d85d2, f17e1b54

### Items

#### `dec-D4` [decision] decision|D4|1 — **pending**

#### `fc-6cb9a7d233` [fact-check] Analyze-and-Visualize-Overview.mdx — **approved** (rewrite-redo)
- 2026-10-19 approved — by chris-wright — Chris confirmed claim 1 (150+ chart types) and claim 3 (Beast Mode AI Assistant) correct as written. Grants were wrong: corrected to Edit Cards (cards), Edit Pages (create/edit dashboards), Edit Apps/App Studio (create/edit/share apps) — 'Create Pages and Apps' is not a real grant. Removed 'Domo Stories' (outdated term Domo no longer uses); Chris confirmed dashboards are themselves responsive across web/mobile/tablet/print. · commit 0e0d85d2 · diff: Required Grants -> Edit Cards / Edit Pages / Edit Apps (App Studio); removed Domo Stories bullet; FAQ responsiveness answer reframed to dashboards.
- 2026-10-19 approved — by chris-wright — Follow-up edits after Chris reviewed: (1) grants reworded to parallel 'Create, edit, and share <object>' for cards/dashboards/apps, 'in Analyzer' removed (you don't share cards in Analyzer); (2) 'Beast Mode' section renamed to 'Calculated Fields' per Chris — term swapped across Intro/excerpt/section/FAQ with a single '(Beast Mode)' gloss in the section body. Beast Mode AI Assistant kept (confirmed product name). SCOPE-C FOLLOW-UP: the 4 linked Beast Mode articles (What-is-Beast-Mode, 360043429913, 360043429933, 360042925474) still carry 'Beast Mode' titles — retitle to Calculated Fields when those articles come up as their own items / confirm product-wide rename. · commit f17e1b54 · diff: Parallel grant language; Beast Mode -> Calculated Fields across Intro/excerpt/heading/prose/FAQ (gloss once); link labels unchanged.

#### `fc-be0e32624f` [fact-check] Dynamic-Dropdowns-in-Table-Cards.mdx — **answered** (provide-answer)
- 2026-10-19 answered — by chris-wright — Chris confirmed the capability boundary and directed the update (couldn't open the file in his editor; reviewing the rendered content in chat). Standard Analyzer table card = display, drill paths, and action-links only; it does NOT support interactive in-cell controls (dropdowns, editable cells) or write-back. In-cell interactivity requires App Studio table elements, Domo Bricks, or the App Framework; writing data back requires a writeback connector, Workflows, or a pro-code app -> AppDB. Adding one explicit boundary sentence to the 'What a Standard Table Card Supports' section and burning the [pm-input] marker. · diff: Add explicit negative-boundary sentence; burn [pm-input] marker.

#### `fc-085c06faa1` [fact-check] Export-Domo-Data-to-Reports.mdx — **approved** (approve)
- 2026-10-19 approved — by chris-wright — Chris reviewed all claims and confirmed correct with no edits: native export formats/limits (4 MB cap, ~3M cells Mega / 1.5M Pivot, 100k/50k default rows, variables dropped from filenames), Pivot/Mega-only color export, Report Builder static output + 'Edit Report (Report Builder)' grant on by default for Admins/editors, and the Google Sheets Add-On behavior. No factual corrections needed.

#### `fc-08f19eea0e` [fact-check] What-is-a-Card.mdx — **approved** (rewrite-redo)
- 2026-10-19 approved — by chris-wright — Chris reviewed and approved after edits: (1) Edit Cards grant reworded to match Analyze & Visualize — 'Create, edit, and share cards' — plus venue 'in Analyzer or App Studio'. (2) Visualization cards now 'Built in Analyzer, App Studio, or Worksheets'. (3) 'App cards' card type relabeled to 'Pro-code components' (description reworded to custom-coded apps/visualizations; dropped App Studio/Appstore phrasing). (4) Build section 'built and edited in Analyzer, App Studio, and Worksheets'. (5) Beast Mode -> Calculated Fields, single '(Beast Mode)' gloss, link label kept. (6) Joins claim in the DataSet FAQ KEPT per Chris's explicit call (flagged as possibly inaccurate; PM chose to retain). · diff: Grant+venue; viz cards built Analyzer/App Studio/Worksheets; App cards -> Pro-code components; Build-section venue; Beast Mode -> Calculated Fields (gloss once); joins claim retained.

#### `fc-c1e9cb05b5` [fact-check] What-is-a-Dashboard.mdx — **approved** (rewrite-redo)
- 2026-10-19 approved — by chris-wright — Chris reviewed and approved after edits: (1) Grants fixed — removed bogus 'Create Pages and Apps'; single bullet 'Edit Pages — Create, edit, and share dashboards' (verb aligned to 'share' per Chris's AskUserQuestion choice; other two A&V articles already used 'share', so no edits there). (2) Domo Stories dropped — line 27 Stories clause removed; 'dashboard/page/Story' FAQ reduced to 'dashboard vs page'. (3) Line 38 'Capitalize Dashboard Filters when referring to this feature' editorial note KEPT per Chris's explicit call. (4) Scheduled-reports FAQ link to Collaborate Overview KEPT per Chris. Completes all 5 fact-checks. · diff: Grants -> 'Edit Pages: Create, edit, and share dashboards'; removed Domo Stories (line 27 + FAQ); line-38 note and scheduled-reports link retained per PM.

#### `pmi-61f63153fa` [pm-input] 360042923914.mdx — **answered** (provide-answer)
- 2026-10-19 answered — by chris-wright — Chris confirmed: multi-select Page Filters combine the individually selected values in a single column with OR logic (rows matching ANY checked value); there is no native AND within one column. Workarounds confirmed: separate Page Filters on different columns (combine with AND), or a Beast Mode indicator column filtered as one value. The restructure-drafted <Note> (lines 193-197) is accurate and kept as-is; burned the [pm-input] marker. (Beast Mode -> Calculated Fields terminology for this article pending Chris's standing-rule decision.) · diff: Confirmed OR-logic Note accurate; burned pm-input marker (no content change to the Note).
- 2026-10-19 answered — by chris-wright — Follow-up same sitting: Chris supplied screenshots of the Page Filter match-type dropdown. Added a 'Page Filter match types' Note documenting the three options — Selection (checkbox list, multi-select OR), Match values (string conditions: contains / does not contain / starts with / does not start with / ends with / does not end with), Aggregation (aggregated-measure filter; links to Aggregated Filters). All three confirmed by Chris via screenshots. Left the existing standalone 'Aggregated Filters' note in place (mildly redundant) pending Chris's call on removal. · diff: Added 'Page Filter match types' Note (Selection / Match values / Aggregation) above the OR-logic Note.

#### `pmi-9bbcde7e78` [pm-input] 360042923914.mdx — **answered** (provide-answer)
- 2026-10-19 answered — by chris-wright — Chris confirmed the workaround does NOT work: sharing a dashboard URL or bookmark with a specific Filter View applied does not reliably target that view for the recipient. Filter View sharing remains all-or-nothing (already documented in the Note above). The supported way to send a pre-filtered view is an in-app deep link with pfilters URL parameters — a SEPARATE mechanism from Filter Views (docs: s/article/360042932994 in-app deep links + s/article/360043430113 full pfilters syntax). Chris chose to leave pfilters content OUT of this Filter Views article for now, so no content added. Marker burned. · diff: Burned pm-input marker; no content change (workaround rejected as unreliable; pfilters cross-ref intentionally omitted per PM).

#### `pmi-6d8a348c99` [pm-input] 360042923914.mdx — **answered** (provide-answer)
- 2026-10-19 answered — by chris-wright — Chris's answers: (1) CONFIRMED — a Beast Mode calculation created only in Analyzer on a single card is NOT available as a Page Filter column unless it is saved to the DataSet. Added a caveat to the literal-values bullet so readers know the Beast Mode must be saved to the DataSet, not just created on the card. (2) DENIED as inaccurate — a table card CAN be controlled by multiple Page Filters; the forum-sourced 'one Page Filter per table card' claim is false and was omitted entirely (no content added). Marker burned. · diff: Added Beast-Mode-saved-to-DataSet caveat on the literal-values bullet; omitted the false one-filter-per-table-card claim; burned marker.

#### `pmi-ba2f4e9f83` [pm-input] 360042923914.mdx — **answered** (provide-answer)
- 2026-10-19 answered — by chris-wright — Chris confirmed both with a screenshot of the card Actions tab. (a) Individual cards opt out of dashboard filters at the CARD level via the 'Filter exceptions' section on the card's Actions tab, with three checkboxes: 'Allow filtering' (all filters incl. interaction filters), 'Allow global date' (the dashboard global date filter), and 'Allow segments'. Uncheck a box to exempt the card. (b) Corrected the forum claim: with interactive filters (on by DEFAULT per Chris), clicking an element HIGHLIGHTS the clicked card and filters the OTHER cards on the dashboard by the selection — it does not 'self-filter' the clicked card. Wrote two subsections ('Exempt a Card from Filters, Global Date, or Segments' and 'Interactive Filter Cards') and burned the marker. · diff: Added 'Exempt a Card...' subsection (Filter exceptions: Allow filtering / Allow global date / Allow segments) + 'Interactive Filter Cards' subsection (on by default; highlights clicked card, filters others); burned marker.

#### `pmi-16ee786ad4` [pm-input] 360042923914.mdx — **answered** (provide-answer)
- 2026-10-19 answered — by chris-wright — Chris confirmed accurate: the per-card 'Allow global date' setting is ON by default and must be enabled for the dashboard's global/dynamic date range filter to apply to that card. The existing troubleshooting bullet in 'Date Selector or Global Date Filter Not Filtering Cards' already documents this correctly, so no content change — just burned the marker. Per Chris, no 'this changed in a release' framing added (not needed for the KB). · diff: Confirmed existing global-date requirement bullet accurate; burned marker (no content change).

#### `pmi-bda58ec18c` [pm-input] 360042923914.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed: (1) a manual start/end date entry IS native — users set an exact window with the 'is between' option and enter a start and end date; (2) period over period is NOT available as a dashboard/page-level control; (3) the recommended approach for period-over-period is Variables (variable controls) — linked to Variables | Overview (7903767835031). Wrote a short paragraph in 'Flexible Date-Range Selection' and burned the marker. This clears all 6 markers in this article. · diff: Added 'is between' manual start/end note + period-over-period-not-native note pointing to Variables (7903767835031); burned final marker.

#### `pmi-54656f909c` [pm-input] 360042924034.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris: card save comments / version-history entries are not believed to surface in any Governance or DomoStats dataset, and he chose NOT to document anything about that (don't want to assert a dataset that may not exist). No content change — the existing 'Save Comments and Version History' section stays as-is; marker burned. · diff: No content change; burned marker (DomoStats/Governance claim intentionally left out per PM).

#### `pmi-a4ad8400ba` [pm-input] 360042924034.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris declined to document an auto-select rule: Domo does choose a date column for the card, but Chris doesn't believe there's a specific/deterministic rule behind it, so he does not want to state a rule that isn't accurate. Also did not want to document the change-steps or the 'no preferred default date field' feature-request claim. Removed the marker with no new content — the existing generic one-liner ('When a card is powered by a date column, Domo uses a date field to drive this control') stays as the accurate description. · diff: Burned marker; no content added (auto-select logic intentionally not documented per PM — no specific rule to state).

#### `pmi-52ca080d0c` [pm-input] 360042924034.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed the Notebook-card content (which card types support HTML/rich formatting, summary-number font, Notebook export limits) does NOT belong in this Analyzer interface reference — Notebook cards aren't part of Analyzer. Burned the marker; added nothing to this article. Not documented in the Notebook Card articles as part of this item (PM did not request that here). · diff: Burned marker; no content added (Notebook-card topic out of scope for the Analyzer reference per PM).

#### `pmi-c20e2f1385` [pm-input] 360042924054.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed Edit Cards is the Required Grant to open Analyzer (consistent with the Analyzer Layout article). Added a '## Required Grants' section using the standardized wording — 'Edit Cards — Create, edit, and share cards in Analyzer or App Studio' + grants link — and burned the marker. · diff: Added Required Grants section (Edit Cards); burned marker.

#### `pmi-48c8e64451` [pm-input] 360042924094.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed all three forum-reported drill behaviors as TRUE: (1) on a table/grid drill, clicking a value cell behaves differently from clicking a category label and can produce an error; (2) a single card cannot both drill in place AND apply a dashboard-wide filter — the workaround is to split it into two cards; (3) there is no bulk action to copy a drill path from one card to many. Added all three as bullets in the 'Drill Behavior and Limitations' section and burned the marker. · diff: Added 3 confirmed drill-limitation bullets (value-cell vs label error; no drill+dashboard-filter on one card; no bulk drill-path copy); burned marker.

#### `pmi-cb436a95be` [pm-input] 360042924454.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris chose to leave the precedence point out — the exact behavior for a matched-but-unvalued region (whether 'No Data' overrides a static SVG fill) is an unverified forum edge case and he doesn't believe it changed, so he doesn't want to assert it. Removed the contentious sentence from the Note (the claim that color rules and 'No Data' take precedence over the SVG fill for matched elements) while keeping the accurate, useful guidance: a static fill is honored only for UNMATCHED elements, and to keep an element a fixed color, don't let its identifier appear in the region column. Burned the marker. · diff: Removed unverified precedence sentence from the static-fill Note (kept the unmatched-element guidance); burned marker.

#### `pmi-2526d9c1d3` [pm-input] 360042924594.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris chose option A: do not enumerate a brittle list of chart types that lack trellis support. The existing guidance already covers it robustly — if the 'Trellis Categories' option doesn't appear in Chart Properties for a chart, that chart type doesn't support it (self-updating, no list to maintain). No content change; burned the marker. · diff: No content change; burned marker (no hard-coded unsupported-chart-type list per PM).

#### `pmi-8bd7d6868a` [pm-input] 360042925314.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris chose to leave the drafted 'Show a Total in the Center of a Donut Chart' paragraph as-is — did not want to pin down the exact control name (forum reported 'Legend Position = Inside') or the persistent-vs-hover detail. No content change; burned the marker. Existing paragraph (use Hover Legend Title Value + Title Text, position the legend inside the chart) stands. · diff: No content change; burned marker (exact control name left unspecified per PM).

#### `pmi-92f12de6b4` [pm-input] 360042932994.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Closed per review: Domo has no bulk or spreadsheet-based sharing option. Sharing is done through the Share dialog; to grant access to many users at once you share with a Group (already documented throughout this article). No content added; burned the marker. · diff: No content change; burned marker (no bulk/spreadsheet share — Groups is the many-at-once mechanism, already covered).

#### `pmi-ee0364eb7f` [pm-input] 360042932994.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed: there is no UI option to auto-generate a shareable link for a filtered page or card view — building the pfilters URL by hand (as documented in 'Link to a Filtered Page or Card View') is currently the way. The drafted Note stands as accurate; burned the marker. · diff: Confirmed by-hand pfilters link is the only method; burned marker (Note retained, no content change).

#### `pmi-3702dafae7` [pm-input] 360042934414.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed the required grant for managing company pages is 'Manage all company settings' (enabled for the Admin default role). Added a '## Required Grants' section in the standardized format and burned the marker. · diff: Added Required Grants section (Manage all company settings, Admin); burned marker.

#### `pmi-6751fa329d` [pm-input] 360043428053.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed the re-roled behavior: switching a stacked bar to a bar-and-line combination reassigns the series to line/bar ROLES by legend order (first=line, rest=bars) rather than keeping the stacked breakdown — it is not dropped or collapsed to a single bar. The drafted FAQ answer is accurate and stands. Kept the FAQ scoped to bar+line (its title/subject); YOY was not separately verified, so no YOY-specific claim was added. Burned the marker. · diff: Confirmed bar+line re-roling FAQ accurate; burned marker (FAQ kept bar+line-scoped, YOY not separately asserted).

#### `pmi-812ec3004c` [pm-input] 360043428593.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed (matches the article body, lines 31/47): deleting Cards requires card ownership, an Admin default role, or the 'Manage All Cards, Pages and Apps (App Studio)' grant (which also enables bulk delete in Admin Settings). Added a '## Required Grants' section mirroring that; burned the marker. · diff: Added Required Grants section (card ownership / Manage All Cards, Pages and Apps (App Studio) / Admin); burned marker.

#### `pmi-303b99d73d` [pm-input] 360043428613.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris corrected the frame: restricting card edit capability is NOT a Required Grants matter. Mechanism: a user with the Edit Cards grant can normally edit a card; to restrict, the owner LOCKS the card ('Only the owner and administrators can edit this card'), which blocks non-owner edits; to let SPECIFIC users edit a locked card, add them as additional OWNERS (a card can have multiple owners, each can edit). Did NOT add a Required Grants section; instead added a clarifying Note on the lock + multiple-owners mechanism after the lock procedure. Burned the marker. · diff: No Required Grants section (per PM); added Note on lock + multiple-owners mechanism; burned marker.

#### `pmi-225a986c27` [pm-input] 360043428713.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed part 1: in a table/Pivot Table the total (grand-total) row mirrors each column's own aggregation — an Average column yields an average of averages, not a sum — and there is currently no option to change the total-row aggregation. Documented that as a Note. Part 2 (the Beast Mode FIXED workaround reported as SUM(AVG(...) FIXED())) OMITTED per Chris — did not want to publish an unverified formula. Burned the marker. · diff: Added total-row-mirrors-aggregation Note; omitted the FIXED workaround per PM; burned marker.

#### `pmi-a58494a4d1` [pm-input] 360043428733.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed: keep the 'Top N and Ranking in Grouped and Nested Charts' section as-is — it's accurate. (Section is net-new: added in the restructure Phase 3b forum-gap pass, commit 12e53470, not present at baseline.) Forum claims resolved: (1) the draft stands — chart sorts rank categories as a whole (Sort on Totals + Maximum Bars); per-group Top N must be pre-computed in Magic ETL Rank & Window. (2) The RANK() OVER() Beast Mode workaround is REJECTED — Beast Mode has no window functions (the section itself says so); Magic ETL Rank & Window is the real per-group workaround. No content change; burned the marker. · diff: Kept accurate Top N section; rejected false Beast Mode RANK() OVER() claim; burned marker (no content change).

#### `pmi-35922a92e4` [pm-input] 360043428813.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris's calls: (1) CONFIRMED — color rules evaluate a single column and cannot reference another column's value (already documented). (2) No native per-row heatmap — kept the Magic ETL normalization workaround and ADDED emoji/Unicode indicators as an alternative per Chris; did NOT add the HTML-table Beast Mode (CONCAT + inline color) approach (Chris: don't want that). (3) Drill-path color follow-through requiring the colored column to be present in the drill view is TRUE, but Chris chose NOT to add it since it's not currently documented. Burned the marker. · diff: Added emoji/Unicode per-row-status alternative to the heatmap bullet (no HTML Beast Mode); #1 already covered; #3 intentionally not added; burned marker.

#### `pmi-d04c47db4e` [pm-input] 360043429293.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris reviewed the article and confirmed the existing content looks good — no additions needed. (2) 'A Single Value gauge shows one number; value + target + % requires a different gauge type' is already documented (Note + goal-vs-actual table) and confirmed. (1) Per-variant options matrix NOT added — out of scope for the Single Value Gauge article (belongs in Properties for Gauges if anywhere). (3) 'Multiple targets' and 'Beast Mode-driven dynamic gauge color not supported' feature-requests LEFT OUT. No content change; burned the marker. · diff: No content change (existing article confirmed good); matrix + feature-requests not added; burned marker.

#### `pmi-7c2038f54e` [pm-input] 360043429473.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed: Pivot Tables do not support HTML-link content, and an HTML-link column (e.g., a Beast Mode field outputting an HTML <a> link) breaks expand/collapse for the affected columns; use a Table chart for clickable HTML links. The drafted bullet is accurate and stands; burned the marker. · diff: Confirmed HTML-link-not-supported bullet accurate; burned marker (no content change).

#### `pmi-018515a89b` [pm-input] 360043429473.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed bullets 1-3 accurate as written: (1) measures in the Values region are columns-only (cannot display as rows); (2) Beast Mode cannot create new calculated pivot total/subtotal rows; (3) dynamic/unknown-column pivoting requires a MySQL DataFlow or R/Python scripting tile, not the native Magic ETL Pivot tile. (4) There is NO supported way to hide empty columns in a Pivot Table; Chris chose to leave that out (not documenting the absence). No content change; burned the marker. · diff: Confirmed existing bullets 1-3; #4 (hide empty columns) left out — no option exists; burned marker.

#### `pmi-d0cf35bd5d` [pm-input] 360043429473.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris chose option A: keep the conceptual TTM/annualized FAQ answer as-is (no built-in TTM layout; build the rolling window in Magic ETL via a month-offset/period-index column, then pivot on that index). Did NOT publish an exact Magic ETL calculation or Beast Mode expression — a precise formula is brittle and unverified, and the conceptual answer already points the right way. No content change; burned the marker. · diff: Kept conceptual TTM FAQ; no exact recipe published per PM; burned marker (no content change).

#### `pmi-15df09eab0` [pm-input] 360043429573.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris confirmed (1): HTML Tables are legacy and users should use the other table types. Updated the HTML Table entry in 'Which Table Type Should I Use?' to flag it as legacy and steer new tables to Mega/Pivot/Flex. Kept wording to 'legacy + use others' — did NOT assert a hard retirement date (none was given). (2) Agreed: Flex Table period-over-period column guidance is out of scope here (belongs in the Flex Table article 360043429073); nothing added for it. Burned the marker. · diff: Flagged HTML Table as legacy + steer to Mega/Pivot/Flex; Flex PoP left out (out of scope); burned marker.

#### `pmi-fa8d8774b9` [pm-input] 360043429793.mdx — **answered** (provide-answer)
- 2026-10-20 answered — by chris-wright — Chris chose A: keep the recommendation generic — to show more categories than fit on a native (non-scrolling) bar chart, split into groups with Trellis/Tiered Date Settings or use a horizontal-bar visualization from the App Store. Did NOT name a specific App Store Brick (brittle; Bricks change/can't verify). No content change; burned the marker. · diff: No content change; kept generic App Store horizontal-bar guidance (no specific Brick named per PM); burned marker.

#### `pmi-cd0070ea03` [pm-input] 360043429793.mdx — **pending**

#### `pmi-1195857267` [pm-input] 360043429793.mdx — **pending**

#### `pmi-b5259a9b2a` [pm-input] 360043429793.mdx — **pending**

#### `pmi-ed4be0b3b3` [pm-input] 360043430233.mdx — **pending**

#### `pmi-fb66637d9e` [pm-input] 360043430233.mdx — **pending**

#### `pmi-5744ce919d` [pm-input] 360043437813.mdx — **pending**

#### `pmi-635e5ee7b2` [pm-input] 360043437813.mdx — **pending**

#### `pmi-3054dcfa9e` [pm-input] 360043437813.mdx — **pending**

#### `pmi-57638a05e9` [pm-input] 360043437813.mdx — **pending**

#### `pmi-499fb23fb8` [pm-input] 360043437813.mdx — **pending**

#### `pmi-b771c6bc94` [pm-input] 4409575159191.mdx — **pending**

#### `pmi-3736799a0e` [pm-input] 4529227357975.mdx — **pending**

#### `pmi-8573a0a9fa` [pm-input] 4529227357975.mdx — **pending**

#### `pmi-bbfc6ded86` [pm-input] 7903767835031.mdx — **pending**

#### `pmi-9955eed9e3` [pm-input] Custom-Card-Visuals-with-HTML-and-Bricks.mdx — **pending**

#### `pmi-d5b548493f` [pm-input] Dataset-Level-Date-and-Fiscal-Calendar-Defaults.mdx — **pending**

#### `pmi-b81520271c` [pm-input] Domo-for-Mobile-Overview.mdx — **pending**

#### `pmi-829eeb0b48` [pm-input] Drill-to-Final-Data-Security.mdx — **pending**

#### `pmi-7a729cab92` [pm-input] Dynamic-Dropdowns-in-Table-Cards.mdx — **pending**

#### `pmi-389cb37e7e` [pm-input] Filter-Funnel-and-PDP-Shield-Icons.mdx — **pending**

#### `pmi-b73a6e1990` [pm-input] Filter-Null-and-Empty-Values.mdx — **pending**

#### `pmi-c94f3d2ca9` [pm-input] Multi-Language-Dashboards.mdx — **pending**

#### `pmi-ece1c8dc84` [pm-input] Troubleshoot-Cards-Not-Updating.mdx — **pending**

#### `pmi-b24c1401c8` [pm-input] Use-Worksheets.mdx — **pending**

#### `rt-855f7a9296` [read-through] Analyze-and-Visualize-Overview.mdx — **pending**
- source: git-added

#### `rt-dc02782d3b` [read-through] Dynamic-Dropdowns-in-Table-Cards.mdx — **pending**
- source: git-added

#### `rt-63baf4bc42` [read-through] Export-Domo-Data-to-Reports.mdx — **pending**
- source: git-added

#### `rt-fd251cd8ea` [read-through] What-is-a-Card.mdx — **pending**
- source: git-added

#### `rt-904a84f407` [read-through] What-is-a-Dashboard.mdx — **pending**
- source: git-added

