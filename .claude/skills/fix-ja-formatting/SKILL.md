---
name: fix-ja-formatting
user-invocable: true
description: "Fix MDX syntax and structural formatting issues in Japanese articles without touching any translation: bold-label rendering, escaped component tags, callouts containing list items, broken links, and other MDX mis-formatting."
argument-hint: "path to a specific JA article, or omit to operate on changed JA files in the current branch"
---

Fix MDX structural and syntax issues in one or more Japanese KB articles. This skill corrects formatting problems only — every Japanese word, phrase, and sentence must be preserved exactly as written.

The user has provided: $ARGUMENTS

---

## Core rule: never touch Japanese text

Do not change, reword, reorder, or delete any Japanese text. Every edit must be a pure MDX syntax or structure fix. If the only way to fix something requires rewriting Japanese content, flag it to the user instead of editing.

---

## Step 1: Identify the file(s)

If `$ARGUMENTS` names a specific file or path, use that. Otherwise, find changed Japanese files in the current branch:

```bash
git diff --name-only $(git merge-base HEAD origin/main) | grep '^ja/'
```

Read each target file in full before making any edits.

---

## Step 2: Apply the formatting checklist

Work through every check below for each file. Use the Edit tool for each fix. Prefer narrow, targeted edits over large block rewrites.

---

### Check 1 — Bold-label rendering after fullwidth punctuation (PRIMARY CHECK)

**Why this matters:** CommonMark requires a closing `**` that is preceded by Unicode punctuation (fullwidth colon `：`, fullwidth period `。`, em-dash `—`, closing paren `）`, closing bracket `」`, etc.) to be followed by whitespace or punctuation, or it is not recognized as a right-flanking delimiter and renders as literal asterisks on screen.

**Pattern to fix:** `**label：**text` → `**label：** text`  
**Also affects:** `**label —**text`, `**label。**text`, and any `**closing-punct**non-space`

**How to find all instances:**

```bash
grep -n '：\*\*[^ *\n]' <file>
grep -n '—\*\*[^ *\n]' <file>
grep -n '。\*\*[^ *\n]' <file>
grep -n '）\*\*[^ *\n]' <file>
```

For each match, insert a single space after the closing `**`:

```
Before: <Note>**注：**このクエリはSELECTクエリのみである必要があり
After:  <Note>**注：** このクエリはSELECTクエリのみである必要があり

Before: **重要：**DataFlowの入力DataSetは
After:  **重要：** DataFlowの入力DataSetは

Before: **入力タイル —**次のタイルを
After:  **入力タイル —** 次のタイルを
```

This check applies everywhere in the file: inside `<Note>`, `<Warning>`, `<Tip>`, inline in body text, inside list items, and inside table cells.

---

### Check 2 — Trailing space inside closing bold marker

**Pattern to fix:** `**text — **` or `**text： **` (space before `**`) → `**text —**` or `**text：**`

```bash
grep -n ' \*\*[^*]' <file>
```

Remove the space that sits immediately before the closing `**`.

---

### Check 3 — HTML-escaped JSX component tags

**Pattern to fix:** `&lt;Note&gt;` / `&lt;/Note&gt;` and similarly for `Warning`, `Tip`, `Frame`, `Accordion`, etc.

```bash
grep -n '&lt;[A-Z]' <file>
```

Replace all HTML-entity-encoded component tags with their literal JSX equivalents:

```
&lt;Note&gt;    →  <Note>
&lt;/Note&gt;   →  </Note>
&lt;Warning&gt; →  <Warning>
```

---

### Check 4 — HTML entities inside inline code spans

Inside backtick code spans, `&lt;` and `&gt;` render as the literal string `&lt;` — not as `<`. Replace them with the actual characters:

```bash
grep -n '`[^`]*&lt;' <file>
```

```
`SELECT &lt;column&gt;`  →  `SELECT <column>`
```

---

### Check 5 — JSX callout containing numbered or bulleted list items

A `<Note>`, `<Warning>`, or `<Tip>` must contain only its label and note text. Numbered or bulleted list items that appear inside the opening/closing tags are structural errors — the callout swallows those steps and they may not render at all.

Look for list-item lines (`1.`, `2.`, `-`) that fall between an opening callout tag and its matching closing tag. The fix is to close the callout after the note text and let the list items continue outside:

```
# Wrong
<Note>
**注：** This is the note.
2. Next step here.
3. Another step.
</Note>

# Correct
<Note>**注：** This is the note.</Note>

2. Next step here.
3. Another step.
```

If the note text and the list item are on the same line inside the callout, split them:

```
# Wrong
<Note>**注：** Note text. 2. Step two follows.</Note>

# Correct
<Note>**注：** Note text.</Note>

2. Step two follows.
```

---

### Check 6 — Broken bold formatting split across lines

A `**` that opens on one line but whose closing `**` is at the start of the next line (with only whitespace between) will not render:

```bash
grep -n '\*\*\s*$' <file>
```

Merge the two lines into a single continuous bold span. Remove any line break or trailing whitespace inside the bold markers.

```
# Wrong
3. タイルエディターの**［設定］**タブの**  
**［データ選択］**ドロップダウンで

# Correct
3. タイルエディターの**［設定］**タブの**［データ選択］**ドロップダウンで
```

---

### Check 7 — Empty bold markers

`****` (four asterisks with nothing between them) produces no output but can confuse the parser. Remove them:

```bash
grep -n '\*\*\*\*' <file>
```

---

### Check 8 — Spaces inside link brackets or anchor IDs

Trailing or leading spaces inside `[link text]` or inside anchor fragment `#anchor-id` break or mis-target the link:

```bash
grep -n '\[ \|\ \](' <file>
grep -n '#[a-zA-Zぁ-ん一-龯].*[  ][^)]' <file>
```

```
[入力DataSet ]  →  [入力DataSet]
(#writeback -タイル )  →  (#writeback-タイル)
(#query-dataset-tile )  →  (#query-dataset-tile)
```

---

### Check 9 — Missing space after `-` at start of list bullet

When a list bullet (`-`) is immediately followed by `**` or another inline element with no space, some parsers do not recognize it as a list item:

```bash
grep -n '^-[^ \-]' <file>
```

```
-**［データベース］**  →  - **［データベース］**
```

---

### Check 10 — Broken link syntax

A Markdown link `[text](url)` must have the bracket group and paren group adjacent with no text between them. Two common failure patterns:

**Bare brackets with URL detached:**
```
# Wrong
[Advanced DataFlow Triggering]でDataFlowの実行については、こちら(/s/article/000005216)を参照

# Correct — make the English title the link anchor
[Advanced DataFlow Triggering](/s/article/000005216)でDataFlowの実行については、こちらを参照
```

**Closing bracket before Japanese text then bare URL in parens:**
```
# Wrong
[［出力DataSet］タイル]の設定方法を確認してください。(/s/article/360045402273).

# Correct — move the URL inside the bracket group
[［出力DataSet］タイル](/s/article/360045402273)の設定方法を確認してください。
```

Do NOT alter the Japanese text between the brackets and the parens — restructure only the link syntax.

---

### Check 11 — Stray comma after a link before a Japanese particle

A comma between a closing link paren `)` and a Japanese particle (`を`, `は`, `で`, etc.) is typically a translation artifact:

```bash
grep -n '),\s*を\|),\s*は\|),\s*で' <file>
```

Remove the comma; the particle follows the link directly.

```
[SQLタイル](/s/article/...), を代わりに  →  [SQLタイル](/s/article/...)を代わりに
```

---

### Check 12 — English-language translation artifacts

Look for obviously untranslated English prose blocks embedded in the Japanese body text. These are typically leftover source fragments accidentally included during translation (e.g., "In the tile configuration panel below the canvas, use the").

```bash
grep -n '[A-Za-z]\{15,\}' <file>
```

Review each long English run. If it is clearly a translation artifact (surrounded by Japanese, duplicating the Japanese text that follows, or interrupted by empty bold like `****`), remove only the English fragment. Do not remove English product names, code, or UI labels that are legitimately English (e.g., `DataSet`, `DataFlow`, SQL keywords, `Databricks`).

---

### Check 13 — Inline `<img>` elements that should use the Domo icon font

When an inline `<img>` has an `alt` text or filename that identifies a known Domo UI glyph (e.g., "settings.png", "gear", "edit"), replace it with the icon font equivalent:

```
<img alt="settings.png" src="/images/kb/..." style={{...}} />
→
<i className="icon-gear sm" aria-hidden="true" />
```

Only substitute when you can confidently identify the icon. If the `alt` is empty or ambiguous, leave the `<img>` in place.

---

## Step 3: Run the table normalizer

For every file that contains a pipe table (whether or not you touched the table directly):

```bash
python3 scripts/pad_md_tables.py <file>
```

---

## Step 4: Preview the diff

After all edits:

```bash
git diff -- <file>
```

Present a summary to the user listing each category of fix applied. Highlight any items you found but could not fix without changing Japanese text — flag those for manual review.

Then tell the user: **"Review the diff above. Reply 'looks good' (or similar) to commit and push, or let me know what to adjust."**

Do not commit or push until the user explicitly approves.

---

## Step 5: Commit and push

```bash
git add <list of revised files>
git commit -m "$(cat <<'EOF'
Fix MDX formatting in JA article(s)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
git push
```

Use specific file paths in `git add` — never `git add -A` or `git add .`.
