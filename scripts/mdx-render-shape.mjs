// What an MDX tree renders, minus the source details formatting may change:
// whitespace, escapes, link titles that repeat the link text, inline vs block
// JSX, and table rows padded or trimmed to the header width. Two trees with
// the same shape produce the same page. Used by remark-domo-format.mjs and
// check-format-safety.mjs.
import remarkFrontmatter from "remark-frontmatter";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import remarkMdx from "remark-mdx";
import remarkParse from "remark-parse";
import { unified } from "unified";

export const mdxParser = unified()
  .use(remarkParse)
  .use(remarkMdx)
  .use(remarkGfm)
  .use(remarkMath)
  .use(remarkFrontmatter);

export function sameRendering(a, b) {
  return JSON.stringify(renderShape(a)) === JSON.stringify(renderShape(b));
}

// `positions`, when given, maps each shaped node back to its source position.
export function renderShape(node, positions) {
  if (Array.isArray(node)) {
    return node.flatMap((n) => (isUnravelled(n) ? n.children : [n])).map((n) => renderShape(n, positions));
  }
  if (!node || typeof node !== "object") return node;

  const out = {};
  for (const [key, value] of Object.entries(node)) {
    if (key === "position" || key === "data" || key === "spread") continue;
    out[key] = renderShape(value, positions);
  }
  if (positions && node.position) positions.set(out, node.position);

  if (out.type === "mdxJsxFlowElement" || out.type === "mdxJsxTextElement") out.type = "mdxJsxElement";
  if (["text", "inlineCode", "html", "mdxFlowExpression", "mdxTextExpression"].includes(out.type)) {
    out.value = out.value.replace(/\s+/g, " ");
  }
  if (out.type === "mdxJsxAttribute" && out.value && typeof out.value === "object") {
    out.value = out.value.value.replace(/\s+/g, "");
  }
  if (out.type === "link" && (!out.title || collapse(textOf(node)) === collapse(out.title))) delete out.title;
  if (node.type === "list") out.loose = node.spread || node.children.some((item) => item.spread);
  if (out.type === "table") {
    const width = out.children[0]?.children.length ?? 0;
    out.align = Array.from({ length: width }, (_, i) => out.align[i] ?? null);
    for (const row of out.children) {
      row.children = row.children.slice(0, width);
      while (row.children.length < width) row.children.push({ type: "tableCell", children: [] });
    }
  }
  if (out.children) out.children = mergeText(out.children);
  return out;
}

// MDX compiles a paragraph holding only JSX and whitespace without a <p>.
function isUnravelled(node) {
  return (
    node?.type === "paragraph" &&
    node.children.every(
      (c) => c.type === "mdxJsxTextElement" || c.type === "mdxTextExpression" || (c.type === "text" && !c.value.trim()),
    )
  );
}

function mergeText(children) {
  const merged = [];
  for (const child of children) {
    const last = merged.at(-1);
    if (child.type === "text" && last?.type === "text") last.value = collapse(last.value + child.value);
    else merged.push(child);
  }
  return merged
    .map((c) => (c.type === "text" ? { ...c, value: c.value.trim() } : c))
    .filter((c) => !(c.type === "text" && c.value === ""));
}

function textOf(node) {
  return node.value ?? (node.children ?? []).map(textOf).join("");
}

function collapse(text) {
  return text.replace(/\s+/g, " ").trim();
}
