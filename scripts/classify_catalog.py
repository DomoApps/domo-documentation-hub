#!/usr/bin/env python3
"""
Classify each KB article in catalog.json by Diátaxis type + content category.

Two-pass approach:
  Pass 1: deterministic heuristics (title + excerpt patterns) — fast, no API calls
  Pass 2: Claude Haiku for any article that heuristics mark as "ambiguous"

Outputs scripts/output/catalog-classified.json with a `type` field added:
  tutorial       — learning-oriented, "first time doing X"
  howto          — task-oriented, "how do I accomplish X"
  reference      — factual lookup, properties/functions/glossary
  explanation    — conceptual "what is X / why / how it works"
  connector      — data connector setup article
  release-notes  — monthly/archived release notes
  retire-candidate — stub, deprecated, or superseded

Also adds a `type_confidence` field: "heuristic" | "api" | "manual"

Usage:
    python3 scripts/classify_catalog.py [--catalog scripts/output/catalog.json]
                                        [--out scripts/output/catalog-classified.json]
                                        [--api-limit N]   # max API calls (0 = heuristics only)
                                        [--dry-run]

Requires ANTHROPIC_API_KEY for pass-2 API classification.
"""

import argparse
import json
import os
import re
import sys

CATALOG_IN = "scripts/output/catalog.json"
CATALOG_OUT = "scripts/output/catalog-classified.json"
DEFAULT_API_LIMIT = 200  # cap spend on first run; raise once heuristics are tuned


# ---------------------------------------------------------------------------
# Heuristic patterns (ordered: first match wins)
# ---------------------------------------------------------------------------

PATTERNS = [
    # --- release-notes (most specific first) ---
    ("release-notes", [
        (r"release notes?", "title"),
        (r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b", "title"),
        (r"\b20\d\d\s+release\b", "title"),
        (r"release notes", "excerpt"),
    ]),

    # --- connector (very distinctive) ---
    ("connector", [
        (r"\bconnector\b", "title"),
        (r"\bwriteback\b", "title"),
        (r"^use the .+ connector to (import|pull|retrieve|ingest|sync)", "excerpt"),
        (r"^configure .+ connector", "excerpt"),
        (r"^use domo.s .+ connector", "excerpt"),
    ]),

    # --- reference ---
    ("reference", [
        (r"\breference\b", "title"),
        (r"\bproperties\b", "title"),
        (r"\bfunctions?\b", "title"),
        (r"\bglossary\b", "title"),
        (r"\blist of\b", "title"),
        (r"\bsyntax\b", "title"),
        (r"\bAPI reference\b", "title"),
        (r"\bchart properties\b", "excerpt"),
        (r"reference (list|guide|table|notes)", "excerpt"),
    ]),

    # --- explanation ---
    ("explanation", [
        (r"^(what is|introduction to|overview of|understanding|about)\b", "title"),
        (r"\boverview\b", "title"),
        (r"\bintroduction\b", "title"),
        (r"\bconcepts?\b", "title"),
        (r"\bFAQ\b", "title"),
        (r"\bglossary\b", "title"),
        (r"^overview of", "excerpt"),
        (r"overview (of|for|to)\b", "excerpt"),
    ]),

    # --- tutorial ---
    ("tutorial", [
        (r"^getting started\b", "title"),
        (r"\bquickstart\b", "title"),
        (r"\bfirst steps?\b", "title"),
        (r"\btutorial\b", "title"),
        (r"\bwalks? (you |through\b)", "excerpt"),
        (r"get (up and running|started)", "excerpt"),
    ]),

    # --- howto (broad catch-all for procedural articles) ---
    ("howto", [
        (r"^(use|create|add|configure|set up|manage|build|edit|delete|remove|install|deploy|connect|enable|disable|run|view|find|import|export|upload|download|schedule|monitor|update|send|publish|share|apply|access|submit|integrate|migrate|register|implement|generate|launch|sign in|join|upgrade|power|send|link|wire|design|record|format|duplicate|backup|restore)\b", "title"),
        (r"^how to\b", "title"),
        (r"\bimplementation guide\b", "title"),
        (r"\buser guide\b", "title"),
        (r"domo on (snowflake|redshift|databricks|bigquery|azure|postgresql|mysql|oracle|sap|hana|dremio|athena)", "title"),
        (r"\binstallation guide\b", "title"),
        (r"\bquick start\b", "title"),
        (r"\bstep.by.step\b", "excerpt"),
        (r"^(use|create|add|configure|set up|manage|build|edit|install|deploy|connect|implement|migrate|register|launch|generate|apply|submit)", "excerpt"),
    ]),
]

RETIRE_PATTERNS = [
    (r"\bdeprecated\b", "title"),
    (r"\blegacy\b", "title"),
    (r"\bold magic etl\b", "title"),
    (r"\bworkbench 4\b", "title"),
]


def match_any(text: str, patterns: list[str]) -> bool:
    if not text:
        return False
    t = text.lower()
    return any(re.search(p.lower(), t) for p in patterns)


def heuristic_classify(entry: dict) -> tuple[str, str]:
    """Return (type, confidence) based on title and excerpt patterns."""
    title = (entry.get("title") or "").strip()
    excerpt = (entry.get("excerpt") or "").strip()

    # Check retire candidates first
    if match_any(title, [p for p, _ in RETIRE_PATTERNS]):
        return "retire-candidate", "heuristic"

    for dtype, rules in PATTERNS:
        for pattern, field in rules:
            text = title if field == "title" else excerpt
            if text and re.search(pattern, text, re.IGNORECASE):
                return dtype, "heuristic"

    return "ambiguous", "heuristic"


# ---------------------------------------------------------------------------
# Claude API classification (pass 2)
# ---------------------------------------------------------------------------

def api_classify_batch(entries: list[dict]) -> list[str]:
    """Call Claude Haiku to classify a batch of ambiguous articles."""
    try:
        import anthropic
    except ImportError:
        print("  anthropic package not installed — skipping API classification", file=sys.stderr)
        return ["howto"] * len(entries)

    client = anthropic.Anthropic()

    items_text = "\n".join(
        f'{i+1}. title: {e["title"]!r}\n   excerpt: {(e["excerpt"] or "")[:150]!r}'
        for i, e in enumerate(entries)
    )

    prompt = f"""You are classifying Domo knowledge base articles by Diátaxis documentation type.

Types:
- tutorial: learning-oriented, guides the reader through a skill for the first time ("Getting Started with X", "Your first DataSet")
- howto: task-oriented procedure for already-competent users ("How to add a Beast Mode calculation", "Configure Snowflake connection")
- reference: factual lookup content — properties tables, function lists, API endpoints, glossary entries
- explanation: conceptual "what is X / why / how it works" — background understanding, not procedures
- connector: a data connector setup article (importing data FROM a third-party tool into Domo)
- release-notes: monthly or archived product release notes
- retire-candidate: stub articles, deprecated features, legacy-only content with no current relevance

Classify each article below. Reply with ONLY a JSON array of strings, one type per article, in order.
Valid values: tutorial, howto, reference, explanation, connector, release-notes, retire-candidate

Articles:
{items_text}"""

    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = resp.content[0].text.strip()
    # Extract JSON array
    m = re.search(r"\[.*\]", raw, re.DOTALL)
    if not m:
        return ["howto"] * len(entries)

    try:
        types = json.loads(m.group(0))
        valid = {"tutorial", "howto", "reference", "explanation", "connector", "release-notes", "retire-candidate"}
        return [t if t in valid else "howto" for t in types]
    except Exception:
        return ["howto"] * len(entries)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", default=CATALOG_IN)
    parser.add_argument("--out", default=CATALOG_OUT)
    parser.add_argument("--api-limit", type=int, default=DEFAULT_API_LIMIT,
                        help="Max articles to classify via API (0 = heuristics only)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open(args.catalog, encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"Classifying {len(catalog)} articles (heuristics pass)…")

    ambiguous = []
    for entry in catalog:
        dtype, conf = heuristic_classify(entry)
        entry["type"] = dtype
        entry["type_confidence"] = conf
        if dtype == "ambiguous":
            ambiguous.append(entry)

    print(f"  Heuristic results:")
    counts = {}
    for e in catalog:
        counts[e["type"]] = counts.get(e["type"], 0) + 1
    for t, c in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"    {t:20s} {c}")

    print(f"\n  Ambiguous (need API): {len(ambiguous)}")

    if ambiguous and args.api_limit > 0:
        to_classify = ambiguous[:args.api_limit]
        print(f"  Sending {len(to_classify)} to Claude Haiku in batches of 20…")

        BATCH = 20
        for i in range(0, len(to_classify), BATCH):
            batch = to_classify[i:i + BATCH]
            print(f"    batch {i//BATCH + 1} ({len(batch)} articles)…", flush=True)
            if not args.dry_run:
                types = api_classify_batch(batch)
                for entry, dtype in zip(batch, types):
                    entry["type"] = dtype
                    entry["type_confidence"] = "api"

        # Any remaining ambiguous beyond api_limit → default to howto
        for entry in ambiguous[args.api_limit:]:
            entry["type"] = "howto"
            entry["type_confidence"] = "heuristic-default"

    elif ambiguous:
        print("  API limit is 0 — defaulting ambiguous articles to 'howto'")
        for entry in ambiguous:
            entry["type"] = "howto"
            entry["type_confidence"] = "heuristic-default"

    if not args.dry_run:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        print(f"\nWrote {args.out}")
    else:
        print("\n[dry-run] No file written.")

    # Final tally
    final_counts = {}
    for e in catalog:
        final_counts[e["type"]] = final_counts.get(e["type"], 0) + 1
    print("\nFinal classification:")
    for t, c in sorted(final_counts.items(), key=lambda x: -x[1]):
        print(f"  {t:20s} {c}")


if __name__ == "__main__":
    main()
