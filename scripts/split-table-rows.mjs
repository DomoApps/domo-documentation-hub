#!/usr/bin/env node
// Break inline <table>...</table> blocks across lines by putting each
// <tr>...</tr> on its own line. Whitespace between table children doesn't
// affect rendering — purely a source-readability transform.
//
// Two modes:
//   * No args  → reads stdin, writes stdout (used by the format-on-save
//                pipeline as the stage after remark).
//   * Args     → treats each as a file path; reads, transforms, writes back
//                in place (used by `yarn format:tables` for bulk runs).
//
// Idempotent: re-running on already-formatted output does not introduce
// extra newlines. Fenced code blocks (```...```) are skipped so literal
// <tr> text in code samples isn't corrupted.

import { readFile, writeFile } from "node:fs/promises";

function transform(content) {
  const parts = content.split(/(```[\s\S]*?```)/g);
  return parts
    .map((part, i) => {
      if (i % 2 === 1) return part;
      return part
        // Insert newline before <tr> unless it already starts a (possibly
        // indented) line. The `[ \t]*` lets remark's indentation pass through.
        .replace(/(?<!\n[ \t]*)(<tr\b[^>]*>)/g, "\n$1")
        // Insert newline after </tr> unless it already ends a line.
        .replace(/(<\/tr>)(?![ \t]*\n)/g, "$1\n");
    })
    .join("");
}

const files = process.argv.slice(2);

if (files.length === 0) {
  let input = "";
  for await (const chunk of process.stdin) input += chunk;
  process.stdout.write(transform(input));
} else {
  for (const file of files) {
    const before = await readFile(file, "utf8");
    const after = transform(before);
    if (after !== before) {
      await writeFile(file, after, "utf8");
    }
  }
}
