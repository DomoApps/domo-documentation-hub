---
name: release-notes
description: Generate user-friendly release notes by diffing the latest git tag against the previous tag and summarizing the changes. Use when the user asks to "generate release notes", "write release notes for the latest release", "summarize the latest release", or similar. Saves a shareable MDX file to `releaseNotes/` and a sanitized external version to `releaseNotesExternal/`.
---

# Release Notes Generator

Produce a friendly, email/Slack-ready release notes summary for the most recent git tag in this repo.

## Workflow

### 1. Identify the release range

```bash
git tag --sort=-creatordate | head -5
```

The top tag is the **latest release**; the next tag is the **previous release**. Confirm with the user only if the intended target is ambiguous (e.g. multiple tags on the same day, or user mentions a specific version).

Also grab tag dates for context:

```bash
git log --tags --simplify-by-decoration --pretty="format:%ai %d" | head -10
```

### 2. Diff the releases

```bash
git log <prev-tag>..<latest-tag> --stat
git diff --name-status <prev-tag>..<latest-tag>
```

`--name-status` is what you'll use later to classify articles as new (`A`), modified (`M`), or renamed (`R…` — always use the new path). For any commit whose purpose isn't obvious from the message + file list, inspect the content:

```bash
git diff <prev-tag>..<latest-tag> -- <path>
```

Skip merge-commit noise — focus on the underlying PRs and file changes. Group related commits (e.g. multiple commits from one PR) into a single theme.

### 3. Identify linkable articles

Every **net-new** article and every **substantially revised** article gets an inline link in the prose (see step 5 for the link format).

**Which paths qualify as articles** — only these prefixes; skip everything else:
- `s/article/`
- `s/topic/`
- `portal/`

Explicitly **skip** `docs.json`, `images/`, `openapi/`, `.csv`, `releaseNotes/`, and the localized roots `de/`, `es/`, `fr/`, `ja/` (translations of existing English content — not separately linkable here).

**Net-new articles** = `A` status in `git diff --name-status`. Always linked.

**Substantially revised articles** = `M` status AND **either**:
- Net change ≥30 lines (check with `git diff --shortstat <prev>..<latest> -- <path>`), **or**
- The diff adds a new heading/section, a new FAQ entry, a new task/procedure, or one or more new screenshots — even if line count is small.

Skip articles whose only diff is a typo fix, single-field rename, table re-sort, or other cosmetic edit. In batch themes (e.g., "Connector Article Polish") this means most bullets stay unlinked — only call out and link the articles inside the batch that independently clear the substantial bar.

To pull the anchor text for a numeric-ID file like `s/article/000005241.mdx`, read the `title:` frontmatter — never use the bare ID as link text. Re-case the title to fit the sentence (mid-sentence prose is usually lowercase except for proper nouns).

### 4. Summarize into themes

Group changes into 2–5 themed sections. Each theme gets:
- An emoji + short title (e.g. "📚 Domo.js Versioned Documentation")
- 1–3 sentences describing what changed and why it matters **to the reader** (developers, admins, customers — not internal mechanics)
- Attribution to the contributor(s) by name — pull author names from `git log`

Prefer customer-visible framing over commit-message literalism. "DOMO-482176: add v4 doc" becomes "Dedicated version-specific docs for Domo.js v4, v5, and v6."

### 5. Add inline article links

For every article identified as linkable in step 3, weave a link into the prose where that article is introduced. The link does **not** stand alone as a "Read more:" bullet — it's part of a natural sentence the reader encounters as they learn about the change.

**URL format:** `https://www.domo.com/docs/` + the repo path with `.mdx` stripped. Examples:
- `s/article/Configure-Data-Freshness-and-Caching-in-Cloud-Integrations.mdx` → `https://www.domo.com/docs/s/article/Configure-Data-Freshness-and-Caching-in-Cloud-Integrations`
- `s/article/000005241.mdx` → `https://www.domo.com/docs/s/article/000005241`
- `portal/Apps/App-Framework/Guides/design-guide.mdx` → `https://www.domo.com/docs/portal/Apps/App-Framework/Guides/design-guide`

**Anchor text:** derive from the article's title or the topic just described, then re-case it for mid-sentence flow. Don't quote the title verbatim if it reads awkwardly. Example: title `"Configuring Data Freshness and Caching in Cloud Integrations"` → anchor `configuring data freshness and caching in Cloud Integrations`.

**Where the link goes:** append a short sentence at the end of the segment that introduces the article — typically starting with "Learn more about…", "Read the full…", "See the new…", or similar. For batch themes, append it to the specific bullet whose article qualifies; leave the other bullets unlinked.

Worked example (Cloud Integrations Overhaul, v2.4.0):

> A brand-new dedicated KB article, "Configuring Data Freshness and Caching in Cloud Integrations," now lives on its own page so admins can find freshness and caching guidance without scrolling through the full overview. The article includes step-by-step enablement instructions, interval configuration, and a grouped FAQ section covering common questions. Learn more about [configuring data freshness and caching in Cloud Integrations](https://www.domo.com/docs/s/article/Configure-Data-Freshness-and-Caching-in-Cloud-Integrations).

**Sanity check:** Mintlify normally maps file path → URL 1:1, but `docs.json` can technically remap routes. If a link looks suspicious, spot-check by opening the generated URL.

### 6. Write the file

Save to `releaseNotes/v<version>.mdx`. The file is MDX so it renders cleanly when viewed in the repo or pasted into Mintlify, but it's also written to read well when copy/pasted into email or Slack — keep prose plain and avoid Mintlify-only components (no `<Frame>`, `<Note>`, `<Accordion>`, etc.).

Follow this structure:

````mdx
---
title: "Domo Documentation Hub v<X.Y.Z> Release Notes"
---

Hello everyone!

We're excited to announce that version <X.Y.Z> of the Domo Documentation Hub is now available! <one-sentence framing of the release's overall theme> You can view these changes in our knowledge base at [www.domo.com/docs](https://www.domo.com/docs).

## 🌟 What's New

### <emoji> <Theme Title>

<1–3 sentences describing the change and its value.>

Thanks to <Contributor> for <brief reason>.

<repeat `###` block for each theme>

## 🙏 Thank You

A heartfelt thank you to everyone who contributed to this release. <one warm closing sentence>

If you have questions or feedback, please reach out — we're always happy to help!
````

Formatting rules:

- YAML frontmatter with a `title` field is required.
- Top-level sections use `##`; per-theme headings use `###`. The emoji stays inline in the heading.
- Use markdown `-` bullets (not `•`) for sub-lists inside a theme.
- Links use markdown syntax `[anchor](https://www.domo.com/docs/...)` — never bare URLs in prose (the intro `www.domo.com/docs` mention is the one exception and should also be linkified).
- Leave a blank line between paragraphs, between a paragraph and a list, and between consecutive headings — MDX rendering needs the breathing room.

Keep tone warm and appreciative.

### 7. Generate the external version

After saving the internal file, produce a sanitized copy for external audiences (customers, partners, public-facing channels) and save it to `releaseNotesExternal/v<version>.mdx`.

**What to strip or omit:**

- **Contributor attribution** — remove every "Thanks to [Name] for…" sentence. The closing "Thank You" section may be kept but must not name individuals; replace with a generic warm sign-off (e.g., "A heartfelt thank you to everyone who helped make this release possible.").
- **Internal-only themes** — drop entire `###` sections whose subject matter is not visible to or useful for Domo customers. Examples of internal-only content:
  - New or updated Claude AI skills, slash commands, or documentation-team workflows
  - GitHub Actions or CI/CD pipeline changes
  - Internal scripts, tooling, or developer-experience improvements that don't affect the public docs site
  - Changes to `CLAUDE.md`, `.claude/`, or other repo-meta files
- **Everything else stays** — all customer-facing article additions and updates remain, including links.

**Title and intro:** Keep the same version number and framing. The title field does not need to change. Adjust the intro only if it references themes you've dropped.

**File location:** `releaseNotesExternal/v<version>.mdx` — the `Write` tool creates the directory automatically.

### 8. Confirm

Tell the user both file paths and offer to adjust tone, detail, or framing for either version.

## Notes

- Always create `releaseNotes/` and `releaseNotesExternal/` if they don't exist — `Write` handles this automatically.
- Do **not** include internal ticket IDs (DOMO-XXXXXX) in either version unless the user asks; parenthetical attribution is fine in the internal version.
- Do **not** commit either file unless the user asks.
