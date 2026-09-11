#!/usr/bin/env bash
#
# mint-preview.sh — trigger a Mintlify preview deploy for a branch and print the URL.
#
# Mirrors the API call in .github/workflows/mint-preview.yml, but for local use.
# Reads MINTLIFY_KEY and MINTLIFY_PROJECT_ID from the repo-root .env (gitignored).
#
# Usage:
#   ./scripts/mint-preview.sh                # preview the current branch
#   ./scripts/mint-preview.sh some-branch    # preview a specific branch
#
# Notes:
#   - Preview deploys require a Mintlify Pro or Enterprise plan.
#   - Mintlify builds from the branch on GitHub, so the branch must be pushed first.
#   - The endpoint is rate-limited to 5 requests/min per org.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$REPO_ROOT/.env"

if [ ! -f "$ENV_FILE" ]; then
  echo "error: $ENV_FILE not found. Copy the Mintlify vars into .env first." >&2
  exit 1
fi

# Load .env without executing it as code: only KEY=VALUE lines, comments/blank ignored.
while IFS='=' read -r key val; do
  case "$key" in
    ''|\#*) continue ;;
  esac
  # Strip a trailing inline comment and surrounding whitespace/quotes from the value.
  val="${val%%#*}"
  val="$(printf '%s' "$val" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/^"\(.*\)"$/\1/' -e "s/^'\(.*\)'$/\1/")"
  export "$key=$val"
done < "$ENV_FILE"

: "${MINTLIFY_KEY:?MINTLIFY_KEY is not set in .env}"
: "${MINTLIFY_PROJECT_ID:?MINTLIFY_PROJECT_ID is not set in .env}"

if [[ "$MINTLIFY_KEY" != mint_* ]]; then
  echo "warning: MINTLIFY_KEY does not start with 'mint_'; Mintlify admin keys are prefixed 'mint_'. The call will likely 401." >&2
fi

BRANCH="${1:-$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)}"
if [ -z "$BRANCH" ] || [ "$BRANCH" = "HEAD" ]; then
  echo "error: could not resolve a branch name (detached HEAD?). Pass one explicitly." >&2
  exit 1
fi

# Warn if the branch isn't on the remote — Mintlify builds from GitHub, not local.
if ! git -C "$REPO_ROOT" ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1; then
  echo "warning: branch '$BRANCH' was not found on origin. Push it before the preview can build:" >&2
  echo "         git push -u origin $BRANCH" >&2
fi

echo "Triggering Mintlify preview for branch: $BRANCH"

RESPONSE_FILE="$(mktemp)"
trap 'rm -f "$RESPONSE_FILE"' EXIT

HTTP_STATUS=$(curl --silent --show-error \
  --write-out '%{http_code}' \
  --output "$RESPONSE_FILE" \
  -X POST "https://api.mintlify.com/v1/project/preview/${MINTLIFY_PROJECT_ID}" \
  -H "Authorization: Bearer ${MINTLIFY_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"branch\": \"${BRANCH}\"}")

case "$HTTP_STATUS" in
  202) ;;
  400) echo "error: Mintlify rejected the request (400): $(cat "$RESPONSE_FILE")" >&2; exit 1 ;;
  401|403) echo "error: auth/plan error (HTTP $HTTP_STATUS). Preview deploys need Pro/Enterprise, and MINTLIFY_KEY must be valid for MINTLIFY_PROJECT_ID." >&2; exit 1 ;;
  429) echo "error: rate limited (429). The endpoint allows 5 req/min/org — wait and retry." >&2; exit 1 ;;
  *) echo "error: unexpected HTTP $HTTP_STATUS: $(cat "$RESPONSE_FILE")" >&2; exit 1 ;;
esac

if command -v jq >/dev/null 2>&1; then
  PREVIEW_URL=$(jq -r '.previewUrl // empty' "$RESPONSE_FILE")
  STATUS_ID=$(jq -r '.statusId // empty' "$RESPONSE_FILE")
else
  PREVIEW_URL=$(sed -n 's/.*"previewUrl"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$RESPONSE_FILE")
  STATUS_ID=$(sed -n 's/.*"statusId"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$RESPONSE_FILE")
fi

echo ""
[ -n "$PREVIEW_URL" ] && echo "Preview URL: $PREVIEW_URL"
[ -n "$STATUS_ID" ]   && echo "Status ID:   $STATUS_ID"
echo ""
echo "The build can take a minute or two — refresh if you see a build-in-progress splash."
