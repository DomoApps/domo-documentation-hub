# Phase 3b cluster: Beth-Saenz__1

**Owning PM:** Beth Saenz
**Files in this cluster:** 1  |  **Gaps:** 2

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360042934394.mdx`
*Time Zone Formatting* — area: Cloud Integrations / Snowflake / Data ingestion

### Gap rank 215 (Medium, score 50.8) — Snowflake/Cloud Amplifier timezone handling of timestamps
- **What's missing:** Need documentation on how Domo converts datetime fields on ingestion (uses Company Settings timezone, defaults to UTC), how it handles Snowflake TIMESTAMP_NTZ vs TIMESTAMP_TZ differently, why behavior differs by source, and how to control/override the conversion. TIMESTAMP_TZ support and a CA timezone-shift option are feature requests.
- **Suggested location:** Update s/article/360042934394.mdx (Time Zone Formatting) with a connector/Cloud Amplifier note: how Snowflake TIMESTAMP_NTZ vs TIMESTAMP_TZ are interpreted on ingestion and that there is currently no per-connection timezone shift for Cloud Amplifier (feature request).

### Gap rank 274 (Medium, score 47.0) — CURRENT_DATE()/NOW() return UTC, not Company Time Zone
- **What's missing:** Explicitly document that CURRENT_DATE()/NOW()/CURDATE() are UTC-based and ignore Company Time Zone, the evening date-rollover impact, and a robust workaround that survives DST (the static DATE_ADD(... INTERVAL -5 HOUR) workaround breaks across daylight saving).
- **Suggested location:** Add an explicit note to the date/time function definitions in the Functions Reference (s/article/360043429933.mdx) and a FAQ entry in s/article/360043430053.mdx that CURRENT_DATE()/NOW() return UTC and ignore the company time zone, with the evening-rollover impact and a DST-aware workaround. Cross-link from Setting Your Company Time Zone.

- **Other referenced articles:** s/article/360043430053.mdx, s/article/360043429933.mdx

---
