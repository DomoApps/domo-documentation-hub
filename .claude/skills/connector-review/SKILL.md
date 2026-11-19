---
name: connector-review
description: >
  Automate the connector PR/Jira review workflow: match open GitHub PRs to Jira tickets,
  check approval status, post follow-ups, merge, and close tickets. Use when Jared asks
  to review connector PRs, run the connector dashboard, follow up on stale tickets, merge
  a specific connector ticket, or when handling a publish or migration request from Arun.
---

# Connector PR Review

Orchestrates `scripts/connector-review.py` to manage the full connector documentation
review lifecycle — from open PR to merged and Jira-closed.

This skill runs in **two modes**:

- **Interactive** — Jared runs it by hand. It presents the dashboard and **asks before any
  merge** (see **Guardrails**). This is the default when a human invokes the skill.
- **Automated daily (CI)** — the **Connector Review Daily** GitHub Action
  (`.github/workflows/connector-review-daily.yml`) runs it unattended every morning (~5–6am
  PST). There is no human to ask, so the manual "ask Jared" approval is replaced by an
  automated **site-safety gate** that performs the same "won't break the site" check Jared
  did by eye. See **Automated Daily Review (CI)** below.

## Prerequisites

Before the first run, ensure `.env` exists at the repo root with these values:
```
JIRA_EMAIL=<your domo email>
JIRA_API_TOKEN=<token from https://id.atlassian.com/manage-profile/security/api-tokens>
```

The `gh` CLI must be authenticated (`gh auth status`). Both are set up once; the script
reads them automatically on every subsequent run.

---

## Workflow

### Step 1 — Run the dashboard

```bash
python3 scripts/connector-review.py
```

This fetches all open PRs from `arun.raj/connectors-DOMO-*` branches, matches each to
its Jira ticket, and prints a status table. Each PR/ticket pair lands in one of these states:

| State | Meaning |
|---|---|
| `READY TO MERGE` | Both Jared (GitHub) and secondary approver (Jira) have approved |
| `AWAITING YOUR GITHUB APPROVAL` | Secondary approved in Jira; Jared still needs to approve on GitHub |
| `Awaiting both approvals` | Neither has approved yet; PR is < 7 days old |
| `Awaiting secondary approval` | Jared approved on GitHub; waiting on secondary in Jira |
| `Changes requested` | Outstanding `CHANGES_REQUESTED` review on GitHub — wait for Arun |
| `STALE ≥7 days` | Secondary hasn't approved; follow-up #1 is due |
| `STALE ≥14 days` | Secondary still hasn't approved; follow-up #2 is due |
| `ESCALATION ≥21 days` | 3 weeks open, 2 follow-ups sent with no response — auto-merge eligible |
| `PUBLISH REQUEST` | Arun's Jira comment asks to publish the document directly (no secondary approval needed) |
| `MIGRATION REQUEST` | Arun's Jira comment requests a missed-migration article — see Migration flow below |
| `ON HOLD` | Ticket is on indefinite hold; excluded from all automatic actions — see On-Hold flow below |

Each PR row also prints the matched ticket's **summary and Jira status**, so a branch
that names the wrong ticket is visible at a glance (e.g. the summary describes a
different feature than the PR title, or the ticket is already Resolved with no approval).

Show the user the dashboard output, including PR numbers, Jira IDs, ages, and states.

#### Wrong-ticket safeguard (sibling approval)

The Jira ID comes from the branch name (`arun.raj/connectors-DOMO-######-...`). Arun
sometimes bakes the **wrong number** into the branch, or files near-duplicate tickets
(e.g. one for the KB body and one for the FAQ) and does the review on the sibling. The
script then checks a ticket with no approval while the real approval sits on its twin.

When a PR's branch ticket has **no secondary approval**, the script searches for a
near-identical sibling ticket (matched on the distinctive words in the summary) that
*does* have one, and prints:

```
  ⚠️  POSSIBLE WRONG-TICKET MATCH: no approval on DOMO-503202, but sibling DOMO-503201 has one
      from @Satish Mahenge  —  DOMO-503201: "Shopify Connector - Discount Codes Using GraphQL re" (Resolved)
      The branch name may reference the wrong ticket. Verify, then route the merge/close to DOMO-503201 if correct.
```

This never auto-acts — it only surfaces the candidate. When you see it:

1. **Verify** the sibling is genuinely the same work (compare summaries and the PR diff).
2. If it is, the PR is approved — but `--merge DOMO-<branch-id>` would comment on and close
   the *wrong* (un-approved) ticket. **Ask Jared how to route the Jira side** (comment +
   close the approved sibling; optionally close the branch ticket as a duplicate), then
   run the merge against the correct ticket. If the Jira routing differs from the branch
   ID, do the merge comment/close on the sibling directly rather than via
   `--merge <branch-id>`.
3. If the sibling is *not* the same work, ignore the warning and treat the PR as awaiting
   approval normally.

### Step 2 — Take actions

After presenting the dashboard, identify any tickets that need action and offer to handle them.

#### Ready to merge
Both approvals are in. Merge, comment, and close:
```bash
python3 scripts/connector-review.py --merge DOMO-######
```
This will:
1. Merge the PR on GitHub (merge commit)
2. Post a comment in the Jira ticket @-mentioning Arun and the secondary approver with the
   next release branch and Monday publish date (e.g., "release/v2.10.0 on Monday June 29, 2026")
3. Close the Jira ticket

#### Awaiting your GitHub approval — auto-approve and merge
When the secondary approver has already verified changes in Jira but Jared has not yet
approved on GitHub, the script **will automatically approve the PR on GitHub and then
merge it** — no need to open GitHub separately or run the skill twice.

**Before taking this action, always ask Jared first:**
> "The secondary approver has already verified the following PR(s) in Jira. Want me to
> approve and merge them now?
> - PR #XXX / DOMO-###### — [title]"

If Jared says **yes**, run:
```bash
python3 scripts/connector-review.py --merge DOMO-######
```
The script will approve on GitHub, merge, post the Jira merge comment, and close the ticket.

If Jared says **no**, skip those tickets and continue with the rest of the dashboard actions.

#### Stale — follow-up due
```bash
python3 scripts/connector-review.py --follow-up DOMO-######
```
Posts a follow-up comment in the Jira ticket @-mentioning the secondary approver.
- Follow-up #1 is posted when the PR has been open ≥ 7 days with no secondary approval.
- Follow-up #2 is posted when ≥ 14 days have passed and the first follow-up got no response
  (minimum 7 days between follow-ups is enforced).

#### Escalation
The PR has been open ≥ 21 days, two follow-ups have been sent, and the secondary has not
responded. The script will auto-merge:
```bash
python3 scripts/connector-review.py --merge DOMO-######
```
If Jared hasn't yet approved on GitHub, the script approves first, then merges.
The Jira merge comment will @-mention the secondary approver and note that if they want
changes, they should open a new ticket.

#### Publish request
Arun has commented in the Jira ticket asking to publish the document directly
(e.g., "@Jared please publish this document"). No secondary approval needed.
Merge immediately:
```bash
python3 scripts/connector-review.py --merge DOMO-######
```

#### Run all due actions at once
```bash
python3 scripts/connector-review.py --auto
```
Handles every ticket in an actionable state — ready-to-merge, awaiting-jared (auto-approve
+ merge), stale (follow-up), escalation, and publish-request — in a single run.

**Before running `--auto`, always ask Jared to confirm**, since it will approve PRs on
GitHub, merge, post Jira comments, and close tickets without further prompts. If there are
any `awaiting-jared` tickets in the batch, call them out explicitly in the confirmation ask.

#### Dry run (preview without writing anything)
```bash
python3 scripts/connector-review.py --dry-run
```

---

## Merge Conflict Resolution

If `merge_pr` detects a conflict (either from the GitHub mergeability check or from a
failed `gh pr merge`), the script will:
1. Fetch origin and check out the conflicting branch locally
2. Run `git merge origin/main` to reverse-merge main into the branch
3. If the merge is clean — push and complete the merge automatically
4. If there are real conflicts — list the conflicting files and stop

When conflicts are reported, resolve them as follows:

1. The branch is already checked out locally. Read each conflicting file and resolve the
   conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`). For KB articles, the right call is
   almost always to keep the incoming changes from the PR branch and update any main-branch
   structural changes (frontmatter, nav registration) around them.

2. After resolving all files:
   ```bash
   git add <resolved-files>
   git commit -m "Merge main into <branch-name>, resolve conflicts"
   git push origin <branch-name>
   ```

3. Return to main and retry the merge:
   ```bash
   git checkout main
   python3 scripts/connector-review.py --merge DOMO-######
   ```

4. The script will re-check mergeability and proceed with the normal merge → Jira comment
   → close flow.

## On-Hold Flow

Some tickets need to be paused indefinitely — for example, a PR whose content is blocked
on a product decision or is no longer being actively reviewed. On-hold tickets appear in a
separate **ON HOLD** section at the bottom of the dashboard and are skipped by all automatic
actions including `--auto`.

Hold state is tracked in `tracking/connector-on-hold.json` in the repo root. This file is
committed to git so the hold list persists across sessions and is visible in history.

### Put a ticket on hold
```bash
python3 scripts/connector-review.py --hold DOMO-###### --reason "reason text"
```
`--reason` is optional but recommended. The entry is saved with today's date as `held_since`.

### Remove a ticket from hold
```bash
python3 scripts/connector-review.py --release-hold DOMO-######
```
The ticket reappears in the normal dashboard on the next run with its current Jira/GitHub
approval state.

### Check held tickets for new Jira activity
```bash
python3 scripts/connector-review.py --check-holds
```
Fetches Jira comments for each on-hold ticket. If any new comment since `held_since`
contains an approval phrase, publish request, or migration request, the script flags it and
suggests running `--release-hold`. It **does not** auto-release — you decide. The
`last_checked` and `check_notes` fields in the JSON are updated on every run.

### Dashboard display
On-hold tickets are shown below the main active table, with held-since date, reason, and
last check notes (e.g., "No new approval activity" or "New activity: Satish: [approval phrase]").

### Guardrails for on-hold tickets
- `--follow-up` and `--merge` refuse to act on a held ticket; run `--release-hold` first.
- `--auto` silently skips all on-hold tickets.
- `--check-holds` is the correct way to monitor held tickets without releasing them.

---

## Migration Request Flow

When a Jira ticket contains a migration request (e.g., "This article was missed from the
migration — please migrate"), the state shows `MIGRATION REQUEST`. There is no existing PR
to merge; the migration work must be done first.

### How to handle it:

1. **Tell Jared**: "This ticket (DOMO-######) is a migration request. To proceed, I'll need
   the HTML content of the article from Salesforce. Can you pull it and paste it here,
   or save it to a local file?"

2. **Once Jared provides the HTML**, invoke the `/migrate-html` skill to convert and publish
   the article. That skill will handle the conversion, save the file to `s/article/`, add
   it to `docs.json`, and create a PR.

3. **After the PR is merged** (the migrate-html skill creates and merges the PR), close the
   Jira ticket:
   ```bash
   python3 scripts/connector-review.py --close-ticket DOMO-######
   ```

4. No follow-up comment is needed beyond what the migrate-html skill produces — the ticket
   closure signals completion.

---

## Find Tickets Without a Matching PR

Publish and migration requests sometimes come in tickets that have no GitHub PR yet.
Search Jira for them:
```bash
python3 scripts/connector-review.py --find-tasks
```
This searches for open tickets where Arun has commented with publish or migration phrases.
Review the list and handle each according to the flows above.

---

## Comment Templates

All comment text lives in `scripts/connector-templates.json`. Edit the `intro`, `body`, and
`secondary_note` values there to change what gets posted. Do **not** change the `marker`
strings — they are used internally to track which follow-ups have been sent.

Available placeholders: `{pr_num}`, `{pr_title}`, `{pr_url}`, `{next_branch}`, `{next_monday}`.

---

## Release Date Logic

The script automatically calculates:
- **Next release branch**: inspects `git branch -r` for the latest `release/v*` branch and
  increments the minor version (e.g., `v2.9.0` → `release/v2.10.0`).
- **Publish date**: always the next Monday from today's date.

No manual input needed; these are computed fresh on every run.

---

## Approval Detection

**GitHub**: the script checks `gh pr list` reviews for a state of `APPROVED` from the
authenticated user (Jared).

**Jira**: the script parses Arun's first comment that @-mentions others, extracts the
mentioned account IDs, then scans subsequent comments from those accounts for approval
phrases defined in `connector-templates.json` (e.g., "looks good", "verified", "LGTM",
"KB looks good to me").

**Sibling fallback**: if the branch's ticket has no approval, the script additionally
checks for a near-identical sibling ticket that does, and flags it on the dashboard (see
*Wrong-ticket safeguard* above). This catches a wrong Jira ID in the branch name. It is a
heads-up only — it never changes merge or `--auto` behavior.

> **Jira search endpoint**: sibling detection and `--find-tasks` use the enhanced
> `/rest/api/3/search/jql` endpoint. The legacy `/rest/api/3/issue/search` endpoint was
> retired on Jira Cloud and now returns HTTP 404, so don't reintroduce it.

---

## Automated Daily Review (CI)

The **Connector Review Daily** workflow (`.github/workflows/connector-review-daily.yml`)
runs this skill headless every morning via `claude -p`. Because no human is present, the
manual GitHub approval is replaced by an automated **site-safety gate**. The gate answers
only the narrow question Jared answered by eye when approving — *does this submission render
and leave the site intact?* — **not** whether the content is correct. **Content approval is
unchanged: it still comes from the secondary approver in the Jira ticket.** No fact-checking.

### The site-safety gate — `scripts/connector-review-gate.py`

Run against a candidate PR's branch (checked out, compared to `origin/main`). It prints a
JSON summary and exits `0` (pass), `1` (fail → do not merge), or `2` (gate could not run).

**Hard checks (any failure blocks the merge, PR left open for manual attention):**
- `docs.json` is valid JSON.
- `docs.json` navigation integrity — every page reference resolves to a real file, in every
  language (reuses `DocStructureExtractor` from `scripts/commands/export_structure.py`).
- **MDX renderability** — `remark` reports no fatal (unparseable MDX/JSX) on the changed files.
- **No new broken internal links** — `scripts/check-broken-links.py --base origin/main`.
- **No case-colliding paths** — same rule as `.github/workflows/case-collision-check.yml`.
- **Alt text on added images** — every image this branch adds carries non-empty `alt`
  (decorative icons marked `aria-hidden="true"` are exempt). Scoped to added lines, so legacy
  images never block. Missing alt can't be invented, so it routes the PR to manual.

**Soft (reported, never blocks):** Domo style-guide warnings from `remark-domo-style.mjs`.
These are auto-fixed by the revise pass below; residual warnings are logged but don't break
the site, so they don't gate the merge.

### Per-candidate automated flow

For each ticket the dashboard puts in a mergeable state — `ready-to-merge`, `awaiting-jared`
(secondary approved in Jira, just missing the human GitHub approval), `publish-request`, or
`escalation`:

1. Check out the PR branch (`gh pr checkout <n>`).
2. **Auto-revise:** apply the `revise-submission` style/MDX checklist to the changed
   `s/article`/`s/topic`/`portal` `.mdx` files and run `python3 scripts/pad_md_tables.py` on
   any with tables. Commit and push the fixes to the PR branch. This must happen **before**
   the merge, because the branch ruleset dismisses stale reviews on push.
3. Run `python3 scripts/connector-review-gate.py`.
4. **Gate passes** → `python3 scripts/connector-review.py --merge DOMO-######` (approves on
   GitHub, merges, posts the Jira comment, closes the ticket). **Gate fails or errors** → do
   **not** merge; leave the PR open and record the exact reason in the run-log and the issue.
5. Return to `main` (`git checkout main`) before processing the next candidate, so the working
   tree is never left on a feature branch.

Other states: `stale-1`/`stale-2` → `--follow-up DOMO-######`; always run `--check-holds`;
`migration-request` is deferred to manual (it needs Salesforce HTML and the `/migrate-html`
skill); `changes-requested` and on-hold tickets are left untouched.

### Outputs every run

- **Run-log:** while on `main` at the end of the run, append a dated entry to
  `.claude/skills/connector-review/run-log.md` — the candidates seen, the gate ruling and
  action for each ticket (merged / followed-up / skipped) **and why**, plus holds activity.
  Then commit this file **and** `tracking/connector-on-hold.json` (if changed) and push to
  `main` (the PAT's admin bypass allows the direct push).
- **Tracking issue:** find-or-create the pinned GitHub issue labeled `connector-review-log`
  and post the same summary as a dated comment (`gh issue list/create/comment`).

### Credentials (CI)

`JIRA_EMAIL` + `JIRA_API_TOKEN` (Jira Basic auth), `ANTHROPIC_API_KEY` (the headless Claude
run), and `CONNECTOR_REVIEW_PAT` — an **admin** GitHub PAT exported as `GH_TOKEN` so `gh`
acts as Jared and merges past the `main` ruleset via the Admin bypass, exactly as a local run
does. The `dry_run` workflow input forces `--dry-run` and skips all writes.

## Guardrails

The script will **refuse to merge** if:
- There is an outstanding `CHANGES_REQUESTED` review on GitHub from any non-Jared reviewer.
- The target ticket is on hold.
- The PR has unresolved merge conflicts that can't be auto-resolved.

**Interactive mode** — when a human runs the skill, it will **always ask Jared before**:
- Running `--auto` (which may approve + merge multiple PRs)
- Merging any `awaiting-jared` ticket (secondary approved; call it out explicitly)

**Automated daily (CI) mode** — there is no human to ask, so the **site-safety gate replaces
Jared's GitHub approval** (see **Automated Daily Review (CI)**). The Jira secondary-approval
precondition is unchanged — the automation never merges content that lacks the approver's
sign-off in Jira (the `publish-request` and `escalation` states remain the same deliberate
exceptions they already were). A gate failure always stops the merge and routes the PR to
manual review.
