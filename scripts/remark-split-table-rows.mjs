// Put each <tr> on its own line in raw <table> blocks. Whitespace between
// table children doesn't affect rendering — this is purely a source-
// readability transform. Migrated KB articles often collapse entire tables
// onto one line, which blows past VS Code's 20,000-char syntax-highlighting
// threshold and makes diffs unreadable.
//
// remark-stringify writes HTML/JSX blocks back roughly as it parsed them,
// so a pure AST transform can't reliably reshape these. We instead wrap the
// processor's stringify() method and post-process its output. Idempotent:
// re-running on already-split content adds no further newlines. Fenced code
// blocks (```...```) are skipped so literal <tr> text in code samples isn't
// corrupted.

export function remarkSplitTableRows() {
  const processor = this;
  const originalStringify = processor.stringify.bind(processor);
  processor.stringify = function stringifyWithSplitTableRows(tree, file) {
    const output = originalStringify(tree, file);
    return typeof output === "string" ? splitRows(output) : output;
  };
}

function splitRows(content) {
  return content
    .split(/(```[\s\S]*?```)/g)
    .map((part, i) => {
      if (i % 2 === 1) return part; // inside a fenced code block
      return part
        .replace(/(?<!\n[ \t]*)(<tr\b[^>]*>)/g, "\n$1")
        .replace(/(<\/tr>)(?![ \t]*\n)/g, "$1\n");
    })
    .join("");
}
