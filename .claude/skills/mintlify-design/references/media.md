# Media components

For images, screenshots, video. Domo has strong conventions here — follow them.

## `<Frame>` — screenshots

Wrap **every screenshot** in `<Frame>`. Frame auto-sizes to content width and renders a subtle border.

```mdx
<Frame>
  <img src="/images/kb/example-screenshot.png" alt="The admin console" />
</Frame>
```

- The inner element is a raw `<img>`, not Markdown image syntax. Markdown image syntax inside `<Frame>` does not always render correctly.
- `alt` is required. Describe what the screenshot shows, not "screenshot of X."
- Optional `caption` prop renders text below the frame.

## Inline UI icons — Domo icon fonts (preferred)

For UI icons that flow inside a sentence (gear, alert bell, chart-line, etc.), use a Domo icon font. Two are wired up in `style.css`, and they share the same glyph set — pick the font that matches the UI you're depicting:

- **`icon-{name}`** — phosphor (the design refresh; ~1,000 glyphs). Browse at [Domo Icons (phosphor)](https://git.empdev.domo.com/pages/Development/DomoIcons/#!/icons/phosphor). **Default for current Domo product surfaces.**
- **`legacy-icon-{name}`** — the previous-generation Domo icons. Browse at [Domo Icons (domocons)](https://git.empdev.domo.com/pages/Development/DomoIcons/#!/icons/domocons). **Only for surfaces that still ship the older icons** — release notes describing the pre-refresh UI, and legacy applications such as Workbench.

Both fonts cover the same glyph names (it's a design refresh, not a coverage gap), so the choice is about *which UI* the article depicts, never about availability.

```mdx
Click <i className="icon-gear" aria-hidden="true" /> **Settings** to open Settings.

In Workbench, click <i className="legacy-icon-database" aria-hidden="true" /> in the left icon bar.
```

- Icons inherit text color and size automatically — they adapt to light/dark mode without any extra props.
- Override size only when needed: `<i className="icon-gear" style={{fontSize: 24}} aria-hidden="true" />`.

**Accessibility: pair every icon with an inline text label**

Icon-font glyphs use Unicode Private Use Area codepoints — screen readers announce them as garbage if not handled. The default pattern hides the icon from the a11y tree and relies on surrounding prose to carry the meaning:

```mdx
Click <i className="icon-gear" aria-hidden="true" /> **Settings** to open Settings.
```

If the existing prose doesn't name the icon (e.g. "click \<icon\>"), rewrite the prose to label it inline. This helps every reader, not just screen-reader users:

- ❌ "Click <i className="icon-chart-line" aria-hidden="true" /> to view the chart."
- ✅ "Click the line chart icon <i className="icon-chart-line" aria-hidden="true" /> to view the chart."

**Narrow exception — `aria-label` for standalone icons**

Use `role="img"` + `aria-label` instead of `aria-hidden` only when the icon truly stands alone with no surrounding prose (icon-only button, icon as a link's sole content, tight table-cell glyph):

```mdx
<i className="icon-gear" role="img" aria-label="Settings" />
```

In flowing KB prose, the inline-label rewrite is always preferable to `aria-label`.

**Avoid** `<Icon icon="/images/icons/gear.svg" />` (Mintlify's component pointing at a local SVG). Mintlify loads the SVG via `<img>`, so the `color` prop and `currentColor` don't reach the paths — the icon stays black in dark mode. Use the icon font instead.

## Inline `<img>` — fallback for non-icon glyphs

When the inline glyph you need isn't in either Domo icon font (e.g. a small UI screenshot or product-specific marker captured as an image), use a native `<img>` with an inline `style` block so the image flows with surrounding text instead of breaking onto its own line. (For a third-party *brand* logo, prefer a coded icon over an image — see "Brand and third-party logos" below.)

```mdx
Click <img src="/images/kb/some-ui-fragment.png" alt="UI fragment" style={{height: '1.2em', display: 'inline', verticalAlign: 'start', margin: '0'}}/> to continue.
```

Use `height: '1.2em'` (or `'1.6em'`) to match body text, `height: '2em'` when the icon stands alone as a row label in a table cell, or a bare number (e.g. `111`) for fixed-pixel screenshots embedded in a table cell. Keep `display: 'inline'`, `verticalAlign: 'start'`, and `margin: '0'` consistent so the image sits on the baseline of the surrounding text without injecting vertical space.

## Brand and third-party logos

Company/product logos (AWS, OpenAI, Anthropic, GitHub, …) aren't in either Domo icon font. Don't reach for an `<img>` — a logo image is almost always a solid-color mark that disappears on a dark background. Prefer a coded icon that inherits text color, in this order:

1. **Font Awesome brands.** Mintlify's default icon library is Font Awesome, and its *brands* family carries most major logos. Reference with the `<Icon>` component:

   ```mdx
   <Icon icon="openai" iconType="brands" aria-hidden="true" />
   ```

   The `icon` value is the brand slug (`aws`, `openai`, `github`, …) — browse at [Font Awesome Brands](https://fontawesome.com/search?f=brands). This is the **one** case where `<Icon>` is correct: it's resolving a font glyph, not loading a local SVG, so the dark-mode caveat below doesn't apply.

2. **Inline `<svg fill="currentColor">`.** Some brands aren't in FA's free set (Anthropic, for one). Paste the logo's SVG directly and set `fill="currentColor"` so it tracks the theme. [Simple Icons](https://simpleicons.org) has ready-to-paste paths:

   ```mdx
   <svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor" style={{height: '1.1em', width: '1.1em', display: 'inline', verticalAlign: '-0.15em', margin: '0'}}><path d="..." /></svg>
   ```

   This is raw inline SVG, not `<Icon>` pointing at a file — `fill="currentColor"` is what makes it theme-adaptive.

Fall back to an uploaded `<img>` only if the logo exists in neither place; if so, use a version legible on both light and dark backgrounds. Accessibility: when adjacent text already names the brand (e.g. a link reading "OpenAI"), use `aria-hidden="true"`; reserve `role="img"` + `aria-label` for a logo that stands alone.

## Video / embeds

Mintlify supports `<iframe>` for YouTube/Loom and a `<video>` tag for self-hosted. WebFetch `https://mintlify.com/docs/image-embeds` for current syntax — usage in this repo is rare.

## Common mistakes

- Using `<Icon icon="/images/icons/*.svg" />` for inline UI icons — Mintlify loads local SVGs via `<img>`, so `color`/`currentColor` can't reach the paths and dark mode breaks. Use the Domo icon font instead (see "Inline UI icons" above).
- Using a raw `<img>` for a UI icon when the glyph is in the icon font — the font versions (`icon-*` for current UI, `legacy-icon-*` for legacy surfaces) inherit color and theme automatically; images don't.
- Using a monochrome `<img>` for a third-party brand logo — it disappears in dark mode. Use a Font Awesome `brands` icon or an inline `<svg fill="currentColor">` instead (see "Brand and third-party logos").
- Using `legacy-icon-*` for a current Domo product surface, or `icon-*` for a legacy surface like Workbench — pick the font that matches the UI being depicted.
- Wrapping inline icons in `<Frame>` — `<Frame>` is only for full screenshots that stand on their own.
- Using Markdown `![alt](src)` inside `<Frame>` — use raw `<img>` instead.
- Forgetting `alt` — required for accessibility and required by lint.
- Putting screenshots at full bleed without `<Frame>` — they look unfinished.

## Mintlify reference

- `https://mintlify.com/docs/components/frames`
- `https://mintlify.com/docs/image-embeds`
