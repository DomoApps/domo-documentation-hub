#!/usr/bin/env python3
"""
Connector PR / Jira Review Dashboard

Automates the connector documentation review workflow:
  - Matches open GitHub PRs to Jira tickets via branch name (DOMO-######)
  - Determines approval state (GitHub + Jira)
  - Posts follow-up comments on stale reviews
  - Merges ready-to-merge PRs, posts merge confirmation, closes Jira tickets
  - Escalates to auto-merge after 3 weeks with 2 unanswered follow-ups
  - Detects publish-request and migration-request action types in Arun's comments

Usage:
    python3 scripts/connector-review.py              # Dashboard only
    python3 scripts/connector-review.py --auto       # Run all due actions
    python3 scripts/connector-review.py --dry-run    # Show what --auto would do (no writes)
    python3 scripts/connector-review.py --follow-up DOMO-123456
    python3 scripts/connector-review.py --merge DOMO-123456
    python3 scripts/connector-review.py --find-tasks  # Jira search: publish/migration requests
"""

import base64
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = "DomoApps/domo-documentation-hub"
JIRA_BASE = "https://domoinc.atlassian.net"
BRANCH_PATTERN = re.compile(r"arun\.raj/connectors?-(DOMO-\d+)", re.IGNORECASE)
TEMPLATES_PATH = Path(__file__).parent / "connector-templates.json"

# ── Credentials ────────────────────────────────────────────────────────────────

def load_env():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def check_credentials():
    missing = [v for v in ("JIRA_EMAIL", "JIRA_API_TOKEN") if not os.environ.get(v)]
    if missing:
        print(f"❌ Missing in .env: {', '.join(missing)}")
        print("   Copy .env.example → .env and fill in your values.")
        sys.exit(1)


def load_templates():
    return json.loads(TEMPLATES_PATH.read_text())


# ── Jira REST API ───────────────────────────────────────────────────────────────

def _ssl_context():
    ctx = ssl.create_default_context()
    # python.org Python on macOS bundles its own OpenSSL without the system CA store;
    # load the macOS system bundle directly so HTTPS to Atlassian works out of the box.
    for path in ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt"):
        if os.path.exists(path):
            ctx.load_verify_locations(path)
            break
    return ctx

_SSL = _ssl_context()


def _jira_creds():
    email = os.environ["JIRA_EMAIL"]
    token = os.environ["JIRA_API_TOKEN"]
    return base64.b64encode(f"{email}:{token}".encode()).decode()


def jira_request(method, path, data=None):
    url = f"{JIRA_BASE}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Basic {_jira_creds()}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, context=_SSL) as r:
            content = r.read()
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode()
        raise RuntimeError(f"Jira {method} {path} → HTTP {e.code}: {detail}") from e


def jira_get(path):
    return jira_request("GET", path)


def jira_post(path, data):
    return jira_request("POST", path, data)


# ── GitHub via gh CLI ───────────────────────────────────────────────────────────

def gh_json(args):
    r = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} → {r.stderr.strip()}")
    return json.loads(r.stdout)


def gh_run(args):
    r = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} → {r.stderr.strip()}")
    return r.stdout.strip()


# ── ADF helpers ─────────────────────────────────────────────────────────────────

def adf_text(text):
    return {"type": "text", "text": text}


def adf_mention(account_id, display_name):
    return {"type": "mention", "attrs": {"id": account_id, "text": display_name, "accessLevel": ""}}


def adf_doc(*paragraphs):
    return {
        "type": "doc",
        "version": 1,
        "content": [{"type": "paragraph", "content": list(p)} for p in paragraphs],
    }


def extract_text(node):
    """Recursively extract plain text from an ADF node."""
    if isinstance(node, dict):
        if node.get("type") == "text":
            return node.get("text", "")
        if node.get("type") == "mention":
            return f"@{node.get('attrs', {}).get('text', '')}"
        return " ".join(extract_text(c) for c in node.get("content", []))
    if isinstance(node, list):
        return " ".join(extract_text(c) for c in node)
    return ""


def extract_mentions(node):
    """Return list of {accountId, displayName} from all @mentions in an ADF node."""
    mentions = []
    if isinstance(node, dict):
        if node.get("type") == "mention":
            a = node.get("attrs", {})
            mentions.append({"accountId": a.get("id", ""), "displayName": a.get("text", "")})
        for child in node.get("content", []):
            mentions.extend(extract_mentions(child))
    elif isinstance(node, list):
        for item in node:
            mentions.extend(extract_mentions(item))
    return mentions


# ── Date helpers ────────────────────────────────────────────────────────────────

def parse_date(date_str):
    """Parse ISO 8601 date string (GitHub Z or Jira +0000) → aware datetime."""
    s = date_str.strip()
    s = re.sub(r"\.\d+", "", s)               # remove milliseconds
    s = s.replace("Z", "+00:00")              # GitHub Z suffix
    s = re.sub(r"([+-])(\d{2})(\d{2})$", r"\1\2:\3", s)  # +0000 → +00:00
    return datetime.fromisoformat(s)


def days_since(date_str):
    dt = parse_date(date_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - dt).days


def next_release_info():
    """Return (branch_name, next_monday_string) for the comment templates."""
    # Find latest release branch
    r = subprocess.run(
        ["git", "branch", "-r", "--list", "origin/release/v*"],
        capture_output=True, text=True,
    )
    branches = [b.strip().replace("origin/release/", "") for b in r.stdout.splitlines() if b.strip()]

    if not branches:
        r = subprocess.run(["git", "tag", "-l", "v*"], capture_output=True, text=True)
        branches = [t.strip() for t in r.stdout.splitlines() if re.match(r"v\d+\.\d+", t)]

    def semver(v):
        m = re.match(r"v?(\d+)\.(\d+)\.(\d+)", v)
        return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else (0, 0, 0)

    if branches:
        current = sorted(branches, key=semver)[-1]
        ma, mi, _ = semver(current)
        next_branch = f"release/v{ma}.{mi + 1}.0"
    else:
        next_branch = "the next release"

    today = datetime.now().date()
    days_to_monday = (7 - today.weekday()) % 7 or 7  # if today is Monday, use next Monday
    next_monday = today + timedelta(days=days_to_monday)
    next_monday_str = next_monday.strftime("Monday %B %-d, %Y")

    return next_branch, next_monday_str


# ── Identity ─────────────────────────────────────────────────────────────────────

def my_github_login():
    r = subprocess.run(["gh", "api", "user", "--jq", ".login"], capture_output=True, text=True)
    return r.stdout.strip()


def my_jira_account():
    return jira_get("/rest/api/3/myself")


# ── PR discovery ─────────────────────────────────────────────────────────────────

def get_open_connector_prs():
    prs = gh_json([
        "pr", "list", "--repo", REPO, "--state", "open", "--limit", "100",
        "--json", "number,title,headRefName,createdAt,reviews,url,author",
    ])
    return [pr for pr in prs if BRANCH_PATTERN.search(pr.get("headRefName", ""))]


def extract_jira_id(branch_name):
    m = BRANCH_PATTERN.search(branch_name)
    return m.group(1) if m else None


# ── Analysis ──────────────────────────────────────────────────────────────────────

def analyze_github_pr(pr, jared_login):
    """Return {jared_approved, changes_requested}."""
    latest_by_reviewer = {}
    for r in pr.get("reviews", []):
        login = r.get("author", {}).get("login", "")
        latest_by_reviewer[login] = r.get("state", "")

    jared_approved = latest_by_reviewer.get(jared_login) == "APPROVED"
    changes_requested = any(
        state == "CHANGES_REQUESTED"
        for login, state in latest_by_reviewer.items()
        if login != jared_login
    )
    return {"jared_approved": jared_approved, "changes_requested": changes_requested}


def analyze_jira_ticket(jira_id, my_account_id, templates):
    """
    Return dict with:
      secondary_approvers, secondary_approved, follow_up_count,
      last_followup_date, has_escalation_comment, action_type,
      arun_account, comments — or 'error' key on failure.
    """
    try:
        data = jira_get(f"/rest/api/3/issue/{jira_id}/comment?maxResults=200&orderBy=created")
    except RuntimeError as e:
        return {"error": str(e)}

    comments = data.get("comments", [])
    approval_phrases = templates.get("approval_phrases", ["looks good", "lgtm", "approved", "verified"])
    publish_phrases = templates.get("publish_request_phrases", ["please publish"])
    migration_phrases = templates.get("migration_request_phrases", ["please migrate"])

    # Find Arun's initial comment that @-mentions others
    arun_comment = None
    for c in comments:
        author = c.get("author", {})
        name = author.get("displayName", "").lower()
        email = author.get("emailAddress", "").lower()
        if "arun" in name or "arun" in email:
            mentions = extract_mentions(c.get("body", {}))
            non_arun = [m for m in mentions if "arun" not in m["displayName"].lower()]
            if non_arun:
                arun_comment = c
                break

    # Extract secondary approvers (Arun's @-mentions minus Jared)
    secondary_approvers = []
    action_type = "review"  # default
    arun_account = None

    if arun_comment:
        arun_account = {
            "accountId": arun_comment.get("author", {}).get("accountId", ""),
            "displayName": arun_comment.get("author", {}).get("displayName", "Arun Raj"),
        }
        mentions = extract_mentions(arun_comment.get("body", {}))
        seen = set()
        for m in mentions:
            if "arun" in m["displayName"].lower():
                continue
            if m["accountId"] == my_account_id:
                continue
            if m["accountId"] not in seen:
                seen.add(m["accountId"])
                secondary_approvers.append(m)

        # Detect action type from Arun's comment text
        comment_text = extract_text(arun_comment.get("body", {})).lower()
        if any(p in comment_text for p in migration_phrases):
            action_type = "migration"
        elif any(p in comment_text for p in publish_phrases):
            action_type = "publish"

    secondary_ids = {a["accountId"] for a in secondary_approvers}

    # Check for secondary approval after Arun's comment
    secondary_approved = False
    past_arun = arun_comment is None  # if no arun comment, scan all
    for c in comments:
        if not past_arun:
            if c.get("id") == arun_comment.get("id"):
                past_arun = True
            continue
        author_id = c.get("author", {}).get("accountId", "")
        if author_id in secondary_ids:
            text = extract_text(c.get("body", {})).lower()
            if any(p in text for p in approval_phrases):
                secondary_approved = True
                break

    # Track follow-ups and escalation posted by Jared
    follow_up_count = 0
    last_followup_date = None
    has_escalation_comment = False
    marker_1 = templates.get("follow_up_1", {}).get("marker", "[CONNECTOR-FOLLOWUP-1]")
    marker_2 = templates.get("follow_up_2", {}).get("marker", "[CONNECTOR-FOLLOWUP-2]")
    marker_esc = templates.get("merge_escalation", {}).get("marker", "[CONNECTOR-ESCALATION]")

    for c in comments:
        if c.get("author", {}).get("accountId", "") != my_account_id:
            continue
        text = extract_text(c.get("body", {}))
        if marker_1 in text:
            follow_up_count = max(follow_up_count, 1)
            d = parse_date(c.get("created", ""))
            if last_followup_date is None or d > last_followup_date:
                last_followup_date = d
        if marker_2 in text:
            follow_up_count = max(follow_up_count, 2)
            d = parse_date(c.get("created", ""))
            if last_followup_date is None or d > last_followup_date:
                last_followup_date = d
        if marker_esc in text:
            has_escalation_comment = True

    return {
        "comments": comments,
        "secondary_approvers": secondary_approvers,
        "secondary_approved": secondary_approved,
        "follow_up_count": follow_up_count,
        "last_followup_date": last_followup_date,
        "has_escalation_comment": has_escalation_comment,
        "action_type": action_type,
        "arun_account": arun_account,
    }


# ── State machine ─────────────────────────────────────────────────────────────────

def determine_state(pr_age, jared_approved, secondary_approved, changes_requested,
                    follow_up_count, last_followup_date, has_escalation, action_type):
    if changes_requested:
        return "changes-requested"

    if action_type == "publish":
        return "publish-request"

    if action_type == "migration":
        return "migration-request"

    if jared_approved and secondary_approved:
        return "ready-to-merge"

    if secondary_approved and not jared_approved:
        return "awaiting-jared"

    # Secondary has not approved — check stale / escalation
    days_since_followup = None
    if last_followup_date:
        if last_followup_date.tzinfo is None:
            last_followup_date = last_followup_date.replace(tzinfo=timezone.utc)
        days_since_followup = (datetime.now(timezone.utc) - last_followup_date).days

    if pr_age >= 21 and follow_up_count >= 2 and not has_escalation:
        return "escalation"

    if pr_age >= 14 and follow_up_count >= 1:
        # Only advance to stale-2 if at least 7 days since last follow-up
        if days_since_followup is None or days_since_followup >= 7:
            return "stale-2"

    if pr_age >= 7 and follow_up_count == 0:
        return "stale-1"

    return "awaiting-secondary" if jared_approved else "awaiting-both"


STATE_DISPLAY = {
    "ready-to-merge":   "✅  READY TO MERGE",
    "awaiting-jared":   "⚠️   AWAITING YOUR GITHUB APPROVAL (secondary already approved in Jira)",
    "awaiting-both":    "⏳  Awaiting both approvals",
    "awaiting-secondary": "⏳  Awaiting secondary approval in Jira",
    "changes-requested": "🔄  Changes requested — waiting for Arun",
    "stale-1":          "📣  STALE ≥7 days — follow-up #1 due",
    "stale-2":          "📣  STALE ≥14 days — follow-up #2 due",
    "escalation":       "🚨  ESCALATION ≥21 days — auto-merge eligible",
    "publish-request":  "📢  PUBLISH REQUEST — Arun asking to publish directly",
    "migration-request": "🔀  MIGRATION REQUEST — article needs to be migrated first",
    "no-jira":          "❓  Jira ticket not found or inaccessible",
}


# ── Comment builders ──────────────────────────────────────────────────────────────

def _fill(template_str, **kwargs):
    for key, val in kwargs.items():
        template_str = template_str.replace("{" + key + "}", str(val))
    return template_str


def _mentions_para(prefix, accounts, suffix):
    """Build a paragraph node: prefix @mention1, @mention2 suffix."""
    nodes = [adf_text(prefix)]
    for i, a in enumerate(accounts):
        nodes.append(adf_mention(a["accountId"], a["displayName"]))
        if i < len(accounts) - 1:
            nodes.append(adf_text(", "))
    nodes.append(adf_text(suffix))
    return nodes


def build_followup_comment(followup_num, secondary_approvers, pr, templates):
    key = f"follow_up_{followup_num}"
    t = templates[key]
    text = _fill(t["intro"], pr_num=pr["number"], pr_title=pr["title"], pr_url=pr["url"])
    cta = _fill(t["cta"], pr_num=pr["number"], pr_title=pr["title"], pr_url=pr["url"])
    para1 = _mentions_para(f"[Follow-up {followup_num} of 2] Hi ", secondary_approvers, f" — {text}")
    para2 = [adf_text(cta)]
    para3 = [adf_text(t["marker"])]
    return adf_doc(para1, para2, para3)


def build_merge_comment(pr, secondary_approvers, arun_account, escalation, templates):
    next_branch, next_monday = next_release_info()
    key = "merge_escalation" if escalation else "merge_standard"
    t = templates[key]

    # Who to @-mention: Arun + secondary approvers
    all_accounts = []
    if arun_account and arun_account.get("accountId"):
        all_accounts.append(arun_account)
    all_accounts.extend(secondary_approvers)

    body = _fill(t["body"], pr_num=pr["number"], next_branch=next_branch, next_monday=next_monday)
    para1 = _mentions_para("Hi ", all_accounts, f" — {body}") if all_accounts else [adf_text(body)]

    paragraphs = [para1]

    if escalation and secondary_approvers:
        note = t.get("secondary_note", "")
        para2 = _mentions_para("Note for ", secondary_approvers, f": {note}")
        paragraphs.append(para2)

    paragraphs.append([adf_text(t["marker"])])
    return adf_doc(*paragraphs)


# ── Actions ───────────────────────────────────────────────────────────────────────

def post_comment(jira_id, adf_body, dry_run=False):
    if dry_run:
        print(f"    [dry-run] Would post comment to {jira_id}")
        return
    jira_post(f"/rest/api/3/issue/{jira_id}/comment", {"body": adf_body})


def setup_conflict_resolution(pr_number, branch_name, dry_run=False):
    """Checkout branch, reverse-merge main. Returns True if resolved cleanly, False if conflicts remain."""
    if dry_run:
        print(f"    [dry-run] Would set up conflict resolution for {branch_name}")
        return False

    print(f"    Fetching origin and checking out {branch_name}...")
    subprocess.run(["git", "fetch", "origin"], capture_output=True)
    r = subprocess.run(["git", "checkout", branch_name], capture_output=True, text=True)
    if r.returncode != 0:
        subprocess.run(["git", "checkout", "-b", branch_name, f"origin/{branch_name}"],
                       capture_output=True, text=True)

    print(f"    Merging origin/main into {branch_name}...")
    r = subprocess.run(["git", "merge", "origin/main"], capture_output=True, text=True)

    if r.returncode == 0:
        # Clean merge — push and retry
        subprocess.run(["git", "push", "origin", branch_name], capture_output=True)
        subprocess.run(["git", "checkout", "main"], capture_output=True)
        result = subprocess.run(
            ["gh", "pr", "merge", str(pr_number), "--repo", REPO, "--merge"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print(f"    ✓ Merged PR #{pr_number} (updated from main, no conflicts)")
            return True
        raise RuntimeError(f"Still failed after main merge: {result.stderr.strip()}")
    else:
        status = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
        conflict_files = [
            line[3:].strip() for line in status.stdout.splitlines()
            if line[:2] in ("UU", "AA", "DD", "AU", "UA", "DU", "UD")
        ]
        print(f"\n    ⚠️  MERGE CONFLICTS in {branch_name}:")
        for f in conflict_files:
            print(f"       - {f}")
        print(f"\n    Branch is checked out locally. Resolve conflicts above, then:")
        print(f"      git add <files> && git commit && git push origin {branch_name}")
        print(f"      python3 scripts/connector-review.py --merge {pr_number}")
        return False


def merge_pr(pr_number, branch_name, dry_run=False):
    """Attempt to merge the PR. Returns True on success, False if conflicts need manual resolution."""
    if dry_run:
        print(f"    [dry-run] Would merge PR #{pr_number}")
        return True

    # Pre-flight mergeability check
    try:
        info = gh_json(["pr", "view", str(pr_number), "--repo", REPO,
                        "--json", "mergeable,mergeStateStatus"])
        if info.get("mergeable") == "CONFLICTING":
            print(f"    ⚠️  PR #{pr_number} has merge conflicts.")
            return setup_conflict_resolution(pr_number, branch_name, dry_run)
    except RuntimeError:
        pass  # proceed and let gh report the error

    result = subprocess.run(
        ["gh", "pr", "merge", str(pr_number), "--repo", REPO, "--merge"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print(f"    ✓ Merged PR #{pr_number}")
        return True

    combined = (result.stderr + result.stdout).lower()
    if "conflict" in combined or "not mergeable" in combined:
        print(f"    ⚠️  PR #{pr_number} has merge conflicts.")
        return setup_conflict_resolution(pr_number, branch_name, dry_run)

    raise RuntimeError(f"Failed to merge PR #{pr_number}: {result.stderr.strip()}")


def approve_pr_on_github(pr_number, body="Approving for merge.", dry_run=False):
    if dry_run:
        print(f"    [dry-run] Would approve PR #{pr_number} on GitHub")
        return
    gh_run(["pr", "review", str(pr_number), "--repo", REPO, "--approve", "--body", body])
    print(f"    ✓ Approved PR #{pr_number} on GitHub")


def close_jira_ticket(jira_id, dry_run=False):
    if dry_run:
        print(f"    [dry-run] Would close {jira_id}")
        return
    data = jira_get(f"/rest/api/3/issue/{jira_id}/transitions")
    transition_id = None
    for t in data.get("transitions", []):
        if t.get("to", {}).get("statusCategory", {}).get("key") == "done":
            transition_id = t["id"]
            break
        if t.get("name", "").lower() in ("done", "closed", "resolved", "close", "resolve"):
            transition_id = t["id"]
    if not transition_id:
        names = [t.get("name") for t in data.get("transitions", [])]
        print(f"    ⚠️  No 'Done' transition found for {jira_id}. Available: {names}")
        print(f"    Please close {jira_id} manually.")
        return
    jira_post(f"/rest/api/3/issue/{jira_id}/transitions", {"transition": {"id": transition_id}})
    print(f"    ✓ Closed {jira_id}")


def do_followup(item, templates, dry_run=False):
    jira_id = item["jira_id"]
    followup_num = item["jira_data"].get("follow_up_count", 0) + 1
    if followup_num > 2:
        print(f"    ℹ️  Already sent 2 follow-ups for {jira_id}. Use --merge to escalate.")
        return
    body = build_followup_comment(followup_num, item["jira_data"]["secondary_approvers"], item["pr"], templates)
    print(f"    Posting follow-up #{followup_num} to {jira_id}...")
    post_comment(jira_id, body, dry_run)
    if not dry_run:
        print(f"    ✓ Follow-up #{followup_num} posted")


def do_merge(item, templates, escalation=False, approve_first=False, dry_run=False):
    pr = item["pr"]
    jira_id = item["jira_id"]
    jira_data = item["jira_data"]
    branch_name = pr["headRefName"]

    if item["gh"].get("changes_requested"):
        print(f"    ⚠️  {jira_id} has CHANGES_REQUESTED on GitHub. Refusing to merge.")
        return

    if (escalation or approve_first) and not item["gh"].get("jared_approved"):
        msg = ("Approving for escalation merge after extended review period."
               if escalation else
               "Approving — secondary reviewer has already verified changes in Jira.")
        print(f"    Approving PR #{pr['number']} on GitHub...")
        approve_pr_on_github(pr["number"], body=msg, dry_run=dry_run)

    print(f"    Merging PR #{pr['number']}...")
    merged = merge_pr(pr["number"], branch_name, dry_run)

    if not merged:
        print(f"    ⚠️  Jira comment and close skipped — resolve conflicts first.")
        return

    print(f"    Posting merge comment to {jira_id}...")
    body = build_merge_comment(pr, jira_data["secondary_approvers"], jira_data.get("arun_account"), escalation, templates)
    post_comment(jira_id, body, dry_run)
    if not dry_run:
        print(f"    ✓ Merge comment posted")

    print(f"    Closing {jira_id}...")
    close_jira_ticket(jira_id, dry_run)


# ── Jira task search (publish / migration requests without a PR) ──────────────────

def find_special_action_tickets(jql, templates):
    """Search Jira for open tickets containing action request phrases."""
    publish_phrases = templates.get("publish_request_phrases", [])
    migration_phrases = templates.get("migration_request_phrases", [])
    all_phrases = publish_phrases + migration_phrases

    # JQL: open connector KB tickets — adjust project key / labels to match your board
    results = []
    for phrase in all_phrases:
        query = f'project = DOMO AND status != Done AND comment ~ "{phrase}" ORDER BY updated DESC'
        try:
            data = jira_request("GET",
                f"/rest/api/3/issue/search?jql={urllib.request.quote(query)}&maxResults=20&fields=summary,status,comment")
            for issue in data.get("issues", []):
                results.append({
                    "key": issue["key"],
                    "summary": issue["fields"]["summary"],
                    "status": issue["fields"]["status"]["name"],
                    "phrase": phrase,
                })
        except RuntimeError:
            pass

    # Deduplicate by ticket key
    seen = set()
    unique = []
    for r in results:
        if r["key"] not in seen:
            seen.add(r["key"])
            unique.append(r)
    return unique


# ── Dashboard ─────────────────────────────────────────────────────────────────────

def print_dashboard(items):
    print("\n" + "=" * 72)
    print("  CONNECTOR PR DASHBOARD")
    print("=" * 72)

    if not items:
        print("  No open connector PRs found.\n")
        return

    for item in items:
        pr = item["pr"]
        state = item["state"]
        jdata = item.get("jira_data", {})
        secondary = jdata.get("secondary_approvers", [])
        secondary_names = ", ".join(a["displayName"] for a in secondary) or "unknown"

        print(f"\n  PR #{pr['number']}: {pr['title'][:58]}")
        print(f"  Jira: {item['jira_id']}  |  Age: {item['pr_age']} days  |  Secondary: {secondary_names}")
        print(f"  GitHub approved: {'✓' if item['gh']['jared_approved'] else '✗'}  "
              f"|  Jira approved: {'✓' if jdata.get('secondary_approved') else '✗'}  "
              f"|  Follow-ups sent: {jdata.get('follow_up_count', 0)}  "
              f"|  Action type: {jdata.get('action_type', 'review')}")
        print(f"  State: {STATE_DISPLAY.get(state, state)}")
        print(f"  URL:   {pr['url']}")

    print("\n" + "=" * 72)


def print_suggested_actions(items):
    actionable = [i for i in items if i["state"] in
                  ("ready-to-merge", "stale-1", "stale-2", "escalation",
                   "awaiting-jared", "publish-request", "migration-request")]
    if not actionable:
        print("\n  Nothing needs immediate action.\n")
        return

    print("\n  Suggested actions:")
    for item in actionable:
        s = item["state"]
        jira_id = item["jira_id"]
        pr = item["pr"]
        if s == "ready-to-merge":
            print(f"    python3 scripts/connector-review.py --merge {jira_id}")
        elif s in ("stale-1", "stale-2"):
            n = item["jira_data"].get("follow_up_count", 0) + 1
            print(f"    python3 scripts/connector-review.py --follow-up {jira_id}  # follow-up #{n}")
        elif s == "escalation":
            print(f"    python3 scripts/connector-review.py --merge {jira_id}  # auto-merge (3 weeks, 2 follow-ups)")
        elif s == "awaiting-jared":
            print(f"    python3 scripts/connector-review.py --merge {jira_id}  # secondary approved in Jira; will auto-approve on GitHub")
        elif s == "publish-request":
            print(f"    Arun requested a direct publish for {jira_id}. Merge via:")
            print(f"      python3 scripts/connector-review.py --merge {jira_id}")
        elif s == "migration-request":
            print(f"    {jira_id} is a migration request. Use the /migrate-html skill, then:")
            print(f"      python3 scripts/connector-review.py --close-ticket {jira_id}")

    print(f"\n  Run all due actions at once:")
    print(f"    python3 scripts/connector-review.py --auto")
    print()


# ── Main ─────────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    auto = "--auto" in args or dry_run

    load_env()
    check_credentials()
    templates = load_templates()

    # Special: search Jira for action tickets without a PR
    if "--find-tasks" in args:
        print("🔍 Searching Jira for publish / migration request tickets...")
        tickets = find_special_action_tickets(None, templates)
        if not tickets:
            print("  None found.")
        for t in tickets:
            print(f"\n  {t['key']}: {t['summary']}")
            print(f"  Status: {t['status']}  |  Matched phrase: \"{t['phrase']}\"")
            print(f"  URL: {JIRA_BASE}/browse/{t['key']}")
        return

    # Close a single ticket (for after migrate-html workflow)
    if "--close-ticket" in args:
        idx = args.index("--close-ticket")
        target = args[idx + 1] if idx + 1 < len(args) else None
        if not target:
            print("Usage: --close-ticket DOMO-123456")
            sys.exit(1)
        print(f"Closing {target}...")
        close_jira_ticket(target, dry_run)
        return

    # Finish the Jira side for a PR that was merged outside the skill
    if "--finish-merged" in args:
        idx = args.index("--finish-merged")
        if idx + 2 >= len(args):
            print("Usage: --finish-merged PR-NUMBER DOMO-123456")
            sys.exit(1)
        pr_num = args[idx + 1]
        jira_id = args[idx + 2]
        jared_jira = my_jira_account()
        jared_jira_id = jared_jira.get("accountId", "")
        print(f"Fetching PR #{pr_num} and Jira ticket {jira_id}...")
        pr = gh_json(["pr", "view", pr_num, "--repo", REPO,
                      "--json", "number,title,headRefName,url,state"])
        jira_data = analyze_jira_ticket(jira_id, jared_jira_id, templates)
        if "error" in jira_data:
            print(f"❌ Could not fetch {jira_id}: {jira_data['error']}")
            sys.exit(1)
        print(f"Posting merge comment to {jira_id}...")
        body = build_merge_comment(
            pr, jira_data.get("secondary_approvers", []),
            jira_data.get("arun_account"), False, templates,
        )
        post_comment(jira_id, body, dry_run)
        if not dry_run:
            print(f"✓ Merge comment posted")
        print(f"Closing {jira_id}...")
        close_jira_ticket(jira_id, dry_run)
        return

    print("🔍 Fetching open connector PRs...")
    jared_login = my_github_login()
    jared_jira = my_jira_account()
    jared_jira_id = jared_jira.get("accountId", "")

    prs = get_open_connector_prs()
    if not prs:
        print("✅ No open connector PRs.\n")
        return

    print(f"   Found {len(prs)} PR(s). Fetching Jira data...\n")

    items = []
    for pr in prs:
        jira_id = extract_jira_id(pr["headRefName"])
        if not jira_id:
            continue
        pr_age = days_since(pr["createdAt"])
        gh_analysis = analyze_github_pr(pr, jared_login)
        jira_data = analyze_jira_ticket(jira_id, jared_jira_id, templates)

        if "error" in jira_data:
            state = "no-jira"
        else:
            state = determine_state(
                pr_age,
                gh_analysis["jared_approved"],
                jira_data.get("secondary_approved", False),
                gh_analysis["changes_requested"],
                jira_data.get("follow_up_count", 0),
                jira_data.get("last_followup_date"),
                jira_data.get("has_escalation_comment", False),
                jira_data.get("action_type", "review"),
            )

        items.append({
            "pr": pr, "jira_id": jira_id, "state": state,
            "pr_age": pr_age, "gh": gh_analysis, "jira_data": jira_data,
        })

    print_dashboard(items)

    # -- Handle specific ticket override flags
    for flag, action in (("--follow-up", "follow-up"), ("--merge", "merge")):
        if flag in args:
            idx = args.index(flag)
            target = args[idx + 1] if idx + 1 < len(args) else None
            if not target:
                print(f"Usage: {flag} DOMO-123456")
                sys.exit(1)
            matches = [i for i in items if i["jira_id"] == target]
            if not matches:
                print(f"No open connector PR found for {target}")
                sys.exit(1)
            item = matches[0]
            if action == "follow-up":
                do_followup(item, templates, dry_run)
            elif action == "merge":
                escalation = item["state"] == "escalation"
                approve_first = item["state"] == "awaiting-jared"
                do_merge(item, templates, escalation=escalation, approve_first=approve_first, dry_run=dry_run)
            return

    # -- Auto mode: act on everything that's due
    if auto:
        print(f"{'[DRY RUN] ' if dry_run else ''}Running automatic actions...\n")
        for item in items:
            s = item["state"]
            jira_id = item["jira_id"]
            pr_num = item["pr"]["number"]
            if s == "ready-to-merge":
                print(f"  {jira_id} (PR #{pr_num}) — merging...")
                do_merge(item, templates, escalation=False, dry_run=dry_run)
            elif s == "awaiting-jared":
                print(f"  {jira_id} (PR #{pr_num}) — secondary approved in Jira, approving + merging...")
                do_merge(item, templates, approve_first=True, dry_run=dry_run)
            elif s == "publish-request":
                print(f"  {jira_id} (PR #{pr_num}) — publish request, merging...")
                do_merge(item, templates, escalation=False, dry_run=dry_run)
            elif s in ("stale-1", "stale-2"):
                n = item["jira_data"].get("follow_up_count", 0) + 1
                print(f"  {jira_id} (PR #{pr_num}) — posting follow-up #{n}...")
                do_followup(item, templates, dry_run)
            elif s == "escalation":
                print(f"  {jira_id} (PR #{pr_num}) — escalation merge (3 weeks, 2 follow-ups)...")
                do_merge(item, templates, escalation=True, dry_run=dry_run)
        print("\nDone.\n")
    else:
        print_suggested_actions(items)


if __name__ == "__main__":
    main()
