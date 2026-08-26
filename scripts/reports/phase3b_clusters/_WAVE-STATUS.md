# Phase 3b general — Forum-Gap Update: Wave Status

Source of truth for the parallel-agent pass. 35 clusters, 4 waves. Each cluster = one
agent editing only the files in `scripts/reports/phase3b_clusters/<CID>.md`.
Shared rules: `scripts/reports/phase3b_clusters/_AGENT-INSTRUCTIONS.md`.
Deferred (portal-only / dead-target, 27 gaps): `_DEFERRED.md`.

## Wave 1 — COMPLETE (committed) — 9 clusters, 36 files, 53 [pm-input] markers

All verified: 0 stray TODO/FIXME, markers well-formed, JSX tags balanced, docs.json clean, no new files.
Skips (target mismatch, logged in manifest): rank 181, 231, 314. Gap-data mislinks: 181, 225, 231, 235, 314.
Clusters: Tasleema__1, Chris__1, Andrea__1, Phil__2, Dan__1, Ryan__1, Jordan__1, Ken__1, Khushboo__2.

## Wave 2 — COMPLETE (committed) — 10 clusters, 45 files, 45 [pm-input] markers
Tasleema__2/3/4/5, Chris__2/3/4, Andrea__2/3/4. Verified clean (docs.json, tags, markers).
Mislinks: 193→360042931954; 234-wb→360042932414; false-claim in 201 (per 000004968).

## Wave 3 — COMPLETE (committed) — 9 clusters, 27 files, 38 [pm-input] markers
Phil__1/3/4, Dan__2/3, Ryan__2/3, Chris__5/6. Chris__5 = 0 edits (all 4 gaps mislinked to Tables).
Verified clean. Re-route backlog captured in manifest (Phase 3b general section).

## Wave 5 (re-route cleanup) — pending
Real gaps skipped for target mismatch, now routed to correct KB homes. See manifest re-route backlog.

## Wave 4 — COMPLETE (committed) — 7 clusters, 9 files, 15 [pm-input] markers
Jordan__2, Khushboo__1/__3, Ken__2, Mamta__1, Beth__1, no-PM-listed__1. Verified clean.
ALL 35 ORIGINAL CLUSTERS DONE. Re-route candidates added: 179→360043438473, 121→000005143, 353→360042932994.

## Notes
- After each wave: aggregate agent reports → RESTRUCTURE-MANIFEST.md (Phase 3b section),
  run `pad_md_tables.py` on any table-touched files, spot-check, then launch next wave.
- Commit per wave (main session only).
