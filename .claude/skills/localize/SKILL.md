---
name: localize
user-invocable: true
description: "localize an article, translate an article into Spanish French German, localize release notes, translate release notes, translate KB article"
argument-hint: "article filename or path (e.g., s/article/March-2026-Release.mdx) — or 'lqa-update ja/s/article/FILENAME.mdx' to run the LQA capture pass on an already-committed Japanese article"
---

Localize a Domo KB article into Spanish, French, and German.

The user has provided: $ARGUMENTS

---

## CRITICAL: Read the Localization Style Guide First

**Before doing anything else — before identifying the article, before asking any questions, before writing a single translated word — read `Localization-Style-Guide.mdx` in full from the root of the repository.**

```bash
# Confirm the file exists and read it
cat localization/Localization-Style-Guide.mdx
```

The style guide is the authoritative reference for every translation decision in this skill. Do not rely on memory or general translation knowledge. Every term, header, and convention must follow what is documented there.

**If Japanese is one of the target languages (or if `$ARGUMENTS` specifies `ja` only), also read the Japanese TM Reference immediately after the style guide — before any translation work begins:**

```bash
cat localization/Japanese-Localization-Reference.mdx
```

`localization/Japanese-Localization-Reference.mdx` contains the XTM Translation Memory–derived term glossary, structural phrase patterns, UI element naming conventions, and the running LQA log. For Japanese translations, this file supersedes the style guide wherever the two conflict.

---

## LQA Capture Mode

**If `$ARGUMENTS` starts with `lqa-update`**, skip Steps 1–6 and run the LQA Capture Pass instead.

### LQA Capture Pass

This mode is run after a human reviewer has edited and committed a Japanese article to the branch. It reads the approved version, compares it against the English source and the existing TM reference, and registers any new nuances.

**1. Parse the target path:**

```
$ARGUMENTS = "lqa-update ja/s/article/FILENAME.mdx"
                          ↑ this is the localized file to inspect
```

**2. Read the approved Japanese article and its English source:**

```bash
cat ja/s/article/FILENAME.mdx
cat s/article/FILENAME.mdx
```

**3. Compare and identify LQA-worthy findings.**

A finding is LQA-worthy if it represents:
- A term choice that differs from the TM glossary in `localization/Japanese-Localization-Reference.mdx`
- A structural or phrasing pattern not yet documented in the reference
- A Domo-specific UI element name, field label, or product term being translated in a way not captured elsewhere
- Any translation decision that a future translator would need to know to be consistent

Ignore findings that are already covered by the style guide or reference file.

**4. For each finding, draft an LQA entry in this format:**

```
### [YYYY-MM-DD] [article filename]
- **Finding**: [description]
- **English source**: "[original text]"
- **Initial/prior translation**: "[what was written before the reviewer's edit, if known; otherwise omit]"
- **Approved translation**: "[what the human reviewer approved]"
- **Rule update**: [state a new rule if this should generalize; otherwise "none — one-off context-specific choice"]
```

**5. Append entries to `localization/Japanese-Localization-Reference.mdx`:**

Use the Edit tool to append each finding under the `## LQA Log` section at the bottom of `localization/Japanese-Localization-Reference.mdx`. Do not overwrite existing entries.

If a finding implies a rule that should be added to the term glossary table (not just the log), also update that table in the same file.

**6. Report to the user:**

- Number of findings registered
- Brief summary of each finding
- Whether any glossary entries were updated

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
2. **Which languages?** Localization defaults to all four — Spanish, French, German, and Japanese — unless the user explicitly requests only specific language(s).

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
- Japanese: "リリースノート" tab → "機能に関する過去のリリースノート" group

### Phase 2: Translate the English Current Release Notes into each language

**1. Read the English Current Release Notes in full:**

```bash
cat s/article/Current-Release-Notes.mdx
```

**2. Translate into each target language** following all rules in `Localization-Style-Guide.mdx` and (for Japanese) `localization/Japanese-Localization-Reference.mdx`.

Key reminders for Current Release Notes translation:
- Translate the `title:` and `excerpt:` frontmatter fields
- Title for the localized Current Release Notes files should be the language's equivalent of "Current Release Notes" (see style guide Release Notes Conventions)
- Translate "## New Features and Enhancements" to the language-specific header (see style guide)
- Preserve all `<Frame>`, `<BetaNote />`, `import` statements, and MDX components unchanged
- For images: check whether localized image versions exist in `/images/kb/{lang}/`; if they exist, use the localized path; if not, use the English image path as-is
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

Following all rules in `Localization-Style-Guide.mdx` and (for Japanese) `localization/Japanese-Localization-Reference.mdx`:

- Translate the `title:` and `excerpt:` frontmatter fields
- Translate all prose, headings, list items, and callout body text
- Apply language-specific term translations from the style guide glossary
- **For Japanese specifically:** Apply the expanded term glossary from `localization/Japanese-Localization-Reference.mdx` — it supersedes the style guide glossary where they conflict. Pay special attention to:
  - `<Note>` callout label → `**注記：**` (not `**注：**`)
  - "Chart" (generic) → `チャート` (not `グラフ`)
  - "Role" (agent field) → `権限` with `［ ］` brackets; "Instructions" (agent field) → `説明` with `［ ］` brackets
  - UI menu names use `「 」` brackets; UI field names use `［ ］` brackets
  - Default verb form for instructions: `〜します` (not `〜してください` unless imperative)
  - "For more information" → `詳細については`; "Step N:" → `ステップ N：`
- For images: check whether localized images exist; if they exist, use the localized path; if not, use the English image path as-is
- Internal links: always keep as English paths (`/s/article/...`) — do not prefix with a language code
- Preserve all MDX components, code blocks, import statements, and formatting exactly — **with two exceptions: BetaNote and legacy TOC blocks** (see below)
- **Legacy TOC blocks:** Some older English articles were originally migrated with an old-format table-of-contents block immediately after frontmatter — a `---` horizontal rule, then `######` or `##` headings with bullet lists summarizing the article, then another `---`. These blocks have since been removed from English. If the English source article you are translating contains one, do NOT include it in the translation. If an existing localized version you are updating has one, remove it. The pattern to recognize: frontmatter `---` → blank line → `---` → section headings with bullets → `---` → actual content.
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
ja/s/article/FILENAME.mdx
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

## Step 4: Quality Review

After writing all translations and before reporting to the user, review every translated file you just wrote against `Localization-Style-Guide.mdx`. This is a mandatory quality checkpoint — catch anything that was hallucinated, mis-applied, or accidentally skipped.

Work through the following checklist for each language. Revise the file in place if you find an issue; do not just note the issue and move on.

### Universal checks (all languages)

- [ ] **Never-translated terms still in English.** Verify that every Domo brand name (DataSet, DataFlow, Beast Mode, Magic ETL, Analyzer, etc.) and every technical acronym (ETL, OAuth, SQL, API, SAML, etc.) appears unchanged in the translation. Search the translated file for any suspicious rendering.
- [ ] **Callout labels are correct for the language.** Check every `<Note>`, `<Warning>`, and `<Tip>` block. The label inside the callout must match the language-specific form from the style guide (e.g., `**注記：**` for Japanese, `**Remarque :**` for French).
- [ ] **BetaNote uses the correct language export.** If the English source used `<BetaNote />`, confirm the translated file imports and uses `<BetaNoteEs />`, `<BetaNoteFr />`, `<BetaNoteDe />`, or `<BetaNoteJa />` as appropriate.
- [ ] **No legacy TOC block.** Confirm there is no old-style table-of-contents block (a sequence of `---` / heading bullets / `---`) immediately after frontmatter.
- [ ] **No content added or removed.** Verify that every section, heading, list item, and callout from the English source is present in the translation, with nothing extra added.
- [ ] **MDX structure is intact.** Component names, attribute names (except translated `title=` on `<Accordion>` and descriptive `alt=`), import statements, code blocks, and inline code are all unchanged.
- [ ] **Frontmatter is correct.** `title` and `excerpt` are translated. No fields were added or removed. `tag` fields (if present) are unchanged.
- [ ] **Internal links are English paths.** No `/s/article/` link was prefixed with a language code.
- [ ] **Blank lines before callouts.** Every `<Note>`, `<Warning>`, and `<Tip>` is preceded by a blank line in the MDX source.
- [ ] **Screenshots remain in `<Frame>`.** All block-level images are still wrapped in `<Frame>`. No `<Frame>` was removed.
- [ ] **Present tense throughout.** No sentence uses future tense (`will`) or conditional tense where the English source used present tense.

### Language-specific checks

**Spanish**
- [ ] Formal register (usted, not tú); imperative verbs use formal forms ("Seleccione", "Haga clic")
- [ ] Magic ETL is expanded as "Magic - Extracción, transformación y carga" on first mention in headings/body
- [ ] Callout labels: `**Nota:**`, `**Importante:**`, `**Sugerencia:**`

**French**
- [ ] Formal register (vous, not tu); imperative verbs use plural formal forms ("Sélectionnez", "Cliquez")
- [ ] Space before `:`, `!`, `?`, `;` in French prose (e.g., `**Remarque :**` not `**Remarque:**`)
- [ ] Callout labels: `**Remarque :**`, `**Important :**`, `**Conseil :**`

**German**
- [ ] Formal register (Sie, always capitalized); imperative verbs use formal forms ("Wählen Sie", "Klicken Sie")
- [ ] All nouns are capitalized, including translated common nouns (e.g., "die Berechtigung", "der Bericht")
- [ ] Hyphenated compounds where one element is English (e.g., "Cloud-Integration", "KI-Chat")
- [ ] Callout labels: `**Hinweis:**`, `**Wichtig:**`, `**Tipp:**`

**Japanese — TM-augmented checklist**

Run all of the following for every Japanese article. These are sourced from `localization/Japanese-Localization-Reference.mdx` and supersede any contradictory items in the base style guide checklist above.

- [ ] `<Note>` callout label is `**注記：**` — **not** `**注：**` (critical TM correction)
- [ ] `<Tip>` label is `**ヒント：**`
- [ ] `<Warning>` label is `**重要：**`
- [ ] "Chart" in a generic context is `チャート` — not `グラフ` (specific chart-type names with グラフ suffix are fine)
- [ ] "Role" (Domo Agent configuration field) is translated as `権限`, displayed as `**［権限］**` or `［権限］`
- [ ] "Instructions" (Domo Agent configuration field) is translated as `説明`, displayed as `**［説明］**` or `［説明］`
- [ ] UI menu/page/dialog names are wrapped in `「 」`; UI field/button labels are wrapped in `［ ］`
- [ ] Instructional verb form defaults to `〜します` — use `〜してください` only when the English is explicitly imperative or urgent
- [ ] "Step N:" formatted as `ステップ N：` (full-width colon, half-width space after)
- [ ] "For more information" / "learn more" → `詳細については` or `詳細`
- [ ] Polite formal (です/ます) style throughout — no plain (だ/である) forms
- [ ] `DataSet`, `DataFlow`, `Magic ETL`, `Beast Mode`, `Analyzer`, `Buzz`, `Domo`, `API`, `CRM`, `SQL`, `OAuth`, `SAML` kept in English

### If you find an issue

Fix it immediately in the translated file using the Edit tool. Do not accumulate issues for a later pass. After fixing, re-check the specific rule to confirm the fix is correct.

---

## Step 5: Output

Tell the user:

1. **Files created or updated** — list each new or modified file path
2. **Navigation entries added** — list each `docs.json` insertion (language, tab, group, position)
3. **Archived files** (Current Release Notes flow only) — what was archived, where, and any languages where the archive was skipped because it already existed
4. **Quality review findings** — briefly note any issues that were found and fixed during the quality checkpoint; if none, say "Quality review passed — no issues found."
5. **docs.json validation** — confirm it passed or report the error
6. **Next step for Japanese articles:** Remind the user that after a human reviewer has edited and approved the Japanese translation, running `/localize lqa-update ja/s/article/FILENAME.mdx` will extract any reviewer-made changes and register them as LQA entries in `localization/Japanese-Localization-Reference.mdx` for future translations.

---

## Step 6: Token Tracking

After reporting to the user, append one row to `localization/localize-token-usage.csv`.

**Get the values:**

```bash
# Today's date
date +%Y-%m-%d

# Git username (the person running the skill)
git config user.name
```

**Estimate tokens:**
Based on the article(s) you just processed, estimate total tokens for this skill run using these rough tiers (includes translation, quality review, nav updates, and prompt overhead):

- Small article (<500 words): ~15,000–25,000 tokens
- Medium article (500–1,500 words): ~25,000–50,000 tokens
- Large article (>1,500 words): ~50,000–100,000 tokens
- Add ~10,000 tokens per additional language beyond the first
- Add ~5,000 tokens when `localization/Japanese-Localization-Reference.mdx` was read (Japanese target)

Write an integer estimate (e.g., `35000`). For exact counts, check the Anthropic Console API logs for this session.

**Append the row:**

```bash
echo "$(date +%Y-%m-%d),$(git config user.name),ARTICLE_FILENAME,LANGUAGES_LIST,TOKEN_ESTIMATE" >> localization/localize-token-usage.csv
```

For `LANGUAGES_LIST`, use a slash-separated list of language codes (e.g., `es/fr/de/ja`). For `ARTICLE_FILENAME`, use just the filename (e.g., `March-2026-Release.mdx`), not the full path.

Do not leave a blank line before or after the appended row — the CSV must stay valid.
