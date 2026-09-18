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

**Preserve the source's wording.** When a change brings in new copy — the user's own words, pasted notes, a draft, or other source material — keep that direct phrasing and word choice by default rather than restating it; the author's terms carry nuance about how the functionality behaves. Take the source text as-is, fit it into the article, and revise wording only where a `Domo-KB-Style-Guide.mdx` or `New-Article-Template.mdx` rule requires it (recast grammatical framing — person, tense, active voice — into house style, but keep the author's substantive terminology). This compounds with *Be conservative about execution*: never rewrite more than the change requires, and never paraphrase source wording for its own sake. If information is missing, ask the user rather than inventing it.

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

Once the file(s) are identified, look up the PM who owns the article in `Article-PM-Ownership-Reference.mdx`:

```bash
grep "filename.mdx" Article-PM-Ownership-Reference.mdx
```

Surface the owning PM and Feature to the user — useful for routing questions, review requests, or approvals before or after the change. If the article isn't in the reference (e.g. a brand-new file), look up the closest matching Feature in `Feature - Owning Squad, PM, Eng, UX.csv`.

Then ask the user what type of change they need — or confirm it if already stated. The change types are:

1. **Rename** — change the article title, filename, or both. By convention the title and filename match, so a title change normally renames the file too (and updates links + `docs.json`); state the rule and ask before keeping them separate. See Step 5 › *Renaming a title*.
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

## Step 4: Confirm screenshot and icon handling

If the approved change adds, replaces, or removes screenshots or icons, confirm with the user up front how to handle them before you execute. (Skip this step for text-only changes that touch no images or icons.)

**Screenshots** — offer these options with AskUserQuestion:

1. **User provides new screenshots** — the files must be committed to `images/kb/` on the same branch before the article references them (see `CLAUDE.md` › **MDX Content Conventions**). Ask for the exact filenames.
2. **Reuse existing screenshots** — an image already in the repo or the source material, with its original `alt` text preserved.
3. **Remove without replacing** — drop a stale screenshot and keep the surrounding text self-sufficient. This is the preferred default when a fresh capture isn't ready; the article should be publishable as-is without the image.
4. **Placeholders (opt-in only)** — `{/* SCREENSHOT: <what the image should show> */}` markers, **only if the user explicitly asks**. The default is a clean article with no TODO or placeholder markers.

Whichever option is chosen, keep step text self-sufficient — a reader can complete the task without ever seeing a screenshot.

**Icons** — if the change introduces *new* UI icons, confirm them and code them per the reference below. (Existing *legacy* icons already in the article are upgraded automatically in Step 7 — you don't need to ask about those.)

**Coding reference** (from `Domo-KB-Style-Guide.mdx` › **Screenshots**, **Icons**, **Inline Images**):

- **Block screenshot:** `<Frame><img src="/images/kb/example.png" alt="Descriptive alt text" /></Frame>` — no inline `width`/`height`; never inside a table cell.
- **Current Domo UI glyph:** `<i className="icon-{name}" aria-hidden="true" />` (Phosphor). Browse names at [Domo Icons](https://git.empdev.domo.com/pages/Development/DomoIcons/#!/icons/phosphor).
- **Legacy UI glyph:** `<i className="legacy-icon-{name}" aria-hidden="true" />` — only for release-notes/Workbench surfaces.
- **Third-party brand logo:** Font Awesome brands `<Icon icon="{slug}" iconType="brands" aria-hidden="true" />`, or inline `<svg fill="currentColor" …>` when the free FA set lacks it. Never a monochrome `<img>` logo — it disappears in dark mode.
- **Glyph not in the font:** inline `<img>` with `style={{height: '1.2em', display: 'inline', verticalAlign: 'start', margin: '0'}}`.
- **Accessibility:** always add `aria-hidden="true"` and name the icon in the prose; reserve `role="img"` + `aria-label` for an icon that stands alone.

---

## Step 5: Execute approved changes

Make changes only for what the user has explicitly approved. Work through the change list one item at a time.

**Preserve source wording as you write.** For any copy you add or rewrite, follow the source-fidelity default: reuse the user's / source's direct phrasing and word choice, reorganize it to fit, add only what flow or structure needs, and change wording only where a style-guide or template rule requires (recast framing into house voice; keep substantive terminology). If the change needs information you don't have, ask the user — don't invent it. See **Core Principles** › *Preserve the source's wording*.

### Renaming a title (and the filename-match convention)

**Convention: an article's `title` and its filename should match.** A slug-named article's filename is the Title-Case, hyphen-separated form of its title (`Article Title Here` ↔ `Article-Title-Here.mdx`). So when a user changes the **title**, the default is to change the **filename to match** — which turns the edit into a full file rename: create the renamed file, delete the old one, update every inbound link (both root-relative and absolute forms — see *Renaming a file* below), and update the `docs.json` page entry.

**Always state this rule, then ask** whether the user wants the title and filename to stay in sync or to diverge intentionally. Sometimes keeping them different is deliberate — do that only when the user confirms it. Use AskUserQuestion so the choice is explicit:

- **Rename the file to match (default).** Full file-rename impact: new file, delete the old one, update all inbound links, update `docs.json`.
- **Change the title only, keep the filename.** Only the `title:` frontmatter changes; the filename, all links, and the `docs.json` page path stay as they are.

**Exception — numeric-ID filenames.** Legacy KB articles are named by numeric ID (`000005874.mdx`), which intentionally does **not** match the title. Never rename these to match a title change — edit the `title:` field only. The match convention applies to slug-named files.

If the user chooses title-only, edit the `title:` field in the frontmatter; the filename and all links remain unchanged.

### Renaming a file

1. Create the new file (copy content, update the `title:` if it's also changing).
2. Delete the old file.
3. Update every inbound link — both root-relative and absolute forms.
4. Update the `docs.json` page entry.

### Content updates, removals, step changes

Use the Edit tool with enough surrounding context (2–3 lines) to make `old_string` unique. Never rewrite more than what was approved.

### Writing or editing a Required Grants section

When an edit adds or changes a **Required Grants** section, use the grant's canonical wording — don't invent a description. Most grants are already described in the standard format elsewhere in the KB; search for and reuse the existing wording so the grant reads consistently across articles:

```bash
grep -rn "Grant Name —" s/article/
```

Reuse the existing description verbatim (adjusting only to fit the em-dash format). If no article describes the grant, write a concise one-sentence description and flag it to the user as newly authored rather than presenting it as canonical. See `Domo-KB-Style-Guide.mdx` › **Required Grants** › _Use canonical grant wording_.

### Image/screenshot swap

Update the `src` attribute in the `<Frame>` or `<img>` tag. Update `alt` text if appropriate. Do not move or delete image files — note to the user that the image asset itself must be updated separately in `images/kb/`.

### Image-based icon → icon font swap

Many older articles use `<img>` or `<Icon icon="/images/icons/*.svg" />` for inline UI icons that now exist in the Domo icon fonts. The font versions inherit text color and adapt to light/dark mode automatically; image-based icons don't.

Two icon fonts are wired up, and they ship the **same glyph set** — the choice is about which UI the article depicts, not glyph availability:

- **`icon-{name}`** — phosphor, the design refresh. **Default for current Domo product surfaces.** Browse at [Domo Icons (phosphor)](https://git.empdev.domo.com/pages/Development/DomoIcons/#!/icons/phosphor).
- **`legacy-icon-{name}`** — the previous-generation Domo icons. **Only for release notes describing the pre-refresh UI and legacy applications like Workbench.** Browse at [Domo Icons (domocons)](https://git.empdev.domo.com/pages/Development/DomoIcons/#!/icons/domocons).

When you're already updating an article and notice an image-based icon, propose swapping it to the font convention. **Pick the font based on the UI surface the article describes:**

```mdx
<i className="icon-{name}" aria-hidden="true" />              {/* current Domo UI */}
<i className="legacy-icon-{name}" aria-hidden="true" />       {/* release notes / Workbench */}
```

**Stale-screenshot upgrade case.** If the article describes the *current* Domo UI but the original `<img>` showed a legacy-style glyph, that screenshot is just out of date — swap to the phosphor `icon-*` version (not `legacy-icon-*`) so the article reflects what users see today.

**Third-party brand logos** (AWS, OpenAI, Anthropic, GitHub, …) are a different swap — they're *not* in the Domo icon font, and a monochrome logo `<img>` disappears in dark mode. Swap to a coded icon that inherits text color: Font Awesome's `brands` family via `<Icon icon="{slug}" iconType="brands" aria-hidden="true" />` (the one correct use of `<Icon>` — it resolves a font glyph, not a local SVG), or, when FA's free set lacks the brand (e.g. Anthropic), an inline `<svg fill="currentColor">` with a path from a source like [Simple Icons](https://simpleicons.org). See `Domo-KB-Style-Guide.mdx` › **Brand and Third-Party Logos**.

**Whole-article legacy-icon migration is now automatic — see Step 7.** By standing instruction from the Knowledge Base Administrator, any article you edit has *all* of its legacy image-based icons upgraded to the icon font across the entire file, not just the section you touched. Step 7 covers that mandatory pass and the notice you give the user. This subsection gives you the mechanics (which font, the stale-screenshot case, brand logos, accessibility); Step 7 tells you when to apply them article-wide.

**Check the surrounding prose for an inline label.** When swapping (or auditing existing font icons), confirm the icon is named in the surrounding prose. If the prose says "click \<icon\>" with no inline label, propose rewriting it to "click the {name} icon \<icon\>". The inline-label rewrite is preferred over `aria-label` in flowing prose because it helps every reader, not just screen-reader users. Reserve `role="img"` + `aria-label="..."` for the narrow case where the icon truly stands alone with no room for prose (icon-only button, sole content of a link). See `Domo-KB-Style-Guide.mdx` › **Icons** for the full convention.

### HTML table normalization

Many migrated articles ship HTML tables collapsed onto a single line, often with data rows wrapped inside `<thead>` instead of `<tbody>`. Both are migration artifacts: the single-line form blows past VS Code's syntax-highlighting threshold (so the table renders as one unhighlighted blob), and the misplaced data rows cause browsers to vertically center-align the cells.

When you're already editing a section that touches one of these tables, normalize it: put `<table>`, `<thead>`, `<tbody>`, each `<tr>`, and their closing tags on their own lines, and move data rows into `<tbody>`. See `Domo-KB-Style-Guide.mdx` › **Tables** › **HTML tables** for the canonical form.

Unlike the automatic legacy-icon migration (Step 7), HTML table normalization stays conservative: don't reformat every HTML table you encounter — only the tables in the section the user asked you to change, plus any directly adjacent ones that would look inconsistent.

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

## Step 6: Fact-check pass

Before the edit pass, and before considering the change complete, fact-check the content you added or rewrote against an authoritative source: the source material the user provided, what the user told you about the change, and the repo itself. Scope this to what you changed — you are not re-verifying the whole article — but every claim your edit introduces or alters must be confirmed at least once. When you correct an unsupported claim, prefer restoring the source's own wording over inventing a replacement.

1. **Go claim by claim over the changed content.** For each statement of fact you added or modified — steps, behaviors, settings, defaults, names, values, URLs, limits — confirm it against the source or existing repo content. Where the repo is the authority, search it and read the relevant article rather than trusting your edit:
   ```bash
   grep -rl "feature or setting name" s/article/ s/topic/
   ```

2. **Verify Prerequisites and Required Grants with special care** whenever your change touches them — they are the highest-risk sections and the most common source of factual errors:
   - Confirm each prerequisite is real and actually required for the task.
   - Confirm each grant name exists and gates the described action. Cross-check the canonical grant wording (`grep -rn "Grant Name —" s/article/`) and any related feature articles.
   - If the source material doesn't establish the exact prerequisites and grants, **do not infer them — ask the user.**

3. **When you can't confirm a claim, or you find an inaccuracy or a discrepancy, STOP and ask the user directly** for the missing or correct information before finalizing. Do not guess, approximate, or fill gaps with plausible-sounding content. Name exactly what you couldn't verify and what you need.

The change is not complete until every fact your edit introduces is confirmed against a source or explicitly confirmed by the user. **When in doubt, ask** — a paused edit beats a confidently wrong one. If, during the fact-check, you discover the requested change itself rests on a wrong premise, surface that to the user rather than encoding it.

---

## Step 7: Upgrade legacy icons (automatic, whole-article)

**Standing instruction from the Knowledge Base Administrator.** Whenever you edit an article, upgrade *every* legacy image-based icon in that file to the Domo icon font — across the whole article, not only the section you changed. This is an automated maintenance pass that runs on every edit until all legacy icons in the KB have been replaced. **You are not asking permission for this** — you make the swap and inform the user (wording below).

1. **Detect legacy icons across the whole file.** Look for the pre-font patterns the style guide flags as legacy:
   ```bash
   grep -nE "images/(kb|icons)/[^\")]*icon|<Icon icon=\"/images" <file>
   ```
   The classic form is an inline `<img>` styled as a glyph — `<img src="/images/kb/*-icon.png" style={{width: 20, height: 20, …}}/>` — or an `<Icon icon="/images/icons/*.svg" />`. See `Domo-KB-Style-Guide.mdx` › **Icons in Migrated Articles**.

2. **Swap each to the font**, using the mechanics in Step 5's *Image-based icon → icon font swap* subsection:
   - Current-UI glyph → `<i className="icon-{name}" aria-hidden="true" />` (Phosphor). This is the default, including the stale-screenshot case where an old `<img>` showed a legacy glyph but the article describes today's UI.
   - Legacy-UI surface (release notes, Workbench) → `<i className="legacy-icon-{name}" aria-hidden="true" />`.
   - Third-party brand logo → Font Awesome brands or inline `<svg fill="currentColor">`, never a monochrome `<img>`.
   - Name each icon in the surrounding prose; add `aria-hidden="true"`.

3. **Genuinely-not-in-font images are not legacy icons.** If an inline `<img>` depicts a UI fragment that has no icon-font equivalent, it is a legitimate inline image (see the style guide's **Inline Images**) — leave it. If you're unsure whether a font glyph matches a given image icon, **ask the user** rather than guessing at a glyph name.

4. **Inform the user.** In your Step 10 output, include a short notice, for example:

   > **Heads-up (automated):** This article had legacy image-based icons, so I upgraded them to the current Domo icon font across the whole file. This is a standing automated update from the Knowledge Base Administrator — I'm just making you aware. We're doing this on every edit until all old icons are replaced with the new icon library.

   If the article had no legacy icons, this step is a no-op — say nothing.

---

## Step 8: Edit pass — style guide and template

Editing introduces style drift just as drafting does. After the fact-check pass (and the icon upgrade), do an explicit editing pass against **both** `Domo-KB-Style-Guide.mdx` **and** `New-Article-Template.mdx` over the content you changed, and revise it in place. This pass catches usage, style, grammar, and structural mistakes. As you fix style, keep the source's substantive wording intact — change only what a rule requires.

1. **Re-read `Domo-KB-Style-Guide.mdx` and `New-Article-Template.mdx` now, in full** — not from memory. Confirm your changed content matches the template's structure and encoding conventions.
2. **Proofread the changed content for plain grammar and usage** — spelling, agreement, punctuation, clarity — alongside the Domo-specific rules below.
3. **Audit the content you added or rewrote** against this checklist and fix every violation. Scope this to what you changed: fix style errors in your edited content and any clearly broken style directly adjacent to it, but do not silently rewrite untouched sections. If you spot broader pre-existing violations outside your edit, note them to the user rather than rewriting them (consistent with this skill's conservative-execution principle). This pass is EN-only — never touch the localized directories.
   - **Intro** (if touched) — opens with "This article explains…" or "This article covers…", states only what the article covers, and is followed by a `---` horizontal rule.
   - **Headings** — imperative mood at every level; the structural labels (Intro, Required Grants, Prerequisites, FAQ, Troubleshoot, Related Articles) are exempt. Top-level sections H2, subsections H3+.
   - **Required Grants** — exact format and canonical grant wording, with the em-dash inside the bold and a space on each side (`**Grant —** description`).
   - **Callouts** — `<Note>`/`<Warning>`/`<Tip>` with the label and its colon bolded (`**Note:**`), and a blank line before the callout (except inside table cells).
   - **Tables** — every pipe table you touched padded so columns align. Run `python3 scripts/pad_md_tables.py <file>` to do this mechanically. Normalize any HTML table you edited (one tag per line, data rows in `<tbody>`).
   - **Links** — internal links use the file path with no `.mdx` extension and no full URL.
   - **Em-dashes** — no spaces in prose; spaces only in the bolded-term list exception.
   - **Voice and word choice** — present tense, not "will"; active voice; "after", not causal "once"; no "utilize"; spell out numbers under 10; "allowlist"/"blocklist"; "select", not "click"; Oxford comma; no exclamation points.
   - **Domo terms** — `DataSet`, `DataFlow`, `DataFusion`, `Beast Mode`, `Workbench`; `dashboard` lowercase except at the start of a sentence or with a type; never "Page" (use "dashboard"). Verify any product term against the **Domo-Specific Terms and Usage** table.
   - **Frontmatter** — if the article still has a `description` field, replace it with a single-sentence `excerpt`.
   - **Images** — block screenshots wrapped in `<Frame>` with a native `<img>` and descriptive `alt`, no inline `width`/`height`; never `<Frame>` inside a table cell. No placeholders unless the user opted in at Step 4.
   - **Icons** — confirm the Step 7 upgrade landed: current-UI glyphs use the `icon-{name}` font, `legacy-icon-{name}` only for release-notes/Workbench, brand logos use Font Awesome brands or inline `<svg fill="currentColor">`, and no legacy image-based icon remains for a glyph that exists in the font. Each icon carries `aria-hidden="true"` and is named in the prose.
4. **Revise in place.** Run `python3 scripts/pad_md_tables.py <file>` on any file whose tables you touched.

---

## Step 8.5: Align with the user on the written copy (final approval)

Now that the change has been fact-checked (Step 6) and style-edited (Step 8), show the user exactly what you wrote and get their approval on the copy — **every time, even for a one-line change**. Step 3 approved the *plan*; this confirms the *literal words*, and it comes *only after* the copy has been verified and styled — never before.

- Show the changed passage (a before/after of just what you touched is ideal for a small edit).
- Call out anything you **added** beyond the source, any place you **recast** source wording for style, and any spot where you're **missing** information the change needs.
- **This is where any wording change the user or PM wants gets made.** Fold in their edits, then re-run the fact-check (Step 6) and edit (Step 8) passes over anything you changed, so the final copy stays accurate and on-style.
- If you need missing detail, ask for it now and fold in the answer — don't invent it.

Only after the user approves the copy do you run Step 9 (verify) and Step 10 (output).

---

## Step 9: Verify

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

## Step 10: Output

Tell the user:
- What was changed, created, or deleted
- Any factual claims you flagged in Step 6 that still need the user's confirmation
- The automated legacy-icon notice from Step 7, if any icons were upgraded
- Any follow-up actions they need to handle manually (e.g., uploading new image assets, updating absolute links on the live Salesforce support site)
- Any files that were intentionally left unchanged and why
- The branch and PR base branch the change belongs on, per **Step 11**

---

## Step 11: Branch and PR routing

If the user is already on a working branch, verify it matches the convention and that its base is correct. Otherwise, tell them what to use. Do not create the branch or open the PR unless they ask.

**Routine updates:** branch `first.last/short-description`, base `main`. Publishes on the normal weekly KB schedule (PR in by Thursday for the following Monday).

**Updates documenting a change that ships with a GA release:** the article must not go live before the feature. If the change is tied to a release and you don't already know the **feature switch date** (the date customers see the feature), ask for it. Never derive it from the product branch cut date.

- Branch: `first.last/short-description-ga-MM-DD-YYYY` (zero-padded numeric date)
- Base: the GA branch for that date, named with a spelled-out month, such as `release-ga/may-20-2026`

Confirm the GA branch exists before telling the user to target it:

```bash
git branch -r | grep release-ga
```

If it doesn't exist, tell the user the Knowledge Base Administrator needs to create it. Do not fall back to `main`.

If the user is on a branch whose name contains `-ga-<date>` but whose PR bases onto `main`, flag it: the change would publish ahead of the feature.

See `CLAUDE.md` › **Contribution Workflow** for the full convention.

---

## Step 12: Offer localization

After delivering the output above, ask the user:

> "Would you like to localize this article (or your changes to it) into Spanish, French, and German? (Note: Japanese localization is handled on a separate pipeline — no action needed there.)"

- **If yes:** invoke the `localize` skill, passing the updated article's file path as the argument.
- **If no:** the skill ends here.
