#!/usr/bin/env python3
"""
Downloads images from Salesforce Knowledge using a session ID (SID) cookie.

Salesforce image URLs use this pattern:
    https://domo.file.force.com/servlet/rtaImage?eid=ka0Vu...&feoid=00N5w...&refid=0EMVu...

The `refid` parameter is used as the local filename (e.g. 0EMVu00000UmLth.jpg),
matching the naming convention already in use in /images/kb/.

Images are language-agnostic — the same image file is referenced by all language
versions of an article.  A single SalesforceImageDownloader instance is shared
across all languages in update_kb_articles.py so each unique image is only
downloaded once, regardless of how many language articles reference it.

Usage as a module:
    from image_downloader import SalesforceImageDownloader
    downloader = SalesforceImageDownloader(sid='YOUR_SID')
    image_local_map = downloader.download_all(list_of_urls)

Usage from CLI:
    python scripts/image_downloader.py --sid YOUR_SID --url "https://domo.file.force.com/..."
    python scripts/image_downloader.py --sid YOUR_SID --url-file urls.txt
"""

import sys
import re
import argparse
import hashlib
from pathlib import Path
from urllib.parse import urlparse, parse_qs

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Run: pip install requests")
    sys.exit(1)

# Default output directory relative to this script's repo root
DEFAULT_IMAGES_DIR = Path(__file__).parent.parent / "images" / "kb"

# MIME type → file extension
MIME_TO_EXT: dict[str, str] = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/svg+xml": ".svg",
    "image/webp": ".webp",
    "image/bmp": ".bmp",
    "image/tiff": ".tiff",
}


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def extract_refid(url: str) -> str | None:
    """Return the refid query parameter from a Salesforce image URL, or None."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    refs = params.get("refid", [])
    return refs[0] if refs else None


def get_extension(content_type: str) -> str:
    """Derive a file extension from a Content-Type header value."""
    mime = content_type.split(";")[0].strip().lower()
    return MIME_TO_EXT.get(mime, ".jpg")


def stable_filename(url: str, content_type: str) -> str:
    """
    Generate a stable local filename for a Salesforce image URL.
    Prefers the refid as the base name (matches existing /images/kb/ convention).
    Falls back to an MD5 hash of the URL.
    """
    refid = extract_refid(url)
    ext = get_extension(content_type)
    if refid:
        return f"{refid}{ext}"
    url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
    return f"img_{url_hash}{ext}"


# ---------------------------------------------------------------------------
# Downloader class
# ---------------------------------------------------------------------------

class SalesforceImageDownloader:
    """
    Downloads images from Salesforce using SID cookie authentication.

    Deduplicates requests: if an image with the same refid already exists
    locally, it is reused without a network request.
    """

    def __init__(self, sid: str, images_dir: Path = DEFAULT_IMAGES_DIR):
        """
        Args:
            sid:        Salesforce session ID (copy from browser devtools → cookies → 'sid').
            images_dir: Directory where images are saved. Created if it doesn't exist.
        """
        self.sid = sid
        self.images_dir = Path(images_dir)
        self.images_dir.mkdir(parents=True, exist_ok=True)

        self._session = requests.Session()
        self._session.headers.update(
            {
                "Cookie": f"sid={sid}",
                "User-Agent": "Mozilla/5.0 (compatible; DomoDocsBot/1.0)",
            }
        )

        # Internal tracking
        self._url_to_filename: dict[str, str] = {}  # canonicalised url → local filename
        self._n_downloaded = 0
        self._n_skipped = 0
        self._failures: list[tuple[str, str]] = []  # (url, error message)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def download(self, url: str) -> str | None:
        """
        Download one image. Returns the local filename on success, None on failure.

        Skips the network request if:
        - The URL was already processed in this session.
        - A file matching the refid already exists on disk.
        """
        canonical = url.strip()

        if canonical in self._url_to_filename:
            return self._url_to_filename[canonical]

        # Check if already on disk (previous run)
        refid = extract_refid(canonical)
        if refid:
            existing = list(self.images_dir.glob(f"{refid}.*"))
            if existing:
                filename = existing[0].name
                self._url_to_filename[canonical] = filename
                self._n_skipped += 1
                return filename

        # Fetch from Salesforce
        try:
            resp = self._session.get(canonical, timeout=30, allow_redirects=True)
            resp.raise_for_status()

            content_type = resp.headers.get("Content-Type", "image/jpeg")
            if "text/html" in content_type:
                self._failures.append((canonical, "Got HTML response instead of image — SID may be invalid for domo.file.force.com (visit a file URL in your browser first, then copy the sid cookie from that domain)"))
                return None
            filename = stable_filename(canonical, content_type)
            filepath = self.images_dir / filename

            with open(filepath, "wb") as fh:
                fh.write(resp.content)

            self._url_to_filename[canonical] = filename
            self._n_downloaded += 1
            return filename

        except Exception as exc:
            self._failures.append((canonical, str(exc)))
            return None

    def download_all(self, urls: list[str]) -> dict[str, str]:
        """
        Download a list of image URLs.

        Returns:
            Mapping of {url: local_filename} for every successfully downloaded image.
            URLs that failed are omitted.
        """
        result: dict[str, str] = {}
        for url in urls:
            local = self.download(url)
            if local:
                result[url] = local
        return result

    def report(self) -> None:
        """Print a summary of activity to stdout."""
        total = self._n_downloaded + self._n_skipped + len(self._failures)
        print(
            f"  Images: {total} total | "
            f"{self._n_downloaded} downloaded, "
            f"{self._n_skipped} already on disk, "
            f"{len(self._failures)} failed"
        )
        if self._failures:
            print("  Failed downloads:")
            for url, err in self._failures[:10]:
                print(f"    {url[:90]}")
                print(f"      → {err}")
            if len(self._failures) > 10:
                print(f"    ... and {len(self._failures) - 10} more")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download Salesforce images using a session ID (SID) cookie"
    )
    parser.add_argument("--sid", required=True, help="Salesforce session ID")
    parser.add_argument("--url", help="Single image URL to download")
    parser.add_argument(
        "--url-file",
        help="Path to a text file with one Salesforce image URL per line",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_IMAGES_DIR),
        help=f"Directory to save images (default: {DEFAULT_IMAGES_DIR})",
    )
    args = parser.parse_args()

    urls: list[str] = []
    if args.url:
        urls.append(args.url)
    if args.url_file:
        with open(args.url_file, encoding="utf-8") as fh:
            urls.extend(line.strip() for line in fh if line.strip())

    if not urls:
        parser.error("Provide at least one of --url or --url-file")

    downloader = SalesforceImageDownloader(args.sid, Path(args.output_dir))
    result = downloader.download_all(urls)
    downloader.report()

    if result:
        print("\nDownloaded files:")
        for url, name in result.items():
            print(f"  {name:<40}  ←  {url[:80]}")


if __name__ == "__main__":
    main()
