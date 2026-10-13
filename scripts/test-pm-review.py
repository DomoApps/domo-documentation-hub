#!/usr/bin/env python3
"""
Smoke test for scripts/pm_review.py — run manually:

    python3 -I scripts/test-pm-review.py

No framework, no CI (nothing else references the engine yet). It monkeypatches the
engine's STATE_DIR / root-file paths to a tmp dir and stubs the builder / git / data
boundaries, so it never reads the live repo tree or real git. Exits 0 when green.

Covers: read-through generation + attribution, the gating block, F5 sign-off
invalidation, v1->v2 back-compat load, the --note requirement, session open/close
(incl. dangling closure), and the reconcile read-through findings.
"""

import argparse
import contextlib
import io
import json
import re
import sys
import tempfile
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pm_review as P  # noqa: E402

PM = "Test PM"
SLUG = "test-pm"
OTHER = "Other PM"
_PASS = 0
_FAIL = 0


def check(cond, msg):
    global _PASS, _FAIL
    if cond:
        _PASS += 1
    else:
        _FAIL += 1
        print(f"  FAIL: {msg}")


def run(fn, **kw):
    """Call a cmd_* handler with an argparse.Namespace, capturing its stdout JSON."""
    buf = io.StringIO()
    exited = None
    with contextlib.redirect_stdout(buf):
        try:
            fn(argparse.Namespace(**kw))
        except SystemExit as e:
            exited = e
    out = buf.getvalue()
    try:
        data = json.loads(out) if out.strip().startswith(("{", "[")) else out
    except json.JSONDecodeError:
        data = out
    return data, exited


def ss_args(**kw):
    base = dict(pm=PM, id=None, status=None, disposition=None, reason=None,
                evidence=None, commit=None, actor=None, note=None, diff_summary=None,
                baseline="BASE")
    base.update(kw)
    return base


def setup(tmp):
    """Point the engine at a tmp workspace and stub its external boundaries."""
    articles = tmp / "s" / "article"
    articles.mkdir(parents=True)
    state = tmp / "pm-review-state"
    state.mkdir()

    P.STATE_DIR = state
    P.SYNC_BASELINE_FILE = state / "sync-baseline.json"
    P.ROLLUP_FILE = tmp / "PM-REVIEW-ROLLUP.md"
    P.DEFERRED_FILE = tmp / "RESTRUCTURE-DEFERRED-ARTICLES.md"
    P.JOURNAL_FILE = tmp / "PM-REVIEW-JOURNAL.md"

    # fake builder module (only the attrs the engine touches)
    P._BUILDER = types.SimpleNamespace(
        ARTICLE_DIR=articles,
        scan_article_pm_inputs=lambda d: [],
        _PM_INPUT_RE=re.compile(r"\{/\*\s*\[pm-input\]\s*(.*?)\*/\}", re.DOTALL),
        _PM_INPUT_SPLIT=re.compile(r"\s*(.+?)\s*[—:]\s*(.*)", re.DOTALL),
    )
    # ownership-reassignment helpers operate on the integration branch + tmp root files
    P.current_branch = lambda: P.INTEGRATION_BRANCH
    P.OVERRIDES_FILE = state / "ownership-overrides.json"
    P.OWNERSHIP_LOG = state / "ownership-change-log.csv"
    P.MANIFEST_FILE = tmp / "RESTRUCTURE-MANIFEST.md"
    P.PM_STATUS_FILE = tmp / "PM-REVIEW-STATUS.md"
    # one brief item: a fact-check sibling on the from-scratch article new1.mdx
    normal = [{
        "id": "fc-sib", "type": "fact-check", "target": "new1.mdx",
        "label": "`new1.mdx` — claim", "occurrence": 1,
        "natural_key": "fact-check|new1.mdx|1", "ask_snapshot": "verify a claim",
        "gap_fill": False,
    }]
    P.regenerate_items = lambda pm: list(normal)
    P.roster = lambda: [PM, OTHER, "Phil Fuchs"]
    P.load_data = lambda: (
        {PM: {"features": {"Cards"},
              "articles": [("Cards", "T1", "new1.mdx"), ("Cards", "T2", "new2.mdx")]}},
        {}, {})
    # new1 is owned+added; unowned.mdx is added but NOT owned/targeted (attribution test)
    P.git_added_since = lambda baseline: {"new1.mdx", "unowned.mdx"}
    P.resolve_baseline = lambda explicit=None: "BASE"
    return articles, state


def rt_id():
    return f"rt-{P.sha('read-through', 'new1.mdx')}"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="pmrev-test-"))
    articles, state = setup(tmp)

    # (a) generation + attribution
    data, _ = run(P.cmd_items, pm=PM, no_write=False)
    ids = {i["id"] for i in data["items"]}
    check(rt_id() in ids, "read-through generated for owned+net-new new1.mdx")
    check(not any(i["type"] == "read-through" and i["target"] == "unowned.mdx" for i in data["items"]),
          "unowned added file does NOT get a read-through (attribution gate)")

    # (b) gating: cannot pass read-through while sibling open
    _, exited = run(P.cmd_set_status, **ss_args(id=rt_id(), status="approved", note="read it"))
    check(exited is not None and exited.code != 0, "read-through pass blocked while sibling open")

    # (e) --note required for terminal
    _, exited = run(P.cmd_set_status, **ss_args(id="fc-sib", status="approved"))
    check(exited is not None, "--note required for a terminal status")

    # resolve the sibling, then the read-through passes
    run(P.cmd_set_status, **ss_args(id="fc-sib", status="approved", note="claim verified"))
    data, exited = run(P.cmd_set_status, **ss_args(id=rt_id(), status="approved", note="whole article good"))
    check(exited is None and data.get("status") == "approved", "read-through passes once siblings terminal")

    # (c) F5: reopening the sibling reopens the read-through
    data, _ = run(P.cmd_set_status, **ss_args(id="fc-sib", status="rewrite-redo", note="needs a tweak"))
    check(data.get("reopened_read_through") == rt_id(), "sibling reopen reopens the read-through")
    led = P.load_ledger(PM, SLUG)
    check(led["items"][rt_id()]["status"] == "pending", "reopened read-through is back to pending")

    # (f) sessions: start, dangling closure, end collects commits
    d1, _ = run(P.cmd_session_start, pm=PM, actor=None, summary="s1")
    d2, _ = run(P.cmd_session_start, pm=PM, actor=None, summary="s2")
    check(d2.get("closed_dangling") == d1["session"], "second session-start closes the dangling first")
    run(P.cmd_set_status, **ss_args(id="fc-sib", status="approved", note="ok now", commit="abc123"))
    de, _ = run(P.cmd_session_end, pm=PM, summary="done")
    check("fc-sib" in de["items_touched"] and "abc123" in de["commits"],
          "session-end collects touched items and their commits")

    # (d) v1 -> v2 back-compat load
    v1 = {"schema": 1, "pm": PM, "slug": SLUG, "branch": f"restructure/pm/{SLUG}",
          "baseline_sha": None, "items": {}}
    (state / f"{SLUG}.json").write_text(json.dumps(v1), encoding="utf-8")
    led = P.load_ledger(PM, SLUG)
    check(led["schema"] == P.SCHEMA_VERSION and "sessions" in led and "decisions" in led
          and "current_session" in led, "v1 ledger upgrades to v2 with new keys")

    # (g) reconcile read-through findings
    # terminal read-through, no marker in the (empty) file -> terminal_without_marker;
    # new1.mdx is from-scratch but has no read-through ledger entry here -> from_scratch_without_item.
    (articles / "new1.mdx").write_text("# new1\n", encoding="utf-8")
    (articles / "marked.mdx").write_text(
        "# marked\n{/* [read-through] pm=test-pm date=2026-10-12 */}\n", encoding="utf-8")
    recon_ledger = {
        "schema": 2, "pm": PM, "slug": SLUG, "branch": f"restructure/pm/{SLUG}",
        "baseline_sha": "BASE", "sessions": [], "decisions": [], "current_session": None,
        "items": {
            "rt-marked": {"type": "read-through", "target": "marked.mdx", "status": "approved",
                          "history": []},
            "rt-nomark": {"type": "read-through", "target": "nomark.mdx", "status": "approved",
                          "history": []},
        },
    }
    (state / f"{SLUG}.json").write_text(json.dumps(recon_ledger), encoding="utf-8")
    data, _ = run(P.cmd_reconcile, pm=None, strict=False)
    rtf = data["read_through_findings"]
    missing_marker_targets = {t for _pm, _id, t in rtf["terminal_without_marker"]}
    check("nomark.mdx" in missing_marker_targets, "terminal read-through without marker is flagged")
    check("marked.mdx" not in missing_marker_targets, "terminal read-through WITH marker is not flagged")
    fs_targets = {t for _pm, t in rtf["from_scratch_without_item"]}
    check("new1.mdx" in fs_targets, "from-scratch article with no read-through item is flagged")
    check("unowned.mdx" not in fs_targets, "unattributed added file is NOT flagged as missing")

    # (h) reassign --article: override map + marker rewrite + manifest/status sweep + audit + decision
    (articles / "new1.mdx").write_text(
        "# new1\n{/* [pm-input] Test PM — confirm the thing */}\n", encoding="utf-8")
    P.MANIFEST_FILE.write_text(
        "## T\n\n| Filename | PM | Notes |\n|---|---|---|\n| `new1.mdx` | Test PM | note |\n", encoding="utf-8")
    P.PM_STATUS_FILE.write_text(
        "| PM | Done |\n|----|------|\n| Test PM | done |\n| Other PM | todo |\n", encoding="utf-8")
    data, _ = run(P.cmd_reassign, article="new1.mdx", feature=None, to=OTHER, from_pm=PM,
                  reason="PM says it's theirs", decided_by=OTHER, actor="other-pm")
    check(data.get("to_pm") == OTHER and data["files"] == ["new1.mdx"], "reassign returns the move")
    ov = json.loads((state / "ownership-overrides.json").read_text())
    check(any(o["filename"] == "new1.mdx" and o["to_pm"] == OTHER for o in ov["overrides"]),
          "override map records filename -> new PM")
    check("[pm-input] Other PM —" in (articles / "new1.mdx").read_text(),
          "inline [pm-input] marker rewritten to new PM")
    check("| `new1.mdx` | Other PM |" in P.MANIFEST_FILE.read_text(), "manifest PM cell swept to new PM")
    check("| Test PM | todo |" in P.PM_STATUS_FILE.read_text(), "status Done reset for affected PM")
    check((state / "ownership-change-log.csv").exists(), "audit log written")
    exp, _ = run(P.cmd_explain, pm=None, target="new1.mdx", id=None, decision=None)
    check(any(d.get("kind") == "ownership-reassign" for d in exp["decisions"]),
          "explain --target surfaces the ownership-reassign decision")
    check("warning" in data, "warns when target PM lacks a CODEOWNERS login")

    # (i) reassign --feature expands to every article under the Feature
    data, _ = run(P.cmd_reassign, article=None, feature="Cards", to=OTHER, from_pm=None,
                  reason="whole area", decided_by=OTHER, actor="other-pm")
    check(set(data["files"]) == {"new1.mdx", "new2.mdx"}, "feature reassign expands to all its articles")

    # (j) reassign to a routed PM → no warning
    data, _ = run(P.cmd_reassign, article="new2.mdx", feature=None, to="Phil Fuchs", from_pm=PM,
                  reason="x", decided_by=None, actor=None)
    check("warning" not in data, "no warning when target PM has a CODEOWNERS login")

    # (k) propagate-ownership --dry-run lists branches without side effects
    real_git = P.git
    P.git = lambda *a, **k: types.SimpleNamespace(
        returncode=0, stdout="restructure/pm/a\nrestructure/pm/b\n", stderr="")
    data, _ = run(P.cmd_propagate_ownership, dry_run=True)
    P.git = real_git
    check(data.get("dry_run") and len(data["branches"]) == 2, "propagate-ownership --dry-run lists branches")

    print(f"\n{_PASS} passed, {_FAIL} failed")
    sys.exit(1 if _FAIL else 0)


if __name__ == "__main__":
    main()
