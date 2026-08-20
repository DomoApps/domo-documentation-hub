---
name: product-release-notes
user-invocable: true
description: "Draft the public-facing product feature-release Release Notes into s/article/Current-Release-Notes.mdx. Archives the outgoing Current Release Notes to a numbered file and nav, ingests a context folder (internal-notes Word docs + a master-epics/beta CSV), pulls each epic's Jira description and Confluence PRD, drafts in Domo house style, fact-checks against the sources, and commits on approval. Use when the user asks to write/draft the monthly (feature-release) release notes, e.g. 'draft the September release notes', 'write the product release notes'."
argument-hint: "(optional) the release month + context folder name"
---

# Product Feature-Release Release Notes

Draft Domo's public-facing **feature-release** Release Notes into `s/article/Current-Release-Notes.mdx`, following the house style in **`release-notes-style.md`** (read it in full before drafting). This skill is for the customer-facing monthly feature release notes only — not the git-tag `release-notes` skill (`releaseNotes/`) and not the PMM link-wiring `release-feature-links` skill.

**Out of scope (do not do these):** opening a PR, localizing. Localization is run separately by the user with the `localize` skill after the English draft is approved.

The user provided: **$ARGUMENTS**

---

## Inputs the user supplies

- A **context folder** committed to the repo (e.g. `Sept-Prod-Release-Notes-Context/`) containing:
  - **Word docs** of the previous **internal** release notes + their embedded screenshots (the short blurb + images per feature).
  - A **CSV** listing the master **epics** for each GA feature **and** the **Beta programs** shipping this release, with a column holding a Jira key (e.g. `DOMO-######`).
- Jira/Confluence auth is already in `.env` (`JIRA_EMAIL`, `JIRA_API_TOKEN`) — same creds work for both, base `https://domoinc.atlassian.net`.

---

## Workflow

### Step 1 — Branch preflight (before any change)

Check the current branch:

```bash
git branch --show-current
```

- If it is already a non-`main` branch (e.g. `release-notes/september2026`), stay on it. If the branch name encodes a month/year, note it as the target release.
- **Only if on `main`**, create a release-notes branch and switch to it. Ask the user for the target release month + year if not already known, then:

  ```bash
  git checkout -b release-notes/<month><year>   # e.g. release-notes/september2026 (lowercase month, 4-digit year, no separator)
  ```

Never make any file change on `main`.

### Step 2 — Archive the outgoing Current Release Notes

Do this **before** asking where the context is, so the file is clear and ready to draft. The outgoing notes are archived under their **own** month (independent of the new release).

1. Preview:
   ```bash
   python3 scripts/archive-current-release-notes.py --dry-run
   ```
   Confirm the derived month/year, archived filename (`s/article/{Month}-{Year}-Release.mdx`), new title (`"{Year} Release {N} | {Month}"`), and the nav insertion point look right.
2. Apply:
   ```bash
   python3 scripts/archive-current-release-notes.py
   ```
   This creates the archived `.mdx` (content copied verbatim, only the `title:` changed) and inserts its path at the end of the **English** "2025-2026" subgroup under "Archived Feature Release Notes" in `docs.json`. It does **not** touch `Current-Release-Notes.mdx` — you overwrite that in Step 6.

   > The script edits only the English nav. Localized nav entries for the archived file are created later by the `localize` flow — do not add them here.
   > If a new calendar year needs a new nav subgroup (e.g. a "2027" group), the script appends to "2025-2026"; flag this to the user so they can decide whether to rename/split the group via the `add-to-nav` skill.

### Step 3 — Ask where the context is

Ask the user for the **name of the context folder** they committed (e.g. `Sept-Prod-Release-Notes-Context`). If `$ARGUMENTS` already names it, confirm rather than re-ask. Then locate its contents:

```bash
ls -R "<folder>"
```

Identify the CSV (epics + betas) and the Word docs (`.docx`).

### Step 4 — Ingest the Word docs (internal notes + screenshots)

For each `.docx`, convert to Markdown and extract embedded images with pandoc (available in this repo's environment):

```bash
mkdir -p scripts/reports/release-context/docx
pandoc "<folder>/<file>.docx" -o scripts/reports/release-context/docx/<file>.md \
  --extract-media=scripts/reports/release-context/docx/<file>-media
```

Read the resulting `.md` for each feature's short internal blurb, and note the extracted media images (in the `-media/media/` subfolder) — these are the primary screenshots for the article.

### Step 5 — Pull Jira epics + Confluence PRDs

Run the fetch script against the CSV (it auto-detects the Jira-key column and pulls each epic's description + any linked Confluence PRD, and downloads image attachments):

```bash
python3 scripts/fetch-jira-context.py --csv "<folder>/<epics>.csv" \
  --out scripts/reports/release-context --download-images
```

Read `scripts/reports/release-context/_manifest.md`, then each `DOMO-*.md`. Each file has the epic summary, description, linked Confluence links, and the PRD body text. Note which items the CSV flags as **Beta programs** vs GA features (that determines section placement). If the CSV's GA-vs-beta column is ambiguous, ask the user.

If a key fails (HTTP 4xx) or a PRD isn't found, note it and rely on the internal-notes blurb + epic description; don't invent detail.

### Step 6 — Draft into Current-Release-Notes.mdx

Read `release-notes-style.md` in full, then overwrite `s/article/Current-Release-Notes.mdx` with the new draft:

- **Title** `"{Month} {Year} Release Notes"` for the **new** release; keep the filename `Current-Release-Notes.mdx`.
- Build the feature list from the CSV; write each as a `### ` entry (sub-features `#### ` under parents like *Magic ETL Enhancements* / *Workflows Updates*). Alphabetize by heading.
- For each feature, synthesize the internal blurb + epic description + PRD into 1–3 benefit-first paragraphs (+ optional bullet list), in Domo house voice. **Never** expose Jira keys, PRD jargon, codenames, squad/PM names, or internal dates.
- **Screenshots:** choose the best image per feature (from the Word-doc media, or a Jira/Confluence image in `scripts/reports/release-context/media/`). Copy it into `images/kb/` with a descriptive **snake_case** name, then embed on its own line as `<Frame>![](/images/kb/<name>.png)</Frame>`. Every referenced image must exist in `images/kb/` on this branch. Never leave a placeholder or TODO.
- **"Learn more" links:** add `Learn more about [text](https://www.domo.com/docs/s/article/<slug-or-id>).` **only** when a real published KB article exists — verify with `grep -rl "title:.*<keyword>" s/article/`. Omit if none.
- **Beta Features** section opens with `<BetaNote generic />`. Include standard non-feature sections (Model Deprecation Notice, Domo AI Models Updates) when present in the internal notes. End with the verbatim **Support** block.

### Step 7 — Fact-check pass (no hallucination)

Go feature by feature and verify **every** claim, model name, capability, bullet, and date traces to the internal-notes blurb, the epic description, or the PRD in `scripts/reports/release-context/`. Cut or correct anything unsupported. Confirm each `<Frame>` path exists (`ls images/kb/<name>.png`) and each "Learn more" link resolves to a real article.

### Step 8 — Edit pass

Read the whole draft top to bottom for clarity, house-style adherence (`release-notes-style.md` §10 checklist), grammar, and consistent product naming. If any Markdown tables were added, run `python3 scripts/pad_md_tables.py s/article/Current-Release-Notes.mdx`. Re-confirm structure: title/excerpt, `import { BetaNote }` + `---`, alphabetized sections, Beta section, Support block.

### Step 9 — Hand off for approval

Show the user a concise summary (features covered, betas, images added, any epics/PRDs that failed to fetch, any features lacking a screenshot or KB link) and the diff. **Do not commit yet.** Wait for explicit approval.

### Step 10 — Commit (only after approval)

Stage the draft, the archived file, the `docs.json` nav change, and the new images, then commit to the branch with a present-tense message:

```bash
git add s/article/Current-Release-Notes.mdx s/article/<Month>-<Year>-Release.mdx docs.json images/kb/
git commit -m "Add <Month> <Year> release notes and archive <prev month> notes"
```

End with the co-author trailer required by repo convention. Do **not** open a PR and do **not** localize — both are out of scope. Remind the user that merged is not published (KB publishing cadence) and that they can run `localize` when ready.

---

## Notes

- The `scripts/reports/release-context/` scratch dir is working output, not repo content — don't commit it. (Add to `.gitignore` if it isn't already ignored.)
- The two helper scripts:
  - `scripts/archive-current-release-notes.py` — archives the outgoing Current notes (file + title + English nav). `--dry-run` to preview.
  - `scripts/fetch-jira-context.py` — pulls epic descriptions + Confluence PRDs from a CSV of keys. `--test` verifies credentials; `--download-images` saves Jira/Confluence images.
- Screenshots from the Word docs are the primary source; Jira/Confluence images are the fallback. Either way, every screenshot that belongs in the article must be copied into `images/kb/` and embedded in a `<Frame>`.
