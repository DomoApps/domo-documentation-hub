---
name: migrate-html
user-invocable: true
description: "migrate an HTML article to a repo-ready MDX KB article: convert HTML to Markdown with pandoc, apply Domo style rules, save to s/article/, and add to docs.json navigation"
argument-hint: "optional: paste HTML inline, or leave blank to be prompted"
---

Migrate an HTML article into a repo-ready MDX file in `s/article/` and register it in `docs.json` navigation.

The user has provided: $ARGUMENTS

---

## Step 1: Gather information

Ask the user for the following if not already provided. Collect all three before proceeding — do not start converting until you have them.

1. **HTML source** — the raw HTML to migrate. The user will paste it directly into the chat.

2. **Target filename** — the MDX filename to use (e.g., `000006094`). This becomes `s/article/<filename>.mdx`. If the user doesn't have a number, ask them to check with the KB admin or look at the highest existing number in `s/article/` as a reference.

3. **Navigation placement** — where the article belongs in `docs.json`. Ask:
   - Is this a connector article, a general KB article, or something else?
   - For connector articles: the `add-to-nav` skill handles alphabetical placement automatically — no extra input needed.
   - For other articles: ask which tab, group, and subgroup it belongs in, and where within that group (beginning, end, or after a specific neighboring article).

---

## Step 2: Convert HTML to Markdown with pandoc

Save the HTML to a temp file, then run pandoc:

```bash
cat > /tmp/migrate-article.html << 'HTMLEOF'
<paste HTML here>
HTMLEOF
pandoc /tmp/migrate-article.html -f html -t markdown --wrap=none -o /tmp/migrate-article.md && cat /tmp/migrate-article.md
```

Inspect the output. Pandoc will:
- Convert headings, bold, italic, lists, links, and tables to Markdown
- Preserve inline HTML it can't express in Markdown
- Leave CSS class spans like `[text]{.s1}` — these must be stripped in Step 3

---

## Step 3: Read the style guide and template

Read both files in parallel before writing any MDX:

- `Domo-KB-Style-Guide.mdx`
- `New-Article-Template.mdx`

Key rules to apply (see those files for full detail):

### Frontmatter
Every article needs at minimum:
```mdx
---
title: "Article Title"
excerpt: "Single sentence summarizing what the article covers."
---
```
Do not use `description` — it renders on the published page and duplicates the Intro.

### Article structure
Intro → (optional) Required Grants → (optional) Prerequisites → task sections → (optional) FAQ

A `---` horizontal rule must follow the **Intro** section.

### Headings
- Structural labels (`Intro`, `Prerequisites`, `FAQ`, etc.) are exempt from imperative mood.
- All other headings must use imperative mood: "Connect to Your Account", not "Connecting to Your Account".
- The frontmatter `title` renders as H1. All top-level sections are H2; subsections H3+.

### Links
- Internal links: root-relative path, no `.mdx` extension — `[Title](/s/article/360042926274)`
- Strip `domo-support.domo.com` prefixes from internal links: `https://domo-support.domo.com/s/article/360042926274?language=en_US` → `/s/article/360042926274`
- External links stay as-is; strip `{target="_blank" rel="noopener noreferrer"}` attributes pandoc may leave behind

### Strip pandoc artifacts
Remove these from the pandoc output:
- `[text]{.s1}` → `text` (CSS class spans — just unwrap the text)
- `{target="_blank" rel="noopener noreferrer"}` after links
- Inline `style=` attributes on elements
- Blank `&nbsp;` paragraphs

### Tables
- Use pipe tables. Pad cells with spaces so column pipes align vertically across all rows.
- Use `<br/>` to separate multiple lines of plain text within a cell. Do not use `<br/>` between callout components.
- **Nested tables:** write the inner table as inline HTML in the outer pipe table cell. Keep it on one line:

```
| Outer Col 1 | Outer Col 2                                                                                                                      |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Row 1       | <table><thead><tr><th>Inner Col 1</th><th>Inner Col 2</th></tr></thead><tbody><tr><td>Value</td><td>Value</td></tr></tbody></table> |
```

- When a cell contains both plain text and a nested table, separate them with `<br/>`.
- Avoid `<Frame>` inside table cells — use native `<img>` instead.

### Callouts
```mdx
<Note>**Note:** Text here.</Note>
<Warning>**Important:** Text here.</Warning>
<Tip>**Tip:** Text here.</Tip>
```
Always bold the label. Leave a blank line before a callout (except inside table cells).

---

## Step 4: Write the MDX file

Save the formatted content to `s/article/<filename>.mdx`. Do not add comments, explanatory headers, or TODO markers unless the style guide explicitly calls for them (e.g., screenshot TODOs per the screenshot policy).

---

## Step 5: Add to navigation

Invoke the `add-to-nav` skill:

```
/add-to-nav s/article/<filename> — <description of where it belongs>
```

For connector articles, describe it as a connector article and name the service — the skill will find the correct alphabetical slot within the right `Data Providers` group automatically (it reads neighboring article titles to confirm exact placement).

---

## Step 6: Verify JSON

After `add-to-nav` makes its edit:

```bash
node -e "JSON.parse(require('fs').readFileSync('docs.json', 'utf8')); console.log('docs.json is valid JSON');"
```

If this fails, show the error and fix it before finishing.

---

## Output

Tell the user:
- The path of the new article (`s/article/<filename>.mdx`)
- Where it was inserted in `docs.json` (group name and neighboring entries)
- That the branch is ready to commit and preview with `mintlify dev`
