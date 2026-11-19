#!/usr/bin/env python3
"""
Regenerate the docs.json navigation for OpenAPI specs in openapi/product/.

Each spec becomes one group under "Product APIs" in the Developer Portal tab:

    {
        "group": "<info.title>",
        "pages": [
            {"group": "<tag>", "pages": ["openapi/product/<file>.yaml GET /path", ...]},
            ...
        ]
    }

Rules (the same as DomoApps/documentation-generator-action, which this
replaces, so existing nav doesn't move), except where noted:
  - group name is the spec's info.title
  - the existing group is the one whose pages point at the spec's file (the
    action matched by title, so a retitled spec got a second group); it is
    rebuilt in place, and a new group is inserted alphabetically
  - a rebuild keeps the pages the spec doesn't own, such as hand-added overview
    pages, ahead of the generated ones (the action dropped them)
  - subgroups are each operation's first tag (or "Untagged"), sorted by name
  - pages inside a subgroup are sorted by HTTP method, then path
  - a spec with exactly one tag matching its title (case-insensitive) is
    flattened: its pages go directly under the group

docs.json is written back as standard 2-space JSON (json.dumps, indent=2), the
format the file is in today, so only nav entries change. (The action collapsed
single-value arrays onto one line, which reformatted the whole file.)

Usage:
    python update_api_nav.py --docs-json ./docs.json openapi/product/Documents.yaml ...
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

import yaml

HTTP_METHODS = ["get", "post", "put", "delete", "patch", "options", "head"]


def build_group(yaml_path: str, openapi_base_path: str) -> Dict[str, Any]:
    """Build the nav group for one spec."""
    with open(yaml_path, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f) or {}

    title = (spec.get("info") or {}).get("title", "API")
    filename = os.path.basename(yaml_path)

    # first tag -> [(method, path)], in spec order
    by_tag: Dict[str, List[tuple]] = {}
    for path, path_item in (spec.get("paths") or {}).items():
        if not isinstance(path_item, dict):
            continue
        for method in HTTP_METHODS:
            operation = path_item.get(method)
            if not isinstance(operation, dict):
                continue
            tags = operation.get("tags") or []
            tag = tags[0] if tags else "Untagged"
            by_tag.setdefault(tag, []).append((method.upper(), path))

    def pages_for(endpoints: List[tuple]) -> List[str]:
        return [f"{openapi_base_path}/{filename} {method} {path}" for method, path in sorted(endpoints)]

    tags = list(by_tag)
    if len(tags) == 1 and tags[0].lower() == title.lower():
        return {"group": title, "pages": pages_for(by_tag[tags[0]])}
    return {
        "group": title,
        "pages": [{"group": tag, "pages": pages_for(by_tag[tag])} for tag in sorted(tags)],
    }


def find_group(node: Any, name: str) -> Optional[Dict[str, Any]]:
    """Depth-first search for the first dict with group == name."""
    if isinstance(node, dict):
        if node.get("group") == name:
            return node
        children = node.values()
    elif isinstance(node, list):
        children = node
    else:
        return None
    for child in children:
        found = find_group(child, name)
        if found is not None:
            return found
    return None


def find_product_apis_pages(docs: Dict[str, Any], language: str = "en") -> Optional[List[Any]]:
    """The pages list of the "Product APIs" group in the Developer Portal tab."""
    languages = (docs.get("navigation") or {}).get("languages", [])
    if isinstance(languages, dict):
        lang = languages.get(language)
    else:
        lang = next((l for l in languages if isinstance(l, dict) and l.get("language") == language), None)
    if not lang:
        return None
    tab = next((t for t in lang.get("tabs", []) if isinstance(t, dict) and t.get("tab") == "Developer Portal"), None)
    if not tab:
        return None
    # Searched rather than addressed by path: the group has moved as the nav was restructured
    product_apis = find_group(tab, "Product APIs")
    if product_apis is None:
        return None
    return product_apis.setdefault("pages", [])


def references_file(node: Any, file_prefix: str) -> bool:
    """Whether any page string under node is an endpoint page of this spec."""
    if isinstance(node, str):
        return node.startswith(file_prefix)
    if isinstance(node, dict):
        return references_file(node.get("pages", []), file_prefix)
    if isinstance(node, list):
        return any(references_file(item, file_prefix) for item in node)
    return False


def without_file_pages(pages: List[Any], file_prefix: str) -> List[Any]:
    """The pages a rebuild must keep: everything except this spec's endpoint pages.

    That's hand-added pages (overviews, guides) and endpoints of other specs.
    Subgroups left empty once this spec's pages are removed are dropped.
    """
    kept: List[Any] = []
    for item in pages:
        if isinstance(item, str):
            if not item.startswith(file_prefix):
                kept.append(item)
        elif isinstance(item, dict) and isinstance(item.get("pages"), list):
            sub = without_file_pages(item["pages"], file_prefix)
            if sub or not references_file(item, file_prefix):
                kept.append({**item, "pages": sub})
        else:
            kept.append(item)
    return kept


def merge_kept(existing: Dict[str, Any], group: Dict[str, Any], file_prefix: str) -> Dict[str, Any]:
    """The rebuilt group, with the pages the old group had that this spec doesn't own.

    Kept pages go first, in their old order. A kept subgroup with the same name
    as a generated tag subgroup is folded into it, its pages ahead of the
    endpoints.
    """
    generated = group["pages"]
    tag_groups = {p["group"]: p for p in generated if isinstance(p, dict)}
    front: List[Any] = []
    for item in without_file_pages(existing.get("pages", []), file_prefix):
        if isinstance(item, dict) and item.get("group") in tag_groups:
            target = tag_groups[item["group"]]
            target["pages"] = item["pages"] + target["pages"]
        else:
            front.append(item)
    return {**existing, "group": group["group"], "pages": front + generated}


def insert_or_replace(pages: List[Any], group: Dict[str, Any], file_prefix: str) -> None:
    """Rebuild the spec's group in place, or insert it alphabetically if it's new.

    The existing group is the one whose pages point at this spec's file, so a
    renamed spec (new info.title) replaces its old group instead of adding a
    second one. A group with no endpoint pages yet is matched by title.
    """
    name = group["group"]
    match = next((i for i, p in enumerate(pages) if isinstance(p, dict) and references_file(p, file_prefix)), None)
    if match is None:
        match = next((i for i, p in enumerate(pages) if isinstance(p, dict) and p.get("group") == name), None)
    if match is not None:
        pages[match] = merge_kept(pages[match], group, file_prefix)
        return
    index = len(pages)
    for i, page in enumerate(pages):
        if isinstance(page, dict) and "group" in page and name.lower() < page["group"].lower():
            index = i
            break
    pages.insert(index, group)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--docs-json", required=True, help="Path to docs.json")
    parser.add_argument("--openapi-base-path", default="openapi/product",
                        help="Prefix for page strings (default: openapi/product)")
    parser.add_argument("yaml_files", nargs="+", help="OpenAPI YAML files to (re)generate nav for")
    args = parser.parse_args()

    with open(args.docs_json, "r", encoding="utf-8") as f:
        docs = json.load(f)

    pages = find_product_apis_pages(docs)
    if pages is None:
        print("::error::Product APIs group not found in the Developer Portal tab of docs.json")
        return 1

    base = args.openapi_base_path.rstrip("/")
    for yaml_path in sorted(args.yaml_files):
        group = build_group(yaml_path, base)
        count = sum(len(p["pages"]) if isinstance(p, dict) else 1 for p in group["pages"])
        print(f"{yaml_path}: '{group['group']}', {count} endpoint(s)")
        insert_or_replace(pages, group, f"{base}/{os.path.basename(yaml_path)} ")

    with open(args.docs_json, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
