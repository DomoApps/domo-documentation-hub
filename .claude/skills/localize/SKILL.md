---
name: localize
user-invocable: true
description: "localize an article, translate an article into Spanish French German, localize release notes, translate release notes, translate KB article"
argument-hint: "article filename or path (e.g., s/article/March-2026-Release.mdx)"
---

Localize a Domo KB article into Spanish, French, and German.

The user has provided: $ARGUMENTS

---

## CRITICAL: Read the Localization Style Guide First

**Before doing anything else — before identifying the article, before asking any questions, before writing a single translated word — read `Localization-Style-Guide.mdx` in full from the root of the repository.**

```bash
# Confirm the file exists and read it
cat Localization-Style-Guide.mdx
```

The style guide is the authoritative reference for every translation decision in this skill. Do not rely on memory or general translation knowledge. Every term, header, and convention must follow what is documented there.

---

## Step 1: Identify the article

If `$ARGUMENTS` specifies an article path or title, confirm the exact file path before proceeding. If it's ambiguous, search:

```bash
grep -rl "title:.*keyword" s/article/ s/topic/
```

Read the identified English article in full before proceeding. You need to understand its content, structure, and any special components before translating.

Also confirm: does this article already have localized versions in any of the three language directories?

```bash
ls es/s/article/$(basename "$ARTICLE_PATH") fr/s/article/$(basename "$ARTICLE_PATH") de/s/article/$(basename "$ARTICLE_PATH") 2>/dev/null
```

If localized versions already exist for any language, flag this to the user and ask whether to overwrite them.

---

## Step 2: Determine the article type

Ask the user two questions (combine into one message):

1. **Is this a Release Notes article?** (yes/no)
2. **Which languages?** Localization defaults to all three — Spanish, French, and German — unless the user explicitly requests only specific language(s). Note to the user: Japanese localization is handled on a separate pipeline and is not part of this skill.

If the article is Release Notes, also ask:

3. **Is this the Current Release Notes** (`s/article/Current-Release-Notes.mdx`) **or a past (archived) release notes article?**

---

## Step 3a: Current Release Notes flow

Follow this flow **only** when the user confirms the article is `s/article/Current-Release-Notes.mdx`.

This flow has two phases per language: (1) archive the existing localized content, then (2) replace it with a fresh translation of the English Current Release Notes.

### Phase 1: Archive the existing localized Current Release Notes

For each target language, perform the following:

**1. Read the existing localized Current Release Notes:**

```bash
cat {es,fr,de}/s/article/Current-Release-Notes.mdx
```

**2. Determine the archive filename.**

Look at the frontmatter `title` and content of the localized Current Release Notes to identify which release it contains. Compare against the English archived release notes to find the corresponding English archive file. Use the same filename as the English equivalent:

```bash
# Find the corresponding English archive by title/content match
grep -rl "title:.*keyword" s/article/
```

Naming conventions for archive files (follow whichever pattern the English archive uses for this release):
- Named pattern (newer): `March-2026-Release.mdx`, `November-2025-Release.mdx`
- Numeric pattern (older): `000006035.mdx`, `000005924.mdx`

If you cannot confidently determine the correct archive filename, ask the user: "The current [language] localized release notes appear to contain [description of content]. What filename should I use for the archive? (For reference, the English archive for this release is `s/article/[filename]`.)"

**3. Check whether the archive file already exists:**

```bash
ls {es,fr,de}/s/article/ARCHIVE-FILENAME.mdx 2>/dev/null
```

If the archive file already exists for a given language, do **not** overwrite it. Skip the archiving step for that language and note this to the user.

**4. Write the archive file:**

Create `{lang}/s/article/ARCHIVE-FILENAME.mdx` with the exact content from `{lang}/s/article/Current-Release-Notes.mdx`. Do not modify the content — this is a straight copy to preserve history.

**5. Add the archived file to docs.json navigation:**

Invoke the `add-to-nav` skill for each language with:
- **Page path:** `{lang}/s/article/ARCHIVE-FILENAME` (no `.mdx`)
- **Operation:** Insert
- **Target:** The language's Release Notes tab, under the appropriate year group in "Archived Feature Release Notes" (or its translated equivalent). Mirror the placement of the corresponding English archived release note.

The localized Release Notes tab names are:
- Spanish: "Notas de la versión" tab → "Notas de la versión de funciones archivadas" group
- French: "Notes de version" tab → "Notes de version des fonctionnalités archivées" group
- German: "Versionshinweise" tab → "Archivierte Versionshinweise zu Funktionen" group

### Phase 2: Translate the English Current Release Notes into each language

**1. Read the English Current Release Notes in full:**

```bash
cat s/article/Current-Release-Notes.mdx
```

**2. Translate into each target language** following all rules in `Localization-Style-Guide.mdx`.

Key reminders for Current Release Notes translation:
- Translate the `title:` and `excerpt:` frontmatter fields
- Title for the localized Current Release Notes files should be the language's equivalent of "Current Release Notes" (see style guide Release Notes Conventions)
- Translate "## New Features and Enhancements" to the language-specific header (see style guide)
- Preserve all `<Frame>`, `<BetaNote />`, `import` statements, and MDX components unchanged
- For images: check whether localized image versions exist in `/images/kb/{lang}/`; if not, use the English image path
- Apply all language-specific term translations from the style guide glossary

**3. Write the translated content to the pre-existing localized Current Release Notes files** — replacing the content that was just archived:

```
es/s/article/Current-Release-Notes.mdx   ← overwrite with Spanish translation
fr/s/article/Current-Release-Notes.mdx   ← overwrite with French translation
de/s/article/Current-Release-Notes.mdx   ← overwrite with German translation
```

These files already exist; use the Edit or Write tool to replace their content entirely.

Do **not** add these to `docs.json` navigation — they are already registered under `{lang}/s/article/Current-Release-Notes`.

**4. Validate docs.json:**

```bash
python3 -c "import json; json.load(open('docs.json')); print('docs.json is valid JSON')"
```

---

## Step 3b: Past Release Notes or Non-Release-Notes flow

Follow this flow for:
- Any archived (past) release notes article
- Any non-release-notes KB article

### 1. Read the English source article in full

```bash
cat s/article/FILENAME.mdx
```

### 2. Translate into each target language

Following all rules in `Localization-Style-Guide.mdx`:

- Translate the `title:` and `excerpt:` frontmatter fields
- Translate all prose, headings, list items, and callout body text
- Apply language-specific term translations from the style guide glossary
- For images: check whether localized images exist; fall back to English paths if not
- Internal links: always keep as English paths (`/s/article/...`) — do not prefix with a language code
- Preserve all MDX components, code blocks, import statements, and formatting exactly — **with one exception: BetaNote** (see below)
- **BetaNote:** When the English source uses `import { BetaNote } from '/snippets/BetaNote.mdx';` and `<BetaNote />` or `<BetaNote generic />`, replace with the language-specific export from the same snippet file. The import path stays identical; only the named export and component name change:
  - Spanish: `import { BetaNoteEs } from '/snippets/BetaNote.mdx';` → `<BetaNoteEs />` / `<BetaNoteEs generic />`
  - French: `import { BetaNoteFr } from '/snippets/BetaNote.mdx';` → `<BetaNoteFr />` / `<BetaNoteFr generic />`
  - German: `import { BetaNoteDe } from '/snippets/BetaNote.mdx';` → `<BetaNoteDe />` / `<BetaNoteDe generic />`
  - Japanese: `import { BetaNoteJa } from '/snippets/BetaNote.mdx';` → `<BetaNoteJa />` / `<BetaNoteJa generic />`
- If the English source contains legacy raw beta text (an italic paragraph mentioning `beta.admin@domo.com` rather than the snippet), replace it with the appropriate `<LangBetaNote generic />` component and add the import line. Never carry forward raw italic beta text into a localized article.

### 3. Write the translated files

Write each localized version to the corresponding language directory using the **same filename as the English source**:

```
es/s/article/FILENAME.mdx
fr/s/article/FILENAME.mdx
de/s/article/FILENAME.mdx
```

(Write only the files for the requested target languages.)

### 4. Add each localized file to docs.json navigation

For each language, invoke the `add-to-nav` skill:

**Find the English article's nav placement first:**

```bash
grep -n "\"s/article/FILENAME\"" docs.json
```

Read ±30 lines around the match to understand the tab, group, subgroup, and position.

Then insert the localized version at the equivalent position in the target language's navigation section of `docs.json`, mirroring the English placement as closely as possible. The localized nav sections follow the same structural hierarchy as English but use translated group names.

For release notes articles specifically, use the localized tab and group names from the style guide (see the Release Notes Conventions section).

**Page path to insert:** `{lang}/s/article/FILENAME` (no `.mdx`)

Invoke `add-to-nav` once per language (three invocations total, or fewer if only specific languages were requested).

### 5. Validate docs.json

```bash
python3 -c "import json; json.load(open('docs.json')); print('docs.json is valid JSON')"
```

---

## Step 4: Output

Tell the user:

1. **Files created or updated** — list each new or modified file path
2. **Navigation entries added** — list each `docs.json` insertion (language, tab, group, position)
3. **Archived files** (Current Release Notes flow only) — what was archived, where, and any languages where the archive was skipped because it already existed
4. **docs.json validation** — confirm it passed or report the error
