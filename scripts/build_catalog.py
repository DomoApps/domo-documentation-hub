#!/usr/bin/env python3
"""
Build a machine-readable catalog of all articles in s/article/.

Extracts frontmatter (title, excerpt, tags), classifies each article's
filename scheme, counts lines, and cross-references docs.json to find
the nav group each article belongs to.

Usage:
    python scripts/build_catalog.py [--article-dir s/article] [--out scripts/output/catalog.json]

Output: scripts/output/catalog.json
Schema per entry:
{
  "filename":      "360042925394.mdx",
  "path":          "s/article/360042925394.mdx",
  "title":         "Properties for Miscellaneous Charts",
  "excerpt":       "Reference chart properties for ...",
  "tags":          ["Beta"],
  "line_count":    412,
  "id_scheme":     "zendesk" | "domo" | "long_numeric" | "slug",
  "nav_group":     "Analyze & Visualize > Charts",   # deepest nav group that contains the article, or null
  "in_nav":        true | false
}
"""

import argparse
import json
import os
import re
import sys

ARTICLE_DIR = "s/article"
DOCS_JSON = "docs.json"
OUTPUT = "scripts/output/catalog.json"


# ---------------------------------------------------------------------------
# Filename classification
# ---------------------------------------------------------------------------

def classify_id_scheme(filename: str) -> str:
    stem = os.path.splitext(filename)[0]
    if re.fullmatch(r"360\d{9,}", stem):
        return "zendesk"
    if re.fullmatch(r"0{2,}\d+", stem):
        return "domo"
    if re.fullmatch(r"\d{10,}", stem):
        return "long_numeric"
    return "slug"


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter fields we care about (title, excerpt, tag/tags)."""
    result = {"title": None, "excerpt": None, "tags": []}

    # Find the frontmatter block
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return result

    fm = m.group(1)

    # title
    tm = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', fm, re.MULTILINE)
    if tm:
        result["title"] = tm.group(1).strip().strip('"\'')

    # excerpt
    em = re.search(r'^excerpt:\s*["\']?(.*?)["\']?\s*$', fm, re.MULTILINE)
    if em:
        result["excerpt"] = em.group(1).strip().strip('"\'')

    # tag / tags (scalar or list)
    tag_scalar = re.search(r'^tag:\s*["\']?(.*?)["\']?\s*$', fm, re.MULTILINE)
    tags_list = re.findall(r'^\s*-\s*["\']?(.*?)["\']?\s*$', fm, re.MULTILINE)

    if tag_scalar:
        val = tag_scalar.group(1).strip().strip('"\'')
        if val:
            result["tags"].append(val)
    if tags_list:
        result["tags"].extend([t for t in tags_list if t])

    return result


# ---------------------------------------------------------------------------
# docs.json nav traversal
# ---------------------------------------------------------------------------

def build_nav_map(docs_json_path: str) -> dict[str, str]:
    """
    Return {article_path_stem: deepest_nav_group_label} by recursively
    walking the docs.json navigation tree.

    Mintlify docs.json structure (this repo):
      navigation.languages[i].tabs[j].pages → list of groups or strings
      group: {group: "Label", pages: [...]}
      leaf: "s/article/slug"

    article_path_stem examples:
      "s/article/360042925394"
      "s/article/Getting-Started-for-Data-Consumers"
    """
    if not os.path.exists(docs_json_path):
        return {}

    with open(docs_json_path, encoding="utf-8") as f:
        data = json.load(f)

    nav_map: dict[str, str] = {}

    def walk_pages(pages, breadcrumb: str):
        for node in pages:
            if isinstance(node, str):
                stem = node.rstrip("/")
                nav_map[stem] = breadcrumb
            elif isinstance(node, dict):
                label = node.get("group") or node.get("tab") or ""
                crumb = f"{breadcrumb} > {label}" if (breadcrumb and label) else (label or breadcrumb)
                sub = node.get("pages", [])
                if isinstance(sub, list):
                    walk_pages(sub, crumb)

    # Entry point: navigation.languages[*].tabs[*].pages
    nav = data.get("navigation", {})
    for lang_entry in nav.get("languages", []):
        lang_label = lang_entry.get("language", "")
        for tab in lang_entry.get("tabs", []):
            tab_label = tab.get("tab", "")
            crumb = f"{lang_label} > {tab_label}" if lang_label else tab_label
            walk_pages(tab.get("pages", []), crumb)

    return nav_map


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Build KB article catalog")
    parser.add_argument("--article-dir", default=ARTICLE_DIR)
    parser.add_argument("--docs-json", default=DOCS_JSON)
    parser.add_argument("--out", default=OUTPUT)
    args = parser.parse_args()

    article_dir = args.article_dir
    if not os.path.isdir(article_dir):
        sys.exit(f"Article directory not found: {article_dir}")

    print(f"Building nav map from {args.docs_json}…", flush=True)
    nav_map = build_nav_map(args.docs_json)
    print(f"  Nav map entries: {len(nav_map)}", flush=True)

    files = sorted(f for f in os.listdir(article_dir) if f.endswith(".mdx"))
    print(f"Processing {len(files)} articles in {article_dir}…", flush=True)

    catalog = []
    missing_nav = 0

    for i, filename in enumerate(files, 1):
        path = os.path.join(article_dir, filename)

        with open(path, encoding="utf-8") as f:
            text = f.read()

        lines = text.splitlines()
        fm = parse_frontmatter(text)
        stem = os.path.splitext(filename)[0]
        article_key = f"{article_dir}/{stem}"

        nav_group = nav_map.get(article_key)
        if nav_group is None:
            missing_nav += 1

        entry = {
            "filename": filename,
            "path": path.replace("\\", "/"),
            "title": fm["title"],
            "excerpt": fm["excerpt"],
            "tags": fm["tags"],
            "line_count": len(lines),
            "id_scheme": classify_id_scheme(filename),
            "nav_group": nav_group,
            "in_nav": nav_group is not None,
        }
        catalog.append(entry)

        if i % 200 == 0:
            print(f"  {i}/{len(files)}…", flush=True)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    # Summary
    schemes = {}
    for e in catalog:
        schemes[e["id_scheme"]] = schemes.get(e["id_scheme"], 0) + 1

    print(f"\nDone. {len(catalog)} articles → {args.out}")
    print(f"  In nav:      {len(catalog) - missing_nav}")
    print(f"  Orphaned:    {missing_nav}")
    print(f"  ID schemes:  {schemes}")
    missing_title = sum(1 for e in catalog if not e["title"])
    missing_excerpt = sum(1 for e in catalog if not e["excerpt"])
    print(f"  Missing title:   {missing_title}")
    print(f"  Missing excerpt: {missing_excerpt}")


if __name__ == "__main__":
    main()
