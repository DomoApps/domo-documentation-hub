# Interactive components

Collapsibles and tabbed code. Used to compress dense reference content without losing it.

## `<AccordionGroup>` and `<Accordion>` — FAQs and progressive detail

The standard for FAQ sections at the bottom of KB articles, and for "advanced details" that most readers should skip.

```mdx
<AccordionGroup>
  <Accordion title="Why isn't my dataset refreshing?">
    Common causes: stale credentials, source schema change, or a paused schedule.
  </Accordion>
  <Accordion title="Can I refresh more than once an hour?">
    Yes — see the **Schedule** tab on the dataset detail page.
  </Accordion>
</AccordionGroup>
```

**Domo convention:** every KB article's FAQ section uses `<AccordionGroup>`. See `Domo-KB-Style-Guide.mdx`.

**When to use:** FAQs, troubleshooting steps, optional/advanced details, long explanations that interrupt the main flow.
**Avoid:** for content the reader *must* see — collapsed-by-default content gets skipped.

## `<CodeGroup>` — tabbed code blocks

Multiple code samples that show the same operation in different languages or clients.

````mdx
<CodeGroup>
```bash cURL
curl -X GET https://api.domo.com/v1/datasets/{id} \
  -H "Authorization: Bearer $TOKEN"
```

```python Python
import requests
resp = requests.get(f"https://api.domo.com/v1/datasets/{id}",
                    headers={"Authorization": f"Bearer {token}"})
```

```javascript JavaScript
const resp = await fetch(`https://api.domo.com/v1/datasets/${id}`, {
  headers: { Authorization: `Bearer ${token}` }
});
```
</CodeGroup>
````

The label after the language (`bash cURL`, `python Python`) becomes the tab name.

**When to use:** API examples in multiple languages, CLI vs. UI, before/after code.

## `<Expandable>` — inline collapsible

Less common than `<Accordion>`. Used for inline detail (e.g., expanding a single property's nested fields in API reference).

```mdx
<Expandable title="properties">
  - `id` — unique identifier
  - `name` — display name
</Expandable>
```

**When to use:** API reference tables where one row has nested detail.
**Avoid:** as a substitute for `<Accordion>` — accordions are for content sections, expandables for inline detail.

## Mintlify reference

- `https://mintlify.com/docs/components/accordions`
- `https://mintlify.com/docs/components/code-groups`
- `https://mintlify.com/docs/components/expandables`
