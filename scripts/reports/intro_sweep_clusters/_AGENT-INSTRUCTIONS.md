# Intro Sweep — Agent Instructions (Phase 3b general, structural)

You are normalizing the **Intro section** of a small set of existing Domo KB articles to match the house style. Your cluster file lists the articles (path, Title, Excerpt, Bucket, Owning PM). Work only on the files in your assigned cluster. These are edits to EXISTING files.

## For each article

1. **Read the file.**

2. **Skip conditions** — do NOT edit; report as `SKIPPED (reason)`:
   - It is a **connector / integration reference page** for a specific third-party data source (e.g., HipChat, Sage 300, a named SaaS). (An *Overview* or *implementation guide* is NOT a connector reference page — those you DO process.)
   - It is clearly **legacy / retirement-bound** (defunct product, "contact LegacyTools@domo.com", a discontinued tool).

3. **Add or normalize the Intro** (the main task):
   - Insert `## Intro` as the first body element, after any `import` lines (imports stay at the very top).
   - Write **one succinct sentence** in the form **"This article explains how to X, Y, and Z."** (use **"This article covers…"** for overview/reference articles). Derive it from the provided Excerpt + the article's actual content. Name 2–3 concrete actions/skills using the SAME terminology as the body. Do NOT explain why it matters.
   - **has_para bucket:** the article already opens with a lead paragraph. Reword that lead into the standard intro sentence. Preserve a genuinely-necessary context sentence if one exists. Move any substantive non-intro content (steps, notes, frames, "To do X," lead-ins) to BELOW the horizontal rule.
   - **opens_heading bucket:** the article jumps straight into a heading. Compose the intro from the Excerpt and place it above that first heading.
   - **opens_component bucket:** the article opens with a `<Note>`/callout. Put `## Intro` + the sentence first, then the callout/body follows after the rule.
   - Add a horizontal rule `---` on its own line immediately after the Intro section, separating it from the body. (If a `---` already exists right after where you put the intro, don't duplicate it.)

4. **Grant-gap flag (conditional):** If the article documents a feature that is plainly gated by a permission grant (admin, governance, configuration, or management features) AND has **no** `## Required Grants` section, add exactly one marker as the first line after the intro's `---`:
   ```
   {/* [pm-input] <Owning PM> — confirm the Required Grants for <feature>; no Required Grants section exists. */}
   ```
   Use the Owning PM from the cluster file. Do NOT add this to ordinary how-tos that don't gate on a grant. Do NOT invent grant names.

## Do NOT
- Add screenshots, Related Articles, or Next Steps (that's Phase 5).
- Add a Required Grants section yourself, or invent grants.
- Change other headings, reorder body content, or edit frontmatter.
- Leave any TODO/FIXME/placeholder. Keep all MDX/JSX tags balanced and all existing images/links/components intact.

## Report back (one line per file)
`<file>: DONE (intro normalized)` | `DONE + grant-flag (<PM>)` | `SKIPPED (<reason>)`
