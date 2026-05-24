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

- **`portal/`** — topic-organized content (Getting-Started, API-Reference, Knowledge-Base, etc.)
- **`s/article/`** — 1,700+ flat KB article files, referenced by numeric ID (e.g. `000005874.mdx`) or slug
- **`s/topic/`** — topic grouping files
- **`de/`, `es/`, `fr/`, `ja/`** — localized content, each mirrors the `s/` structure
- **`images/kb/`** — screenshots and diagrams (\~7,100 files)

### Navigation

All navigation is defined in **`docs.json`** (large file, \~307KB). The schema is `https://mintlify.com/docs.json`. Navigation is organized into tabs → groups → pages. The OpenAPI sync workflow auto-updates this file when YAML specs change.

## MDX Content Conventions

All articles use YAML frontmatter with at minimum a `title` field.

Key Mintlify components in use:

- `<Frame>` — wraps screenshots (auto-sizes to content width)
- `<Note>`, `<Warning>`, `<Tip>` — callout blocks (always bold the label: `**Note:**`)
- `<AccordionGroup>` + `<Accordion title="...">` — FAQ sections
- Inline UI icons use the Domo icon font: `<i className="icon-{name}" aria-hidden="true" />`. Avoid Mintlify's `<Icon>` component for local SVGs — color/dark-mode breaks. When a glyph isn't in either icon font, fall back to a native `<img>` with inline `style={{display: 'inline', verticalAlign: 'start', height: '1.2em', margin: '0'}}` (use `'2em'` if the icon stands alone as a row label in a table cell). See `Domo-KB-Style-Guide.mdx` › **Icons**.

Internal links use root-relative paths: `[text](/s/article/Article-Title)`

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

## Style Standards

See `Domo-KB-Style-Guide.mdx` for full standards. Key points:

- Article structure: Intro → Required Grants → Access Feature → Tasks (CRUD order) → FAQ
- FAQ sections go at the bottom, coded as `<AccordionGroup>`
- For technical style questions not in the guide, follow the [Google developer documentation style guide](https://developers.google.com/style)
- For nontechnical style, follow The Chicago Manual of Style (18th ed.)

Use `New-Article-Template.mdx` as the starting point for new KB articles.

## Skills

||SKILL||ALWAYS USE FOR||
|kb-intake|Interviewing the user to gather information that is important to writing a good KB document|
|new-kb-article|Drafting a new KB article following Domo's style guide and template. This skill calls the kb-intake skill|
|add-to-nav|Adding a page to docs.json navigation or moving an existing page to a different location in docs.json|
|update-kb-article|Any update to an existing KB article: renames, content edits, image swaps, content removal, file path updates, cross-file changes, step/process edits, navigation moves, merges, or splits|
|mintlify-design|Mintlify component/page-design expert: choosing components, composing custom layouts, building rich pages, "is there a component for X" questions, or authoring reusable snippets in `/snippets/`|
|fix-ja-formatting|Fixing structural formatting issues in queued Japanese articles: inline image placement, block vs. inline `<img>` mismatches, callout wrapping, and redundant blank lines|
