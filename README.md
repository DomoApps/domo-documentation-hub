# Domo Documentation Hub

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FDomoApps%2Fdomo-documentation-hub.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FDomoApps%2Fdomo-documentation-hub?ref=badge_shield)

Domo's public documentation site — Getting Started guides, the Knowledge Base (~1,700 articles), API Reference, and topic pages. Content is authored in MDX, navigation is defined in `docs.json`, and the site is built and hosted by [Mintlify](https://mintlify.com).

## Repository layout

- `portal/` — Developer Portal, topic-organized content (Getting Started, API Reference, etc.)
- `s/article/`, `s/topic/` — Knowledge Base articles and topic grouping pages
- `de/`, `es/`, `fr/`, `ja/` — localized content mirroring `s/`
- `openapi/product/` — OpenAPI YAML specs that drive the interactive API reference
- `images/` — screenshots and diagrams
- `docs.json` — Mintlify navigation and configuration (Mintlify manifest)
- `.github/workflows/` — automation for OpenAPI sync and Mintlify preview deployments

## Preview changes locally

We recommend using Visual Mode in the [Mintlify MDX](https://marketplace.visualstudio.com/items?itemName=mintlify.mintlify-snippets) VS Code extension. It provides a rich editor experience that matches the Mintlify dashboard. Live preview is also available, which uses the Mintlify CLI (see below) to open a browser preview that can follow as you navigate between files in VS Code. Additionally, selecting the extension icon from the left sidebar opens a file explorer that mirrors the published site's structure.

Use the [`mint`](https://www.npmjs.com/package/mint) npm package (the Mintlify CLI) for a local dev server against this repo's content. It requires Node.js v20.17.0 or later.

```bash
npm i -g mint           # once per machine — see https://www.mintlify.com/docs/cli/install
git checkout <branch>   # any branch with changes you want to preview
mint dev                # run from the repo root (where docs.json lives)
```

Open [http://localhost:3000](http://localhost:3000). Most edits hot-reload; `docs.json` schema changes may need a server restart.

### Switching from the old `mintlify` package

The CLI used to be published as `mintlify`. That package is now legacy and should not be used. If you installed it before, remove it and install `mint` instead:

```bash
npm uninstall -g mintlify
npm cache clean --force
npm i -g mint
```

To check which one you have, run `npm ls -g` (look for `mint` versus `mintlify`) or `which mint`. See [mintlify versus mint package](https://www.mintlify.com/docs/cli/install#mintlify-versus-mint-package) for details.

### Troubleshooting

#### "Client not built" error

If `mint dev` fails with:

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
mint dev
```

## Deployment

Merging does not publish. Once your changes are approved and merged into `main`, they are held until the next scheduled release, at which point Mintlify rebuilds the site and the updated content goes live.

- **Release schedule:** to be included in the following Monday's release, submit your PR by Thursday. The release is cut Friday early afternoon. Monday morning, the Enablement team switches over the release branch via an EC ticket; after that changeover completes, Mintlify rebuilds and the content is live.
- **Mid-week releases:** in certain circumstances, such as a specific customer ask or a highly visible fix, a release can be cut mid-week. Contact the Knowledge Base Administrator to request one.
- **`release/**`** — pushes to release branches create a Mintlify preview via `.github/workflows/mint-preview.yml`. Preview URL is posted to any open PR whose head is the release branch.
- **Any PR** — Mintlify's GitHub App posts a preview link in the PR's Checks tab.

## Contributing

Training on how to contribute to this repository is available in the [KB Contribution App](https://domo.domo.com/app-studio/649552668/pages/1393071293). To request access to the app, contact the Knowledge Base Administrator: Jared Peterson ([jared.peterson@domo.com](mailto:jared.peterson@domo.com)).

## Writing content

- `CLAUDE.md` — repo conventions and MDX style.
- `Domo-KB-Style-Guide.mdx` — full style standards.
- `New-Article-Template.mdx` — starting point for new KB articles.

## Useful Mintlify references

- [Mintlify docs](https://mintlify.com/docs) · [CLI](https://mintlify.com/docs/cli) · [`docs.json` schema](https://mintlify.com/docs/settings/global) · [Components](https://mintlify.com/docs/components/overview) · [MDX VS Code Extension](https://www.mintlify.com/docs/cli/mdx-extension)

## License

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FDomoApps%2Fdomo-documentation-hub.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FDomoApps%2Fdomo-documentation-hub?ref=badge_large)
