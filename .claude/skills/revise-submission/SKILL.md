---
name: revise-submission
user-invocable: true
description: "Revise the MDX content in the current branch's PR for Domo style guide compliance and MDX code conventions, validate that any newly added images exist and will render, and validate that docs.json changes are relevant and won't break site navigation — then preview the diff before committing and pushing."
argument-hint: "optional: a specific file or concern to focus on; otherwise all changed MDX files are revised"
---

Revise the MDX content committed on the current branch for style and convention compliance, validate that any images newly referenced by the changed articles exist and are encoded so they will render, validate that any `docs.json` changes are relevant to this PR and won't break the site navigation once published, then let the user preview the diff before committing the changes and pushing them to the branch.

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

Exclude everything in the localized roots (`de/`, `es/`, `fr/`, `ja/`) — those are never touched by this skill. Also exclude `docs.json`, `images/`, `openapi/`, `.csv`, and any non-`.mdx` file from the style-revision pass. (`docs.json` and the images referenced by the changed articles are not *revised*, but they are *validated* later — see Step 5 and Step 6.)

If `$ARGUMENTS` names a specific file, revise only that file (confirm it exists in the PR diff first). Otherwise, revise every qualifying file found above.

If there are no qualifying MDX files in the PR, tell the user and stop.

### Check the base branch against the branch name

Using the `headRefName` and `baseRefName` already returned above, verify the PR targets the right base. This is cheap to check here and expensive to catch after merge.

- If `headRefName` contains `-ga-<month>-<year>` and `baseRefName` is `main`, don't assume it's wrong — this is correct for an **off-train** standalone product GA, where the KB Administrator holds the PR and merges it on the feature's switch date within the `-ga-` month. It's only a mistake if the work belongs to the company-wide monthly GA train, in which case it should base onto the `release-ga/*` branch for that month (`release-ga/<month>-<year>`, such as `release-ga/november-2026`; confirm with `git branch -r | grep release-ga`). If a matching `release-ga/*` branch exists, mention that the PR may belong on it; if none exists, note that main is expected for off-train GA and leave routing to the contributor. Never suggest dropping the `-ga-<month>-<year>` suffix. See `CLAUDE.md` › **GA Release Workflow**.
- If `baseRefName` is a `release-ga/*` branch but `headRefName` has no GA month, mention it. Either the branch name is missing its `-ga-<month>-<year>` suffix or the base is wrong.

Report the mismatch and let the user decide whether to retarget the PR. Do not retarget it yourself, and do not let this block the style revision. Continue to Step 2 either way.

See `CLAUDE.md` › **Contribution Workflow** for the convention.

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
- Use `description` (single sentence, phrased simply and directly — imperative for a task article, plain declarative for a conceptual/overview article — with no "This article explains…" / "This article covers…" preamble; Markdown such as inline code is allowed), not `excerpt`. If a legacy `excerpt` field is present, replace it with `description` (reuse its sentence, recast into the direct format).
- If the article is beta: `tag: "Beta"` present in frontmatter and the standard beta Note appears immediately after the frontmatter, above the article body.

### Lead sentence and Intro
- The one-sentence summary lives in the `description` frontmatter, not the body.
- Most articles have no `## Intro` section. When one is present (extra context only), it has no `---` horizontal rule after it.
- Do not add or remove an existing legacy `## Intro` section wholesale here — that bulk migration is handled separately. Only fix an Intro that falls within the content you are already revising.

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
- Pipe tables: columns must be padded so pipes align. Run the normalizer after revising (see Step 7).
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
- **Whole-article beta:** `tag: "Beta"` in frontmatter + standard verbatim beta Note immediately after the frontmatter, above the article body.
- **Section-level beta:** `<Badge>Beta</Badge>` (no `className`) appended to the section heading + one standard beta Note under the first beta section only.
- **GA:** no beta tag, badge, or Note.
- Convert any legacy beta markers (`(Beta)` in titles, ad-hoc notes, `betafeedback@domo.com` references) to the current convention.

### Images
- Block screenshots must be wrapped in `<Frame>` containing a native `<img>`. No inline `width` or `height` on block screenshots.
- **Alt text is required on every screenshot and content image** — detailed and accurate, for accessibility compliance, LLM readability, and SEO (`Domo-KB-Style-Guide.mdx` › **Alt Text Is Required on Every Screenshot**). Flag any image with weak or missing alt text (empty `alt=""`, `"screenshot"`, `"image"`, a filename, a bare `alt-text-here` placeholder, or alt that's too vague to convey what the image shows). Where you can tell what the image shows from the surrounding prose, rewrite the alt to describe it accurately; where you can't, surface it to the user as a fix they must supply — don't invent a description of an image you can't see. Decorative inline icons already named in the prose are the exception (they use `aria-hidden="true"`, not alt).
- Inline UI glyphs use the Domo icon font: `<i className="icon-{name}" aria-hidden="true" />` for current Domo UI; `<i className="legacy-icon-{name}" aria-hidden="true" />` for release notes / Workbench.
- Third-party brand logos: Font Awesome brands via `<Icon icon="{slug}" iconType="brands" aria-hidden="true" />` or inline `<svg fill="currentColor">` — not `<img>` (disappears in dark mode).
- Never `<Frame>` inside a table cell.
- When an inline icon is used, verify the surrounding prose names the icon (e.g., "select the **More** icon <icon>"). If it doesn't, rewrite the prose to include the name.

### MDX encoding conventions
- Follow the structural template from `New-Article-Template.mdx` for section order, component syntax, and code block formatting.
- Ensure all JSX components are properly closed and attributes are quoted.

---

## Step 5: Validate newly added images render

When this PR adds image references to any article, a reference that points at a missing or corrupt file ships a broken image. Per `CLAUDE.md`, every image must be committed to `images/kb/` on the same branch *before* an article references it. For how Mintlify serves and optimizes images, read the **`mintlify`** skill (`.claude/skills/mintlify/SKILL.md`) › **Images** — load it if you need the detail.

Scope this to image references that are **new or changed in this PR**. Get the added lines from each revised file's diff:

```bash
git diff $(git merge-base HEAD origin/main) -- <file> | grep -E '^\+' | grep -oE '(src="[^"]+"|\]\([^)]+\))'
```

From those added lines, collect every referenced image path — Markdown `![alt](/images/kb/…)`, `<img src="/images/kb/…">` (including the native-`<img>` icon fallback), and the `<img>` inside a `<Frame>`. Image paths are root-relative, so `/images/kb/foo.png` maps to `<repo-root>/images/kb/foo.png`. Ignore `<DomoEmbed src>` (an iframe URL, not an image) and absolute `http(s)://` image URLs (hosted elsewhere — note them, but you can't validate them locally).

For each new image path, verify all of the following. Report any that fail — never invent or substitute a file:

1. **The file exists** at the repo-relative path:
   ```bash
   test -f ".<path>" && echo exists || echo MISSING
   ```
2. **It is tracked on this branch** (committed, not just an untracked file sitting on disk):
   ```bash
   git ls-files --error-unmatch ".<path>" >/dev/null 2>&1 && echo tracked || echo UNTRACKED
   ```
3. **It will render** — the bytes are a real image whose encoding matches the extension:
   ```bash
   file --mime-type -b ".<path>"
   ```
   - The MIME type must be an `image/*` type consistent with the extension (`.png` → `image/png`, `.jpg`/`.jpeg` → `image/jpeg`, `.gif` → `image/gif`, `.webp` → `image/webp`). A mismatch (e.g. a `.png` whose bytes are really `image/jpeg`), a non-image type, a zero-byte file, or a Git LFS pointer (shows as `text/plain` beginning `version https://git-lfs…`) all mean the image won't render as referenced.
   - `.svg`: Mintlify serves SVGs unoptimized and doesn't accept SVG for optimized page images, and a monochrome SVG disappears in dark mode. Flag an SVG page screenshot as a **warning** (prefer a coded icon per the style guide), but don't hard-fail it.

Also check the reverse — image files this PR **adds** that **no** changed article references (an orphaned asset, or a reference spelled wrong):

```bash
git diff --name-only --diff-filter=A $(git merge-base HEAD origin/main) -- images/
```

Fix what's safely fixable (a wrong path or extension you can confirm against an existing file). For a genuinely missing or corrupt image, surface it to the user as a fix they must supply — name the article, the referenced path, and exactly what's wrong. Carry every finding into the Step 8 summary.

---

## Step 6: Validate docs.json changes

`docs.json` is excluded from the style pass, but when the PR touches it you must do two things: confirm every change belongs to *this* PR, **and actively validate that the navigation will still work once published** — a malformed `docs.json` breaks the whole site nav on build. For how navigation works, read the **`mintlify`** skill › **Navigation** / **Global settings**.

First, did `docs.json` change at all?

```bash
git diff --name-only $(git merge-base HEAD origin/main) -- docs.json
```

### If `docs.json` changed

**1. Gate on nav validity first — the `add-to-nav` skill's verification step (Step 5 › Verify).** Invalid JSON (a trailing comma, an unclosed array, a stray quote) makes Mintlify drop or fail the navigation once published, so this is the check that most directly answers "will this break the site." Run the same validity check `add-to-nav` uses:

```bash
node -e "JSON.parse(require('fs').readFileSync('docs.json', 'utf8')); console.log('docs.json is valid JSON');"
```

If it throws, the nav is broken — show the error, locate the offending edit in the diff, and fix it (or hand it back to the user) before going any further. **Never let an invalid `docs.json` reach the preview.**

If the `mint` CLI is installed, also run Mintlify's deeper nav checks — they catch broken nav targets and links that valid JSON alone won't:

```bash
mint validate --no-build --format json
mint broken-links
```

Fix anything these flag that your change introduced. If `mint` isn't installed, skip them and rely on the JSON gate plus the target-resolution check below.

**2. Confirm the changes are relevant and the targets resolve.** Read the diff:

```bash
git diff $(git merge-base HEAD origin/main) -- docs.json
```

- **Every page path newly added to the nav must resolve to a real file.** A nav entry is a slug like `s/article/My-Article` → `s/article/My-Article.mdx`. Verify the target exists on the branch:
  ```bash
  test -f "<slug>.mdx" && echo ok || echo "MISSING TARGET"
  ```
  A nav entry pointing at a file that doesn't exist on the branch is a broken nav link — flag it and fix the slug or add the file.
- **Changes should be scoped to this PR.** Flag edits not explained by the PR's added/removed/moved articles: unrelated group reordering, pages removed that this PR didn't touch, or theme/color/redirect/settings changes that don't belong in a content PR (`CLAUDE.md` › **Pull Requests**, one topic per PR).
- **Localized nav exception:** for `ja` Data Providers connector entries, ordering follows Japanese collation of the Japanese title, not the English order (`CLAUDE.md` › **Navigation parity exception**). Don't flag a JA connector that's correctly alphabetized in Japanese.

### If `docs.json` did NOT change but the PR adds net-new articles

Those articles won't appear in the sidebar. For each net-new `s/article/` or `s/topic/` file the PR adds, check whether its slug is present in `docs.json`:

```bash
grep -c "s/article/<slug>" docs.json
```

If a new article is absent, flag it as a likely missing nav entry — unless it's an intentional link-only / closed-beta page deliberately kept out of the nav (see `CLAUDE.md` and project memory on closed-beta nav exclusion). When in doubt, surface it and let the user decide.

Route any nav *edit* through the `add-to-nav` skill rather than hand-editing `docs.json` here — but always re-run the JSON validity gate above after any such edit, since this skill's job is to guarantee the nav still builds. Carry every finding into the Step 8 summary.

---

## Step 7: Run the table normalizer

For every file you revised that contains a pipe table, run:

```bash
python3 scripts/pad_md_tables.py <file>
```

This is idempotent — run it even if you didn't touch the table directly.

---

## Step 8: Preview the diff

After all revisions are saved, run:

```bash
git diff
```

Present a brief summary to the user:
- List each file revised.
- For each file, name the categories of fixes applied (e.g., "recast the description into the 'This article…' format, bolded callout labels, corrected two Domo terms").
- **Image validation (Step 5):** report any newly referenced image that is missing, untracked, or wrongly encoded, and any orphaned added image — or state that all newly added images exist and will render. Separate findings you fixed from findings the user must resolve (a missing or corrupt image file the author has to supply).
- **docs.json validation (Step 6):** state the result of the JSON-validity gate (and `mint validate` / `broken-links` if run), then report any nav entry pointing at a missing file, any change unrelated to this PR, or any net-new article missing from the nav — or state that `docs.json` is valid and its changes are relevant and complete (or that `docs.json` wasn't changed).

Then tell the user: **"Review the diff above, along with the image and docs.json findings. Reply 'looks good' (or similar) to commit and push, or let me know what to adjust first."**

Do not commit or push until the user explicitly approves.

---

## Step 9: Commit and push

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
