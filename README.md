# Domo Documentation Hub

Domo's public documentation site — Getting Started guides, the Knowledge Base (\~1,700 articles), API Reference, and topic pages. Content is authored in MDX, navigation is defined in `docs.json`, and the site is built and hosted by [Mintlify](https://mintlify.com).

## Repository layout

- `portal/` — Developer Portal, topic-organized content (Getting Started, API Reference, etc.)
- `s/article/`, `s/topic/` — Knowledge Base articles and topic grouping pages
- `de/`, `es/`, `fr/`, `ja/` — localized content mirroring `s/`
- `openapi/product/` — OpenAPI YAML specs that drive the interactive API reference
- `images/` — screenshots and diagrams
- `docs.json` — Mintlify navigation and configuration (Mintlify manifest)
- `.github/workflows/` — automation for OpenAPI sync and Mintlify preview deployments

## Preview changes locally

Uses the [`mint`](https://www.npmjs.com/package/mint) npm package (pinned as a devDependency, so `yarn install` is all you need) for a local dev server against this repo's content.

```bash
git checkout <branch>   # any branch with changes you want to preview
yarn dev                # run from the repo root (where docs.json lives)
```

Open [http://localhost:3000](http://localhost:3000). Most edits hot-reload; `docs.json` schema changes may need a server restart.

Other handy scripts:

```bash
yarn broken-links   # scan internal links and flag broken ones
yarn validate       # strict build check — fails on any warning or error
```

For a faster, but less robust preview experience, VS Code has several extenstions offering an MDX preview. For example: [Modern MDX Preview](https://marketplace.visualstudio.com/items?itemName=ggfincke.vsc-mdx-preview).

### Troubleshooting

#### "Client not built" error

If `yarn dev` fails with:

```text
Error: Client not built. Run: cd <path>/apps/client && STANDALONE_BUILD=true NEXT_PUBLIC_ENV=cli yarn build
```

The Mintlify CLI's internal `tar` library may have silently skipped dotfile directories (like `.next/`) when extracting its client package, leaving the cache broken (see [this issue](https://github.com/mintlify/docs/issues/5624)). Work around it by extracting manually with the system `tar`:

```bash
# 1. Clear the broken cache
rm -rf ~/.mintlify

# 2. Download the client package manually (uses system tar, which handles dotfiles correctly)
VERSION=$(curl -s https://releases.mintlify.com/mint-version.txt)
mkdir -p ~/.mintlify
curl -s -o /tmp/mint.tar.gz "https://releases.mintlify.com/mint-${VERSION}.tar.gz"
tar -xzf /tmp/mint.tar.gz -C ~/.mintlify
echo "$VERSION" > ~/.mintlify/mint/mint-version.txt
rm /tmp/mint.tar.gz

# 3. Run as normal — mint will see the version file and skip the re-download
yarn dev
```

## Editor setup & formatting

MDX is formatted and linted with [remark](https://github.com/remarkjs/remark) + plugins (config in [.remarkrc.mjs](.remarkrc.mjs)). Format-on-save in VS Code shells out to the same pipeline, so editor and CLI produce identical output.

### One-time setup

1. **Install Node 20+** via [nvm](https://github.com/nvm-sh/nvm) (recommended), [fnm](https://github.com/Schniz/fnm), or [volta](https://volta.sh). The format-on-save wrapper at [scripts/format-mdx.sh](scripts/format-mdx.sh) currently sources nvm — if you use a different manager, add the equivalent block.
2. **Enable Yarn 4** (the repo pins `yarn@4.14.1` via `packageManager`):
   ```bash
   corepack enable
   ```
3. **Install dependencies** from the repo root:
   ```bash
   yarn install
   ```
4. **Install the recommended VS Code extensions.** When you open the repo, VS Code will prompt for the ones listed in [.vscode/extensions.json](.vscode/extensions.json):
   - [`unifiedjs.vscode-mdx`](https://marketplace.visualstudio.com/items?itemName=unifiedjs.vscode-mdx) — MDX language support (syntax highlighting, JSX-aware parsing).
   - [`jkillian.custom-local-formatters`](https://marketplace.visualstudio.com/items?itemName=jkillian.custom-local-formatters) — runs `scripts/format-mdx.sh` as the MDX formatter so format-on-save uses our remark pipeline.

[.vscode/settings.json](.vscode/settings.json) wires `formatOnSave` for `[mdx]` to the local-formatters extension — no per-user config needed.

### Manual formatting & linting

```bash
yarn format         # split wide table rows, then run remark --output across all .mdx
yarn format:remark  # remark only (skip the table-row splitter)
yarn format:tables  # table-row splitter only
yarn check          # lint without writing — exits non-zero on any remark warning
```

Run `yarn check` before opening a PR if you've made bulk changes outside the editor.

## Deployment

- **`main`** — merges auto-deploy to production via the Mintlify GitHub App.
- **`release/**`** — pushes to release branches create a Mintlify preview via `.github/workflows/mint-preview.yml`. Preview URL is posted to any open PR whose head is the release branch.
- **Any PR** — Mintlify's GitHub App posts a preview link in the PR's Checks tab.

## Writing content

- `CLAUDE.md` — repo conventions and MDX style.
- `Domo-KB-Style-Guide.mdx` — full style standards.
- `New-Article-Template.mdx` — starting point for new KB articles.

## Useful Mintlify references

- [Mintlify docs](https://mintlify.com/docs) · [CLI](https://mintlify.com/docs/cli) · [`docs.json` schema](https://mintlify.com/docs/settings/global) · [Components](https://mintlify.com/docs/components/overview)
