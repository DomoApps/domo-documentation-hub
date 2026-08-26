#!/usr/bin/env python3
"""Phase 3b general — build re-route cluster task files.

Gaps that Wave 1-4 agents correctly skipped because the gap data mislinked them
to the wrong article. Each is re-homed to its correct KB target (verified to
exist). Grouped into 3 collision-free clusters by product area.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "scripts/reports/phase3b_clusters")
gaps = {g["rank"]: g for g in json.load(open(os.path.join(ROOT, "_gaps_with_support.json")))["gaps"]}

# cluster_id -> list of (home_file, pm, [ (rank, routing_note) ])
CLUSTERS = {
    "reroute__1-charting": [
        ("s/article/360043429793.mdx", "Chris Wright", [
            (115, "Was mislinked to the Tables-properties article. This is 'Properties Available for Most Charts' — add Maximum Items top-N + rotate/overlap data labels + Trellis parts here; pie-specific Maximum Items/'Other'/donut-center goes to 360042925314."),
            (120, "Was mislinked to Tables. Add time-scale (Category Scale X) + Trellis date-settings content here."),
            (178, "Was mislinked to Tables. Add Y-axis Goal / Scale Marker (static + dynamic goal line) content here."),
        ]),
        ("s/article/360042925314.mdx", "Chris Wright", [
            (115, "Pie-specific portion only: Maximum Items + 'Other' bucketing, donut center total via Legend Position=Inside."),
        ]),
        ("s/article/360043429473.mdx", "Chris Wright", [
            (323, "Pivot Table chart-type article (was pointed at the aggregated-Beast-Mode article 000005559). Add the HTML-link-column expand/collapse limitation note here."),
        ]),
        ("s/article/360043437813.mdx", "Chris Wright", [
            (356, "Export Visualization Cards (was pointed at the Tables-properties article). Add pivot Excel-export column-width / frozen-panes guidance. NOTE: this file already got gaps 256/360 in Wave 2 — read current state, add only the 356 content."),
        ]),
        ("s/article/360043428253.mdx", "Chris Wright", [
            (135, "Manage Dashboards (was pointed at Beast Mode Manager). Add move/detach sub-dashboard between parents / to Top Level. NOTE: already got gap 334 in Wave 2 — add only 135 content."),
        ]),
    ],
    "reroute__2-data-etl": [
        ("s/article/360042923134.mdx", "Andrea Henderson", [
            (181, "Copying a DataFlow (was pointed at the unique-key-join article). Add dataset/dataflow lineage replication for dev/prod + bulk source swapping."),
        ]),
        ("s/article/4405337525783.mdx", "Andrea Henderson", [
            (289, "Data Fundamentals — join/differing-granularity HALF ONLY (the CASE reclassification half was already done in 360042925434). Add: aggregate finer set with a DataSet View, then join in Magic ETL."),
        ]),
        ("s/article/What-is-Magic-ETL.mdx", "Andrea Henderson", [
            (339, "Magic ETL overview (was pointed at Create a Beast Mode Calculation). Add access-prerequisites note (role/grants) + referenced-cloud-connector-dataset dependency error."),
        ]),
        ("s/article/360046074774.mdx", "Phil Fuchs", [
            (231, "Manage DataSet Views (was pointed at the Virtual DataSets article). Add Dataset Views join/blend limitations (same-type join, UNION, Cloud Amplifier). NOTE: already got gaps 271/347 in Wave 3 — add only 231 content."),
        ]),
        ("s/article/360043439313.mdx", "Dan Brinton", [
            (157, "DomoStats - Projects and Tasks (was pointed at the Activity Log app article). Add field limitations: no start date, no priority/estimation, Tags absent from Tasks dataset. Likely needs a [pm-input] for the unverifiable field-absence specifics."),
        ]),
    ],
    "reroute__3-connectors-gov": [
        ("s/article/360042931954.mdx", "Tasleema Lallmamode", [
            (193, "DataSet via Email connector (was pointed at a Pinterest connector). Add subject/attachment regex, CSV vs CSV-UTF-8 encoding, sender identification."),
        ]),
        ("s/article/360042933494.mdx", "Tasleema Lallmamode", [
            (314, "Campaigns App User Guide (was pointed at a Campaigns date-format reference). Add re-subscribe-after-unsubscribe / manual removal from unsubscribers list. Likely [pm-input] — mechanic not documented in KB."),
        ]),
        ("s/article/360042932414.mdx", "Tasleema Lallmamode", [
            (234, "NetSuite Writeback connector — writeback object/transform reference HALF ONLY (the SuiteAnalytics Upsert/date parts were done in 360043433453). Add writeback-specific object/transform reference."),
        ]),
        ("s/article/360043438213.mdx", "Dan Brinton", [
            (200, "Troubleshoot Single Sign-On Using SAML (the SCIM article 000005241 was the wrong home; the inferred 360042934374 does not exist). Add the two-certificate distinction (IdP-needs vs from-IdP) and which cert expiration affects SAML auth-request signing. Likely [pm-input] for the cert mechanics."),
        ]),
        ("s/article/360043438473.mdx", "Jordan Jensen", [
            (179, "CourseBuilder YouTube-embed portion ONLY (edit/import halves were handled in 360042935714). This 'Best Practices for Using CourseBuilder' article documents Video IDs / provider selection. Correct the guidance: CourseBuilder uses the video ID from a youtube.com/watch?v=ID URL via a provider selector, NOT an /embed/ URL. Flag 'YouTube not showing' as a possible bug via [pm-input]."),
        ]),
    ],
    "reroute__4-embed-office": [
        ("s/article/360042932994.mdx", "Chris Wright", [
            (353, "Sharing and Removing Access to Cards and Dashboards (was pointed at the embed-only filter reference 4418999855639). Add the in-app deep-link how-to: pfilter URL construction + object-ID-based page/card linking (distinct from embed-only pfilters)."),
        ]),
        ("s/article/000005143.mdx", "Khushboo", [
            (121, "Office Add-In User Guide (was pointed at the install-only guide 000005146). Add/confirm add-in usage behavior: PowerPoint one-card-per-slide, slide layout/ordering, image resolution, 100-row import preview. Much may already be covered — read first and add only genuinely new items; defer relative-date-filtering roadmap / Excel re-import-in-place / Google Slides via [pm-input]."),
        ]),
    ],
}

def exists(p): return os.path.exists(os.path.join(ROOT, p))

missing = []
for cid, files in CLUSTERS.items():
    lines = [f"# Phase 3b RE-ROUTE cluster: {cid}", "",
             "These gaps were correctly skipped by earlier waves because the gap data "
             "mislinked them. Each is re-homed to its correct article below. Some target "
             "files were already edited in an earlier wave — read current state first and "
             "add ONLY the new gap's content.", "",
             "Follow the shared agent instructions (3 quality gates, [pm-input] deferral, "
             "no TODO markers, imperative Title Case, English-only, no Next Steps/Related links).",
             "", "---", ""]
    for home, pm, entries in files:
        if not exists(home):
            missing.append((cid, home))
        lines += [f"## `{home}`", f"**Marker PM for this file:** {pm}", ""]
        for rank, note in entries:
            g = gaps[rank]
            lines += [f"### Gap rank {rank} ({g['priority']}, score {g['score']}) — {g['topic']}",
                      f"- **Routing note:** {note}",
                      f"- **What's missing:** {g['gap_detail']}",
                      f"- **Original suggested location:** {g.get('suggested_location','')}", ""]
        lines += ["---", ""]
    open(os.path.join(OUT, f"{cid}.md"), "w").write("\n".join(lines))
    n = sum(len(e) for _, _, e in files)
    print(f"{cid:26} files={len(files)} gaps={n}")

if missing:
    print("\n!! MISSING target files (fix mapping):")
    for cid, h in missing: print(f"  {cid}: {h}")
else:
    print("\nAll re-route target files exist ✓")
