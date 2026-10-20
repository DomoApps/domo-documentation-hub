#!/usr/bin/env bash
# Optional MDX formatter for the Custom Local Formatters VS Code extension.
# Always exits 0 and falls back to echoing the input, because the extension
# replaces the document with stdout: a failed run must never blank the file.

cd "$(dirname "$0")/.." || exit 0
repo=$PWD
file=${1:-}

input=$(mktemp)
output=$(mktemp)
trap 'rm -f "$input" "$output"' EXIT
cat > "$input"

case "$file" in
  "$repo"/*) ;;
  *)
    echo "format-mdx: skipped, file is outside $repo" >&2
    cat "$input"
    exit 0
    ;;
esac

# GUI-launched editors can miss PATH entries added by Node version managers.
if ! command -v node > /dev/null 2>&1; then
  export PATH="$HOME/.local/share/mise/shims:$HOME/.volta/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
  export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
  [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" > /dev/null 2>&1
fi

remark=node_modules/.bin/remark
if ! command -v node > /dev/null 2>&1 || [ ! -x "$remark" ]; then
  echo "format-mdx: skipped, Node or node_modules missing (run yarn install)" >&2
  cat "$input"
  exit 0
fi

# remark skips .remarkignore for stdin input, so check it with the same matcher.
status=$(node -e '
  const ig = require("ignore")().add(require("fs").readFileSync(".remarkignore", "utf8"));
  console.log(ig.ignores(process.argv[1]) ? "ignored" : "ok");
' "${file#"$repo"/}" 2> /dev/null)
if [ "$status" != ok ]; then
  echo "format-mdx: skipped, file is in .remarkignore (or the check failed)" >&2
  cat "$input"
  exit 0
fi

format() { "$remark" --silent --rc-path .remarkrc.mjs --file-path "$file" "$@"; }
# Re-parse the result so a plugin bug can never save a file that no longer builds.
if format < "$input" > "$output" && [ -s "$output" ] && format --no-stdout < "$output" 2> /dev/null; then
  cat "$output"
else
  cat "$input"
fi
exit 0
