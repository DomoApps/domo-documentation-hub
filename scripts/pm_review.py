#!/usr/bin/env python3
"""
pm_review.py — engine for the interactive `pm-review` skill (KB restructure Phase 4.5).

The `pm-review` skill drives this CLI; it does not reimplement the brief logic. All
item data comes from the SAME source as the per-PM briefs and RESTRUCTURE-TASKS.md:
`scripts/build-pm-review-briefs.py`. Its filename has hyphens (not importable by name),
so it is loaded via importlib and its pure helpers are called directly — never main().

Durable per-item state lives in one tracked JSON ledger per PM at
`pm-review-state/<slug>.json`. The ledger is the superset of truth; the regenerated
item list is a volatile view reconciled against it on every run (see sync_ledger).

Subcommands
  items   --pm NAME                 Emit the PM's reconciled worklist (JSON).
  resume  --pm NAME                 Emit the first non-terminal item (JSON), or done.
  set-status --pm NAME --id ID --status S [--disposition D] [--reason R]
             [--evidence E] [--commit SHA] [--actor A] [--note WHY] [--diff-summary S]
                                     Record a disposition for one item. --note is
                                     REQUIRED for terminal statuses (the WHY).
  session-start --pm NAME           Open a review session (closes any dangling one).
  session-end --pm NAME             Close the open session (collects items/commits).
  link    --pm NAME --kind K --summary S --items ID,ID --targets F,F --narrative N
                                     Record ONE linked cross-article decision (e.g.
                                     drop gap-fill X, fold its content into article Y).
  journal --pm NAME                 Render per-PM pm-review-state/<slug>.journal.md.
  journal --all                     Render the root PM-REVIEW-JOURNAL.md (INTEGRATION
                                     branch only).
  explain [--pm NAME] [--target F] [--id ID] [--decision D]
                                     Reconstruct what a PM did and why (read-only).
  reconcile [--pm NAME]             Marker <-> ledger sweep (the Phase 4.5->4.6 gate).
  rollup                            Regenerate PM-REVIEW-ROLLUP.md (INTEGRATION only).
  deferred-report                   Regenerate RESTRUCTURE-DEFERRED-ARTICLES.md (ditto).
  check-baseline [--baseline SHA]   Report whether the diff baseline is an ancestor
                                     of HEAD (the skill's refuse-to-run guard).

A read-through item (type "read-through") is auto-generated per FROM-SCRATCH article
in a PM's lane (net-new since baseline, attributed to the PM, plus gap-fills the PM
authored). It is the article's FINAL sign-off: it passes only after every other item
on the same article is terminal (set-status enforces this).

Shared, derived artifacts (RESTRUCTURE-TASKS.md, PM-REVIEW-ROLLUP.md,
RESTRUCTURE-DEFERRED-ARTICLES.md, docs.json nav) are regenerated on the INTEGRATION
branch after per-PM branches merge back — never hand-edited on a PM branch.
"""

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILDER_PATH = Path(__file__).resolve().parent / "build-pm-review-briefs.py"
STATE_DIR = REPO_ROOT / "pm-review-state"
ROLLUP_FILE = REPO_ROOT / "PM-REVIEW-ROLLUP.md"
DEFERRED_FILE = REPO_ROOT / "RESTRUCTURE-DEFERRED-ARTICLES.md"
JOURNAL_FILE = REPO_ROOT / "PM-REVIEW-JOURNAL.md"
INTEGRATION_BRANCH = "update/fullRestructure"

TYPE_ORDER = ["fact-check", "pm-input", "legacy", "retired", "update", "decision", "read-through"]
TYPE_PREFIX = {
    "fact-check": "fc", "pm-input": "pmi", "legacy": "life",
    "retired": "ret", "update": "upd", "decision": "dec", "read-through": "rt",
}
TERMINAL = {"approved", "denied", "rejected", "answered", "deferred", "dropped"}
NONTERMINAL = {"pending", "rewrite-redo", "skipped"}
SCHEMA_VERSION = 2

# A read-through is a from-scratch article's final, holistic sign-off.
RT_ASK = ("Read the full article end-to-end (MDX file or preview). Confirm it is factually "
          "correct AND phrased the way you want. This is the article's final sign-off; it can "
          "pass only after every other item on this article is resolved.")

_FILE_RE = re.compile(r"`([^`]+?\.mdx)`")
_DID_RE = re.compile(r"^(D\d+)\b")
SCHEMA_NOTE = "schema: pm_review.py v%d" % SCHEMA_VERSION


# ── builder import (hyphenated filename) ─────────────────────────────────────

def load_builder():
    """Import build-pm-review-briefs.py as a module without running its main()."""
    spec = importlib.util.spec_from_file_location("build_pm_review_briefs", BUILDER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # safe: all side effects are under __main__
    return mod


_BUILDER = None
_DATA = None


def builder():
    global _BUILDER
    if _BUILDER is None:
        _BUILDER = load_builder()
    return _BUILDER


def load_data():
    """Mirror build-pm-review-briefs.main()'s data load (ownership, gaps, forum)."""
    global _DATA
    if _DATA is not None:
        return _DATA
    m = builder()
    ownership = m.load_ownership_reference(m.OWNERSHIP_FILE)
    gaps = m.load_forum_gaps(m.GAPS_FILE)
    manifest_text = m.MANIFEST_FILE.read_text(encoding="utf-8") if m.MANIFEST_FILE.exists() else ""
    forum = {
        "written": m.parse_manifest_forum_written(manifest_text),
        "deferred": m.parse_manifest_forum_deferred(manifest_text),
        "checkpoints": m.scan_article_pm_inputs(m.ARTICLE_DIR),
    }
    _DATA = (ownership, gaps, forum)
    return _DATA


def roster():
    """Union of PMs that get a brief — mirrors build-pm-review-briefs.main()."""
    m = builder()
    ownership, _gaps, forum = load_data()
    r = set(ownership.keys())
    for _, _, _, pm, _, _ in m.PHASE3A_ARTICLES:
        r.add(pm)
    for _, _, pm, _ in m.PHASE3A_PM_ARTICLES:
        r.add(pm)
    r.update(m.MANIFEST_PM_INPUT_FLAGS.keys())
    for c in forum["checkpoints"]:
        r.add(c["pm"])
    return sorted(r)


# ── small helpers ────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def sha(*parts: str) -> str:
    h = hashlib.sha1("\x00".join(parts).encode("utf-8")).hexdigest()
    return h[:10]


def extract_target(label: str):
    """First `foo.mdx` token in a task label, else None."""
    m = _FILE_RE.search(label or "")
    return m.group(1) if m else None


def canonical_pm(name: str):
    """Map a (possibly slug/typo'd) PM name to its canonical roster name, else None."""
    want = slugify(name)
    for pm in roster():
        if slugify(pm) == want:
            return pm
    return None


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r


def current_branch() -> str:
    return git("rev-parse", "--abbrev-ref", "HEAD", check=False).stdout.strip()


def git_added_since(baseline) -> set:
    """
    Basenames of s/article/*.mdx files ADDED between baseline and HEAD.

    No rename detection (-M/-C): the baseline is a content-sync point, not an ancestor,
    so rename detection would reclassify a genuine net-new article as a rename of a
    deleted one and HIDE it. (This deliberately differs from the per-item display diff,
    which keeps -M -C.) The raw add-set is noisy — callers MUST attribute it to a PM.
    """
    if not baseline:
        return set()
    r = git("diff", "--name-only", "--diff-filter=A", baseline, "HEAD", "--", "s/article", check=False)
    if r.returncode != 0:
        return set()
    return {Path(line.strip()).name for line in r.stdout.splitlines()
            if line.strip().endswith(".mdx")}


def _require_integration_branch(cmd: str, outfile: Path):
    """Guard a shared repo-root writer: it must run only on the integration branch."""
    br = current_branch()
    if br != INTEGRATION_BRANCH:
        sys.exit(f"error: `{cmd}` writes the shared root file {outfile.name} and runs only on "
                 f"{INTEGRATION_BRANCH} (current branch: {br or 'unknown'}). Regenerate it after "
                 "the PM branches merge back — never on a PM branch.")


# ── item extraction (1:1 with collect_pm_tasks → the briefs/tasks source) ─────

def regenerate_items(pm_name: str) -> list:
    """
    Reconstruct the PM's typed worklist from collect_pm_tasks (the exact source that
    feeds RESTRUCTURE-TASKS.md), attaching a stable id, occurrence index, secondary
    natural key, target, ask snapshot, and a gap_fill flag. Order is TYPE_ORDER then
    insertion order, which is deterministic across runs.
    """
    m = builder()
    _ownership, gaps, forum = load_data()
    tasks = m.collect_pm_tasks(pm_name, gaps, forum)

    # `pos` = positional index per (type, target) in document order → the fallback
    #   natural key, used only when an ask is reworded (primary id would miss).
    # `dup` = index per ask-hash → suffixes the primary id ONLY for a genuine
    #   identical-ask-same-file collision, so IDs stay stable when a *sibling*
    #   marker elsewhere in the file is burned.
    pos = defaultdict(int)
    dup = defaultdict(int)
    items = []
    for typ in TYPE_ORDER:
        for label, desc in tasks.get(typ, []):
            target = extract_target(label)
            pos_key = (typ, target or label)
            pos[pos_key] += 1
            occurrence = pos[pos_key]

            if typ == "decision":
                dm = _DID_RE.match(label.strip())
                item_id = f"dec-{dm.group(1)}" if dm else f"dec-{sha(label)}"
            else:
                base_id = f"{TYPE_PREFIX[typ]}-{sha(typ, target or label, normalize(desc))}"
                dup[base_id] += 1
                item_id = base_id if dup[base_id] == 1 else f"{base_id}-{dup[base_id]}"

            # gap-fill = a pm-input whose target article does not exist yet
            # (deferred forum rows + PHASE3A_PM_ARTICLES). Inline-marker pm-inputs
            # and cross-cutting (no-file) pm-inputs are NOT gap-fill.
            gap_fill = bool(
                typ == "pm-input"
                and target
                and not (m.ARTICLE_DIR / target).exists()
            )

            items.append({
                "id": item_id,
                "type": typ,
                "target": target,
                "label": label,
                "occurrence": occurrence,
                "natural_key": f"{typ}|{target or label}|{occurrence}",
                "ask_snapshot": desc,
                "gap_fill": gap_fill,
            })
    return items


# ── read-through items (git-derived, NOT from the briefs) ─────────────────────

def _owned_files(pm: str) -> set:
    """Article filenames owned by this PM per Article-PM-Ownership-Reference.mdx."""
    ownership, _gaps, _forum = load_data()
    entry = ownership.get(pm) or {}
    return {a[2] for a in entry.get("articles", []) if len(a) >= 3 and a[2]}


def from_scratch_targets(pm: str, normal_items: list, ledger: dict, baseline) -> dict:
    """
    Map {filename -> provenance} of every FROM-SCRATCH article in this PM's lane.

    A — net-new since baseline, ATTRIBUTED to the PM. The raw added-set is noisy
        (a content-sync re-created files), so attribution is a hard AND-gate: a file
        counts only if it is OWNED by the PM (ownership reference) OR is the target of
        one of the PM's generated brief items (covers net-new whose ownership .mdx lags,
        since build-pm-ownership.py is not run on PM branches).
    B — gap-fills the PM AUTHORED this phase. Keyed off the persisted
        disposition=="author" (NOT the gap_fill flag, which flips to False the moment
        the file exists), for files that now exist.
    """
    m = builder()
    article_dir = m.ARTICLE_DIR
    added = git_added_since(baseline)
    owned = _owned_files(pm)
    targeted = {it.get("target") for it in normal_items if it.get("target")}

    out = {}
    for f in added:
        if f in owned or f in targeted:
            out[f] = "git-added"
    for e in ledger.get("items", {}).values():
        tgt = e.get("target")
        if e.get("disposition") == "author" and tgt and (article_dir / tgt).exists():
            out[tgt] = "authored-gapfill"
    return out


def regenerate_read_throughs(pm: str, normal_items: list, ledger: dict, baseline) -> list:
    """One read-through item per from-scratch article; id hashes the target only, so it
    is stable across reruns and content edits (unlike fact-check, which hashes the ask)."""
    rts = []
    for target, source in sorted(from_scratch_targets(pm, normal_items, ledger, baseline).items()):
        rts.append({
            "id": f"rt-{sha('read-through', target)}",
            "type": "read-through",
            "target": target,
            "label": f"`{target}` — full read-through sign-off",
            "occurrence": 1,
            "natural_key": f"read-through|{target}|1",
            "ask_snapshot": RT_ASK,
            "gap_fill": False,
            "source": source,
        })
    return rts


def regenerate_all(pm: str, slug: str):
    """Brief items + read-through items, synced against the loaded ledger.
    Returns (items, ledger, new_ids, stale_ids). Caller persists (save_ledger)."""
    normal = regenerate_items(pm)
    ledger = load_ledger(pm, slug)
    baseline = ledger.get("baseline_sha") or resolve_baseline()
    items = normal + regenerate_read_throughs(pm, normal, ledger, baseline)
    new_ids, stale = sync_ledger(ledger, items)
    return items, ledger, new_ids, stale


def _rt_blockers(ledger: dict, rt_id: str, target: str) -> list:
    """Non-terminal, non-read-through items on the same article (block the sign-off)."""
    return sorted(
        iid for iid, e in ledger["items"].items()
        if iid != rt_id and e.get("target") == target
        and e.get("type") != "read-through" and e.get("status") not in TERMINAL
    )


# ── ledger I/O + reconciliation ──────────────────────────────────────────────

def ledger_path(slug: str) -> Path:
    return STATE_DIR / f"{slug}.json"


def new_ledger(pm_name: str, slug: str) -> dict:
    return {
        "schema": SCHEMA_VERSION,
        "pm": pm_name,
        "slug": slug,
        "branch": f"restructure/pm/{slug}",
        "baseline_sha": None,
        "generated_from": SCHEMA_NOTE,
        "updated": date.today().isoformat(),
        "sessions": [],
        "decisions": [],
        "current_session": None,
        "items": {},
    }


def load_ledger(pm_name: str, slug: str) -> dict:
    p = ledger_path(slug)
    if p.exists():
        data = json.loads(p.read_text(encoding="utf-8"))
        # schema v1 -> v2 back-compat: default-fill the new top-level keys. (No live
        # ledger exists on disk yet; this is belt-and-suspenders.)
        if data.get("schema", 1) < SCHEMA_VERSION:
            data.setdefault("sessions", [])
            data.setdefault("decisions", [])
            data.setdefault("current_session", None)
            data["schema"] = SCHEMA_VERSION
        return data
    return new_ledger(pm_name, slug)


def save_ledger(ledger: dict):
    STATE_DIR.mkdir(exist_ok=True)
    ledger["updated"] = date.today().isoformat()
    p = ledger_path(ledger["slug"])
    p.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sync_ledger(ledger: dict, items: list):
    """
    Reconcile the durable ledger against the freshly regenerated item list.
    - match by id, then by secondary natural_key (reworded ask) — never orphan+create
    - new regenerated item -> insert as pending (first_seen)
    - ledger item absent from scan -> never deleted; flag non-terminal ones as stale
    Returns (new_item_ids, stale_item_ids).
    """
    today = date.today().isoformat()
    by_id = ledger["items"]
    by_natkey = {e.get("natural_key"): e for e in by_id.values() if e.get("natural_key")}

    seen_ids = set()
    new_ids = []
    for it in items:
        entry = by_id.get(it["id"]) or by_natkey.get(it["natural_key"])
        if entry is None:
            entry = {
                "type": it["type"],
                "target": it["target"],
                "occurrence": it["occurrence"],
                "natural_key": it["natural_key"],
                "ask_snapshot": it["ask_snapshot"],
                "gap_fill": it["gap_fill"],
                "source": it.get("source"),
                "status": "pending",
                "disposition": None,
                "reason": None,
                "evidence": None,
                "commit": None,
                "present_in_latest_scan": True,
                "first_seen": today,
                "last_seen": today,
                "history": [],
            }
            by_id[it["id"]] = entry
            new_ids.append(it["id"])
        else:
            # keep id canonical; refresh volatile fields, preserve status/history
            entry["type"] = it["type"]
            entry["target"] = it["target"]
            entry["occurrence"] = it["occurrence"]
            entry["natural_key"] = it["natural_key"]
            entry.setdefault("ask_snapshot", it["ask_snapshot"])
            entry["gap_fill"] = it["gap_fill"]
            if it.get("source") is not None:
                entry["source"] = it["source"]
            entry["present_in_latest_scan"] = True
            entry["last_seen"] = today
            # if matched by natural key under a new id, re-home under the new id
            if by_id.get(it["id"]) is not entry:
                old = next((k for k, v in by_id.items() if v is entry), None)
                if old is not None:
                    del by_id[old]
                by_id[it["id"]] = entry
        seen_ids.add(it["id"])

    stale = []
    for iid, entry in by_id.items():
        if iid in seen_ids:
            continue
        entry["present_in_latest_scan"] = False
        if entry.get("status") not in TERMINAL:
            stale.append(iid)
    return new_ids, stale


def resolve_pm(name: str):
    pm = canonical_pm(name)
    if not pm:
        sys.exit(f"error: '{name}' matches no PM in the roster. Known PMs:\n  "
                 + "\n  ".join(roster()))
    return pm, slugify(pm)


# ── baseline guard ────────────────────────────────────────────────────────────

SYNC_BASELINE_FILE = STATE_DIR / "sync-baseline.json"


def load_sync_baseline() -> dict:
    if SYNC_BASELINE_FILE.exists():
        try:
            return json.loads(SYNC_BASELINE_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    return {}


def resolve_baseline(explicit=None):
    if explicit:
        return explicit
    sb = load_sync_baseline().get("baseline_sha")
    if sb:
        return sb
    for ref in ("origin/main", "main"):
        r = git("rev-parse", "--verify", "--quiet", ref, check=False)
        if r.returncode == 0:
            return r.stdout.strip()
    return None


def is_commit(sha_ref: str) -> bool:
    if not sha_ref:
        return False
    return git("cat-file", "-e", f"{sha_ref}^{{commit}}", check=False).returncode == 0


def is_ancestor(sha_ref: str) -> bool:
    if not sha_ref:
        return False
    return git("merge-base", "--is-ancestor", sha_ref, "HEAD", check=False).returncode == 0


# ── commands ──────────────────────────────────────────────────────────────────

def cmd_items(args):
    pm, slug = resolve_pm(args.pm)
    items, ledger, new_ids, stale = regenerate_all(pm, slug)
    if not args.no_write:
        save_ledger(ledger)
    out = []
    for it in sorted(items, key=lambda i: (TYPE_ORDER.index(i["type"]), i["target"] or "", i["occurrence"])):
        e = ledger["items"][it["id"]]
        out.append({**it, "status": e["status"], "disposition": e.get("disposition"),
                    "reason": e.get("reason"), "evidence": e.get("evidence")})
    print(json.dumps({
        "pm": pm, "slug": slug, "branch": ledger["branch"],
        "baseline_sha": ledger.get("baseline_sha"),
        "counts": _status_counts(ledger),
        "new_items": new_ids, "stale_items": stale,
        "items": out,
    }, indent=2, ensure_ascii=False))


def cmd_resume(args):
    pm, slug = resolve_pm(args.pm)
    items, ledger, _new, _stale = regenerate_all(pm, slug)
    if not args.no_write:
        save_ledger(ledger)
    ordered = sorted(items, key=lambda i: (TYPE_ORDER.index(i["type"]), i["target"] or "", i["occurrence"]))
    blocked_rts = []
    for it in ordered:
        st = ledger["items"][it["id"]]["status"]
        if st in TERMINAL or st == "skipped":
            continue
        # a read-through can't be worked until every sibling on its article is terminal;
        # hold it back so the skill never offers an un-passable item
        if it["type"] == "read-through":
            blockers = _rt_blockers(ledger, it["id"], it["target"])
            if blockers:
                blocked_rts.append({"id": it["id"], "target": it["target"], "blockers": blockers})
                continue
        print(json.dumps({"pm": pm, "slug": slug, "next": {**it, "status": st},
                          "counts": _status_counts(ledger)}, indent=2, ensure_ascii=False))
        return
    # then surface skipped (come-back items)
    for it in ordered:
        if ledger["items"][it["id"]]["status"] == "skipped":
            print(json.dumps({"pm": pm, "slug": slug, "next": {**it, "status": "skipped"},
                              "counts": _status_counts(ledger)}, indent=2, ensure_ascii=False))
            return
    # nothing actionable: either truly done, or only read-throughs waiting on open siblings
    print(json.dumps({"pm": pm, "slug": slug, "next": None, "done": not blocked_rts,
                      "blocked_read_throughs": blocked_rts,
                      "counts": _status_counts(ledger)}, indent=2, ensure_ascii=False))


def cmd_set_status(args):
    pm, slug = resolve_pm(args.pm)
    status = args.status
    if status not in TERMINAL | NONTERMINAL:
        sys.exit(f"error: invalid status '{status}'. Valid: {sorted(TERMINAL | NONTERMINAL)}")
    note = (args.note or "").strip()
    if status in TERMINAL and not note:
        sys.exit(f"error: --note is required for a terminal status ({sorted(TERMINAL)}). "
                 "Record WHY the PM made this decision — it is the durable record.")
    items, ledger, _new, _stale = regenerate_all(pm, slug)
    entry = ledger["items"].get(args.id)
    if entry is None:
        sys.exit(f"error: item id '{args.id}' not found for {pm}. Run `items --pm \"{pm}\"` to list.")

    # read-through is the article's final sign-off: block the pass while siblings are open
    if entry.get("type") == "read-through" and status == "approved":
        blockers = _rt_blockers(ledger, args.id, entry.get("target"))
        if blockers:
            sys.exit(f"error: cannot pass the read-through for {entry.get('target')} while other "
                     f"items on that article are still open: {', '.join(blockers)}. Resolve every "
                     "sibling first — the read-through is the whole-article final sign-off.")

    entry["status"] = status
    if args.disposition:
        entry["disposition"] = args.disposition
    if args.reason is not None:
        entry["reason"] = args.reason
    if args.evidence is not None:
        entry["evidence"] = args.evidence
    if args.commit:
        entry["commit"] = args.commit
    hist = {"date": date.today().isoformat(), "status": status, "actor": args.actor or slug,
            "session": ledger.get("current_session")}
    if note:
        hist["note"] = note
    if args.disposition:
        hist["disposition"] = args.disposition
    if args.commit:
        hist["commit"] = args.commit
    if args.diff_summary:
        hist["diff_summary"] = args.diff_summary
    entry.setdefault("history", []).append(hist)

    # sign-off invalidation: if a sibling just re-opened, a prior whole-article sign-off
    # is stale — reopen its read-through so it must be re-passed.
    reopened = None
    if entry.get("type") != "read-through" and status not in TERMINAL and entry.get("target"):
        for iid, e in ledger["items"].items():
            if (e.get("type") == "read-through" and e.get("target") == entry["target"]
                    and e.get("status") in TERMINAL):
                e["status"] = "pending"
                e.setdefault("history", []).append({
                    "date": date.today().isoformat(), "status": "pending",
                    "actor": args.actor or slug, "session": ledger.get("current_session"),
                    "note": f"reopened: sibling {args.id} changed to {status} after sign-off",
                })
                reopened = iid

    if ledger.get("baseline_sha") is None and args.baseline:
        ledger["baseline_sha"] = args.baseline
    save_ledger(ledger)
    out = {"ok": True, "id": args.id, "status": status, "counts": _status_counts(ledger)}
    if reopened:
        out["reopened_read_through"] = reopened
    print(json.dumps(out, indent=2, ensure_ascii=False))


# ── session log + linked decisions ────────────────────────────────────────────

def cmd_session_start(args):
    pm, slug = resolve_pm(args.pm)
    ledger = load_ledger(pm, slug)
    ledger.setdefault("sessions", [])
    closed = None
    cur = ledger.get("current_session")
    if cur:
        for s in ledger["sessions"]:
            if s["id"] == cur and not s.get("ended"):
                s["ended"] = date.today().isoformat()
                closed = cur
    sid = f"s{len(ledger['sessions']) + 1}-{date.today().isoformat()}"
    ledger["sessions"].append({
        "id": sid, "started": date.today().isoformat(), "ended": None,
        "actor": args.actor or slug, "summary": args.summary or "",
        "items_touched": [], "commits": [],
    })
    ledger["current_session"] = sid
    save_ledger(ledger)
    print(json.dumps({"ok": True, "session": sid, "closed_dangling": closed},
                     indent=2, ensure_ascii=False))


def cmd_session_end(args):
    pm, slug = resolve_pm(args.pm)
    ledger = load_ledger(pm, slug)
    sid = ledger.get("current_session")
    if not sid:
        sys.exit("error: no open session. Run `session-start` first.")
    touched, commits = set(), set()
    for iid, e in ledger.get("items", {}).items():
        for h in e.get("history", []):
            if h.get("session") == sid:
                touched.add(iid)
                if h.get("commit"):
                    commits.add(h["commit"])
    for s in ledger["sessions"]:
        if s["id"] == sid:
            s["ended"] = date.today().isoformat()
            s["items_touched"] = sorted(touched)
            s["commits"] = sorted(commits)
            if args.summary:
                s["summary"] = args.summary
    ledger["current_session"] = None
    save_ledger(ledger)
    print(json.dumps({"ok": True, "session": sid, "items_touched": sorted(touched),
                      "commits": sorted(commits)}, indent=2, ensure_ascii=False))


def cmd_link(args):
    pm, slug = resolve_pm(args.pm)
    ledger = load_ledger(pm, slug)
    ledger.setdefault("decisions", [])
    did = f"link-{len(ledger['decisions']) + 1}-{date.today().isoformat()}"
    rec = {
        "id": did,
        "date": args.date or date.today().isoformat(),
        "actor": args.actor or slug,
        "kind": args.kind,
        "summary": args.summary,
        "items": [s.strip() for s in (args.items or "").split(",") if s.strip()],
        "targets": [s.strip() for s in (args.targets or "").split(",") if s.strip()],
        "narrative": args.narrative or "",
        "session": ledger.get("current_session"),
    }
    ledger["decisions"].append(rec)
    save_ledger(ledger)
    print(json.dumps({"ok": True, "decision": rec}, indent=2, ensure_ascii=False))


def _status_counts(ledger: dict) -> dict:
    c = defaultdict(int)
    for e in ledger["items"].values():
        c[e["status"]] += 1
    c["total"] = len(ledger["items"])
    c["open"] = sum(1 for e in ledger["items"].values() if e["status"] not in TERMINAL)
    return dict(c)


def _all_ledgers():
    if not STATE_DIR.exists():
        return []
    out = []
    for p in sorted(STATE_DIR.glob("*.json")):
        if p.name == SYNC_BASELINE_FILE.name:   # the sync sentinel is not a ledger
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"  WARNING: could not read {p.name}: {e}", file=sys.stderr)
            continue
        if "items" not in data:   # skip any non-ledger json that lands here
            continue
        out.append(data)
    return out


def cmd_rollup(args):
    _require_integration_branch("rollup", ROLLUP_FILE)
    ledgers = _all_ledgers()
    lines = [
        "---",
        'title: "KB Restructure — PM Review Rollup (derived)"',
        'excerpt: "Machine rollup of per-item PM-review status, unioned from pm-review-state/*.json. Regenerated by scripts/pm_review.py rollup on the integration branch — do not hand-edit. PM-REVIEW-STATUS.md remains the hand-maintained workflow ledger."',
        "---",
        "",
        "# KB Restructure — PM Review Rollup (derived)",
        "",
        f"**Generated:** {date.today().isoformat()} by `scripts/pm_review.py rollup`.",
        "**Source:** union of `pm-review-state/*.json`. **Do not hand-edit** — regenerate after merge-backs.",
        "Companion to the hand-maintained `PM-REVIEW-STATUS.md` (workflow milestones) and `RESTRUCTURE-TASKS.md` (burndown).",
        "",
        "## Status by PM",
        "",
        "| PM | total | open | approved | answered | authored* | deferred | dropped | denied | rejected | skipped |",
        "|----|------:|-----:|---------:|---------:|----------:|---------:|--------:|-------:|---------:|--------:|",
    ]
    tot = defaultdict(int)
    for lg in ledgers:
        c = _status_counts(lg)
        authored = sum(1 for e in lg["items"].values() if e.get("disposition") == "author")
        for k in ("total", "open", "approved", "answered", "deferred", "dropped", "denied", "rejected", "skipped"):
            tot[k] += c.get(k, 0)
        tot["authored"] += authored
        lines.append(
            f"| {lg['pm']} | {c.get('total',0)} | {c.get('open',0)} | {c.get('approved',0)} | "
            f"{c.get('answered',0)} | {authored} | {c.get('deferred',0)} | {c.get('dropped',0)} | {c.get('denied',0)} | "
            f"{c.get('rejected',0)} | {c.get('skipped',0)} |"
        )
    lines.append(
        f"| **TOTAL** | {tot['total']} | {tot['open']} | {tot['approved']} | {tot['answered']} | "
        f"{tot['authored']} | {tot['deferred']} | {tot['dropped']} | {tot['denied']} | {tot['rejected']} | {tot['skipped']} |"
    )
    lines += ["", "_*authored = gap-fill article written this phase (disposition=author)._",
              "_dropped = gap-fill article the owning PM judged unnecessary; not written and not carried to the follow-up list._", ""]
    for lg in ledgers:
        open_items = [(iid, e) for iid, e in lg["items"].items() if e["status"] not in TERMINAL]
        if not open_items:
            continue
        lines += [f"## {lg['pm']} — {len(open_items)} open", ""]
        for iid, e in sorted(open_items, key=lambda x: (x[1].get("type", ""), x[1].get("target") or "")):
            tgt = e.get("target") or e.get("natural_key", "")
            lines.append(f"- `{iid}` [{e.get('type')}] {tgt} — **{e['status']}**")
        lines += [""]
    # Articles still awaiting their final whole-article read-through sign-off.
    awaiting = []
    for lg in ledgers:
        for e in lg["items"].values():
            if e.get("type") == "read-through" and e.get("status") != "approved":
                awaiting.append((lg["pm"], e.get("target") or "", e.get("status")))
    lines += ["## Articles awaiting final read-through", ""]
    if awaiting:
        lines.append("| PM | Article | Status |")
        lines.append("|----|---------|--------|")
        for pm, tgt, st in sorted(awaiting):
            lines.append(f"| {pm} | `{tgt}` | {st} |")
    else:
        lines.append("_(none — every from-scratch article has a passed read-through)_")
    lines += [""]
    ROLLUP_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✓ wrote {ROLLUP_FILE.relative_to(REPO_ROOT)} ({len(ledgers)} ledgers)")


def cmd_deferred_report(args):
    _require_integration_branch("deferred-report", DEFERRED_FILE)
    ledgers = _all_ledgers()
    rows = []
    for lg in ledgers:
        for iid, e in lg["items"].items():
            if e["status"] == "deferred":
                rows.append((lg["pm"], e.get("target") or e.get("natural_key", ""), iid,
                             e.get("reason") or "", (e.get("history") or [{}])[-1].get("date", "")))
    rows.sort(key=lambda r: (r[0], r[1]))
    lines = [
        "---",
        'title: "KB Restructure — Out-of-Scope Gap-Fill Articles (derived)"',
        'excerpt: "Gap-fill articles a PM marked out of scope for the current restructure, to seed a follow-up project. Regenerated by scripts/pm_review.py deferred-report from pm-review-state/*.json."',
        "---",
        "",
        "# KB Restructure — Out-of-Scope Gap-Fill Articles (derived)",
        "",
        f"**Generated:** {date.today().isoformat()} by `scripts/pm_review.py deferred-report`. **Do not hand-edit.**",
        "",
        "At project end this is the seed list for a follow-up project: gap-fill articles that "
        "could not be written now and were explicitly deferred by their owning PM. Gap-fill "
        "articles a PM judged unnecessary (disposition=drop) are intentionally excluded — a drop "
        "ends the article's life, a defer carries it forward.",
        "",
        f"**Total deferred:** {len(rows)}",
        "",
        "| PM | Intended Article | Item ID | Reason | Deferred |",
        "|----|------------------|---------|--------|----------|",
    ]
    for pm, target, iid, reason, when in rows:
        lines.append(f"| {pm} | `{target}` | `{iid}` | {reason} | {when} |")
    if not rows:
        lines.append("| _(none yet)_ | | | | |")
    DEFERRED_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✓ wrote {DEFERRED_FILE.relative_to(REPO_ROOT)} ({len(rows)} deferred)")


# ── journal (human-readable decision record) + explain (recall) ───────────────

def _render_journal(ledger: dict) -> list:
    """Markdown lines reconstructing what this PM did and why, from the ledger."""
    pm = ledger.get("pm", "?")
    lines = [
        f"## {pm} — review journal",
        "",
        f"**Branch:** `{ledger.get('branch','')}` · **Baseline:** `{ledger.get('baseline_sha') or '—'}`",
        "",
    ]
    sessions = ledger.get("sessions", [])
    if sessions:
        lines += ["### Sessions", ""]
        for s in sessions:
            span = f"{s.get('started','?')} → {s.get('ended') or 'open'}"
            lines.append(f"- `{s['id']}` ({span}) by {s.get('actor','')}"
                         + (f" — {s['summary']}" if s.get("summary") else ""))
            if s.get("items_touched"):
                lines.append(f"  - items: {', '.join(s['items_touched'])}")
            if s.get("commits"):
                lines.append(f"  - commits: {', '.join(s['commits'])}")
        lines += [""]
    decisions = ledger.get("decisions", [])
    if decisions:
        lines += ["### Linked cross-article decisions", ""]
        for d in decisions:
            lines.append(f"- **{d.get('summary','')}** _({d.get('kind','')}, {d.get('date','')})_")
            if d.get("items"):
                lines.append(f"  - items: {', '.join(d['items'])}")
            if d.get("targets"):
                lines.append(f"  - articles: {', '.join('`%s`' % t for t in d['targets'])}")
            if d.get("narrative"):
                lines.append(f"  - why: {d['narrative']}")
        lines += [""]
    lines += ["### Items", ""]
    items = ledger.get("items", {})
    for iid, e in sorted(items.items(), key=lambda x: (x[1].get("type", ""), x[1].get("target") or "")):
        tgt = e.get("target") or e.get("natural_key", "")
        head = f"#### `{iid}` [{e.get('type')}] {tgt} — **{e.get('status')}**"
        if e.get("disposition"):
            head += f" ({e['disposition']})"
        lines.append(head)
        if e.get("source"):
            lines.append(f"- source: {e['source']}")
        if e.get("reason"):
            lines.append(f"- reason: {e['reason']}")
        if e.get("evidence"):
            lines.append(f"- evidence: {e['evidence']}")
        for h in e.get("history", []):
            bits = [h.get("date", ""), h.get("status", "")]
            tail = []
            if h.get("note"):
                tail.append(h["note"])
            if h.get("commit"):
                tail.append(f"commit {h['commit']}")
            if h.get("diff_summary"):
                tail.append(f"diff: {h['diff_summary']}")
            line = f"- {' '.join(b for b in bits if b)} — by {h.get('actor','')}"
            if tail:
                line += " — " + " · ".join(tail)
            lines.append(line)
        lines += [""]
    return lines


def cmd_journal(args):
    if args.all:
        _require_integration_branch("journal --all", JOURNAL_FILE)
        ledgers = _all_ledgers()
        lines = [
            "---",
            'title: "KB Restructure — PM Review Journal (derived)"',
            'excerpt: "Human-readable reconstruction of what every PM did and why during Phase 4.5 review, unioned from pm-review-state/*.json. Regenerated by scripts/pm_review.py journal --all on the integration branch — do not hand-edit."',
            "---",
            "",
            "# KB Restructure — PM Review Journal (derived)",
            "",
            f"**Generated:** {date.today().isoformat()} by `scripts/pm_review.py journal --all`. "
            "**Do not hand-edit** — regenerate after merge-backs.",
            "",
        ]
        for lg in ledgers:
            lines += _render_journal(lg)
            lines += ["---", ""]
        if not ledgers:
            lines += ["_(no PM ledgers yet)_", ""]
        JOURNAL_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"✓ wrote {JOURNAL_FILE.relative_to(REPO_ROOT)} ({len(ledgers)} ledgers)")
        return
    pm, slug = resolve_pm(args.pm)
    ledger = load_ledger(pm, slug)
    STATE_DIR.mkdir(exist_ok=True)
    path = STATE_DIR / f"{slug}.journal.md"
    lines = [f"# PM Review Journal — {pm}", "",
             f"_Generated {date.today().isoformat()} by `pm_review.py journal`. Do not hand-edit._", ""]
    lines += _render_journal(ledger)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✓ wrote {path.relative_to(REPO_ROOT)}")


def cmd_explain(args):
    if not any([args.pm, args.target, args.id, args.decision]):
        sys.exit("error: `explain` needs at least one of --pm / --target / --id / --decision.")
    if args.pm:
        pm, slug = resolve_pm(args.pm)
        ledgers = [load_ledger(pm, slug)]
    else:
        ledgers = _all_ledgers()
    items_out, decisions_out = [], []
    # With only --decision, show the decision records alone; otherwise dump matching items.
    want_items = bool(args.id or args.target or args.pm)
    for lg in ledgers:
        for iid, e in lg.get("items", {}).items():
            if args.id and iid != args.id:
                continue
            if args.target and e.get("target") != args.target:
                continue
            if not want_items:
                continue
            items_out.append({
                "pm": lg.get("pm"), "slug": lg.get("slug"), "id": iid,
                "type": e.get("type"), "target": e.get("target"), "status": e.get("status"),
                "disposition": e.get("disposition"), "reason": e.get("reason"),
                "evidence": e.get("evidence"), "commit": e.get("commit"),
                "source": e.get("source"), "ask_snapshot": e.get("ask_snapshot"),
                "history": e.get("history", []),
            })
        for d in lg.get("decisions", []):
            if (args.decision and d.get("id") == args.decision) \
               or (args.id and args.id in d.get("items", [])) \
               or (args.target and args.target in d.get("targets", [])) \
               or (args.pm and not (args.id or args.target or args.decision)):
                decisions_out.append({"pm": lg.get("pm"), **d})
    print(json.dumps({"items": items_out, "decisions": decisions_out},
                     indent=2, ensure_ascii=False))


# ── reconciliation sweep (the Phase 4.5 -> 4.6 gate) ──────────────────────────

_PM_INPUT_LOOSE = re.compile(r"\[pm-input\]")
_REVIEWED_RE = re.compile(
    r"\{/\*\s*\[reviewed\]\s+pm=(\S+)\s+status=(\S+)\s+date=(\d{4}-\d{2}-\d{2})\s*\*/\}"
)
_READTHROUGH_RE = re.compile(
    r"\{/\*\s*\[read-through\]\s+pm=(\S+)\s+date=(\d{4}-\d{2}-\d{2})\s*\*/\}"
)


def cmd_reconcile(args):
    m = builder()
    article_dir = m.ARTICLE_DIR
    ledgers = _all_ledgers()
    # index every ledger entry by target file for cross-reference
    answered_by_file = defaultdict(int)   # file -> count of terminal 'answered' pm-input entries
    for lg in ledgers:
        for e in lg["items"].values():
            if e.get("type") == "pm-input" and e.get("target") and e.get("status") == "answered":
                answered_by_file[e["target"]] += 1

    well_formed = m.scan_article_pm_inputs(article_dir)        # parseable open markers
    well_by_file = defaultdict(int)
    for c in well_formed:
        well_by_file[c["filename"]] += 1

    stragglers = []       # open marker, no terminal coverage
    malformed = []        # [pm-input] token the parser dropped
    inconsistencies = []  # answered in ledger but marker still present, or [reviewed] w/o backing
    reviewed_ok = 0
    orphan_names = set()

    known = {slugify(pm) for pm in roster()}
    for path in sorted(article_dir.glob("*.mdx")):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        loose = len(_PM_INPUT_LOOSE.findall(text))
        parsed = len(m._PM_INPUT_RE.findall(text))
        if loose > parsed:
            malformed.append((path.name, loose - parsed))
        # open markers vs any terminal coverage recorded for this file
        open_here = well_by_file.get(path.name, 0)
        if open_here and answered_by_file.get(path.name, 0) == 0:
            stragglers.append((path.name, open_here))
        # [reviewed] stamps
        for pm_slug, status, _dt in _REVIEWED_RE.findall(text):
            if slugify(pm_slug) not in known:
                orphan_names.add(pm_slug)
            backed = any(
                any(e.get("status") in TERMINAL and e.get("target") == path.name
                    for e in lg["items"].values())
                for lg in ledgers if slugify(lg["slug"]) == slugify(pm_slug)
            )
            if backed:
                reviewed_ok += 1
            else:
                inconsistencies.append((path.name, f"[reviewed] by {pm_slug}={status} with no backing ledger entry"))
        # also check for marker names that match no PM (open markers)
    for c in well_formed:
        if canonical_pm(c["pm"]) is None:
            orphan_names.add(c["pm"])

    # decision/lifecycle items have no file anchor: list any non-terminal ones
    anchorless_open = []
    for lg in ledgers:
        for iid, e in lg["items"].items():
            if e.get("type") in ("decision", "legacy", "retired") and e["status"] not in TERMINAL:
                anchorless_open.append((lg["pm"], iid, e.get("type"), e["status"]))

    # Read-through checks. Both reuse the SAME attribution function as generation
    # (from_scratch_targets), so they can never flag a file the generator wouldn't
    # also claim. Reported in a separate key and NON-BLOCKING for the first real run
    # (fold into `blocking` only after a clean dry run — see SKILL.md / the plan).
    rt_terminal_without_marker = []   # passed read-through, no [read-through] marker in file
    rt_from_scratch_without_item = [] # from-scratch article with no read-through ledger entry
    for lg in ledgers:
        slug = slugify(lg["slug"])
        for iid, e in lg["items"].items():
            if e.get("type") == "read-through" and e.get("status") in TERMINAL:
                tgt = e.get("target")
                p = (article_dir / tgt) if tgt else None
                has_marker = False
                if p and p.exists():
                    try:
                        txt = p.read_text(encoding="utf-8")
                    except (OSError, UnicodeDecodeError):
                        txt = ""
                    has_marker = any(slugify(ps) == slug for ps, _dt in _READTHROUGH_RE.findall(txt))
                if not has_marker:
                    rt_terminal_without_marker.append((lg["pm"], iid, tgt))
        try:
            normal = regenerate_items(lg["pm"])
        except Exception:
            normal = []
        baseline = lg.get("baseline_sha") or resolve_baseline()
        have_rt = {e.get("target") for e in lg["items"].values() if e.get("type") == "read-through"}
        for tgt in from_scratch_targets(lg["pm"], normal, lg, baseline):
            if tgt not in have_rt:
                rt_from_scratch_without_item.append((lg["pm"], tgt))

    report = {
        "well_formed_open_markers": len(well_formed),
        "reviewed_stamps_backed": reviewed_ok,
        "stragglers": stragglers,
        "malformed_markers": malformed,
        "inconsistencies": inconsistencies,
        "anchorless_open_items": anchorless_open,
        "orphan_marker_pm_names": sorted(orphan_names),
        "read_through_findings": {
            "terminal_without_marker": rt_terminal_without_marker,
            "from_scratch_without_item": rt_from_scratch_without_item,
        },
    }
    blocking = (len(stragglers) + len(malformed) + len(inconsistencies)
                + len(anchorless_open) + len(orphan_names))
    report["gate_clear"] = (blocking == 0)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.strict and blocking:
        sys.exit(1)


def cmd_check_baseline(args):
    # Phase 3c sync is a CONTENT sync, not a git merge, so origin/main is NOT an
    # ancestor of HEAD. Readiness therefore means: a sync baseline has been RECORDED
    # (pm-review-state/sync-baseline.json) and points at a real commit. Per-file review
    # diffs (`git diff <baseline> HEAD -- <file>`) are valid against that SHA regardless
    # of ancestry, because the sync incorporated main's content for the reviewed files.
    sb = load_sync_baseline()
    baseline = resolve_baseline(args.baseline)
    recorded = bool(sb.get("baseline_sha"))
    valid = is_commit(baseline)
    ready = recorded and valid
    head = git("rev-parse", "HEAD").stdout.strip()
    main_tip = git("rev-parse", "--verify", "--quiet", "origin/main", check=False).stdout.strip() or None
    print(json.dumps({
        "baseline_sha": baseline,
        "recorded_sync": sb or None,
        "head": head,
        "is_commit": valid,
        "is_ancestor": is_ancestor(baseline),
        "main_tip": main_tip,
        "main_advanced_since_sync": bool(main_tip and baseline and main_tip != baseline),
        "ready": ready,
        "message": ("baseline recorded + valid — per-file review diffs are valid" if ready else
                    "no recorded sync baseline — run the Phase 3c content sync and record "
                    "pm-review-state/sync-baseline.json before the pm-review skill will run"),
    }, indent=2, ensure_ascii=False))
    if args.strict and not ready:
        sys.exit(2)


# ── argparse ──────────────────────────────────────────────────────────────────

def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("items", help="emit the PM's reconciled worklist (JSON)")
    pi.add_argument("--pm", required=True)
    pi.add_argument("--no-write", action="store_true", help="do not persist ledger changes")
    pi.set_defaults(func=cmd_items)

    pr = sub.add_parser("resume", help="emit the first non-terminal item (JSON)")
    pr.add_argument("--pm", required=True)
    pr.add_argument("--no-write", action="store_true")
    pr.set_defaults(func=cmd_resume)

    ps = sub.add_parser("set-status", help="record a disposition for one item")
    ps.add_argument("--pm", required=True)
    ps.add_argument("--id", required=True)
    ps.add_argument("--status", required=True)
    ps.add_argument("--disposition")
    ps.add_argument("--reason")
    ps.add_argument("--evidence")
    ps.add_argument("--commit")
    ps.add_argument("--actor")
    ps.add_argument("--note", help="WHY (required for terminal statuses); logged to history")
    ps.add_argument("--diff-summary", dest="diff_summary", help="short summary of the edit this commit made")
    ps.add_argument("--baseline", help="pin baseline_sha on first write")
    ps.set_defaults(func=cmd_set_status)

    pss = sub.add_parser("session-start", help="open a review session (closes any dangling one)")
    pss.add_argument("--pm", required=True)
    pss.add_argument("--actor")
    pss.add_argument("--summary")
    pss.set_defaults(func=cmd_session_start)

    pse = sub.add_parser("session-end", help="close the open review session")
    pse.add_argument("--pm", required=True)
    pse.add_argument("--summary")
    pse.set_defaults(func=cmd_session_end)

    pl = sub.add_parser("link", help="record one linked cross-article decision")
    pl.add_argument("--pm", required=True)
    pl.add_argument("--kind", required=True, help="e.g. fold, split, merge, supersede, other")
    pl.add_argument("--summary", required=True)
    pl.add_argument("--items", help="comma-separated item ids this decision ties together")
    pl.add_argument("--targets", help="comma-separated article filenames involved")
    pl.add_argument("--narrative", help="the full reasoning")
    pl.add_argument("--date")
    pl.add_argument("--actor")
    pl.set_defaults(func=cmd_link)

    pj = sub.add_parser("journal", help="render the per-PM (or --all root) decision journal")
    pj.add_argument("--pm")
    pj.add_argument("--all", action="store_true", help="render root PM-REVIEW-JOURNAL.md (INTEGRATION branch only)")
    pj.set_defaults(func=cmd_journal)

    pe = sub.add_parser("explain", help="reconstruct what a PM did and why (read-only)")
    pe.add_argument("--pm")
    pe.add_argument("--target")
    pe.add_argument("--id")
    pe.add_argument("--decision")
    pe.set_defaults(func=cmd_explain)

    pc = sub.add_parser("reconcile", help="marker<->ledger sweep (the 4.5->4.6 gate)")
    pc.add_argument("--pm", help="(informational; the sweep is global by design)")
    pc.add_argument("--strict", action="store_true", help="exit 1 if the gate is not clear")
    pc.set_defaults(func=cmd_reconcile)

    sub.add_parser("rollup", help="regenerate PM-REVIEW-ROLLUP.md").set_defaults(func=cmd_rollup)
    sub.add_parser("deferred-report", help="regenerate RESTRUCTURE-DEFERRED-ARTICLES.md").set_defaults(func=cmd_deferred_report)

    pb = sub.add_parser("check-baseline", help="refuse-to-run guard for the skill")
    pb.add_argument("--baseline")
    pb.add_argument("--strict", action="store_true")
    pb.set_defaults(func=cmd_check_baseline)
    return p


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
