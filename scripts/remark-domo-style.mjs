// Custom remark lint plugins that encode the Domo KB Style Guide
// (Domo-KB-Style-Guide.mdx) as mechanical rules.
//
// Each plugin only emits warnings (`file.message(...)`); none modify the
// AST. That means saving a file won't auto-rewrite anything — authors see
// warnings and fix manually. Run via `yarn check` or in the editor's remark
// language server.

// --- 1. Forbidden / replacement lexicon -----------------------------------
//
// Style guide bans these terms outright or pins them to specific Domo
// vocabulary. Single-word patterns use `\b` for word boundaries; phrase
// patterns are explicit. Patterns intentionally exclude tokens that overlap
// with general English (e.g. "Page", "graph", "Story") because we can't tell
// the Domo sense from the everyday sense without context.
const FORBIDDEN_TERMS = [
  {
    pattern: /\butilize[ds]?\b/gi,
    message: 'Never use "utilize"; use "use" instead.',
  },
  {
    pattern: /\bverbiage\b/gi,
    message: 'Avoid "verbiage"; use "words" or rewrite the sentence.',
  },
  {
    pattern: /\bwhitelist(s|ed|ing)?\b/gi,
    message: 'Use "allowlist" instead of "whitelist".',
  },
  {
    pattern: /\bblacklist(s|ed|ing)?\b/gi,
    message: 'Use "blocklist" instead of "blacklist".',
  },
  {
    pattern: /\bDojo\b/g,
    message: 'Use "Community Forums" instead of "Dojo".',
  },
  {
    pattern: /\bdrilldowns?\b/gi,
    message: 'Use "Drill Path(s)" or "drill into" instead of "drilldown".',
  },
  {
    pattern: /\bBeastmode\b/gi,
    message: 'Use "Beast Mode" (two words) instead of "Beastmode".',
  },
  {
    pattern: /\bDomoFusion\b/gi,
    message: 'Use "DataFusion" instead of "DomoFusion".',
  },
  {
    pattern: /\bSlicers?\b/g,
    message: 'Use "Quick Filter(s)" instead of "Slicer(s)".',
  },
  {
    pattern: /\bKPI cards?\b/gi,
    message: 'Use "Visualization Card" instead of "KPI card".',
  },
  {
    pattern: /\bImage cards?\b/gi,
    message: 'Use "Doc Card" instead of "Image card".',
  },
  {
    pattern: /\bPage Filters?\b/g,
    message: 'Use "Dashboard Filter(s)" instead of "Page Filter(s)".',
  },
  {
    pattern: /\bi\.e\./gi,
    message: 'Avoid Latin "i.e."; use "that is" or rewrite.',
  },
  {
    pattern: /\be\.g\./gi,
    message: 'Avoid Latin "e.g."; use "such as" or rewrite.',
  },
  {
    pattern: /\betc\./gi,
    message: 'Avoid Latin "etc."; end the list cleanly or rewrite.',
  },
];

export function remarkDomoForbiddenTerms() {
  return (tree, file) => {
    walk(tree, (node) => {
      if (node.type !== "text" || typeof node.value !== "string") return;
      for (const { pattern, message } of FORBIDDEN_TERMS) {
        pattern.lastIndex = 0;
        if (pattern.test(node.value)) {
          file.message(message, node);
        }
      }
    });
  };
}

// --- 2. No exclamation points in prose ------------------------------------
//
// Style guide: "Do not use exclamation points; if you think you may have an
// exception, speak to the Knowledge Base admin." Walking only `text` nodes
// naturally skips code blocks, inline code, JSX, and link URLs.
export function remarkDomoNoExclamation() {
  return (tree, file) => {
    walk(tree, (node) => {
      if (node.type !== "text" || typeof node.value !== "string") return;
      if (node.value.includes("!")) {
        file.message(
          "Do not use exclamation points; rephrase the sentence.",
          node,
        );
      }
    });
  };
}

// --- 3. No "(Beta)" parenthetical in titles or headings -------------------
//
// Style guide forbids `(Beta)` / `(BETA)` on titles and headings; use the
// frontmatter `tag: "Beta"` or a Badge component instead.
const BETA_PAREN = /\((?:Beta|BETA|beta)\)/;

export function remarkDomoNoBetaParenthetical() {
  return (tree, file) => {
    walk(tree, (node) => {
      if (node.type === "yaml" && typeof node.value === "string") {
        const titleLine = node.value.match(/^title:\s*(.+)$/m);
        if (titleLine && BETA_PAREN.test(titleLine[1])) {
          file.message(
            'Do not append "(Beta)" to the article title; use `tag: "Beta"` in frontmatter instead.',
            node,
          );
        }
      }
      if (node.type === "heading" && BETA_PAREN.test(headingText(node))) {
        file.message(
          'Do not append "(Beta)" to a heading; use a <Badge>Beta</Badge> after the heading text instead.',
          node,
        );
      }
    });
  };
}

// --- 4. No H1 in article body ---------------------------------------------
//
// Frontmatter `title:` renders as H1, so body headings should start at H2.
export function remarkDomoNoH1() {
  return (tree, file) => {
    walk(tree, (node) => {
      if (node.type === "heading" && node.depth === 1) {
        file.message(
          "Body content should not contain an H1; the frontmatter `title` renders as H1. Use H2 (##) or deeper.",
          node,
        );
      }
    });
  };
}

// --- 5. Image alt-text presence -------------------------------------------
//
// Style guide screenshot example uses `alt="Descriptive alt text"`. We flag
// both Markdown images (`![](src)`) and MDX JSX `<img>` whose `alt` is
// missing or an empty/whitespace string. Expression-valued `alt={...}` is
// skipped since we can't evaluate it at lint time.
export function remarkDomoImgAlt() {
  return (tree, file) => {
    walk(tree, (node) => {
      // Markdown image syntax
      if (node.type === "image") {
        const alt = typeof node.alt === "string" ? node.alt.trim() : "";
        if (!alt) {
          file.message(
            "Image is missing alt text. Provide descriptive alt text.",
            node,
          );
        }
        return;
      }

      // MDX JSX <img ...>
      if (
        (node.type === "mdxJsxFlowElement" ||
          node.type === "mdxJsxTextElement") &&
        node.name === "img"
      ) {
        const attrs = Array.isArray(node.attributes) ? node.attributes : [];
        const altAttr = attrs.find(
          (a) => a && a.type === "mdxJsxAttribute" && a.name === "alt",
        );
        if (!altAttr) {
          file.message(
            "<img> is missing the required `alt` attribute. Provide descriptive alt text.",
            node,
          );
          return;
        }
        const value = altAttr.value;
        // value is `null` for `alt`, a string for `alt="..."`, or an object
        // for `alt={...}` expressions. Only flag the first two empty cases.
        if (value === null) {
          file.message(
            "<img alt> has no value. Provide descriptive alt text.",
            node,
          );
        } else if (typeof value === "string" && value.trim() === "") {
          file.message(
            '<img alt=""> is empty. Provide descriptive alt text.',
            node,
          );
        }
      }
    });
  };
}

// --- helpers --------------------------------------------------------------

function walk(node, visitor) {
  if (!node || typeof node !== "object") return;
  visitor(node);
  if (Array.isArray(node.children)) {
    for (const child of node.children) walk(child, visitor);
  }
}

function headingText(node) {
  let out = "";
  const collect = (n) => {
    if (!n) return;
    if (n.type === "text" && typeof n.value === "string") out += n.value;
    if (Array.isArray(n.children)) n.children.forEach(collect);
  };
  collect(node);
  return out;
}
