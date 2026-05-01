# Callouts

Inline emphasis blocks. Used to highlight prerequisites, warnings, tips, or contextual notes inside running prose.

## Components

| Component | Use for |
|---|---|
| `<Note>` | Side information that's helpful but not critical. Most common. |
| `<Warning>` | Destructive actions, irreversible changes, security implications, breaking-change behavior. |
| `<Tip>` | Optional shortcut, best practice, or efficiency hint. |
| `<Info>` | Neutral context (less common in this repo than `<Note>`). |
| `<Check>` | Success/confirmation state. Rare. |

## Domo convention — bold inline label

Always lead the body with a bolded label that names the callout type. The label is not a separate line.

```mdx
<Note>**Note:** You must have the Admin grant to perform this action.</Note>

<Warning>**Warning:** Deleting a connection cannot be undone.</Warning>

<Tip>**Tip:** Use keyboard shortcut `Cmd+K` to jump between articles.</Tip>
```

This convention exists because Mintlify's default callout rendering does not include a visible label, and Domo readers rely on the label to triage scan-reading.

## When to use vs. avoid

- **Use** when the information would be lost or skimmed past as plain prose, but is important.
- **Avoid** stacking 3+ callouts in a row — that's a sign the surrounding prose is structured wrong. Convert to a list, table, or `<Steps>` instead.
- **Avoid** putting a callout inside a list item; rendering is inconsistent. Lift it out.

## Mintlify reference

Current syntax: `https://mintlify.com/docs/components/callouts`

WebFetch this page if you need to confirm prop signatures or see new callout types.
