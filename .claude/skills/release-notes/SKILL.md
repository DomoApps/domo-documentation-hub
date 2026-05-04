---
name: release-notes
description: Generate user-friendly release notes by diffing the latest git tag against the previous tag and summarizing the changes. Use when the user asks to "generate release notes", "write release notes for the latest release", "summarize the latest release", or similar. Saves a shareable text file to `releaseNotes/`.
---

# Release Notes Generator

Produce a friendly, email/Slack-ready release notes summary for the most recent git tag in this repo.

## Workflow

### 1. Identify the release range

```bash
git tag --sort=-creatordate | head -5
```

The top tag is the **latest release**; the next tag is the **previous release**. Confirm with the user only if the intended target is ambiguous (e.g. multiple tags on the same day, or user mentions a specific version).

Also grab tag dates for context:

```bash
git log --tags --simplify-by-decoration --pretty="format:%ai %d" | head -10
```

### 2. Diff the releases

```bash
git log <prev-tag>..<latest-tag> --stat
```

For any commit whose purpose isn't obvious from the message + file list, inspect the content:

```bash
git diff <prev-tag>..<latest-tag> -- <path>
```

Skip merge-commit noise — focus on the underlying PRs and file changes. Group related commits (e.g. multiple commits from one PR) into a single theme.

### 3. Summarize into themes

Group changes into 2–5 themed sections. Each theme gets:
- An emoji + short title (e.g. "📚 Domo.js Versioned Documentation")
- 1–3 sentences describing what changed and why it matters **to the reader** (developers, admins, customers — not internal mechanics)
- Attribution to the contributor(s) by name — pull author names from `git log`

Prefer customer-visible framing over commit-message literalism. "DOMO-482176: add v4 doc" becomes "Dedicated version-specific docs for Domo.js v4, v5, and v6."

### 4. Write the file

Save to `releaseNotes/v<version>.txt` (plain text, not MDX — this is meant to be copy/pasted into email or Slack).

Follow this structure:

```
Hello everyone!

We're excited to announce that version <X.Y.Z> of the Domo Documentation Hub is now available! <one-sentence framing of the release's overall theme> You can view these changes in our knowledge base at www.domo.com/docs.

---

**🌟 What's New**

**<emoji> <Theme Title>**
<1–3 sentences describing the change and its value.>
Thanks to <Contributor> for <brief reason>.

<repeat for each theme>

---

**🙏 Thank You**

A heartfelt thank you to everyone who contributed to this release. <one warm closing sentence>

If you have questions or feedback, please reach out — we're always happy to help!
```

Keep tone warm and appreciative. Use bullets (`  •`) for sub-lists inside a theme when listing many discrete items. All section headers — including "🌟 What's New", each theme title, and "🙏 Thank You" — must be **bolded** using `**...**`.

### 5. Confirm

Tell the user the file path and offer to adjust tone, detail, or framing.

## Notes

- Always create `releaseNotes/` if it doesn't exist — `Write` handles this automatically.
- Do **not** include internal ticket IDs (DOMO-XXXXXX) in the final notes unless the user asks; parenthetical attribution is fine.
- Do **not** commit the file unless the user asks.
