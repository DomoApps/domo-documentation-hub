---
name: pm-review
user-invocable: true
description: "Walk a PM through every change in their KB-restructure review brief like a resumable checklist: show the exact diff of each change, let the PM approve / deny / rewrite / reject / answer, author or defer the gap-fill articles still owed in their area, fact-check with any context they provide, and record every disposition as inline markers + a tracked ledger. Phase 4.5 of the KB restructure."
argument-hint: "PM name or slug (e.g. \"Ken Boyer\" or ken-boyer); omit to infer from the current restructure/pm/<slug> branch"
---

Run an interactive, resumable PM review of the KB restructure (Phase 4.5) for one PM.

The user has provided: $ARGUMENTS

This skill is the interactive front end for the Phase 4.5 operating loop documented in
`RESTRUCTURE-PROGRESS.md`. It drives `scripts/pm_review.py` (the engine) and reuses the
existing authoring skills. **You never reimplement item/brief logic** — the engine derives
items from the same source as the per-PM briefs and `RESTRUCTURE-TASKS.md`.

---

## Core model (read before doing anything)

- **One PM = one branch = one ledger.** Each PM reviews on `restructure/pm/<slug>`, cut from
  `update/fullRestructure`. Durable per-item state lives in `pm-review-state/<slug>.json`
  (tracked). It is the superset of truth; the item list is a volatile view reconciled against
  it on every run.
- **Hybrid state.** Every disposition is recorded TWO ways: (1) an inline marker in the article
  — burn the `{/* [pm-input] … */}` when answered, or stamp
  `{/* [reviewed] pm=<slug> status=<status> date=YYYY-MM-DD */}` for an article-level sign-off;
  (2) a ledger entry via `pm_review.py set-status`.
- **Ordering invariant (never violate):** write the ledger entry FIRST → then edit/burn the
  marker → then commit. A marker burned before the ledger records its ask can never be
  re-derived.
- **PM branches never touch shared files.** `RESTRUCTURE-TASKS.md`, `PM-REVIEW-ROLLUP.md`,
  `RESTRUCTURE-DEFERRED-ARTICLES.md`, and `docs.json` nav are regenerated on the integration
  branch after merge-backs — never hand-edited on a PM branch. `add-to-nav` for new gap-fill
  articles is **deferred to the integration branch** (Phase 7 owns the nav rebuild).
- **Diff baseline is pinned.** Diffs are shown against the single `baseline_sha` (the `main`
  commit merged into the branch), never symbolic `origin/main`.

---

## Step 0 — Preconditions (do all three; stop if any fails)

**0a. Baseline guard.** The skill cannot show meaningful diffs until `main` has been merged into
`update/fullRestructure`:

```bash
python3 scripts/pm_review.py check-baseline
```

If `ready` is `false`, STOP and tell the user: the `main`→`update/fullRestructure` merge
(incl. the localization system + Phase 3c sync-#2 numeric-ID parity) must be completed first;
that merge pins `baseline_sha`. Do not proceed.

**0b. Identify the PM.** Resolve `$ARGUMENTS` to a canonical roster name. If empty, infer from
the current branch (`git branch --show-current` → `restructure/pm/<slug>`). If still ambiguous,
ask. Confirm the PM is in the roster:

```bash
python3 scripts/pm_review.py items --pm "<PM>" --no-write   # errors + lists roster if unknown
```

**0c. Be on the PM's branch.** Ensure you are on `restructure/pm/<slug>` (the branch should
already exist; if not, tell the user — branch creation is done centrally, not here). Never run
the review on `update/fullRestructure` itself.

Also read `RESTRUCTURE-PROGRESS.md` § "Phase 4.5 — PM Review System" once to orient.

---

## Step 1 — Load the worklist and find the resume point

```bash
python3 scripts/pm_review.py items --pm "<PM>"      # full reconciled worklist (JSON)
python3 scripts/pm_review.py resume --pm "<PM>"     # first non-terminal item
```

`items` seeds/updates the ledger: it inserts new items as `pending`, refreshes existing ones,
and reports `new_items` and `stale_items`. **If `stale_items` is non-empty, surface it to the
user** — an item that was open but is no longer generated means the manifest or ownership
changed; do not silently drop it.

Tell the user the shape of the work (counts by type, how many gap-fill, open vs done), then
begin at the `resume` item. Offer to filter by type ("just the fact-checks today").

---

## Step 2 — Walk each item

For each item, in the engine's stable order, present the context (type, target, the ask /
claims to verify from `ask_snapshot`), then show **the exact change** according to its type:

| Item type | What to show |
|-----------|--------------|
| `fact-check`, `update` (existing article) | `git diff -M -C <baseline_sha> HEAD -- s/article/<target>` — the restructure change the PM signs off on. |
| gap-fill `pm-input` (target file absent) | The intended article + what must be supplied (it isn't written yet). Go to **Step 3**. |
| inline `pm-input` (target file present) | The `{/* [pm-input] … */}` marker **and its surrounding section**, so the PM answers in context. |
| `decision` (`dec-D#`), `legacy`, `retired` | **No git diff** (retirements are staged for Phase 4.6; files are unchanged). Show the staged plan from the brief + `RESTRUCTURE-MANIFEST.md`. |

For a correction you just made this session (see `rewrite/redo`), re-show only the branch-local
delta so it isn't buried under the full restructure diff:

```bash
git diff $(git merge-base update/fullRestructure HEAD)..HEAD -- s/article/<target>
git diff -- s/article/<target>     # plus any uncommitted working-tree change
```

Then offer the PM these actions:

- **approve** — the change is correct. Ledger `status=approved disposition=approve`; stamp
  `{/* [reviewed] pm=<slug> status=approved date=… */}` on the article (append; multiple PMs may
  stamp the same multi-owner overview).
- **deny (reason)** — the change is wrong but you're not fixing it now. Ledger
  `status=denied disposition=deny reason="…"`. Leave the article; the reason carries forward.
- **rewrite / redo** — the PM supplies a correction. Apply it with Edit, re-show the branch-local
  diff, loop until they approve. Then ledger `status=approved disposition=rewrite-redo`
  (+ `[reviewed]` stamp). While iterating, you may hold the item at `status=rewrite-redo`.
- **reject entirely** — back the change out. **For a modified existing article, do a targeted
  hunk/line revert or re-synthesis — NEVER `git checkout <baseline> -- <file>`** (that would wipe
  other PMs' and the main-merge content in the same file). Only a net-new file added since
  baseline may be dropped wholesale. Ledger `status=rejected disposition=reject reason="…"`.
- **provide-answer** (inline `pm-input`) — the PM answers. Edit the section with the confirmed
  content, then burn the marker. Ledger `status=answered disposition=provide-answer` FIRST.
- **skip** — come back later. Ledger `status=skipped`; it re-surfaces at the end of the pass.

Record every disposition with the engine (ledger entry FIRST, per the ordering invariant):

```bash
python3 scripts/pm_review.py set-status --pm "<PM>" --id <item_id> --status <status> \
  --disposition <disposition> [--reason "…"] [--evidence "…"] [--commit <sha>] --actor <slug>
```

Then make the article edit / marker change, then commit (see Step 5). For fact-checks confirmed
fine with no edit, the `approved` ledger entry + `[reviewed]` stamp are the record (this closes
the old "confirmed-fine fact-check leaves no diff" tracking hole).

---

## Step 3 — Gap-fill articles (author now, or defer out of scope)

Gap-fill items are `pm-input` items whose target article does not exist yet (`gap_fill: true`)
— the ~40 articles the KB couldn't write without PM input. For each in the PM's area, ask:

**Author now?** If yes:
1. Invoke `kb-intake` to gather what's needed, then `new-kb-article` (or `new-overview-article`
   for a "What is X" / hub page) to draft it into `s/article/<target>`.
2. Run the three restructure quality gates (`RESTRUCTURE-PROGRESS.md` § Quality Gates):
   fact-check → screenshot audit → style-guide review.
3. **Do NOT run `add-to-nav`** — nav registration is deferred to the integration branch. Note in
   the ledger that nav is pending.
4. Ledger `status=authored disposition=author --commit <sha>`.

**Out of scope?** If the PM can't/won't supply it now:
- Ledger `status=deferred disposition=out-of-scope --reason "<why + what it would cover>"`.
- Do not write a stub article. The deferral is the record.
- At project end, `pm_review.py deferred-report` regenerates `RESTRUCTURE-DEFERRED-ARTICLES.md` —
  the seed list for a follow-up project. Tell the user this is where it will surface.

---

## Step 4 — Fact-checking with provided context

The PM (or an assisting dev / PgM) can hand you context to verify claims yourself: paths to
connector code repositories with annotations, product specs, CSVs, screenshots. When given:
- Read/ingest the context, verify the claims in the diff against it, and record what you used in
  the ledger `--evidence` field (e.g. a repo path + commit, a spec section, a CSV).
- **Bulk verification for high-volume areas (Connectors, 1000+):** this is NOT thousands of
  tasks — it lives *inside* a single connector `fact-check` item. Drive from a provided
  source-of-truth (e.g. a connector-metadata CSV keyed by connector). Auto-confirm the rows you
  can verify, write a **batch summary** into that one ledger item's `--evidence`, and surface
  only the rows you could not verify as follow-ups for the PM.
- Respect permission boundaries: never take an action the PM's own session couldn't take, and
  never ask another session to do blocked work for you.

---

## Step 5 — Checkpoint, commit, report

- Commit on the PM branch at natural breakpoints (end of a type group, or every handful of
  items) with a structured message, e.g.:
  `pm-review(<slug>): approve 4 fact-checks, answer 2 pm-inputs, defer 1 gap-fill`.
  Include the attribution lines the session requires.
- The ledger and article edits are the only things that change on a PM branch. Do **not** touch
  the shared derived files.
- At any time the user asks "where are we?", run `items`/`resume` and report counts + the next
  item. On session resume, Step 1 re-finds the resume point automatically.
- When the PM's worklist is all terminal (`resume` returns `done: true`), tell the user this PM
  is ready to merge back; mark their row in `PM-REVIEW-STATUS.md` (hand-maintained ledger).

---

## Step 6 — Integration-branch duties (NOT on a PM branch)

These run on `update/fullRestructure` after PM branches merge back — mention them when relevant,
but only perform them when the user is on the integration branch:

```bash
python3 scripts/pm_review.py rollup             # regenerate PM-REVIEW-ROLLUP.md from all ledgers
python3 scripts/pm_review.py deferred-report    # regenerate RESTRUCTURE-DEFERRED-ARTICLES.md
python3 scripts/pm_review.py reconcile --strict # the Phase 4.5 → 4.6 marker-reconciliation gate
```

**The reconciliation sweep is the machine gate behind "every PM row Done → proceed to Phase
4.6."** It cross-references every inline marker against the ledgers and reports: `stragglers`
(open markers with no terminal coverage), `malformed_markers` (markers the generator can't
parse), `inconsistencies` (answered in ledger but marker not burned, or a `[reviewed]` stamp
with no backing), `anchorless_open_items` (open decision/lifecycle items, which have no file
anchor), and `orphan_marker_pm_names` (marker PM names matching no roster PM). Drive every one to
zero — answer+burn, defer, or fix the marker — before the restructure advances past 4.5.

---

## Guardrails

- Pre-merge: if `check-baseline` is not `ready`, do nothing else.
- Never edit shared/derived files or run `add-to-nav` on a PM branch.
- Never `git checkout <baseline> -- <file>` to reject a change on a modified file.
- Always: ledger entry → marker edit → commit, in that order.
- Keep articles clean: no TODO/placeholder markers (restructure quality-gate rule). The only
  markers that belong in articles are open `[pm-input]` (until answered) and `[reviewed]`
  sign-offs.
