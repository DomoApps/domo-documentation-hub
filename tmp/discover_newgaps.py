#!/usr/bin/env python3
"""Discover candidate NET-NEW doc gaps from support cases not tied to any existing gap.

Excludes every case lexically matched (loose, cosine>=0.12) to an existing forum gap,
then clusters the remainder by normalized topic and ranks clusters by a doc-gap signal
(volume + low answer-confidence + 'documentable resolution' closure reasons), while
down-weighting pure provisioning/service-request clusters.
"""
import json, re, math
from collections import Counter, defaultdict

ROOT = "tmp"
cases = json.load(open(f"{ROOT}/support_cases_summary.json"))
matched = json.load(open(f"{ROOT}/_match_gap_cases.json"))   # {rank: [[idx,score]]}

exclude = set()
for pairs in matched.values():
    for i, _ in pairs:
        exclude.add(i)

DOC_RESOLUTION = {"User needs more training", "Lite Education", "Referral to Knowledge Base"}
# closure reasons / topic markers that indicate a one-off service/provisioning request
# (support just *does* the thing) rather than a documentation gap
SERVICE_CLOSURES = {"Feature Enablement", "Account Team Engagement", "Account Question",
                    "Enhancement Request", "Work Outside Support Scope"}
SERVICE_TOPIC_RX = re.compile(
    r"(deletion|delete|provision|enablement|enable feature|password reset|reset password"
    r"|account access|portal access|university access|billing|invoice|contract|renewal"
    r"|whitelist|ip address|instance management|instance access|migration request)", re.I)

def norm_topic(t):
    t = (t or "").lower().strip()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    t = re.sub(r"\b(issue|issues|error|errors|problem|problems|setup|set up|help|question"
               r"|request|requests|assistance|support|failure|failures|config|configuration)\b", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    # crude singularization
    words = [w[:-1] if (w.endswith("s") and len(w) > 4) else w for w in t.split()]
    return " ".join(words)

clusters = defaultdict(list)
for i, c in enumerate(cases):
    if i in exclude:
        continue
    key = norm_topic(c.get("topic", ""))
    if not key:
        continue
    clusters[key].append(c)

def cluster_stats(cs):
    n = len(cs)
    confs = [c.get("answer_confidence", 0) for c in cs]
    low = sum(1 for c in cs if c.get("answer_confidence", 0) < 0.3)
    docres = sum(1 for c in cs if c.get("closure_reason", "") in DOC_RESOLUTION)
    service = sum(1 for c in cs if c.get("closure_reason", "") in SERVICE_CLOSURES
                  or SERVICE_TOPIC_RX.search(c.get("topic", "")))
    dates = sorted(c["created"][:10] for c in cs if c.get("created"))
    pa = Counter(c.get("product_area", "") for c in cs).most_common(2)
    latest_year = int(dates[-1][:4]) if dates else 2019
    recency = {2026: 1.0, 2025: 0.85, 2024: 0.6, 2023: 0.4}.get(latest_year, 0.25)
    vol = min(1.0, math.log(1 + n) / math.log(1 + 80))
    low_ratio = low / n
    docres_ratio = docres / n
    service_ratio = service / n
    # doc-gap score: reward volume + low-confidence + documentable closures,
    # penalize service/provisioning clusters
    doc_gap = (0.45 * vol + 0.30 * low_ratio + 0.25 * docres_ratio) * (1 - 0.6 * service_ratio) * (0.8 + 0.2 * recency)
    return dict(n=n, avg_conf=round(sum(confs)/n, 2), low_ratio=round(low_ratio, 2),
                docres=docres, docres_ratio=round(docres_ratio, 2),
                service_ratio=round(service_ratio, 2), pa=pa, latest=dates[-1] if dates else "",
                doc_gap=round(doc_gap, 3))

rows = []
for key, cs in clusters.items():
    if len(cs) < 8:    # ignore tiny clusters for the overview
        continue
    rows.append((key, cluster_stats(cs)))

print(f"excluded (tied to existing gaps): {len(exclude)}")
print(f"uncovered cases: {sum(len(v) for v in clusters.values())}")
print(f"clusters >=8 cases: {len(rows)}")
print()
print("=== TOP 45 UNCOVERED CLUSTERS BY DOC-GAP SCORE ===")
print(f"{'score':>6} {'n':>4} {'conf':>4} {'low':>4} {'docr':>4} {'svc':>4}  topic / area")
for key, s in sorted(rows, key=lambda r: r[1]['doc_gap'], reverse=True)[:45]:
    pa = s['pa'][0][0] if s['pa'] else ''
    print(f"{s['doc_gap']:>6.3f} {s['n']:>4} {s['avg_conf']:>4} {s['low_ratio']:>4} "
          f"{s['docres_ratio']:>4} {s['service_ratio']:>4}  {key[:42]:42} [{pa}]")
