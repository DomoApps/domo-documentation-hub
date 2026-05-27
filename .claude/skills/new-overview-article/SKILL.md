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

Save the resulting list — you'll group it in Step 6.

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

## Step 6: Draft the article

Create `s/article/<Product>-Overview.mdx` (title-case filename, hyphen-separated, no `.mdx` collisions). The structure below is the canonical Overview shape — it is what the existing modern overviews (`Cloud Integrations Overview`, `App Studio | Overview`, `Variables | Overview`, plus the recently authored `Analyzer Overview` and `DomoStats Overview`) all converge on, and it differs from a generic how-to.

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

## Step 7: Verify every internal link

Each `/s/article/<slug>` link must resolve to an article whose title matches what the link text claims. This is the second-biggest failure mode for Overview drafts.

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

## Step 8: Handle the legacy collision (if Step 2 selected "New file + rename legacy")

If Step 2 chose to rename the legacy article (option 2), do it now:

1. **Update the legacy article's `title:` and `excerpt:`** in `s/article/<legacy-id>.mdx` to reflect its actual content. Common new titles: `"Save a Visualization Card in Analyzer"`, `"Configure X"`, `"<Old Title> Walkthrough"`. The file path stays the same — only the frontmatter changes, so no redirect or inbound-link updates are needed.

2. **Mirror the rename on the JA sibling** at `ja/s/article/<legacy-id>.mdx`. The JA title should be a translation of the new EN title in the same imperative style as adjacent JA articles. Example:

   ```
   title: "Analyzerで可視化カードを保存する"  // (EN: "Save a Visualization Card in Analyzer")
   ```

   Match the existing JA voice — if neighbor articles use polite/imperative forms with `する`, follow that pattern. Match the existing excerpt style too.

3. **Skip the JA sibling for the new Overview article itself.** Translation work happens separately on the JA pipeline. Note in your final summary that the JA Overview is deferred.

---

## Step 9: Add the new article to navigation

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

## Step 10: Output

Tell the user:

1. **File created:** `s/article/<Product>-Overview.mdx`.
2. **Legacy collision handling:** what was done with any collision (replaced, renamed, or sidestepped).
3. **JA work deferred:** the JA Overview translation has not been written; the JA sibling of any renamed legacy article was updated for parity.
4. **Nav placement:** where the new article was added in `docs.json` (and any restructure performed).
5. **Verification:** all internal links resolved to the correct target articles, and `docs.json` is valid JSON.
6. **Local preview:** suggest `mintlify dev` to confirm the rendered Overview reads the way the user expects.

---

## Reference: Good prior examples

When in doubt about voice, length, or cluster organization, read one of these as a model:

- `s/article/Analyzer-Overview.mdx` — link-cluster heavy; product with many small how-to children.
- `s/article/DomoStats-Overview.mdx` — two-halves product (connector + apps); shows the description-list pattern in the Intro.
- `s/article/4412849158167.mdx` — `Cloud Integrations Overview`; "Why X?" framing instead of "What You Can Do".
- `s/article/7903767835031.mdx` — `Variables | Overview`; shorter, more conceptual.
- `s/article/000005295.mdx` — `App Studio | Overview`; very long edge of the range, useful for products with many integrated sub-features.

Do not blindly copy these — they pre-date this skill and contain legacy patterns (HTML tables, image-based icons). Use them for shape, not for line-by-line conventions.
