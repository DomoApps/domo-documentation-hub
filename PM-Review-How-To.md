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

## A special case: articles that still need to be written

Part of your checklist may be **gap-fill articles** — pages the restructure identified as
missing in your area but that couldn't be written without your input. These don't exist yet,
so instead of reviewing a change, you'll decide what should happen to each one. You have three
choices, and Claude will record whichever you pick:

- **Write it now** — the article is needed and you'll help. Claude interviews you for the
  details, drafts it, and you give it a full read-through (see below) before it's done.
- **Defer it** — the article is still worth having, but not something you can get to this
  cycle. It's set aside and carried onto a follow-up list so it isn't lost; it just won't be
  written as part of this restructure.
- **Drop it** — the article isn't actually needed (already covered elsewhere, no longer
  relevant, or not a real gap). It's removed from the restructure's scope for good. Unlike a
  deferral, a dropped article is **not** carried onto the follow-up list — so only drop when
  you're sure it shouldn't be written at all. Claude will ask you to confirm, and to say briefly
  why, before recording it.

If you're unsure whether something belongs in your area or should exist at all, defer it and
flag it for Jared rather than dropping it.

---

## Brand-new articles: a final read-through

Any article that was written from scratch for this project — whether the restructure drafted it
(an overview or "What is X" page) or you just had Claude write a gap-fill — gets one extra step:
a **read-through**. You read the whole article end-to-end (in the file or the preview) and confirm
two things: it's **factually correct**, and it's **phrased the way you'd want it published**.

A few things to know:

- It's the **last** step on that article — Claude brings it to you only after you've handled the
  specific fact-checks and questions on it, so you're signing off on the finished page.
- It's a genuine read, not a spot-check. This is your name on the article.
- If something's off, just tell Claude what to change; it edits and shows you, and you give the
  final OK when you're happy.
- Claude tracks this sign-off, so an unread new article won't slip through to publication.

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
