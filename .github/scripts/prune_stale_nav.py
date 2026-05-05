#!/usr/bin/env python3
"""
Remove OpenAPI nav entries from docs.json that point at YAML files which
no longer exist on disk.

Mintlify references OpenAPI operations as page strings like:
    "openapi/product/filesets.yaml GET /api/files/v1/filesets"

If the referenced YAML has been removed or renamed (including case-only
renames on a case-sensitive filesystem), Mintlify's preview deploy fails.
This script walks docs.json, drops page strings whose YAML is missing,
and prunes any groups that become empty as a result.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, List, Tuple

# Matches a Mintlify OpenAPI page entry. Captures the YAML path.
OPENAPI_PAGE_RE = re.compile(r"^(?P<yaml>[^\s]+\.ya?ml)\s+[A-Z]+\s+/")


_dir_cache: dict = {}


def yaml_exists(yaml_path: str, repo_root: str) -> bool:
    """Does the YAML referenced by an OpenAPI page entry exist on disk?

    Uses an explicit case-sensitive check against os.listdir() rather than
    os.path.isfile(), because the dev repo is typically on a case-insensitive
    filesystem (macOS APFS) while GitHub Actions and Mintlify preview run on
    case-sensitive Linux. A stale `Filesets.yaml` reference must be pruned
    even when the disk only has `filesets.yaml`.
    """
    dir_part, file_part = os.path.split(yaml_path)
    abs_dir = os.path.join(repo_root, dir_part)
    if abs_dir not in _dir_cache:
        try:
            _dir_cache[abs_dir] = set(os.listdir(abs_dir))
        except FileNotFoundError:
            _dir_cache[abs_dir] = set()
    return file_part in _dir_cache[abs_dir]


def prune_pages(pages: List[Any], repo_root: str, dropped: List[str]) -> List[Any]:
    """Filter a `pages` array: drop dangling OpenAPI strings, recurse into groups.
    Empty groups are left intact — they may have been authored empty on purpose,
    and Mintlify tolerates them. Only dangling OpenAPI page strings are removed.
    """
    kept: List[Any] = []
    for item in pages:
        if isinstance(item, str):
            m = OPENAPI_PAGE_RE.match(item)
            if m and not yaml_exists(m.group("yaml"), repo_root):
                dropped.append(item)
                continue
            kept.append(item)
        elif isinstance(item, dict):
            kept.append(prune_node(item, repo_root, dropped))
        else:
            kept.append(item)
    return kept


def prune_node(node: dict, repo_root: str, dropped: List[str]) -> dict:
    """Recurse into any node that may contain a `pages` array."""
    if "pages" in node and isinstance(node["pages"], list):
        node["pages"] = prune_pages(node["pages"], repo_root, dropped)
    # Mintlify nests structures under tabs/groups/anchors/dropdowns/languages.
    for key in ("tabs", "groups", "anchors", "dropdowns", "languages"):
        if key in node and isinstance(node[key], list):
            node[key] = [
                prune_node(child, repo_root, dropped) if isinstance(child, dict) else child
                for child in node[key]
            ]
    return node


def walk_and_prune(doc: dict, repo_root: str) -> Tuple[dict, List[str]]:
    dropped: List[str] = []
    if "navigation" in doc and isinstance(doc["navigation"], dict):
        doc["navigation"] = prune_node(doc["navigation"], repo_root, dropped)
    return doc, dropped


def main():
    parser = argparse.ArgumentParser(description="Prune stale OpenAPI nav entries from docs.json")
    parser.add_argument("--docs-json", default="./docs.json", help="Path to docs.json")
    parser.add_argument("--repo-root", default=".", help="Repo root (for resolving YAML paths)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report stale entries without writing changes (exit 1 if any found).",
    )
    args = parser.parse_args()

    with open(args.docs_json, "r") as f:
        doc = json.load(f)

    doc, dropped = walk_and_prune(doc, args.repo_root)

    if not dropped:
        print("No stale OpenAPI nav entries found.")
        return

    print(f"Pruned {len(dropped)} stale entries:")
    for d in dropped:
        print(f"  - {d}")

    if args.check:
        sys.exit(1)

    with open(args.docs_json, "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
    print(f"Wrote pruned docs.json to {args.docs_json}")


if __name__ == "__main__":
    main()
