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

## Wave 3 — pending (9)
Phil-Fuchs__1, __3, __4; Dan-Brinton__2, __3; Ryan-Despain__2, __3; Chris-Wright__5, __6

## Wave 4 — pending (7)
Jordan-Jensen__2; Khushboo__1, __3; Ken-Boyer__2; Mamta-Bolaki__1; Beth-Saenz__1; no-PM-listed__1

## Notes
- After each wave: aggregate agent reports → RESTRUCTURE-MANIFEST.md (Phase 3b section),
  run `pad_md_tables.py` on any table-touched files, spot-check, then launch next wave.
- Commit per wave (main session only).
