#!/usr/bin/env python3
"""Generate redirect CSV from Salesforce Knowledge redirect file.

Articles in Mintlify KB keep their original redirect target.
Articles in DocumentationLocations (internal-only) are excluded entirely.
Remaining articles get a generic fallback redirect to https://domo.com/docs.
"""

import csv
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_DIR = SCRIPT_DIR / "inputcsv"

MINTLIFY_KB = INPUT_DIR / "Mintlify KB.csv"
SALESFORCE_REDIRECTS = INPUT_DIR / "Salesforce Knowledge Redirect File - 1 of 2 Article Versions 1.csv"
DOC_LOCATIONS = INPUT_DIR / "DocumentationLocations.csv"
OUTPUT_FILE = SCRIPT_DIR / "output" / "redirects.csv"

FALLBACK_URL = "https://domo.com/docs"
ARTICLE_ID_RE = re.compile(r"/s/article/([^?/]+)")


def normalize_url(url: str) -> str:
    """Strip www. prefix for comparison."""
    return url.replace("://www.", "://")


def load_mintlify_urls() -> set[str]:
    """Load Mintlify KB URLs into a set, normalized."""
    urls = set()
    with open(MINTLIFY_KB, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            urls.add(normalize_url(row["url"].strip()))
    return urls


def load_excluded_article_ids() -> set[str]:
    """Extract article IDs from DocumentationLocations rows with KB URLs."""
    excluded = set()
    with open(DOC_LOCATIONS, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get("URL of Location", "")
            if "domo-support.domo.com/s/article/" in url:
                match = ARTICLE_ID_RE.search(url)
                if match:
                    excluded.add(match.group(1))
    return excluded


def extract_article_id(url: str) -> str | None:
    """Extract article ID from a redirect target URL."""
    match = ARTICLE_ID_RE.search(url)
    return match.group(1) if match else None


def main():
    mintlify_urls = load_mintlify_urls()
    excluded_ids = load_excluded_article_ids()

    kept = 0
    redirected = 0
    excluded = 0
    total = 0

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(SALESFORCE_REDIRECTS, newline="", encoding="utf-8") as infile, \
         open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            total += 1
            target = row["DESIRED TARGET FOR REDIRECT FILE"].strip()
            article_id = extract_article_id(target)

            # Skip internal-only articles
            if article_id and article_id in excluded_ids:
                excluded += 1
                continue

            # Check if target exists in Mintlify KB
            if normalize_url(target) in mintlify_urls:
                kept += 1
            else:
                row["DESIRED TARGET FOR REDIRECT FILE"] = FALLBACK_URL
                redirected += 1

            writer.writerow(row)

    print(f"Total Salesforce rows:  {total}")
    print(f"Kept (Mintlify match):  {kept}")
    print(f"Redirected (fallback):  {redirected}")
    print(f"Excluded (internal):    {excluded}")
    print(f"Output rows written:    {kept + redirected}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
