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

### Apply the beta convention (if applicable)

Use the release-status answer from Step 2 to decide which beta treatment, if any, to apply. The full convention lives in `Domo-KB-Style-Guide.mdx` › **Beta Features** — read it before writing.

- **Entire article is beta:** add `tag: "Beta"` to the frontmatter and place the standard beta Note immediately after the frontmatter, above the Intro. Do not append `(Beta)` to the title.
- **Only certain sections are beta:** append `<Badge className="text-primary bg-primary/10 font-bold">Beta</Badge>` to each beta section's heading. Place the standard beta Note under the **first** beta section only — do not repeat it for subsequent beta sections in the same article. Do not append `(Beta)` to any heading.
- **Entire article is GA:** no beta tag, badge, or Note.

The `className` on the Badge is required and must be exactly `text-primary bg-primary/10 font-bold` — it matches the sidebar `tag` styling.

The standard beta Note must be used verbatim — do not paraphrase or change the links. Copy it from the style guide.

---

## Output

1. Write the completed MDX file to `s/article/Article-Title-Here.mdx`.
2. Tell the user the file path and suggest running `/add-to-nav` to register it in `docs.json` navigation if they want it to appear on the site.
3. Note any sections left as placeholders (screenshots, specific grant names, etc.) that the user will need to fill in.
