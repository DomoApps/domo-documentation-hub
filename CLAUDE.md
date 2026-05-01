# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A [Mintlify](https://mintlify.com)-based documentation hub for Domo. Content is written in MDX, navigation is defined in `docs.json`, and the site auto-deploys on push to `main`.

## Architecture

### Content Layout

- **`portal/`** — topic-organized content (Getting-Started, API-Reference, Knowledge-Base, etc.)
- **`s/article/`** — 1,700+ flat KB article files, referenced by numeric ID (e.g. `000005874.mdx`) or slug
- **`s/topic/`** — topic grouping files
- **`de/`, `es/`, `fr/`, `ja/`** — localized content, each mirrors the `s/` structure
- **`images/kb/`** — screenshots and diagrams (~7,100 files)

### Navigation

All navigation is defined in **`docs.json`** (large file, ~307KB). The schema is `https://mintlify.com/docs.json`. Navigation is organized into tabs → groups → pages. The OpenAPI sync workflow auto-updates this file when YAML specs change.

## MDX Content Conventions

All articles use YAML frontmatter with at minimum a `title` field.

Key Mintlify components in use:
- `<Frame>` — wraps screenshots (auto-sizes to content width)
- `<Note>`, `<Warning>`, `<Tip>` — callout blocks (always bold the label: `**Note:**`)
- `<AccordionGroup>` + `<Accordion title="...">` — FAQ sections
- Inline images use raw `<img>` with inline `style={{}}` props

Internal links use root-relative paths: `[text](/s/article/Article-Title)`

## Domo Release Cadence

Domo releases monthly. Branches are named by the date the branch is cut. From branch cut:
- Code ships ~5 weeks later
- Feature release (feature switches enabled, customers see new features) is ~1 week after code ships

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
|fix-ja-formatting|Fixing structural formatting issues in queued Japanese articles: inline image placement, Frame vs. InlineImage mismatches, callout wrapping, and redundant blank lines|
