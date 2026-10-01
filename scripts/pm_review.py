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
             [--evidence E] [--commit SHA] [--actor A]
                                     Record a disposition for one item.
  reconcile [--pm NAME]             Marker <-> ledger sweep (the Phase 4.5->4.6 gate).
  rollup                            Regenerate PM-REVIEW-ROLLUP.md from all ledgers.
  deferred-report                   Regenerate RESTRUCTURE-DEFERRED-ARTICLES.md.
  check-baseline [--baseline SHA]   Report whether the diff baseline is an ancestor
                                     of HEAD (the skill's refuse-to-run guard).

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
INTEGRATION_BRANCH = "update/fullRestructure"

TYPE_ORDER = ["fact-check", "pm-input", "legacy", "retired", "update", "decision"]
TYPE_PREFIX = {
    "fact-check": "fc", "pm-input": "pmi", "legacy": "life",
    "retired": "ret", "update": "upd", "decision": "dec",
}
TERMINAL = {"approved", "denied", "rejected", "answered", "deferred"}
NONTERMINAL = {"pending", "rewrite-redo", "skipped"}
SCHEMA_VERSION = 1

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
        "items": {},
    }


def load_ledger(pm_name: str, slug: str) -> dict:
    p = ledger_path(slug)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
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
    items = regenerate_items(pm)
    ledger = load_ledger(pm, slug)
    new_ids, stale = sync_ledger(ledger, items)
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
    items = regenerate_items(pm)
    ledger = load_ledger(pm, slug)
    sync_ledger(ledger, items)
    if not args.no_write:
        save_ledger(ledger)
    ordered = sorted(items, key=lambda i: (TYPE_ORDER.index(i["type"]), i["target"] or "", i["occurrence"]))
    for it in ordered:
        if ledger["items"][it["id"]]["status"] not in TERMINAL and ledger["items"][it["id"]]["status"] != "skipped":
            print(json.dumps({"pm": pm, "slug": slug, "next": {**it, "status": ledger["items"][it["id"]]["status"]},
                              "counts": _status_counts(ledger)}, indent=2, ensure_ascii=False))
            return
    # then surface skipped (come-back items)
    for it in ordered:
        if ledger["items"][it["id"]]["status"] == "skipped":
            print(json.dumps({"pm": pm, "slug": slug, "next": {**it, "status": "skipped"},
                              "counts": _status_counts(ledger)}, indent=2, ensure_ascii=False))
            return
    print(json.dumps({"pm": pm, "slug": slug, "next": None, "done": True,
                      "counts": _status_counts(ledger)}, indent=2, ensure_ascii=False))


def cmd_set_status(args):
    pm, slug = resolve_pm(args.pm)
    status = args.status
    if status not in TERMINAL | NONTERMINAL:
        sys.exit(f"error: invalid status '{status}'. Valid: {sorted(TERMINAL | NONTERMINAL)}")
    items = regenerate_items(pm)
    ledger = load_ledger(pm, slug)
    sync_ledger(ledger, items)
    entry = ledger["items"].get(args.id)
    if entry is None:
        sys.exit(f"error: item id '{args.id}' not found for {pm}. Run `items --pm \"{pm}\"` to list.")
    entry["status"] = status
    if args.disposition:
        entry["disposition"] = args.disposition
    if args.reason is not None:
        entry["reason"] = args.reason
    if args.evidence is not None:
        entry["evidence"] = args.evidence
    if args.commit:
        entry["commit"] = args.commit
    entry.setdefault("history", []).append({
        "date": date.today().isoformat(), "status": status,
        "actor": args.actor or slug,
    })
    if ledger.get("baseline_sha") is None and args.baseline:
        ledger["baseline_sha"] = args.baseline
    save_ledger(ledger)
    print(json.dumps({"ok": True, "id": args.id, "status": status,
                      "counts": _status_counts(ledger)}, indent=2, ensure_ascii=False))


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
        "| PM | total | open | approved | answered | authored* | deferred | denied | rejected | skipped |",
        "|----|------:|-----:|---------:|---------:|----------:|---------:|-------:|---------:|--------:|",
    ]
    tot = defaultdict(int)
    for lg in ledgers:
        c = _status_counts(lg)
        authored = sum(1 for e in lg["items"].values() if e.get("disposition") == "author")
        for k in ("total", "open", "approved", "answered", "deferred", "denied", "rejected", "skipped"):
            tot[k] += c.get(k, 0)
        tot["authored"] += authored
        lines.append(
            f"| {lg['pm']} | {c.get('total',0)} | {c.get('open',0)} | {c.get('approved',0)} | "
            f"{c.get('answered',0)} | {authored} | {c.get('deferred',0)} | {c.get('denied',0)} | "
            f"{c.get('rejected',0)} | {c.get('skipped',0)} |"
        )
    lines.append(
        f"| **TOTAL** | {tot['total']} | {tot['open']} | {tot['approved']} | {tot['answered']} | "
        f"{tot['authored']} | {tot['deferred']} | {tot['denied']} | {tot['rejected']} | {tot['skipped']} |"
    )
    lines += ["", "_*authored = gap-fill article written this phase (disposition=author)._", ""]
    for lg in ledgers:
        open_items = [(iid, e) for iid, e in lg["items"].items() if e["status"] not in TERMINAL]
        if not open_items:
            continue
        lines += [f"## {lg['pm']} — {len(open_items)} open", ""]
        for iid, e in sorted(open_items, key=lambda x: (x[1].get("type", ""), x[1].get("target") or "")):
            tgt = e.get("target") or e.get("natural_key", "")
            lines.append(f"- `{iid}` [{e.get('type')}] {tgt} — **{e['status']}**")
        lines += [""]
    ROLLUP_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✓ wrote {ROLLUP_FILE.relative_to(REPO_ROOT)} ({len(ledgers)} ledgers)")


def cmd_deferred_report(args):
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
        "could not be written now and were explicitly deferred by their owning PM.",
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


# ── reconciliation sweep (the Phase 4.5 -> 4.6 gate) ──────────────────────────

_PM_INPUT_LOOSE = re.compile(r"\[pm-input\]")
_REVIEWED_RE = re.compile(
    r"\{/\*\s*\[reviewed\]\s+pm=(\S+)\s+status=(\S+)\s+date=(\d{4}-\d{2}-\d{2})\s*\*/\}"
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

    report = {
        "well_formed_open_markers": len(well_formed),
        "reviewed_stamps_backed": reviewed_ok,
        "stragglers": stragglers,
        "malformed_markers": malformed,
        "inconsistencies": inconsistencies,
        "anchorless_open_items": anchorless_open,
        "orphan_marker_pm_names": sorted(orphan_names),
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
    ps.add_argument("--baseline", help="pin baseline_sha on first write")
    ps.set_defaults(func=cmd_set_status)

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
