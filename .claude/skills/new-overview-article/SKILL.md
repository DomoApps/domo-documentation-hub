---
name: new-overview-article
user-invocable: true
description: "write an Overview article, create a product overview, draft a feature overview article, write a 'What is X' article, build a SaaS-style overview that links to deeper how-tos"
argument-hint: "product or feature name (e.g., 'Analyzer', 'DomoStats', 'Beast Mode')"
---

Generate a Domo Knowledge Base **Overview article** for a Domo product or feature.

The user has provided: $ARGUMENTS

An Overview article is a distinct article type. It is **not** a how-to. Its job is to:

1. Explain conceptually what the product or feature is.
2. State the high-level use cases and outcomes.
3. Surface the required grants and the access path.
4. Cluster links to every related deep-dive article in the repo, organized by purpose.
5. Anchor a small FAQ with the highest-leverage questions a new reader asks.

If the user's request is for a how-to article instead, stop and recommend the `new-kb-article` skill.

---

## Step 1: Identify the product or feature

If `$ARGUMENTS` names a product or feature, use that. Otherwise ask the user which one in a single short question — do not run a full Socratic intake. Overview articles are scoped to a single product or feature surface.

Capture in plain English:

- **Product/feature name** as it appears in the product and the style guide (e.g., `Analyzer`, `DomoStats`, `Beast Mode`, `Cloud Integrations`).
- **Audience** — who reads this? Admins? Analysts? End viewers? Usually a mix; default to "Domo customers across roles" unless the user narrows it.

Do NOT proceed to research or drafting until the name is locked in. The name drives every grep and every link in the rest of the process.

---

## Step 2: Check for title collisions

This step is mandatory. Skipping it is the single biggest failure mode for new Overview articles, because Domo's legacy SF migration left many articles with titles like `<Product> Overview` that are actually how-tos.

Run:

```bash
grep -rl "^title: \".*<Product>.*Overview\"" s/article/
grep -rl "^title: \"<Product>" s/article/
```

For each match, read the frontmatter and the first ~30 lines and decide:

- **No collision** — proceed to Step 3.
- **Legacy article with the title `<Product> Overview` already exists but is actually a how-to** — surface this to the user before writing. Use AskUserQuestion to offer:
  1. **Replace in place** — rewrite the legacy article's body to be a real Overview. Keeps the URL slug, preserves nav position, requires JA parity update only.
  2. **New file + rename legacy** — create the new Overview at `s/article/<Product>-Overview.mdx`, rename the legacy article's title to reflect its actual content (file path stays the same so no redirect needed). Update JA sibling title to match.
  3. **Brand-new file with a different title** — sidestep the collision (e.g., "What Is X?"). Leaves the legacy article alone.

  Default recommendation is option 2 unless the legacy content is so close to a real Overview that a rewrite-in-place is cleaner.

- **Article with the same title but in a different language directory** (`ja/s/article/...`) — that is a JA sibling, not a collision; note it for the JA parity step.

Stop and confirm the chosen handling before continuing.

---

## Step 3: Inventory existing content for the product

Map every repo article that touches the product. These become the link list in the body. Run these searches and collect the resulting set:

```bash
# Articles whose title mentions the product
grep -l -E "^title: \".*<Product>" s/article/*.mdx

# Articles whose body mentions the product (broader net)
grep -rli -E "(\\b<product>\\b)" s/article/ s/topic/

# The product's current location(s) in docs.json
grep -n "<Product>" docs.json
```

For each article hit, pull the title and excerpt so you know what to link to:

```bash
for f in <id1> <id2> ...; do
  echo "$f: $(grep -m1 '^title:' s/article/${f}.mdx)"
done
```

If the inventory is large (more than ~30 candidate articles), spawn an `Explore` sub-agent with a prompt like: *"Find every article in `s/article/` and `s/topic/` whose title, excerpt, or body materially discusses `<Product>`. For each, return the file path, title, and a one-line summary of how it relates to `<Product>`. Skip articles that only mention `<Product>` in passing."*

Save the resulting list — you'll group it in Step 7.

---

## Step 4: Confirm style-guide treatment for the product name

Open `Domo-KB-Style-Guide.mdx` and search the **Domo-Specific Terms and Usage** table for the product name. The table dictates:

- Whether to capitalize it
- Whether to use it with `the`
- Whether to bold it when referring to it conceptually vs. as a UI element

Apply that treatment consistently throughout the new article. Common pitfalls from past Overview drafts:

- `Analyzer` — do **not** use with `the`. Bold only when it is a UI element (e.g., **Open With** > **Analyzer**), not when discussing conceptually.
- `Beast Mode` — capitalize both words. The tool is "Beast Mode"; the calculations are "Beast Mode calculations" (not "a Beast Mode" as a noun for the calculation).
- `Cloud Integrations` — default to plural; singular only with a determiner.
- `DataSet`, `DataFlow`, `DataFusion` — one word, both caps.

If the product is not in the style-guide table, ask the user how it should be styled before writing.

---

## Step 5: Read the style guide and template

Before writing, read in full:

1. **`Domo-KB-Style-Guide.mdx`** — apply every rule.
2. **`New-Article-Template.mdx`** — use as the structural and encoding template.

Pay special attention to:

- **Frontmatter** — `title` plus a single-sentence `excerpt` (required). Never `description`.
- **Article structure** — Intro → horizontal rule → Required Grants → Access → body sections → FAQ → Related Articles.
- **Imperative-mood headings** — task headings are commands ("Build a Card", not "Building a Card"). Structural labels (`Intro`, `Required Grants`, `FAQ`, etc.) are exempt.
- **Bold + em-dash convention** for description lists — `**Term —** description`.
- **Internal links** — `[Title](/s/article/Title-Slug)` with no `.mdx`.
- **Voice** — present tense, active voice, no future tense. Spell out numbers under 10. No "utilize", no "whitelist/blacklist", no Latin abbreviations.

---

## Step 6: Decide how to handle screenshots and icons

Overviews are link-rich entry points, so they carry **no screenshots by default** — the deep how-to articles hold those. The one exception is a single optional hero screenshot of the product UI directly under the Intro, if it genuinely helps orient a new reader. Overviews *do* commonly use inline UI icons (for example in the **Access** section).

Before drafting, confirm with the user:

1. **Hero screenshot?** Ask whether they want the one optional hero screenshot. If yes, it must be committed to `images/kb/` on the same branch before the article references it (see `CLAUDE.md` › **MDX Content Conventions**), coded as a block screenshot (below). If no, skip it — that is the default.
2. **Placeholders are opt-in only.** Do not leave `{/* SCREENSHOT: … */}` markers unless the user explicitly asks for them. The default is a clean article with no TODO or placeholder markers.
3. **Icons?** Confirm whether the **Access** section and link clusters reference any UI icons, and code them per the reference below.

**Coding reference** (from `Domo-KB-Style-Guide.mdx` › **Screenshots**, **Icons**, **Brand and Third-Party Logos**):

- **Block (hero) screenshot:** `<Frame><img src="/images/kb/example.png" alt="Descriptive alt text" /></Frame>` — no inline `width`/`height`; never inside a table cell.
- **Current Domo UI glyph:** `<i className="icon-{name}" aria-hidden="true" />` (Phosphor font). Browse names at [Domo Icons](https://git.empdev.domo.com/pages/Development/DomoIcons/#!/icons/phosphor).
- **Legacy UI glyph:** `<i className="legacy-icon-{name}" aria-hidden="true" />` — only for release-notes/Workbench surfaces.
- **Third-party brand logo:** Font Awesome brands `<Icon icon="{slug}" iconType="brands" aria-hidden="true" />`, or inline `<svg fill="currentColor" …>` when the free FA set lacks it. Never a monochrome `<img>` logo — it disappears in dark mode.
- **Glyph not in the font:** inline `<img>` with `style={{height: '1.2em', display: 'inline', verticalAlign: 'start', margin: '0'}}`.
- **Accessibility:** always add `aria-hidden="true"` and name the icon in the prose; reserve `role="img"` + `aria-label` for an icon that stands alone.

---

## Step 7: Draft the article

Create `s/article/<Product>-Overview.mdx` (title-case filename, hyphen-separated, no `.mdx` collisions). The structure below is the canonical Overview shape — it is what the existing modern overviews (`Cloud Integrations Overview`, `App Studio | Overview`, `Variables | Overview`, plus the recently authored `Analyzer Overview` and `DomoStats Overview`) all converge on, and it differs from a generic how-to.

**The drafting default — preserve the source's wording.** Where the user gave you their own description of the product (Step 1) or you're reusing an existing article's `excerpt`/definition, **keep that direct phrasing and word choice** rather than restating it in your own words — the author's terms carry nuance about what the product is and does. Take the source text as-is and fit it into the Overview structure; **add** connective or framing text only where the structure needs it; and **revise wording only** to satisfy a `Domo-KB-Style-Guide.mdx` or `New-Article-Template.mdx` rule (recast grammatical framing into house voice, but keep the substantive terminology). If you're missing a definition, a use case, or an access path, **ask the user** — don't invent it. (An Overview is more structural than a how-to, so more connective text is normal here; the fidelity rule still governs every sentence you lift from a source.)

### Canonical Overview structure

```mdx
---
title: "<Product> Overview"
excerpt: "<One sentence describing what the product is and the main value it provides>."
---

## Intro

<Product> is <one-sentence definition that names the category — "Domo's chart-building tool", "Domo's built-in observability layer", "Domo's calculation engine">. <One or two more sentences naming the high-level use cases.> This article explains what <Product> is, how to access it, and points to the specific articles for each task.

<Optional: a 2-3 item description list of the major sub-parts of the product, if it has distinct halves (e.g., DomoStats has the connector + the QuickStart apps).>

- **<Sub-part name> —** <one-sentence description>.
- **<Sub-part name> —** <one-sentence description>.

---

## Required Grants

To <verb describing the primary action — open Analyzer, install DomoStats, create a Beast Mode>, the following grants must be enabled for your role:

- **<Grant Name> —** <one-sentence description of what the grant allows>.
- **<Grant Name> —** <one-sentence description>.

Learn more about [grants](/s/article/360043438973).

> **Use canonical grant wording.** Don't invent grant descriptions. Search the KB for an existing description in the standard format — `grep -rn "Grant Name —" s/article/` — and reuse it verbatim. If none exists, write a concise description and flag it as newly authored. See `Domo-KB-Style-Guide.mdx` › **Required Grants** › _Use canonical grant wording_.

## What You Can Do With <Product>

<Product> covers <one sentence framing the scope>. Common questions it answers / things you can do with it:

- **<Capability or use case> —** <one-sentence description>. <Optional: link to deep article inline.> See [Article Title](/s/article/...).
- **<Capability or use case> —** <one-sentence description>. See [Article Title](/s/article/...).
- **<Capability or use case> —** <one-sentence description>. See [Article Title](/s/article/...).

## Access <Product>

<One short paragraph or numbered list showing the 1–3 ways to open or get to the product. Reference the dedicated "Opening X" article if one exists.>

1. **From <surface 1>.** <Action sentence with the icon if applicable, e.g., select <i className="icon-pencil sm" aria-hidden="true" /> **Edit**.>
2. **From <surface 2>.** <Action sentence.>
3. **From <surface 3>.** <Action sentence.>

For a step-by-step walkthrough, see [Opening <Product>](/s/article/...).

## <Link Cluster Heading 1>

<One short sentence framing the cluster — what kind of task or surface this group of articles covers.>

- [<Article Title>](/s/article/...) — <one-sentence description of what the article covers, written in the same voice as the article's own excerpt>.
- [<Article Title>](/s/article/...) — <one-sentence description>.
- [<Article Title>](/s/article/...) — <one-sentence description>.

## <Link Cluster Heading 2>

<Same pattern as above. Group clusters by purpose — Build, Format, Manage, Govern, Best Practices, etc.>

- [<Article Title>](/s/article/...) — <one-sentence description>.
- [<Article Title>](/s/article/...) — <one-sentence description>.

## Best Practices

<If the product has 1–2 dedicated best-practices articles, link them here with one-sentence framing each.>

- [<Best Practices Article>](/s/article/...) — <description>.

## FAQ

<AccordionGroup>

<Accordion title="<Highest-leverage question — typically about who can use the product>?">
  <Answer in 1–3 sentences. Link to a deep article if there is one.>
</Accordion>

<Accordion title="<Second question — usually about scope or a common point of confusion>?">
  <Answer.>
</Accordion>

<Accordion title="<Third question — usually about a related product or how it interacts with another feature>?">
  <Answer.>
</Accordion>

<Accordion title="<Optional pointer to the broader FAQ article if one exists>?">
  See [<Product> FAQs](/s/article/...) for additional questions about <topic>.
</Accordion>

</AccordionGroup>
```

### Drafting rules

- **One concept per cluster heading.** Each `## Heading` introduces a single grouping (Build, Format, Manage, etc.). Do not mix tasks across clusters.
- **Every link gets a one-sentence description.** No bare link lists. The description should mirror the linked article's `excerpt` field, not duplicate its title.
- **Order clusters by reader journey.** Setup/access first, then build/create, then refine/format, then manage/govern, then best practices.
- **Three or four FAQ questions.** Pick the highest-leverage ones — who can use it, what scope is and isn't covered, how it relates to neighboring features, where to file issues.
- **No screenshots in an Overview by default.** Overviews are link-rich entry points; screenshots belong in the deep articles. The exception is one optional hero screenshot of the product UI immediately under the Intro if it materially helps orient a new reader.
- **Length target: 150–400 lines of MDX.** Anything shorter is probably a stub; anything longer is probably a how-to in disguise.

---

## Step 7.5: Align with the user on the draft (before fact-checking)

Before the fact-check pass, show the user exactly what you've written and confirm you're aligned on the copy — **every time**, no exceptions. The point is that you and the user agree on the literal words before you spend effort verifying and polishing them.

- Present the drafted Overview, flagging anything you **added** beyond what the user or the deep articles gave you, any place you **recast** source wording for style, and any spot where you're **missing** a definition, use case, or access path.
- If you need missing detail, ask for it now and fold in the answer — don't invent it.
- Only after the user confirms the copy do you run Step 8 (fact-check), Step 9 (edit), and Step 10 (link verification). Those passes preserve the agreed wording — they verify and style-correct; they don't re-paraphrase.

---

## Step 8: Fact-check pass

Before the edit pass, and before considering the Overview complete, verify every factual claim at least once against an authoritative source: what the user told you in Step 1, the style-guide treatment from Step 4, and the repo itself. This pass is about **accuracy**; link-target verification happens next in Step 10. When you correct an unsupported claim, prefer restoring the source's own wording over inventing a replacement. Overviews carry fewer procedural claims than how-tos, but the two they do carry are high-risk:

1. **Required Grants and any prerequisites.** Confirm every grant named in the Required Grants section actually exists and gates the described action. Cross-check the canonical grant wording (`grep -rn "Grant Name —" s/article/`) and the product's deep articles. If you can't establish the exact grants from the repo, **do not infer them — ask the user.**
2. **The access path.** Confirm the ways to open or reach the product in the **Access** section are real and current. Check the product's "Opening X" article if one exists, or ask the user.
3. **Conceptual claims and use cases.** Confirm the Intro's definition, sub-parts, and "what you can do" claims match how the product actually works — read the deep articles rather than trusting the draft.

**When you can't confirm a claim, or you find an inaccuracy or a discrepancy, STOP and ask the user directly** before finalizing. Do not guess or fill gaps with plausible-sounding content. The Overview is not complete until every factual claim is either confirmed against a source or explicitly confirmed by the user. **When in doubt, ask.**

---

## Step 9: Edit pass — style guide and template

Drafting always introduces style drift. After the fact-check pass, and before verifying links or finalizing, do an explicit editing pass against **both** `Domo-KB-Style-Guide.mdx` **and** `New-Article-Template.mdx`, and revise the article in place. This pass catches every usage, style, grammar, and structural mistake. As you fix style, keep the source's substantive wording intact — change only what a rule requires, exactly as at Step 7. **Do not skip this even if the draft looks right** — the most common misses (intro framing, imperative cluster headings, unpadded tables, lowercase Domo terms, future tense) are easy to introduce and easy to miss without a deliberate re-read.

1. **Re-read `Domo-KB-Style-Guide.mdx` and `New-Article-Template.mdx` now, in full** — not from memory. Step 5's "pay special attention to" list is a primer, not a substitute for the re-read.
2. **Proofread for plain grammar and usage** — spelling, agreement, punctuation, and clarity — alongside the Domo-specific rules below.
3. **Audit the Overview against this checklist** and fix every violation:
   - **Frontmatter** — `title` plus a single-sentence `excerpt`; never a `description` field.
   - **Intro** — opens with "This article explains…" / "This article covers…", states only what the Overview covers, and is followed by a `---` horizontal rule.
   - **Headings** — imperative mood at every level (link-cluster headings included — "Build Cards", not "Building Cards"; "Manage Access", not "Management"); structural labels (Intro, Required Grants, FAQ, Related Articles) are exempt. Top-level sections H2, subsections H3+.
   - **Required Grants** — exact format and canonical grant wording, with the em-dash inside the bold and a space on each side (`**Grant —** description`).
   - **Callouts** — `<Note>`/`<Warning>`/`<Tip>` with the label and its colon bolded (`**Note:**`), and a blank line before the callout (except inside table cells).
   - **Tables** — every pipe table padded so columns align. Run `python3 scripts/pad_md_tables.py <file>` to do this mechanically. Normalize any HTML tables (one tag per line, data rows in `<tbody>`).
   - **Links** — internal links use the file path with no `.mdx` extension and no full URL; every link still carries its one-sentence description.
   - **Em-dashes** — no spaces in prose; spaces only in the bolded-term list exception.
   - **Voice and word choice** — present tense, not "will"; active voice; "after", not causal "once"; no "utilize"; spell out numbers under 10; "allowlist"/"blocklist"; "select", not "click"; Oxford comma; no exclamation points.
   - **Domo terms** — apply the Step 4 treatment for the product name consistently, plus `DataSet`, `DataFlow`, `DataFusion`, `Beast Mode`, `Workbench`; `dashboard` lowercase except at the start of a sentence or with a type; never "Page". Verify against the **Domo-Specific Terms and Usage** table.
   - **Beta** — correct convention applied (frontmatter `tag` + verbatim Note for a whole-article beta; Badge + single verbatim Note for section-level).
   - **Images** — if you included the optional hero screenshot, it is wrapped in `<Frame>` with a native `<img>` and descriptive `alt`, no inline `width`/`height`; never `<Frame>` inside a table cell. No placeholders unless the user opted in at Step 6.
   - **Icons** — current UI glyphs use the `icon-{name}` font; `legacy-icon-{name}` only for release-notes/Workbench surfaces; brand logos use Font Awesome brands or inline `<svg fill="currentColor">`; never the old inline-image icon pattern for a glyph that exists in the font. Each icon carries `aria-hidden="true"` and is named in the prose.
4. **Revise the Overview in place** to resolve every issue found, then re-run the table normalizer if you changed any tables.

---

## Step 10: Verify every internal link

Each `/s/article/<slug>` link must resolve to an article whose title matches what the link text claims. This is the second-biggest failure mode for Overview drafts, and it completes the fact-check begun in Step 8.

For each link, confirm the target exists and the title matches:

```bash
for slug in <slug1> <slug2> <slug3>; do
  if [ -f "s/article/${slug}.mdx" ]; then
    echo "$slug: $(grep -m1 '^title:' s/article/${slug}.mdx)"
  else
    echo "$slug: MISSING"
  fi
done
```

Common silent failures:

- A numeric slug like `000005307` that you assumed was "Beast Mode Overview" actually resolves to "Nested Calculations".
- A slug like `360042925254` that sounded like "Card History" is actually "Setting Options for Gauges".
- A slug that doesn't exist at all because the article was deleted in migration.

Fix every mismatch before finalizing. If a referenced article truly does not exist, either:

- Drop the link and rewrite the surrounding text to not promise it.
- Or note it as a follow-up gap and flag for the user.

---

## Step 11: Handle the legacy collision (if Step 2 selected "New file + rename legacy")

If Step 2 chose to rename the legacy article (option 2), do it now:

1. **Update the legacy article's `title:` and `excerpt:`** in `s/article/<legacy-id>.mdx` to reflect its actual content. Common new titles: `"Save a Visualization Card in Analyzer"`, `"Configure X"`, `"<Old Title> Walkthrough"`. The file path stays the same — only the frontmatter changes, so no redirect or inbound-link updates are needed.

2. **Mirror the rename on the JA sibling** at `ja/s/article/<legacy-id>.mdx`. The JA title should be a translation of the new EN title in the same imperative style as adjacent JA articles. Example:

   ```
   title: "Analyzerで可視化カードを保存する"  // (EN: "Save a Visualization Card in Analyzer")
   ```

   Match the existing JA voice — if neighbor articles use polite/imperative forms with `する`, follow that pattern. Match the existing excerpt style too.

3. **Skip the JA sibling for the new Overview article itself.** Translation work happens separately on the JA pipeline. Note in your final summary that the JA Overview is deferred.

---

## Step 12: Add the new article to navigation

Invoke the `add-to-nav` skill with:

- **Page path:** `s/article/<Product>-Overview`
- **Operation:** Insert
- **Target:** the existing group or subgroup that contains the deep articles for this product. The new Overview should be the **first** page in that group so it functions as the section's landing page.

If the product is currently buried 3+ levels deep in nav (a common state — DomoStats was at Admin > Administrate Domo > Governance > DomoStats), pause and surface the placement question to the user via AskUserQuestion before adding. Three reasonable options:

1. **Top-level group under the relevant tab** — high visibility, peer of other major sections.
2. **Promote one level out of the current burial** — moderate visibility, keeps the contextual parent.
3. **Leave nested and just add the Overview at the top of the existing group** — minimal disruption.

If a nav restructure is requested, mirror the structural change on the JA side of `docs.json` (without adding a JA Overview entry, since JA translation is deferred).

After every `docs.json` edit, validate:

```bash
node -e "JSON.parse(require('fs').readFileSync('docs.json', 'utf8')); console.log('docs.json is valid JSON');"
```

---

## Step 13: Output

Tell the user:

1. **File created:** `s/article/<Product>-Overview.mdx`.
2. **Legacy collision handling:** what was done with any collision (replaced, renamed, or sidestepped).
3. **JA work deferred:** the JA Overview translation has not been written; the JA sibling of any renamed legacy article was updated for parity.
4. **Nav placement:** where the new article was added in `docs.json` (and any restructure performed).
5. **Verification:** every factual claim was confirmed against a source or with the user (Step 8), all internal links resolved to the correct target articles (Step 10), and `docs.json` is valid JSON.
6. **Open items:** any fact-check items you flagged in Step 8 that still need the user's confirmation.
7. **Local preview:** suggest `mintlify dev` to confirm the rendered Overview reads the way the user expects.

---

## Step 14: Offer localization

After delivering the output above, ask the user:

> "Would you like to localize this article into Spanish, French, and German? (Note: Japanese localization is handled on a separate pipeline — no action needed there.)"

- **If yes:** invoke the `localize` skill, passing the new article's file path as the argument.
- **If no:** the skill ends here.

---

## Reference: Good prior examples

When in doubt about voice, length, or cluster organization, read one of these as a model:

- `s/article/Analyzer-Overview.mdx` — link-cluster heavy; product with many small how-to children.
- `s/article/DomoStats-Overview.mdx` — two-halves product (connector + apps); shows the description-list pattern in the Intro.
- `s/article/4412849158167.mdx` — `Cloud Integrations Overview`; "Why X?" framing instead of "What You Can Do".
- `s/article/7903767835031.mdx` — `Variables | Overview`; shorter, more conceptual.
- `s/article/000005295.mdx` — `App Studio | Overview`; very long edge of the range, useful for products with many integrated sub-features.

Do not blindly copy these — they pre-date this skill and contain legacy patterns (HTML tables, image-based icons). Use them for shape, not for line-by-line conventions.
