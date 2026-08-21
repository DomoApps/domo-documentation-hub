#!/usr/bin/env python3
"""Tests for check-broken-links.py. Run: python3 scripts/test-check-broken-links.py

No test framework, so there is nothing to install. Exits 0 when green.

The parser tests matter more than they look: a mis-parse does not fail loudly,
it silently mis-attributes a finding, and the gate then names a file that does
not exist or reports a target that was never written.
"""

import collections
import importlib.util
import os
import pathlib
import sys
import tempfile
import textwrap

_HERE = pathlib.Path(__file__).resolve().parent


def _load():
    spec = importlib.util.spec_from_file_location(
        "lc", _HERE / "check-broken-links.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lc = _load()
M = lc.TARGET_MARK
_results = []


def check(name, got, want):
    ok = got == want
    _results.append((ok, name))
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        print(f"       got : {got!r}\n       want: {want!r}")


def raises(name, fn, exc, needle=""):
    try:
        fn()
    except exc as e:
        ok = needle in str(e)
        _results.append((ok, name))
        print(("PASS " if ok else "FAIL ") + name
              + ("" if ok else f"  [message lacked {needle!r}: {e}]"))
        return
    except BaseException as e:          # noqa: BLE001 - report the wrong type
        _results.append((False, name))
        print(f"FAIL {name}  [raised {type(e).__name__}, wanted {exc.__name__}]")
        return
    _results.append((False, name))
    print(f"FAIL {name}  [nothing raised]")


def counter(d):
    return collections.Counter(d)


def bare(body):
    with tempfile.NamedTemporaryFile("w", suffix=".mdx", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(textwrap.dedent(body))
        path = fh.name
    try:
        return lc.bare_path_links(path)
    finally:
        os.unlink(path)


# --- parse(): the report format ------------------------------------------

print("== parse ==")

check("one file, two broken targets",
      lc.parse(f"a.mdx\n {M} /x\n {M} /y\n"),
      counter({("a.mdx", "/x"): 1, ("a.mdx", "/y"): 1}))

check("ANSI colour codes stripped",
      lc.parse(f"\x1b[1ma.mdx\x1b[0m\n\x1b[31m {M} /x\x1b[0m\n"),
      counter({("a.mdx", "/x"): 1}))

check("spinner prefix stripped",
      lc.parse(f"⠋ a.mdx\n⠹ {M} /x\n"),
      counter({("a.mdx", "/x"): 1}))

check("the same target breaking twice counts twice",
      lc.parse(f"a.mdx\n {M} /x\n {M} /x\n"),
      counter({("a.mdx", "/x"): 2}))

check("summary line is not a finding",
      lc.parse(f"found 1 broken link in 1 file\n\na.mdx\n {M} /x\n"),
      counter({("a.mdx", "/x"): 1}))

check("progress line is not a finding",
      lc.parse(f"checking for broken links...\n\na.mdx\n {M} /x\n"),
      counter({("a.mdx", "/x"): 1}))

check("two files, blank line between",
      lc.parse(f"a.mdx\n {M} /x\n\nb.mdx\n {M} /y\n"),
      counter({("a.mdx", "/x"): 1, ("b.mdx", "/y"): 1}))

# The CLI hard-wraps its output and cannot be told not to (it ignores
# COLUMNS), so both a long target and a long source path arrive split.
check("wrapped target is rejoined",
      lc.parse(f"a.mdx\n {M} /portal/very/long/pa\nth/to/thing\n"),
      counter({("a.mdx", "/portal/very/long/path/to/thing"): 1}))

check("wrapped source path is rejoined",
      lc.parse(f"portal/deep/long-name-that-wr\napped.mdx\n {M} /x\n"),
      counter({("portal/deep/long-name-that-wrapped.mdx", "/x"): 1}))

check("wrapped source path does not corrupt the previous file's target",
      lc.parse(f"a.mdx\n {M} /x\n\nportal/deep/long-name-that-wr\napped.mdx\n {M} /y\n"),
      counter({("a.mdx", "/x"): 1,
               ("portal/deep/long-name-that-wrapped.mdx", "/y"): 1}))

check("a source path not ending .mdx/.md is still a source path",
      lc.parse(f"a.mdx\n {M} /x\n\ndocs.json\n {M} /y\n"),
      counter({("a.mdx", "/x"): 1, ("docs.json", "/y"): 1}))

check("trailing non-report text is not absorbed into the last target",
      lc.parse(f"a.mdx\n {M} /x\n\nreal 130.06 user 138.29\n"),
      counter({("a.mdx", "/x"): 1}))

check("a file listed with no targets yields nothing",
      lc.parse("a.mdx\n\nb.mdx\n"), counter({}))


# --- scan(): refusing to gate on a report it cannot trust ----------------

print("\n== scan trust guards ==")


# scan() resolves every source path it parsed against the tree it scanned, so
# these fixtures need a tree with the named files actually in it.
_TREE = tempfile.mkdtemp()
for _name in ("a.mdx", "b.mdx"):
    pathlib.Path(_TREE, _name).write_text("x\n", encoding="utf-8")


def with_report(text):
    mod = _load()
    mod.run_scan = lambda cwd, files=None: text
    return mod


def scan_of(text):
    return lambda: with_report(text).scan(_TREE, "t")


check("a consistent report is accepted",
      with_report(f"a.mdx\n {M} /x\n {M} /y\nfound 2 broken links in 1 file\n")
      .scan(_TREE, "t")[1:],
      (2, 1))

raises("a report truncated mid-way is refused",
       scan_of(f"a.mdx\n {M} /x\nfound 99 broken links in 40 files\n"),
       Exception, "cannot be trusted")

raises("a report with no summary at all is refused",
       scan_of("Error: something exploded\n"), Exception, "no usable report")

# The parser can only be trusted if every source path it produced is real.
# A mis-parse that happens to preserve the counts would otherwise slip through:
# this is exactly what a wrapped source path used to do.
raises("a parsed source path that is not on disk is refused",
       scan_of(f"no-such-file-xyz.mdx\n {M} /x\nfound 1 broken link in 1 file\n"),
       Exception, "not on disk")

check("two real source paths both pass the on-disk check",
      with_report(f"a.mdx\n {M} /x\n\nb.mdx\n {M} /y\n"
                  f"found 2 broken links in 2 files\n").scan(_TREE, "t")[1:],
      (2, 2))


# --- bare_path_links(): the class the CLI cannot see --------------------

print("\n== bare-path links ==")

check("bare markdown target is flagged",
      bare("See [x](s/article/123).\n"), [(1, "s/article/123")])
check("root-relative target is not flagged",
      bare("See [x](/s/article/123).\n"), [])
check("anchor-only target is not flagged", bare("[x](#heading)\n"), [])
check("./ and ../ targets are not flagged", bare("[a](./x)\n[b](../y)\n"), [])
check("absolute URLs are not flagged",
      bare("[a](https://x.com)\n[b](http://x.com)\n[c](mailto:a@b.c)\n"), [])
check("bare href is flagged", bare('<a href="s/article/9">x</a>\n'),
      [(1, "s/article/9")])
check("bare src is flagged", bare('<img src="images/kb/x.png" />\n'),
      [(1, "images/kb/x.png")])
check("src holding a URL is not flagged",
      bare('<DomoEmbed src="https://x.domo.com/e/1" />\n'), [])
check("root-relative src is not flagged",
      bare('<img src="/images/kb/x.png" />\n'), [])
check("src holding a JSX expression is not flagged",
      bare("<img src={imgVar} />\n"), [])
check("fenced code is skipped",
      bare("```\n[x](s/article/1)\n```\n[y](s/article/2)\n"),
      [(4, "s/article/2")])
check("tilde-fenced code is skipped", bare("~~~\n[x](s/article/1)\n~~~\n"), [])
check("indented fenced code is skipped",
      bare("- item\n  ```\n  [x](s/article/1)\n  ```\n"), [])
check("inline code is skipped", bare("Use `[x](s/article/1)` here.\n"), [])
check("bare image target is flagged", bare("![alt](images/kb/x.png)\n"),
      [(1, "images/kb/x.png")])
check("line numbers survive stripped code",
      bare("one\ntwo\nthree\n[x](s/article/7)\n"), [(4, "s/article/7")])
check("a markdown title after the target is not part of it",
      bare('[x](s/article/7 "Title")\n'), [(1, "s/article/7")])
check("whitespace after the opening paren is ignored",
      bare("[x](  s/article/5)\n"), [(1, "s/article/5")])


# --- argument handling --------------------------------------------------

print("\n== arguments ==")
import contextlib   # noqa: E402
import io           # noqa: E402


def cli(*argv):
    """Run main() against the temp tree, since --all scans the cwd."""
    mod = _load()
    mod.run_scan = lambda cwd, files=None: (
        f"a.mdx\n {M} /x\nfound 1 broken link in 1 file\n")
    sys.argv = ["check-broken-links.py", *argv]
    here = os.getcwd()
    os.chdir(_TREE)
    try:
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return mod.main()
    finally:
        os.chdir(here)


check("--all reports without failing the build", cli("--all"), 0)
raises("--all with --base is rejected", lambda: cli("--all", "--base", "main"),
       SystemExit)
raises("--all with files is rejected", lambda: cli("--all", "f.mdx"), SystemExit)
raises("--base with files is rejected",
       lambda: cli("--base", "main", "f.mdx"), SystemExit)
raises("no arguments is rejected", lambda: cli(), SystemExit)

print()
failed = [n for ok, n in _results if not ok]
print(f"{len(_results) - len(failed)}/{len(_results)} passed")
for n in failed:
    print(f"  FAILED: {n}")
sys.exit(1 if failed else 0)
