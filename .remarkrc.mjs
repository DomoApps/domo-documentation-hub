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
import remarkMath from "remark-math";
import remarkMdx from "remark-mdx";
import remarkPresetLintConsistent from "remark-preset-lint-consistent";
import remarkPresetLintMarkdownStyleGuide from "remark-preset-lint-markdown-style-guide";
import remarkPresetLintRecommended from "remark-preset-lint-recommended";
import remarkRetext from "remark-retext";
import retextEnglish from "retext-english";
import retextRepeatedWords from "retext-repeated-words";
import retextSentenceSpacing from "retext-sentence-spacing";
import retextSyntaxUrls from "retext-syntax-urls";
import stringWidth from "string-width";
import { unified } from "unified";

import { remarkDomoFormat } from "./scripts/remark-domo-format.mjs";
import {
  remarkDomoForbiddenTerms,
  remarkDomoImgAlt,
  remarkDomoNoBetaParenthetical,
  remarkDomoNoExclamation,
  remarkDomoNoH1,
} from "./scripts/remark-domo-style.mjs";
import { remarkStripRedundantLinkTitle } from "./scripts/remark-strip-redundant-link-title.mjs";

// Transformer: a list renders loose when it or any item is spread, but
// `remark-stringify` writes blank lines between items only when
// `list.spread === true`. Promote the list when an item is spread so the
// output spaces every item consistently. Never demote: a list written with
// blank lines between single-block items renders loose, and tightening it
// would change the page's spacing.
function remarkNormalizeListSpread() {
  return (tree) => {
    const walk = (node) => {
      if (!node || typeof node !== "object") return;
      if (node.type === "list" && Array.isArray(node.children)) {
        if (node.children.some((child) => child && child.spread === true)) {
          node.spread = true;
        }
      }
      if (Array.isArray(node.children)) {
        for (const child of node.children) walk(child);
      }
    };
    walk(tree);
  };
}

const config = {
  // `settings` configures remark-stringify (the formatter behind format-on-save
  // and `yarn format`) to match `remark-preset-lint-markdown-style-guide`, so
  // formatting never produces output the linter then flags.
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
    // this, the linter crashes on the first JSX tag. `tightSelfClosing` keeps
    // `<br/>` and `<img .../>` as most articles write them.
    [remarkMdx, { tightSelfClosing: true }],
    // `remark-gfm` must run on the outer mdast tree so the parser
    // recognizes task lists, tables, strikethrough, and autolinks.
    // Without this, `- [ ] item` parses as a plain list item and the
    // stringifier escapes the `[` to `\[` on every format-on-save.
    // `stringWidth` pads table columns by display width, so emoji and CJK
    // count as two columns (matching scripts/pad_md_tables.py).
    [remarkGfm, { stringLength: stringWidth }],
    // Mintlify renders `$...$` as LaTeX, so the formatter must parse math too
    // or it drops the `\$` escapes that keep a literal dollar sign literal.
    remarkMath,
    // Must run before stringify so the corrected `spread` flag drives output.
    remarkNormalizeListSpread,
    // Drop `[Text](/url "Text")` redundant titles — leftover from CMS
    // migration; the title duplicates the visible label.
    remarkStripRedundantLinkTitle,
    // Stringify overrides (see the file): each <tr> on its own line, one-line
    // single-child elements like <Frame><img/></Frame>, flush Accordions,
    // two-space hard breaks, no `\_` escapes, bare URLs left bare.
    remarkDomoFormat,
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
    // Off: blank lines between items decide whether a list renders loose, so
    // every mode of this rule asks writers to change the page's spacing.
    // remarkNormalizeListSpread adds the blank lines a list needs instead.
    [remarkLintListItemSpacing, false],
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
