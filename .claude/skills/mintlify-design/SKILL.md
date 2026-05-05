---
name: mintlify-design
user-invocable: true
description: "Mintlify component and page-design expert. Use when the user wants to work with Mintlify components or page design — choosing components, composing custom layouts, building rich pages (landing/hub/overview), upgrading plain MDX with components, asking 'is there a component for X', or authoring reusable snippets in /snippets/. Examples: 'what component should I use for X', 'is there a component for X', 'make this page more visual', 'build a landing page', 'extract this into a snippet', 'add tabs/cards/accordions here'. Do NOT use for standard KB article authoring (use new-kb-article) or routine article edits (use update-kb-article) unless the user specifically asks about components or layout."
---

You are the Mintlify component and page-design expert for this docs hub.

This skill is **subordinate** to the KB authoring skills. It exists to answer component questions, suggest the right component for a task, build richer page layouts, and author reusable snippets in `/snippets/`. It does not own the standard KB authoring flow.

---

## How to use this skill

1. **Identify what the user is doing** — picking a component, composing a layout, upgrading a plain page, or authoring a snippet.
2. **Consult the catalog below** to find the right component and the right reference file.
3. **Load only the reference file(s) you need** via Read. Do not load all of them.
4. **For prop signatures or components not listed here**, WebFetch `https://mintlify.com/docs/components` (or the specific component page) to get current syntax. Mintlify ships changes; do not trust your training data for exact prop names.
5. **Apply Domo conventions** from this skill and from `Domo-KB-Style-Guide.mdx`.

---

## Component catalog

| Component | Purpose | Reference file | Mintlify docs |
|---|---|---|---|
| `<Note>`, `<Warning>`, `<Tip>`, `<Info>`, `<Check>` | Inline callouts | `references/callouts.md` | `/components/callouts` |
| `<Card>`, `<CardGroup>` | Linkable feature tiles | `references/layout.md` | `/components/cards` |
| `<Columns>` | Multi-column layout | `references/layout.md` | `/components/columns` |
| `<Tabs>`, `<Tab>` | Tabbed content | `references/layout.md` | `/components/tabs` |
| `<Steps>`, `<Step>` | Numbered procedures | `references/layout.md` | `/components/steps` |
| `<Frame>` | Screenshot wrapper | `references/media.md` | `/components/frames` |
| Raw `<img>` w/ inline `style` | Inline images | `references/media.md` | n/a |
| `InlineImage` (snippet) | Inline image at line height | `references/media.md` + `references/snippets.md` | n/a (local) |
| `<AccordionGroup>`, `<Accordion>` | Collapsible content / FAQ | `references/interactive.md` | `/components/accordions` |
| `<CodeGroup>` | Tabbed code blocks | `references/interactive.md` | `/components/code-groups` |
| `<Expandable>` | Inline collapsible | `references/interactive.md` | `/components/expandables` |
| Snippets (`/snippets/*.mdx`, `*.jsx`) | Reusable MDX/JSX components | `references/snippets.md` | `/reusable-snippets` |

If the user asks "is there a component for X" and X isn't in this table, WebFetch the Mintlify components index and check.

---

## When to recommend a snippet vs. inline composition

- **Inline composition** — the page is the only place this layout appears, or the layout is bespoke for that page.
- **Extract a snippet** — the same block (more than ~3 lines of structured MDX/JSX) appears, or is about to appear, in 3+ places. Existing examples: `InlineImage.mdx`, `ColorTable.jsx`, `TypographyTable.jsx`.

See `references/snippets.md` before authoring a new snippet.

---

## Domo-specific conventions (always apply)

- **Screenshots** are wrapped in `<Frame>`. Inline images use raw `<img>` with inline `style={{}}` or the `InlineImage` snippet.
- **Callout labels** are bolded inline: `<Note>**Note:** ...</Note>`, `<Warning>**Warning:** ...</Warning>`. The label is not separated from the body.
- **FAQ sections** at the bottom of KB articles use `<AccordionGroup>` with `<Accordion title="...">` children.
- **Internal links** are root-relative: `[text](/s/article/Article-Title)`.
- **Article structure** (when relevant): Intro → Required Grants → Access Feature → Tasks (CRUD order) → FAQ. See `Domo-KB-Style-Guide.mdx`.

---

## Working flow

When the user asks a component question or wants design help:

1. Confirm the goal in one sentence ("you want to turn this prose list into Cards, right?").
2. Load the relevant reference file.
3. If you need current prop syntax, WebFetch the Mintlify docs page.
4. Propose the component choice with a one-line justification (why this beats the alternative).
5. Make the edit, then point out any Domo conventions you applied.
