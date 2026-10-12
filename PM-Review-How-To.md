# KB Restructure — PM Review How-To

**Your deadline to finish your review: ~November 13, 2026**
**Restructured KB goes live: November 30, 2026**

Thanks for helping with the Knowledge Base restructure. This guide walks you through
reviewing the changes in your product area. The whole process is driven by a Claude
skill, so you don't need to hunt through files or know any git — you'll mostly answer
questions.

---

## What you're being asked to do

As part of the restructure, Claude generated new navigation articles (overviews, "What
is X" pages) and gap-fill articles, and made edits to some existing articles in your
area. All of it has been drafted and fact-checked by AI, but it needs a human expert —
you — to confirm it's **accurate** and **phrased the way you'd want**.

For each item, you'll do one of the following:

- **Approve** — it's correct as written.
- **Change / rewrite** — tell Claude what to fix; it edits, shows you, and you confirm.
- **Reject** — back the change out entirely.
- **Answer** — some articles have an open question marked for you (`[pm-input]`); you
  provide the missing information so the article can be finished or written.

That's the whole job: go down your checklist and give each item one of those responses.

---

## One-time check: make sure you're on your branch

You have your own branch so your changes never collide with anyone else's. Open the
`domo-documentation-hub` repo in VS Code with the Claude extension, then confirm you're
on your branch. You can just ask Claude:

> What branch am I on?

It should be **`restructure/pm/<your-name>`** (for example, `restructure/pm/jordan-jensen`).
If it isn't, ask Claude to switch you to it. If the branch doesn't exist, let Jared know —
branches are created centrally.

---

## Step 1 — Pull the latest

Before you start (and any time you come back to it), get the newest version of your
branch. Just tell Claude:

> Pull the latest for my branch.

---

## Step 2 — Start the review

In Claude, run the review skill:

```
/pm-review
```

It automatically loads **your** checklist based on the branch you're on. It'll tell you
how much there is to review and pick up wherever you left off, so you can do it in one
sitting or a little at a time.

---

## Step 3 — Walk the checklist

Claude presents one item at a time. For each one it shows you the exact change (or the
question it needs answered) and asks how you'd like to respond. Reply in plain language —
**approve**, **change it** (and say how), **reject**, or **answer the question**. If you
want to come back to something later, say **skip** and it'll resurface at the end.

A few tips:

- If you're not sure about a claim, you can hand Claude context to check it against — a
  spec, a CSV, a doc, screenshots, or notes. Just point it at them.
- Want to focus? Ask it to show you only a certain kind of item (for example, "just the
  fact-checks today").
- Ask "where are we?" any time for a count of what's done and what's left.

---

## Step 4 — Commit and push when you're done (or at a stopping point)

When you finish — or just want to save progress — tell Claude:

> Commit and push my changes.

**You do not need to create a pull request.** Your branch already has a PR open that
feeds back into the restructure. Committing and pushing is all that's needed; Jared
merges the branches together at the end.

---

## See your changes in a live preview

Because a PR already exists for your branch, there's a self-updating preview of the full
restructured KB **with your changes included**. If you'd rather see the pages rendered
than read diffs, ask Jared for your preview link — it refreshes automatically each time
you push.

---

## When you're finished

Once you've given every item a response and pushed, you're done — let Jared know so he
can roll your branch into the restructure. Please aim to wrap up by **~November 13** so
everything lands in time for the **November 30** go-live.

**Questions or stuck?** Reach out to Jared Peterson (Knowledge Base Administrator) — happy
to give you a quick refresher or jump on a screen share to get you started.
