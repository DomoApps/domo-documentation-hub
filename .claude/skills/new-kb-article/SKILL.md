---
name: new-kb-article
user-invocable: true
description: "write a new KB article, generate knowledge base article, draft a KB doc, create a new article, write documentation, create MDX article"
argument-hint: "article title or topic, or paste any source material"
---

Generate a new Domo Knowledge Base article as an MDX file.

The user will provide: $ARGUMENTS

---

## Step 1: Run the kb-intake skill

Before writing anything, invoke the `kb-intake` skill, passing `$ARGUMENTS` directly as the input. Let the Socratic intake conversation run to completion, ending with the Article Intake Summary.

Use the original source material and the Article Intake Summary as the authoritative source of truth for everything that follows — it defines the title, persona, structure, scope, and key details of the article. If there are conflicts between the original source material and the Article Intake Summary, the Article Intake Summary takes precedence. Be sure to call out any discrepancies and be clear to the user about which information is taken as the truth.

---

## Step 2: Gather release information

After the Article Intake Summary is confirmed, ask the following two questions before writing:

1. **Release status:** What is the release status of the feature(s) covered in this article? For each distinct feature or section, is it GA (generally available) or beta? If mixed, which parts are beta?
2. **Planned branch cut date:** What is the planned **branch cut date** for this release? This is the internal branch name (NOT the feature release date).

---

## Step 3: Read the style guide and article template

Before writing, read both of these files:

1. **`Domo-KB-Style-Guide.mdx`** — the authoritative style guide. Apply every rule in this file when writing the article.
2. **`New-Article-Template.mdx`** — the canonical file structure and encoding conventions (frontmatter, section order, image syntax, callout components, code blocks, tables, etc.). Use this as the structural template for the new article.

---

## Step 4: Write the article

Once the Article Intake Summary, release information, style guide, and template are all loaded, create the MDX file. Do not ask for any information already answered.

Create a new MDX file in `s/article/` using the filename format `Article-Title-Here.mdx` (Title Case, hyphen-separated, no special characters).

Follow the structure from `New-Article-Template.mdx` and apply all style rules from `Domo-KB-Style-Guide.mdx` exactly.

### Use canonical grant wording in Required Grants

When writing the **Required Grants** section, do not invent grant descriptions. Most grants are already described in the standard format elsewhere in the KB — search for and reuse the existing wording so the grant reads consistently across articles:

```bash
grep -rn "Grant Name —" s/article/
```

Reuse the existing description verbatim (adjusting only to fit the em-dash format). If no article describes the grant, write a concise one-sentence description and flag it to the user as newly authored. See `Domo-KB-Style-Guide.mdx` › **Required Grants** › _Use canonical grant wording_.

### Apply the beta convention (if applicable)

Use the release-status answer from Step 2 to decide which beta treatment, if any, to apply. The full convention lives in `Domo-KB-Style-Guide.mdx` › **Beta Features** — read it before writing.

- **Entire article is beta:** add `tag: "Beta"` to the frontmatter and place the standard beta Note immediately after the frontmatter, above the Intro. Do not append `(Beta)` to the title.
- **Only certain sections are beta:** append `<Badge className="text-primary bg-primary/10 font-bold">Beta</Badge>` to each beta section's heading. Place the standard beta Note under the **first** beta section only — do not repeat it for subsequent beta sections in the same article. Do not append `(Beta)` to any heading.
- **Entire article is GA:** no beta tag, badge, or Note.

The `className` on the Badge is required and must be exactly `text-primary bg-primary/10 font-bold` — it matches the sidebar `tag` styling.

The standard beta Note must be used verbatim — do not paraphrase or change the links. Copy it from the style guide.

---

## Step 5: Style-guide revision pass

Drafting always introduces style drift. Before finalizing, do an explicit pass against the style guide and revise the article in place. **Do not skip this even if the draft looks right** — the most common misses (intro framing, imperative headings, unpadded tables, lowercase Domo terms, future tense) are easy to introduce and easy to miss without a deliberate re-read.

1. **Re-read `Domo-KB-Style-Guide.mdx` now, in full** — not from memory. You will have drifted from at least one rule while drafting.
2. **Audit the article against this checklist** and fix every violation in both the EN file and the JA sibling, if you authored one:
   - **Frontmatter** — `title` plus a single-sentence `excerpt`; never a `description` field.
   - **Intro** — opens with "This article explains…" or "This article covers…", states only what the article covers (not why it matters), and is immediately followed by a `---` horizontal rule.
   - **Headings** — imperative mood at every level (H2–H4); the structural labels (Intro, Required Grants, Prerequisites, FAQ, Troubleshoot, Related Articles) are exempt. Top-level sections are H2, subsections H3+.
   - **Required Grants** — exact format and canonical grant wording, with the em-dash inside the bold and a space on each side (`**Grant —** description`).
   - **Callouts** — `<Note>`/`<Warning>`/`<Tip>` with the label and its colon bolded (`**Note:**`), and a blank line before the callout (except inside table cells).
   - **Tables** — every pipe table padded so columns align. Run `python3 scripts/pad_md_tables.py <file>` to do this mechanically. Normalize any HTML tables (one tag per line, data rows in `<tbody>`).
   - **Links** — internal links use the file path with no `.mdx` extension and no full URL.
   - **Em-dashes** — no spaces in prose (`tools—such as`); spaces only in the bolded-term list exception.
   - **Voice and word choice** — present tense, not "will"; active voice; "after", not causal "once"; no "utilize"; spell out numbers under 10; "allowlist"/"blocklist"; "select", not "click"; Oxford comma; no exclamation points.
   - **Domo terms** — `DataSet`, `DataFlow`, `DataFusion`, `Beast Mode`, `Workbench`; `dashboard` lowercase except at the start of a sentence or with a type; never "Page" (use "dashboard"). Verify any product term against the **Domo-Specific Terms and Usage** table.
   - **Beta** — correct convention applied (frontmatter `tag` + verbatim Note for a whole-article beta; Badge + single verbatim Note for section-level).
   - **Images** — block screenshots wrapped in `<Frame>` with a native `<img>` and descriptive `alt`, no inline `width`/`height`; inline glyphs use the icon font or the inline `<img>` style; never `<Frame>` inside a table cell.
3. **Revise the article in place** to resolve every issue found, then re-run the table normalizer if you changed any tables.

---

## Step 6: Add the new article to navigation

A new article file does not appear on the site until it is registered in `docs.json`. As the final step, invoke the `add-to-nav` skill to place the article in the navigation — do not edit `docs.json` by hand:

- **Page path:** `s/article/Article-Title-Here`
- **Operation:** Insert
- **Target:** the group or subgroup that best fits the article's topic. If you are unsure where it belongs, let `add-to-nav` surface the placement options and use AskUserQuestion to confirm the location with the user.

After `add-to-nav` edits `docs.json`, confirm it is still valid JSON:

```bash
python3 -c "import json; json.load(open('docs.json')); print('docs.json is valid JSON')"
```

---

## Output

1. Tell the user the file path of the new MDX article (`s/article/Article-Title-Here.mdx`).
2. Confirm the article was added to `docs.json` navigation and state where it was placed.
3. Note any sections left as placeholders (screenshots, specific grant names, etc.) that the user will need to fill in.
