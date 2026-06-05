#!/usr/bin/env python3
"""Write per-product-area input files of documentable-uncovered support cases,
for extraction subagents to mine specific recurring doc-gap topics."""
import json, os
from collections import defaultdict

ROOT = "tmp"
cases = json.load(open(f"{ROOT}/support_cases_summary.json"))
matched = json.load(open(f"{ROOT}/_match_gap_cases.json"))
exclude = set(i for pairs in matched.values() for i, _ in pairs)
DOC = {"User needs more training", "Lite Education", "Referral to Knowledge Base"}

by_area = defaultdict(list)
for i, c in enumerate(cases):
    if i in exclude:
        continue
    if c.get("closure_reason") not in DOC:
        continue
    by_area[c.get("product_area", "Other")].append({
        "case": c.get("case_number"),
        "topic": c.get("topic"),
        "conf": c.get("answer_confidence"),
        "q": c.get("question_summary"),
        "a": (c.get("answer_summary") or "")[:240],
    })

os.makedirs(f"{ROOT}/extract", exist_ok=True)
slug = lambda s: s.replace("/", "-").replace(" ", "_")
index = {}
for area, items in sorted(by_area.items(), key=lambda kv: -len(kv[1])):
    fn = f"{ROOT}/extract/{slug(area)}.jsonl"
    with open(fn, "w") as f:
        for it in items:
            f.write(json.dumps(it) + "\n")
    index[area] = {"file": fn, "n": len(items)}
    print(f"{len(items):5}  {area:22} -> {fn}")
json.dump(index, open(f"{ROOT}/extract/_index.json", "w"), indent=2)
