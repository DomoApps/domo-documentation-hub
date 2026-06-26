---
name: revise-submission
user-invocable: true
description: "Revise the MDX content in the current branch's PR for Domo style guide compliance and MDX code conventions — then preview the diff before committing and pushing."
argument-hint: "optional: a specific file or concern to focus on; otherwise all changed MDX files are revised"
---

Revise the MDX content committed on the current branch for style and convention compliance, then let the user preview the diff before committing the changes and pushing them to the branch.

The user has provided: $ARGUMENTS

---

## Step 1: Identify the PR and changed MDX files

Find the open PR for the current branch and list its changed files:

```bash
gh pr view --json number,title,headRefName,baseRefName
```

Then get the list of files changed in the PR:

```bash
gh pr diff --name-only
```

Filter to MDX content files only. Include files under these paths:
- `s/article/`
- `s/topic/`
- `portal/`

Exclude everything in the localized roots (`de/`, `es/`, `fr/`, `ja/`) — those are never touched by this skill. Also exclude `docs.json`, `images/`, `openapi/`, `.csv`, and any non-`.mdx` file.

If `$ARGUMENTS` names a specific file, revise only that file (confirm it exists in the PR diff first). Otherwise, revise every qualifying file found above.

If there are no qualifying MDX files in the PR, tell the user and stop.

---

## Step 2: Get the added/changed text for each file

For each qualifying file, identify which content is new or changed in this PR so the revision pass is scoped correctly:

```bash
git diff $(git merge-base HEAD origin/main) -- <file>
```

If the file is net-new (Added status in the PR), the entire file is in scope. If the file is Modified, only the added/changed lines are in scope — but read the whole file so you understand context and don't introduce inconsistencies.

Read the full current content of each qualifying file with the Read tool.

---

## Step 3: Read the style guide and article template

Before revising anything, read both reference files in full:

1. **`Domo-KB-Style-Guide.mdx`** — authoritative style rules: voice, terminology, callout syntax, heading conventions, image conventions, beta treatment, Domo-specific terms, and more.
2. **`New-Article-Template.mdx`** — canonical MDX structure and encoding conventions: frontmatter fields, section order, component syntax, table format, etc.

Read them now, not from memory. Apply every rule in these files to the revision pass.

---

## Step 4: Revise each file

For each qualifying file, apply a full style-guide and MDX-convention pass against the content that is new or changed in this PR. Fix every violation. Use the Edit tool to revise in place.

**Scope:** Fix style and convention errors in the new/changed content and any clearly broken style directly adjacent to those changes. Do not silently rewrite untouched sections that were already in the repo before this PR.

Work through this checklist for every file:

### Frontmatter
- `title` field is present.
- Use `excerpt` (single sentence), not `description`. Remove `description` if present and replace with `excerpt`.
- If the article is beta: `tag: "Beta"` present in frontmatter and the standard beta Note appears immediately after the frontmatter, above the Intro.

### Intro
- Opens with "This article explains…" or "This article covers…" — states only what the article covers.
- Immediately followed by a `---` horizontal rule.

### Headings
- Imperative mood at every level (H2–H4). Structural labels — Intro, Required Grants, Prerequisites, FAQ, Troubleshoot, Related Articles — are exempt.
- Top-level sections use H2 (`##`), subsections H3+ (`###`, `####`).

### Required Grants
- Exact format: **Grant —** description (em-dash inside the bold, a space on each side).
- Use canonical grant wording — search other articles for existing wording before writing new descriptions:
  ```bash
  grep -rn "Grant Name —" s/article/
  ```

### Callouts
- Use `<Note>`, `<Warning>`, or `<Tip>` — not blockquotes or bold-only text.
- Label and colon are bolded: `**Note:**`, `**Warning:**`, `**Tip:**`.
- Blank line before the callout opening tag (except inside table cells).

### Tables
- Pipe tables: columns must be padded so pipes align. Run the normalizer after revising (see Step 5).
- HTML tables: one tag per line; data rows inside `<tbody>`, not `<thead>`. See the style guide's **Tables › HTML tables** section for the canonical form.

### Links
- Internal links use the repo path with no `.mdx` extension and no full URL (`/s/article/Article-Title`, not `https://domo-support.domo.com/...`).

### Em-dashes
- No spaces in prose: `tools—such as`, not `tools — such as`.
- Exception: spaces only in the bolded-term list format (`**Term —** description`).

### Voice and word choice
- Present tense — not "will".
- Active voice.
- "after", not causal "once".
- No "utilize" — use "use".
- Spell out numbers under 10 in prose.
- "allowlist"/"blocklist" (not whitelist/blacklist).
- "select", not "click".
- Oxford comma.
- No exclamation points.

### Domo-specific terms
Verify every Domo product term against the **Domo-Specific Terms and Usage** table in the style guide. Key terms:
- `DataSet` (capital S), `DataFlow` (capital F), `DataFusion`, `Beast Mode`, `Workbench`
- `dashboard` lowercase (except at sentence start or when paired with a type like "Sumo dashboard")
- Never "Page" — use "dashboard"

### Beta treatment
- **Whole-article beta:** `tag: "Beta"` in frontmatter + standard verbatim beta Note above the Intro.
- **Section-level beta:** `<Badge className="text-primary bg-primary/10 font-bold">Beta</Badge>` appended to the section heading + one standard beta Note under the first beta section only.
- **GA:** no beta tag, badge, or Note.
- Convert any legacy beta markers (`(Beta)` in titles, ad-hoc notes, `betafeedback@domo.com` references) to the current convention.

### Images
- Block screenshots must be wrapped in `<Frame>` containing a native `<img>` with descriptive `alt` text. No inline `width` or `height` on block screenshots.
- Inline UI glyphs use the Domo icon font: `<i className="icon-{name}" aria-hidden="true" />` for current Domo UI; `<i className="legacy-icon-{name}" aria-hidden="true" />` for release notes / Workbench.
- Third-party brand logos: Font Awesome brands via `<Icon icon="{slug}" iconType="brands" aria-hidden="true" />` or inline `<svg fill="currentColor">` — not `<img>` (disappears in dark mode).
- Never `<Frame>` inside a table cell.
- When an inline icon is used, verify the surrounding prose names the icon (e.g., "select the **More** icon <icon>"). If it doesn't, rewrite the prose to include the name.

### MDX encoding conventions
- Follow the structural template from `New-Article-Template.mdx` for section order, component syntax, and code block formatting.
- Ensure all JSX components are properly closed and attributes are quoted.

---

## Step 5: Run the table normalizer

For every file you revised that contains a pipe table, run:

```bash
python3 scripts/pad_md_tables.py <file>
```

This is idempotent — run it even if you didn't touch the table directly.

---

## Step 6: Preview the diff

After all revisions are saved, run:

```bash
git diff
```

Present a brief summary to the user:
- List each file revised.
- For each file, name the categories of fixes applied (e.g., "fixed intro framing, bolded callout labels, corrected two Domo terms").

Then tell the user: **"Review the diff above. Reply 'looks good' (or similar) to commit and push, or let me know what to adjust first."**

Do not commit or push until the user explicitly approves.

---

## Step 7: Commit and push

After the user approves, commit the revisions and push them to the branch:

```bash
git add <list of revised files>
git commit -m "$(cat <<'EOF'
Apply style-guide and MDX convention revisions

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
git push
```

Use specific file paths in `git add` — never `git add -A` or `git add .`.

Confirm the push succeeded and tell the user the branch is updated.
