# Domo Documentation Hub
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FDomoApps%2Fdomo-documentation-hub.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FDomoApps%2Fdomo-documentation-hub?ref=badge_shield)


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

Uses the [`mintlify`](https://www.npmjs.com/package/mintlify) npm package for a local dev server against this repo's content.

```bash
npm i -g mintlify       # once per machine — see https://www.npmjs.com/package/mintlify
git checkout <branch>   # any branch with changes you want to preview
mintlify dev            # run from the repo root (where docs.json lives)
```

Open [http://localhost:3000](http://localhost:3000). Most edits hot-reload; `docs.json` schema changes may need a server restart.

For a faster, but less robust preview experience, VS Code has several extenstions offering an MDX preview. For example: [Modern MDX Preview](https://marketplace.visualstudio.com/items?itemName=ggfincke.vsc-mdx-preview).

### Troubleshooting

#### "Client not built" error

If `mintlify dev` fails with:

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

# 3. Run as normal — mintlify will see the version file and skip the re-download
mintlify dev
```

## Deployment

- **`main`** — merges auto-deploy to production via the Mintlify GitHub App.
- **`release/**`** — pushes to release branches create a Mintlify preview via `.github/workflows/mint-preview.yml`. Preview URL is posted to any open PR whose head is the release branch.
- **Any PR** — Mintlify's GitHub App posts a preview link in the PR's Checks tab.

## Contributing

Training on how to contribute to this repository is available in the [KB Contribution App](https://domo.domo.com/app-studio/649552668/pages/1393071293). To request access to the app, contact the Knowledge Base Administrator: Jared Peterson ([jared.peterson@domo.com](mailto:jared.peterson@domo.com)).

## Writing content

- `CLAUDE.md` — repo conventions and MDX style.
- `Domo-KB-Style-Guide.mdx` — full style standards.
- `New-Article-Template.mdx` — starting point for new KB articles.

## Useful Mintlify references

- [Mintlify docs](https://mintlify.com/docs) · [CLI](https://mintlify.com/docs/cli) · [`docs.json` schema](https://mintlify.com/docs/settings/global) · [Components](https://mintlify.com/docs/components/overview)


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FDomoApps%2Fdomo-documentation-hub.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FDomoApps%2Fdomo-documentation-hub?ref=badge_large)