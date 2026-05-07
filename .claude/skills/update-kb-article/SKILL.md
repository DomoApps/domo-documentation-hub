---
name: update-kb-article
user-invocable: true
description: "update a KB article, rename a document, edit article content, update screenshots, swap screenshots, remove content, update file paths, cross-file updates, update steps in a process, combine articles, split an article, merge articles"
argument-hint: "article title, filename, or description of the change needed"
---

Update one or more existing KB articles. This skill handles all types of article edits, from simple content changes to complex multi-file operations like merges and splits.

The user has provided: $ARGUMENTS

---

## Core Principles

**Be eager about impact.** Before any change, identify every file and location that could be affected — across `s/article/`, `s/topic/`, `portal/`, and `docs.json`. Surface things the user might not have thought of.

**Be conservative about execution.** NEVER make a change without explicit user direction. Present findings, propose a plan, and wait for approval. When there are multiple possible changes, use the AskUserQuestion tool to let the user choose.

**Never touch localized directories.** Do not read, modify, suggest changes to, or reference anything in `/de`, `/es`, `/fr`, or `/ja`. These are managed separately.

**Follow shared standards.** When writing or rewriting any article content — including merged or split articles — read `New-Article-Template.mdx` for document structure and encoding conventions, and `Domo-KB-Style-Guide.mdx` for voice, formatting, and terminology. Read both files before writing any content.

---

## Step 1: Identify the article(s) and change type

If `$ARGUMENTS` names a file or topic, confirm the exact file path before proceeding.

To find an article by title keyword:
```bash
grep -rl "title:.*keyword" s/article/ s/topic/
```

To find by filename:
```bash
ls s/article/ | grep keyword
```

Once the file(s) are identified, ask the user what type of change they need — or confirm it if already stated. The change types are:

1. **Rename** — change the article title, filename, or both
2. **Content update** — edit body text, callouts, or other prose
3. **Image/screenshot swap** — replace one or more images, or swap a legacy image-based UI icon for the Domo icon font
4. **Content removal** — delete a section, step, or block
5. **File path update** — rename a file and update all references to it
6. **Cross-file change** — the same change needs to appear in multiple articles
7. **Step/process update** — add, remove, or reorder steps in a numbered list
8. **Navigation move** — relocate the article in the site nav
9. **Merge** — combine two or more articles into one
10. **Split** — break one article into two or more
11. **Beta status change** — mark a feature as beta, promote a beta feature to GA, or convert a legacy beta marker to the current convention

Use AskUserQuestion if you need to clarify which type applies, or if the user's description could map to more than one type.

---

## Step 2: Impact analysis

Run impact analysis before proposing any changes. The scope depends on the change type.

### For any change involving a filename or article path

Search for all references to the file across the codebase:

```bash
# Root-relative links: /s/article/Article-Name
grep -rn "s/article/Article-Name" s/article/ s/topic/ portal/ docs.json

# Absolute links: https://domo-support.domo.com/s/article/Article-Name
grep -rn "domo-support.domo.com/s/article/Article-Name" s/article/ s/topic/ portal/
```

**Both link formats must be found and updated.** Do not assume only one form is in use.

Also check `docs.json` for the page entry:
```bash
grep -n "Article-Name" docs.json
```

### For content updates and cross-file changes

If the change involves a feature, behavior, or setting that may be documented in multiple articles, search for the feature name across all articles to surface related files the user may not have considered:

```bash
grep -rl "feature name" s/article/ s/topic/
```

Present the list to the user and ask: which of these files also need to reflect this change?

### For image/screenshot swaps

Identify the current image filename(s) in the article and check if the same image is referenced in any other article:

```bash
grep -rn "image-filename.png" s/article/ s/topic/ portal/
```

If the image is shared, warn the user before any changes.

### For merges

For each source article being merged:
1. Find its current location in `docs.json`
2. Find all inbound links to it from other articles (both link formats)
3. Note its title and frontmatter

### For splits

1. Find all inbound links to the original article from other articles
2. Identify which inbound links should point to which new article after the split
3. Note the original's location in `docs.json`

---

## Step 3: Present findings and confirm the plan

After impact analysis, present a structured summary:

- **Files to be modified:** list each file and what would change
- **Files to be created:** (merges, splits)
- **Files to be deleted:** (merges, splits, after user confirms)
- **docs.json changes:** any navigation entries to add, remove, or move
- **Link updates:** list of files with inbound links that need updating
- **Things to watch out for:** anything ambiguous, risky, or that requires a human judgment call (e.g., which inbound links should point to which new article after a split)

If the list is long or involves choices, use AskUserQuestion to walk the user through their options rather than dumping everything at once.

**Do not proceed until the user has explicitly approved the plan.**

---

## Step 4: Execute approved changes

Make changes only for what the user has explicitly approved. Work through the change list one item at a time.

### Renaming a title only (frontmatter, not filename)

Edit the `title:` field in the article's frontmatter. The filename and all links remain unchanged.

### Renaming a file

1. Create the new file (copy content, update the `title:` if it's also changing).
2. Delete the old file.
3. Update every inbound link — both root-relative and absolute forms.
4. Update the `docs.json` page entry.

### Content updates, removals, step changes

Use the Edit tool with enough surrounding context (2–3 lines) to make `old_string` unique. Never rewrite more than what was approved.

### Image/screenshot swap

Update the `src` attribute in the `<Frame>` or `<img>` tag. Update `alt` text if appropriate. Do not move or delete image files — note to the user that the image asset itself must be updated separately in `images/kb/`.

### Image-based icon → icon font swap

Many older articles use `<img>`, `InlineImage`, or `<Icon icon="/images/icons/*.svg" />` for inline UI icons that now exist in the Domo icon font. The font version inherits text color and adapts to light/dark mode automatically; image-based icons don't.

When you're already updating an article and notice an image-based icon, propose swapping it to the font convention:

```mdx
<i className="icon-{name}" aria-hidden="true" />
```

Confirm a matching glyph exists at [Domo Icons](https://git.empdev.domo.com/pages/Development/DomoIcons/#!/icons/domocons) before proposing the swap — if the icon isn't in the font, leave the image as-is. Don't open a wholesale icon migration as a side effect of an unrelated update; only swap icons in the section the user asked you to change, plus any that read awkwardly inconsistent next to the change.

**Check the surrounding prose for an inline label.** When swapping (or auditing existing font icons), confirm the icon is named in the surrounding prose. If the prose says "click \<icon\>" with no inline label, propose rewriting it to "click the {name} icon \<icon\>". The inline-label rewrite is preferred over `aria-label` in flowing prose because it helps every reader, not just screen-reader users. Reserve `role="img"` + `aria-label="..."` for the narrow case where the icon truly stands alone with no room for prose (icon-only button, sole content of a link). See `Domo-KB-Style-Guide.mdx` › **Icons** for the full convention.

### Navigation move

Invoke the `add-to-nav` skill. Do not attempt to edit `docs.json` directly for navigation moves.

### Beta status change

Apply the convention defined in `Domo-KB-Style-Guide.mdx` › **Beta Features**. Read it before making changes. Summary:

- **Mark a whole article as beta:** add `tag: "Beta"` to the frontmatter and insert the standard beta Note immediately after the frontmatter, above the Intro. Do not append `(Beta)` to the title.
- **Mark a section as beta:** append `<Badge className="text-primary bg-primary/10 font-bold">Beta</Badge>` to the heading. If the article has no other beta sections, also place the standard beta Note under that section. If another section in the same article is already marked beta, do not add another Note — one Note per article.
- **Promote beta to GA (whole article):** remove the `tag: "Beta"` line from frontmatter and remove the standard beta Note above the Intro.
- **Promote beta to GA (section):** remove the Badge from the heading. If the Note immediately below this section was the article's single beta Note, decide where it should go: if other sections remain beta, move it under the first remaining beta section; if no beta sections remain, remove the Note.
- **Convert legacy beta markers:** when you find `(Beta)` or `(BETA)` in titles or headings, ad-hoc beta notes, references to `betafeedback@domo.com` or `betadmin@domo.com`, or other legacy treatments, replace them with the current convention (tag + standard Note for whole-article betas; Badge + single standard Note for section-level betas). When updating cross-article links whose anchor text contained `(Beta)`, drop the parenthetical from the link text as well.

The Badge `className` must be exactly `text-primary bg-primary/10 font-bold`. The standard beta Note must be used verbatim — copy it from the style guide.

### Merge

1. Draft the merged article content and show it to the user for approval before writing any files.
2. Write the new merged file to `s/article/`.
3. Add it to `docs.json` navigation (use `add-to-nav` skill).
4. Update all inbound links from other articles to point to the new file.
5. Ask the user explicitly whether to delete each source article before deleting anything.
6. If deleting, remove from `docs.json` as well.

### Split

1. Draft both (or all) new article files and show them to the user for approval before writing any files.
2. Write the new files to `s/article/`.
3. Add each to `docs.json` navigation (use `add-to-nav` skill).
4. For each inbound link to the original article, determine (with the user) which new article it should point to, then update.
5. Ask the user explicitly whether to delete the original article before deleting anything.
6. If deleting, remove from `docs.json` as well.

---

## Step 5: Verify

After all edits:

1. Validate `docs.json` if it was changed:
   ```bash
   python3 -c "import json; json.load(open('docs.json')); print('docs.json is valid JSON')"
   ```

2. Confirm no broken references remain for any renamed or deleted file:
   ```bash
   grep -rn "old-filename" s/article/ s/topic/ portal/ docs.json
   ```

Report any remaining references to the user.

---

## Step 6: Output

Tell the user:
- What was changed, created, or deleted
- Any follow-up actions they need to handle manually (e.g., uploading new image assets, updating absolute links on the live Salesforce support site)
- Any files that were intentionally left unchanged and why
