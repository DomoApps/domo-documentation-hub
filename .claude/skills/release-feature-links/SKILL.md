---
name: release-feature-links
description: For a monthly release, match every feature in the PMM source copy to a KB article in s/article/ and produce link sentences. Two targets — (1) PMM Release Article: emit copy-paste-ready feature + link sentences (with https://www.domo.com/docs prefix) for the shared Word doc; (2) Current Release Notes: edit s/article/Current-Release-Notes.mdx in place, inserting link sentences inline. Two intents — net-new generation (all features) or update (refresh missing/generic links after new KB articles publish). Use when the user asks to "add KB links to the release article", "wire up links for the May release", "update the May release links now that the X article shipped", "match KB articles to release features", or similar.
---

# Release Feature → KB Article Linker

Each Domo monthly release ships a marketing/PMM article that introduces every new feature, plus an in-repo `Current-Release-Notes.mdx`. Both documents need links from each feature blurb back to the relevant KB article in `s/article/`. KB articles often publish on a staggered schedule — some features ship without a dedicated article and only get one a week or two later. So linking happens in two phases:

- **Net-new** — first pass when the release ships; produce link sentences for every feature that already has an article.
- **Update** — later passes after additional KB articles publish; replace missing or generic/umbrella links with the new, more specific article.

Combined with the two output targets (PMM, Current Release Notes), that gives **four pathways**. The skill picks the right one based on the user's answers in step 1.

## Workflow

### 1. Ask the user three clarifying questions

Use **AskUserQuestion** with three questions in a single call:

1. **Intent** — net-new or update?
   - `Net-new` — first pass; generate link sentences for every feature in the source copy.
   - `Update` — refresh existing links; only handle features that previously had no link or pointed to a generic/umbrella article and now have a better match.
2. **Target document** — which output mode?
   - `PMM Release Article` (external Word doc — output is copy-paste-ready text).
   - `Current Release Notes` (in-repo `s/article/Current-Release-Notes.mdx` — edit the file directly).
3. **Source copy file** — which `.txt` file in the repo contains the PMM draft copy for this release?

If helpful, list candidate `.txt` files before asking question 3:

```bash
ls *.txt 2>/dev/null
```

The user can pick by name.

Once you have the user's three answers, route to the matching pathway in step 5. Steps 2–4 (extract features, match articles, build link sentences) are shared by all four pathways with small variations noted below.

### 2. Extract the feature list from the PMM source copy

Read the chosen `.txt` file. Features are typically introduced in two ways:

- An ordered list near the top under headings like *"Order of Release for New Features Page"* or *"New Features / Feature Enhancements"* / *"Beta Features"*.
- Each feature then appears again as its own section header further down with its target persona, meta description, tags, and web copy.

Extract a deduplicated list of feature names, preserving the release ordering. Be alert for:

- Slight name variations between the table-of-contents list and the section headers (e.g. *"AI Classification tile"* vs *"AI Classification Tile"* vs *"Magic ETL AI Classification Tile"*) — normalize to the section-header form.
- Sub-features nested under a parent (e.g. *Workflow Event Triggering – Access Request* and *Queue Notification Controls* under *Workflows Updates*; *AI Classification Tile*, *Sentiment Analysis Tile*, *Multi-Statement SQL Tile* under *Magic ETL Enhancements*). Treat each sub-feature as its own item — they each need their own link.

**Update mode narrows this list** — see step 5's pathway sections for how to scope it.

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
- **Feature umbrella articles** — multiple new tiles can share one article (e.g. *"Magic ETL Tiles: AI Services"* covers Text Generation, Classification, and Sentiment). Use the same article for all sub-features and **deep-link to the sub-section's header anchor** (see "Header anchors" below). If the sub-section may not yet be published, flag that in your output.
- **Newly added articles** — recently-added KB content for this release will likely show up here:

  ```bash
  git log main..HEAD --name-status --pretty=format: -- s/article/ | grep -E "^A\s"
  ```

  Check those first before broader searches. **Update mode especially relies on this** — see pathway B/D below.
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

**Header anchors for sub-features** — if the matched article is an umbrella article and the feature is documented as a sub-section within it, **append the section's Mintlify anchor** to the URL so the link jumps straight to that section. Anchors are the rendered section header converted to lowercase, with spaces and most punctuation replaced by hyphens, and inline `<Badge>` content (e.g. `Beta`) included as a trailing hyphenated word.

To find the anchor, read the matched article and locate the `##` / `###` header that names the sub-feature. Then derive:

- `## Text Generation Tile <Badge ...>Beta</Badge>` → `#text-generation-tile-beta`
- `## AI Classification Tile` → `#ai-classification-tile`
- `### Admin Notification Setting` → `#admin-notification-setting`

Apply the anchor to both PMM mode and Current Release Notes mode URLs.

**Sentence style** — keep it short and conversational. Prefer "Learn more about..." or "Learn more about how to..." patterns, but vary if the feature name doesn't slot naturally. Examples:

> Learn more about [Domo Essentials MCP](https://www.domo.com/docs/s/article/Connect-AI-Tools-to-Domo-Using-MCP).

> Learn more about the [Text Generation DataFlow Tile in Magic ETL](https://www.domo.com/docs/s/article/000005741#text-generation-tile-beta).

### 5. Deliver based on pathway

Pick exactly one of the four pathways below based on the user's intent + target answers in step 1.

---

#### Pathway A — Net-new × PMM Release Article

**When**: First-pass link generation for the marketing PMM article (external Word doc).

1. Use the full feature list extracted in step 2.
2. Match each feature against `s/article/` per step 3.
3. For each feature with a confirmed match, build a link sentence (step 4) using the **external** `https://www.domo.com/docs/...` URL.
4. Output a flat list, one block per feature:

   ```markdown
   **<Feature Name>**
   > <link sentence with full https://www.domo.com/docs URL>
   ```

5. For features without a matched article, emit the feature name plus an italicized note explaining what was checked and recommending the user follow up with the writer. Do **not** fabricate a link.
6. Do **not** edit the source `.txt` file — it's a reference snapshot.

User pastes each link sentence into the corresponding feature section of the Word doc.

---

#### Pathway B — Update × PMM Release Article

**When**: A KB article has just published for a feature that shipped without one (or with a generic umbrella link), and the user needs an updated link sentence to swap into the Word doc.

1. **Scope the update**. The Word doc isn't in the repo, so we can't tell which features have weak links — ask the user. Use **AskUserQuestion** with one question:

   > Which features need updated link sentences? Pick from the feature list in `<source-copy.txt>`, or describe the criteria (e.g. "any feature whose KB article was added this week").

   Offer concrete options based on context:
   - A list of the specific feature names the user mentions.
   - `Scan recently-added articles` — find articles added since the release tag, then map them back to PMM features automatically.
   - `Other` — let the user free-form a list.

   If the user picks "Scan recently-added articles," run:

   ```bash
   # Articles added on this release branch
   git log main..HEAD --name-status --pretty=format: -- s/article/ | grep -E "^A\s"

   # Or articles added since a specific date
   git log --since="<date>" --name-status --pretty=format: -- s/article/ | grep -E "^A\s"
   ```

   Then cross-reference titles against the feature list from step 2 to identify candidates for update.

2. For each scoped feature, run step 3 (match) and step 4 (build sentence) — **always using the external URL format**.

3. Output only the **changed** features, in the same per-block format as pathway A, with a one-line lead-in indicating what changed:

   ```markdown
   **<Feature Name>** *(previously: no link / linked to umbrella article X)*
   > <new link sentence with full https://www.domo.com/docs URL>
   ```

   Skip features whose best match hasn't changed since the prior pass — no point cluttering the output.

4. Do **not** edit the source `.txt` file.

User pastes each updated link sentence into the corresponding feature section of the Word doc, replacing the prior link (or filling in where there was none).

---

#### Pathway C — Net-new × Current Release Notes

**When**: First-pass link generation for the in-repo `s/article/Current-Release-Notes.mdx`.

1. Read `s/article/Current-Release-Notes.mdx` to see the current section structure.
2. Use the full feature list extracted in step 2 (from the source `.txt`).
3. For each feature with a confirmed match (step 3), locate the corresponding section in `Current-Release-Notes.mdx` by section header (e.g. `### Domo Essentials MCP`). Section headers in the release notes are usually shorter/cleaner than PMM headers — match on the core feature name, not exact string.
4. Draft an inline link sentence (step 4) using the **internal** `/s/article/<slug>` format. Place it at the end of the section's body text (after the `<Frame>` screenshot block if one exists, but before the next `###` header).
5. **Before saving any edits**, show the user every proposed change as a preview — feature name, target section, exact sentence you'll insert. Wait for confirmation.
6. After approval, use the **Edit** tool to insert each sentence. **One edit per feature** — do not bundle multiple feature edits into a single replace block (keeps diffs reviewable).
7. For features without a matched article, list them at the end with a short note — do not edit those sections.

---

#### Pathway D — Update × Current Release Notes

**When**: New KB articles have published since the initial release-notes commit and need to be linked into existing sections of `Current-Release-Notes.mdx`.

1. Read `s/article/Current-Release-Notes.mdx`.
2. **Identify update candidates automatically** — for each `###` (or `####`) feature section, check whether it already contains an inline `/s/article/...` link in its body. Build two buckets:
   - **No link** — sections with no inline KB link at all.
   - **Generic / umbrella link** — sections whose only link points to an umbrella article when a more specific article now exists. (Detect by re-running step 3 for those features and seeing if the best match has changed since the existing link was written.)
3. Present the candidate list back to the user for confirmation:

   ```markdown
   Found <N> sections that may need link updates:
   - **<Feature>** — currently <no link | links to umbrella X>; proposed <new article Y>
   - ...
   ```

   Ask the user to confirm the scope (all, subset, or skip any).
4. For each confirmed candidate, draft an inline link sentence (step 4, internal URL format) and place it at the end of the section body.
5. **Show every proposed edit as a preview** — section header, existing text around the insertion point, exact sentence you'll insert. Wait for confirmation before any writes.
6. After approval, use **Edit** to insert each sentence one feature at a time.
7. If a section already has a weaker link sentence that's being replaced (not just supplemented), make that explicit in the preview and use **Edit**'s `old_string` → `new_string` to swap the sentence cleanly.

### 6. Final summary

After delivery, give the user a one-paragraph summary:

- **Pathway A/C** — total features in source copy, count linked, count flagged for follow-up. For C, confirm the file was saved.
- **Pathway B/D** — number of features re-checked, number updated, number unchanged, number still without a match. For D, confirm the file was saved.

## Important reminders

- **Never edit the source `.txt` file.** It's a reference snapshot of the marketing doc, not the canonical version.
- **Verify before linking.** A keyword grep can produce false positives (e.g. *"Jupyter Workspaces"* vs *"Workspaces"*). Always confirm with title + a brief body read.
- **Don't invent URLs.** If no matching KB article exists, say so — recommend the user check with the writer assigned to that feature.
- **Slug or ID, never both.** Each article has exactly one canonical filename — use it as-is. No fabricated slugs.
- **Update pathways replace, not duplicate.** When updating Current-Release-Notes.mdx, if a weaker link sentence already exists in the section, swap it cleanly with `Edit`'s old_string → new_string; don't append a second sentence.
- **All in-repo edits get a preview-and-confirm step.** Direct edits to `Current-Release-Notes.mdx` always need user approval before saving — true in both pathway C and pathway D.
