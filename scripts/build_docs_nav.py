#!/usr/bin/env python3
"""
build_docs_nav.py

Phase 2 script: Rebuilds the English Knowledge Base tab in docs.json using the
11-pillar IA structure from ia-mapping.json.

What it does:
  - Reads scripts/output/ia-mapping.json  (article → {pillar, group, sub_group})
  - Reads scripts/output/catalog.json     (article → full path like s/article/foo.mdx)
  - Builds 11 pillar groups, each with nested sub-groups where applicable
  - Appends an Archive group at the bottom
  - Replaces the Knowledge Base tab pages in docs.json (English only)
  - All other tabs (Developer Portal, Release Notes) and all localized tabs are untouched
  - Writes updated docs.json in-place

Usage:
  python3 scripts/build_docs_nav.py [--dry-run]

  --dry-run   Print the generated KB groups as JSON instead of writing docs.json.
"""

import json
import sys
import os
from collections import defaultdict, OrderedDict

IA_MAPPING = "scripts/output/ia-mapping.json"
CATALOG = "scripts/output/catalog.json"
DOCS_JSON = "docs.json"

# Pillar display order (Archive always last)
PILLAR_ORDER = [
    "Getting Started",
    "Connect & Bring In Data",
    "Manage Data",
    "Prepare & Transform Data",
    "Analyze & Visualize",
    "Build Apps & Automate",
    "Share & Collaborate",
    "AI & Data Science",
    "Administer & Govern",
    "Develop & Integrate",
    "Release Notes",
    "Archive",
]


def load_path_map(catalog_path):
    """Build filename → nav path (without .mdx) from catalog.json."""
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    path_map = {}
    for item in catalog:
        filename = item["filename"]
        full_path = item["path"]  # e.g. s/article/000003989.mdx
        nav_path = full_path.removesuffix(".mdx")
        path_map[filename] = nav_path
    return path_map


def build_pillar_groups(ia_mapping, path_map):
    """
    Build {pillar: {group: {sub_group: [nav_paths]}}} from ia-mapping.

    Articles with no sub_group go into a flat list under the group.
    Articles whose path is unknown (not in path_map) are skipped with a warning.
    """
    # pillar → group → sub_group → [nav_path]
    # Use "_flat" as the key for articles with no sub_group
    tree = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    skipped = 0

    for filename, data in ia_mapping.items():
        pillar = data.get("pillar", "Archive")
        group = data.get("group", "General")
        sub_group = data.get("sub_group") or "_flat"

        nav_path = path_map.get(filename)
        if not nav_path:
            skipped += 1
            continue

        tree[pillar][group][sub_group].append(nav_path)

    if skipped:
        print(f"  Warning: {skipped} articles skipped (not found in catalog path map)",
              file=sys.stderr)

    return tree


def sort_pages(pages):
    """Sort page paths alphabetically for deterministic output."""
    return sorted(pages)


def build_group_node(group_name, sub_groups):
    """
    Build a docs.json group node from a group's sub_groups dict.

    If there's only a _flat bucket (no sub-groups), emit a flat group.
    If there are named sub-groups (with or without _flat), emit nested groups.
    """
    named = {k: v for k, v in sub_groups.items() if k != "_flat"}
    flat = sub_groups.get("_flat", [])

    if not named:
        # All articles are flat — single group node
        return {
            "group": group_name,
            "pages": sort_pages(flat),
        }
    else:
        # Has sub-groups — nested structure
        pages = []
        # Flat articles at the top of the group (if any)
        if flat:
            pages.extend(sort_pages(flat))
        # Then named sub-groups, sorted alphabetically
        for sub_name in sorted(named.keys()):
            pages.append({
                "group": sub_name,
                "pages": sort_pages(named[sub_name]),
            })
        return {
            "group": group_name,
            "pages": pages,
        }


def build_kb_pages(tree):
    """
    Convert the pillar tree into the docs.json pages array for the KB tab.

    Returns a list of group nodes in PILLAR_ORDER, with Archive last.
    Each pillar becomes a top-level group node.
    Each group within a pillar becomes a nested group within that pillar.
    """
    kb_pages = []

    for pillar in PILLAR_ORDER:
        if pillar not in tree:
            continue

        groups = tree[pillar]
        pillar_pages = []

        # Sort groups alphabetically within each pillar
        for group_name in sorted(groups.keys()):
            node = build_group_node(group_name, groups[group_name])
            pillar_pages.append(node)

        pillar_node = {
            "group": pillar,
            "pages": pillar_pages,
        }
        kb_pages.append(pillar_node)

    # Any pillars not in PILLAR_ORDER (shouldn't happen, but defensive)
    unknown = [p for p in tree if p not in PILLAR_ORDER]
    for pillar in sorted(unknown):
        print(f"  Warning: pillar '{pillar}' not in PILLAR_ORDER — appending at end",
              file=sys.stderr)
        groups = tree[pillar]
        pillar_pages = [build_group_node(g, tree[pillar][g]) for g in sorted(groups.keys())]
        kb_pages.append({"group": pillar, "pages": pillar_pages})

    return kb_pages


def count_pages(pages):
    """Recursively count flat page strings in a pages array."""
    count = 0
    for p in pages:
        if isinstance(p, str):
            count += 1
        elif isinstance(p, dict):
            count += count_pages(p.get("pages", []))
    return count


def main():
    dry_run = "--dry-run" in sys.argv

    print("Loading ia-mapping.json...")
    with open(IA_MAPPING, "r", encoding="utf-8") as f:
        ia_mapping = json.load(f)
    print(f"  {len(ia_mapping)} articles in mapping")

    print("Loading catalog.json for path resolution...")
    path_map = load_path_map(CATALOG)
    print(f"  {len(path_map)} articles with resolved paths")

    print("Building pillar tree...")
    tree = build_pillar_groups(ia_mapping, path_map)
    for pillar in PILLAR_ORDER:
        if pillar in tree:
            n = sum(
                len(arts)
                for group in tree[pillar].values()
                for arts in group.values()
            )
            print(f"  {pillar}: {n} articles, {len(tree[pillar])} groups")

    print("Building KB tab pages array...")
    kb_pages = build_kb_pages(tree)
    total = count_pages(kb_pages)
    print(f"  {len(kb_pages)} top-level pillar groups, {total} total page references")

    if dry_run:
        print("\n--- DRY RUN: generated KB pages (JSON) ---")
        print(json.dumps(kb_pages, indent=2))
        return

    print(f"Loading {DOCS_JSON}...")
    with open(DOCS_JSON, "r", encoding="utf-8") as f:
        docs = json.load(f)

    # Find English KB tab and replace its pages
    languages = docs["navigation"]["languages"]
    en_lang = next((l for l in languages if l.get("language", "en") == "en"), None)
    if en_lang is None:
        # First language entry is English (no explicit language key)
        en_lang = languages[0]

    tabs = en_lang.get("tabs", [])
    kb_tab = next((t for t in tabs if t.get("tab") == "Knowledge Base"), None)
    if kb_tab is None:
        print("ERROR: Could not find 'Knowledge Base' tab in English navigation",
              file=sys.stderr)
        sys.exit(1)

    old_count = count_pages(kb_tab.get("pages", []))
    kb_tab["pages"] = kb_pages
    new_count = count_pages(kb_tab["pages"])

    print(f"  Replaced KB tab: {old_count} → {new_count} page references")

    print(f"Writing {DOCS_JSON}...")
    with open(DOCS_JSON, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("Done.")


if __name__ == "__main__":
    main()
