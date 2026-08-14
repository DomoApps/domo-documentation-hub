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

Show the user the dashboard output, including PR numbers, Jira IDs, ages, and states.

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

---

## Guardrails

The script will **refuse to merge** if:
- There is an outstanding `CHANGES_REQUESTED` review on GitHub from any non-Jared reviewer.

The skill will **always ask Jared before**:
- Running `--auto` (which may approve + merge multiple PRs)
- Merging any `awaiting-jared` ticket (secondary approved; call it out explicitly)
