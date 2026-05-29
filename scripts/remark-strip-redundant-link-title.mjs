// Strip a Markdown link's title when it duplicates the link text. Migrated
// KB articles often shipped with `[Text](/url "Text")` patterns from the
// source CMS — the title adds nothing (renders as a tooltip identical to
// the visible label) and visually clutters source.
//
// Conservative: only removes the title when its whitespace-normalized form
// matches the link text's whitespace-normalized form. This catches the case
// where the source-wrapped link text (newline + indent between words) maps
// to the single-line title. Titles that differ semantically from the label
// are left alone, since they may be intentional.

export function remarkStripRedundantLinkTitle() {
  return (tree) => {
    walk(tree, (node) => {
      if (node.type !== "link") return;
      if (!node.title) return;
      if (normalize(linkText(node)) === normalize(node.title)) {
        node.title = null;
      }
    });
  };
}

function normalize(s) {
  return s.replace(/\s+/g, " ").trim();
}

function linkText(node) {
  let out = "";
  const collect = (n) => {
    if (!n) return;
    if (n.type === "text" && typeof n.value === "string") out += n.value;
    if (Array.isArray(n.children)) n.children.forEach(collect);
  };
  collect(node);
  return out;
}

function walk(node, visitor) {
  if (!node || typeof node !== "object") return;
  visitor(node);
  if (Array.isArray(node.children)) {
    for (const child of node.children) walk(child, visitor);
  }
}
