#!/usr/bin/env python3
"""
apply_group_roots.py

Promote each group's Overview/hub article to a Mintlify **root page**
(https://www.mintlify.com/docs/organize/navigation#root-page): clicking the
group title in the sidebar opens that page, and the page is removed from the
group's child list (consolidation).

Two jobs:
  1. PROPOSE a group -> root-article map by scanning the English Knowledge Base
     tab of docs.json for each group's overview-type child.
  2. APPLY that map additively to docs.json: set "root" on the matching group
     node and drop the root page from its "pages" list. Nothing else in the nav
     is touched (safe to run mid-restructure, unlike the full build_docs_nav.py
     rebuild).

Resolution rule (per group, among its DIRECT string children):
  a. Prefer a modern restructure overview slug: "What-is-*" or "*-Overview"
     (non-numeric slug).  [these are the restructure's deliberate first child]
  b. else a child whose title == "<group> Overview".
  c. else the single overview-type child, if exactly one.
  If 0 candidates -> no root. If a tie remains -> prefer the first child.
A committed override map (scripts/group_roots.json, {"Pillar > Sub": "navpath"})
wins over the auto-proposal and can also force "none".

Guard: if promoting would empty a group's "pages", the promotion is SKIPPED and
reported (Mintlify groups need child pages alongside a root).

English KB tab only. Localized tabs (ja/fr/de/es) mirror this in Phase 6.

Usage:
  python3 -I scripts/apply_group_roots.py            # dry-run: print resolved map
  python3 -I scripts/apply_group_roots.py --apply     # write docs.json
  python3 -I scripts/apply_group_roots.py --json       # emit resolved map as JSON
"""

import json
import os
import re
import sys

DOCS_JSON = "docs.json"
OVERRIDES = "scripts/group_roots.json"


def title_of(navpath):
    fp = navpath + ".mdx"
    if not os.path.exists(fp):
        return None
    try:
        txt = open(fp, encoding="utf-8").read(3000)
    except OSError:
        return None
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', txt, re.M)
    return m.group(1).strip() if m else None


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def is_numeric_slug(slug):
    return bool(re.fullmatch(r"\d+", slug))


def resolve_root(gname, str_children):
    """Return the navpath to promote as this group's root, or None."""
    ng = norm(gname)
    modern = []   # (index, navpath)  non-numeric What-is-* / *-Overview
    titled = []   # (index, navpath)  title == "<group> Overview"
    any_ov = []   # (index, navpath)  any overview-type child
    for i, p in enumerate(str_children):
        slug = os.path.basename(p)
        t = title_of(p)
        sl = slug.lower()
        slug_ov = sl.startswith("what-is") or sl.endswith("-overview")
        title_ov = bool(t) and (t.lower().endswith("overview") or t.lower().startswith("what is"))
        if slug_ov and not is_numeric_slug(slug):
            modern.append((i, p))
        if t and norm(t) == ng + "overview":
            titled.append((i, p))
        if slug_ov or title_ov or "overview" in sl:
            any_ov.append((i, p))
    for bucket in (modern, titled, any_ov):
        if bucket:
            bucket.sort(key=lambda x: x[0])  # prefer first child on ties
            return bucket[0][1]
    return None


def walk(node, trail, out):
    """Collect (trail_key, node, str_children) for every group node."""
    if isinstance(node, dict) and "group" in node:
        gname = node["group"]
        key = " > ".join(trail + [gname])
        str_children = [p for p in node.get("pages", []) if isinstance(p, str)]
        out.append((key, node, str_children))
        for p in node.get("pages", []):
            if isinstance(p, dict):
                walk(p, trail + [gname], out)


def main():
    apply = "--apply" in sys.argv
    as_json = "--json" in sys.argv

    docs = json.load(open(DOCS_JSON, encoding="utf-8"))
    langs = docs["navigation"]["languages"]
    en = next((l for l in langs if l.get("language", "en") == "en"), langs[0])
    kb = next(t for t in en["tabs"] if t.get("tab") == "Knowledge Base")

    overrides = {}
    if os.path.exists(OVERRIDES):
        overrides = json.load(open(OVERRIDES, encoding="utf-8"))

    groups = []
    for g in kb.get("pages", []):
        walk(g, [], groups)

    resolved, skipped_empty, no_root = {}, [], []
    for key, node, str_children in groups:
        # Idempotent: an existing root is authoritative — leave it untouched so
        # re-runs (and a second Phase-7 run) are no-ops rather than promoting a
        # second overview from the now-rootless child list.
        if node.get("root"):
            resolved[key] = node["root"]
            continue
        # Archive is a holding area, not a curated pillar — never root its groups.
        if key.split(" > ", 1)[0] == "Archive":
            no_root.append(key)
            continue
        if key in overrides:
            root = overrides[key] or None  # explicit null/"" => force none
        else:
            root = resolve_root(node["group"], str_children)
        if not root:
            no_root.append(key)
            continue
        # Guard: don't empty the group.
        remaining = [p for p in node.get("pages", []) if not (isinstance(p, str) and p == root)]
        if not remaining:
            skipped_empty.append((key, root))
            continue
        resolved[key] = root

    if as_json:
        print(json.dumps(resolved, indent=2, ensure_ascii=False))
        return

    print(f"Groups scanned: {len(groups)}   roots resolved: {len(resolved)}")
    print(f"No overview child (left rootless): {len(no_root)}")
    if skipped_empty:
        print(f"SKIPPED (would empty group): {len(skipped_empty)}")
        for k, r in skipped_empty:
            print(f"    ! {k}  ->  {r}")
    print("\n--- Resolved root map ---")
    for key in sorted(resolved):
        t = title_of(resolved[key])
        print(f"  {key}\n      root = {resolved[key]}  ({t!r})")

    if not apply:
        print("\n(dry-run; re-run with --apply to write docs.json)")
        return

    changed = 0
    gmap = {k: n for k, n, _ in groups}
    for key, root in resolved.items():
        node = gmap[key]
        node["pages"] = [p for p in node.get("pages", []) if not (isinstance(p, str) and p == root)]
        node["root"] = root
        changed += 1

    with open(DOCS_JSON, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"\nApplied {changed} root pages. Wrote {DOCS_JSON}.")


if __name__ == "__main__":
    main()
