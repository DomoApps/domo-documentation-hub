#!/usr/bin/env bash
# Format-on-save wrapper for the VS Code customLocalFormatters extension.
#
# The extension spawns commands via `/bin/sh`, which doesn't source `.bashrc`
# and therefore doesn't pick up `nvm` (or `fnm`/`volta`). That means `node`
# isn't on PATH, and the formatter command fails with exit 127.
#
# This wrapper sources nvm directly so `node` resolves before invoking the
# pipeline. Add fnm/volta/etc. blocks here if you switch Node managers.

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

node scripts/split-table-rows.mjs | ./node_modules/.bin/remark --silent
