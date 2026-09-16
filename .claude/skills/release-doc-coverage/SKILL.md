---
name: release-doc-coverage
description: Build or update the KB Documentation Coverage tracker CSV for a GA release. Uses Current-Release-Notes.mdx as the checklist of every feature in the release, checks each feature against what the GA branch actually submitted for KB (git diff main...HEAD over s/article/ + s/topic/), assigns the owning PM from Article-PM-Ownership-Reference.mdx, and writes releaseCoverage/<Month>-<Year>-Release-Doc-Coverage.csv. Always asks first whether to CREATE the tracker or UPDATE an existing one; UPDATE re-runs the same coverage pass and first verifies the GA date agrees across the release-notes title, the CSV filename, and the branch name. Use when the user asks to "build the doc coverage tracker", "update the coverage CSV", "check KB coverage for the release", "which release features are missing KB", or similar.
---

# Release Documentation Coverage Tracker

Every GA release branch (`release-ga/<month>-<day>-<year>`) is the single place that holds three things for that release: the new KB additions/updates, the Release Notes (`s/article/Current-Release-Notes.mdx`), and a **coverage tracker** that reconciles the two. The Release Notes are the authoritative checklist of everything shipping in the GA cycle; the coverage tracker answers, feature by feature, *"do we have a KB submission from the right PM for this, and if not, why not?"*

This skill produces (or refreshes) that tracker as a CSV in `releaseCoverage/`. The canonical example is `releaseCoverage/September-2026-Release-Doc-Coverage.csv` — match its columns and value vocabulary exactly.

## Why this exists

KB submissions publish on a staggered schedule and come from many PMs. Without a reconciliation artifact, features silently ship with no documentation. The tracker turns the Release Notes into a line-by-line checklist so the KB Administrator can see, at a glance, which features are covered, which link to existing articles, which are documented externally, and which have nothing — and who to chase for each gap.

## Step 1 — Ask: create or update?

Always start here. Use **AskUserQuestion** with one question:

> Are we **creating** the coverage tracker for this release, or **updating** an existing one?

- **Create** — no tracker exists yet for this release (or the user wants to regenerate from scratch). Runs the full pass and writes a new CSV.
- **Update** — a tracker already exists in `releaseCoverage/`. Re-runs the same coverage pass, first verifying GA-date alignment, then reconciles the existing CSV in place.

Do not guess from whether a file exists — ask. (A file can exist and still need a from-scratch rebuild.) Once answered, both paths share Steps 3–6; Step 2 differs only by the alignment gate.

## Step 2 — Resolve the release identity (and, for UPDATE, verify alignment)

Three things must name the **same GA release**:

1. **Release Notes title** — the `title:` frontmatter of `s/article/Current-Release-Notes.mdx`, e.g. `"September 2026 Release Notes"` → month/year = **September 2026**.
2. **Branch name** — the current branch, e.g. `release-ga/sept-23-2026` → month/year = **September 2026** (the day is the feature-switch date, not part of the tracker identity).
3. **CSV filename** — `releaseCoverage/<Month>-<Year>-Release-Doc-Coverage.csv`, e.g. `September-2026-Release-Doc-Coverage.csv`.

Gather them:

```bash
git branch --show-current
grep -m1 '^title:' s/article/Current-Release-Notes.mdx
ls releaseCoverage/ 2>/dev/null
```

The branch abbreviates the month (`sept`, `oct`); the title and filename spell it out (`September`, `October`). Normalize before comparing — `sept` ↔ `September`, and the years must be identical.

- **CREATE**: derive the CSV filename from the Release-Notes month/year. If the current branch isn't a `release-ga/*` branch, or its month/year doesn't match the Release-Notes title, **stop and tell the user** — a coverage tracker built off a mismatched branch would record the wrong "KB Submission" column. Don't proceed on a guess.
- **UPDATE**: this alignment check is the whole point of the mode. If the Release-Notes title, the branch name, and the existing CSV filename don't all resolve to the same month/year, **stop and report the mismatch** (state all three values). Only continue once they agree. This catches the common error of updating last month's tracker on this month's branch, or editing a tracker after the release notes were rolled to the next cycle.

The **branch name is embedded in the CSV's coverage column header** — `KB Submission (release-ga/sept-23-2026)` — so the CSV itself records which branch state it reflects. On UPDATE, if the branch's full name changed (e.g. a new feature-switch date), update that header to the current branch.

## Step 3 — Extract the feature checklist from the Release Notes

Read `s/article/Current-Release-Notes.mdx`. Its heading hierarchy maps to the CSV:

- `##` headers → the **Section** column. In September these were `New Features and Enhancements`, `Fast Follows - October 1st`, `Beta Features`, `Resolved Issues`. The example CSV lightly compacts them (`New Features & Enhancements`, `Fast Follows - October 1`); either the exact heading or that compact form is fine — be consistent within the file.
- `###` headers → a **feature**, *unless* the section nests `####` children under it.
- `####` headers under a `###` parent → each child is its own feature row, named **`<parent> - <child>`**. Strip a trailing ` Enhancements` from the parent first:
  - `### App Components` → `#### KPI Templates` ⇒ **App Components - KPI Templates**
  - `### App Studio Enhancements` → `#### Move and Copy Cards` ⇒ **App Studio - Move and Copy Cards**
  - `### Magic ETL Enhancements` → `#### Classification Tile` ⇒ **Magic ETL - Classification Tile**
  - `### Workflows Enhancements` → `#### MCP Trigger` ⇒ **Workflows - MCP Trigger**
- A `###` with no `####` children is a flat feature row using the header text verbatim (e.g. `User Impersonation`, `Card Embed Enhancements`, `Workspaces as Nav`).

Include `Resolved Issues` as their own rows (they're part of the release checklist; their Submission Type is almost always `None` with a `Bug fix; …` note). Skip the `## Support` boilerplate section and the `import`/`<BetaNote />` lines.

Every `##`/`###`/`####` becomes exactly one row. Preserve release order.

## Step 4 — Determine coverage against the branch

"What's been submitted" = what this GA branch changed relative to `main`. Compute the net change set once:

```bash
git diff --name-status main...HEAD -- s/article/ s/topic/
```

`A` = added (new article), `M` = modified (update), `R` = rename. **Exclude** files that aren't feature KB submissions:

- `s/article/Current-Release-Notes.mdx` (the release notes themselves)
- archived release files like `s/article/<Month>-<Year>-Release.mdx` (created by the `product-release-notes` archive step)

For each feature, find its article(s) and fill three columns:

1. **Article Filepath** — the `s/article/…` path(s), semicolon-separated when a feature spans more than one. Two strong signals, used together:
   - **Release-Notes inline links.** The RN body frequently links a feature to its article — `[…](/s/article/<slug>)` or `[…](https://www.domo.com/docs/s/article/<slug>#anchor)`. That link is the feature's intended article. Grab the slug/ID (strip the `#anchor` and the `https://www.domo.com/docs` prefix).
   - **The branch diff.** Cross-check whether that article appears in the `A`/`M` set above.
   - For features with no RN link, search `s/article/` by title/slug keyword (`grep -rli "title:.*<kw>" s/article/`, `ls s/article/ | grep -iE "<kw>"`) and confirm by reading the frontmatter — don't trust a bare keyword hit.

2. **KB Submission (`<branch>`)** — **Yes** only if the feature's article is in the branch's `A`/`M` set (a real submission landed on this branch). Otherwise **No** — including features that merely *link to an existing, unchanged article* and features documented *externally*. This column is strictly "did this branch add/modify a KB article for this feature," not "does any article mention it."

3. **Submission Type** — the vocabulary from the example CSV:
   - `New` — a new article (`A`) is the feature's primary doc.
   - `Update` — an existing article was modified (`M`) for the feature.
   - `New + Update` / `Update + New` — the feature touches both a new and a modified article.
   - `None` — nothing on the branch and no article to link.
   - `None (links to existing article)` — the RN links to an existing article that was **not** changed on this branch (Filepath is still populated with that article; KB Submission = No).
   - `External (developer.domo.com)` — the RN says the feature is documented in the developer docs (KB Submission = No, Filepath empty).

## Step 5 — Assign the PM

PM ownership comes from `Article-PM-Ownership-Reference.mdx` (generated from the squad CSV / CODEOWNERS — the same source of truth used for review routing).

- **Matched article** — look up the PM by filename:
  ```bash
  grep "<matched-filename>.mdx" Article-PM-Ownership-Reference.mdx
  ```
- **No matched article** — look up by the closest Feature name to find who would own it:
  ```bash
  grep -i "^| *<Feature keyword>" Article-PM-Ownership-Reference.mdx | head
  ```
- **Inference** — when ownership isn't directly listed, infer from the product area and mark it in **Notes**, mirroring the example vocabulary: `PM inferred (Cloud Amplifier)`, `PM inferred (Charting); confirm`, `PM needs confirmation (...)`. When no PM can be identified at all, put `(no PM listed)` in the PM column and explain in Notes.

## Step 6 — Notes and CSV output

**Notes** is a short human explanation of the row's status. Reuse the example's phrasings:

- `No KB content on branch`
- `No KB content on branch (image only in release notes)` / `(release notes ship images inline only)`
- `Beta badge removed -> GA`
- `Links to existing <X> article; not updated on branch`
- `Target article NOT updated on branch for this toolkit`
- `PM inferred (<area>)` / `; confirm` / `PM needs confirmation (...)`
- a one-line description of what the update/new article covers

**Columns**, in this exact order (header row verbatim, with the live branch name in the coverage header):

```
Section,Feature,KB Submission (<branch>),Submission Type,Article Filepath,PM,Notes
```

**Write** to `releaseCoverage/<Month>-<Year>-Release-Doc-Coverage.csv`. Quote any field containing a comma or semicolon per normal CSV rules. Keep rows in release-notes order.

### CREATE
Write the new CSV to the path above. If a file already exists at that path, you're likely in the wrong mode — confirm with the user before overwriting.

### UPDATE
Read the existing CSV first. Re-run Steps 3–5 against the current branch and Release Notes, then reconcile **in place** (same filename), preserving human edits that automation can't re-derive:

- **Recompute** the automation-owned columns — `KB Submission`, `Submission Type`, `Article Filepath` — from the current branch state. Update the coverage-column header if the branch name changed.
- **Preserve** human-confirmed **PM** values and any hand-written **Notes**; only change a PM/Note when the automated evidence now contradicts it (say so in the change preview).
- **Add** rows for features that appear in the Release Notes now but aren't in the CSV.
- **Flag** rows in the CSV whose feature is no longer in the Release Notes (a feature was pulled or renamed) — don't silently delete; surface them to the user.

Before writing, show the user a concise diff-style preview: features newly covered, features whose type/filepath changed, new rows, and dropped/renamed features. Write only after confirmation.

## Step 7 — Summary

After writing, give a one-paragraph summary: release identified, total features, count covered (Yes), count linking to existing articles, count external, count with nothing, and the CSV path. For UPDATE, lead with the alignment result and the count of rows that changed since last run.

## Important reminders

- **Ask create vs. update first — every invocation.**
- **Alignment is non-negotiable on UPDATE.** RN title, branch name, and CSV filename must resolve to the same month/year, or stop and report.
- **KB Submission = Yes means the branch actually added/modified the article** — not that some article mentions the feature. A feature can have a populated Filepath and still be `No` (links to an existing, unchanged article).
- **The Release Notes are the checklist.** Every `##`/`###`/`####` heading (except Support/boilerplate) becomes exactly one row.
- **PMs come from `Article-PM-Ownership-Reference.mdx`** (the CODEOWNERS/squad source). Infer only when necessary and mark inferences in Notes.
- **Don't invent article paths.** If no submission and no linkable article exist, leave Filepath empty and set Type to `None`.
- **The CSV always lives in `releaseCoverage/`.** Never write it to the repo root.
