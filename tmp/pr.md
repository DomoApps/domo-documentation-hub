## Summary

Large multi-theme branch that lands the new Domo icon library alongside a sweeping cleanup of legacy Salesforce-export artifacts, several new/updated connector articles, and the repo's first Node tooling for MDX linting and format-on-save.

81 commits, \~2,600 files touched (most are content edits, not net-new files). Roughly 14K English + \~1,100 JA articles affected.

## What's changing

### 1. New icon library (`new-icon-library` core work)

- **Phosphor icon font** is now the default for inline UI icons. \~620 inline-icon `<img>` tags across English and localized KB articles migrated to `<i className="icon-{name}" aria-hidden="true" />`. Theme-adaptive (icons inherit text color), so light/dark mode works without color-prop juggling.
- **Legacy icon font** (`<i className="legacy-icon-{name}" />`) added in parallel for documentation depicting the pre-refresh Domo UI — release notes, Workbench, etc. Both fonts ship the same glyphs; pick the one matching the UI being shown, never based on availability.
- **`sm` size class** applied to icon usages in translated (de/es/fr/ja) articles to match the size set on the English versions.
- **Custom SVG fallback** for glyphs missing from both fonts: hand-authored SVG under `images/kb/`, referenced via `<InlineImage>`, with `fill="currentColor"` and a content-tight `viewBox` so it inherits text color and sizes naturally inline. First instance: [`legacy-icon-workbench-preview-window.svg`](../images/kb/legacy-icon-workbench-preview-window.svg) (Workbench Preview Window icon — no phosphor or legacy-icon font equivalent). 12 inline `<img>` references migrated across [s/article/4407032210199.mdx](../s/article/4407032210199.mdx), [ja/s/article/4407032210199.mdx](../ja/s/article/4407032210199.mdx), and [ja/s/article/360042932654.mdx](../ja/s/article/360042932654.mdx); each picks up an `InlineImage` import. Sizing convention: `height="1.2em"` inline in prose, `height="2em"` when the icon stands alone as a row label in a table cell.
- **External-link arrows** in release notes were upgraded (docs chrome, not UI). Otherwise release notes deliberately keep the OLD `<img>` icons since they're snapshots of the product at a moment in time.
- **Alerts overview** ([s/article/360043430373.mdx](../s/article/360043430373.mdx)) fully rewritten for the new left-nav structure (Features > Alerting): "Alerts Center" no longer exists; subpages are now top-level features (Discover → Alerts Explorer, Settings → Alert settings).
- **Style guide updates** ([Domo-KB-Style-Guide.mdx](../Domo-KB-Style-Guide.mdx)) documenting the icon font conventions.

### 2. Salesforce-export cleanup sweep

- **Anchor migration**: `#snake_case` → `#kebab-case` across the entire KB. App Studio Overview ([s/article/000005295.mdx](../s/article/000005295.mdx)) had 27+ updates; full sweep also covered TOC blocks, `(#top)` back-to-top links (including DE/ES/JA), and \~5 malformed edge cases.
- **Heading hierarchy normalization** across all KB articles.
- **Title cleanup**: removed leading `> ` prefix from article titles.
- **URL fixes**: removed `/minasan/` path segment from `domo-support` URLs.
- **Typography**: malformed bold fixes, beta-tag drop from permalinks.
- **Inline image refactor**: `<InlineImage>` snippet → native `<img>` tags repo-wide (refactor commit b08ec66c).

### 3. New / updated content (subsumed sub-PRs)

| Sub-PR | Article                                                                                       |
| ------ | --------------------------------------------------------------------------------------------- |
| #134   | Microsoft SharePoint Online Single-Tenant Writeback Connector                                 |
| #148   | Domo on Lakebase / Domo-on-BigQuery prep                                                      |
| #149   | Mintlify "Client not built" troubleshooting workaround                                        |
| #150   | Access token generation requirements + role clarifications                                    |
| #151   | Beta conventions doc (canonical source for beta articles)                                     |
| #152   | Domo BigQuery GA (FAQ, new UI, WIF auth, prereqs, query metadata)                             |
| #153   | DomoApps publish docs update                                                                  |
| #154   | MCP grants article: beta note under title                                                     |
| #155   | v2.2.0 release notes                                                                          |
| #156   | PostgreSQL SSH Writeback Connector (new)                                                      |
| #157   | Azure Data Lake Storage Gen2 with AAD Writeback                                               |
| #158   | Tenant ID typo fix                                                                            |
| #159   | Internal anchor updates                                                                       |
| —      | Microsoft OneDrive Business Connector: HTML→Markdown tables + typo fix                        |
| —      | HubSpot Connector typo (`** Accounts**` → `**Accounts**`)                                     |
| —      | DomoStats: beta tag on last report ([s/article/360042934614.mdx](../s/article/360042934614.mdx)) |
| —      | `/portal` redirect added to `docs.json` (community link target)                               |

### 4. Repo tooling

- **Yarn 4 (node-modules linker) + remark** for MDX linting and format-on-save. Pipeline runs `scripts/split-table-rows.mjs | remark` via `jkillian.custom-local-formatters` — breaks legacy single-line `<table>` blocks (Salesforce exports) onto one `<tr>` per line, then remark indents. Buffer stays in sync via stdin/stdout.
  - `yarn check` lints all `.mdx`
  - `yarn format` bulk-formats every `.mdx` in place
- **Mintlify CLI (`mint`)** pinned as a devDependency — no more global `mintlify` install required. New scripts:
  - `yarn dev` — local preview server (replaces `mintlify dev`)
  - `yarn broken-links` — scan internal links
  - `yarn validate` — strict build check (fails on any warning)
  - README updated end-to-end to drop the global-install instructions and reference the new scripts.
- **Remark config**: italic emphasis marker set to `_` in [.remarkrc.mjs](../.remarkrc.mjs) so format-on-save no longer fights Mintlify's `_italic_` convention.
- Helper scripts: `scripts/fix-heading-levels.py`, `scripts/fix_anchors.py`, `scripts/split-table-rows.mjs`, `scripts/duplicates_report.json`.

## Test plan (run once the Mintlify preview is live)

### Icons (highest-risk area)

- [ ] Open 3–5 random English KB articles in both light and dark mode. Inline UI icons inherit text color and render crisply at body-text size.
- [ ] Open the **Alerts** overview ([s/article/360043430373.mdx](../s/article/360043430373.mdx)). Verify the rewritten content matches the new left-nav structure (no "Alerts Center"; Alerts Explorer and Alert settings are top-level).
- [ ] Workbench articles ([s/article/4407032210199.mdx](../s/article/4407032210199.mdx) — "Understanding the Workbench 5.1 UI", plus the two JA Workbench articles): the **Preview Window** icon renders via `InlineImage` pointing at [`legacy-icon-workbench-preview-window.svg`](../images/kb/legacy-icon-workbench-preview-window.svg). Verify (a) the `InlineImage` import is present at the top of each, (b) the SVG inherits text color in both light and dark mode (uses `fill="currentColor"`), and (c) the icon looks correctly sized — `~1.2em` inline in prose, `~2em` as a row label in the icon-bar table cell — with no excess whitespace beside it.
- [ ] System Roles grants table at [s/article/360043438953.mdx](../s/article/360043438953.mdx): green check (Yes) and red X (No) cells render with `text-green-600` / `text-red-600` and the right `aria-label`s.
- [ ] External-link arrow appears with the `sm` class inside link text — e.g. anywhere `Domo University <i className="icon-arrow-square-out sm" ... />` shows up.
- [ ] Sample one article from each locale (de/es/fr/ja). Icons inherit text color and use the `sm` size class.
- [ ] Release notes (e.g. [s/article/000005784.mdx](../s/article/000005784.mdx), [s/article/360042934794.mdx](../s/article/360042934794.mdx)): OLD `<img>` icons preserved EXCEPT for any external-link arrow next to hyperlinks (those should be the new font glyph + `sm`).

### Anchors, headings, URLs

- [ ] App Studio Overview ([s/article/000005295.mdx](../s/article/000005295.mdx)): every internal anchor link (e.g. "main navigation", "Apps Home", "page drill", "configuration tab") jumps to the right section.
- [ ] Sample 5 articles: heading hierarchy starts at H1/H2 sensibly, no orphan H3 under H1.
- [ ] No `(#top)` or back-to-top links visible anywhere in the rendered preview.
- [ ] Sample any article that had a `domo-support` link — URL no longer contains `/minasan/`.
- [ ] No article title in the sidebar renders with a leading `> `.

### New / updated content

- [ ] [PostgreSQL SSH Writeback Connector](../s/article/PostgreSQL-SSH-Writeback-Connector.mdx) renders; reachable from Connectors nav.
- [ ] [Microsoft SharePoint Online Single-Tenant Writeback Connector](../s/article/Microsoft-SharePoint-Online-Single-Tenant-Writeback-Connector.mdx) renders.
- [ ] [Azure Data Lake Storage Gen2 with AAD Writeback](../s/article/) article reflects the updates (look for the most recent merge from #157).
- [ ] \[Microsoft OneDrive Business Connector] tables render as proper Markdown tables (not nested HTML), and the typo fix landed.
- [ ] Domo BigQuery GA article: no Beta tag/badge, FAQ section visible, new UI instructions present, WIF authentication described, prerequisites/permissions updated, BQ query metadata section visible.
- [ ] [Connect AI Tools to Domo Using MCP](../s/article/Connect-AI-Tools-to-Domo-Using-MCP.mdx) — beta note appears under the title (not buried mid-article); grants list correct.
- [ ] [Current Release Notes](../s/article/Current-Release-Notes.mdx) — v2.2.0 entries render with proper line breaks.
- [ ] DomoStats article ([s/article/360042934614.mdx](../s/article/360042934614.mdx)): beta tag visible on the last DomoStats report entry.
- [ ] Mintlify "Client not built" troubleshooting section visible in the contributor README/Getting Started area.
- [ ] Access token generation page: roles required clearly listed, no "Create access token" grant shown (intentionally hidden for now).
- [ ] DomoApps publish docs updates render.
- [ ] Navigate to `/portal` — expect redirect to the developer portal landing (defined in `docs.json`).

### Translations

- [ ] DE / ES / FR / JA — pick one updated article from each locale, confirm icons render and `sm` class applied; anchors/headings clean.
- [ ] No JA article shows broken nav anchors.

### Tooling (local, not via Mintlify preview)

- [ ] `yarn install && yarn check` succeeds on a clean clone.
- [ ] `yarn format` is idempotent on already-clean files.
- [ ] In VS Code with `jkillian.custom-local-formatters` and `unifiedjs.vscode-mdx` installed (WSL side if applicable), save a legacy `<table>`-heavy article — table rows split onto separate lines and the buffer updates in place.
- [ ] `yarn dev` starts without parse errors against `.vscode/settings.json` (no YAML/JSON parse errors).
- [ ] `yarn broken-links` reports no new internal-link breakage introduced by this branch.
- [ ] `yarn validate` passes (strict build check — useful sanity gate before merge).

## Notes

- Working docs now live under `tmp/` and are committed alongside this PR so other contributors can browse the audit data without pulling files into the repo root:
  - [`chart-mapping.mdx`](chart-mapping.mdx) — chart-thumbnail → sprite-class mapping
  - [`deletion-candidates.md`](deletion-candidates.md) — unreferenced images safe to delete (1,923 files, \~173 MB)
  - [`icon-image-audit.mdx`](icon-image-audit.mdx) — original inline-icon `<img>` audit (3,672 refs across 722 articles)
  - [`inline-icon-mapping.md`](inline-icon-mapping.md) + [`inline-icon-mapping.json`](inline-icon-mapping.json) — image-hash → icon-font-class mapping driving the migration script (1,076 distinct icon images, 2,250 refs)
  - [`pr.md`](pr.md) — this PR description
  - `tmp/` was removed from `.gitignore` to track these. Future scratch work placed in `tmp/` will also be tracked — re-add `tmp/` to `.gitignore` or use a different scratch dir if that's not desired.
- The `App Studio Internal Links to Update.csv` working file (already-applied anchor list) was deleted in commit `06441618`.
- This branch carries several merged sub-PRs (#134, #148-#159). Squashing or rebase-merging here would consolidate those into a single landed change on `main`; pick whichever merge strategy your team prefers.
