# Code Engine Documentation Rework — Followups

Items that emerged during the rework but weren't resolved. Each is a candidate for a future ticket.

## Unverified against source

- [ ] **JS `codeengine` module method surface** — Current docs list `sendRequest`, `getAccount`, `axios`, `getPersonDetails`, `getExecutionDetails`. Runtime source was not located in accessible sibling repos during the rework. Confirm against the actual Code Engine Lambda/sandbox runtime (likely a separate internal service). Update `concepts/the-codeengine-library.mdx` if signatures differ.
- [ ] **JS `require()` allowlist** — The runtime allowlist was not located. `javascript-libraries.mdx` ships with 2 third-party entries (`axios`, `google-auth-library`) and an "as of 2026-04-23" qualifier. Confirm the full list and add any missing libraries.
- [ ] **Python runtime allowlist** — The list in `python-packages.mdx` (`boto3`, `botocore`, `certifi`, `numpy`, `pandas`, `requests`) was carried over from the prior page and not verified. Confirm by locating a `requirements.txt` or equivalent in the Python runtime service.
- [ ] **Python-side `codeengine` equivalent module** — Existence unconfirmed. `concepts/the-codeengine-library.mdx` has an explicit "Python equivalents" section marked UNVERIFIED. Fill it in once the Python surface is known, or remove the section if no equivalent exists.
- [ ] **Account alias configuration model (server side)** — `AccountAliasConfiguration` is defined in the DomoWeb UI but the server-side contract (how the mapping is stored, resolved at call time, and retrieved from the function via `codeengine.getAccount`) was not traced. Deep-dive and expand `concepts/functions-and-types.mdx` Account Aliasing section if the server-side model exposes anything users should know.

## Scope deferrals (explicitly out of scope for this project)

- [ ] Localization of new pages (`de/`, `es/`, `fr/`, `ja/`) — follows the existing Domo localization process; no action needed here.
- [ ] Per-package tutorials beyond `Packages/Instance-Management` and `Packages/Cards-to-PDF`.
- [ ] Exposing any of the UI-owned endpoints (package create/update/delete, version save/delete, working-version code updates) as documented contracts. Current decision: keep out of the public contract.

## Maintenance / polish

- [ ] If additional endpoints are added to `openapi/product/codeengine.yaml`, update the `docs.json` "Code Engine API" nav group (around line 2777) to include them.
- [ ] Audit remaining cross-references to the old KB-article permalinks (e.g. `/s/article/000005173`) across the rest of the docs and repoint to the new concept pages where sensible. The rework already caught the Code Engine section's references; other sections (e.g. App Framework guides, Partner Developer guides) may still link at the old KB.
- [ ] The framework OpenAPI spec uses `{functionAlias}` as the path parameter for the primary path and `{alias}` for the deprecated `/complex` path. Align both to one name (likely `{alias}`) for consistency — cosmetic.
- [ ] Confirm the Mintlify preview build renders the Mermaid diagram on `concepts/packages-and-versions.mdx`. Mermaid support varies by Mintlify config; if it doesn't render, replace with a plain prose lifecycle description or an image.
- [ ] Verify the three screenshot paths referenced in `calling/from-a-custom-app.mdx` (`/images/dev/stoplight.io/images/Screenshot-2024-02-13-at-2.3*.png`) render in the Mintlify preview. They were reused from the previous guide so should work, but confirm visually.

## Observations worth noting

- The permalink `fbhbpt1mt4gog-code-engine-api` was previously on two files simultaneously (a Mintlify collision). Resolved by retiring the app-framework page; the permalink now uniquely identifies `API-Reference/Product-APIs/Code-Engine.mdx` with a redirect entry for legacy traffic.
- The ShareRequest and GroupedEntityPermissions enum values in `openapi/product/codeengine.yaml` were initially drafted as `[VIEW, EDIT, EXECUTE, OWNER]` but corrected during execution to `[OWNER, WRITE, READ, EXECUTE, NONE]` to match the `accessLevelToPermissionsMap` in DomoWeb `codeEngine/models/constants.ts:63`. Future contributors to the spec should use the latter set.
