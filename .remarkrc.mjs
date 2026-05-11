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
import remarkLintNoFileNameMixedCase from "remark-lint-no-file-name-mixed-case";
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

const config = {
  // `settings` configures remark-stringify (the formatter that
  // `unified-prettier` runs on format-on-save) to match the lint rules
  // enforced by `remark-preset-lint-markdown-style-guide`. Without these,
  // Prettier emits `*` bullets while the linter wants `-` — fight on every
  // save.
  settings: {
    bullet: "-",
    emphasis: "*",
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
    [remarkLintListItemSpacing, false],
    // KB articles use numeric IDs (e.g. 000005784.mdx) and snake_case asset
    // names, both of which trip this rule.
    [remarkLintNoFileNameIrregularCharacters, false],
    // Mintlify uses `.mdx`, not `.md`.
    [remarkLintFileExtension, "mdx"],
    // KB filenames like `Domo-KB-Style-Guide.mdx` and `New-Article-Template.mdx`
    // are intentionally Title-Case-Kebab.
    [remarkLintNoFileNameMixedCase, false],
  ],
};

export default config;
