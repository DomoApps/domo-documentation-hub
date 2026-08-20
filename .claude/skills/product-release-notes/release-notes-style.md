# Release Notes House Style

Authoritative style standard for Domo's public-facing product **feature-release** Release Notes — the `s/article/Current-Release-Notes.mdx` file and its archived siblings (`s/article/{Month}-{Year}-Release.mdx`). Derived from the two best current examples: **May 2026** (`Current-Release-Notes.mdx`) and **March 2026** (`March-2026-Release.mdx`). Every release note must read as if the same author wrote it, so follow this exactly.

> This is the writing standard only. The end-to-end process (branch, archive, ingest context, Jira/PRD, draft, fact-check, commit) lives in `SKILL.md`.

---

## 1. File skeleton

Every file — current or archived — has this exact shape:

```mdx
---
title: "September 2026 Release Notes"
excerpt: "September 2026 release notes covering <3–5 headline features>, and additional new features and enhancements."
---

import { BetaNote } from '/snippets/BetaNote.mdx';

---

## New Features and Enhancements

### <Feature A>

<body>

<Frame>![](/images/kb/<name>.png)</Frame>

Learn more about [<link text>](https://www.domo.com/docs/s/article/<slug-or-id>).

### <Feature B>
...

## Beta Features

<BetaNote generic />

### <Beta feature A>
...

## Support

Domo provides education, community answers, and technical support.

- Search for a topic in the [Help Center](https://www.domo.com/domo-central/help).  
- Learn from [Domo University](https://www.domo.com/domo-central/university). 
- Search for training apps in the [Appstore](https://www.domo.com/appstore/) .
- Get answers in the [Community Forums](https://community-forums.domo.com/main).
- Contact Technical Support by entering a help ticket in the [Domo Support Portal](https://www.domo.com/login/customer-community).
- Reach out to your Domo account team.
```

Invariants:

- Only three top-level (`##`) sections, in this order: **New Features and Enhancements**, **Beta Features**, **Support**. If a release has no beta programs, omit the Beta Features section entirely (do not leave an empty heading).
- The `import { BetaNote } ...` line and the standalone `---` divider directly under it are always present, even when there are no betas (they cost nothing and keep files uniform).
- The **Support** block is fixed boilerplate — copy it verbatim, including the trailing spaces shown above. Never reword it.

---

## 2. Frontmatter

- **`title`** — Current file: `"{Month} {Year} Release Notes"` (e.g. `"September 2026 Release Notes"`). Archived file: `"{Year} Release {N} | {Month}"` (see `SKILL.md` › archival). Nothing else.
- **`excerpt`** — one sentence, invisible on the page, used for search/AI context. Pattern: `"{Month} {Year} release notes covering {2–5 headline features}, and additional new features and enhancements."` Never use `description` in place of `excerpt`.
- No other frontmatter fields.

---

## 3. Section ordering

- Within **New Features and Enhancements** and within **Beta Features**, order the `###` feature sections **alphabetically by heading text**. (Both examples do this — e.g. March runs App Studio → Column PDP → Cloud Integrations → Deprecated Models → Domo AI … → Worksheets.)
- Sub-features under a parent are ordered alphabetically among themselves.
- "Enhancements to X" headings sort under **E** as written — don't re-alphabetize by the noun.

---

## 4. Anatomy of one feature entry

```mdx
### <Feature Name>

<Lead paragraph: what it is + the value, in the customer's terms. 1–2 sentences.>

<Optional second paragraph: how it works or a secondary benefit.>

- <Optional bulleted list of capabilities, benefits, or options>
- <Keep each bullet a short phrase or single sentence>

<Frame>![](/images/kb/<descriptive_name>.png)</Frame>

Learn more about [<natural link text>](https://www.domo.com/docs/s/article/<slug-or-id>).
```

Rules:

- **Headings** — Title Case; the product/feature name as customers see it. No internal codenames, squad names, or Jira keys. Use imperative/noun phrasing, never a gerund-led sentence.
- **Body length** — 1–3 short paragraphs. Lead with what the customer can now do and why it helps; keep the mechanism brief. This is an announcement, not a how-to.
- **Bulleted lists** — use for a set of new options, capabilities, or benefits (see Flex Table, Workflows Annotations examples). Parallel phrasing; no terminal punctuation on fragment bullets unless full sentences.
- **`<Frame>`** — wrap every screenshot in `<Frame>![](/images/kb/<name>.png)</Frame>` on its own line, placed after the prose/bullets. A feature may have two stacked Frames when it needs two shots (see Connector Execution Details: `_failed` + `_pass`). Omit the Frame only when there is genuinely no usable screenshot — never insert a placeholder, TODO, or broken path.
- **"Learn more" line** — include only when a **real, published** KB article covers the feature. Format: `Learn more about [descriptive text](URL).` — a single sentence, no bold, ending in a period. If no article exists yet, omit the line entirely (do not invent a slug or link to a generic page just to have a link).

### Sub-features (parent + children)

When several related items ship under one product area, group them:

```mdx
### Workflows Updates

#### Queue Notification Controls

<body + Frame + optional Learn more>

#### Workflow Event Triggering - Access Request

<body + Frame>
```

Common parents: **Magic ETL Enhancements**, **Workflows Updates / Workflows Enhancements**. Each `####` child is a full entry (body, Frame, optional link). The parent `###` usually carries no body of its own.

---

## 5. Links

- **Release-notes links are absolute:** `https://www.domo.com/docs/s/article/<slug-or-id>`. This is the current convention (the May file uses it throughout) and matches the PMM release-article prefix. Prefer it over the older root-relative `/s/article/...` form seen in some March entries.
- You may deep-link to an anchor: `.../s/article/000005172#admin-notification-setting`.
- Link text is natural prose ("Learn more about **Domo Documents**"), not a bare URL.
- Before adding any link, confirm the target article actually exists in `s/article/` (search by title/slug). No link is better than a wrong or generic link.

---

## 6. Beta Features section

- Opens with exactly `<BetaNote generic />` (renders the standardized beta-program callout without the "This feature is in beta." sentence). Do not hand-write the beta callout.
- Then `###`/`####` entries in the same anatomy as above.
- A feature belongs here when the source CSV / internal notes flag it as a **Beta program**, not a GA feature. When unsure which bucket an item belongs in, ask rather than guess.

---

## 7. Voice and tone

- **Second person, present tense, active voice.** "You can now…", "The new X lets you…".
- **Benefit-first.** Open with the customer outcome; keep implementation detail short and only where it clarifies.
- **Plainspoken and concrete.** Short sentences. No marketing superlatives stacked up, no hedging.
- **Consistent product naming.** Match how the product surfaces the name in-product and in existing KB articles.
- **No internal artifacts.** Never expose Jira keys, epic titles, PRD jargon, squad/PM names, branch-cut dates, or "feature switch" mechanics.
- **Dates:** state real, source-confirmed dates only (e.g. a model deprecation date from the internal notes). Never compute or infer a date.

---

## 8. Recurring non-feature sections

Some entries are standard announcements rather than a single feature — include them when present in the internal notes even if they have no epic:

- **Model Deprecation Notice / Deprecated Models** — bullet the models entering deprecation, state the availability-until date (verbatim from the source), then bullet the recommended replacements. See both examples for exact shape.
- **Domo AI Models Updates** — new model versions and their key improvements as bullets.

Place these alphabetically among the `###` entries like any other feature.

---

## 9. Screenshots — naming and placement

- Save to `images/kb/`. Name descriptively in lowercase; the recent Release Notes convention is **snake_case** (`queue_notification_controls.png`, `report_builder_pdf.png`); kebab-case (`app-studio-editor.png`) also appears in older files — prefer snake_case for new work and stay consistent within a release.
- One image → one feature; name it after the feature/sub-feature.
- Use the source file's real extension (`.png` or `.jpg`).
- Check for an existing file of the same name before writing; if it collides with an unrelated image, add a short qualifier (`_v2`, or a feature prefix).
- The image must be committed to `images/kb/` on the same branch before the article references it.

---

## 10. Quick checklist before handoff

- [ ] Title + excerpt match the conventions in §2.
- [ ] `import { BetaNote }` + `---` divider present.
- [ ] Sections alphabetized; sub-features grouped correctly.
- [ ] Every feature has a body; screenshots wrapped in `<Frame>`; every referenced image exists in `images/kb/`.
- [ ] No placeholders, TODOs, broken links, or invented "Learn more" links.
- [ ] Beta section (if any) opens with `<BetaNote generic />`.
- [ ] Support block is the verbatim boilerplate.
- [ ] Every factual claim traces to the internal notes, epic, or PRD (see fact-check step in `SKILL.md`).
