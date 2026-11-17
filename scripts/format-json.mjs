#!/usr/bin/env node
// Pretty-print the JSON on stdin with 2-space indentation, for the "Format JSON"
// Filter Text command. Re-indents the original tokens instead of round-tripping
// through JSON.parse, so number literals like 1786548125.374035183 keep every digit.

import { readFileSync } from "node:fs";

const input = readFileSync(0, "utf8");
const leading = input.match(/^\s*/)[0];
const trailing = input.match(/\s*$/)[0];
const json = input.trim();

function fail(message) {
  // Filter Text replaces the selection with stdout, so print nothing on failure.
  process.stderr.write(`format-json: ${message}\n`);
  process.exit(1);
}

if (!json) fail("nothing selected");
try {
  JSON.parse(json);
} catch (err) {
  fail(`selection is not valid JSON (${err.message})`);
}

const tokens = json.match(/"(?:[^"\\]|\\.)*"|[{}[\],:]|[^\s{}[\],:"]+/g);

// The selection may start at the opening brace (mid-line) rather than at the
// start of the line, so fall back to the closing line's indentation.
const lines = json.split("\n");
const baseIndent =
  leading.split("\n").pop() || (lines.length > 1 ? lines.at(-1).match(/^\s*/)[0] : "");

const pad = (depth) => baseIndent + "  ".repeat(depth);
let out = "";
let depth = 0;
for (let i = 0; i < tokens.length; i++) {
  const token = tokens[i];
  const next = tokens[i + 1];
  if (token === "{" || token === "[") {
    if (next === (token === "{" ? "}" : "]")) {
      out += token + next;
      i++;
    } else {
      out += token + "\n" + pad(++depth);
    }
  } else if (token === "}" || token === "]") {
    out += "\n" + pad(--depth) + token;
  } else if (token === ",") {
    out += ",\n" + pad(depth);
  } else if (token === ":") {
    out += ": ";
  } else {
    out += token;
  }
}

process.stdout.write(leading + out + trailing);
