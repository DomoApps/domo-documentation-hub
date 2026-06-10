#!/usr/bin/env python3
"""
Phase 1.3 + 1.4: Find orphaned articles, near-duplicate candidates, and content gaps.

Outputs:
  scripts/output/orphans.json          — articles not in docs.json nav
  scripts/output/merge-candidates.json — articles with similar titles (possible duplication)
  scripts/output/gap-analysis.json     — product areas missing tutorial/explanation coverage

Usage:
    python3 scripts/find_duplicates_and_gaps.py
"""

import json
import re
from collections import defaultdict

CATALOG = "scripts/output/catalog-classified.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize(text: str) -> str:
    """Lowercase, strip punctuation/articles for comparison."""
    t = text.lower()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    t = re.sub(r"\b(a|an|the|in|on|for|to|of|and|or|with|using|your)\b", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def token_overlap(a: str, b: str) -> float:
    """Jaccard similarity on word tokens."""
    sa = set(normalize(a).split())
    sb = set(normalize(b).split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


# ---------------------------------------------------------------------------
# Product area extraction
# ---------------------------------------------------------------------------

# Map nav breadcrumb fragments → pillar name
PILLAR_MAP = [
    ("connect", "Connect & Bring In Data"),
    ("cloud data warehouse", "Connect & Bring In Data"),
    ("workbench", "Connect & Bring In Data"),
    ("data provider", "Connect & Bring In Data"),
    ("transform", "Prepare & Transform Data"),
    ("magic etl", "Prepare & Transform Data"),
    ("dataflow", "Prepare & Transform Data"),
    ("data model", "Prepare & Transform Data"),
    ("analyze", "Analyze & Visualize"),
    ("visualiz", "Analyze & Visualize"),
    ("analyzer", "Analyze & Visualize"),
    ("beast mode", "Analyze & Visualize"),
    ("chart", "Analyze & Visualize"),
    ("app studio", "Build Apps & Automate"),
    ("workflow", "Build Apps & Automate"),
    ("code engine", "Build Apps & Automate"),
    ("appstore", "Build Apps & Automate"),
    ("share", "Share & Collaborate"),
    ("publish", "Share & Collaborate"),
    ("buzz", "Share & Collaborate"),
    ("alert", "Share & Collaborate"),
    ("ai", "AI & Data Science"),
    ("data science", "AI & Data Science"),
    ("jupyter", "AI & Data Science"),
    ("automl", "AI & Data Science"),
    ("admin", "Administer & Govern"),
    ("govern", "Administer & Govern"),
    ("security", "Administer & Govern"),
    ("role", "Administer & Govern"),
    ("sandbox", "Administer & Govern"),
    ("api", "Develop & Integrate"),
    ("developer", "Develop & Integrate"),
    ("sdk", "Develop & Integrate"),
    ("getting started", "Getting Started"),
]


def infer_pillar(entry: dict) -> str:
    """Infer which pillar an article belongs to from nav_group + title."""
    text = ((entry.get("nav_group") or "") + " " + (entry.get("title") or "")).lower()
    for fragment, pillar in PILLAR_MAP:
        if fragment in text:
            return pillar
    return "Other"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    with open(CATALOG) as f:
        catalog = json.load(f)

    # --- 1.3a: Orphans ---
    orphans = [
        {"filename": e["filename"], "title": e["title"], "excerpt": e["excerpt"]}
        for e in catalog if not e["in_nav"]
    ]

    with open("scripts/output/orphans.json", "w") as f:
        json.dump(orphans, f, indent=2)
    print(f"Orphaned articles: {len(orphans)}")
    for o in orphans:
        print(f"  {o['filename']} | {o['title']}")

    # --- 1.3b: Near-duplicate detection by title similarity ---
    print("\nScanning for near-duplicate titles (Jaccard >= 0.55)…")
    entries = [(e["filename"], e["title"] or "", e["excerpt"] or "", e["type"]) for e in catalog]
    merge_candidates = []

    # Only compare within same type to keep it manageable
    by_type = defaultdict(list)
    for e in entries:
        by_type[e[3]].append(e)

    for dtype, group in by_type.items():
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                fa, ta, ea, _ = group[i]
                fb, tb, eb, _ = group[j]
                title_sim = token_overlap(ta, tb)
                if title_sim >= 0.55:
                    merge_candidates.append({
                        "article_a": {"filename": fa, "title": ta},
                        "article_b": {"filename": fb, "title": tb},
                        "title_similarity": round(title_sim, 3),
                        "type": dtype,
                        "action": "review-for-merge",
                    })

    # Sort by similarity descending
    merge_candidates.sort(key=lambda x: -x["title_similarity"])

    with open("scripts/output/merge-candidates.json", "w") as f:
        json.dump(merge_candidates, f, indent=2)
    print(f"Merge candidate pairs: {len(merge_candidates)}")
    print("Top 20:")
    for mc in merge_candidates[:20]:
        print(f"  [{mc['title_similarity']:.2f}] {mc['article_a']['title']!r}")
        print(f"         vs {mc['article_b']['title']!r}")

    # --- 1.4: Gap analysis by pillar ---
    print("\n--- Gap Analysis by Pillar ---")

    pillar_data = defaultdict(lambda: {"tutorial": 0, "explanation": 0, "howto": 0,
                                       "reference": 0, "connector": 0, "total": 0})

    for e in catalog:
        if e["type"] in ("release-notes", "retire-candidate"):
            continue
        pillar = infer_pillar(e)
        pillar_data[pillar]["total"] += 1
        if e["type"] in pillar_data[pillar]:
            pillar_data[pillar][e["type"]] += 1

    gaps = []
    for pillar, counts in sorted(pillar_data.items()):
        gap_entry = {
            "pillar": pillar,
            "counts": dict(counts),
            "gaps": [],
        }
        if counts["explanation"] == 0:
            gap_entry["gaps"].append("MISSING: explanation/overview articles ('What is X?')")
        elif counts["explanation"] < 2:
            gap_entry["gaps"].append("LOW: only 1 explanation article — likely needs 'What is X?' + concept articles")
        if counts["tutorial"] == 0:
            gap_entry["gaps"].append("MISSING: tutorial articles ('Getting Started with X')")
        if counts["howto"] < 3:
            gap_entry["gaps"].append("LOW: fewer than 3 how-to articles — may be underdocumented")
        gaps.append(gap_entry)
        print(f"\n  {pillar}")
        print(f"    total={counts['total']}  tutorial={counts['tutorial']}  "
              f"explanation={counts['explanation']}  howto={counts['howto']}  reference={counts['reference']}")
        for g in gap_entry["gaps"]:
            print(f"    ⚠  {g}")

    with open("scripts/output/gap-analysis.json", "w") as f:
        json.dump(gaps, f, indent=2)
    print(f"\nWrote gap-analysis.json ({len(gaps)} pillars analyzed)")


if __name__ == "__main__":
    main()
