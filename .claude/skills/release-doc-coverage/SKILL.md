---
name: release-doc-coverage
description: Build or update the KB Documentation Coverage tracker CSV for a GA release. Uses Current-Release-Notes.mdx as the checklist of every feature in the release, then checks each feature for coverage from BOTH the GA branch (git diff main...HEAD over s/article/ + s/topic/) AND already-published content in the repo (pre-GA betas / small updates already on main), records where the coverage lives, and for features with no coverage researches the KB to recommend what's needed (net-new article, update to a specific existing article, or both). Assigns the owning PM from Article-PM-Ownership-Reference.mdx and writes releaseCoverage/<Month>-<Year>-Release-Doc-Coverage.csv. Always asks first whether to CREATE the tracker or UPDATE an existing one; UPDATE re-runs the same coverage pass and first verifies the GA date agrees across the release-notes title, the CSV filename, and the branch name. Use when the user asks to "build the doc coverage tracker", "update the coverage CSV", "check KB coverage for the release", "which release features are missing KB", or similar.
---

# Release Documentation Coverage Tracker

Every GA release branch (`release-ga/<month>-<day>-<year>`) is the single place that holds three things for that release: the new KB additions/updates, the Release Notes (`s/article/Current-Release-Notes.mdx`), and a **coverage tracker** that reconciles the two. The Release Notes are the authoritative checklist of everything shipping in the GA cycle; the coverage tracker answers, feature by feature, *"do we have a KB submission from the right PM for this, and if not, why not?"*

This skill produces (or refreshes) that tracker as a CSV in `releaseCoverage/`. It writes the **9-column schema** defined in Step 6 — match that column order and value vocabulary exactly.

## Why this exists

KB submissions publish on a staggered schedule and come from many PMs. Without a reconciliation artifact, features silently ship with no documentation. The tracker turns the Release Notes into a line-by-line checklist so the KB Administrator can see, at a glance, which features are covered, where that coverage lives, which are documented externally, which have nothing — and, for every gap, what the PM needs to submit.

**Coverage is not only "what landed on this branch."** Domo runs rolling betas and small updates every month, and their KB content is often written and merged to `main` (already published) *before* the feature is officially announced at its GA train date. That already-published content is real coverage. So this skill checks each feature against **two** sources:

1. **The GA branch** — articles added/modified on `release-ga/*` relative to `main` (these ship on the release date).
2. **The already-published repo** — articles already on `main` that genuinely document the feature (submitted in an earlier beta / small-update cycle).

And for any feature with **no** coverage from either source, it researches the existing KB to recommend the specific content the PM needs — a net-new article, an update to a named existing article, or both.

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

## Step 4 — Determine coverage: GA branch + pre-GA repo

Coverage comes from **two** sources. Check both for every feature.

### 4a. The GA branch delta

What this branch changed relative to `main`. Compute the net change set once:

```bash
git diff --name-status main...HEAD -- s/article/ s/topic/
```

`A` = added (new article), `M` = modified (update), `R` = rename. **Exclude** files that aren't feature KB submissions:

- `s/article/Current-Release-Notes.mdx` (the release notes themselves)
- archived release files like `s/article/<Month>-<Year>-Release.mdx` (created by the `product-release-notes` archive step)

An article in this `A`/`M`/`R` set is **GA branch** coverage — it ships on the release date.

### 4b. The already-published repo (pre-GA)

Because the branch is cut from `main`, **any article NOT in the 4a delta is identical to `main`** — i.e., already published (or publishing on the normal KB cadence), independent of this GA release. Rolling betas and small updates routinely land KB content here *before* the GA announcement, and that content is real coverage.

For each feature, find its article(s) and judge coverage:

- **Release-Notes inline links.** The RN body frequently links a feature to its article — `[…](/s/article/<slug>)` or `[…](https://www.domo.com/docs/s/article/<slug>#anchor)`. Grab the slug/ID (strip the `#anchor` and the `https://www.domo.com/docs` prefix).
- **Keyword search** when there's no RN link: `grep -rli "title:.*<kw>" s/article/ s/topic/`, `ls s/article/ | grep -iE "<kw>"`.
- **Then READ the candidate** — frontmatter and the relevant body section. This is the judgment that separates coverage from a gap:
  - The article **documents this specific capability** ⇒ **pre-GA (published) coverage** (if not in the 4a delta) or **GA branch** coverage (if it is).
  - The article only covers the **general product area** and doesn't describe this feature ⇒ **not coverage**. It's a gap, and that article becomes the likely *update target* in Step 4.5.
  - Never trust a bare keyword hit or a bare RN link — a link can point at a general area article that predates the feature.

### 4c. Fill the coverage columns

1. **KB Submission (`<branch>`)** — **Yes** iff the feature's covering article is in the branch's `A`/`M`/`R` set (a real submission landed on this branch and ships on the release date). Otherwise **No** — including features covered only by already-published (pre-GA) content, features documented externally, and gaps. Strictly "did this branch add/modify an article for this feature."

2. **Coverage Source** — where the documentation for this feature lives:
   - `GA branch` — covered by an article in the 4a delta.
   - `Pre-GA (published)` — covered by an already-published article (exists on `main`, not in the 4a delta) that genuinely documents the feature.
   - `GA branch + Pre-GA` — some covering content is on the branch and some is already published (e.g., a pre-GA article plus a new branch article for the same feature).
   - `External (developer.domo.com)` — the RN says the feature is documented in the developer docs.
   - `None` — no KB content documents the feature anywhere yet (a gap → Step 4.5).

3. **Submission Type** — describes the **coverage that exists** (from either source), using the "3 kinds" vocabulary:
   - `Net-new` — a net-new article is the feature's doc.
   - `Update` — an existing article was updated to cover the feature.
   - `Net-new + Update` — the feature is covered by both a net-new article and an update to a pre-existing one.
   - `External` — Coverage Source is External.
   - `None` — no coverage exists (a gap; the recommendation goes in **KB Content Needed**, Step 4.5).

4. **Article Filepath** — the covering `s/article/…` path(s), semicolon-separated for multiple. Empty only when Coverage Source is `None` or `External` (a `None` gap fills this in Step 4.5 with the update target, if any).

## Step 4.5 — Recommend KB content for gaps

For every row where **Coverage Source = `None`**, research the KB and record **KB Content Needed** — the concrete content the PM must submit. For every row that already has coverage (any source other than `None`), **KB Content Needed = `N/A`** (nothing needed).

Determine the recommendation by researching what already exists (this is where the Explore-agent fan-out runs on a full regeneration):

- `Update to <article>` — a pre-existing article should absorb this feature (it owns the area but doesn't yet describe the capability). Name the target article in **Article Filepath** and in the value, e.g. `Update to s/article/000005216.mdx`.
- `Net-new` — no suitable existing article exists; a brand-new article is needed. Leave Article Filepath empty (optionally suggest a title in Notes).
- `Net-new + Update` — the feature needs a new article **and** a touch-up to a related existing one (e.g., a link or a cross-reference). Name the update target in Article Filepath.
- `None` — genuinely no KB needed (typically **Resolved Issues** / bug fixes). Note the reason (`Bug fix; no KB needed`).

Base every recommendation on reading candidate articles, not a keyword guess. If research can't establish the right target, say so in Notes (`update target needs PM confirmation`) rather than inventing a path.

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
- **Gap rows** — the PM is whoever owns the recommended update-target article (Step 4.5) or, for a net-new recommendation, whoever owns the feature's product area.

## Step 6 — Notes and CSV output

**Notes** is a short human explanation of the row's status. Typical phrasings:

- a one-line description of what the coverage covers (`Beta badge removed -> GA`, `Webhook configuration section added to Activity Log article`, `New article for Documents tiles`)
- for pre-GA coverage: `Documented pre-GA in <X> article (already published)`
- for gaps: `Net-new <feature> article needed`, `Add <capability> section to existing <X> article`, `update target needs PM confirmation`
- `Bug fix; no KB needed`
- `PM inferred (<area>)` / `; confirm` / `PM needs confirmation (...)`

**Columns**, in this exact order (header row verbatim, with the live branch name in the KB Submission header):

```
Section,Feature,KB Submission (<branch>),Coverage Source,Submission Type,KB Content Needed,Article Filepath,PM,Notes
```

Value vocabulary (from Steps 4–4.5):
- **Coverage Source**: `GA branch` / `Pre-GA (published)` / `GA branch + Pre-GA` / `External (developer.domo.com)` / `None`
- **Submission Type** (coverage that exists): `Net-new` / `Update` / `Net-new + Update` / `External` / `None`
- **KB Content Needed** (gaps only, else `N/A`): `Net-new` / `Update to <article>` / `Net-new + Update` / `None`

**Write** to `releaseCoverage/<Month>-<Year>-Release-Doc-Coverage.csv`. Quote any field containing a comma or semicolon per normal CSV rules. Keep rows in release-notes order.

### CREATE
Write the new CSV to the path above. If a file already exists at that path, you're likely in the wrong mode — confirm with the user before overwriting.

### UPDATE
Read the existing CSV first. Re-run Steps 3–4.5 against the current branch, the already-published repo, and the Release Notes, then reconcile **in place** (same filename), preserving human edits that automation can't re-derive:

- **Recompute** the automation-owned columns — `KB Submission`, `Coverage Source`, `Submission Type`, `KB Content Needed`, `Article Filepath` — from the current branch + repo state. Update the KB-Submission-column header if the branch name changed.
- **Preserve** human-confirmed **PM** values and any hand-written **Notes**; only change a PM/Note when the automated evidence now contradicts it (say so in the change preview).
- **Add** rows for features that appear in the Release Notes now but aren't in the CSV.
- **Flag** rows in the CSV whose feature is no longer in the Release Notes (a feature was pulled or renamed) — don't silently delete; surface them to the user.

Before writing, show the user a concise diff-style preview: features newly covered (and from which source), features whose coverage-source/type/filepath/needed changed, new rows, and dropped/renamed features. Write only after confirmation.

## Step 7 — Summary

After writing, give a one-paragraph summary: release identified, total features, count shipping on the branch (KB Submission = Yes), count covered pre-GA (already published), count external, count gaps — split into gaps needing net-new vs. gaps needing an update to an existing article — and the CSV path. For UPDATE, lead with the alignment result and the count of rows that changed since last run.

## Important reminders

- **Ask create vs. update first — every invocation.**
- **Alignment is non-negotiable on UPDATE.** RN title, branch name, and CSV filename must resolve to the same month/year, or stop and report.
- **Coverage has two sources — check both.** The GA branch delta (ships on the release date) **and** already-published content on `main` (pre-GA betas / small updates). Pre-GA published content that genuinely documents a feature counts as coverage.
- **KB Submission = Yes means *this branch* added/modified the article** — it stays `No` for a feature covered only by pre-GA published content (that's what Coverage Source records). Don't conflate the two columns.
- **Coverage vs. gap is a read, not a keyword hit.** An article counts as coverage only if it documents *this specific capability*; a general-area article that doesn't is a gap whose update-target it becomes.
- **Every gap gets a research-backed recommendation.** `KB Content Needed` names net-new, update-to-a-specific-article, or both — never guessed. Covered rows are `N/A`.
- **The Release Notes are the checklist.** Every `##`/`###`/`####` heading (except Support/boilerplate) becomes exactly one row.
- **PMs come from `Article-PM-Ownership-Reference.mdx`** (the CODEOWNERS/squad source). Infer only when necessary and mark inferences in Notes.
- **Don't invent article paths.** If no coverage and no credible update-target exist, leave Filepath empty, Coverage Source `None`, Submission Type `None`, and put the recommendation in KB Content Needed.
- **The CSV always lives in `releaseCoverage/`.** Never write it to the repo root.
