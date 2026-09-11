#!/usr/bin/env python3
"""
Fetch release context from Jira epics + linked Confluence PRDs.

For the product-release-notes skill. Given a CSV of master epics / beta programs
(or an explicit list of Jira keys), this fetches each epic's summary + description
and the body of any linked Confluence PRD, flattens them to readable text, and
writes one Markdown file per epic into an output directory the skill then reads.
Image attachments on the epic and PRD are optionally downloaded so screenshots
found in-context in Jira/Confluence can make it into the article.

Auth: reuses JIRA_EMAIL / JIRA_API_TOKEN from .env (same as connector-review.py).
Both Jira and Confluence Cloud live under https://domoinc.atlassian.net.

Usage:
    # From a CSV that has a column containing Jira keys (DOMO-#####):
    python3 scripts/fetch-jira-context.py --csv "Sept-Prod-Release-Notes-Context/epics.csv" \\
        --out scripts/reports/release-context --download-images

    # From explicit keys:
    python3 scripts/fetch-jira-context.py --keys DOMO-123456,DOMO-234567 --out scripts/reports/release-context

    # Just verify credentials / connectivity:
    python3 scripts/fetch-jira-context.py --test
"""

import argparse
import base64
import csv
import html
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

JIRA_BASE = "https://domoinc.atlassian.net"
KEY_RE = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")
CONF_PAGE_RE = re.compile(r"/pages/(\d+)")
CONF_PAGEID_RE = re.compile(r"[?&]pageId=(\d+)")

# ── Credentials (same pattern as connector-review.py) ───────────────────────────

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
        sys.exit(f"❌ Missing in .env: {', '.join(missing)}")


def _ssl_context():
    ctx = ssl.create_default_context()
    for path in ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt"):
        if os.path.exists(path):
            ctx.load_verify_locations(path)
            break
    return ctx


_SSL = _ssl_context()


def _creds():
    email = os.environ["JIRA_EMAIL"]
    token = os.environ["JIRA_API_TOKEN"]
    return base64.b64encode(f"{email}:{token}".encode()).decode()


def _get(url, raw=False):
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Basic {_creds()}",
            "Accept": "*/*" if raw else "application/json",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, context=_SSL) as r:
        data = r.read()
        return data if raw else (json.loads(data) if data else {})


# ── ADF (Atlassian Document Format) → text ──────────────────────────────────────

def adf_to_text(node, depth=0):
    """Recursively flatten an ADF description node to readable Markdown-ish text.
    Also surfaces link/card URLs inline so Confluence PRD links are discoverable."""
    if node is None:
        return ""
    if isinstance(node, list):
        return "".join(adf_to_text(n, depth) for n in node)

    ntype = node.get("type", "")
    content = node.get("content")

    if ntype == "text":
        text = node.get("text", "")
        for mark in node.get("marks", []):
            if mark.get("type") == "link":
                href = mark.get("attrs", {}).get("href", "")
                if href:
                    text = f"{text} ({href})"
        return text
    if ntype == "hardBreak":
        return "\n"
    if ntype in ("inlineCard", "blockCard", "embedCard"):
        url = node.get("attrs", {}).get("url", "")
        return f"[link: {url}]\n" if url else ""
    if ntype == "mention":
        return "@" + node.get("attrs", {}).get("text", "").lstrip("@")
    if ntype == "paragraph":
        return adf_to_text(content, depth) + "\n\n"
    if ntype == "heading":
        level = node.get("attrs", {}).get("level", 1)
        return "#" * min(level + 1, 6) + " " + adf_to_text(content, depth).strip() + "\n\n"
    if ntype == "bulletList":
        return adf_to_text(content, depth) + "\n"
    if ntype == "orderedList":
        return adf_to_text(content, depth) + "\n"
    if ntype == "listItem":
        inner = adf_to_text(content, depth + 1).strip()
        indent = "  " * depth
        return f"{indent}- {inner}\n"
    if ntype in ("codeBlock",):
        return "```\n" + adf_to_text(content, depth) + "\n```\n\n"
    if ntype in ("table", "tableRow", "tableCell", "tableHeader"):
        inner = adf_to_text(content, depth)
        if ntype == "tableCell" or ntype == "tableHeader":
            return inner.strip() + " | "
        if ntype == "tableRow":
            return inner.rstrip(" |") + "\n"
        return inner + "\n"
    if ntype == "mediaSingle" or ntype == "mediaGroup" or ntype == "media":
        return "[image/attachment in epic]\n"
    # Fallback: recurse into content if present
    return adf_to_text(content, depth) if content else ""


def collect_urls_from_adf(node, out):
    """Walk ADF collecting every href / card url (for Confluence PRD discovery)."""
    if node is None:
        return
    if isinstance(node, list):
        for n in node:
            collect_urls_from_adf(n, out)
        return
    attrs = node.get("attrs", {})
    if "url" in attrs and attrs["url"]:
        out.append(attrs["url"])
    for mark in node.get("marks", []):
        if mark.get("type") == "link":
            href = mark.get("attrs", {}).get("href")
            if href:
                out.append(href)
    collect_urls_from_adf(node.get("content"), out)


# ── HTML (Confluence storage/view) → text ───────────────────────────────────────

def html_to_text(raw):
    if not raw:
        return ""
    text = raw
    text = re.sub(r"(?is)<(script|style).*?</\1>", "", text)
    text = re.sub(r"(?i)<li[^>]*>", "\n- ", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</(p|div|h[1-6]|tr|table|ul|ol)>", "\n", text)
    text = re.sub(r"(?i)<h([1-6])[^>]*>", lambda m: "\n" + "#" * int(m.group(1)) + " ", text)
    text = re.sub(r"(?i)</t[dh]>", " | ", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


# ── Confluence ───────────────────────────────────────────────────────────────────

def confluence_page_ids(urls):
    ids = []
    for u in urls:
        if "/wiki/" not in u and "confluence" not in u.lower():
            continue
        m = CONF_PAGE_RE.search(u) or CONF_PAGEID_RE.search(u)
        if m:
            ids.append(m.group(1))
    # de-dup preserve order
    seen, out = set(), []
    for i in ids:
        if i not in seen:
            seen.add(i)
            out.append(i)
    return out


def fetch_confluence_page(page_id):
    try:
        data = _get(f"{JIRA_BASE}/wiki/rest/api/content/{page_id}"
                    f"?expand=body.storage,body.view,title,space")
    except urllib.error.HTTPError as e:
        return None, f"[Confluence page {page_id}: HTTP {e.code}]"
    title = data.get("title", "")
    body = (data.get("body", {}).get("storage", {}).get("value")
            or data.get("body", {}).get("view", {}).get("value") or "")
    return {"id": page_id, "title": title, "text": html_to_text(body)}, None


def fetch_confluence_attachments(page_id, out_dir, prefix):
    saved = []
    try:
        data = _get(f"{JIRA_BASE}/wiki/rest/api/content/{page_id}/child/attachment?limit=50")
    except urllib.error.HTTPError:
        return saved
    for att in data.get("results", []):
        media = att.get("metadata", {}).get("mediaType", "")
        if not media.startswith("image/"):
            continue
        link = att.get("_links", {}).get("download", "")
        if not link:
            continue
        url = link if link.startswith("http") else f"{JIRA_BASE}/wiki{link}"
        name = re.sub(r"[^A-Za-z0-9._-]", "_", att.get("title", "img"))
        dest = out_dir / f"{prefix}__conf__{name}"
        try:
            dest.write_bytes(_get(url, raw=True))
            saved.append(dest.name)
        except Exception:
            pass
    return saved


# ── Jira issue ────────────────────────────────────────────────────────────────────

def fetch_issue(key):
    fields = "summary,description,status,issuetype,labels,fixVersions,parent,issuelinks,attachment"
    return _get(f"{JIRA_BASE}/rest/api/3/issue/{key}?fields={fields}")


def fetch_remote_links(key):
    try:
        return _get(f"{JIRA_BASE}/rest/api/3/issue/{key}/remotelink")
    except urllib.error.HTTPError:
        return []


def download_issue_images(issue, out_dir, prefix):
    saved = []
    for att in issue.get("fields", {}).get("attachment", []) or []:
        if not str(att.get("mimeType", "")).startswith("image/"):
            continue
        url = att.get("content", "")
        if not url:
            continue
        name = re.sub(r"[^A-Za-z0-9._-]", "_", att.get("filename", "img"))
        dest = out_dir / f"{prefix}__jira__{name}"
        try:
            dest.write_bytes(_get(url, raw=True))
            saved.append(dest.name)
        except Exception:
            pass
    return saved


# Document attachments that may BE a PRD (uploaded to the epic as a file rather
# than linked as a Confluence page). Downloaded so the skill can convert (.docx
# via pandoc) or Read (.pdf) them directly.
DOC_EXTS = (".pdf", ".doc", ".docx", ".ppt", ".pptx", ".txt", ".md", ".rtf", ".odt")


def download_issue_docs(issue, out_dir, prefix):
    saved = []
    for att in issue.get("fields", {}).get("attachment", []) or []:
        fname = att.get("filename", "")
        mime = str(att.get("mimeType", "")).lower()
        is_doc = fname.lower().endswith(DOC_EXTS) or any(
            t in mime for t in ("pdf", "word", "presentation", "text", "document")
        )
        if not is_doc:
            continue
        url = att.get("content", "")
        if not url:
            continue
        name = re.sub(r"[^A-Za-z0-9._-]", "_", fname or "doc")
        dest = out_dir / f"{prefix}__jira__{name}"
        try:
            dest.write_bytes(_get(url, raw=True))
            saved.append(dest.name)
        except Exception:
            pass
    return saved


def page_ids_from_remote_links(remote):
    """Confluence links in Jira Cloud often carry the page id only in the remote
    link's globalId (appId=...&pageId=123456), not in a /pages/123456/ URL."""
    ids = []
    for rl in remote:
        gid = rl.get("globalId", "") or ""
        m = re.search(r"pageId=(\d+)", gid)
        if m:
            ids.append(m.group(1))
    return ids


# ── CSV key extraction ──────────────────────────────────────────────────────────

def keys_from_csv(csv_path):
    """Return list of (key, row_label) preserving order and de-duping keys.
    Auto-detects the column that holds Jira keys."""
    rows = list(csv.reader(Path(csv_path).read_text(encoding="utf-8-sig").splitlines()))
    if not rows:
        return []
    out, seen = [], set()
    for row in rows:
        found = None
        for cell in row:
            m = KEY_RE.search(cell or "")
            if m:
                found = m.group(1)
                break
        if not found:
            continue
        if found in seen:
            continue
        seen.add(found)
        # label = first non-empty cell that isn't the key itself
        label = next((c.strip() for c in row if c and KEY_RE.search(c) is None), "")
        out.append((found, label))
    return out


# ── Main ───────────────────────────────────────────────────────────────────────

def render_epic_md(key, issue, remote_links, prd_pages, images, docs):
    f = issue.get("fields", {})
    summary = f.get("summary", "")
    status = (f.get("status") or {}).get("name", "")
    itype = (f.get("issuetype") or {}).get("name", "")
    labels = ", ".join(f.get("labels", []) or [])
    desc = adf_to_text(f.get("description"))
    lines = [
        f"# {key} — {summary}",
        "",
        f"- **Type:** {itype}",
        f"- **Status:** {status}",
        f"- **Labels:** {labels or '—'}",
        f"- **Jira:** {JIRA_BASE}/browse/{key}",
        "",
        "## Epic description",
        "",
        desc.strip() or "_(no description)_",
        "",
    ]
    if remote_links:
        lines.append("## Linked remote/Confluence links")
        lines.append("")
        for rl in remote_links:
            obj = rl.get("object", {})
            lines.append(f"- {obj.get('title','')}: {obj.get('url','')}")
        lines.append("")
    for pg in prd_pages:
        lines.append(f"## PRD (Confluence): {pg['title']}  \n{JIRA_BASE}/wiki/pages/viewpage.action?pageId={pg['id']}")
        lines.append("")
        lines.append(pg["text"] or "_(empty page body)_")
        lines.append("")
    if docs:
        lines.append("## PRD / document attachments (in scripts output media/)")
        lines.append("")
        lines.append("_These files are attached to the epic and may be the PRD. "
                     "Convert `.docx` with pandoc, or Read `.pdf` directly, before drafting._")
        lines.append("")
        for d in docs:
            lines.append(f"- {d}")
        lines.append("")
    if images:
        lines.append("## Downloaded images (in scripts output media/)")
        lines.append("")
        for im in images:
            lines.append(f"- {im}")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Fetch Jira epic + Confluence PRD context for release notes.")
    ap.add_argument("--csv", help="CSV containing Jira keys (auto-detects the key column)")
    ap.add_argument("--keys", help="Comma-separated Jira keys (alternative to --csv)")
    ap.add_argument("--out", default="scripts/reports/release-context", help="Output directory")
    ap.add_argument("--download-images", action="store_true", help="Also download image attachments from Jira + Confluence")
    ap.add_argument("--test", action="store_true", help="Verify credentials and exit")
    args = ap.parse_args()

    load_env()
    check_credentials()

    if args.test:
        me = _get(f"{JIRA_BASE}/rest/api/3/myself")
        print(f"✅ Jira auth OK as {me.get('displayName')} ({me.get('emailAddress','')})")
        c = _get(f"{JIRA_BASE}/wiki/rest/api/space?limit=1")
        print(f"✅ Confluence auth OK ({len(c.get('results', []))} space visible)")
        return

    if args.csv:
        pairs = keys_from_csv(args.csv)
    elif args.keys:
        pairs = [(k.strip(), "") for k in args.keys.split(",") if k.strip()]
    else:
        sys.exit("Provide --csv or --keys (or --test).")

    if not pairs:
        sys.exit("No Jira keys found. Check the CSV or --keys value.")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    media_dir = out_dir / "media"
    media_dir.mkdir(exist_ok=True)

    manifest = ["# Release context manifest", "", f"Fetched {len(pairs)} epic(s) into `{out_dir}`.", ""]
    print(f"Fetching {len(pairs)} epic(s)…")
    for key, label in pairs:
        try:
            issue = fetch_issue(key)
        except urllib.error.HTTPError as e:
            print(f"  ⚠️  {key}: HTTP {e.code} — skipped")
            manifest.append(f"- ❌ {key} — HTTP {e.code}")
            continue
        except Exception as e:
            print(f"  ⚠️  {key}: {type(e).__name__} — skipped")
            manifest.append(f"- ❌ {key} — {type(e).__name__}")
            continue

        # discover Confluence pages: remote links (object.url + globalId pageId)
        # + urls inside the description
        remote = fetch_remote_links(key)
        urls = [rl.get("object", {}).get("url", "") for rl in remote]
        collect_urls_from_adf(issue.get("fields", {}).get("description"), urls)
        page_ids = confluence_page_ids(urls) + page_ids_from_remote_links(remote)
        # de-dup, preserve order
        seen_pid, page_ids = set(), [p for p in page_ids if not (p in seen_pid or seen_pid.add(p))]

        prd_pages = []
        for pid in page_ids:
            pg, err = fetch_confluence_page(pid)
            if pg:
                prd_pages.append(pg)

        # PRD document attachments on the epic (uploaded file rather than a
        # linked Confluence page) are always downloaded — they're core context.
        docs = download_issue_docs(issue, media_dir, key)

        images = []
        if args.download_images:
            images += download_issue_images(issue, media_dir, key)
            for pid in page_ids:
                images += fetch_confluence_attachments(pid, media_dir, key)

        md = render_epic_md(key, issue, remote, prd_pages, images, docs)
        (out_dir / f"{key}.md").write_text(md, encoding="utf-8")
        summary = issue.get("fields", {}).get("summary", "")
        if prd_pages:
            prd_note = f", {len(prd_pages)} PRD page(s)"
        elif docs:
            prd_note = f", {len(docs)} PRD doc attachment(s)"
        else:
            prd_note = ", no PRD found"
        img_note = f", {len(images)} image(s)" if images else ""
        print(f"  OK  {key}: {summary[:60]}{prd_note}{img_note}")
        manifest.append(f"- OK [{key}]({key}.md) — {summary}{prd_note}{img_note}")

    (out_dir / "_manifest.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    print(f"\nWrote per-epic context to {out_dir}/ (see _manifest.md).")
    print(f"Any PRD doc attachments / images are in {media_dir}/ "
          "(convert .docx with pandoc or Read .pdf; copy chosen screenshots into images/kb/).")


if __name__ == "__main__":
    main()
