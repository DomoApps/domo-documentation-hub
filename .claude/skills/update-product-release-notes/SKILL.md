---
name: update-product-release-notes
user-invocable: true
description: "Reconcile an EXISTING s/article/Current-Release-Notes.mdx against a newly supplied context source (an internal-notes .docx, a PMM copy doc, an epics/beta CSV, or a Jira/PRD pull) and apply an in-place UPDATE. Never archives, never creates the file, never opens a PR, never localizes. Use when the release notes already exist and the user wants them checked and corrected against a new/updated source — e.g. 'update the release notes from this docx', 'reconcile the September notes against the 8-4 branch email', 'the internal notes changed, sync the release notes'. For a first-time draft (archive + build from scratch), use product-release-notes instead."
argument-hint: "the context file/folder to reconcile against (e.g. a .docx name)"
---

# Update Product Release Notes (reconcile-in-place)

Update an **already-existing** `s/article/Current-Release-Notes.mdx` against a **newly supplied context source**. This is the surgical sibling of the `product-release-notes` skill: that skill builds the file from scratch (archive → ingest → draft → commit); **this** skill assumes the file already exists and a fresh or corrected source has arrived, and reconciles the two.

The user provided: **$ARGUMENTS**

## Hard boundaries (what this skill must NOT do)

- **Do NOT archive.** Never run `scripts/archive-current-release-notes.py`. The outgoing file is not being rotated — it's being edited.
- **Do NOT create new files.** The only file you write is the existing `s/article/Current-Release-Notes.mdx` (plus any genuinely new feature screenshot into `images/kb/`, and only if the source supplies a usable one).
- **Do NOT open a PR and do NOT localize.** Same out-of-scope rule as `product-release-notes`. Localization runs later via the `localize` skill after the English update is approved.
- **Do NOT touch features the source doesn't mention.** A context source is often a *subset* of the release (e.g. one branch's preview email). Leave every unmentioned feature exactly as it is. Reconcile only the overlap, plus true additions.

Read `.claude/skills/product-release-notes/release-notes-style.md` in full before editing — the house voice, file skeleton, alphabetization, and §10 checklist all still govern the result.

---

## The four reconciliation lenses

The whole job is a diff between the **source of truth** (the newly supplied context) and the **current article**. Every change you make falls into one of four buckets. Ask the user up front which lens(es) matter most if they haven't said; by default check all four, and treat the **supplied context as the source of truth** for the first two.

1. **Factual discrepancies** — any claim, count, list, capability, model name, or date in the article that the source contradicts. Correct the article to match the source. Examples: an aggregation list, the set of supported engines, a number of chart types, a deprecation date. These are non-negotiable corrections.

2. **Nomenclature changes** — feature names, headings, capitalization, and product-term casing where the source and the article disagree. Align the article to the source's naming. Watch for *internal inconsistency in the source itself* (a summary bullet naming a feature one way and its detail header another) — when the source disagrees with itself, don't silently pick one; flag it and prefer the customer-facing name the source uses in its quick-list, since that's what the article's audience will see. Note that a source's internal/detail heading is often more descriptive than a real product name; use judgment, and surface the call rather than burying it.

3. **Phrasing changed for effect** — spots where the article's wording was tuned for a different emotional register or a different shade of understanding than the source (e.g. plain "easier to follow" → evocative "read as movement", or a neutral term swapped for a punchier one). These are usually **report, don't auto-revert**: they're style, not fact. Surface each with a before/after so the user decides. Only revert to the source's phrasing when the user has said the source governs tone too, or when the article's version drifts into marketing superlatives the house style forbids.

4. **Straight-up additions** — features present in the source but **absent** from the article. These are the highest-value finds. Draft each new feature as a full entry in house voice (§4 of the style guide: benefit-first lead, optional bullets, `<Frame>` if a real screenshot exists, `Learn more` only if a real published KB article exists), then insert it in the correct **alphabetized** position and under the correct section (New Features vs Beta — see the placement note below).

---

## Workflow

### Step 1 — Branch preflight

```bash
git branch --show-current
```

Stay on the current non-`main` release branch (e.g. `release-notes/september2026`). If on `main`, stop and ask — an update should already have a branch. Never edit on `main`.

### Step 2 — Locate and fully ingest the context source

Find the file(s) the user named:

```bash
ls -la          # or: find . -iname "*<name>*"
```

**`.docx` / `.doc`** — convert with pandoc and extract embedded media (same as `product-release-notes` Step 4):

```bash
mkdir -p scripts/reports/release-context/docx
pandoc "<file>.docx" -o scripts/reports/release-context/docx/<file>.md \
  --extract-media=scripts/reports/release-context/docx/<file>-media
```

Then **Read the whole `.md`, top to bottom.** Do not skim. Internal notes usually have two layers: a short **summary/quick-list** at the top (the customer-facing feature names) and **detailed sections** lower down (fuller blurbs, sometimes with different internal headings). You need both — the quick-list gives you the naming and the full feature inventory; the detail gives you the facts to reconcile.

**CSV of epics/betas** — note which items are flagged Beta vs GA (drives section placement). **Jira keys / PRD needs** — if the source is thin and you need epic descriptions or PRDs, run `scripts/fetch-jira-context.py --csv <csv> --out scripts/reports/release-context --download-images` and prefer the PRD text over the epic description, exactly as in `product-release-notes` Step 5. For a plain docx/email, this is usually unnecessary.

`scripts/reports/release-context/` is gitignored scratch — never commit it.

### Step 3 — Inventory the source and map it onto the article

Build an explicit feature list from the source (use its quick-list). For **each** source feature, find the matching `###`/`####` entry in `Current-Release-Notes.mdx` (`grep -n` by feature name/keyword). Produce a small mapping table: *source feature → article heading (or "MISSING")*. This table is what makes the reconciliation auditable and is the backbone of your handoff summary.

The mapping immediately reveals:
- **MISSING rows → lens 4 additions.**
- **Present rows → candidates for lenses 1–3**, checked entry by entry.
- Whether the source is a **subset** (common) or introduces net-new scope. If it's a pure subset with no conflicts, that itself is the finding — say so plainly rather than inventing changes.

### Step 4 — Reconcile entry by entry (the four lenses)

Walk every mapped pair. For present features, compare the source blurb to the article body and classify each delta into lens 1/2/3. For missing features, draft a new entry (lens 4). Keep a running list of every change and every observation, tagged by lens, for the handoff.

Guidance that recurs:
- **Screenshots:** only add one if the source supplies a genuine feature screenshot. Ignore decorative email banners/headers (check dimensions — a wide, short image like ~936×356 is almost always a banner). Real feature shots get copied into `images/kb/` with a snake_case name and embedded as `<Frame>![](/images/kb/<name>.png)</Frame>`. Never leave a placeholder/TODO.
- **Placement (New vs Beta):** if the source doesn't clearly flag GA vs Beta, **do not move an existing entry between sections** — preserve the placement the prior draft chose. Only use an explicit Beta/GA signal from the source (usually the CSV) to place a *new* addition.
- **Detail already in the article that the source doesn't mention** is NOT a discrepancy — the original draft may have sourced it from a Jira epic/PRD. Leave it unless the source actually contradicts it; note in the summary that it's beyond the current source and thus unverifiable from this source alone.

### Step 5 — Apply the edits

Use `Edit` for targeted in-place changes (nomenclature, factual fixes, any user-approved phrasing reverts) and to insert new feature entries at the correct alphabetized position. Re-verify alphabetization after any heading rename or insertion (§3 of the style guide). Preserve the file skeleton exactly: frontmatter, `import { BetaNote }` + `---`, the three `##` sections, `<BetaNote generic />` atop Beta, and the verbatim Support block.

If you changed a heading, confirm it doesn't disturb sort order (e.g. "New Chart **Improvements**" vs "New Chart **Types**" both sort under "New Chart", so position is unchanged). If any Markdown tables were touched, run `python3 scripts/pad_md_tables.py s/article/Current-Release-Notes.mdx`.

### Step 6 — Verify

- Re-read the edited region(s) top to bottom for house-voice consistency and §10 checklist adherence.
- Every `<Frame>` path exists: `ls images/kb/<name>.png`.
- Every `Learn more` link points at a real published article: `grep -rl "title:.*<keyword>" s/article/`.
- Every applied factual/nomenclature change traces to the source.

### Step 7 — Hand off (do NOT commit unless asked)

Give the user a tight, lens-organized summary:
- **Additions** applied (or "none — source is a subset already fully covered").
- **Factual corrections** applied, each as source → old → new.
- **Nomenclature changes** applied, each as before → after, and flag any where the source was internally inconsistent or where the source's term is arguably weaker than the article's (offer a one-line revert).
- **Phrasing-for-effect observations** — before/after, marked as reported-not-changed unless the user directed otherwise.
- Any screenshots added; any source features that lacked a usable screenshot or a KB link.

Show the diff. Commit only if the user asks; if they do, use a present-tense message describing the reconciliation (e.g. `Reconcile September release notes against 8-4 branch internal notes`) and end with the repo's required co-author trailer. Remind them merged ≠ published (KB publishing cadence) and that `localize` runs separately when the English update is final.

---

## Notes

- This skill deliberately reuses `product-release-notes`' ingest mechanics (pandoc for docx, `fetch-jira-context.py` for Jira/PRD) and its `release-notes-style.md` house style. The difference is intent: **reconcile-in-place, not archive-and-rebuild.**
- When the source and the article already agree, resist inventing edits. A clean "no discrepancies; source is a subset" is a valid and valuable outcome.
- The `scripts/reports/release-context/` scratch dir is gitignored working output — leave it, don't commit it.
