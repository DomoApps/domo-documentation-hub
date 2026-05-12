---
name: release-feature-links
description: For a monthly release, match every feature in the PMM source copy to a KB article in s/article/ and produce link sentences. Two modes — (1) PMM Release Article: emit copy-paste-ready feature + link sentences (with https://www.domo.com/docs prefix) for the shared Word doc; (2) Current Release Notes: edit s/article/Current-Release-Notes.mdx in place, inserting link sentences inline. Use when the user asks to "add KB links to the release article", "wire up links for the May release", "match KB articles to release features", or similar.
---

# Release Feature → KB Article Linker

Each Domo monthly release ships a marketing/PMM article that introduces every new feature, plus an in-repo `Current-Release-Notes.mdx`. Both documents need links from each feature blurb back to the relevant KB article in `s/article/`. This skill automates the matching and either emits link sentences for copy-paste (PMM mode) or edits the in-repo release notes directly (Current Release Notes mode).

## Workflow

### 1. Ask the user two clarifying questions

Use **AskUserQuestion** with two questions in a single call:

1. **Target document** — which output mode?
   - `PMM Release Article` (external Word doc — output is copy-paste-ready text)
   - `Current Release Notes` (in-repo `s/article/Current-Release-Notes.mdx` — edit the file directly)
2. **Source copy file** — which `.txt` file in the repo contains the PMM draft copy for this release? (Free-form short text or selection of `.txt` files at the repo root.)

If helpful, list candidate `.txt` files first:

```bash
ls *.txt 2>/dev/null
```

so the user can pick by name.

### 2. Extract the feature list from the PMM source copy

Read the chosen `.txt` file. Features are typically introduced in two ways:

- An ordered list near the top under headings like *"Order of Release for New Features Page"* or *"New Features / Feature Enhancements"* / *"Beta Features"*.
- Each feature then appears again as its own section header further down with its target persona, meta description, tags, and web copy.

Extract a deduplicated list of feature names, preserving the release ordering. Be alert for:

- Slight name variations between the table-of-contents list and the section headers (e.g. *"AI Classification tile"* vs *"AI Classification Tile"* vs *"Magic ETL AI Classification Tile"*) — normalize to the section-header form.
- Sub-features nested under a parent (e.g. *Workflow Event Triggering – Access Request* and *Queue Notification Controls* under *Workflows Updates*; *AI Classification Tile*, *Sentiment Analysis Tile*, *Multi-Statement SQL Tile* under *Magic ETL Enhancements*). Treat each sub-feature as its own item — they each need their own link.

### 3. For each feature, find the best-matching KB article

Search `s/article/` by frontmatter `title:`. Run these in parallel where possible:

```bash
# Primary search — feature name keywords
grep -rli -E "title:.*<keyword>" s/article/

# Slug-based filenames (newer articles)
ls s/article/ | grep -iE "<keyword>"
```

Then verify each hit by reading the frontmatter and a snippet of the body to confirm the article is actually about the feature (not a coincidental keyword match — e.g. *"Jupyter Workspaces"* is **not** the same as the *"Workspaces (Mobile & Web)"* feature).

Tips for tricky cases:

- **Rebranded features** — search the old name too. Example: *Domo Documents* was formerly *FileSets*.
- **Feature umbrella articles** — multiple new tiles can share one article (e.g. *"Magic ETL Tiles: AI Services"* covers Text Generation, Classification, and Sentiment). Use the same article for all sub-features and flag in your output that the sub-section may not yet be live.
- **Newly added articles** — recently-added KB content for this release will likely show up here:

  ```bash
  git log main..HEAD --name-status --pretty=format: -- s/article/ | grep -E "^A\s"
  ```

  Check those first before broader searches.
- **No match found** — do **not** invent a link. Mark the feature with a brief note explaining what was searched and recommend the user confirm with the writer assigned to the feature.

### 4. Build link sentences

For every feature with a confirmed KB article, write **one short link sentence** that:

- Includes the feature name naturally and conversationally (it should drop cleanly into the bottom of the feature's Web copy block — don't echo the marketing pitch, don't restate the meta description, don't add bold/emphasis).
- Wraps the feature-name phrase (or a natural variation of it) as the link text.
- Uses the article slug or numeric ID from the matched file's path.

**URL format for PMM mode (external):**

```
https://www.domo.com/docs/s/article/<slug-or-id>
```

The article's slug-or-id is the filename of the matched `s/article/*.mdx` without the `.mdx` extension. Examples: `Connect-AI-Tools-to-Domo-Using-MCP`, `000005172`, `Documents`.

**URL format for Current Release Notes mode (internal):**

Use root-relative paths only:

```
/s/article/<slug-or-id>
```

(This matches the existing internal-link convention in the repo per `CLAUDE.md`.)

**Sentence style** — keep it short and conversational. Prefer "Learn more about..." or "Learn more about how to..." patterns, but vary if the feature name doesn't slot naturally. The example template the user gave is:

> Learn more about [Domo Essentials MCP](https://www.domo.com/docs/s/article/Connect-AI-Tools-to-Domo-Using-MCP).

### 5. Deliver based on mode

#### Mode A — PMM Release Article (copy-paste output)

For each feature, output two pieces:

1. The feature name (so the user knows which section in the Word doc to paste into).
2. The link sentence (ready to paste into the bottom of that feature's Web copy block).

Format as a flat list, one feature per block:

```markdown
**<Feature Name>**
> <link sentence with full https://www.domo.com/docs URL>
```

For features without a matched article, emit the feature name and an italicized note explaining what was checked and what the user should do (don't fabricate a link).

Do **not** edit `may-*-pmm-copy.txt` (or whatever the chosen `.txt` is) — it's a reference snapshot, not the canonical doc.

#### Mode B — Current Release Notes (in-repo edits)

1. Read `s/article/Current-Release-Notes.mdx`.
2. For each feature with a matched article, locate the corresponding section in the file by section header (e.g. `### Domo Essentials MCP`). Section headers in the release notes are usually shorter/cleaner than PMM headers — match on the core feature name, not exact string.
3. Draft an inline link sentence using the **internal** `/s/article/<slug>` format. Place it at the end of the section's body text (after the `<Frame>` screenshot block if one exists, but before the next `###` header). Use the same conversational "Learn more about..." style.
4. **Before saving any edits**, show the user every proposed change as a small preview — feature name, the target section, the exact sentence you'll insert. Wait for confirmation.
5. After approval, use the **Edit** tool to insert each sentence. Make one edit per feature; do not bundle multiple feature edits into a single replace block (keeps diffs reviewable).
6. For features without a matched article, list them at the end with a short note — do not edit those sections.

### 6. Final summary

After delivery, give the user a one-paragraph summary: total features in source copy, count linked, count flagged for follow-up, and (Mode B only) confirmation that the file was saved.

## Important reminders

- **Never edit the source `.txt` file.** It's a reference snapshot of the marketing doc, not the canonical version.
- **Verify before linking.** A keyword grep can produce false positives (e.g. *"Jupyter Workspaces"* vs *"Workspaces"*). Always confirm with title + a brief body read.
- **Don't invent URLs.** If no matching KB article exists, say so — recommend the user check with the writer assigned to that feature.
- **Slug or ID, never both.** Each article has exactly one canonical filename — use it as-is. No fabricated slugs.
- **Mode B edits get a preview-and-confirm step.** Direct edits to `Current-Release-Notes.mdx` always need user approval before saving.
