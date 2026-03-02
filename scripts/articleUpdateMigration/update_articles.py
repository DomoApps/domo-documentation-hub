#!/usr/bin/env python3
"""
Article Content Update Script (HTML → MDX)

Reads a CSV export from Salesforce Knowledge, converts HTML article bodies
to MDX format, and writes them into existing article files across all
languages (en_US, ja, fr, de, es).

Dependencies: markdownify (pip install markdownify)
"""

import argparse
import csv
import logging
import re
import shutil
import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup, NavigableString, Tag
from markdownify import markdownify

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LANGUAGE_DIR_MAP = {
    "en_US": "s/article",
    "ja": "ja/s/article",
    "fr": "fr/s/article",
    "de": "de/s/article",
    "es": "es/s/article",
}

LANGUAGE_IMAGE_PREFIX = {
    "en_US": "images/kb",
    "ja": "images/kb/ja",
    "fr": "images/kb/fr",
    "de": "images/kb/de",
    "es": "images/kb/es",
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
TITLE_RE = re.compile(r'title:\s*"([^"\n]+)"')
TITLE_SINGLE_RE = re.compile(r"title:\s*'([^'\n]+)'")
TITLE_UNQUOTED_RE = re.compile(r"title:\s*([^\n]+)")


# ---------------------------------------------------------------------------
# HtmlToMdxConverter
# ---------------------------------------------------------------------------


class HtmlToMdxConverter:
    """Converts Salesforce Knowledge HTML to MDX via BS4 pre-processing + markdownify."""

    def __init__(self, language: str = "en_US", default_image_ext: str = "png"):
        self.language = language
        self.default_image_ext = default_image_ext
        self.images_found: List[Dict] = []

    def convert(self, html: str) -> str:
        """Full pipeline: preprocess → markdownify → postprocess."""
        self.images_found = []
        preprocessed = self._preprocess_html(html)
        mdx = self._convert_to_mdx(preprocessed)
        return self._postprocess_mdx(mdx)

    # ----- Step 1: BS4 Pre-processing -----

    def _preprocess_html(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        self._convert_info_boxes(soup)
        self._convert_images(soup)
        self._convert_code_spans(soup)
        self._clean_tables(soup)
        self._cleanup(soup)

        return str(soup)

    # Unique markers that markdownify will pass through as raw text
    # No underscores — markdownify escapes them in markdown
    _NOTE_OPEN = "%%%NOTEOPEN%%%"
    _NOTE_CLOSE = "%%%NOTECLOSE%%%"
    _WARNING_OPEN = "%%%WARNINGOPEN%%%"
    _WARNING_CLOSE = "%%%WARNINGCLOSE%%%"
    _FRAME_OPEN = "%%%FRAMEOPEN%%%"
    _FRAME_CLOSE = "%%%FRAMECLOSE%%%"

    def _convert_info_boxes(self, soup: BeautifulSoup) -> None:
        """Convert info-box note/important divs to text markers."""
        for div in soup.find_all("div", class_="info-box"):
            classes = div.get("class", [])
            if "note" in classes:
                open_marker = self._NOTE_OPEN
                close_marker = self._NOTE_CLOSE
            elif "important" in classes:
                open_marker = self._WARNING_OPEN
                close_marker = self._WARNING_CLOSE
            else:
                continue

            # Extract text content from info-box-content
            content_div = div.find("div", class_="info-box-content")
            if content_div:
                inner_html = content_div.decode_contents()
            else:
                inner_html = div.get_text(strip=True)

            # Replace with markers wrapping the inner HTML
            marker_html = f"{open_marker}{inner_html}{close_marker}"
            div.replace_with(BeautifulSoup(marker_html, "html.parser"))

    def _convert_images(self, soup: BeautifulSoup) -> None:
        """Convert Force.com image URLs to local paths and wrap block images."""
        for img in soup.find_all("img"):
            src = img.get("src", "")
            if "force.com" not in src and "file.force.com" not in src:
                continue

            # Decode HTML entities in URL
            clean_src = src.replace("&amp;", "&")
            parsed = urlparse(clean_src)
            params = parse_qs(parsed.query)

            eid = params.get("eid", [""])[0]
            feoid = params.get("feoid", [""])[0]
            refid = params.get("refid", [""])[0]

            if not (eid and feoid and refid):
                continue

            # Determine extension
            ext = self.default_image_ext
            filename = f"{eid}-{feoid}-{refid}.{ext}"

            # Build local path
            image_prefix = LANGUAGE_IMAGE_PREFIX.get(self.language, "images/kb")
            local_path = f"/{image_prefix}/{filename}"

            # Collect image metadata
            width = img.get("width")
            height = img.get("height")

            # Also check style attribute for dimensions
            style = img.get("style", "")
            if not width and "width" in style:
                w_match = re.search(r"width:\s*([\d.]+)", style)
                if w_match:
                    width = w_match.group(1)
            if not height and "height" in style:
                h_match = re.search(r"height:\s*([\d.]+)", style)
                if h_match:
                    height = h_match.group(1)

            self.images_found.append({
                "url": clean_src,
                "eid": eid,
                "feoid": feoid,
                "refid": refid,
                "width": width,
                "height": height,
                "local_path": local_path,
                "filename": filename,
            })

            # Update img tag
            img["src"] = local_path
            # Remove old width/height attrs — we'll use style
            for attr in ["width", "height", "style"]:
                if attr in img.attrs:
                    del img[attr]

            # Build JSX style for dimensions
            if width or height:
                style_parts = []
                if width:
                    style_parts.append(f"width: {_to_number(width)}")
                if height:
                    style_parts.append(f"height: {_to_number(height)}")
                img["style"] = "{{" + ", ".join(style_parts) + "}}"

            # Convert alt if missing
            if not img.get("alt"):
                img["alt"] = ""

            # Determine if block-level (not inside a table cell or inline)
            parent = img.parent
            is_inline = False
            while parent:
                if parent.name in ("td", "th"):
                    is_inline = True
                    break
                parent = parent.parent

            if not is_inline:
                # Build the final <img .../> string with JSX style
                img_tag = self._build_img_tag(local_path, img.get("alt", ""), width, height)
                # Replace with a single NavigableString marker
                marker = NavigableString(f"{self._FRAME_OPEN}{img_tag}{self._FRAME_CLOSE}")
                img.replace_with(marker)

    @staticmethod
    def _build_img_tag(src: str, alt: str, width: str, height: str) -> str:
        """Build a JSX-compatible <img .../> tag string."""
        parts = [f'<img alt="{alt}" src="{src}"']
        if width or height:
            style_parts = []
            if width:
                style_parts.append(f"width: {_to_number(width)}")
            if height:
                style_parts.append(f"height: {_to_number(height)}")
            parts.append(f' style={{{{{", ".join(style_parts)}}}}}')
        parts.append("/>")
        return "".join(parts)

    def _convert_code_spans(self, soup: BeautifulSoup) -> None:
        """Convert courier/nowiki spans to <code> tags."""
        for span in soup.find_all("span", class_=["mt-font-courier-new", "nowiki"]):
            code_tag = soup.new_tag("code")
            code_tag.string = span.get_text()
            span.replace_with(code_tag)

    def _clean_tables(self, soup: BeautifulSoup) -> None:
        """Clean Salesforce artifacts from tables."""
        for table in soup.find_all("table"):
            # Remove data-aura-rendered-by
            if "data-aura-rendered-by" in table.attrs:
                del table["data-aura-rendered-by"]

            # Clean up inner elements
            for el in table.find_all(True):
                # Remove Salesforce editorial classes
                if el.get("class"):
                    sf_classes = {"s1", "p1", "p2", "p3"}
                    remaining = [c for c in el["class"] if c not in sf_classes]
                    if remaining:
                        el["class"] = remaining
                    else:
                        del el["class"]

                # Remove data-aura-rendered-by from inner elements
                if "data-aura-rendered-by" in el.attrs:
                    del el["data-aura-rendered-by"]

            # Convert img tags inside tables to JSX style format
            for img in table.find_all("img"):
                width = img.get("width")
                height = img.get("height")
                style = img.get("style", "")

                if not width and "width" in style:
                    w_match = re.search(r"width:\s*([\d.]+)", style)
                    if w_match:
                        width = w_match.group(1)
                if not height and "height" in style:
                    h_match = re.search(r"height:\s*([\d.]+)", style)
                    if h_match:
                        height = h_match.group(1)

                # Remove old attrs
                for attr in ["width", "height", "style"]:
                    if attr in img.attrs:
                        del img[attr]

                if width or height:
                    style_parts = []
                    if width:
                        style_parts.append(f"width: {_to_number(width)}")
                    if height:
                        style_parts.append(f"height: {_to_number(height)}")
                    img["style"] = "{{" + ", ".join(style_parts) + "}}"

                if not img.get("alt"):
                    img["alt"] = ""

    def _cleanup(self, soup: BeautifulSoup) -> None:
        """Remove empty spans, decorative wrappers, Salesforce artifacts."""
        # Remove empty spans — collect first to avoid mutation during iteration
        empty_spans = [
            span for span in soup.find_all("span")
            if span.attrs is not None
            and not span.get_text(strip=True)
            and not span.find("img")
        ]
        for span in empty_spans:
            span.decompose()

        # Remove empty divs — collect first
        empty_divs = [
            div for div in soup.find_all("div")
            if div.attrs is not None
            and not div.get_text(strip=True)
            and not div.find(["img", "table"])
        ]
        for div in empty_divs:
            div.decompose()

    # ----- Step 2: markdownify conversion -----

    def _convert_to_mdx(self, preprocessed_html: str) -> str:
        result = markdownify(
            preprocessed_html,
            heading_style="ATX",
            bullets="-",
            strip=["span"],
        )
        return result

    # ----- Step 3: Post-processing -----

    def _postprocess_mdx(self, mdx_text: str) -> str:
        # Replace text markers with MDX components
        mdx_text = re.sub(
            re.escape(self._NOTE_OPEN) + r"(.*?)" + re.escape(self._NOTE_CLOSE),
            lambda m: f"\n<Note>\n{m.group(1).strip()}\n</Note>\n",
            mdx_text,
            flags=re.DOTALL,
        )
        mdx_text = re.sub(
            re.escape(self._WARNING_OPEN) + r"(.*?)" + re.escape(self._WARNING_CLOSE),
            lambda m: f"\n<Warning>\n{m.group(1).strip()}\n</Warning>\n",
            mdx_text,
            flags=re.DOTALL,
        )
        mdx_text = re.sub(
            re.escape(self._FRAME_OPEN) + r"(.*?)" + re.escape(self._FRAME_CLOSE),
            lambda m: f"\n<Frame>{m.group(1).strip()}</Frame>\n",
            mdx_text,
            flags=re.DOTALL,
        )

        # Fix img tags: convert style="{{...}}" back to JSX style={...}
        # markdownify may have escaped or altered the style attribute
        mdx_text = re.sub(
            r'style="\{\{(.*?)\}\}"',
            r"style={{\1}}",
            mdx_text,
        )

        # Ensure self-closing img tags use JSX format
        mdx_text = re.sub(r"<img ([^>]*?)(?<!/)>", r"<img \1/>", mdx_text)

        # Collapse excessive blank lines (3+ → 2)
        mdx_text = re.sub(r"\n{3,}", "\n\n", mdx_text)

        # Clean up whitespace around components
        mdx_text = re.sub(r"\n{3,}(<(?:Note|Warning|Frame))", r"\n\n\1", mdx_text)
        mdx_text = re.sub(r"(</(?:Note|Warning|Frame)>)\n{3,}", r"\1\n\n", mdx_text)

        return mdx_text.strip()


# ---------------------------------------------------------------------------
# ImageReplacer
# ---------------------------------------------------------------------------


class ImageReplacer:
    """Handles copying pre-downloaded images to their destination paths."""

    def __init__(
        self,
        source_dir: Path,
        project_dir: Path,
        match_strategy: str = "eid-feoid-refid",
        manifest_path: Optional[Path] = None,
    ):
        self.source_dir = source_dir
        self.project_dir = project_dir
        self.match_strategy = match_strategy
        self.manifest_path = manifest_path
        self._source_files: Dict[str, Path] = {}
        self._manifest: Dict[str, str] = {}
        self.stats = {
            "copied": 0,
            "skipped_existing": 0,
            "unresolved": 0,
        }
        self.unresolved_urls: List[str] = []

        self._scan_source_dir()
        if match_strategy == "manifest" and manifest_path:
            self._load_manifest()

    def _scan_source_dir(self) -> None:
        """Walk source directory and build lookup of available image files."""
        if not self.source_dir.exists():
            return
        for f in self.source_dir.rglob("*"):
            if f.is_file() and f.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".svg"):
                self._source_files[f.stem.lower()] = f

    def _load_manifest(self) -> None:
        """Load manifest mapping Force.com URLs to local filenames."""
        if not self.manifest_path or not self.manifest_path.exists():
            return
        suffix = self.manifest_path.suffix.lower()
        if suffix == ".json":
            import json
            with open(self.manifest_path, encoding="utf-8") as f:
                self._manifest = json.load(f)
        elif suffix == ".csv":
            with open(self.manifest_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    url = row.get("url", "")
                    filename = row.get("filename", "")
                    if url and filename:
                        self._manifest[url] = filename

    def resolve(self, image_info: Dict) -> Optional[Path]:
        """Resolve a Force.com image to a local source file."""
        if self.match_strategy == "eid-feoid-refid":
            key = f"{image_info['eid']}-{image_info['feoid']}-{image_info['refid']}".lower()
            return self._source_files.get(key)
        elif self.match_strategy == "refid-only":
            key = image_info["refid"].lower()
            return self._source_files.get(key)
        elif self.match_strategy == "manifest":
            filename = self._manifest.get(image_info["url"])
            if filename:
                stem = Path(filename).stem.lower()
                return self._source_files.get(stem)
        return None

    def process_images(
        self,
        images: List[Dict],
        language: str,
        logger: logging.Logger,
    ) -> None:
        """Copy matched images to their destination paths."""
        image_prefix = LANGUAGE_IMAGE_PREFIX.get(language, "images/kb")
        dest_dir = self.project_dir / image_prefix
        dest_dir.mkdir(parents=True, exist_ok=True)

        for img in images:
            source_file = self.resolve(img)
            if source_file is None:
                self.stats["unresolved"] += 1
                self.unresolved_urls.append(img["url"])
                logger.info(
                    "    Image: %s → %s (not found in source)",
                    _short_url(img["url"]),
                    img["local_path"],
                )
                continue

            dest_path = dest_dir / img["filename"]
            if dest_path.exists() and dest_path.stat().st_size == source_file.stat().st_size:
                self.stats["skipped_existing"] += 1
                logger.info(
                    "    Image: %s → %s (already exists)",
                    _short_url(img["url"]),
                    img["local_path"],
                )
                continue

            shutil.copy2(source_file, dest_path)
            self.stats["copied"] += 1
            logger.info(
                "    Image: %s → %s (copied)",
                _short_url(img["url"]),
                img["local_path"],
            )


# ---------------------------------------------------------------------------
# ArticleUpdater
# ---------------------------------------------------------------------------


class ArticleUpdater:
    """Orchestrates CSV reading, dedup, conversion, and file writing."""

    def __init__(
        self,
        project_dir: Path,
        csv_path: Path,
        image_replacer: ImageReplacer,
        dry_run: bool = False,
        only_language: Optional[str] = None,
        only_urlname: Optional[str] = None,
        default_image_ext: str = "png",
        limit: int = 0,
        skip_images: bool = False,
    ):
        self.project_dir = project_dir
        self.csv_path = csv_path
        self.image_replacer = image_replacer
        self.dry_run = dry_run
        self.only_language = only_language
        self.only_urlname = only_urlname
        self.default_image_ext = default_image_ext
        self.limit = limit
        self.skip_images = skip_images

        self.stats = {
            "csv_rows_total": 0,
            "csv_rows_after_dedup": 0,
            "csv_rows_skipped_empty": 0,
            "csv_rows_skipped_language": 0,
            "articles_processed": 0,
            "articles_updated": 0,
            "articles_skipped_no_file": 0,
            "articles_skipped_no_changes": 0,
            "titles_updated": 0,
            "images_found": 0,
            "errors": 0,
        }
        self.errors: List[str] = []

        # Set up logging
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("article_updater")
        logger.setLevel(logging.DEBUG)

        # File handler — full detail
        log_path = self.csv_path.parent / "update_articles.log"
        fh = logging.FileHandler(log_path, mode="w", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        logger.addHandler(fh)

        return logger

    def run(self) -> None:
        """Main entry point."""
        articles = self._read_and_dedup_csv()
        items = list(articles.items())
        if self.limit > 0:
            items = items[: self.limit]
        total = len(items)

        for idx, ((urlname, language), row) in enumerate(items, 1):
            print(f"\r[{idx}/{total}] Processing {urlname} ({language})...", end="", flush=True)
            self._process_article(idx, urlname, language, row)

        print()  # newline after progress
        self.print_report()

    def _read_and_dedup_csv(self) -> Dict[Tuple[str, str], Dict]:
        """Read CSV, group by (URLNAME, LANGUAGE), keep most recent."""
        rows: Dict[Tuple[str, str], Dict] = {}

        try:
            content = self.csv_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = self.csv_path.read_text(encoding="latin-1")

        reader = csv.DictReader(content.splitlines())

        for row in reader:
            self.stats["csv_rows_total"] += 1
            urlname = row.get("URLNAME", "").strip()
            language = row.get("LANGUAGE", "").strip()
            body = row.get("ARTICLE_BODY__C", "").strip()
            last_modified = row.get("LASTMODIFIEDDATE", "")

            if not urlname or not language:
                continue

            # Filter by language/urlname if specified
            if self.only_language and language != self.only_language:
                self.stats["csv_rows_skipped_language"] += 1
                continue
            if self.only_urlname and urlname != self.only_urlname:
                continue

            # Skip unsupported languages
            if language not in LANGUAGE_DIR_MAP:
                if language == "zh_CN":
                    self.logger.warning(
                        "Skipping %s (%s): zh_CN directory does not exist", urlname, language
                    )
                self.stats["csv_rows_skipped_language"] += 1
                continue

            if not body:
                self.stats["csv_rows_skipped_empty"] += 1
                continue

            key = (urlname, language)
            if key in rows:
                # Keep the more recent row (ISO 8601 strings sort lexicographically)
                existing_date = rows[key].get("LASTMODIFIEDDATE", "")
                if last_modified > existing_date:
                    rows[key] = row
            else:
                rows[key] = row

        self.stats["csv_rows_after_dedup"] = len(rows)
        self.logger.info(
            "CSV: %d total rows, %d after dedup, %d skipped empty, %d skipped language",
            self.stats["csv_rows_total"],
            self.stats["csv_rows_after_dedup"],
            self.stats["csv_rows_skipped_empty"],
            self.stats["csv_rows_skipped_language"],
        )
        return rows

    def _process_article(
        self, idx: int, urlname: str, language: str, row: Dict
    ) -> None:
        """Process a single article."""
        self.stats["articles_processed"] += 1
        self.logger.info(
            "Processing article %s (%s) from CSV row %d", urlname, language, idx
        )

        # Resolve MDX file path
        article_dir = LANGUAGE_DIR_MAP.get(language, "")
        mdx_path = self.project_dir / article_dir / f"{urlname}.mdx"

        if not mdx_path.exists():
            self.stats["articles_skipped_no_file"] += 1
            self.logger.warning(
                "Article %s (%s): MDX file not found at %s, skipping",
                urlname, language, mdx_path,
            )
            return

        try:
            # Read existing file
            try:
                existing_content = mdx_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                existing_content = mdx_path.read_text(encoding="latin-1")

            # Extract existing frontmatter and title
            existing_title = self._extract_title(existing_content)
            existing_frontmatter = self._extract_frontmatter(existing_content)

            # CSV title
            csv_title = row.get("TITLE", "").strip()
            title_changed = csv_title and csv_title != existing_title

            if title_changed:
                self.stats["titles_updated"] += 1
                self.logger.info(
                    '  Title: "%s" → "%s"', existing_title, csv_title
                )
            else:
                self.logger.info('  Title: "%s" (unchanged)', existing_title)

            # Convert HTML → MDX
            html_body = row.get("ARTICLE_BODY__C", "")
            self.logger.info(
                "  Converting HTML body (%d chars) → MDX", len(html_body)
            )

            converter = HtmlToMdxConverter(
                language=language,
                default_image_ext=self.default_image_ext,
            )
            mdx_body = converter.convert(html_body)

            # Log images
            self.stats["images_found"] += len(converter.images_found)
            if converter.images_found:
                self.logger.info("  Images found: %d", len(converter.images_found))

            # Process images via ImageReplacer
            if converter.images_found and not self.dry_run and not self.skip_images:
                self.image_replacer.process_images(
                    converter.images_found, language, self.logger
                )

            # Build frontmatter
            final_title = csv_title if title_changed else existing_title
            frontmatter = self._build_frontmatter(existing_frontmatter, final_title)

            # Check if InlineImage import is needed
            has_inline_images = self._needs_inline_image(mdx_body)
            import_line = ""
            if has_inline_images:
                import_line = '\nimport {InlineImage} from "/snippets/InlineImage.mdx";\n'

            # Assemble final content
            final_content = f"{frontmatter}{import_line}\n{mdx_body}\n"

            # Compare with existing
            if final_content.strip() == existing_content.strip():
                self.stats["articles_skipped_no_changes"] += 1
                self.logger.info("  No changes detected, skipping write")
                return

            # Write
            if self.dry_run:
                self.logger.info("  [DRY RUN] Would write %s", mdx_path)
                self.stats["articles_updated"] += 1
            else:
                mdx_path.write_text(final_content, encoding="utf-8")
                self.logger.info("  Writing %s", mdx_path)
                self.stats["articles_updated"] += 1

        except Exception as e:
            self.stats["errors"] += 1
            error_msg = f"Article {urlname} ({language}): Conversion failed - {e}"
            self.errors.append(error_msg)
            self.logger.error(error_msg, exc_info=True)

    def _extract_frontmatter(self, content: str) -> str:
        """Extract raw frontmatter block including --- delimiters."""
        match = FRONTMATTER_RE.match(content)
        if match:
            return match.group(0)
        return ""

    def _extract_title(self, content: str) -> str:
        """Extract title from frontmatter."""
        match = FRONTMATTER_RE.match(content)
        if not match:
            return ""
        yaml_content = match.group(1)

        title_match = TITLE_RE.search(yaml_content)
        if title_match:
            return title_match.group(1).strip()

        title_match = TITLE_SINGLE_RE.search(yaml_content)
        if title_match:
            return title_match.group(1).strip()

        title_match = TITLE_UNQUOTED_RE.search(yaml_content)
        if title_match:
            return title_match.group(1).strip()

        return ""

    def _build_frontmatter(self, existing_frontmatter: str, title: str) -> str:
        """Rebuild frontmatter with potentially updated title."""
        if not existing_frontmatter:
            return f'---\ntitle: "{title}"\n---\n'

        # Replace title in existing frontmatter
        updated = TITLE_RE.sub(f'title: "{title}"', existing_frontmatter)
        if updated == existing_frontmatter:
            # Try single-quoted
            updated = TITLE_SINGLE_RE.sub(f'title: "{title}"', existing_frontmatter)
        if updated == existing_frontmatter:
            # Try unquoted
            updated = TITLE_UNQUOTED_RE.sub(f'title: "{title}"', existing_frontmatter)
        return updated + "\n"

    def _needs_inline_image(self, mdx_body: str) -> bool:
        """Check if the MDX body uses InlineImage component."""
        return "<InlineImage" in mdx_body

    def print_report(self) -> None:
        """Print summary report to console."""
        print()
        print("=" * 60)
        print("Article Update Report")
        print("=" * 60)
        print(f"CSV rows total:            {self.stats['csv_rows_total']}")
        print(f"CSV rows after dedup:      {self.stats['csv_rows_after_dedup']}")
        print(f"CSV rows skipped (empty):  {self.stats['csv_rows_skipped_empty']}")
        print(f"CSV rows skipped (lang):   {self.stats['csv_rows_skipped_language']}")
        print(f"---")
        print(f"Articles processed:        {self.stats['articles_processed']}")
        print(f"Articles updated:          {self.stats['articles_updated']}")
        print(f"Articles skipped (no file):{self.stats['articles_skipped_no_file']}")
        print(f"Articles skipped (no chg): {self.stats['articles_skipped_no_changes']}")
        print(f"Titles updated:            {self.stats['titles_updated']}")
        print(f"---")
        print(f"Images found:              {self.stats['images_found']}")
        print(f"Images copied:             {self.image_replacer.stats['copied']}")
        print(f"Images skipped (existing): {self.image_replacer.stats['skipped_existing']}")
        print(f"Images unresolved:         {self.image_replacer.stats['unresolved']}")
        print(f"---")
        print(f"Errors:                    {self.stats['errors']}")
        if self.dry_run:
            print(f"Mode:                      DRY RUN (no files written)")
        print("=" * 60)

        if self.errors:
            print(f"\nErrors ({len(self.errors)}):")
            for err in self.errors[:20]:
                print(f"  - {err}")
            if len(self.errors) > 20:
                print(f"  ... and {len(self.errors) - 20} more")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _to_number(val: str) -> str:
    """Convert a dimension string to a numeric value for JSX style."""
    val = val.strip().rstrip("px").strip()
    try:
        num = float(val)
        if num == int(num):
            return str(int(num))
        return str(num)
    except ValueError:
        return val


def _short_url(url: str) -> str:
    """Shorten a Force.com URL for logging."""
    match = re.search(r"refid=(\w+)", url)
    if match:
        return f"...refid={match.group(1)}"
    return url[:60]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _find_csv(script_dir: Path) -> Optional[Path]:
    """Auto-detect CSV file in the script directory."""
    csvs = list(script_dir.glob("*.csv"))
    if len(csvs) == 1:
        return csvs[0]
    # Look for the known filename
    known = script_dir / "Knowledge Article Mod 1Aug2025 - 13Feb2026.csv"
    if known.exists():
        return known
    if csvs:
        return csvs[0]
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Update article MDX files from Salesforce Knowledge CSV export"
    )
    parser.add_argument(
        "--project-dir",
        type=str,
        default=".",
        help="Project root directory (default: .)",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Path to CSV file (default: auto-detected in script dir)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files",
    )
    parser.add_argument(
        "--image-dir",
        type=str,
        default=None,
        help="Source directory for pre-downloaded images (default: scripts/articleUpdateMigration/images/)",
    )
    parser.add_argument(
        "--image-ext",
        type=str,
        default="png",
        help="Default image extension (default: png)",
    )
    parser.add_argument(
        "--image-match",
        type=str,
        choices=["eid-feoid-refid", "refid-only", "manifest"],
        default="eid-feoid-refid",
        help="Image matching strategy (default: eid-feoid-refid)",
    )
    parser.add_argument(
        "--manifest",
        type=str,
        default=None,
        help="Path to image manifest file (for --image-match manifest)",
    )
    parser.add_argument(
        "--only-language",
        type=str,
        default=None,
        help="Process only this language (e.g., en_US)",
    )
    parser.add_argument(
        "--only-urlname",
        type=str,
        default=None,
        help="Process only this article URLNAME (for testing)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable DEBUG-level logging",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Process only the first N articles (0 = all)",
    )
    parser.add_argument(
        "--skip-images",
        action="store_true",
        help="Skip image copying (still generates correct paths in MDX)",
    )

    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    script_dir = project_dir / "scripts" / "articleUpdateMigration"

    # Resolve CSV path
    if args.csv:
        csv_path = Path(args.csv)
        if not csv_path.is_absolute():
            csv_path = project_dir / csv_path
    else:
        csv_path = _find_csv(script_dir)

    if not csv_path or not csv_path.exists():
        print(f"Error: CSV file not found. Use --csv to specify the path.")
        return 1

    # Resolve image directory
    if args.image_dir:
        image_dir = Path(args.image_dir)
        if not image_dir.is_absolute():
            image_dir = project_dir / image_dir
    else:
        image_dir = script_dir / "images"

    manifest_path = Path(args.manifest) if args.manifest else None

    print(f"Project dir: {project_dir}")
    print(f"CSV file:    {csv_path}")
    print(f"Image dir:   {image_dir}")
    print(f"Image match: {args.image_match}")
    if args.dry_run:
        print("Mode:        DRY RUN")
    print()

    # Create ImageReplacer
    image_replacer = ImageReplacer(
        source_dir=image_dir,
        project_dir=project_dir,
        match_strategy=args.image_match,
        manifest_path=manifest_path,
    )

    # Create ArticleUpdater and run
    updater = ArticleUpdater(
        project_dir=project_dir,
        csv_path=csv_path,
        image_replacer=image_replacer,
        dry_run=args.dry_run,
        only_language=args.only_language,
        only_urlname=args.only_urlname,
        default_image_ext=args.image_ext,
        limit=args.limit,
        skip_images=args.skip_images,
    )

    if args.verbose:
        updater.logger.setLevel(logging.DEBUG)

    updater.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
