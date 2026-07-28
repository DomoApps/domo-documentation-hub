# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A [Mintlify](https://mintlify.com)-based documentation hub for Domo. Content is written in MDX, navigation is defined in `docs.json`, and the site auto-deploys on push to `main`.

## Audience and Tooling Policy

This repo is edited by a mix of technical and non-technical contributors. Non-technical writers update KB articles directly in VS Code with no local setup — no Node, no yarn, no extensions, no remark.

All local tooling — `.remarkrc.mjs`, the `scripts/` directory, the `yarn` scripts, format-on-save, the lint rules in `scripts/remark-domo-style.mjs` — is **optional**. Treat it as a quality-of-life layer for technical contributors, not a requirement.

Consequences for what you write into the repo:

- Keep `README.md`, `Domo-KB-Style-Guide.mdx`, and any in-article guidance non-technical. No references to yarn, remark, lint rules, scripts, or VS Code extensions in these files. Use plain language a writer would understand.
- Tooling setup and developer-facing guidance belongs in a separate technical-contributor doc (to be added). Until that file exists, default to leaving tooling docs out of repo-level files entirely.
- When in doubt, ask whether a non-technical writer would need to read the change you're about to write. If not, it doesn't belong in a writer-facing file.

CLAUDE.md is AI-facing, so it's fine to discuss tooling here.

## Architecture

### Content Layout

- **`portal/`** — topic-organized content (Getting-Started, API-Reference, embed, Security, etc.) plus auto-generated OpenAPI endpoint pages (hash-named files) synced from the internal API repo
- **`s/article/`** — 1,822 flat KB article files, referenced by numeric ID (e.g. `000005874.mdx`) or slug
- **`s/topic/`** — topic grouping files
- **`de/`, `es/`, `fr/`, `ja/`** — localized content, each mirrors the `s/` structure
- **`images/kb/`** — screenshots and diagrams (\~7,100 files)
- **`snippets/`** — reusable MDX components imported into articles: `DomoEmbed.mdx` (embeds Domo-hosted iframes with auto-resize), `BetaNote.mdx` (standardized beta-feature callout), `ColorTable.jsx`, `TypographyTable.jsx`

### Navigation

All navigation is defined in **`docs.json`** (large file, \~307KB). The schema is `https://mintlify.com/docs.json`. Navigation is organized into tabs → groups → pages. The OpenAPI sync workflow auto-updates this file when YAML specs change.

## MDX Content Conventions

All articles use YAML frontmatter with at minimum a `title` field.

Key Mintlify components in use:

- `<Frame>` — wraps screenshots (auto-sizes to content width)
- `<Note>`, `<Warning>`, `<Tip>` — callout blocks (always bold the label: `**Note:**`)
- `<AccordionGroup>` + `<Accordion title="...">` — FAQ sections
- Inline UI icons use the Domo icon font: `<i className="icon-{name}" aria-hidden="true" />`. Avoid Mintlify's `<Icon>` component for local SVGs — color/dark-mode breaks. When a glyph isn't in either icon font, fall back to a native `<img>` with inline `style={{display: 'inline', verticalAlign: 'start', height: '1.2em', margin: '0'}}` (use `'2em'` if the icon stands alone as a row label in a table cell). See `Domo-KB-Style-Guide.mdx` › **Icons**.
- Third-party brand logos (AWS, OpenAI, Anthropic, GitHub, …) are not in the Domo icon font. Prefer a coded icon over an `<img>` — a monochrome logo image disappears in dark mode. First choice: Font Awesome's brands set via `<Icon icon="{slug}" iconType="brands" aria-hidden="true" />` (this is the one case where `<Icon>` is correct — it's a font glyph, not a local SVG). When the free FA set lacks it (e.g. Anthropic), inline raw `<svg fill="currentColor" …>` with a path from a source like Simple Icons. See `Domo-KB-Style-Guide.mdx` › **Brand and Third-Party Logos**.

Internal links use root-relative paths: `[text](/s/article/Article-Title)`

### Snippets

Reusable components live in `snippets/`. Import them at the top of an MDX file:

```mdx
import { DomoEmbed } from "/snippets/DomoEmbed.mdx";
import { BetaNote } from "/snippets/BetaNote.mdx";
```

- **`<DomoEmbed src="..." />`** — embeds a Domo-hosted card or page in an iframe with automatic height-resize. Props: `src` (required — embed URL), `width` (CSS width, default `"100%"`), `initialHeight` (px, default `"600"`).
- **`<BetaNote />`** — renders the standardized beta-program callout (links to the enable-features and sign-up pages). Pass `generic={true}` to omit "This feature is in beta." and emit only the program links. Use this instead of writing the beta Note by hand — it stays up-to-date with the program URLs automatically.

## Domo Release Cadence

Domo releases monthly. Branches are named by the date the branch is cut. From branch cut:

- Code ships \~5 weeks later
- Feature release (feature switches enabled, customers see new features) is \~1 week after code ships

Internally, releases are always identified by the **branch cut date** (the branch name). Customers and client-facing teams only care about when features appear in their environments, so they talk in terms of the feature release date — PMs translate between the two. For tracking feature availability and mapping KB articles to releases, always use the **branch cut date** as the canonical identifier.

## Finding Existing Articles

To find an article by title keyword, search frontmatter across all KB articles:

```bash
grep -r "title:.*keyword" s/article/ s/topic/
```

To find by filename or slug, use a glob against `s/article/*.mdx` or `s/topic/*.mdx`.

Both `s/article/` and `s/topic/` should be searched — topics are grouping pages and articles are the detailed content.

## Article PM Ownership

Every article in `s/article/` is mapped to a **Feature** (using the same nomenclature as the internal squad-ownership CSV) and its **Product Manager** in `Article-PM-Ownership-Reference.mdx` at the repo root.

- **Reference file:** `Article-PM-Ownership-Reference.mdx` — searchable table of Feature, Article Title, Article File Name, PM.
- **Source CSV:** `Feature - Owning Squad, PM, Eng, UX.csv` — authoritative squad/PM roster; the Feature column is the canonical identifier used in the reference.
- **Generation script:** `scripts/build-pm-ownership.py` — regenerates the reference by cross-referencing the CSV against `docs.json` navigation hierarchy and article frontmatter. Re-run whenever articles are added in bulk or the CSV changes.

To look up who owns a specific article:
```bash
grep "filename.mdx" Article-PM-Ownership-Reference.mdx
```

To look up all articles owned by a PM:
```bash
grep "PM Name" Article-PM-Ownership-Reference.mdx
```

To look up all articles for a Feature:
```bash
grep "^| Feature Name" Article-PM-Ownership-Reference.mdx
```

## Scripts

All scripts live in `scripts/`. They are optional dev-quality tools — non-technical writers never need to run them.

| Script | Purpose |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `pad_md_tables.py` | Pad all Markdown pipe-table columns in a file so pipes align. Run after editing any article that has Markdown tables: `python3 scripts/pad_md_tables.py s/article/Filename.mdx` |
| `build-pm-ownership.py` | Regenerate `Article-PM-Ownership-Reference.mdx` from the squad CSV + `docs.json`. See the `update-pm-ownership` skill. |
| `docs_cli.py` | Export the full nav structure (all tabs/groups/pages) to CSV. `python3 scripts/docs_cli.py export` → `scripts/reports/doc_structure.csv`. Supports `--language` (en/jp/fr/de/es) and `--output`. |
| `html_to_mdx.py` | Bulk Salesforce-to-MDX conversion pipeline (used with the `csv-to-mdx` skill). Reads an exported Salesforce CSV, converts HTML bodies to MDX, and writes files to `s/article/`. |
| `html-to-mdx.mjs` | Node.js single-file HTML-to-MDX converter (used by the `migrate-html` skill for one-off article migrations via pandoc). |
| `add_excerpts.py` | Batch-add `excerpt:` frontmatter to articles that only have `title:`. |
| `fix-heading-levels.py` | Normalize heading levels across migrated articles. |
| `fix_anchors.py` | Fix broken anchor IDs introduced by the HTML migration. |
| `diff_kb_articles.py` | Diff two versions of a KB article (e.g., Salesforce export vs. repo copy). |
| `build_video_library.py` | Build a video library index from article frontmatter. |
| `update_kb_articles.py` | Entry point for the bulk Salesforce CSV import pipeline. |
| `remark-domo-style.mjs` | Remark lint plugin enforcing Domo style rules (optional; runs via `yarn lint`). |

## DomoStats Schema Sync

`s/article/360043433813.mdx` (DomoStats Connector) is kept in step with the connector source
automatically. Do not hand-diff Java against MDX.

- **Source of truth:** `domo-development/domostats` emits `domostats-schema.json` from a Gradle
  task (`./gradlew generateSchemaManifest`, implemented in
  `src/tooling/java/com/domo/connector/domostats/tooling/SchemaManifestGenerator.java`) and
  commits it. It lists every report, its gating, and its columns with types and descriptions.
- **This side:** `.github/workflows/sync-domostats-schema.yml` clones that repo, runs
  `.github/scripts/reconcile_domostats.py`, and opens a draft PR. Read
  `.github/scripts/README.md` before touching either.
- **The two sides are deliberately not byte-identical.** Java descriptions are plain text; the
  article keeps Markdown presentation. Comparison is on a normalized form (backticks stripped,
  whitespace collapsed, trailing periods dropped, case-insensitive). When editing these tables
  by hand, keep house style (backticks on enum values, terminal periods, `DataSet` not
  "dataset"). Never "fix" a table to match Java verbatim, and keep field order in schema order.
- **An empty source description never overwrites the article.** Most columns still have no
  description in Java.
- Callouts in that article were hand-audited; the sync never adds, removes, or rewords one.
- **This repo is public and the connector repo is not.** Two consequences, both load-bearing:
  the manifest records gating as a *kind* (`customer-allowlist`, `environment-allowlist`,
  `runtime-check`) and never the customer or environment names behind it; and a report the
  connector has but this article does not is **opt-in**, because a connector report can exist
  weeks before its feature ships. Until a human adds its key to `documentedReportKeys` in
  `.github/domostats-sync-config.json`, the report's name is withheld from the PR body. Do not
  pass `--no-redact` in CI and do not upload the report JSON as an artifact.

## Style Standards

See `Domo-KB-Style-Guide.mdx` for full standards. Key points:

- Article structure: Intro → Required Grants → Access Feature → Tasks (CRUD order) → FAQ
- FAQ sections go at the bottom, coded as `<AccordionGroup>`
- For technical style questions not in the guide, follow the [Google developer documentation style guide](https://developers.google.com/style)
- For nontechnical style, follow The Chicago Manual of Style (18th ed.)

Use `New-Article-Template.mdx` as the starting point for new KB articles.

## Local Setup

After cloning, run this once to enable the repo's git hooks:

```bash
git config core.hooksPath .githooks
```

This activates a `post-merge` hook that warns you when a `git pull` leaves tracked files missing from your working tree — a known failure mode on case-insensitive filesystems (macOS APFS, Windows NTFS) after commits that rename case-colliding files. The hook prints the one-liner needed to restore them; it does not mutate your working tree.

## Skills

||SKILL||ALWAYS USE FOR||
|kb-intake|Interviewing the user to gather information that is important to writing a good KB document|
|new-kb-article|Drafting a new KB article following Domo's style guide and template. This skill calls the kb-intake skill|
|new-overview-article|Drafting a product or feature Overview article (the "What is X" landing page that explains a feature conceptually and clusters links to deeper how-tos). Distinct from `new-kb-article` — handles title-collision checks against legacy "X Overview" articles, link-cluster structure, and nav placement|
|add-to-nav|Adding a page to docs.json navigation or moving an existing page to a different location in docs.json|
|update-kb-article|Any update to an existing KB article: renames, content edits, image swaps, content removal, file path updates, cross-file changes, step/process edits, navigation moves, merges, or splits|
|mintlify-design|Mintlify component/page-design expert: choosing components, composing custom layouts, building rich pages, "is there a component for X" questions, or authoring reusable snippets in `/snippets/`|
|fix-ja-formatting|Fix MDX syntax and structural formatting issues in Japanese articles WITHOUT touching translation: bold-label rendering (space after `**` when preceded by fullwidth punctuation or em-dash), HTML-escaped component tags, callouts containing list items, broken links, broken bold spans, English translation artifacts, and inline icon replacement. Run after any JA article edit to catch MDX mis-formatting before merge.|
|update-pm-ownership|Regenerate `Article-PM-Ownership-Reference.mdx` after the squad CSV or article list changes|
|csv-to-mdx|Review and audit an MDX article produced by the Salesforce-to-Domo programmatic conversion pipeline (`scripts/html_to_mdx.py`)|
|migrate-html|Migrate a single HTML article to a repo-ready MDX file: convert with pandoc, apply Domo style rules, save to `s/article/`, and register in `docs.json`|
|release-feature-links|Match every feature in a PMM release copy to a KB article and produce link sentences for the shared PMM Word doc or `Current-Release-Notes.mdx`|
|release-notes|Generate user-friendly internal release notes by diffing the latest git tag against the previous tag|
|mintlify-preview-workflow|Working on `.github/workflows/mint-preview.yml` — the Mintlify preview deployment GitHub Action|
|openapi-sync-workflow|Working on the OpenAPI sync GitHub Action (`sync-api-docs.yml`) — YAML detection, sync scripts, or `docs.json` nav-generation integration|
|connector-review|Manage the connector PR/Jira review lifecycle: run the dashboard, post follow-ups on stale tickets, merge approved PRs, post release-date comments, close Jira tickets, and handle publish/migration requests from Arun|
