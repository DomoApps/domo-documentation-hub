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

## Inline images — raw `<img>` with inline style

For images that flow inside a sentence (icons, button glyphs at line height), do **not** use `<Frame>`. Use a raw `<img>` with inline `style={{}}`:

```mdx
Click the gear icon <img src="/images/kb/gear.png" alt="" style={{display: 'inline', height: '1.2em', verticalAlign: 'middle'}} /> to open settings.
```

## `InlineImage` snippet — preferred for inline images

The repo has a snippet at `/snippets/InlineImage.mdx` that wraps the inline-image pattern with sane defaults:

```mdx
import { InlineImage } from '/snippets/InlineImage.mdx';

Click the gear icon <InlineImage src="/images/kb/gear.png" /> to open settings.
```

Defaults: `height='1.6em'`, `display: inline`, `verticalAlign: start`, `noZoom`. Prefer `InlineImage` over hand-rolled inline `<img>` styles when the result fits the defaults.

## Video / embeds

Mintlify supports `<iframe>` for YouTube/Loom and a `<video>` tag for self-hosted. WebFetch `https://mintlify.com/docs/image-embeds` for current syntax — usage in this repo is rare.

## Common mistakes

- Wrapping inline icons in `<Frame>` — `<Frame>` is only for full screenshots that stand on their own.
- Using Markdown `![alt](src)` inside `<Frame>` — use raw `<img>` instead.
- Forgetting `alt` — required for accessibility and required by lint.
- Putting screenshots at full bleed without `<Frame>` — they look unfinished.

## Mintlify reference

- `https://mintlify.com/docs/components/frames`
- `https://mintlify.com/docs/image-embeds`
