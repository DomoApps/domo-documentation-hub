# Layout components

For composing pages: cards, columns, tabs, steps. Use these when prose alone won't carry the structure — landing pages, hub pages, multi-path procedures, comparison content.

## `<Card>` and `<CardGroup>`

Linkable feature tiles. The dominant pattern for landing/hub pages.

```mdx
<CardGroup cols={2}>
  <Card title="Get started" icon="rocket" href="/portal/Getting-Started">
    Set up your first dataset in under 10 minutes.
  </Card>
  <Card title="Connect data" icon="plug" href="/portal/Connectors">
    Pull data from 1,000+ sources.
  </Card>
</CardGroup>
```

- `cols` controls column count; 2 is most common for hub pages, 3 for dense indexes.
- `icon` accepts Font Awesome / Lucide names — see Mintlify docs for current icon library.
- `href` makes the whole card clickable. Use root-relative paths (`/s/article/...`).

**When to use:** index/hub pages, "next steps" sections at the bottom of overviews, feature catalogs.
**Avoid:** for pure body content. Cards are navigation furniture, not prose.

## `<Columns>`

Multi-column body content. Less link-flavored than `<CardGroup>`.

```mdx
<Columns cols={2}>
  <div>**Before:** Manual export each Monday.</div>
  <div>**After:** Scheduled refresh, no human in the loop.</div>
</Columns>
```

**When to use:** before/after, comparison, side-by-side image + text.

## `<Tabs>` and `<Tab>`

Tabbed content for parallel paths through the same task.

```mdx
<Tabs>
  <Tab title="macOS">
    Run `brew install domo-cli`.
  </Tab>
  <Tab title="Windows">
    Download the installer from the releases page.
  </Tab>
</Tabs>
```

**When to use:** OS variants, role-specific instructions (Admin vs. Editor), API client variants.
**Avoid:** when the alternatives have different *outcomes*, not just different *paths* — readers miss content hidden in unselected tabs. Use separate sections instead.

## `<Steps>` and `<Step>`

Numbered procedures rendered with persistent step numbers. Better than markdown ordered lists for multi-paragraph steps.

```mdx
<Steps>
  <Step title="Open the admin console">
    Navigate to **Admin → Security**.
  </Step>
  <Step title="Add the user">
    Click **Invite** and enter the email address.
  </Step>
</Steps>
```

**When to use:** procedures with 3+ steps where each step has more than one sentence or contains a screenshot.
**Avoid:** for short 2-step lists — markdown `1.` is fine.

## Mintlify reference

WebFetch these for current prop signatures:
- `https://mintlify.com/docs/components/cards`
- `https://mintlify.com/docs/components/columns`
- `https://mintlify.com/docs/components/tabs`
- `https://mintlify.com/docs/components/steps`
