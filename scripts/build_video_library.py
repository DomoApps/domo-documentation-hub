#!/usr/bin/env python3
"""Rebuild the Domo Video Library directory article from a Domo DataSet.

Pulls video rows from a Domo DataSet via the Domo API, downloads each
thumbnail into images/kb/, and regenerates s/article/Domo-Video-Library.mdx
as a flat, alphabetical CardGroup. Output is deterministic, so a run with
unchanged data produces no git diff.

Run locally or from CI. Required environment variables:

  DOMO_CLIENT_ID         Domo OAuth client id   (developer.domo.com, scope "data")
  DOMO_CLIENT_SECRET     Domo OAuth client secret
  DOMO_VIDEO_DATASET_ID  GUID of the DataSet backing the library

Optional:

  DOMO_API_HOST          API host (default: api.domo.com)

The DataSet must expose these columns (header row, any order):
  description, title, tags, thumbnail_url, date_added, share_url
(`tags` is read but not currently rendered.)
"""

import base64
import csv
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime

# --- Repo-relative paths (script lives in scripts/) ---
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLE_PATH = os.path.join(REPO_ROOT, "s", "article", "Domo-Video-Library.mdx")
IMAGES_DIR = os.path.join(REPO_ROOT, "images", "kb")
IMAGE_PREFIX = "microlearning-"  # keeps these files namespaced for safe cleanup

# --- Fixed page copy (kept in sync with the published article) ---
INTRO_EMBED_URL = "https://embed.domo.com/cards/2W9VW"
EXCERPT = (
    "Browse the Domo Video Library — a searchable directory of short videos "
    "covering Domo features and workflows, from AI and Magic ETL to dashboards, "
    "governance, and pro-code apps. Each entry links to the full video."
)
INTRO = (
    f"The [Domo Video Library]({INTRO_EMBED_URL}) is a searchable directory of "
    "focused videos that walk you through specific Domo features and workflows. "
    "Each card below shows a preview and a brief summary of what the video covers. "
    "Select any card to open and watch the full microlearning video."
)
REQUIRED_COLUMNS = {"description", "title", "tags", "thumbnail_url", "date_added", "share_url"}


def log(msg):
    print(msg, flush=True)


# --------------------------------------------------------------------------- #
# Domo API
# --------------------------------------------------------------------------- #
def get_access_token(host, client_id, client_secret):
    creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    url = f"https://{host}/oauth/token?" + urllib.parse.urlencode(
        {"grant_type": "client_credentials", "scope": "data"}
    )
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Basic {creds}")
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.load(resp)
    token = body.get("access_token")
    if not token:
        raise RuntimeError(f"No access_token in Domo OAuth response: {body}")
    return token


def export_dataset_csv(host, token, dataset_id):
    url = f"https://{host}/v1/datasets/{dataset_id}/data?includeHeader=true"
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "text/csv")
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read().decode("utf-8-sig")


def load_rows():
    host = os.environ.get("DOMO_API_HOST") or "api.domo.com"
    client_id = os.environ.get("DOMO_CLIENT_ID")
    client_secret = os.environ.get("DOMO_CLIENT_SECRET")
    dataset_id = os.environ.get("DOMO_VIDEO_DATASET_ID")
    missing = [
        n
        for n, v in [
            ("DOMO_CLIENT_ID", client_id),
            ("DOMO_CLIENT_SECRET", client_secret),
            ("DOMO_VIDEO_DATASET_ID", dataset_id),
        ]
        if not v
    ]
    if missing:
        raise SystemExit(f"Missing required env var(s): {', '.join(missing)}")

    log(f"Authenticating to Domo ({host}) ...")
    token = get_access_token(host, client_id, client_secret)
    log(f"Exporting DataSet {dataset_id} ...")
    csv_text = export_dataset_csv(host, token, dataset_id)

    reader = csv.DictReader(io.StringIO(csv_text))
    cols = set(reader.fieldnames or [])
    if not REQUIRED_COLUMNS.issubset(cols):
        raise SystemExit(
            "DataSet is missing required columns. "
            f"Expected superset of {sorted(REQUIRED_COLUMNS)}; got {sorted(cols)}."
        )
    rows = [r for r in reader if (r.get("title") or "").strip()]
    log(f"Loaded {len(rows)} video rows.")
    return rows


# --------------------------------------------------------------------------- #
# Rendering helpers (must match the published article's formatting exactly)
# --------------------------------------------------------------------------- #
def slugify(title):
    s = title.lower().replace("&", " and ")
    s = re.sub(r"[''']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def image_filename(title, thumbnail_url):
    ext = "jpg" if re.search(r"\.jpe?g(\?|$)", thumbnail_url.lower()) else "png"
    return f"{IMAGE_PREFIX}{slugify(title)}.{ext}"


def fmt_added_date(raw):
    raw = (raw or "").strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", raw)
    if not m:
        return None
    try:
        dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None
    return dt.strftime("%B %-d, %Y")


def fmt_body(desc):
    """2-space-indented MDX card body; converts bullet (•) lines to markdown lists."""
    out = []
    for raw in (desc or "").replace("\r\n", "\n").split("\n"):
        s = raw.strip()
        if s == "":
            if out and out[-1] != "":
                out.append("")
            continue
        if s.startswith("•"):
            if out and out[-1] != "" and not out[-1].startswith("  - "):
                out.append("")
            out.append("  - " + s.lstrip("•").strip())
        else:
            if out and out[-1] != "":
                out.append("")
            out.append("  " + s)
    while out and out[0] == "":
        out.pop(0)
    while out and out[-1] == "":
        out.pop()
    return out


def download_thumbnail(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = resp.read()
    if len(data) < 256:
        raise RuntimeError(f"Suspiciously small download ({len(data)} bytes) from {url}")
    if not (data.startswith(b"\x89PNG\r\n\x1a\n") or data.startswith(b"\xff\xd8\xff")):
        raise RuntimeError(f"Downloaded data is not a PNG/JPEG: {url}")
    with open(dest, "wb") as fh:
        fh.write(data)


def render_article(rows):
    """Pure render: rows -> full MDX string. No I/O, so it is unit-testable."""
    ordered = sorted(rows, key=lambda r: r["title"].strip().lower())
    lines = [
        "---",
        'title: "Domo Video Library"',
        f'excerpt: "{EXCERPT}"',
        "---",
        "",
        INTRO,
        "",
        "<CardGroup cols={3}>",
        "",
    ]
    for r in ordered:
        title = r["title"].strip()
        fname = image_filename(title, (r.get("thumbnail_url") or "").strip())
        share_url = (r.get("share_url") or "").strip()
        title_attr = title.replace('"', "'")
        lines.append(f'<Card title="{title_attr}" img="/images/kb/{fname}" href="{share_url}">')
        lines.extend(fmt_body(r.get("description", "")))
        added = fmt_added_date(r.get("date_added"))
        if added:
            lines.append("")
            lines.append(f"  *Added {added}*")
        lines.append("</Card>")
        lines.append("")
    lines.append("</CardGroup>")
    return "\n".join(lines).rstrip() + "\n"


def build():
    rows = load_rows()
    os.makedirs(IMAGES_DIR, exist_ok=True)

    failures = []
    referenced = set()
    for r in rows:
        title = r["title"].strip()
        thumb_url = (r["thumbnail_url"] or "").strip()
        fname = image_filename(title, thumb_url)
        referenced.add(fname)
        if not thumb_url:
            continue
        dest = os.path.join(IMAGES_DIR, fname)
        try:
            download_thumbnail(thumb_url, dest)
        except Exception as exc:  # noqa: BLE001 — keep going, report at end
            failures.append((title, str(exc)))
            if not os.path.exists(dest):
                log(f"  ! thumbnail failed and no cached copy: {title} ({exc})")

    content = render_article(rows)
    with open(ARTICLE_PATH, "w") as fh:
        fh.write(content)
    log(f"Wrote {os.path.relpath(ARTICLE_PATH, REPO_ROOT)} ({len(rows)} cards).")

    # Remove thumbnails for videos no longer in the DataSet (only our namespace).
    removed = 0
    for existing in os.listdir(IMAGES_DIR):
        if existing.startswith(IMAGE_PREFIX) and existing not in referenced:
            os.remove(os.path.join(IMAGES_DIR, existing))
            removed += 1
    if removed:
        log(f"Removed {removed} orphaned thumbnail(s).")

    if failures:
        log(f"WARNING: {len(failures)} thumbnail download(s) failed:")
        for title, err in failures:
            log(f"  - {title}: {err}")

    return len(rows)


if __name__ == "__main__":
    try:
        build()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        log(f"ERROR: {exc}")
        sys.exit(1)
