#!/usr/bin/env python3
"""Fail a pull request that introduces a broken link.

Scans the whole project twice — once at the base ref, once at HEAD — and fails
on findings present at HEAD but not at the base. The repo carries a large
backlog of pre-existing broken links, so an absolute threshold is useless; only
the difference matters.

Why scan everything rather than the changed files: nearly all of the runtime is
the CLI building its route table over the whole project, so a single-file scan
costs about as much as a full one. The two scans run concurrently, so the pair
costs little more than one. Scoping bought no time and cost correctness — it
missed renames, deletions, and docs.json changes, all of which break links in
files the pull request never touches, and pulling those files in by hand dragged
their unrelated pre-existing breakage into the report.

Why `mint broken-links` and not a generic link checker: Mintlify serves routes,
not files. It resolves extensionless paths, docs.json navigation, and the
/api-reference/* pages generated from the OpenAPI specs at build time. A
filesystem checker reports those generated pages as missing while also missing
real bugs like image paths whose case differs from the file on disk (fine on a
case-insensitive macOS working copy, 404 once published).

One class the CLI cannot see, so it is checked separately: a *bare* link target
(no leading "/", no "./") that also resolves from the site root. The CLI
resolves bare targets against the root and is satisfied; a browser resolves them
against the current page. So `](s/article/123)` written in portal/.../Guides/ is
accepted by the CLI and 404s in production. Diffing cannot help — the finding
never appears in either scan. (A bare target that is missing at the root too is
reported by the CLI normally.)

Usage:
  scripts/check-broken-links.py --base origin/main   # gate: new findings only
  scripts/check-broken-links.py --all                # every finding (triage)
  scripts/check-broken-links.py path/to/file.mdx ... # just these files

Exit codes: 0 = nothing new, 1 = new broken links, 2 = the check could not run.
"""

from __future__ import annotations

import argparse
import collections
import concurrent.futures
import os
import re
import shutil
import subprocess
import sys
import tempfile

MINT_BIN = "mint"

ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
TARGET_MARK = "⎿"
SUMMARY = re.compile(r"found (\d+) broken links? in (\d+) files?")


def die(message: str) -> None:
    """Exit 2 for a tooling failure, keeping exit 1 for real broken links."""
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


# --- running the CLI -------------------------------------------------------

def run_scan(cwd: str, files: list[str] | None = None) -> str:
    """Return the CLI's full report text.

    Output is collected through a real file, never a pipe: Node writes pipes
    asynchronously and this CLI exits before they flush, which silently
    truncates a long report. A short report means missed findings, so this
    matters — see the parse check in scan().
    """
    if not shutil.which(MINT_BIN):
        die(f"`{MINT_BIN}` not found. Install with "
            f"`PUPPETEER_SKIP_DOWNLOAD=1 npm install -g {MINT_BIN}`.")
    cmd = [MINT_BIN, "broken-links", "--check-anchors"]
    if files:
        cmd += ["--files", *files]
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "report.txt")
        with open(path, "w", encoding="utf-8") as sink:
            subprocess.run(cmd, cwd=cwd, stdout=sink, stderr=subprocess.STDOUT)
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()


def parse(text: str) -> collections.Counter:
    """Report text -> Counter of (source file, broken target).

    The report is a run of blank-line-separated blocks. Within a block the
    lines above the first marked line are the source path, and each marked line
    below it starts one broken target. The CLI hard-wraps its output and ignores
    COLUMNS, so a long source path and a long target both arrive split across
    lines; an unmarked line continues whatever preceded it, rejoined with no
    separator.

    The blank lines are the only reliable delimiter, which is why they are not
    simply skipped: mid-block, a wrapped source path and a wrapped target look
    alike, and guessing between them mis-attributes findings to files that do
    not exist.

    A Counter rather than a set because the same target can legitimately break
    twice in one file.
    """
    found: collections.Counter = collections.Counter()

    def flush(block: list[str]) -> None:
        marks = [i for i, line in enumerate(block) if TARGET_MARK in line]
        if not marks:
            return                  # a block naming no target is not a finding
        source = "".join(block[:marks[0]]).strip()
        if not source:
            return
        target = None
        for line in block[marks[0]:]:
            if TARGET_MARK in line:
                if target:
                    found[(source, target)] += 1
                target = line.split(TARGET_MARK, 1)[1].strip()
            else:
                target = (target or "") + line.strip()
        if target:
            found[(source, target)] += 1

    block: list[str] = []
    for raw in text.splitlines():
        line = ANSI.sub("", raw).lstrip(SPINNER).rstrip()
        if "checking for broken links" in line or line.startswith("found "):
            continue
        if not line:
            flush(block)
            block = []
            continue
        block.append(line)
    flush(block)
    return found


class ScanError(Exception):
    """A scan that cannot be trusted. Raised on a worker thread, handled above."""


def scan(cwd: str, label: str) -> tuple[collections.Counter, int, int]:
    """Scan `cwd` and verify the parse against the CLI's own summary.

    Raises rather than exiting, and prints nothing, because the two scans run
    concurrently on worker threads — interleaved output would be unreadable and
    SystemExit from a thread would not propagate.
    """
    text = run_scan(cwd)
    found = parse(text)
    claimed = SUMMARY.search(ANSI.sub("", text))
    if not claimed:
        raise ScanError(f"{label}: the scan produced no usable report:\n{text[:1500]}")
    want, want_files = int(claimed.group(1)), int(claimed.group(2))
    got = sum(found.values())
    got_files = len({f for f, _ in found})
    if (got, got_files) != (want, want_files):
        raise ScanError(
            f"{label}: parsed {got} findings in {got_files} files but the CLI "
            f"reported {want} in {want_files}. The report was captured "
            f"incompletely, so this run cannot be trusted to gate.")
    # Counts alone do not prove the parse: a mis-parse can preserve them while
    # attributing findings to the wrong file. Every source path must be real.
    missing = sorted({f for f, _ in found
                      if not os.path.exists(os.path.join(cwd, f))})
    if missing:
        raise ScanError(
            f"{label}: the report named {len(missing)} source file(s) that are "
            f"not on disk, so it was parsed wrongly and this run cannot be "
            f"trusted to gate: {', '.join(missing[:5])}")
    return found, want, want_files


# --- bare-path links, invisible to the CLI ---------------------------------

FENCE = re.compile(r"^([ \t]*)(```|~~~)[\s\S]*?^\1\2[ \t]*$", re.M)
INLINE_CODE = re.compile(r"`[^`\n]*`")
TARGETS = re.compile(r"\]\(\s*([^)\s]+)|\b(?:href|src)=\"([^\"]*)\"")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def bare_path_links(path: str) -> list[tuple[int, str]]:
    """(line, target) for each bare-path internal link in `path`."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return []
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))  # keep line numbers
    text = INLINE_CODE.sub(blank, FENCE.sub(blank, text))
    hits = []
    for m in TARGETS.finditer(text):
        t = (m.group(1) or m.group(2) or "").strip()
        if not t or t.startswith(("/", "#", "./", "../")) or SCHEME.match(t):
            continue
        hits.append((text.count("\n", 0, m.start()) + 1, t))
    return hits


def changed_mdx(base: str) -> list[str]:
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMR",
             f"{base}...HEAD", "--", "*.mdx"],
            capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError as exc:
        die(f"could not diff against {base}: {exc.stderr}")
    return [p for p in out.splitlines() if p.strip()]


def check_bare_paths(files: list[str]) -> int:
    found = [(f, ln, t) for f in files for ln, t in bare_path_links(f)]
    if not found:
        return 0
    print(f"\n{len(found)} internal link(s) missing a leading slash. A bare path "
          f"resolves against the current page's directory once published, not "
          f"the site root, so these 404 — and the link checker cannot see them:\n")
    for f, ln, t in found:
        print(f"  {f}:{ln}  ({t})  ->  (/{t})")
    return 1


# --- entry point -----------------------------------------------------------

def gate(base: str) -> int:
    """Scan base and HEAD, fail on findings that are new at HEAD."""
    with tempfile.TemporaryDirectory() as tmp:
        tree = os.path.join(tmp, "base")
        r = subprocess.run(["git", "worktree", "add", "--detach", tree, base],
                           capture_output=True, text=True)
        if r.returncode:
            die(f"could not create a worktree for {base}: {r.stderr}")
        try:
            # Run both scans at once. Each is a separate single-threaded
            # Node process and subprocess.run releases the GIL, so two threads
            # genuinely overlap.
            print(f"Scanning HEAD and {base} concurrently…")
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                fut_head = pool.submit(scan, os.getcwd(), "HEAD")
                fut_base = pool.submit(scan, tree, f"base ({base})")
                try:
                    head, hn, hf = fut_head.result()
                    baseline, bn, bf = fut_base.result()
                except ScanError as exc:
                    die(str(exc))
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", tree],
                           capture_output=True)
    print(f"HEAD: {hn} findings in {hf} files")
    print(f"base ({base}): {bn} findings in {bf} files")

    new = head - baseline          # Counter subtraction drops non-positives
    fixed = baseline - head
    if fixed:
        print(f"\n{sum(fixed.values())} finding(s) fixed by this branch. Nice.")
    if not new:
        print("\nNo new broken links.")
        return 0

    by_file: dict[str, list[str]] = collections.defaultdict(list)
    for (f, t), n in sorted(new.items()):
        by_file[f].extend([t] * n)
    print(f"\n{sum(new.values())} NEW broken link(s) in {len(by_file)} file(s):\n")
    for f in sorted(by_file):
        print(f)
        for t in by_file[f]:
            print(f"  {t}")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*", help="check only these files")
    ap.add_argument("--base", help="git ref to compare against, e.g. origin/main")
    ap.add_argument("--all", action="store_true", help="report every finding")
    args = ap.parse_args()

    if args.all:
        if args.base or args.files:
            ap.error("--all takes no files and no --base")
        try:
            found, n, nf = scan(os.getcwd(), "whole project")
        except ScanError as exc:
            die(str(exc))
        print(f"{n} findings in {nf} files\n")
        by_file: dict[str, list[str]] = collections.defaultdict(list)
        for (f, t), n in sorted(found.items()):
            by_file[f].extend([t] * n)
        for f in sorted(by_file):
            print(f)
            for t in by_file[f]:
                print(f"  {t}")
        return 0

    if args.files:
        if args.base:
            ap.error("give either --base REF or a list of files")
        text = run_scan(os.getcwd(), args.files)
        for line in text.splitlines():
            line = ANSI.sub("", line).lstrip(SPINNER).rstrip()
            if line and "checking for broken links" not in line:
                print(line)
        return max(1 if SUMMARY.search(ANSI.sub("", text)) else 0,
                   check_bare_paths(args.files))

    if not args.base:
        ap.error("one of --base, --all, or a list of files is required")

    # The bare-path check is scoped to changed files: diffing cannot catch this
    # class, since the CLI never reports it in either scan.
    return max(gate(args.base), check_bare_paths(changed_mdx(args.base)))


if __name__ == "__main__":
    sys.exit(main())
