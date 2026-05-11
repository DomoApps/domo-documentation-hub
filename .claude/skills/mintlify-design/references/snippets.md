# Authoring snippets

Snippets are reusable MDX/JSX components that live in `/snippets/` and import into pages. Mintlify supports two flavors:

- **`.mdx` snippets** — exported MDX components, optionally JSX-flavored. Best when the snippet is mostly markup with light parameterization. Example: `/snippets/InlineImage.mdx`.
- **`.jsx` snippets** — React components with logic, props, and computation. Best when the snippet needs real behavior (computed styles, data transforms). Examples: `/snippets/ColorTable.jsx`, `/snippets/TypographyTable.jsx`.

## When to extract a snippet

Extract when **all** of:
- The same MDX/JSX block appears in 3+ places, or is about to.
- The block is more than ~3 lines of structured markup (not just a single styled element).
- The block has at least one parameter that varies between uses.

Don't extract just because a pattern repeats once or twice — inline MDX is fine and usually clearer.

## `.mdx` snippet pattern (preferred for markup)

Filename: `/snippets/MyComponent.mdx`

```mdx
export const MyComponent = ({ title, children }) => {
  return (
    <div className="my-component">
      <h3>{title}</h3>
      {children}
    </div>
  );
};
```

Usage in a page:

```mdx
import { MyComponent } from '/snippets/MyComponent.mdx';

<MyComponent title="Hello">Body content here.</MyComponent>
```

Real example — `InlineImage.mdx`:

```mdx
export const InlineImage = ({ src, alt = '', height = '1.6em' }) => {
  return (
    <img
      noZoom
      src={src}
      alt={alt}
      style={{
        display: 'inline',
        verticalAlign: 'start',
        height: height,
        margin: '0'
      }}
    />
  );
};
```

## `.jsx` snippet pattern (preferred for logic)

Filename: `/snippets/MyComponent.jsx`. Same `export const Foo = () => {}` shape, but you can include real computation, state (rare in docs), and helpers. See `/snippets/ColorTable.jsx` for a worked example with luminance computation.

## Conventions

- **Default exports vs. named exports** — this repo uses **named exports** (`export const InlineImage = ...`). Match that.
- **Default props** — provide defaults for optional props in the destructure: `({ src, alt = '', height = '1.6em' })`.
- **Imports** — page imports use the absolute path from repo root: `import { Foo } from '/snippets/Foo.mdx';`.
- **No external React imports** — Mintlify provides the React runtime. Don't add `import React from 'react'`.

## Mintlify reference

`https://mintlify.com/docs/reusable-snippets`

WebFetch this page when authoring a snippet that needs features beyond what's documented here (props validation, async data, etc.).
