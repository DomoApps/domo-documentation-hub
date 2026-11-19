# PM Review Journal — Ken Boyer

_Generated 2026-11-06 by `pm_review.py journal`. Do not hand-edit._

## Ken Boyer — review journal

**Branch:** `restructure/pm/ken-boyer` · **Baseline:** `—`

### Sessions

- `s1-2026-10-14` (2026-10-14 → 2026-11-06) by ken-boyer
  - items: dec-D6, fc-320c41746e, fc-4fa898e7d5, fc-7724ee2ffe, fc-8ec9682411, fc-94945debd4, fc-f22a8fd312, pmi-243851692b, pmi-2d81ad740d, pmi-2e73961d4f, pmi-33f6f49122, pmi-53d9e7edd5, pmi-68861a25bf, pmi-78766422cd, pmi-8d2291b0f9, pmi-9699d36aac, pmi-9f7b820515, pmi-9fd7e4a27e, pmi-d8c6a8ad9b, pmi-d985dd4e2b, pmi-dfd19ab90d, rt-03896a75bd, rt-2bd1545200, rt-6b42e4ba50, rt-ae8f4df8f6, rt-b97dfa3616, rt-c75a531f0d
  - commits: 38f67fdb, 50c7479b, 55838257, 55c1e10d, 5800c7b7, a6a8201a, ac4c9d42, df90c70b, e0b72a1a, e9edcead

### Linked cross-article decisions

- **Retire AI Chat v1 (000005539); AI-Chat-v2 replaces it** _(supersede, 2026-10-19)_
  - items: pmi-2d81ad740d
  - articles: `000005539.mdx`, `AI-Chat-v2.mdx`
  - why: Ken Boyer (PM) during review: 000005539 'AI Chat v1' should have been removed and replaced with AI-Chat-v2. Apply in Phase 4.6 on the integration branch: set 000005539 lifecycle to retired (remove from nav, docs.json line with s/article/000005539), add a redirect 000005539 -> AI-Chat-v2, and retarget the 8 inbound links (000005812, 000005720, 000005295, 000005848, 000005698, 000005561, s/topic/0TO5w000000ZmGPGA0.mdx, s/topic/0TO5w000000ZmGPGA0/domoai.mdx). Ken already retargeted v1 links to AI-Chat-v2 in AI-and-Data-Science-Overview and What-is-Domo-AI on this branch.
- **Retire FileSets (000005849); rebranded to Domo Documents** _(supersede, 2026-10-19)_
  - items: pmi-78766422cd, fc-320c41746e
  - articles: `000005849.mdx`, `Documents.mdx`, `Extract-Data-from-PDFs-with-Domo-AI.mdx`
  - why: Ken Boyer (PM) during review: FileSets was rebranded to Domo Documents; files are now added to Document Collections. Retire 000005849 'Use FileSets to Gather Information from Unstructured Data' in favor of Documents.mdx. Apply in Phase 4.6 on the integration branch: set 000005849 lifecycle to retired (remove docs.json nav entry s/article/000005849), redirect 000005849 -> Documents, retarget the 4 inbound links (000005797, 000005904, s/topic/0TO5w000000ZmGPGA0.mdx, s/topic/0TO5w000000ZmGPGA0/domoai.mdx), and sweep remaining 'FileSet(s)' terminology to Documents / Document Collections. Already done on this branch: Extract-Data-from-PDFs-with-Domo-AI now references Documents instead of FileSets (fc-320c41746e).
- **Reassign Create-and-Use-Data-Models.mdx from Ken Boyer to Phil Fuchs (pending integration owner)** _(other, 2026-10-23)_
  - items: pmi-9f7b820515, pmi-2e73961d4f, pmi-243851692b
  - articles: `Create-and-Use-Data-Models.mdx`
  - why: Ken Boyer disclaimed ownership during review on 2026-10-23: the article belongs to Phil Fuchs. Attempted 'pm_review.py reassign' on update/fullRestructure; reassign itself succeeded, but regenerating with build-pm-ownership.py (no squad CSV present) changed the PM on 464 articles and the Feature on 514, plus 60 rows added / 15 removed — far beyond this one move. Nothing was committed or pushed; integration branch restored. Integration-branch owner to resolve the generator drift (likely needs the squad CSV), then re-run: reassign --article Create-and-Use-Data-Models.mdx --to 'Phil Fuchs' --from 'Ken Boyer' --decided-by 'Ken Boyer', regenerate, commit, propagate-ownership. Phil Fuchs then owns the 3 open questions (Sandbox/repo deployment limits, Bad Request error, Analyzer date-field errors).
- **Reassign Retrieve-Dataset-Source-Query-via-API.mdx from Ken Boyer to Tasleema Lallmamode (pending integration owner)** _(other, 2026-11-06)_
  - items: fc-7724ee2ffe, rt-ae8f4df8f6
  - articles: `Retrieve-Dataset-Source-Query-via-API.mdx`
  - why: Ken Boyer disclaimed ownership on 2026-11-06 and chose Tasleema Lallmamode (he also named Kory, who is not in the PM roster). Not applied: build-pm-ownership.py regeneration drift (see link-3) blocks reassignment. Once fixed, run: reassign --article Retrieve-Dataset-Source-Query-via-API.mdx --to 'Tasleema Lallmamode' --from 'Ken Boyer' --decided-by 'Ken Boyer', regenerate, commit, propagate-ownership. Open fact-check findings for Tasleema (verified against portal/API-Reference/Product-APIs/Datasets.mdx): (1) the streamId 25222 example in Step 1 comes from a Get Metadata response with transportType WEBFORM, contradicting Step 1's last sentence and the FAQ claim that webform/uploaded datasets have no streamId — suggest saying they may have a streamId but no query entry; (2) com.domo.connector.snowflakeunloadv2 is attributed to Stream Get dataProvider.key but comes from the Stream Create request's transport.description (portal Stream Get example returns dataProvider.key 'covid-19') — suggest removing the specific example. All six endpoints, the X-DOMO-Developer-Token header, the four portal links, and the non-'query' connector warning match the portal.

### Items

#### `dec-D6` [decision] decision|D6|1 — **approved** (approve)
- evidence: Consistent with fc-f22a8fd312, fc-94945debd4 (links retargeted to /portal/*) and pmi-68861a25bf (session-ID content belongs on Developer Portal)
- 2026-10-23 approved — by ken-boyer — Ken confirmed D6: the KB keeps short Develop & Integrate overview/hub pages plus tool-level articles (CLI, ODBC, SDKs, MCP). Detailed API and app-developer documentation lives on the Developer Portal (/portal/ in this docs hub); KB links point there rather than to developer.domo.com.

#### `fc-4fa898e7d5` [fact-check] AI-and-Data-Science-Overview.mdx — **approved** (rewrite-redo)
- 2026-10-14 rewrite-redo — by ken-boyer — Ken: Required Grants were wrong. Remove Manage All Company Settings; list the grants that actually gate AI & data science features: Create Jupyter Workspace (Data science in Jupyter), Use AI Services / Edit Conversational Agents / Edit Toolkits (AI Services), Edit Pages / Edit Cards (Content). · diff: Rewrite Required Grants section
- 2026-10-14 rewrite-redo — by ken-boyer — Ken: add AI Library link to the AI Agents section — it's where agents and Toolkits are built. · diff: Add AI Library link to AI Agents section
- 2026-10-14 rewrite-redo — by ken-boyer — Ken: add AI Reporting link to the DomoStats section — DomoStats AI reports cover AI usage monitoring. · diff: Add AI Reporting link to DomoStats section
- 2026-10-14 rewrite-redo — by ken-boyer — Ken: add an AI Chat reference to the FAQ answer on connecting AI Chat to DataSets. · diff: Add Use AI Chat link to FAQ 'How do I connect AI Chat to my own DataSets?'
- 2026-10-14 rewrite-redo — by ken-boyer — Ken: FAQ AI Chat link should point to the AI-Chat-v2 article, not Use AI Chat (000005539). · diff: Retarget FAQ AI Chat link to /s/article/AI-Chat-v2
- 2026-10-15 rewrite-redo — by ken-boyer — Ken: point the Domo AI section's AI Chat link at AI-Chat-v2 (instead of Use AI Chat, 000005539) for consistency with the FAQ. · diff: Retarget Domo AI section AI Chat link to /s/article/AI-Chat-v2; description from v2 excerpt
- 2026-10-15 approved — by ken-boyer — Ken approved after rewrite: Required Grants replaced with the actual gating grants (Create Jupyter Workspace, Use AI Services, Edit Conversational Agents, Edit Toolkits, Edit Pages, Edit Cards); added AI Library and AI Reporting links; AI Chat links retargeted to AI-Chat-v2. Remaining claims (features, links, FAQ, screenshot) confirmed. · commit 50c7479b · diff: Grants rewrite + 3 link additions/retargets

#### `fc-f22a8fd312` [fact-check] Develop-and-Integrate-Overview.mdx — **approved** (rewrite-redo)
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: Required Grants is wrong — developer tools need either the relevant Manage All (Admin) grant or Edit rights within the area being controlled, not specifically Can Create DataSets / Manage All Company Settings. · diff: Rewrite Required Grants as Manage-All vs Edit grants per area
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: add an MCP section linking to Domo-MCP — brief calls for MCP integration coverage and the article had none. · diff: Add Domo MCP section (Beta) linking Domo-MCP and Connect-AI-Tools-to-Domo-Using-MCP
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: remove the Beta badge from the Domo MCP section heading. · diff: Remove Beta badge from Domo MCP heading
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: auth FAQ conflated two methods. App Framework APIs use access tokens; Platform (OAuth) APIs use OAuth (client ID + secret). · diff: Rewrite auth FAQ to distinguish App Framework (access token) vs Platform (OAuth) APIs; link Manage Access Tokens + Manage API Clients
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: remove the outdated (Aug 2023) CLI screenshot. · diff: Remove CLI screenshot from Domo CLI section
- 2026-10-19 approved — by ken-boyer — Ken approved after rewrite: grants reframed as Manage All (Admin) vs Edit grants per area; added Domo MCP section (no Beta badge); auth FAQ split into App Framework = access token, Platform = OAuth; removed outdated CLI screenshot. Remaining sections and FAQs confirmed. · commit ac4c9d42 · diff: Grants rewrite, MCP section, auth FAQ split, screenshot removed

#### `fc-320c41746e` [fact-check] Extract-Data-from-PDFs-with-Domo-AI.mdx — **approved** (rewrite-redo)
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: remove references to Domo Bricks. · diff: Remove Domo Bricks from excerpt, Intro, and availability list
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: replace FileSets with the Documents feature throughout. · diff: Replace FileSets with Documents (Document Collections) in excerpt, Intro, section, FAQ, Related Articles; link Documents + Magic ETL Tiles: Documents
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: rename the Documents section heading to 'Work with Unstructured Data Using Documents'. · diff: Rename Documents section heading
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: add Required Grants — Use AI Services, Manage DataFlows, Edit Magic ETL v2 DataFlow. · diff: Add Required Grants section
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: also add Manage Workflows and Manage Documents grants. · diff: Add Manage Workflows + Manage Documents to Required Grants
- 2026-10-19 approved — by ken-boyer — Ken approved after rewrite: removed Domo Bricks; FileSets replaced by Documents (section renamed 'Work with Unstructured Data Using Documents'); Magic ETL Text Generation tile is the bulk-PDF best practice (S3/SFTP via Document Collection -> Collection Input -> Text Generation); Prepare Your Source PDFs removed; Required Grants added (Use AI Services, Manage DataFlows, Edit Magic ETL v2 DataFlow, Manage Workflows, Manage Documents). · commit 55c1e10d · diff: Bricks removed, FileSets->Documents, Magic ETL path, limits section removed, grants added

#### `fc-94945debd4` [fact-check] Getting-Started-for-Developers.mdx — **approved** (rewrite-redo)
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: swap Developer Documentation links to the docs-hub portal pages — Getting Started overview and API Reference overview (instead of developer.domo.com). · diff: Retarget Developer Documentation links to /portal/Getting-Started/overview and /portal/API-Reference/overview
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: remove the Domo Bricks link (consistent with removing Bricks references elsewhere). · diff: Remove Domo Bricks overview link from Build and Extend Apps
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: retarget the App Dev SDK link to the docs-hub portal Apps overview. · diff: Retarget App Dev SDK link to /portal/Apps/Overview
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: add MCP — brief asks about MCP integration availability; matches the MCP section added to Develop-and-Integrate-Overview. · diff: Add 'Connect AI Tools with MCP' section linking Domo-MCP and Connect-AI-Tools-to-Domo-Using-MCP
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: mention MCP in the excerpt and Intro. · diff: Add MCP to excerpt and Intro
- 2026-10-19 approved — by ken-boyer — Ken approved after rewrite: Developer Documentation + App Dev SDK links retargeted to docs-hub portal (Getting Started, API Reference, Apps overviews); Domo Bricks link removed; MCP section added and MCP named in excerpt/Intro. Oct 2023 App Studio screenshot kept (approved without removing it). · commit 38f67fdb · diff: Portal links, Bricks removed, MCP section + excerpt/Intro

#### `fc-7724ee2ffe` [fact-check] Retrieve-Dataset-Source-Query-via-API.mdx — **skipped** (reassign-pending)
- 2026-10-19 skipped — by ken-boyer — Ken skipped for now. Open findings: streamId 25222 example is a WEBFORM dataset in the portal (contradicts FAQ 'webform has no streamId'); snowflakeunloadv2 attributed to Stream Get dataProvider.key but comes from Create transport.description.
- 2026-11-06 skipped — by ken-boyer — Ken: Retrieve-Dataset-Source-Query-via-API.mdx is not his — reassign to Tasleema Lallmamode. Handed off to the integration-branch owner (same regeneration drift that blocked the Data Models move).

#### `fc-8ec9682411` [fact-check] What-is-Domo-AI.mdx — **approved** (rewrite-redo)
- evidence: s/article/AI-Library.mdx (Toolkits: customer-created or Domo-provided); MCP-Toolkits-* articles
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: Required Grants should be Use AI Services, Use AI Chat, Manage Conversational Agents, Manage Toolkits (replacing Edit Cards / Manage All Company Settings). · diff: Rewrite Required Grants
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: pull the AI Pro credits note out of Required Grants and move the Domo AI Pro section to the top. · diff: Remove credits note from grants; move Domo AI Pro section to first content section (after Required Grants)
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: switch the AI Chat link to AI-Chat-v2 (consistent with AI-and-Data-Science-Overview). · diff: Retarget AI Chat link to /s/article/AI-Chat-v2; description from v2 excerpt
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: rewrite the AI Chat section intro for v2 capabilities. · diff: Rewrite AI Chat section paragraph for v2 (multi-part, multi-DataSet, Documents, visualizations, uploads/images, @mentions)
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: AI Library belongs under AI Agents (not AI Models and Projects); add a callout on Toolkits — Domo-provided and custom. · diff: Move AI Library link to AI Agents with corrected description; add Toolkits Note (Domo-provided vs custom)
- 2026-10-19 approved — by ken-boyer — Ken approved after rewrite: grants = Use AI Services, Use AI Chat, Manage Conversational Agents, Manage Toolkits; credits note removed from grants and Domo AI Pro moved to first section; AI Chat link -> AI-Chat-v2 and paragraph rewritten for v2; AI Library moved under AI Agents with corrected description; Toolkits note (Domo-provided vs custom) added. Approved as-is on: no Beta labels, FAQ provider list, Sept 2024 screenshot. · commit 5800c7b7 · diff: Grants, AI Pro moved, AI Chat v2, AI Library + Toolkits note

#### `pmi-2d81ad740d` [pm-input] 000005539.mdx — **rejected** (reject)
- reason: 000005539 (AI Chat v1) should be removed and replaced by AI-Chat-v2; the v1 FAQ addition and its question are moot.
- 2026-10-19 rejected — by ken-boyer — Ken: AI Chat v1 (000005539) should have been removed and replaced with AI-Chat-v2. Question not answered — article is to be retired (Phase 4.6), not improved.

#### `pmi-33f6f49122` [pm-input] 000005561.mdx — **answered** (provide-answer)
- 2026-10-19 answered — by ken-boyer — Ken: AI Readiness metadata does carry over to Domo Everywhere subscriber instances; AI Chat must be turned on separately in the subscriber instance. · diff: Rewrite Domo Everywhere FAQ with confirmed answers; burn pm-input marker

#### `pmi-d985dd4e2b` [pm-input] 000005561.mdx — **answered** (provide-answer)
- 2026-10-19 rewrite-redo — by ken-boyer — Ken (partial, 2 of 3): synonyms are committed as a pill with Enter or Tab; bulk AI Dictionary updates via Workflow are supported using Code Engine functions. Edit All change-loss question still open; marker narrowed to it. · diff: Apply Enter/Tab synonym + Code Engine Workflow answers; narrow pm-input to Edit All question
- 2026-10-19 rewrite-redo — by ken-boyer — Ken: the AI Dictionary can be edited from either the AI Readiness tab or the Schema tab of a DataSet. · diff: Access AI Readiness: note AI Dictionary is also editable from the Schema tab
- 2026-10-19 answered — by ken-boyer — Ken: Edit All change-loss is unknown (possibly a bug), not a documented limitation — remove the Edit All save-periodically advice. Earlier answers applied: Enter/Tab creates synonym pill; bulk AI Dictionary updates via Workflow + Code Engine functions; AI Dictionary editable from AI Readiness or Schema tab. · diff: Remove Edit All advice; burn pm-input marker

#### `pmi-78766422cd` [pm-input] 000005849.mdx — **rejected** (reject)
- reason: FileSets (000005849) was rebranded to Domo Documents; article to be retired in favor of Documents, so the App Studio FileSet-image question is moot.
- 2026-10-19 rejected — by ken-boyer — Ken: retire. FileSets was rebranded to Domo Documents; files are added to Document Collections.

#### `pmi-8d2291b0f9` [pm-input] 36004740075.mdx — **answered** (provide-answer)
- evidence: s/article/Understand-Jupyter-Workspace-Consumption.mdx
- 2026-10-23 rewrite-redo — by ken-boyer — Ken: rephrase the Enable Jupyter note — Jupyter is part of Domo's consumption-based pricing (not a 'premium feature'); link Understand-Jupyter-Workspace-Consumption. · diff: Rewrite Enable Jupyter note around consumption-based pricing + link consumption article
- 2026-10-23 answered — by ken-boyer — Ken: Jupyter is part of consumption-based pricing; if Jupyter Workspaces isn't in the Features menu, check your user grants or contact your Domo account team to request enablement. This covers the enablement-request process (no separate student/non-standard process documented). · diff: Replace last sentence of Enable Jupyter note; burn pm-input marker

#### `pmi-53d9e7edd5` [pm-input] 36004740075.mdx — **skipped**
- 2026-10-23 skipped — by ken-boyer — Ken: check with Kimberly Perez on current write_dataframe type handling (booleans -> empty ints, date/datetime) and whether astype(str) + ETL type fix is still the workaround or a fix has shipped. Skipped pending her answer.

#### `pmi-9699d36aac` [pm-input] 36004740075.mdx — **answered** (provide-answer)
- 2026-10-23 answered — by ken-boyer — Ken: kernels shipped — Python 3.9, 3.10, 3.11, 3.12 (Conda 24.11.3); R 4.1 (Conda 21.11.0). Pre-installed package list not specified; FAQ keeps pointer to installing libraries. · diff: Add kernel/version table to R version FAQ; retitle to cover Python; burn pm-input marker

#### `pmi-68861a25bf` [pm-input] AI-Chat-API-Session-ID.mdx — **deferred** (out-of-scope)
- reason: Out of scope this cycle. If written, it belongs on the Developer Portal (portal/), not the KB: how the Ask Chat / AI API requires a Domo-generated session ID — obtaining and using it, plus client-UUID canned-refusal behavior.
- 2026-10-23 deferred — by ken-boyer — Ken: defer; if we do this one it would belong under the Developer Portal.

#### `pmi-9f7b820515` [pm-input] Create-and-Use-Data-Models.mdx — **skipped** (reassign-pending)
- 2026-10-23 skipped — by ken-boyer — Ken: Create-and-Use-Data-Models.mdx is not his — it belongs to Phil Fuchs. Reassignment handed off to the integration-branch owner (regeneration drift blocked applying it). Item will go stale from Ken's list once the reassignment lands.

#### `pmi-2e73961d4f` [pm-input] Create-and-Use-Data-Models.mdx — **skipped** (reassign-pending)
- 2026-10-23 skipped — by ken-boyer — Ken: Create-and-Use-Data-Models.mdx is not his — it belongs to Phil Fuchs. Reassignment handed off to the integration-branch owner (regeneration drift blocked applying it). Item will go stale from Ken's list once the reassignment lands.

#### `pmi-243851692b` [pm-input] Create-and-Use-Data-Models.mdx — **skipped** (reassign-pending)
- 2026-10-23 skipped — by ken-boyer — Ken: Create-and-Use-Data-Models.mdx is not his — it belongs to Phil Fuchs. Reassignment handed off to the integration-branch owner (regeneration drift blocked applying it). Item will go stale from Ken's list once the reassignment lands.

#### `pmi-dfd19ab90d` [pm-input] Extract-Data-from-PDFs-with-Domo-AI.mdx — **rejected** (reject)
- reason: PM chose to remove the Prepare Your Source PDFs section rather than document extraction limits.
- 2026-10-19 rejected — by ken-boyer — Ken: remove the Prepare Your Source PDFs section (and its pm-input ask on scanned/multi-column extraction limits). · diff: Remove Prepare Your Source PDFs section + marker; drop FAQ sentence referencing it

#### `pmi-9fd7e4a27e` [pm-input] Extract-Data-from-PDFs-with-Domo-AI.mdx — **answered** (provide-answer)
- evidence: s/article/Documents.mdx (S3/SFTP file connectors); s/article/Magic-ETL-Tiles-Documents.mdx (Collection Input tile)
- 2026-10-19 rewrite-redo — by ken-boyer — Ken (partial answer, part 1 of 2): Image-to-Text is available in Magic ETL via the Text Generation tile. Part 2 (S3/SFTP batch-PDF pattern) still open; marker narrowed to that ask. · diff: Add Magic ETL Text Generation tile section; narrow pm-input marker to S3/SFTP question
- 2026-10-19 answered — by ken-boyer — Ken: Magic ETL is the best practice for bulk-processing PDFs (incl. from S3/SFTP). Documented as: S3/SFTP Document Collection connector -> Collection Input tile -> Text Generation tile (chain per Documents + Magic ETL Tiles: Documents articles). · diff: Add bulk-processing steps under Extract Text in Magic ETL; burn pm-input marker

#### `pmi-d8c6a8ad9b` [pm-input] Private-Embed-Token-Validation-Errors.mdx — **deferred** (out-of-scope)
- reason: Out of scope this cycle. Would cover: why a valid private embed token 302-redirects to login, client ID/secret + authorized-domains setup, and token regeneration after a domain change. KB vs Developer Portal placement not yet decided.
- 2026-10-23 deferred — by ken-boyer — Ken: defer.

#### `rt-b97dfa3616` [read-through] AI-and-Data-Science-Overview.mdx — **approved** (read-through)
- source: git-added
- 2026-10-23 rewrite-redo — by ken-boyer — Ken: before passing, remove the Domo Bricks mention from the Use AI Services grant description. · diff: Use AI Services description: drop Bricks (use canonical 'Access to features and Apps built using the AI Services Layer.')
- 2026-10-23 approved — by ken-boyer — Ken read the full article and signed off after removing the Bricks mention from Use AI Services. · commit df90c70b · diff: Bricks removed from grants; read-through passed

#### `rt-6b42e4ba50` [read-through] Develop-and-Integrate-Overview.mdx — **approved** (read-through)
- source: git-added
- 2026-10-23 rewrite-redo — by ken-boyer — Ken: before passing, fix the broken API Reference link and add MCP to the excerpt and Intro (matching Getting-Started-for-Developers). · diff: Fix /portal/API-Reference -> /portal/API-Reference/overview; add MCP to excerpt + Intro
- 2026-10-23 approved — by ken-boyer — Ken read the full article and signed off after fixing the API Reference link and adding MCP to the excerpt and Intro. · commit e9edcead · diff: Link fix + MCP in excerpt/Intro; read-through passed

#### `rt-2bd1545200` [read-through] Extract-Data-from-PDFs-with-Domo-AI.mdx — **approved** (read-through)
- source: git-added
- 2026-11-06 rewrite-redo — by ken-boyer — Ken: before passing, add Magic ETL to excerpt/Intro/availability, reframe first FAQ around Workflow vs Magic ETL bulk, add Text Generation tile to Related Articles, and drop 'structured data' (article only covers text extraction). · diff: Magic ETL in excerpt/Intro/availability; FAQ reframed; Related Articles + Text Generation tile; drop 'structured data'
- 2026-11-06 approved — by ken-boyer — Ken read the full article and signed off after Magic ETL was added to excerpt/Intro/availability, the first FAQ reframed (Workflow vs Magic ETL), Text Generation tile article added to Related Articles, and 'structured data' dropped. · commit e0b72a1a · diff: Magic ETL consistency fixes; read-through passed

#### `rt-03896a75bd` [read-through] Getting-Started-for-Developers.mdx — **approved** (read-through)
- source: git-added
- 2026-11-06 rewrite-redo — by ken-boyer — Ken: before passing, relabel the App Dev SDK link — it points to the portal Apps overview, not the full developer docs. · diff: Relabel link to 'App Dev SDK and app developer documentation'
- 2026-11-06 approved — by ken-boyer — Ken read the full article and signed off after relabeling the App Dev SDK link. · commit 55838257 · diff: Link relabel; read-through passed

#### `rt-ae8f4df8f6` [read-through] Retrieve-Dataset-Source-Query-via-API.mdx — **skipped** (reassign-pending)
- source: git-added
- 2026-11-06 skipped — by ken-boyer — Ken: Retrieve-Dataset-Source-Query-via-API.mdx is not his — reassign to Tasleema Lallmamode. Handed off to the integration-branch owner (same regeneration drift that blocked the Data Models move).

#### `rt-c75a531f0d` [read-through] What-is-Domo-AI.mdx — **approved** (read-through)
- source: git-added
- evidence: s/article/Documents.mdx (collections, connectors, Agent Knowledge, Workflows/AI Library/Magic ETL)
- 2026-11-06 rewrite-redo — by ken-boyer — Ken: add Documents to Required Grants; add a Magic ETL section calling out the Text Generation, Sentiment Analysis, and Classification tiles and Documents as inputs. · diff: Add Manage Documents grant; add AI in Magic ETL section (3 AI tiles + Collection Input); fold Magic ETL bullet out of AI-Assisted Tools
- 2026-11-06 rewrite-redo — by ken-boyer — Ken: keep 'automate summaries' in the excerpt and add classification; add an Unstructured Data section referencing Documents. · diff: Excerpt + classification; add Unstructured Data section (Documents)
- 2026-11-06 approved — by ken-boyer — Ken read the full article and signed off after adding Manage Documents to grants, an AI in Magic ETL section (Text Generation, Sentiment Analysis, Classification; Documents as input), an Unstructured Data section (Documents), and 'classification' to the excerpt. · commit a6a8201a · diff: Grant + 2 sections + excerpt; read-through passed

