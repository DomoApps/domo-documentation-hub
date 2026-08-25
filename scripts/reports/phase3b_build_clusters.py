#!/usr/bin/env python3
"""Phase 3b general — build per-agent cluster task files for the forum-gap update pass.

Editable universe = Medium/Low `update` gaps whose target is an existing s/article
or s/topic file. portal/-only gaps and dead-target gaps are deferred (logged).

Outputs:
  scripts/reports/phase3b_clusters/<PM-slug>__<n>.md   one task file per agent cluster
  scripts/reports/phase3b_clusters/_WAVE-PLAN.md        master plan (clusters, files, gaps)
  scripts/reports/phase3b_clusters/_DEFERRED.md         out-of-scope / dead-target gaps
"""
import json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "scripts/reports/phase3b_clusters")
os.makedirs(OUT, exist_ok=True)
MAX_FILES_PER_CLUSTER = 5
MAX_GAPS_PER_CLUSTER = 9

# domo_area substring -> PM, used only when the ownership reference has no entry for
# the target file (newer/renamed overview articles missing from the June snapshot).
# Checked in order; first substring match wins.
AREA_PM_FALLBACK = [
    ("app studio", "Khushboo"), ("office", "Khushboo"),
    ("workbench", "Tasleema Lallmamode"),
    ("jupyter", "Ken Boyer"),
    ("workflow", "Ryan Despain"),
    ("etl", "Andrea Henderson"), ("dataflow", "Andrea Henderson"),
    ("variable", "Chris Wright"), ("charting", "Chris Wright"),
    ("analyzer", "Chris Wright"), ("dashboard", "Chris Wright"),
    ("role", "Dan Brinton"), ("admin", "Dan Brinton"), ("governance", "Dan Brinton"),
    ("dataset", "Jordan Jensen"), ("cli", "Jordan Jensen"), ("api", "Jordan Jensen"),
]

def fallback_pm(domo_area):
    a = (domo_area or "").lower()
    for key, pm in AREA_PM_FALLBACK:
        if key in a:
            return pm
    return "UNASSIGNED"

def ex(p): return os.path.exists(os.path.join(ROOT, p))

# ownership: stem -> {pm, feature, title}
own = {}
with open(os.path.join(ROOT, "Article-PM-Ownership-Reference.mdx")) as f:
    for line in f:
        if not line.startswith("|"): continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 4 or cells[0] == "Feature" or set(cells[0]) <= {"-"}: continue
        feature, title, fname, pm = cells
        own[fname.strip("`").replace(".mdx", "")] = {"pm": pm, "feature": feature, "title": title}

d = json.load(open(os.path.join(ROOT, "_gaps_with_support.json")))
gaps = [g for g in d["gaps"] if g["priority"] in ("Medium", "Low") and g["recommendation"] == "update"]

def editable_target(g):
    """First existing s/article target, else first existing s/topic target, else None."""
    targets = [r["path"] for r in g.get("existing_related_articles", []) if r.get("path")]
    arts = [t for t in targets if t.startswith("s/article/") and ex(t)]
    tops = [t for t in targets if t.startswith("s/topic/") and ex(t)]
    return (arts[0] if arts else (tops[0] if tops else None)), targets

active, deferred = [], []
for g in gaps:
    tgt, all_t = editable_target(g)
    if not tgt:
        deferred.append((g, all_t)); continue
    stem = os.path.basename(tgt).replace(".mdx", "")
    info = own.get(stem, {})
    pm = info.get("pm") or fallback_pm(g["domo_area"])
    active.append({
        "rank": g["rank"], "priority": g["priority"], "score": g["score"],
        "topic": g["topic"], "domo_area": g["domo_area"], "gap_detail": g["gap_detail"],
        "suggested_location": g.get("suggested_location", ""), "target": tgt,
        "all_targets": all_t, "pm": pm,
        "feature": info.get("feature", ""), "title": info.get("title", ""),
    })

# group: pm -> file -> [gaps]
by_pm = collections.defaultdict(lambda: collections.defaultdict(list))
for e in active:
    by_pm[e["pm"]][e["target"]].append(e)

def slug(s): return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")

clusters = []  # (cluster_id, pm, {file:[gaps]})
for pm in sorted(by_pm, key=lambda p: -len(by_pm[p])):
    files = by_pm[pm]
    # order files by domo_area so a cluster is topically coherent
    ordered = sorted(files, key=lambda f: (files[f][0]["domo_area"], f))
    cur, cur_gaps, n = [], 0, 0
    def emit(chunk):
        global n
        n += 1
        cid = f"{slug(pm)}__{n}"
        clusters.append((cid, pm, {f: files[f] for f in chunk}))
    for f in ordered:
        g = len(files[f])
        if cur and (len(cur) >= MAX_FILES_PER_CLUSTER or cur_gaps + g > MAX_GAPS_PER_CLUSTER):
            emit(cur); cur, cur_gaps = [], 0
        cur.append(f); cur_gaps += g
    if cur:
        emit(cur)

# write cluster task files
for cid, pm, files in clusters:
    lines = [f"# Phase 3b cluster: {cid}", "", f"**Owning PM:** {pm}",
             f"**Files in this cluster:** {len(files)}  |  "
             f"**Gaps:** {sum(len(v) for v in files.values())}", "",
             "Edit ONLY the files listed below. Each file gets the forum-gap additions "
             "described under it. Follow the shared agent instructions (3 quality gates, "
             "[pm-input] deferral, no TODO markers, imperative Title Case, English-only, "
             "no Next Steps/Related links — that is Phase 5).", "", "---", ""]
    for f in sorted(files):
        gs = files[f]
        lines += [f"## `{f}`", f"*{gs[0].get('title','')}* — area: {gs[0]['domo_area']}", ""]
        for g in sorted(gs, key=lambda x: -x["score"]):
            lines += [f"### Gap rank {g['rank']} ({g['priority']}, score {g['score']}) — {g['topic']}",
                      f"- **What's missing:** {g['gap_detail']}",
                      f"- **Suggested location:** {g['suggested_location']}", ""]
            other = [t for t in g["all_targets"] if t != f]
            if other:
                lines.append(f"- **Other referenced articles:** {', '.join(other)}")
                lines.append("")
        lines += ["---", ""]
    open(os.path.join(OUT, f"{cid}.md"), "w").write("\n".join(lines))

# wave plan
wp = ["# Phase 3b general — Forum-Gap Update Wave Plan", "",
      f"Active gaps: {len(active)}  |  Clusters (agents): {len(clusters)}  |  "
      f"Deferred: {len(deferred)}", "",
      f"Suggested wave size: ~10 parallel agents.  Waves: {(len(clusters)+9)//10}", "",
      "| Cluster | PM | Files | Gaps |", "|---|---|---|---|"]
for cid, pm, files in clusters:
    wp.append(f"| `{cid}` | {pm} | {len(files)} | {sum(len(v) for v in files.values())} |")
open(os.path.join(OUT, "_WAVE-PLAN.md"), "w").write("\n".join(wp))

# deferred log
dl = ["# Phase 3b — Deferred Medium/Low update gaps (out of scope for this pass)", "",
      "portal/-only targets (portal/ is out of restructure scope) or no live KB target.", ""]
for g, all_t in sorted(deferred, key=lambda x: -x[0]["score"]):
    dl.append(f"- **rank {g['rank']}** ({g['priority']}, {g['score']}) {g['topic']}  "
              f"→ targets: {', '.join(all_t) or 'none'}")
open(os.path.join(OUT, "_DEFERRED.md"), "w").write("\n".join(dl))

print(f"Active gaps: {len(active)}  |  Deferred: {len(deferred)}")
print(f"Clusters (agents): {len(clusters)}  |  Waves @10: {(len(clusters)+9)//10}\n")
print(f"{'Cluster':28} {'PM':22} {'files':>5} {'gaps':>5}")
print("-" * 64)
for cid, pm, files in clusters:
    print(f"{cid:28} {pm:22} {len(files):>5} {sum(len(v) for v in files.values()):>5}")
print(f"\nWrote {len(clusters)} cluster files + _WAVE-PLAN.md + _DEFERRED.md to {OUT}")
