#!/usr/bin/env python3
"""
Tests for connector-review-gate.py — the pure, tooling-free pieces of the site-safety
gate (alt-text detection, case-collision grouping, docs.json validity). No framework:

    python3 scripts/test-connector-review-gate.py

Exits 0 when green, 1 on the first failure. Run after touching the alt-text regexes or
the case-collision logic — a mistake there would silently pass bad submissions.
"""

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "connector_review_gate", HERE / "connector-review-gate.py"
)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

_failures = []


def check(name, cond):
    print(f"{'ok  ' if cond else 'FAIL'} {name}")
    if not cond:
        _failures.append(name)


# --- alt-text detection ---------------------------------------------------- #

def alt(path, line):
    return gate._alt_offenders_in_lines(path, [line])

# Markdown images
check("md image with alt passes",
      alt("a.mdx", "![A chart of usage](/images/kb/x.png)") == [])
check("md image empty alt flagged",
      len(alt("a.mdx", "![](/images/kb/x.png)")) == 1)
check("md image whitespace alt flagged",
      len(alt("a.mdx", "![   ](/images/kb/x.png)")) == 1)

# JSX <img>
check("jsx img with alt passes",
      alt("a.mdx", '<img src="/x.png" alt="The settings panel" />') == [])
check("jsx img missing alt flagged",
      len(alt("a.mdx", '<img src="/x.png" style={{height:"1em"}} />')) == 1)
check("jsx img empty alt flagged",
      len(alt("a.mdx", '<img src="/x.png" alt="" />')) == 1)
check("jsx decorative icon aria-hidden exempt",
      alt("a.mdx", '<img src="/icon.png" aria-hidden="true" />') == [])
check("jsx img single-quoted alt passes",
      alt("a.mdx", "<img src='/x.png' alt='Dashboard view' />") == [])
check("two images on one line flagged twice",
      len(alt("a.mdx", "![](/a.png) and ![](/b.png)")) == 2)
check("prose with no image passes",
      alt("a.mdx", "This line mentions an image but has none.") == [])

# --- case collisions -------------------------------------------------------- #

check("no collisions on distinct paths",
      gate._collisions(["s/article/A.mdx", "s/article/B.mdx"]) == {})
check("collision detected on case-only difference",
      len(gate._collisions(["s/article/Foo.mdx", "s/article/foo.mdx"])) == 1)
check("unrelated casing variety is fine",
      gate._collisions(["Images/x.png", "docs.json", "README.md"]) == {})

# --- docs.json validity (uses the repo's real docs.json) -------------------- #

ok, msg = gate.check_docs_json_valid()
check("repo docs.json is valid JSON", ok)

# --- changed-file filtering helper is importable ---------------------------- #

check("CONTENT_PREFIXES covers article/topic/portal",
      gate.CONTENT_PREFIXES == ("s/article/", "s/topic/", "portal/"))


if _failures:
    print(f"\n{len(_failures)} failing: {', '.join(_failures)}")
    sys.exit(1)
print("\nAll gate tests passed.")
sys.exit(0)
