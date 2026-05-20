// ESM config: every `remark-*`/`retext-*`/`unified` package in this project is
// `"type": "module"` so CJS `require()` cannot load them. The `.mjs` extension
// forces ESM resolution regardless of the cosmiconfig version inside
// `unified-engine` / `remark-language-server`.
import remarkFrontmatter from "remark-frontmatter";
import remarkGfm from "remark-gfm";
import remarkLintFileExtension from "remark-lint-file-extension";
import remarkLintListItemSpacing from "remark-lint-list-item-spacing";
import remarkLintMaximumHeadingLength from "remark-lint-maximum-heading-length";
import remarkLintMaximumLineLength from "remark-lint-maximum-line-length";
import remarkLintNoDuplicateHeadings from "remark-lint-no-duplicate-headings";
import remarkLintNoFileNameIrregularCharacters from "remark-lint-no-file-name-irregular-characters";
import remarkLintEmphasisMarker from "remark-lint-emphasis-marker";
import remarkLintNoFileNameMixedCase from "remark-lint-no-file-name-mixed-case";
import remarkLintOrderedListMarkerValue from "remark-lint-ordered-list-marker-value";
import remarkMdx from "remark-mdx";
import remarkPresetLintConsistent from "remark-preset-lint-consistent";
import remarkPresetLintMarkdownStyleGuide from "remark-preset-lint-markdown-style-guide";
import remarkPresetLintRecommended from "remark-preset-lint-recommended";
import remarkRetext from "remark-retext";
import retextEnglish from "retext-english";
import retextRepeatedWords from "retext-repeated-words";
import retextSentenceSpacing from "retext-sentence-spacing";
import retextSyntaxUrls from "retext-syntax-urls";
import { unified } from "unified";

import {
  remarkDomoForbiddenTerms,
  remarkDomoImgAlt,
  remarkDomoNoBetaParenthetical,
  remarkDomoNoExclamation,
  remarkDomoNoH1,
} from "./scripts/remark-domo-style.mjs";

// Transformer: normalize a list's `spread` to match its items. CommonMark says
// a list is loose iff any item has internal blank-line block separation, but
// remark only sets list-level `spread` from sibling spacing in the source. On
// save, `remark-stringify` writes blank lines between items only when
// `list.spread === true`, so we promote it whenever any child item is spread,
// and demote it when none are. Result: tight by default, loose only when an
// item contains sub-blocks (continuation paragraph, sub-list, Note, code, etc.).
function remarkNormalizeListSpread() {
  return (tree) => {
    const walk = (node) => {
      if (!node || typeof node !== "object") return;
      if (node.type === "list" && Array.isArray(node.children)) {
        node.spread = node.children.some(
          (child) => child && child.spread === true,
        );
      }
      if (Array.isArray(node.children)) {
        for (const child of node.children) walk(child);
      }
    };
    walk(tree);
  };
}

const config = {
  // `settings` configures remark-stringify (the formatter that
  // `unified-prettier` runs on format-on-save) to match the lint rules
  // enforced by `remark-preset-lint-markdown-style-guide`. Without these,
  // Prettier emits `*` bullets while the linter wants `-` — fight on every
  // save.
  settings: {
    bullet: "-",
    emphasis: "_",
    listItemIndent: "one",
    rule: "-",
  },
  plugins: [
    remarkFrontmatter,
    // `remark-mdx` lets the parser handle JSX, imports, and expressions in
    // .mdx files (Mintlify components like <Frame>, <Note>, etc.). Without
    // this, the linter crashes on the first JSX tag.
    remarkMdx,
    // `remark-gfm` must run on the outer mdast tree so the parser
    // recognizes task lists, tables, strikethrough, and autolinks.
    // Without this, `- [ ] item` parses as a plain list item and the
    // stringifier escapes the `[` to `\[` on every format-on-save.
    remarkGfm,
    // Must run before stringify so the corrected `spread` flag drives output.
    remarkNormalizeListSpread,
    [
      remarkRetext,
      unified().use({
        plugins: [
          retextEnglish,
          retextSyntaxUrls,
          [retextSentenceSpacing, { preferred: 1 }],
          retextRepeatedWords,
        ],
      }),
    ],
    remarkPresetLintConsistent,
    remarkPresetLintRecommended,
    remarkPresetLintMarkdownStyleGuide,
    // Override style-guide rules that fight prose docs. Order matters —
    // these must come *after* the preset to win the last-in-wins merge.
    [remarkLintMaximumLineLength, false],
    [remarkLintMaximumHeadingLength, false],
    [remarkLintNoDuplicateHeadings, false],
    // Enforce CommonMark loose/tight list convention: lists stay tight unless
    // any item has multi-block content (continuation paragraph, sub-list,
    // Note/Frame/code block, etc.), in which case every sibling needs a blank
    // line between it and the next.
    [remarkLintListItemSpacing, { checkBlanks: true }],
    // Authors number ordered lists explicitly (1./2./3.); the style-guide
    // default ("1.") forces every item to `1.` which is noisy in source.
    [remarkLintOrderedListMarkerValue, false],
    // Mintlify-style: italics use `_` (the style-guide preset enforces `*`).
    // Strong stays `**` via the preset default.
    [remarkLintEmphasisMarker, "_"],
    // KB articles use numeric IDs (e.g. 000005784.mdx) and snake_case asset
    // names, both of which trip this rule.
    [remarkLintNoFileNameIrregularCharacters, false],
    // Mintlify supports both `.md` and `.mdx`.
    [remarkLintFileExtension, ["md", "mdx"]],
    // KB filenames like `Domo-KB-Style-Guide.mdx` and `New-Article-Template.mdx`
    // are intentionally Title-Case-Kebab.
    [remarkLintNoFileNameMixedCase, false],
    // Domo KB Style Guide enforcement (see scripts/remark-domo-style.mjs).
    // Lint-only; never auto-fix.
    remarkDomoForbiddenTerms,
    remarkDomoNoExclamation,
    remarkDomoNoBetaParenthetical,
    remarkDomoNoH1,
    remarkDomoImgAlt,
  ],
};

export default config;
