#!/usr/bin/env node
/**
 * html-to-mdx.mjs — convert HTML in stdin to Markdown/MDX on stdout.
 *
 * Wired to VS Code via the "Filter Text" extension: select an HTML block, run
 * the "Convert HTML to Markdown" command, and the selection is replaced with
 * Markdown that conforms to Domo-KB-Style-Guide.mdx. Surrounding text is left
 * alone (the extension only pipes the selection through stdin → stdout).
 *
 * Engine: unified — rehype-parse (tolerant HTML5 parser) → rehype-remark
 * (HTML AST → Markdown AST) → remark-gfm + remark-stringify (Markdown AST →
 * text). This handles the full set of standard HTML elements automatically:
 *
 *   <p>                       paragraph (tag removed, blank-line separated)
 *   <b>/<strong>              **bold**
 *   <i>/<em>                  _italic_
 *   <code>                    `inline code`
 *   <pre>/<pre><code>         ```fenced code block```
 *   <h1>–<h6>                 # … ###### headings
 *   <ul>/<ol>/<li>            - / 1. lists
 *   <a href>                  [text](href)
 *   <img src>                 ![alt](src)
 *   <blockquote>              > quote
 *   <hr>                      ---
 *   <br>                      hard line break
 *   <table>                   padded GFM pipe table
 *
 * Stringify options mirror .remarkrc.mjs (bullet "-", emphasis "_", rule "-",
 * one-space list indent) so output matches format-on-save and causes no churn.
 *
 * MDX/JSX preservation
 * --------------------
 * rehype-parse is a *pure HTML* parser — it would mangle JSX such as
 * style={{…}}, className, and PascalCase components (<Note>, <Frame>, …). So
 * before parsing we lift every MDX/JSX construct out as an inert sentinel
 * token and splice it back verbatim after stringify. A tag is treated as MDX
 * (and preserved) when it is:
 *
 *   - a PascalCase component:        <Note>, <Frame>, <Accordion title="…">, …
 *   - any tag with a JSX className:  <i className="icon-foo" />
 *   - any tag with a JSX expression: <img style={{display:'inline'}} />
 *
 * Everything around and inside a preserved component is still converted, so a
 * <Note> wrapping <p>/<b> keeps the <Note> wrapper and converts its contents.
 *
 * Known limitations (chosen trade-offs, not bugs)
 * ----------------------------------------------
 *   - rowspan/colspan and nested tables flatten (GFM pipe tables can't express
 *     spans). The old table-only script left these as HTML; this one does not.
 *   - A paired *lowercase* JSX element (e.g. <i className="x">text</i>) keeps
 *     its open tag but its bare </i> may be dropped. Repo convention writes
 *     these self-closing (<i className="…" />), which is handled correctly.
 *
 * On any failure the original selection is written back unchanged (never
 * blanked) and the reason is written to stderr.
 */

const STRINGIFY_OPTIONS = {
  bullet: "-",
  emphasis: "_",
  listItemIndent: "one",
  rule: "-",
  fences: true,
};

function warn(msg) {
  process.stderr.write(`html-to-mdx: ${msg}\n`);
}

// --- MDX/JSX masking -------------------------------------------------------

// Matches a single open, close, or self-closing tag. Attribute values
// containing ">" are not supported (JSX style={{…}} and quoted attrs don't
// contain ">", so this is safe for our content).
const TAG_RE = /<\/?[A-Za-z][A-Za-z0-9.-]*(?:\s[^<>]*?)?\/?>/g;

// HTML void elements never have a closing tag, so a non-self-closed one (e.g.
// <img style={{…}}>) is still a complete element, not the start of a region.
const VOID = new Set([
  "area", "base", "br", "col", "embed", "hr", "img", "input",
  "link", "meta", "param", "source", "track", "wbr",
]);

function parseTag(tag) {
  const close = tag.match(/^<\/\s*([A-Za-z][A-Za-z0-9.-]*)/);
  if (close) return { name: close[1], kind: "close" };
  const name = (tag.match(/^<\s*([A-Za-z][A-Za-z0-9.-]*)/) || [])[1] || "";
  if (/\/>\s*$/.test(tag) || VOID.has(name.toLowerCase())) {
    return { name, kind: "self" };
  }
  return { name, kind: "open" };
}

// A tag begins an MDX construct (to preserve, not convert) when it is a
// PascalCase component, carries a JSX className, or carries a JSX expression
// attribute (style={{…}}, attr={…}).
function startsMdx(tag, info) {
  if (info.kind === "close") return false;
  if (/^[A-Z]/.test(info.name)) return true;
  if (/\bclassName\b/.test(tag)) return true;
  if (/=\s*\{/.test(tag)) return true;
  return false;
}

// Replace [start,end) with a sentinel token. A component that sits on its own
// line(s) in the source is wrapped in a <p> so the HTML parser keeps it a
// standalone block — it stringifies to its own paragraph and won't merge with
// neighbours (HTML collapses blank lines to whitespace, so a bare token would
// glue onto adjacent text). Inline JSX (icons, inline images) stays in place.
//
// Inside a table cell, everything must stay on one line: never block-wrap, and
// store a whitespace-collapsed (single-line) copy of the component so restoring
// it can't inject newlines that would shatter the pipe-table row.
function emitToken(input, start, end, store, base, inCell) {
  const token = `${base}${store.length}zz`;
  const value = input.slice(start, end);
  if (inCell) {
    store.push(value.replace(/\s*\n\s*/g, " "));
    return token;
  }
  store.push(value);
  const blockBefore = /(^|\n)[ \t]*$/.test(input.slice(0, start));
  const blockAfter = /^[ \t]*(\n|$)/.test(input.slice(end));
  return blockBefore && blockAfter ? `<p>${token}</p>` : token;
}

// Lift MDX/JSX out of the HTML before parsing. PascalCase components are
// preserved as whole blocks (open tag through matching close, nesting-aware)
// so their already-authored Markdown content is never re-escaped; self-closing
// JSX and inline JSX-attributed tags are preserved as single tokens.
function maskMdx(input) {
  let base = "zzMDXMASKzz";
  while (input.includes(base)) base += "z";
  const store = [];
  let out = "";
  let cursor = 0; // input copied verbatim up to here
  let regionStart = -1; // -1 when not inside a preserved block
  let depth = 0;
  let cellDepth = 0; // >0 when inside a <td>/<th> (components must stay inline)

  TAG_RE.lastIndex = 0;
  for (let m; (m = TAG_RE.exec(input)) !== null; ) {
    const tag = m[0];
    const info = parseTag(tag);

    if (regionStart === -1) {
      if (!startsMdx(tag, info)) {
        // ordinary HTML — leave for rehype, but track table-cell context.
        if (info.name === "td" || info.name === "th") {
          cellDepth =
            info.kind === "close" ? Math.max(0, cellDepth - 1) : cellDepth + 1;
        }
        continue;
      }
      if (info.kind === "self") {
        out += input.slice(cursor, m.index);
        out += emitToken(input, m.index, m.index + tag.length, store, base, cellDepth > 0);
        cursor = m.index + tag.length;
      } else {
        regionStart = m.index; // begin a paired component block
        depth = 1;
      }
    } else {
      if (info.kind === "open") depth++;
      else if (info.kind === "close" && --depth === 0) {
        const end = m.index + tag.length;
        out += input.slice(cursor, regionStart);
        out += emitToken(input, regionStart, end, store, base, cellDepth > 0);
        cursor = end;
        regionStart = -1;
      }
    }
  }

  if (regionStart !== -1) {
    warn("unterminated MDX component; preserved it to end of selection");
    out += input.slice(cursor, regionStart);
    out += emitToken(input, regionStart, input.length, store, base);
    cursor = input.length;
  }
  out += input.slice(cursor);
  return { masked: out, store, base };
}

function restoreMdx(output, store, base) {
  return output.replace(
    new RegExp(`${base}(\\d+)zz`, "g"),
    (_, i) => store[Number(i)] ?? "",
  );
}

// Move whitespace from just inside an inline formatting tag to just outside it,
// so "<b> Number </b>" becomes " <b>Number</b> ". Markdown can't keep a space
// adjacent to the marker ("** Number **" isn't emphasis), so without this
// remark-stringify encodes the space as a noisy &#x20; entity and escapes the
// abutting character. Runs after masking, so preserved components are inert
// tokens and left alone.
const INLINE = "b|strong|i|em|code|a|span|sub|sup|abbr|mark|del|ins";
function hoistInlineWhitespace(html) {
  return html
    .replace(new RegExp(`<(${INLINE})((?:\\s[^<>]*)?)>[ \\t\\n]+`, "gi"), " <$1$2>")
    .replace(new RegExp(`[ \\t\\n]+</(${INLINE})>`, "gi"), "</$1> ");
}

// --- pipeline --------------------------------------------------------------

// Sentinel marking a paragraph break inside a table cell. A GFM pipe cell is a
// single line and can't hold paragraph breaks, so multiple <p> blocks in one
// cell would otherwise collapse onto one run-on line. A real hard-break node
// renders as a space inside a cell, so instead we drop this placeholder between
// the paragraphs and swap it for a literal <br/> after stringify — scoped to
// cells, leaving <br> elsewhere as a normal Markdown hard break.
//
// `<br/>` (no space) is the form the Domo KB Style Guide and the rest of the
// repo use. The sentinel is exactly as long as "<br/>" (5 chars) and replaced
// 1:1, so the column padding remark-gfm computes while the sentinel is in place
// stays valid after the swap (a different length would misalign the table).
const CELL_BREAK = "zzBRz";

// rehype (hast) transform: within <td>/<th>, insert CELL_BREAK between adjacent
// <p> children so their boundaries survive into the pipe table.
function rehypeTableCellParagraphBreaks() {
  const walk = (node) => {
    if (!node || typeof node !== "object") return;
    if (
      node.type === "element" &&
      (node.tagName === "td" || node.tagName === "th") &&
      Array.isArray(node.children)
    ) {
      const out = [];
      let prevWasP = false;
      for (const child of node.children) {
        const isP = child.type === "element" && child.tagName === "p";
        if (isP && prevWasP) out.push({ type: "text", value: CELL_BREAK });
        out.push(child);
        if (child.type === "element") prevWasP = isP;
      }
      node.children = out;
    }
    if (Array.isArray(node.children)) node.children.forEach(walk);
  };
  return (tree) => walk(tree);
}

// Escape literal "$" as "\$". Mintlify renders `$...$` as LaTeX inline math
// (KaTeX), so an unescaped dollar — common in KB content as a currency symbol —
// gets paired with the next `$` on the line and swallows the text between them
// into a math span. Scoped to phrasing, so `$` inside inline code and code
// blocks (e.g. `$HOME`, `$10`) is left untouched. Registered as a toMarkdown
// extension because remark-stringify ignores an `extensions` option passed
// directly to it.
function remarkEscapeDollar() {
  const data = this.data();
  (data.toMarkdownExtensions || (data.toMarkdownExtensions = [])).push({
    unsafe: [{ character: "$", inConstruct: "phrasing" }],
  });
}

// Collapse whitespace-only JSX expressions like {" "} / {' '} to a plain space.
// These are MDX migration cruft (the HTML parser passes them through as text).
// Operates on mdast `text` nodes only, so an occurrence inside a code span or
// code block — where it'd be real code — is left alone (code is not a text node).
//
// Then trims whitespace at the edges of phrasing blocks (paragraph, heading,
// table cell) and drops paragraphs left empty. A {" "} at the start/end of a
// block collapses to a lone edge space, which is insignificant when rendered
// but which remark-stringify would otherwise preserve as a noisy &#x20; entity.
const JSX_SPACE = /\{\s*(["'])\s*\1\s*\}/g;
const EDGE_TRIM_BLOCKS = new Set(["paragraph", "heading", "tableCell"]);

function remarkCollapseJsxSpace() {
  const walk = (node) => {
    if (!Array.isArray(node.children)) return;

    for (const child of node.children) {
      if (child.type === "text" && typeof child.value === "string") {
        child.value = child.value.replace(JSX_SPACE, " ");
      }
    }

    if (EDGE_TRIM_BLOCKS.has(node.type)) {
      const kids = node.children;
      const first = kids[0];
      const last = kids[kids.length - 1];
      if (first && first.type === "text") {
        first.value = first.value.replace(/^\s+/, "");
      }
      if (last && last.type === "text") {
        last.value = last.value.replace(/\s+$/, "");
      }
      node.children = kids.filter(
        (c) => !(c.type === "text" && c.value === ""),
      );
    }

    node.children.forEach(walk);
  };

  const prune = (node) => {
    if (!Array.isArray(node.children)) return;
    node.children = node.children.filter(
      (c) => !(c.type === "paragraph" && c.children.length === 0),
    );
    node.children.forEach(prune);
  };

  return (tree) => {
    walk(tree);
    prune(tree);
  };
}

async function buildProcessor() {
  const [{ unified }, rehypeParse, rehypeRemark, remarkGfm, remarkStringify] =
    await Promise.all([
      import("unified"),
      import("rehype-parse"),
      import("rehype-remark"),
      import("remark-gfm"),
      import("remark-stringify"),
    ]);
  return unified()
    .use(rehypeParse.default, { fragment: true })
    .use(rehypeTableCellParagraphBreaks)
    .use(rehypeRemark.default)
    .use(remarkGfm.default)
    .use(remarkCollapseJsxSpace)
    .use(remarkEscapeDollar)
    .use(remarkStringify.default, STRINGIFY_OPTIONS);
}

async function convert(html, processor) {
  const { masked, store, base } = maskMdx(html);
  const file = await processor.process(hoistInlineWhitespace(masked));
  const out = String(file).split(CELL_BREAK).join("<br/>");
  return restoreMdx(out, store, base).replace(/\n+$/, "");
}

function readStdin() {
  return new Promise((resolve) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (data += chunk));
    process.stdin.on("end", () => resolve(data));
  });
}

async function main() {
  const input = await readStdin();
  let processor;
  try {
    processor = await buildProcessor();
  } catch (err) {
    warn(
      `could not load the conversion libraries (${err.message}). ` +
        `Run "yarn install" in the repo root. Selection left unchanged.`,
    );
    process.stdout.write(input);
    return;
  }
  try {
    process.stdout.write(await convert(input, processor));
  } catch (err) {
    warn(`conversion failed (${err.message}); selection left unchanged.`);
    process.stdout.write(input);
  }
}

main();
