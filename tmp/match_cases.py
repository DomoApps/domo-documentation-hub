#!/usr/bin/env python3
"""Match support cases to existing forum gaps via TF-IDF cosine + area filter.

Outputs:
  tmp/_match_gap_cases.json  -> {gap_rank: [case_idx, ...]} matched case indices per gap
  tmp/_match_debug.json      -> per-gap top matches with scores (for spot-checking)
Also prints coverage stats and a few sample gap->case matches.
"""
import json, re, math
from collections import Counter, defaultdict

ROOT = "tmp"
gaps = json.load(open(f"{ROOT}/documentation_gaps_from_forums.json"))["gaps"]
cases = json.load(open(f"{ROOT}/support_cases_summary.json"))

STOP = set("""a an and are as at be by for from has have how i if in into is it its of on or
that the their them then there these this to was were what when where which who will with your you
can could should would may might do does did not no yes need needs needed want wants get gets getting
able about after also any been being but more most other our out over so some such than they we via
domo customer user users using use used able issue issues error errors help unable trying tries within
question asking wants ability understand also like would when set setting""".split())

WORD = re.compile(r"[a-z0-9]+")

def toks(text):
    return [w for w in WORD.findall((text or "").lower()) if len(w) >= 3 and w not in STOP]

def bigrams(tokens):
    return [tokens[i] + "_" + tokens[i+1] for i in range(len(tokens) - 1)]

# ---- Build case corpus ----
case_text = []
for c in cases:
    t = " ".join([c.get("question_summary", ""), c.get("topic", ""), c.get("topic", ""),
                  c.get("product_area", "")])
    case_text.append(t)

case_tokens = []
for t in case_text:
    tk = toks(t)
    tk = tk + bigrams(tk)
    case_tokens.append(tk)

N = len(cases)
df = Counter()
for tk in case_tokens:
    for w in set(tk):
        df[w] += 1
idf = {w: math.log(1 + N / (1 + c)) for w, c in df.items()}

# inverted index token -> set(case idx) ; only index reasonably distinctive tokens
inv = defaultdict(list)
for i, tk in enumerate(case_tokens):
    for w in set(tk):
        if df[w] <= 0.30 * N:   # drop ultra-common tokens
            inv[w].append(i)

# case tf-idf norms (over indexed tokens)
case_vec = []
case_norm = []
for tk in case_tokens:
    tf = Counter(w for w in tk if w in idf and df[w] <= 0.30 * N)
    v = {w: (1 + math.log(c)) * idf[w] for w, c in tf.items()}
    case_vec.append(v)
    case_norm.append(math.sqrt(sum(x * x for x in v.values())) or 1.0)

# ---- Area compatibility: gap category_bucket -> allowed support product_area set ----
AREA = {
    "Connectors-Ingestion": {"Connectors", "Datasets/ETL", "Other"},
    "Magic-ETL-Dataflows": {"Datasets/ETL", "Beast Mode", "Other"},
    "Datasets": {"Datasets/ETL", "Connectors", "Admin/Governance", "Other"},
    "Governance-Security-Admin": {"Admin/Governance", "Auth/SSO", "Billing/Account", "Other"},
    "Pro-Code-Jupyter-API": {"Developer/APIs", "Apps/AppStudio", "Datasets/ETL", "Other"},
    "BeastMode-Calc-Variables": {"Beast Mode", "Cards/Analyzer", "Datasets/ETL", "Other"},
    "Charting-Analyzer": {"Cards/Analyzer", "Beast Mode", "Other"},
    "App-Studio": {"Apps/AppStudio", "Cards/Analyzer", "Embed/Publish", "Other"},
    "Workflows": {"Workflows/Automation", "Apps/AppStudio", "Other"},
    "Domo-Everywhere-Embed": {"Embed/Publish", "Apps/AppStudio", "Auth/SSO", "Other"},
    "Reporting-Export": {"Cards/Analyzer", "Admin/Governance", "Other"},
    "Dashboards": {"Cards/Analyzer", "Apps/AppStudio", "Other"},
    "Domo-AI": {"Cards/Analyzer", "Apps/AppStudio", "Datasets/ETL", "Other"},
    "Other": None,  # no restriction
}

DISTINCT_CAP = 0.04 * N    # "distinctive": appears in <= 4% of cases
RARE_CAP = 0.015 * N       # "rare anchor": appears in <= 1.5% of cases (~365)

def gap_query(g):
    # Build ONLY from the specific fields (topic + source-post titles + area).
    # gap_detail/description are intentionally excluded: they add common words
    # that dilute narrow-topic queries and cause over-matching.
    parts = []
    parts += toks(g.get("topic", "")) * 3
    parts += toks(g.get("domo_area", "")) * 1
    for sp in g.get("source_posts", []):
        parts += toks(sp.get("title", "")) * 2
    base = toks(g.get("topic", "")) + [w for sp in g.get("source_posts", []) for w in toks(sp.get("title", ""))]
    parts += bigrams(base) * 3
    tf = Counter(w for w in parts if w in idf and df[w] <= 0.30 * N)
    return {w: (1 + math.log(c)) * idf[w] for w, c in tf.items()}

THRESH = 0.12         # cosine threshold
MIN_TERMS = 2         # min shared terms overall
MIN_DISTINCT = 2      # min shared *distinctive* terms (df <= DISTINCT_CAP)
MIN_RARE = 1          # min shared *rare anchor* terms (df <= RARE_CAP)
matched = {}        # gap_rank -> [case_idx]
debug = {}
case_matched = set()

for g in gaps:
    q = gap_query(g)
    qnorm = math.sqrt(sum(x * x for x in q.values())) or 1.0
    allowed = AREA.get(g.get("category_bucket"))
    # gather candidate cases
    cand = defaultdict(float)
    cand_terms = defaultdict(int)
    cand_distinct = defaultdict(int)
    cand_rare = defaultdict(int)
    for w, qw in q.items():
        dfw = df.get(w, N)
        distinctive = dfw <= DISTINCT_CAP
        rare = dfw <= RARE_CAP
        for i in inv.get(w, ()):
            cand[i] += qw * case_vec[i].get(w, 0.0)
            cand_terms[i] += 1
            if distinctive:
                cand_distinct[i] += 1
            if rare:
                cand_rare[i] += 1
    scored = []
    for i, dot in cand.items():
        if (cand_terms[i] < MIN_TERMS or cand_distinct[i] < MIN_DISTINCT
                or cand_rare[i] < MIN_RARE):
            continue
        cos = dot / (qnorm * case_norm[i])
        # area penalty
        if allowed is not None and cases[i].get("product_area") not in allowed:
            cos *= 0.45
        if cos >= THRESH:
            scored.append((round(cos, 4), i))
    scored.sort(reverse=True)
    matched[g["rank"]] = [[i, s] for s, i in scored]   # [case_idx, score]
    case_matched.update(i for _, i in scored)
    debug[g["rank"]] = {
        "topic": g["topic"],
        "category_bucket": g["category_bucket"],
        "n_matched": len(scored),
        "top": [{"score": round(s, 3), "pa": cases[i]["product_area"],
                 "topic": cases[i]["topic"], "q": cases[i]["question_summary"][:140]}
                for s, i in scored[:6]],
    }

json.dump(matched, open(f"{ROOT}/_match_gap_cases.json", "w"))
json.dump(debug, open(f"{ROOT}/_match_debug.json", "w"), indent=2)

# ---- stats ----
counts = sorted((len(v) for v in matched.values()))
total_matched_links = sum(len(v) for v in matched.values())
print(f"gaps: {len(gaps)}")
print(f"cases total: {N}")
print(f"unique cases matched to >=1 gap: {len(case_matched)} ({100*len(case_matched)/N:.1f}%)")
print(f"total gap<->case links: {total_matched_links}")
print(f"matched-per-gap: min {counts[0]}, median {counts[len(counts)//2]}, "
      f"p90 {counts[int(len(counts)*0.9)]}, max {counts[-1]}")
print(f"gaps with 0 matches: {sum(1 for c in counts if c==0)}")
print(f"gaps with >=3 matches: {sum(1 for c in counts if c>=3)}")
