#!/usr/bin/env python3
"""Attach a support_signal block to each existing forum gap.

Reads tmp/_match_gap_cases.json (gap rank -> [case idx]) and the raw cases,
computes per-gap support metrics, and writes tmp/_gaps_with_support.json
(the full gaps doc with support_signal + support_strength on each gap).
Also writes tmp/_matched_case_idx.json (set of strongly-matched case indices)
for the new-gap discovery phase.
"""
import json, math
from collections import Counter

ROOT = "tmp"
doc = json.load(open(f"{ROOT}/documentation_gaps_from_forums.json"))
gaps = doc["gaps"]
cases = json.load(open(f"{ROOT}/support_cases_summary.json"))
matched = json.load(open(f"{ROOT}/_match_gap_cases.json"))  # {rank(str): [idx]}

DOC_RESOLUTION = {"User needs more training", "Lite Education", "Referral to Knowledge Base"}

def support_strength(num, low_ratio, doc_ratio):
    vol = min(1.0, math.log(1 + num) / math.log(1 + 60))
    return round(0.50 * vol + 0.30 * low_ratio + 0.20 * doc_ratio, 4)

STRONG = 0.20   # cosine bar for a high-confidence (trustworthy headline) match

all_matched_strong = set()
for g in gaps:
    pairs = matched.get(str(g["rank"]), [])     # [[idx, score], ...] sorted desc
    score_of = {i: s for i, s in pairs}
    strong_idx = [i for i, s in pairs if s >= STRONG]
    loose_idx = [i for i, s in pairs if s < STRONG]
    all_matched_strong.update(strong_idx)
    # Headline metrics are computed over STRONG matches only. If a gap has too few
    # strong matches to be meaningful, we still report the loose count for context.
    cs = [cases[i] for i in strong_idx]
    if not cs:
        g["support_signal"] = {
            "num_cases": 0,
            "loose_related_cases": len(loose_idx),
            "note": "No high-confidence support-case match; "
                    f"{len(loose_idx)} loosely-related case(s) share keywords but were not confidently matched.",
        }
        g["support_strength"] = 0.0
        continue
    confs = [c.get("answer_confidence", 0) for c in cs]
    low = [c for c in cs if c.get("answer_confidence", 0) < 0.3]
    docres = [c for c in cs if c.get("closure_reason", "") in DOC_RESOLUTION]
    dates = sorted(c["created"][:10] for c in cs if c.get("created"))
    prio = Counter(c.get("priority", "") for c in cs)
    pa = Counter(c.get("product_area", "") for c in cs)
    cats = Counter(c.get("category", "") for c in cs)
    low_ratio = len(low) / len(cs)
    doc_ratio = len(docres) / len(cs)
    # representative cases: strongest-matching first, tie-broken toward recent +
    # (low confidence OR elevated priority)
    idx_by_relevance = sorted(strong_idx, key=lambda i: (
        score_of.get(i, 0),
        1 if (cases[i].get("priority") in ("High", "Escalated", "Prod", "Medium")
              or cases[i].get("answer_confidence", 1) < 0.3) else 0,
        cases[i].get("created", "")[:10],
    ), reverse=True)
    reps = [cases[i] for i in idx_by_relevance[:6]]
    g["support_signal"] = {
        "num_cases": len(cs),
        "loose_related_cases": len(loose_idx),
        "date_range": f"{dates[0]} to {dates[-1]}" if dates else "",
        "avg_answer_confidence": round(sum(confs) / len(confs), 3),
        "low_confidence_cases": len(low),
        "low_confidence_ratio": round(low_ratio, 3),
        "documentable_resolution_cases": len(docres),
        "documentable_resolution_note": "closed as 'User needs more training' / 'Lite Education' / 'Referral to Knowledge Base' — i.e. resolvable by docs",
        "priority_breakdown": {k: v for k, v in prio.most_common() if k},
        "top_product_areas": pa.most_common(4),
        "top_categories": cats.most_common(4),
        "representative_cases": [
            {"case_number": c.get("case_number"), "created": c.get("created", "")[:10],
             "topic": c.get("topic"), "priority": c.get("priority"),
             "answer_confidence": c.get("answer_confidence"),
             "closure_reason": c.get("closure_reason"),
             "question_summary": c.get("question_summary")}
            for c in reps
        ],
    }
    g["support_strength"] = support_strength(len(cs), low_ratio, doc_ratio)

all_matched = all_matched_strong

json.dump(doc, open(f"{ROOT}/_gaps_with_support.json", "w"), indent=2)
json.dump(sorted(all_matched), open(f"{ROOT}/_matched_case_idx.json", "w"))

# stats
strengths = sorted((g["support_strength"] for g in gaps), reverse=True)
ncases = sorted((g["support_signal"]["num_cases"] for g in gaps), reverse=True)
print(f"gaps enriched: {len(gaps)}")
print(f"unique cases strongly matched: {len(all_matched)} / {len(cases)}")
print(f"gaps with >=1 support case: {sum(1 for n in ncases if n>0)}")
print(f"gaps with >=10 support cases: {sum(1 for n in ncases if n>=10)}")
print(f"support_strength: max {strengths[0]}, median {strengths[len(strengths)//2]}")
print("\nTop 12 gaps by support volume:")
for g in sorted(gaps, key=lambda x: x['support_signal']['num_cases'], reverse=True)[:12]:
    s = g['support_signal']
    print(f"  #{g['rank']:>3} cases={s['num_cases']:>3} lowconf={s.get('low_confidence_ratio',0):.2f} "
          f"docres={s.get('documentable_resolution_cases',0):>2} str={g['support_strength']:.2f}  {g['topic'][:60]}")
