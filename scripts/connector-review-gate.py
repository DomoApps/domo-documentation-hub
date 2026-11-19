#!/usr/bin/env python3
"""
Connector-review site-safety gate.

This is the automated replacement for the human "won't break the site" check that
used to live in Jared's manual GitHub approval. The *content* of a connector PR is
approved by the secondary approver in the Jira ticket; this gate only answers the
narrower question Jared was answering by eye: does the submission render, follow the
repository's structural rules, and leave docs.json and the site's links intact?

It runs against a PR branch that is already checked out, comparing to a base ref
(default: origin/main). It prints a JSON summary to stdout and exits:

    0  every hard check passed  -> the connector-review flow may merge
    1  one or more hard checks failed -> do NOT merge; route to manual
    2  the gate itself could not run (tooling/environment failure)

Hard checks (any failure blocks the merge):
  - docs.json is valid JSON
  - docs.json navigation integrity: every page reference resolves to a real file,
    in every language (reuses DocStructureExtractor from docs_cli's export command)
  - MDX renderability: `remark` reports no FATAL (unparseable MDX/JSX) on changed files
  - no NEW broken internal links (reuses scripts/check-broken-links.py --base)
  - no case-colliding tracked paths (same rule as case-collision-check.yml)
  - every image ADDED by this branch carries non-empty alt text (repo standard;
    decorative icons marked aria-hidden="true" are exempt). Scoped to added lines so
    legacy images in unchanged files never block a merge.

Soft findings (reported, never block): Domo style-guide warnings from
remark-domo-style.mjs. These are auto-fixed by the skill's revise pass; whatever
remains is logged but does not break the site, so it does not gate the merge.

Usage:
    python3 scripts/connector-review-gate.py                 # base origin/main
    python3 scripts/connector-review-gate.py --base origin/main
    python3 scripts/connector-review-gate.py --json          # (default) JSON summary
"""

import argparse
import collections
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Content roots a connector PR is expected to touch. We validate MDX renderability
# and alt text only on these; docs.json / links / case-collision are repo-wide.
CONTENT_PREFIXES = ("s/article/", "s/topic/", "portal/")
LANGUAGES = ("en", "es", "fr", "de", "ja")


def _run(cmd, **kw):
    """Run a command from the repo root, capturing output."""
    return subprocess.run(
        cmd, cwd=REPO_ROOT, capture_output=True, text=True, **kw
    )


def changed_files(base):
    """Files changed on this branch vs. base (added/copied/modified/renamed; no deletions)."""
    res = _run(["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"])
    if res.returncode != 0:
        raise RuntimeError(f"git diff failed: {res.stderr.strip()}")
    return [f for f in res.stdout.splitlines() if f.strip()]


def added_lines(base, path):
    """The lines this branch ADDS to `path` (diff '+' lines, excluding the +++ header)."""
    res = _run(["git", "diff", f"{base}...HEAD", "--", path])
    if res.returncode != 0:
        return []
    out = []
    for line in res.stdout.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            out.append(line[1:])
    return out


# --------------------------------------------------------------------------- #
# Hard checks
# --------------------------------------------------------------------------- #

def check_docs_json_valid():
    """docs.json parses as JSON."""
    path = REPO_ROOT / "docs.json"
    if not path.exists():
        return True, "docs.json not present (nothing to validate)"
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True, "docs.json is valid JSON"
    except json.JSONDecodeError as e:
        return False, f"docs.json is not valid JSON: {e}"


def check_docs_json_nav_integrity():
    """Every page reference in docs.json resolves to a real file, in every language."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    try:
        from commands.export_structure import DocStructureExtractor
    except Exception as e:  # pragma: no cover - import/environment failure
        raise RuntimeError(f"could not import DocStructureExtractor: {e}")

    missing = []
    for lang in LANGUAGES:
        extractor = DocStructureExtractor(
            project_dir=REPO_ROOT, language=lang, base_url="https://docs.domo.com"
        )
        try:
            extractor.run()
        except ValueError:
            # Language block absent from docs.json; skip it.
            continue
        if extractor.stats["files_missing"]:
            for w in extractor.warnings:
                if w.startswith("File not found"):
                    missing.append(f"[{lang}] {w}")

    if missing:
        detail = "; ".join(missing[:15])
        if len(missing) > 15:
            detail += f" (+{len(missing) - 15} more)"
        return False, f"docs.json references {len(missing)} missing page(s): {detail}"
    return True, "docs.json nav: every page reference resolves to a file"


def _remark_bin():
    local = REPO_ROOT / "node_modules" / ".bin" / "remark"
    if local.exists():
        return [str(local)]
    if shutil.which("yarn"):
        return ["yarn", "--silent", "remark"]
    if shutil.which("npx"):
        return ["npx", "--no-install", "remark"]
    return None


def check_mdx_renderable(files):
    """`remark` reports no FATAL error on the changed MDX files (unparseable MDX/JSX)."""
    mdx = [f for f in files if f.endswith(".mdx") and (REPO_ROOT / f).exists()]
    if not mdx:
        return True, "no changed MDX files to parse"

    binary = _remark_bin()
    if binary is None:
        raise RuntimeError("remark not available (run `yarn install`)")

    # remark-cli exits non-zero only on FATAL messages (not warnings) when --frail
    # is omitted, so a non-zero return here means a genuine parse/render failure.
    res = _run(binary + mdx + ["--no-stdout", "--quiet"])
    if res.returncode == 0:
        return True, f"remark parsed {len(mdx)} MDX file(s) with no fatal errors"
    # --quiet keeps only fatals on stderr.
    detail = (res.stderr or res.stdout).strip().splitlines()
    detail = " | ".join(detail[-8:]) if detail else "see remark output"
    return False, f"MDX fails to parse/render: {detail}"


def check_no_new_broken_links(base):
    """No internal links broken BY this branch (reuses check-broken-links.py gate mode)."""
    script = REPO_ROOT / "scripts" / "check-broken-links.py"
    if not script.exists():
        raise RuntimeError("scripts/check-broken-links.py not found")
    res = _run([sys.executable, str(script), "--base", base])
    if res.returncode == 0:
        return True, "no new broken internal links"
    if res.returncode == 2:
        raise RuntimeError(
            f"broken-link checker could not run: {(res.stderr or res.stdout).strip()[:300]}"
        )
    detail = (res.stdout or res.stderr).strip().splitlines()
    detail = " | ".join(detail[-10:]) if detail else "see checker output"
    return False, f"new broken link(s): {detail}"


def _collisions(paths):
    """Groups of tracked paths that differ only by case (pure; testable)."""
    by_lower = collections.defaultdict(list)
    for p in paths:
        by_lower[p.lower()].append(p)
    return {k: v for k, v in by_lower.items() if len(v) > 1}


def check_no_case_collisions():
    """No two tracked paths differ only by case (same rule as case-collision-check.yml)."""
    res = _run(["git", "ls-files"])
    if res.returncode != 0:
        raise RuntimeError(f"git ls-files failed: {res.stderr.strip()}")
    colliders = _collisions(res.stdout.splitlines())
    if not colliders:
        return True, "no case-colliding tracked paths"
    sample = "; ".join(" / ".join(sorted(v)) for v in list(colliders.values())[:5])
    return False, f"{len(colliders)} case-colliding path group(s): {sample}"


# Image syntaxes: Markdown ![alt](src) and JSX <img ... />
_MD_IMG = re.compile(r"!\[(?P<alt>[^\]]*)\]\([^)]*\)")
_JSX_IMG = re.compile(r"<img\b[^>]*?/?>", re.IGNORECASE)
_ALT_ATTR = re.compile(r'\balt\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|\{[^}]*\})', re.IGNORECASE)
_ARIA_HIDDEN = re.compile(r'aria-hidden\s*=\s*(?:"true"|\'true\'|\{true\})', re.IGNORECASE)


def _alt_offenders_in_lines(path, lines):
    """Image references on `lines` that lack alt text, aria-hidden icons exempt (pure; testable)."""
    offenders = []
    for line in lines:
        for m in _MD_IMG.finditer(line):
            if not m.group("alt").strip():
                offenders.append(f"{path}: Markdown image with empty alt")
        for m in _JSX_IMG.finditer(line):
            tag = m.group(0)
            if _ARIA_HIDDEN.search(tag):
                continue  # decorative icon, correctly marked
            alt = _ALT_ATTR.search(tag)
            if not alt or not ((alt.group(1) or alt.group(2) or "").strip()):
                offenders.append(f"{path}: <img> with missing/empty alt")
    return offenders


def check_added_images_have_alt(base, files):
    """Every image this branch ADDS carries non-empty alt text (aria-hidden icons exempt)."""
    offenders = []
    content_mdx = [
        f for f in files
        if f.endswith(".mdx") and f.startswith(CONTENT_PREFIXES) and (REPO_ROOT / f).exists()
    ]
    for f in content_mdx:
        offenders.extend(_alt_offenders_in_lines(f, added_lines(base, f)))
    if offenders:
        detail = "; ".join(offenders[:10])
        if len(offenders) > 10:
            detail += f" (+{len(offenders) - 10} more)"
        return False, f"{len(offenders)} newly added image(s) lack alt text: {detail}"
    return True, "all newly added images carry alt text"


# --------------------------------------------------------------------------- #
# Soft check (reported, never blocks)
# --------------------------------------------------------------------------- #

def style_warnings(files):
    """Count remark style warnings (non-fatal) on changed MDX. Informational only."""
    mdx = [f for f in files if f.endswith(".mdx") and (REPO_ROOT / f).exists()]
    binary = _remark_bin()
    if not mdx or binary is None:
        return 0, ""
    res = _run(binary + mdx + ["--no-stdout"])
    warns = [l for l in (res.stderr or "").splitlines() if " warning " in l]
    return len(warns), "\n".join(warns[-20:])


# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="origin/main",
                    help="git ref to compare against (default: origin/main)")
    args = ap.parse_args()

    try:
        files = changed_files(args.base)
    except RuntimeError as e:
        print(json.dumps({"passed": False, "error": str(e)}, indent=2))
        return 2

    hard_checks = [
        ("docs_json_valid", check_docs_json_valid, ()),
        ("docs_json_nav_integrity", check_docs_json_nav_integrity, ()),
        ("mdx_renderable", check_mdx_renderable, (files,)),
        ("no_new_broken_links", check_no_new_broken_links, (args.base,)),
        ("no_case_collisions", check_no_case_collisions, ()),
        ("added_images_have_alt", check_added_images_have_alt, (args.base, files)),
    ]

    results = {}
    failures = []
    try:
        for name, fn, fargs in hard_checks:
            ok, msg = fn(*fargs)
            results[name] = {"passed": ok, "detail": msg}
            if not ok:
                failures.append(f"{name}: {msg}")
    except RuntimeError as e:
        print(json.dumps({"passed": False, "tooling_error": str(e),
                          "checks": results}, indent=2))
        return 2

    warn_count, warn_sample = style_warnings(files)

    summary = {
        "passed": not failures,
        "base": args.base,
        "changed_files": len(files),
        "checks": results,
        "failures": failures,
        "style_warnings": {"count": warn_count, "sample": warn_sample},
    }
    print(json.dumps(summary, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
