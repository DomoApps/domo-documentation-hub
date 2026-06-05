#!/usr/bin/env python3
"""Merge support-derived NET-NEW gaps into the support-enriched forum gaps,
compute a combined forum+support score, re-rank, and write the final file back
to tmp/documentation_gaps_from_forums.json.

Inputs:
  tmp/_gaps_with_support.json     -> 361 forum gaps, each now carrying support_signal + support_strength
  tmp/extract/out/*.json          -> arrays of support-derived candidate gaps (from subagents)
  tmp/support_cases_summary.json  -> raw cases (to enrich new gaps' example cases)
"""
import json, glob, math, os
from collections import Counter

ROOT = "tmp"
doc = json.load(open(f"{ROOT}/_gaps_with_support.json"))
gaps = doc["gaps"]
cases = json.load(open(f"{ROOT}/support_cases_summary.json"))
by_case = {c.get("case_number"): c for c in cases}

DOC_RESOLUTION = {"User needs more training", "Lite Education", "Referral to Knowledge Base"}

# area weight mirrors the spirit of the forum impact model (security/data-correctness heavier)
AREA_WEIGHT = {
    "Governance-Security-Admin": 0.95, "Connectors-Ingestion": 0.85, "Magic-ETL-Dataflows": 0.85,
    "Datasets": 0.85, "BeastMode-Calc-Variables": 0.8, "Charting-Analyzer": 0.75,
    "Dashboards": 0.75, "App-Studio": 0.7, "Workflows": 0.7, "Domo-Everywhere-Embed": 0.8,
    "Reporting-Export": 0.7, "Pro-Code-Jupyter-API": 0.75, "Domo-AI": 0.7, "Other": 0.6,
}
CONF_W = {"high": 1.0, "medium": 0.8, "low": 0.6}

def support_strength(num, low_ratio, doc_ratio):
    vol = min(1.0, math.log(1 + num) / math.log(1 + 60))
    return round(0.50 * vol + 0.30 * low_ratio + 0.20 * doc_ratio, 4)

# ---------- 1. combined score for existing forum gaps ----------
# Preserve original forum rank/score; lift gaps that ALSO carry support signal (max +30%).
for g in gaps:
    g["sources"] = ["forums", "support"] if g.get("support_signal", {}).get("num_cases", 0) > 0 else ["forums"]
    g["forum_score"] = g["score"]
    g["forum_rank"] = g["rank"]
    g["forum_priority"] = g["priority"]          # preserve the original forum-only priority
    s = g.get("support_strength", 0.0)
    g["combined_score"] = round(g["forum_score"] * (1 + 0.15 * s), 2)

# ---------- 2. load + score support-derived new gaps ----------
new_gaps = []
seen_files = sorted(glob.glob(f"{ROOT}/extract/out/*.json"))
for fp in seen_files:
    try:
        arr = json.load(open(fp))
    except Exception as e:
        print(f"WARN: could not parse {fp}: {e}")
        continue
    for cand in arr:
        ex = cand.get("support_case_signal", {}) or {}
        ex_cases = [by_case[cn] for cn in (ex.get("example_cases") or []) if cn in by_case]
        # low-confidence ratio from whatever example cases we can resolve (these are all
        # documentable-resolution cases, so doc_ratio = 1.0)
        if ex_cases:
            low_ratio = sum(1 for c in ex_cases if c.get("answer_confidence", 0) < 0.3) / len(ex_cases)
            dates = sorted(c["created"][:10] for c in ex_cases if c.get("created"))
            date_range = f"{dates[0]} to {dates[-1]}" if dates else ""
            avg_conf = round(sum(c.get("answer_confidence", 0) for c in ex_cases) / len(ex_cases), 3)
        else:
            low_ratio, date_range, avg_conf = 0.15, "", None
        num = int(ex.get("num_cases") or len(ex_cases) or 0)
        strength = support_strength(num, low_ratio, 1.0)
        sev = 1.0 if cand.get("documentation_status") == "none" else 0.6
        impact = AREA_WEIGHT.get(cand.get("category_bucket"), 0.6) * sev * CONF_W.get(cand.get("confidence", "medium"), 0.8)
        combined = round(100 * (0.55 * strength + 0.45 * impact), 2)
        g = {
            "score": combined,
            "combined_score": combined,
            "forum_score": None,
            "forum_rank": None,
            "sources": ["support"],
            "priority": None,  # set after global ranking
            "topic": cand.get("topic"),
            "domo_area": cand.get("domo_area"),
            "category_bucket": cand.get("category_bucket"),
            "description": cand.get("description"),
            "gap_detail": cand.get("gap_detail"),
            "is_feature_request": False,
            "documentation_status": cand.get("documentation_status"),
            "recommendation": cand.get("recommendation"),
            "suggested_location": cand.get("suggested_location"),
            "existing_related_articles": cand.get("existing_related_articles", []),
            "doc_gap_summary": cand.get("doc_gap_summary"),
            "support_strength": strength,
            "support_signal": {
                "num_cases": num,
                "date_range": date_range,
                "avg_answer_confidence": avg_conf,
                "documentable_resolution_cases": num,
                "documentable_resolution_note": "all cases in this cluster were closed as training / Lite Education / KB referral",
                "example_cases": ex.get("example_cases", []),
                "representative_questions": ex.get("representative_questions", []),
                "discovery_confidence": cand.get("confidence"),
            },
        }
        new_gaps.append(g)

print(f"existing forum gaps: {len(gaps)}")
print(f"support-derived new gaps loaded: {len(new_gaps)} from {len(seen_files)} files")

# ---------- 3. merge, re-rank, re-prioritize ----------
allg = gaps + new_gaps
allg.sort(key=lambda g: g["combined_score"], reverse=True)
# priority bands by combined_score, using the EXACT forum thresholds so forum-only
# gaps keep their original priority and only support-corroborated gaps can be elevated.
def band(s):
    if s >= 75: return "Critical"
    if s >= 60: return "High"
    if s >= 45: return "Medium"
    return "Low"
for i, g in enumerate(allg, 1):
    g["rank"] = i
    g["score"] = g["combined_score"]
    g["priority"] = band(g["combined_score"])

doc["gaps"] = allg

# ---------- 4. metadata ----------
m = doc["metadata"]
m["generated_at"] = "2026-06-05"
m["updated"] = "2026-06-05: cross-referenced against Domo support cases; added support-derived net-new gaps"
m["source_scope"]["support_cases"] = {
    "total_cases": len(cases),
    "date_range": "2022-08-26 to 2026-06-03",
    "source_file": "tmp/support_cases_summary.json",
    "note": "Support cases summarized with question/answer summaries, answer_confidence, topic, product_area, priority, and closure_reason.",
}
m["what_this_is"] = ("Topics discussed in the Domo community forums AND/OR surfaced by Domo support cases that are "
                     "MISSING or only PARTIALLY covered in the documentation. Each gap carries forum signal and/or "
                     "support-case signal; support-derived gaps were mined from cases closed as resolvable by docs "
                     "(training / Lite Education / KB referral) and verified against the repo.")
m["support_signal_method"] = ("Each forum gap was matched to support cases via TF-IDF cosine over case "
                              "question_summary/topic/product_area with a rare-anchor-term gate (lexical, approximate). "
                              "support_signal.num_cases counts HIGH-CONFIDENCE matches (cosine>=0.20); "
                              "loose_related_cases counts weaker keyword matches (0.12-0.20). Net-new support gaps were "
                              "extracted from documentable-resolution cases not tied to any forum gap, then repo-verified.")
m["scoring"]["combined"] = ("combined_score = forum_score*(1 + 0.15*support_strength) for forum gaps; "
                            "for support-only gaps, combined_score = 100*(0.55*support_strength + 0.45*impact), "
                            "impact = area_weight * severity(none=1.0,partial=0.6) * discovery_confidence. "
                            "support_strength = 0.50*log-scaled num_cases(cap 60) + 0.30*low_confidence_ratio + 0.20*documentable_resolution_ratio. "
                            "Final list is re-ranked by combined_score. forum_rank/forum_score preserve the original forum-only ranking.")
m["field_notes"]["sources"] = "['forums'] | ['forums','support'] | ['support'] — which signal(s) evidence this gap."
m["field_notes"]["combined_score"] = "drives rank & priority. forum_score/forum_rank/forum_priority preserve the original forum-only values."
m["field_notes"]["priority"] = "banded from combined_score with the forum thresholds (Critical>=75, High>=60, Medium>=45, else Low). Support corroboration can only raise a forum gap's priority, never lower it."
m["field_notes"]["support_signal"] = "forum gaps: high-confidence matched support cases (num_cases) + loose_related_cases, confidence/closure/priority breakdowns, representative_cases. support-derived gaps: cluster size, example_cases, representative_questions, discovery_confidence."
totals = m["totals"]
totals["total_gaps"] = len(allg)
totals["forum_gaps"] = len(gaps)
totals["support_derived_new_gaps"] = len(new_gaps)
totals["by_priority"] = dict(Counter(g["priority"] for g in allg if g.get("priority")))
totals["by_source"] = dict(Counter("+".join(g["sources"]) for g in allg))
totals["by_documentation_status"] = dict(Counter(g.get("documentation_status") for g in allg))
totals["by_recommendation"] = dict(Counter(g.get("recommendation") for g in allg))
totals["feature_requests_included"] = sum(1 for g in allg if g.get("is_feature_request"))

out = f"{ROOT}/documentation_gaps_from_forums.json"
json.dump(doc, open(out, "w"), indent=2, ensure_ascii=False)
print(f"\nwrote {out}")
print("by_priority:", totals["by_priority"])
print("by_source:", totals["by_source"])
print("\nTop 15 after merge:")
for g in allg[:15]:
    src = "+".join(g["sources"])
    print(f"  #{g['rank']:>3} {g['combined_score']:>6.1f} [{src:14}] {g.get('priority',''):8} {g['topic'][:60]}")
print("\nTop support-only gaps:")
for g in [x for x in allg if x['sources'] == ['support']][:12]:
    print(f"  #{g['rank']:>3} {g['combined_score']:>6.1f} {g['documentation_status']:7} {g['topic'][:65]}")
