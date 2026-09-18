---
name: new-kb-article
user-invocable: true
description: "write a new KB article, generate knowledge base article, draft a KB doc, create a new article, write documentation, create MDX article"
argument-hint: "article title or topic, or paste any source material"
---

Generate a new Domo Knowledge Base article as an MDX file.

The user will provide: $ARGUMENTS

---

## Step 1: Run the kb-intake skill

Before writing anything, invoke the `kb-intake` skill, passing `$ARGUMENTS` directly as the input. Let the Socratic intake conversation run to completion, ending with the Article Intake Summary.

Use the original source material and the Article Intake Summary as the authoritative source of truth for everything that follows — it defines the title, persona, structure, scope, and key details of the article. If there are conflicts between the original source material and the Article Intake Summary, the Article Intake Summary takes precedence. Be sure to call out any discrepancies and be clear to the user about which information is taken as the truth.

---

## Step 2: Look up PM ownership

Before gathering release information, identify the PM who owns this article's feature area. Search `Article-PM-Ownership-Reference.mdx` for the closest matching Feature name:

```bash
grep -i "feature keyword" Article-PM-Ownership-Reference.mdx | head -5
```

If the feature is brand-new and not yet in the reference, find the closest matching Feature in the reference (or in `Feature - Owning Squad, PM, Eng, UX.csv`) and note that PM as the likely owner. Surface the PM name to the user so they can route review, approvals, or follow-up questions.

---

## Step 3: Gather release information

After the Article Intake Summary is confirmed, ask the following questions before writing:

1. **Release status:** What is the release status of the feature(s) covered in this article? For each distinct feature or section, is it GA (generally available) or beta? If mixed, which parts are beta?
2. **Planned branch cut date:** What is the planned **branch cut date** for this release? This is the internal branch name (NOT the feature release date).
3. **Feature switch date:** (Ask only if the article is tied to a GA release.) On what date do customers see the feature? This determines the branch name and the base branch (see **Step 10**). Do not try to derive it from the branch cut date; if the user doesn't know it, tell them the article can't be routed to a GA branch until they get it from the PM or release checklist.

---

## Step 4: Decide how to handle screenshots and icons

Ask the user up front how they want to handle screenshots for this article, and whether it will use any UI icons, before you draft. (If the `kb-intake` Article Intake Summary already captured this, confirm it rather than re-asking.)

### Screenshots

Offer these options with AskUserQuestion:

1. **User provides screenshots** — the user will supply the image files. They must be committed to `images/kb/` on the same branch *before* the article references them (see `CLAUDE.md` › **MDX Content Conventions**). Ask for the exact filenames and reference them with the syntax below.
2. **Reuse existing screenshots** — pull applicable screenshots that already exist in the repo or in the source material, preserving their original `alt` text.
3. **No screenshots** — text only.
4. **Insert placeholders (opt-in only)** — leave `{/* SCREENSHOT: <what the image should show> */}` markers where a human will capture images later. **Only do this if the user explicitly chooses it.** The default is clean articles with no TODO or placeholder markers.

Whichever option is chosen, write every step so the text is self-sufficient — a reader can complete the task without ever seeing a screenshot. Screenshots are supplemental, never load-bearing.

**Screenshot coding reference** (from `Domo-KB-Style-Guide.mdx` › **Screenshots** and **Inline Images**):

- **Block screenshot:** wrap in `<Frame>` with a native `<img>` and descriptive `alt`; no inline `width`/`height` (they override Frame's auto-sizing). Image files live in `images/kb/` and are referenced by a root-relative path:

  ```mdx
  <Frame>
    <img src="/images/kb/example.png" alt="Descriptive alt text" />
  </Frame>
  ```

- **Never** put a `<Frame>` inside a table cell — use an inline `<img>` there.

### Icons

Ask whether the article will show any UI icons or third-party logos. If yes, code them as follows (see `Domo-KB-Style-Guide.mdx` › **Icons** and **Brand and Third-Party Logos**):

- **Current Domo UI glyph** — the Domo icon font (Phosphor): `<i className="icon-{name}" aria-hidden="true" />`. Add a size class such as `sm`, or `style={{fontSize: 24}}` only if one icon looks visibly wrong. Browse names at [Domo Icons](https://git.empdev.domo.com/pages/Development/DomoIcons/#!/icons/phosphor).
- **Legacy UI glyph** — `<i className="legacy-icon-{name}" aria-hidden="true" />`. Same glyph set, older styling. Use **only** for release notes describing the pre-refresh UI and legacy apps such as Workbench.
- **Third-party brand logo** (AWS, OpenAI, GitHub, …) — Font Awesome brands: `<Icon icon="{slug}" iconType="brands" aria-hidden="true" />`. If the free FA set lacks it (e.g. Anthropic), inline `<svg fill="currentColor" …>` with a path from [Simple Icons](https://simpleicons.org). Never a monochrome `<img>` logo — it disappears in dark mode.
- **Glyph genuinely not in the font** — fall back to an inline `<img>` with `style={{height: '1.2em', display: 'inline', verticalAlign: 'start', margin: '0'}}` (use `'2em'` for a header or table-cell row label).
- **Accessibility** — always add `aria-hidden="true"` and name the icon in the surrounding prose ("select the gear icon `<i …/>`"). Reserve `role="img"` + `aria-label` for an icon that stands alone with no prose to name it.
- **Do not** use the old inline-image icon pattern (`<img src="/images/kb/*-icon.png" style={{width: 20, height: 20, …}}/>`) for any glyph that exists in the font — that is the legacy pattern being phased out.

---

## Step 5: Read the style guide and article template

Before writing, read both of these files:

1. **`Domo-KB-Style-Guide.mdx`** — the authoritative style guide. Apply every rule in this file when writing the article.
2. **`New-Article-Template.mdx`** — the canonical file structure and encoding conventions (frontmatter, section order, image syntax, callout components, code blocks, tables, etc.). Use this as the structural template for the new article.

---

## Step 6: Write the article

Once the Article Intake Summary, release information, style guide, and template are all loaded, create the MDX file. Do not ask for any information already answered.

**The drafting default — preserve the source's wording.** The Article Intake Summary, the user's own answers, any pasted notes or draft, and the original source material were written by people who know the feature; their word choice carries nuance about how the functionality actually behaves. Your default is to **keep their direct phrasing and word choice**, not to rewrite the content in your own words:

- **Take the source text as-is** wherever it already works, and **reorganize** it into the article structure from `New-Article-Template.mdx`. Reordering and regrouping source sentences is expected; paraphrasing them for its own sake is not.
- **Recast the framing, keep the wording.** House voice (present tense, active voice, imperative task headings, second person) is a style rule — shift grammatical framing into it where the source doesn't already match. But that is the *only* rewrite you make by default: swapping the author's precise term for a synonym, or restating a described behavior in looser words, is not allowed. Preserve the substance (specific verbs, named behaviors, qualifiers, terminology); recast the frame.
- **Add text only where genuinely needed** for flow or structure — e.g., a missing one-sentence intro to the product, or a connective clause between two source passages. Don't pad, and don't invent capability detail.
- **Revise wording only where it breaks a rule** — a `Domo-KB-Style-Guide.mdx` style/voice/term rule, or a `New-Article-Template.mdx` MDX/structure convention. Fidelity never overrides the style guide; it governs everything the style guide doesn't touch.
- **If information is missing, ask the user** — never fill a gap with plausible-sounding content.

Create a new MDX file in `s/article/` using the filename format `Article-Title-Here.mdx` (Title Case, hyphen-separated, no special characters).

Follow the structure from `New-Article-Template.mdx` and apply all style rules from `Domo-KB-Style-Guide.mdx` exactly.

### Use canonical grant wording in Required Grants

When writing the **Required Grants** section, do not invent grant descriptions. Most grants are already described in the standard format elsewhere in the KB — search for and reuse the existing wording so the grant reads consistently across articles:

```bash
grep -rn "Grant Name —" s/article/
```

Reuse the existing description verbatim (adjusting only to fit the em-dash format). If no article describes the grant, write a concise one-sentence description and flag it to the user as newly authored. See `Domo-KB-Style-Guide.mdx` › **Required Grants** › _Use canonical grant wording_.

### Apply the beta convention (if applicable)

Use the release-status answer from Step 3 to decide which beta treatment, if any, to apply. The full convention lives in `Domo-KB-Style-Guide.mdx` › **Beta Features** — read it before writing.

- **Entire article is beta:** add `tag: "Beta"` to the frontmatter and place the standard beta Note immediately after the frontmatter, above the Intro. Do not append `(Beta)` to the title.
- **Only certain sections are beta:** append `<Badge className="text-primary bg-primary/10 font-bold">Beta</Badge>` to each beta section's heading. Place the standard beta Note under the **first** beta section only — do not repeat it for subsequent beta sections in the same article. Do not append `(Beta)` to any heading.
- **Entire article is GA:** no beta tag, badge, or Note.

The `className` on the Badge is required and must be exactly `text-primary bg-primary/10 font-bold` — it matches the sidebar `tag` styling.

The standard beta Note must be used verbatim — do not paraphrase or change the links. Copy it from the style guide.

---

## Step 7: Fact-check pass

Before the edit pass, and before considering the copy complete, verify every factual claim in the draft at least once against an authoritative source: the source material the user provided, the `kb-intake` Article Intake Summary, and the repo itself. This pass is about **accuracy**, not style — the style and template edit comes next. When you correct an unsupported claim, prefer restoring the source's own wording over inventing a replacement.

1. **Go claim by claim.** For each statement of fact — steps, behaviors, settings, defaults, names, values, URLs, limits — confirm it against the source material or existing repo content. Where the repo is the authority, search it and read the relevant article rather than trusting the draft:
   ```bash
   grep -rl "feature or setting name" s/article/ s/topic/
   ```

2. **Verify Prerequisites and Required Grants with special care.** These are the highest-risk sections and the most common source of factual errors:
   - Confirm each prerequisite is real and actually required for the task.
   - Confirm each grant name exists and gates the described action. Cross-check the canonical grant wording (`grep -rn "Grant Name —" s/article/`) and any related feature articles in the repo.
   - If the source material and the intake summary don't establish the exact prerequisites and grants, **do not infer them — ask the user.**

3. **When you can't confirm a claim, or you find an inaccuracy or a discrepancy, STOP and ask the user directly** for the missing or correct information before finalizing. Do not guess, approximate, or fill gaps with plausible-sounding content. Name exactly what you couldn't verify and what you need. If the source material and the intake summary conflict, surface the conflict and confirm which is authoritative (per Step 1, the intake summary wins unless the user says otherwise).

The article is not complete until every factual claim is either confirmed against a source or explicitly confirmed by the user. **When in doubt, ask** — a paused draft beats a confidently wrong one.

---

## Step 8: Edit pass — style guide and template

Drafting always introduces style drift. After the fact-check pass, do an explicit editing pass against **both** `Domo-KB-Style-Guide.mdx` **and** `New-Article-Template.mdx`, and revise the article in place. This pass catches every usage, style, grammar, and structural mistake. As you fix style, keep the source's substantive wording intact — change only what a rule requires, exactly as at Step 6. **Do not skip this even if the draft looks right** — the most common misses (intro framing, imperative headings, unpadded tables, lowercase Domo terms, future tense) are easy to introduce and easy to miss without a deliberate re-read.

1. **Re-read `Domo-KB-Style-Guide.mdx` and `New-Article-Template.mdx` now, in full** — not from memory. You will have drifted from at least one rule while drafting. Confirm the article's structure and encoding match the template (frontmatter, section order, component syntax, code blocks, tables).
2. **Proofread for plain grammar and usage** — spelling, subject-verb agreement, punctuation, and sentence clarity — in addition to the Domo-specific rules below. A factually correct article still isn't done if it reads poorly.
3. **Audit the article against this checklist** and fix every violation in both the EN file and the JA sibling, if you authored one:
   - **Frontmatter** — `title` plus a single-sentence `excerpt`; never a `description` field.
   - **Intro** — opens with "This article explains…" or "This article covers…", states only what the article covers (not why it matters), and is immediately followed by a `---` horizontal rule.
   - **Headings** — imperative mood at every level (H2–H4); the structural labels (Intro, Required Grants, Prerequisites, FAQ, Troubleshoot, Related Articles) are exempt. Top-level sections are H2, subsections H3+.
   - **Required Grants** — exact format and canonical grant wording, with the em-dash inside the bold and a space on each side (`**Grant —** description`).
   - **Callouts** — `<Note>`/`<Warning>`/`<Tip>` with the label and its colon bolded (`**Note:**`), and a blank line before the callout (except inside table cells).
   - **Tables** — every pipe table padded so columns align. Run `python3 scripts/pad_md_tables.py <file>` to do this mechanically. Normalize any HTML tables (one tag per line, data rows in `<tbody>`).
   - **Links** — internal links use the file path with no `.mdx` extension and no full URL.
   - **Em-dashes** — no spaces in prose (`tools—such as`); spaces only in the bolded-term list exception.
   - **Voice and word choice** — present tense, not "will"; active voice; "after", not causal "once"; no "utilize"; spell out numbers under 10; "allowlist"/"blocklist"; "select", not "click"; Oxford comma; no exclamation points.
   - **Domo terms** — `DataSet`, `DataFlow`, `DataFusion`, `Beast Mode`, `Workbench`; `dashboard` lowercase except at the start of a sentence or with a type; never "Page" (use "dashboard"). Verify any product term against the **Domo-Specific Terms and Usage** table.
   - **Beta** — correct convention applied (frontmatter `tag` + verbatim Note for a whole-article beta; Badge + single verbatim Note for section-level).
   - **Images** — block screenshots wrapped in `<Frame>` with a native `<img>` and descriptive `alt`, no inline `width`/`height`; never `<Frame>` inside a table cell. Verify any placeholders match what the user chose in Step 4 (none unless they opted in).
   - **Icons** — current UI glyphs use the `icon-{name}` font; `legacy-icon-{name}` only for release-notes/Workbench surfaces; brand logos use Font Awesome brands or inline `<svg fill="currentColor">`; never the old inline-image icon pattern for a glyph that exists in the font. Each icon carries `aria-hidden="true"` and is named in the prose.
4. **Revise the article in place** to resolve every issue found, then re-run the table normalizer if you changed any tables.

---

## Step 8.5: Align with the user on the copy (final approval)

Now that the draft has been fact-checked (Step 7) and style-edited (Step 8), show the user exactly what you've written and get their approval on the copy — **every time**, no exceptions. This is the single point where the user reviews the words, and it comes *only after* the copy has been verified and styled — never before.

- Present the finished article (a section-by-section view helps wherever you recast source wording for style).
- Call out anything you **added** beyond the source, any place you **recast** source wording to satisfy the style guide, and any spot where you're **missing** information the source didn't supply.
- **This is where any wording change the user or PM wants gets made.** Fold in their edits, then re-run the relevant parts of the fact-check (Step 7) and edit (Step 8) passes over anything you changed, so the final copy stays accurate and on-style.
- If you need missing detail, ask for it now and fold in the answer — don't invent it.

Only after the user approves the copy do you proceed to navigation and handoff.

---

## Step 9: Add the new article to navigation

A new article file does not appear on the site until it is registered in `docs.json`. As the final step, invoke the `add-to-nav` skill to place the article in the navigation — do not edit `docs.json` by hand:

- **Page path:** `s/article/Article-Title-Here`
- **Operation:** Insert
- **Target:** the group or subgroup that best fits the article's topic. If you are unsure where it belongs, let `add-to-nav` surface the placement options and use AskUserQuestion to confirm the location with the user.

After `add-to-nav` edits `docs.json`, confirm it is still valid JSON:

```bash
python3 -c "import json; json.load(open('docs.json')); print('docs.json is valid JSON')"
```

---

## Output

1. Tell the user the file path of the new MDX article (`s/article/Article-Title-Here.mdx`).
2. Confirm the article was added to `docs.json` navigation and state where it was placed.
3. Note any sections left as placeholders (screenshots, specific grant names, etc.) that the user will need to fill in — and any fact-check items you flagged in Step 7 that still need the user's confirmation.
4. State the branch name and PR base branch the article should use, per **Step 10**.

---

## Step 10: Branch and PR routing

Tell the user which branch and base branch this article belongs on. Do not create the branch or open the PR unless they ask.

**If the article is not tied to a GA release:** branch `first.last/short-description`, base `main`. It publishes on the normal weekly KB schedule (PR in by Thursday for the following Monday).

**If the article is tied to a GA release:** use the feature switch date collected in Step 3. Name the branch `first.last/Article-Title-ga-MM-DD-YYYY` (zero-padded numeric date — the date customers see the feature). Keep the `-ga-<date>` suffix on any GA-tied branch — it is how the Knowledge Base Administrator knows the feature's availability date. **Never tell a contributor to drop the suffix just to base onto `main`.**

Two kinds of GA work route differently. Check whether a GA train branch exists for that date:

```bash
git branch -r | grep release-ga
```

- **On the company GA release train** — a matching `release-ga/<spelled-month-date>` branch exists (e.g. `release-ga/sept-23-2026`): base the PR onto that `release-ga/*` branch. It merges to `main` with the rest of the train on the feature switch date.
- **No matching `release-ga/*` branch:** don't assume. Ask the contributor whether this is part of the monthly company GA train or a standalone, off-train product GA (an article tied to one product feature that ships on its own date, outside the company-wide train — this is common):
  - *Company train, branch not created yet:* the Knowledge Base Administrator needs to create the `release-ga/*` branch. Do not fall back to `main`.
  - *Off-train standalone product GA:* keep the `-ga-<date>` suffix and base the PR onto `main`. The suffix records when that product feature reaches customers; the KB Administrator holds the PR open and merges it on or after the `-ga-` date so it publishes in sync with the feature. Assign it to the KB Administrator and call out the GA date in the PR description.

See `CLAUDE.md` › **Contribution Workflow** for the full convention.

---

## Step 11: Offer localization

After delivering the output above, ask the user:

> "Would you like to localize this article into Spanish, French, and German? (Note: Japanese localization is handled on a separate pipeline — no action needed there.)"

- **If yes:** invoke the `localize` skill, passing the new article's file path as the argument.
- **If no:** the skill ends here.
