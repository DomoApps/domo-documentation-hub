#!/usr/bin/env python3
"""Phase 3b general — build the Medium/Low forum-gap update work plan.

Reads _gaps_with_support.json (Medium+Low, recommendation=update), maps each
gap's primary target article to its owning PM via Article-PM-Ownership-Reference.mdx,
and emits a clustered work plan for the parallel-agent batch pass.
"""
import json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 1. filename-stem -> {pm, feature, title} from the ownership reference
own = {}
ref = os.path.join(ROOT, "Article-PM-Ownership-Reference.mdx")
with open(ref) as f:
    for line in f:
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 4 or cells[0] == "Feature" or set(cells[0]) <= {"-"}:
            continue
        feature, title, fname, pm = cells
        stem = fname.strip("`").replace(".mdx", "")
        own[stem] = {"pm": pm, "feature": feature, "title": title}

# 2. Medium/Low update gaps -> primary existing target + PM
d = json.load(open(os.path.join(ROOT, "_gaps_with_support.json")))
gaps = [g for g in d["gaps"]
        if g["priority"] in ("Medium", "Low") and g["recommendation"] == "update"]

def existing(path):
    return os.path.exists(os.path.join(ROOT, path))

by_pm = collections.defaultdict(list)      # pm -> list of gap entries
unassigned = []                             # gaps whose target file has no PM / no existing file
for g in gaps:
    targets = [r["path"] for r in g.get("existing_related_articles", []) if r.get("path")]
    existing_targets = [t for t in targets if existing(t)]
    primary = existing_targets[0] if existing_targets else (targets[0] if targets else None)
    stem = os.path.basename(primary).replace(".mdx", "") if primary else None
    info = own.get(stem, {})
    pm = info.get("pm", "UNASSIGNED")
    entry = {
        "rank": g["rank"], "priority": g["priority"], "score": g["score"],
        "topic": g["topic"], "domo_area": g["domo_area"],
        "gap_detail": g["gap_detail"], "suggested_location": g.get("suggested_location", ""),
        "primary_target": primary, "primary_exists": bool(existing_targets),
        "all_targets": targets, "pm": pm, "feature": info.get("feature", ""),
    }
    (by_pm[pm] if primary and existing_targets else unassigned).append(entry)
    if not (primary and existing_targets):
        entry["_reason"] = "no existing target file" if not existing_targets else "no target"

# 3. Emit JSON + a human-readable cluster summary
out_json = os.path.join(ROOT, "scripts/reports/phase3b_gap_plan.json")
json.dump({"by_pm": by_pm, "unassigned": unassigned}, open(out_json, "w"), indent=2)

print(f"Total Medium/Low update gaps: {len(gaps)}")
print(f"Assigned to a PM (with existing target): {sum(len(v) for v in by_pm.values())}")
print(f"Unassigned / no existing target: {len(unassigned)}\n")
print(f"{'PM':22} {'gaps':>5} {'files':>6}")
print("-" * 36)
for pm in sorted(by_pm, key=lambda p: -len(by_pm[p])):
    files = len({e["primary_target"] for e in by_pm[pm]})
    print(f"{pm:22} {len(by_pm[pm]):>5} {files:>6}")
if unassigned:
    print(f"\n{'UNASSIGNED':22} {len(unassigned):>5}")
print(f"\nWrote {out_json}")
