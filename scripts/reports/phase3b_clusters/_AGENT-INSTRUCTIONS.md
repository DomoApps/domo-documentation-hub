# Phase 3b general — Forum-Gap Update: Shared Agent Instructions

You are updating existing **Domo Knowledge Base** articles (Mintlify MDX) to fill
documented content gaps that Domo community-forum users hit. This is Phase 3b of a KB
restructure. Your changes are **additions to existing articles**, not rewrites.

## Your inputs

1. **Your cluster task file** (path given in your prompt): lists the exact files you own
   and, under each, the specific gaps to fill (rank, what's missing, suggested location).
2. The gap detail is your spec for *what content to add and where*.

## Hard rules

- **Edit ONLY the files listed under `##` headings in your cluster file.** Never create
  new files (use Edit, never Write). Never edit any file not in your cluster — other
  agents own other files and simultaneous edits would collide. "Other referenced
  articles" lines are **read-only context**, not edit targets.
- **Do NOT edit `docs.json`.** No navigation changes in this phase.
- **Do NOT commit or push.** The main session handles git.
- **Do NOT add `## Next Steps` or `## Related Articles` link sections** — interlinking is
  Phase 5 (article slugs aren't stable yet). You may still add a single inline
  cross-reference link inside prose where it's genuinely helpful.
- **English only.** No localization.

## How to fill each gap

1. **Read the whole target article first.** Understand its existing structure, voice, and
   what it already covers. If a gap is already covered, note it and skip — don't duplicate.
2. **Add the missing content where the suggested location indicates**, integrated
   naturally into the existing structure:
   - A new concept/limitation → a short new `##`/`###` section, or a `<Note>`/`<Warning>`.
   - A Q&A-style gap → a new `<Accordion title="…">` inside the article's existing
     `<AccordionGroup>` FAQ (create one at the bottom only if none exists).
   - A worked example / recipe → a fenced code block or a small worked-example subsection.
   - A one-line fact (e.g. "Beast Mode uses a MySQL-like dialect") → a sentence in the
     most-findable existing spot.
3. **Match the surrounding article** in heading depth, tone, and formatting.

## Synthesizability rule (critical)

- If the gap can be **fully and accurately written** from the target article + closely
  related KB articles + the gap detail, **write it completely**. Prefer real content.
- If a gap needs **undocumented mechanics or PM-only facts you cannot verify** from
  existing KB content, **do not invent them.** Write whatever surrounding context is
  safely synthesizable, then drop a marker at the exact spot for the missing specifics:

  ```
  {/* [pm-input] <PM Name> — <the specific thing that needs confirmation>. Synthesized from community forum reports; needs confirmation. */}
  ```

  Use the PM name from your cluster file's **Owning PM**. The em-dash after the name is
  required (a script parses it). Never leave `TODO`, `FIXME`, or `[FACT-CHECK]` text in an
  article — only the `[pm-input]` comment form above.

## Quality gates — apply all three to every edit, in order

**Gate 1 — Fact-check.** Verify every claim against the actual article and related KB
content. Do not invent grant names, row/size limits, function names, or UI labels. If you
reference a grant, confirm its canonical wording (`grep -rn "Grant Name" s/article/`). Any
claim you can't verify becomes a `[pm-input]` marker, not a stated fact.

**Gate 2 — Screenshots.** If your addition describes a UI action and an applicable
screenshot already exists in the target article or a closely related source article,
include it wrapped in `<Frame>` with its original alt text. Do **not** fabricate image
paths and do **not** leave screenshot TODO markers — include a real one or none.

**Gate 3 — Style.** Imperative mood for task/action headings (no gerunds); Title Case
(Chicago: prepositions lowercase). Bold every callout label (`**Note:**`, `**Warning:**`,
`**Tip:**`). Internal links are root-relative with no extension: `/s/article/slug`. FAQ
uses `<AccordionGroup>` + `<Accordion title="…">` at the bottom. Block screenshots in
`<Frame>`.

## After editing

- If you added or changed a Markdown pipe table in a file, run:
  `python3 scripts/pad_md_tables.py <file>` on that file.

## Return this report (it feeds the restructure manifest)

For each file you edited, report concisely:
- **File** and the **gap ranks addressed** (and one phrase on what you added for each).
- **`[pm-input]` markers inserted**: PM name + the specific need, per marker.
- **Gaps skipped** (already covered / not synthesizable / target mismatch) + why.
Keep it tight — no need to paste diffs.
