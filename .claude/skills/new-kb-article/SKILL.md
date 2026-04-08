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

## Step 3: Write the article

Once the Article Intake Summary and release information are confirmed, create the MDX file. Do not ask for any information already answered.

## Instructions

Create a new MDX file in `s/article/` using the filename format `Article-Title-Here.mdx` (Title Case, hyphen-separated, no special characters).

The file must follow the structure and conventions below exactly.

---

## File Structure

```mdx
---
title: "Article Title Here"
---



## Intro

Brief overview of what this article covers and why it matters to the user. One to three sentences.

---



## Required Grants

List the grants a user needs to complete the tasks in this article. If none are required, write "No special grants are required."



## Access [Feature Name]

Step-by-step instructions for navigating to the feature. Use numbered steps.

1. In the navigation header, select **[Menu Item]**.
   The [result of the action].

2. Select **[Next Element]**.



## Create [Something]

Step-by-step instructions. Follow the CRUD order (Create, Review, Update, Delete) — only include sections that apply.

1. First step. Include orienting language if needed.
   
   <Frame>![Alt text describing the screenshot](/images/kb/image-name.png)</Frame>

2. Second step. Always an action.

3. (Optional) Optional step.

4. (Conditional) Conditional step.



## FAQ


<AccordionGroup>

<Accordion title="Frequently asked question?">
Frequently asked answer.
</Accordion>

<Accordion title="Frequently asked question?">
Frequently asked answer.
</Accordion>

</AccordionGroup>
```

---

## Style Rules to Apply

**Article structure**
- Do not include a table of contents — written or linked — at the top of the article. Tables of contents are generated automatically from the article's headings when the page renders on the Knowledge Base site.

**Voice and tense**
- Write in present tense: "This opens the panel" not "This will open the panel."
- Use active voice. Avoid passive voice unless who performs the action does not matter.
- Use "select" not "click," except when specifying right-click, left-click, or double-click.
- Contractions are acceptable unless you need to emphasize "not."
- Spell out numbers less than 10.
- Never use "utilize" — use "use."
- No exclamation points.
- Use the Oxford comma.
- Eliminate unnecessary words ("will," "you are able to," "that").
- Avoid Latin expressions (i.e., e.g., etc.) — use "such as," "as in," or a list.
- Use "allowlist" and "blocklist," never "whitelist" or "blacklist."
- Write all headings (article titles, section headings, step headings) in the imperative mood — never the gerund. **Correct:** "Connect Data to Domo" **Incorrect:** "Connecting Data to Domo"
- When describing a sequence of actions in a step, do not use "once" to denote a causal or dependent relationship — use "after" instead. **Correct:** "After you save the DataSet, select **Done**." **Incorrect:** "Once you save the DataSet, select **Done**."
- Do not place spaces on either side of an em-dash. **Correct:** "AI tools—such as Claude—secure access" **Incorrect:** "AI tools — such as Claude — secure access"

**Text emphasis**
- **Bold** static UI elements (fields, menus, buttons, icons). For a series: **Admin** > **Security** > **Whitelist** (do not bold the >).
- *Italics* for variables the user fills in with their own data.
- "Quotation marks" for on-screen text not used as an interface element, and for DataSet column names and ETL actions.
- `Code style` for code snippets.

**Domo-specific terminology (capitalize exactly as shown)**
- DataSet, DataFlow, DataFusion, Magic ETL, Beast Mode, AppDB
- Admin Settings (not bolded, not a UI element)
- Data Center, Alerts Center, Knowledge Base
- Dashboard (not Page), Dashboard Filters (not Page Filters)
- Grants (lowercase unless naming a specific grant, e.g., Manage All Users grant)
- "select" not "click"; "field" not "box"; "pill" for rounded non-button elements
- Do not use: Dojo (use Community Forums), KPI card (use Visualization Card), image card (use Doc Card), Domo story (use Dashboard), Drilldown (use Drill Path or "drill into"), Page/Page Filters

**Links**
- Internal article links: `[link text](/s/article/Article-Title)`
- Section links: `[link text](/s/article/Article-Title#section-heading)`
- External links: `[link text](https://full-url.com)`

**Images**
- Auto-sized screenshot wrapped in Frame: `<Frame>![alt text](/images/kb/image-name.png)</Frame>`
- Specifically sized: `<Frame><img alt="alt text" src="/images/kb/image-name.png" style={{width: 500, height: 500}}/></Frame>`
- Inline icon: `<img alt="alt text" src="/images/kb/icon-name.png" style={{width: 20, height: 20, display: 'inline', verticalAlign: 'start', margin: '0'}}/>`
- Screenshots should be taken in Modocorp or a demo instance, not the company instance.

**Callout components** (always bold the label)
- `<Note>**Note:** Text here.</Note>`
- `<Warning>**Important:** Text here.</Warning>`
- `<Tip>**Tip:** Text here.</Tip>`

**Beta features**
- Do not put "(Beta)" in the article title. A single article can cover a mix of GA and beta functionality, so beta status is marked at the section level, not the title level.
- Immediately below the heading for any beta section or feature, add:
  ```mdx
  <Note>
    **Note:** This feature is in beta. Contact your Domo account team to join.
  </Note>
  ```
- If the entire article covers only beta functionality, place this note at the top of the Intro section.

**FAQ**
- Place at the bottom of the article, above Troubleshooting if it exists.
- Always use `<AccordionGroup>` containing `<Accordion title="Question?">` items.

---

## Output

1. Write the completed MDX file to `s/article/Article-Title-Here.mdx`.
2. Tell the user the file path and suggest adding it to `docs.json` navigation if they want it to appear on the site.
3. Note any sections left as placeholders (screenshots, specific grant names, etc.) that the user will need to fill in.
