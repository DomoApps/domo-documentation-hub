---
name: csv-to-mdx
user-invocable: true
description: "review converted MDX article, audit programmatic conversion output, check batch CSV to MDX output, validate Salesforce article conversion, post-conversion review"
argument-hint: "path to an MDX file or article title to review"
---

Review and audit an MDX article produced by the Salesforce-to-Domo programmatic conversion pipeline (`scripts/html_to_mdx.py`). Identify anything the script cannot fix automatically and provide a corrected version.

The user will provide: $ARGUMENTS

---

## Pipeline Overview

The full programmatic conversion runs in this order:

1. **CSV extraction** — `update_kb_articles.py` reads `ARTICLE_BODY__C` (HTML), `TITLE`, `URLNAME`, `LANGUAGE`, and `PUBLISHSTATUS` from the Salesforce CSV export.
2. **Pre-processing** — `_strip_toc_elements()` removes ToC jump-link lists, "Back/Return to top" navigation, and orphaned `---` horizontal-rule artifacts before the HTML is converted.
3. **markdownify conversion** — `_DomoMDXConverter` converts HTML to Markdown with image placeholders, rewriting internal Salesforce URLs to language-appropriate repo-relative paths.
4. **Image restoration** — `_restore_images()` replaces placeholders with either `<Frame>` screenshot blocks or inline `<img>` icon syntax, based on image dimensions and HTML context.
5. **Callout conversion** — `_convert_callouts()` converts `**Note:**`, `**Important:**`, `**Warning:**`, `**Tip:**` paragraphs to `<Note>`, `<Warning>`, `<Tip>` components.
6. **FAQ conversion** — `_convert_faq()` converts FAQ sections to `<AccordionGroup>`/`<Accordion>` components.
7. **Artifact cleanup** — strips `— | —` Salesforce divider artifacts, collapses consecutive `---` lines, removes leading `---` artifacts, and normalizes excess blank lines.
8. **Frontmatter** — wraps the result in a `---\ntitle: "..."\n---` YAML block.

---

## Post-Run: Add New Articles to Navigation

After the script runs, any net-new English articles must be added to `docs.json` navigation using the `/add-to-nav` skill. The script prints a list of these articles at the end of the run under "New English articles requiring /add-to-nav."

Run `/add-to-nav s/article/<article-id>` for each one. Localized (Japanese, German, French, Spanish) articles do not need separate navigation entries.

---

## Formatting Rules (from New-Article-Template.mdx)

Apply these exact MDX patterns wherever the corresponding element appears.

**Screenshots**
```mdx
<Frame>![alt text describing the screenshot](/images/kb/image-name.png)</Frame>
```
- Wrapping in `<Frame>` is required — it auto-sizes the image to the content column width.
- Alt text must describe what the screenshot shows, not just "screenshot."

**Inline icons**
```mdx
<img alt="alt text" src="/images/kb/icon-name.png" style={{width: 20, height: 20, display: 'inline', verticalAlign: 'start', margin: '0'}}/>
```
- Use for small icons embedded mid-sentence (≤ 40px in either dimension).
- Recommended sizes: 20×20 (matches display text), 30×30 (most inline icons), 40×40 (header-level icons).

**Callout components** (always bold the label inside; always a blank line before the callout in body text)
```mdx
<Note>**Note:** Text here.</Note>
<Warning>**Important:** Text here.</Warning>
<Tip>**Tip:** Text here.</Tip>
```

**Description lists**
```mdx
- **Term —** description of term
- **Another Term —** description of another term
```
- Em-dash is inside the bold formatting, with a space on either side of it (exception to the no-spaces em-dash rule).

**Bullet lists with sub-items**
```mdx
- First item
- Second item
  - Sub-item under Second item
    - Sub-sub item
```

**Tabbed code blocks** (for showing the same code in multiple languages)
```mdx
<CodeGroup>

```javascript JavaScript
// Your JavaScript code here
```

```python Python
# Your Python code here
```

</CodeGroup>
```

**Tables** — pipe tables must be padded with spaces so columns align vertically:
```mdx
| First Column | Second Column |
| ------------ | ------------- |
| Row text 1   | Row text 1    |
| Row text 2   | Row text 2    |
```

Use `<br/>` to separate multiple lines of plain text within a single table cell. Do not use `<br/>` between multiple callout elements in a cell — they render on their own lines automatically. When a callout follows plain text in a cell, `<br/>` before the callout is not needed:
```mdx
| Column       | Column                                                                 |
| ------------ | ---------------------------------------------------------------------- |
| Multi-line   | First line.<br/>Second line.                                           |
| With note    | Cell content. <Note>**Note:** Note text.</Note>                        |
| Two callouts | <Note>**Note:** First.</Note><Warning>**Warning:** Second.</Warning>   |
```

**Nested tables** — write the inner table as HTML embedded in the outer table cell:
```mdx
| Outer Col 1 | Outer Col 2                                                                                                                      |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Row 1       | <table><thead><tr><th>Inner Col 1</th><th>Inner Col 2</th></tr></thead><tbody><tr><td>Value</td><td>Value</td></tr></tbody></table> |
```

**FAQ section**
```mdx
## FAQ

<AccordionGroup>

<Accordion title="Question text here?">
Answer text here.
</Accordion>

</AccordionGroup>
```
- FAQ goes at the bottom of the article, above Troubleshoot or Related Articles if those sections exist.

**Frontmatter**
```mdx
---
title: "Article Title Here"
---
```

---

## Article Structure (from Domo-KB-Style-Guide.mdx)

The required order of sections:
1. **Intro** — followed immediately by a `---` horizontal rule
2. **Required Grants**
3. *(Optional)* **Prerequisites**
4. **Access [Feature Name]** (can swap with Required Grants if the grant is needed to see the access path)
5. **Task headings** in CRUD order — Create, Review, Update, Delete (include only those that apply)
6. *(Optional)* **FAQ**
7. *(Optional)* **Troubleshoot**
8. *(Optional)* **Related Articles**

The structural labels Intro, Required Grants, Prerequisites, FAQ, Troubleshoot, and Related Articles are exempt from the imperative-mood rule.

**Intro section format:** Keep it to one sentence in most cases. Use "This article explains how to…" or "This article covers…" followed by 2–3 concrete actions or skills the reader gains, using the same terminology as the article body. Do not explain why the skills matter.

**Correct:** "This article explains how to connect a DataSet to a card, schedule a DataFlow refresh, and configure row-level security."

**Heading Hierarchy:** The frontmatter `title` field renders as H1. Top-level sections (Intro, Required Grants, tasks, FAQ, etc.) are H2. Subsections are H3, H4, and so on. The ToC renders through H4 — avoid going deeper than three levels.

---

## Style Rules

### A — Enforced programmatically by `html_to_mdx.py`

These are already handled and should be correct in any script output:

| Rule | What the script does |
|------|---------------------|
| No table of contents | `_strip_toc_elements()` removes jump-link `<ul>`/`<ol>` lists before conversion |
| No "Back/Return to top" links | `_strip_toc_elements()` removes these anchor links and their parent paragraphs |
| No `— \| —` divider artifacts | Stripped with `re.sub(r"\n*—\s*\|\s*—\n*", "\n\n", md)` |
| No consecutive `---` artifacts | Collapsed to a single `---`; leading `---` before any content removed |
| Callout blocks use MDX components | `_convert_callouts()` converts bold-label paragraphs |
| FAQs use AccordionGroup | `_convert_faq()` converts FAQ sections |
| Internal links are repo-relative | `convert_a()` rewrites `domo-support.domo.com/s/article/…` links |
| Screenshots wrapped in `<Frame>` | `_restore_images()` wraps large/standalone images |
| Inline icons use `<img style>` | `_restore_images()` uses dimension + context signals |
| YAML frontmatter added | `html_to_mdx()` wraps output in `---\ntitle: "..."\n---` |

### B — Requiring human review after conversion

The script cannot reliably fix these. Review every converted article for:

**Article structure**
- [ ] Intro → `---` → Required Grants → (Optional: Prerequisites) → Access Feature → CRUD tasks → (Optional: FAQ) → (Optional: Troubleshoot) → (Optional: Related Articles)
- [ ] Intro section uses "This article explains how to…" or "This article covers…" format, one sentence, 2–3 concrete actions
- [ ] Any `<!-- TODO: embed image → ... -->` comments must be resolved manually
- [ ] FAQ items that didn't match the bold-Q/paragraph-A or numbered-list patterns are left verbatim and need manual `<AccordionGroup>` conversion
- [ ] New English articles need `/add-to-nav` run to add them to `docs.json`

**Image paths — case collisions**

Salesforce image IDs are case-sensitive (`…vPFA.png` and `…vPFa.png` are different images in Salesforce), but macOS APFS and Windows NTFS are case-insensitive by default. Two filenames that differ only by case collapse to one file on disk for most contributors, silently breaking articles. CI now blocks merging case-colliding paths (see `.github/workflows/case-collision-check.yml`).

- [ ] For every new image the conversion writes under `images/kb/`, check whether its lowercase form matches an already-tracked path (`git ls-files images/kb/ | tr A-Z a-z | sort | uniq -d` against the new basenames). If it collides, rename the new file by inserting `-2` before the extension (e.g., `…vPFa.png` → `…vPFa-2.png`) and update every reference the script wrote.

**Inline icons (image → font)**

The converter emits image-based inline icons (`<img src="/images/kb/...">`). Both Domo icon fonts cover the full glyph set, so any inline icon that depicts a UI element should be migrated to the font convention. Pick the font that matches the surface the article describes — see `Domo-KB-Style-Guide.mdx` › **Icons** for full guidance.

- [ ] Inline `<img>` icons depicting **current Domo product UI** → migrate to `<i className="icon-{name}" aria-hidden="true" />` (phosphor). If the original image showed a pre-refresh icon, this is also a stale-screenshot upgrade — go to phosphor anyway.
- [ ] Inline `<img>` icons depicting **legacy surfaces** (release notes describing pre-refresh UI, Workbench, other legacy apps) → migrate to `<i className="legacy-icon-{name}" aria-hidden="true" />`.
- [ ] Inline `<img>` icons that are **third-party brand logos** (AWS, OpenAI, Anthropic, GitHub, …) → these aren't in the Domo icon font, and a monochrome logo image breaks in dark mode. Migrate to a coded icon: `<Icon icon="{slug}" iconType="brands" aria-hidden="true" />` (Font Awesome brands), or an inline `<svg fill="currentColor">` (e.g. a [Simple Icons](https://simpleicons.org) path) when FA's free set lacks the brand. See `Domo-KB-Style-Guide.mdx` › **Brand and Third-Party Logos**.
- [ ] After migration, confirm the surrounding prose names the icon (e.g. "click the line chart icon \<icon\>"). If it doesn't, rewrite the prose inline rather than reaching for `aria-label`.
- [ ] Remove any leftover `import { InlineImage } from "/snippets/InlineImage.mdx";` line — the snippet is no longer in use anywhere in the repo. Inline images should always be a native `<img>` with an inline `style` block (see `Domo-KB-Style-Guide.mdx` › **Inline images**).

**Headings**
- [ ] All headings use the **imperative mood** — never the gerund. **Correct:** "Connect a DataSet" **Incorrect:** "Connecting a DataSet"
- [ ] Top-level sections are H2 (`##`), subsections are H3 (`###`) and deeper — never jump levels
- [ ] The structural labels (Intro, Required Grants, etc.) are exempt from the imperative-mood rule

**Voice and tense**
- [ ] Present tense throughout ("This opens the panel" not "This will open the panel")
- [ ] Active voice — no passive voice unless the actor is genuinely unknown
- [ ] "select" not "click" (except right-click, left-click, double-click)
- [ ] No exclamation points
- [ ] Numbers below 10 are spelled out

**Word choices to fix manually**
- [ ] `whitelist` → `allowlist`, `blacklist` → `blocklist`
- [ ] `utilize` / `utilizes` / `utilizing` → `use`
- [ ] `once` used as a causal connector → `after` ("After you save" not "Once you save")
- [ ] No Latin abbreviations (`i.e.`, `e.g.`, `etc.`) — use "such as," "as in," or a list
- [ ] No "verbiage" — use "words"
- [ ] No "Dojo" — use "Community Forums"
- [ ] No "KPI card" — use "Visualization Card"
- [ ] No "image card" — use "Doc Card"
- [ ] No "Page" or "Page Filters" — use "Dashboard" / "Dashboard Filters"
- [ ] No "Domo story/stories" — use "Dashboard/Dashboards"
- [ ] No "Drilldown" — use "Drill Path" or "drill into"
- [ ] No "Slicers" — use "Quick Filters"

**Beta markers**

Salesforce-era articles use a variety of legacy beta indicators. Convert any you find to the current convention defined in `Domo-KB-Style-Guide.mdx` › **Beta Features**:

- [ ] `(Beta)` or `(BETA)` in a `title:` frontmatter value → remove the parenthetical and add `tag: "Beta"` to the frontmatter; insert the standard beta Note above the Intro
- [ ] `(Beta)` or `(BETA)` appended to a heading → remove the parenthetical and append `<Badge className="text-primary bg-primary/10 font-bold">Beta</Badge>` to the heading
- [ ] Ad-hoc beta notes (e.g., "This feature is in beta. Contact your account team…") → replace with the standard beta Note from the style guide
- [ ] References to `betafeedback@domo.com` or `betadmin@domo.com` → replace with `beta.admin@domo.com` (the standard Note already contains the right address)
- [ ] If multiple sections in one article are beta, keep only one standard Note in the article (under the first beta section) — do not repeat it under each
- [ ] If the converted article links to other articles whose link text contains `(Beta)`/`(BETA)`, drop the parenthetical from the link text

**Punctuation and formatting**
- [ ] Em-dashes in body text: no spaces — `tools—such as these—work`
- [ ] Em-dashes in description lists: spaces inside the bold — `**Term —** description`
- [ ] Oxford comma in lists of three or more
- [ ] Bold static UI elements (`**Save**`, `**Admin** > **Security**`) — do not bold the `>`
- [ ] Table columns padded with spaces so pipes align vertically

**Domo terminology (capitalize exactly)**

| Correct | Never use |
|---------|-----------|
| DataSet | Dataset, dataset |
| DataFlow | Dataflow |
| DataFusion | Data Fusion |
| Magic ETL | magic ETL |
| Beast Mode | Beastmode, beast mode |
| AppDB | App DB, appDB |
| Dashboard | Page, Domo story |
| Dashboard Filters | Page Filters |
| Data Center | data center |
| Alerts Center | alerts center |
| Drill Path / drill into | Drilldown |
| Visualization Card | KPI card |
| Doc Card | image card |
| Community Forums | Dojo |
| Quick Filters | Slicers |
| Scheduled Reports | scheduled reports |
| Pro-code Editor | Procode Editor |

---

## Review Procedure

When invoked, do the following:

1. **Read the file** at the path provided in `$ARGUMENTS`. If a title is given instead, find the file with `grep -r "title:.*<title>" s/article/`.
2. **Scan for human-review items** from Section B above.
3. **Check image placeholders** — search for `<!-- TODO: embed image` comments and flag them.
4. **Check image-path case collisions** — for any image path the article references under `images/kb/`, run `git ls-files images/kb/ | grep -i "<basename>"` to confirm no case-sibling exists. If one does, rename the new file with a `-2` suffix and update the article's references.
5. **Check for leftover Salesforce artifacts** — any remaining `— | —`, bare Salesforce URLs, or raw HTML tags that markdownify didn't convert.
6. **Apply fixes** to items from Section B that are clearly wrong (e.g., incorrect Domo terminology, `whitelist` → `allowlist`).
7. **List items requiring editorial judgment** (e.g., gerund headings, passive-voice sentences) with line numbers so the user can decide.
8. **Write the corrected file** and report what was changed vs. what needs the user's review.
