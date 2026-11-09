#!/usr/bin/env node
// Verify that formatting with .remarkrc.mjs only changes how MDX is written,
// never what it renders. Each file is formatted in memory (nothing is written),
// then both versions are parsed and compared (see mdx-render-shape.mjs).
//
//   node scripts/check-format-safety.mjs <file-or-dir>...
//   node scripts/check-format-safety.mjs --compare <before.mdx> <after.mdx>
//
// Exits 1 when any output fails to parse or renders differently.
import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import ignore from "ignore";
import remarkParse from "remark-parse";
import remarkStringify from "remark-stringify";
import { unified } from "unified";
import { mdxParser, renderShape } from "./mdx-render-shape.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");

const args = process.argv.slice(2);
if (args.length === 0 || (args[0] === "--compare" && args.length !== 3)) {
  console.error(readFileSync(fileURLToPath(import.meta.url), "utf8").split("\n").slice(1, 9).join("\n"));
  process.exit(2);
}

if (args[0] === "--compare") {
  const [before, after] = args.slice(1).map((p) => readFileSync(p, "utf8"));
  const problem = compare(before, after);
  console.log(problem ? `${args[1]}: ${problem}` : "Same rendered structure.");
  process.exit(problem ? 1 : 0);
}

const { default: config } = await import(pathToFileURL(join(root, ".remarkrc.mjs")).href);
const formatter = unified().use(remarkParse).use(remarkStringify).use(config);
const ignored = ignore().add(readFileSync(join(root, ".remarkignore"), "utf8"));

let checked = 0;
let failed = 0;
let skipped = 0;
for (const path of args.flatMap((arg) => collect(resolve(arg)))) {
  const value = readFileSync(path, "utf8");
  const name = relative(process.cwd(), path);
  let output;
  try {
    output = String(await formatter.process({ path, value }));
  } catch (error) {
    skipped++;
    console.log(`${name}: skipped, original does not parse: ${error.reason ?? error.message}`);
    continue;
  }
  checked++;
  const problem = compare(value, output);
  if (problem) {
    failed++;
    console.log(`${name}: ${problem}`);
  }
}
console.log(`${checked} files checked, ${failed} with problems, ${skipped} skipped.`);
process.exit(failed ? 1 : 0);

function collect(path) {
  const rel = relative(root, path);
  if (rel && !rel.startsWith("..") && ignored.ignores(statSync(path).isDirectory() ? `${rel}/` : rel)) return [];
  if (!statSync(path).isDirectory()) return [path];
  return readdirSync(path).flatMap((name) => {
    if (name.startsWith(".") || name === "node_modules") return [];
    const child = join(path, name);
    return statSync(child).isDirectory() || name.endsWith(".mdx") ? collect(child) : [];
  });
}

function compare(before, after) {
  const positions = new WeakMap();
  const a = renderShape(mdxParser.parse(before), positions);
  let b;
  try {
    b = renderShape(mdxParser.parse(after), positions);
  } catch (error) {
    return `formatted output does not parse: ${error.reason ?? error.message}`;
  }
  const diff = firstDifference(a, b, []);
  if (!diff) return null;
  const at = (side) => {
    const node = [...diff.trail[side]].reverse().find((n) => positions.has(n));
    return node ? positions.get(node).start.line : "?";
  };
  const where = `line ${at(0)} before, line ${at(1)} after`;
  if (diff.key === "loose") return `list renders ${diff.b ? "loose" : "tight"} instead of ${diff.a ? "loose" : "tight"} (${where})`;
  return `rendered structure changes (${where}): ${preview(diff.key, diff.a)} -> ${preview(diff.key, diff.b)}`;
}

function preview(key, value) {
  const text = `${key}=${JSON.stringify(value) ?? String(value)}`;
  return text.length > 120 ? `${text.slice(0, 117)}...` : text;
}

function firstDifference(a, b, trail, key) {
  if (typeof a !== typeof b || typeof a !== "object" || a === null || b === null) {
    return a === b ? null : { a, b, key, trail: [trail.map((t) => t[0]), trail.map((t) => t[1])] };
  }
  for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) {
    const diff = firstDifference(a[k], b[k], [...trail, [a, b]], k);
    if (diff) return diff;
  }
  return null;
}
