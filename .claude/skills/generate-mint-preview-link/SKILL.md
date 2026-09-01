---
name: generate-mint-preview-link
user-invocable: true
description: "generate a Mintlify preview link for a branch, get a preview URL, preview this branch on Mintlify, trigger a Mintlify preview deploy locally"
argument-hint: "optional branch name (defaults to the current branch)"
---

Generate a Mintlify preview deploy for a branch and return the preview URL, using the local wrapper around the Mintlify preview API.

The user has provided: $ARGUMENTS

---

## What this does

Runs `scripts/mint-preview.sh`, which POSTs to the Mintlify preview API (`POST https://api.mintlify.com/v1/project/preview/{projectId}`) — the same call the CI workflow `.github/workflows/mint-preview.yml` makes — and prints back the `previewUrl`. This is the local, on-demand equivalent of the CI preview: use it when you want a preview link without waiting for the PR automation, or for a branch the automation doesn't cover.

## Prerequisites

1. **Credentials in `.env`** (repo root, gitignored). The script reads:
   - `MINTLIFY_KEY` — admin API key, prefixed `mint_`
   - `MINTLIFY_PROJECT_ID` — project ID

   Both come from https://dashboard.mintlify.com/settings/organization/api-keys and match the `MINTLIFY_KEY` / `MINTLIFY_PROJECT_ID` repo secrets. If either is missing, the script errors and names the missing variable — tell the user to add it to `.env`; never print or ask for the secret value in chat.
2. **A Mintlify Pro or Enterprise plan.** Without it the API returns 401/403 regardless of a valid key.
3. **The branch must be pushed to `origin`.** Mintlify builds the preview from the branch on GitHub, not the local working tree. The script warns if the branch isn't on `origin` and prints the `git push` command; a preview for an unpushed branch will fail to build.

## Steps

1. **Resolve the branch.** If the user named a branch in `$ARGUMENTS`, pass it as the argument. Otherwise the script defaults to the current branch.
2. **Confirm it's pushed.** If the target branch isn't on `origin`, offer to push it first (`git push -u origin <branch>`) — pushing is outward-facing, so confirm before doing it unless the user already asked.
3. **Run the script:**
   ```bash
   ./scripts/mint-preview.sh              # current branch
   ./scripts/mint-preview.sh <branch>     # named branch
   ```
4. **Report the URL.** Relay the `previewUrl` to the user. Note the build can take a minute or two — the link may show a build-in-progress splash until it finishes.

## Handling errors

The script maps the API's HTTP statuses to clear messages; relay them plainly:

| Status | Meaning | What to tell the user |
|---|---|---|
| 202 | Accepted | Success — preview is building; share the URL. |
| 400 | Bad request | Mintlify rejected the request (often a bad branch name). Check the branch exists on `origin`. |
| 401 / 403 | Auth / plan | Key invalid for the project, or the plan doesn't include preview deploys (needs Pro/Enterprise). |
| 429 | Rate limited | The endpoint allows 5 req/min per org. Wait and retry. |

Do not retry a 401/403 or 429 in a tight loop — surface it and let the user act.
