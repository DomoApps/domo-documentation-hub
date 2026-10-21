// Stringify overrides that keep formatter output close to how KB articles are
// already written, so format-on-save doesn't rewrite untouched content.
import { defaultHandlers } from "mdast-util-to-markdown";
import { visit } from "unist-util-visit";
import { mdxParser, sameRendering } from "./mdx-render-shape.mjs";

// The style guide writes these flush-left; the MDX serializer indents children.
const FLUSH_CHILDREN = new Set(["AccordionGroup", "Accordion"]);

export function remarkDomoFormat() {
  const data = this.data();
  const jsxHandlers = {};
  const jsx = (name) =>
    (jsxHandlers[name] ??= findHandler(data.toMarkdownExtensions ?? [], name));

  data.settings = {
    ...data.settings,
    handlers: {
      ...data.settings?.handlers,
      text: unescapeIntrawordUnderscores,
      break: twoSpaceBreak,
      link: preserveLiteralLink,
      mdxJsxFlowElement(node, parent, state, info) {
        let out = jsx("mdxJsxFlowElement")(node, parent, state, info);
        if (node.data?.splitRows) out = splitTableRows(node, out);
        if (FLUSH_CHILDREN.has(node.name)) out = dedentChildren(out);
        return collapseSingleChild(node, out);
      },
      mdxJsxTextElement(node, parent, state, info) {
        const out = jsx("mdxJsxTextElement")(node, parent, state, info);
        return node.data?.splitRows ? splitTableRows(node, out) : out;
      },
    },
  };

  return (tree, file) => {
    const source = String(file.value);
    visit(tree, "link", (node) => {
      const start = source[node.position?.start.offset];
      if (start && start !== "[" && start !== "<") {
        const { start: s, end: e } = node.position;
        node.data = { ...node.data, literalSource: source.slice(s.offset, e.offset) };
      }
    });
    markSplittableTables(tree, null);
    // GFM renders only the header's columns, but the serializer pads every row
    // (header included) to the widest one, which would add visible columns.
    visit(tree, "table", (table) => {
      const width = table.children[0]?.children.length ?? 0;
      for (const row of table.children) row.children = row.children.slice(0, width);
    });
  };
}

// Splitting a table onto several lines is only valid MDX when nothing else
// shares its lines: a block, or an inline table that is its paragraph's only
// content. A tag-only line interrupts a paragraph, so a table after text (or
// nested in a cell after text) would lose its closing tags. Nested tables stay
// inline inside their row's line.
function markSplittableTables(node, parent) {
  if (isJsx(node) && node.name === "table") {
    const alone =
      node.type === "mdxJsxFlowElement" ||
      (parent?.type === "paragraph" && parent.children.every((c) => c === node || isBlank(c)));
    if (alone) node.data = { ...node.data, splitRows: true };
    return;
  }
  for (const child of node.children ?? []) markSplittableTables(child, node);
}

const isJsx = (node) => node.type === "mdxJsxFlowElement" || node.type === "mdxJsxTextElement";
const isBlank = (node) => node.type === "text" && !node.value.trim();

// Mirrors how mdast-util-to-markdown merges extensions: nested first, later wins.
function findHandler(extensions, name) {
  let found;
  for (const extension of extensions) {
    if (extension.extensions) found = findHandler(extension.extensions, name) ?? found;
    if (extension.handlers?.[name]) found = extension.handlers[name];
  }
  return found;
}

// CommonMark never treats an intraword `_` as emphasis, so the escape is noise.
function unescapeIntrawordUnderscores(...args) {
  return defaultHandlers
    .text(...args)
    .replace(/(?<=[\p{L}\p{N}])\\_(?=[\p{L}\p{N}])/gu, "_");
}

function twoSpaceBreak(...args) {
  return defaultHandlers.break(...args).replace(/\\\n$/, "  \n");
}

// A bare URL is a GFM autolink literal; print it back the way it was written,
// unless the next character (say, a decoded `&gt;`) would extend the literal.
function preserveLiteralLink(node, parent, state, info) {
  const source = node.data?.literalSource;
  if (source && /^$|^[\s<.,;:!?)*_~]/.test(info.after)) return source;
  return defaultHandlers.link(node, parent, state, info);
}

// Runs in the handler so new lines pick up the indentation of an enclosing list
// item. Nested tables are masked so only this table's own rows move. A row
// whose content already spans lines can end up with a tag-only line that ends
// the paragraph early, so a split is kept only if it parses back the same.
function splitTableRows(node, out) {
  const split = splitRows(out);
  if (split === out) return out;
  try {
    return sameRendering([node], mdxParser.parse(split).children) ? split : out;
  } catch {
    return out;
  }
}

function splitRows(out) {
  const nested = [];
  let depth = 0;
  let start = 0;
  const masked = out.replace(/<table\b|<\/table>/g, (tag, offset) => {
    if (tag === "</table>") {
      if (--depth === 1) nested.push(out.slice(start, offset + tag.length));
    } else if (++depth === 2) start = offset;
    return tag;
  });
  let result = masked;
  nested.forEach((segment, i) => (result = result.replace(segment, `\u0000${i}\u0000`)));
  result = result
    .replace(/(?<!\n[ \t]*)(<tr\b[^>]*>)/g, "\n$1")
    .replace(/(<\/tr>)(?![ \t]*\n)/g, "$1\n");
  return result.replace(/\u0000(\d+)\u0000/g, (_, i) => nested[i]);
}

function dedentChildren(out) {
  const lines = out.split("\n");
  if (lines.length < 3) return out;
  const inner = lines.slice(1, -1).map((line) => (line.startsWith("  ") ? line.slice(2) : line));
  return [lines[0], ...inner, lines.at(-1)].join("\n");
}

// `<Frame><img /></Frame>` style: one element child that fits on one line.
// Only applied when the one-line form parses back to the same structure, since
// MDX turns a line holding text plus tags into inline JSX inside a paragraph.
function collapseSingleChild(node, out) {
  const [child] = node.children;
  if (node.children.length !== 1 || child.type !== "mdxJsxFlowElement") return out;
  const lines = out.split("\n");
  if (lines.length !== 3) return out;
  const collapsed = lines[0] + lines[1].trim() + lines[2];
  return sameRendering([node], mdxParser.parse(collapsed).children) ? collapsed : out;
}
