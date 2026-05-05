#!/usr/bin/env python3
"""
Converts Salesforce Knowledge HTML article bodies to Domo MDX format.

Full conversion workflow and style/formatting rules are documented in:
    .claude/skills/csv-to-mdx/SKILL.md

That document covers:
  - The complete pipeline (extraction → pre-processing → markdownify → post-processing)
  - Exact MDX component syntax from New-Article-Template.mdx
  - Style rules from Domo-KB-Style-Guide.mdx, split into (A) enforced here
    programmatically and (B) requiring human review after conversion

Handles:
  - Images:     width/height ≤ 40px → inline <img style> syntax (icon)
                larger or unsized   → <Frame>![alt](path)</Frame> (screenshot)
  - Links:      domo-support.domo.com/s/article/… → language-appropriate relative path
                  en_US → /s/article/…
                  ja    → /ja/s/article/…
                  de    → /de/s/article/…
                  fr    → /fr/s/article/…
                  es    → /es/s/article/…
  - ToC removal: lists of in-page anchor links and "Back/Return to top" navigation
                links are stripped (Mintlify auto-generates a ToC from headings);
                orphaned <hr> artifacts (--- lines) left by the removed ToC block
                are also collapsed so only one --- divider remains
  - Callouts:   **Note:**, **Important:**, **Warning:**, **Tip:** paragraphs
                → <Note>, <Warning>, <Tip> MDX components
  - FAQ:        ## FAQ/FAQs heading with bold-question / paragraph-answer pairs
                → <AccordionGroup>/<Accordion> components
  - Frontmatter: YAML ---title--- block added at the top

Content-level style rules from Domo-KB-Style-Guide.mdx that CANNOT be enforced
programmatically (e.g. imperative-mood headings, "select" not "click") are noted
in inline TODO comments when the pattern is detectable but left for human review
otherwise.

Usage as a module:
    from html_to_mdx import html_to_mdx
    mdx = html_to_mdx(html_body, title, image_local_map, language="en_US")

Usage from CLI (for testing a single article):
    python scripts/html_to_mdx.py input.html --title "My Article" [--language ja] [--image-map map.json]
"""

import re
import sys
import json
import argparse
from pathlib import Path

from bs4 import BeautifulSoup

try:
    import markdownify
except ImportError:
    print("ERROR: markdownify required. Run: pip install markdownify")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Images with width OR height at/below this value (px) are treated as inline icons.
# Larger images (or images with no dimension attributes) are treated as screenshots.
INLINE_ICON_MAX_PX = 40

# Base URL for Salesforce-hosted Domo support articles (used to fix internal links)
SF_SUPPORT_BASE = "https://domo-support.domo.com/s/article/"

# Maps CSV language code → repo-relative article URL prefix
# Matches the directory structure: en_US → s/article, ja → ja/s/article, etc.
LANG_ARTICLE_PREFIX: dict[str, str] = {
    "en_US": "/s/article",
    "ja": "/ja/s/article",
    "de": "/de/s/article",
    "fr": "/fr/s/article",
    "es": "/es/s/article",
}

# Callout label → (MDX component name, bold label displayed inside component)
# English labels are matched case-insensitively; Japanese labels are exact-match
# (Japanese has no concept of letter case).
CALLOUT_MAP: dict[str, tuple[str, str]] = {
    # English
    "note": ("Note", "Note"),
    "important": ("Warning", "Important"),
    "warning": ("Warning", "Warning"),
    "caution": ("Warning", "Important"),
    "tip": ("Tip", "Tip"),
    # Japanese — preserve the original label text inside the component
    "注記": ("Note", "注記"),
    "重要": ("Warning", "重要"),
    "ヒント": ("Tip", "ヒント"),
}


# ---------------------------------------------------------------------------
# Pre-processing: strip table-of-contents elements
# ---------------------------------------------------------------------------

_BACK_TO_TOP_RE = re.compile(r"(back|return)\s+to\s+top", re.IGNORECASE)


def _strip_toc_elements(html: str) -> str:
    """
    Remove table-of-contents and in-page navigation elements from HTML before
    conversion.  Mintlify generates a ToC automatically from headings, so
    manually written or linked ToCs violate the style guide.

    Removes:
    1. <ul>/<ol> lists where every <li> contains only in-page anchor links
       (<a href="#...">).  These are ToC jump-link blocks.
    2. Any element whose sole visible content is an <a href="#..."> whose text
       matches "back/return to top" (case-insensitive).
    """
    soup = BeautifulSoup(html, "html.parser")

    # 1. Remove lists where every item is an in-page anchor link
    for list_el in soup.find_all(["ul", "ol"]):
        items = list_el.find_all("li", recursive=False)
        if not items:
            continue
        all_toc_links = all(
            item.find("a", href=lambda h: h and h.startswith("#"))
            and not item.find("a", href=lambda h: h and not h.startswith("#"))
            for item in items
        )
        if all_toc_links:
            list_el.decompose()

    # 2. Remove "back/return to top" links and their containing paragraphs
    for a_tag in soup.find_all("a", href=lambda h: h and h.startswith("#")):
        if _BACK_TO_TOP_RE.search(a_tag.get_text()):
            parent = a_tag.parent
            if parent and parent.name in ("p", "div", "li"):
                if parent.get_text(strip=True) == a_tag.get_text(strip=True):
                    parent.decompose()
                    continue
            a_tag.decompose()

    return str(soup)


# ---------------------------------------------------------------------------
# Custom markdownify converter
# ---------------------------------------------------------------------------

class _DomoMDXConverter(markdownify.MarkdownConverter):
    """
    Extends markdownify.MarkdownConverter with Domo-specific behaviour:

    - <img>  →  placeholder string (restored after conversion via _restore_images)
    - <a>    →  internal Salesforce links rewritten to language-appropriate relative paths
    """

    def __init__(self, article_prefix: str = "/s/article", **kwargs):
        """
        Args:
            article_prefix: The repo-relative URL prefix for internal article links,
                            e.g. "/s/article" for English or "/ja/s/article" for Japanese.
        """
        super().__init__(**kwargs)
        self._article_prefix = article_prefix
        # Populated during conversion; key → {src, alt, width, height}
        self._images: dict[str, dict[str, str]] = {}

    def convert_img(self, el, text, parent_tags):
        """Replace each <img> with a unique placeholder and record its metadata."""
        key = f"__DOMO_IMG_{len(self._images)}__"

        # Context signal: is this image embedded inside a paragraph/list item that
        # also contains meaningful text?  If so it's an inline icon even when no
        # explicit dimensions are present (Salesforce uses class="internal default"
        # for these without width/height attributes).
        context_inline = False
        parent = el.parent
        if parent and parent.name in ("p", "li", "td", "span"):
            alt = (el.attrs.get("alt", "") or "").strip()
            surrounding = parent.get_text(strip=True).replace(alt, "").strip()
            context_inline = len(surrounding) > 20

        self._images[key] = {
            "src": el.attrs.get("src", "") or "",
            "alt": (el.attrs.get("alt", "") or "").strip(),
            "width": str(el.attrs.get("width", "") or ""),
            "height": str(el.attrs.get("height", "") or ""),
            "context_inline": context_inline,
        }
        # Extra newlines ensure the placeholder is on its own paragraph
        return f"\n\n{key}\n\n"

    def convert_a(self, el, text, parent_tags):
        """Rewrite internal Domo KB links to language-appropriate repo-relative paths."""
        href = (el.get("href") or "").strip()
        text = (text or "").strip()

        if not href:
            return text

        # Rewrite Salesforce support article links to repo-relative paths
        if SF_SUPPORT_BASE in href:
            slug = href.split(SF_SUPPORT_BASE, 1)[1]
            # Drop ?language=xx_XX and similar query params
            slug = re.sub(r"[?&]language=[^&\s]*", "", slug).strip("/")
            href = f"{self._article_prefix}/{slug}"

        if not text:
            text = href

        return f"[{text}]({href})"


# ---------------------------------------------------------------------------
# Image MDX helpers
# ---------------------------------------------------------------------------

def _is_inline_icon(width: str, height: str, context_inline: bool = False) -> bool:
    """
    Return True if the image should be rendered as an inline icon.

    Decision priority:
    1. Explicit small dimensions (either ≤ 40px) → inline icon.
    2. Explicit large dimensions (both > 40px)   → screenshot.
    3. No dimensions at all                       → use HTML context:
         True  if the <img> sits inside a paragraph/list with substantial
               surrounding text (Salesforce class="internal default" icons).
         False otherwise (standalone image → screenshot).
    """
    has_width = bool(width)
    has_height = bool(height)

    if has_width or has_height:
        for val in (width, height):
            try:
                if int(val) <= INLINE_ICON_MAX_PX:
                    return True
            except (ValueError, TypeError):
                pass
        return False  # has dimensions but both are large

    # No dimensions — fall back to HTML context
    return context_inline


def _screenshot_mdx(alt: str, img_path: str) -> str:
    """Auto-sizing screenshot block using Mintlify's <Frame> component."""
    return f"<Frame>![{alt or 'Screenshot'}]({img_path})</Frame>"


def _inline_icon_mdx(alt: str, img_path: str, width: str, height: str) -> str:
    """Inline icon using raw <img> with Domo's standard inline style."""
    try:
        w = int(width)
    except (ValueError, TypeError):
        w = 20
    try:
        h = int(height)
    except (ValueError, TypeError):
        h = 20
    return (
        f'<img alt="{alt}" src="{img_path}" '
        f"style={{{{width: {w}, height: {h}, display: 'inline', "
        f"verticalAlign: 'start', margin: '0'}}}}/>"
    )


# ---------------------------------------------------------------------------
# Post-processing: image restoration
# ---------------------------------------------------------------------------

def _restore_images(
    text: str,
    image_registry: dict[str, dict[str, str]],
    image_local_map: dict[str, str],
    image_base_path: str = "/images/kb",
) -> str:
    """
    Replace __DOMO_IMG_N__ placeholders with MDX image components.

    image_local_map maps Salesforce URL → local filename (e.g. '0EMVu000.jpg').
    Both raw (&) and HTML-encoded (&amp;) forms of the URL are tried.

    image_base_path controls the repo-relative directory prefix embedded in the
    MDX src attributes.  Defaults to '/images/kb' (English); localized articles
    pass their language-specific subdirectory, e.g. '/images/kb/ja'.
    """
    for key, info in image_registry.items():
        src = info["src"]
        # Try both URL forms since BeautifulSoup decodes &amp; → & automatically
        local_name = image_local_map.get(src) or image_local_map.get(
            src.replace("&", "&amp;")
        )

        if local_name:
            img_path = f"{image_base_path}/{local_name}"
            if _is_inline_icon(
                info["width"], info["height"], info.get("context_inline", False)
            ):
                img_mdx = _inline_icon_mdx(
                    info["alt"], img_path, info["width"], info["height"]
                )
            else:
                img_mdx = _screenshot_mdx(info["alt"], img_path)
        else:
            # Image wasn't downloaded — leave a comment for manual follow-up
            img_mdx = f"\n<!-- TODO: embed image → {src} -->\n"

        text = text.replace(key, img_mdx)
    return text


# ---------------------------------------------------------------------------
# Post-processing: callout blocks
# ---------------------------------------------------------------------------

def _convert_callouts(text: str) -> str:
    """
    Convert bold-label callout paragraphs to MDX <Note>, <Warning>, <Tip> components.

    Matches patterns like:
        **Note:** Some information here.
        **Important:** Another note spanning
        multiple lines until a blank line.
    """

    def _replace(match: re.Match) -> str:
        raw_label = match.group(1)
        body = match.group(2).strip()
        component, display = CALLOUT_MAP.get(raw_label.lower(), ("Note", raw_label))
        return f"\n<{component}>**{display}:** {body}</{component}>\n"

    # Match **Label:** followed by the rest of the paragraph.
    # English labels are matched case-insensitively (re.IGNORECASE).
    # Japanese labels (注記, 重要, ヒント) are included as literal alternatives;
    # case-insensitivity is harmless for CJK characters.
    pattern = (
        r"\*\*(Note|Important|Warning|Caution|Tip|注記|重要|ヒント):\*\*"  # bold label
        r"\s*"                                                               # optional whitespace
        r"(.+?)"                                                             # callout body (lazy)
        r"(?=\n\n|\n<|\Z)"                                                   # until blank line, tag, or EOF
    )
    return re.sub(pattern, _replace, text, flags=re.IGNORECASE | re.DOTALL)


# ---------------------------------------------------------------------------
# Post-processing: FAQ → AccordionGroup
# ---------------------------------------------------------------------------

def _convert_faq(text: str) -> str:
    """
    Convert a FAQ section into Mintlify's <AccordionGroup>/<Accordion> components.

    Detects headings:  ## FAQ  |  ## FAQs  |  ## Frequently Asked Questions

    Handles two common Salesforce FAQ formats after markdownify conversion:

    Format A – standalone bold lines (most articles):
        **Question text here?**
        Answer paragraph here.

    Format B – numbered list items (connector articles):
        1. **Question text here?**
        Answer paragraph here.

        2. **Another question?**
        Another answer.

    Sections that don't match either pattern are left unchanged for manual review.
    """
    heading_re = re.compile(
        r"^(#{1,3})\s+(FAQ[s]?|Frequently Asked Questions)\s*$",
        re.IGNORECASE | re.MULTILINE,
    )

    match = heading_re.search(text)
    if not match:
        return text

    faq_body_start = match.end()
    heading_level = len(match.group(1))

    # Find the start of the next section at the same or higher level
    next_section_re = re.compile(
        r"^#{1," + str(heading_level) + r"}\s+\S",
        re.MULTILINE,
    )
    next_match = next_section_re.search(text, faq_body_start + 1)
    faq_body_end = next_match.start() if next_match else len(text)
    faq_body = text[faq_body_start:faq_body_end]

    # --- Try Format B first: numbered list bold questions ---
    # Matches: "1. **Question?**\n\nAnswer..."
    numbered_qa_re = re.compile(
        r"\d+\.\s+\*\*(.+?)\*\*\s*\n+"     # N. **Question text**
        r"((?:(?!\d+\.\s+\*\*).)+?)"        # Answer (anything before next numbered item)
        r"(?=\s*\d+\.\s+\*\*|\s*\Z)",
        re.DOTALL,
    )
    qa_pairs = numbered_qa_re.findall(faq_body)

    # --- Try Format A: standalone bold-text questions ---
    if not qa_pairs:
        bold_qa_re = re.compile(
            r"\*\*(.+?)\*\*\s*\n+"             # **Question text**
            r"((?:(?!\*\*.+?\*\*).)+?)"        # Answer (anything before next bold block)
            r"(?=\s*\*\*|\s*\Z)",
            re.DOTALL,
        )
        qa_pairs = bold_qa_re.findall(faq_body)

    if not qa_pairs:
        # Can't detect Q&A structure — leave the section as-is for manual review
        return text

    # Build the AccordionGroup block
    parts = ["\n## FAQ\n\n<AccordionGroup>\n"]
    for question, answer in qa_pairs:
        q = question.strip()
        a = answer.strip()
        if q and a:
            safe_q = q.replace('"', "&quot;")
            parts.append(f'<Accordion title="{safe_q}">\n{a}\n</Accordion>\n')
    parts.append("\n</AccordionGroup>")

    accordion_block = "\n".join(parts)
    return text[: match.start()] + accordion_block + text[faq_body_end:]


# ---------------------------------------------------------------------------
# Main public function
# ---------------------------------------------------------------------------

def html_to_mdx(
    html: str,
    title: str,
    image_local_map: dict[str, str],
    language: str = "en_US",
    image_base_path: str = "/images/kb",
) -> str:
    """
    Convert a Salesforce Knowledge HTML body to a complete Domo MDX file.

    Args:
        html:             Raw HTML from the ARTICLE_BODY__C CSV column.
        title:            Article title (written into YAML frontmatter).
        image_local_map:  {salesforce_url: local_filename} mapping produced by
                          SalesforceImageDownloader.download_all().
        language:         CSV language code ("en_US", "ja", "de", "fr", "es").
                          Controls the article URL prefix used in internal links.
        image_base_path:  Repo-relative directory prefix for image src attributes.
                          Defaults to "/images/kb" (English).  Localized languages
                          pass their subdirectory, e.g. "/images/kb/ja".

    Returns:
        Complete MDX string ready to write to the appropriate language directory.

    Notes:
        - Heading text is preserved from the source; manual review is needed to
          ensure imperative mood (e.g. "Connect X" not "Connecting X").
        - "click" → "select" substitution is not done automatically because the
          context varies; flag with TODO comments if needed.
        - FAQ detection works for the bold-Q/paragraph-A pattern. Unusual FAQ
          layouts are preserved verbatim for manual conversion.
    """
    # Strip ToC jump-link lists and back/return-to-top navigation before conversion
    html = _strip_toc_elements(html)

    article_prefix = LANG_ARTICLE_PREFIX.get(language, "/s/article")
    converter = _DomoMDXConverter(
        article_prefix=article_prefix,
        heading_style="ATX",        # Use ## syntax (not underline style)
        bullets="-",                # Unordered list marker
        strip=["script", "style"],  # Remove script/style tag content entirely
    )

    md = converter.convert(html)

    # Apply post-processing in dependency order
    md = _restore_images(md, converter._images, image_local_map, image_base_path)
    md = _convert_callouts(md)
    md = _convert_faq(md)

    # Strip Salesforce section-divider artifacts (— | —)
    md = re.sub(r"\n*—\s*\|\s*—\n*", "\n\n", md)

    # Remove leading horizontal-rule artifacts — the original HTML often had an <hr>
    # immediately before the ToC block; after ToC stripping that <hr> is left dangling
    # at the top of the content with nothing before it.
    md = re.sub(r"^(---\n\s*)+", "", md)

    # Collapse consecutive horizontal rules into one — the original HTML had an <hr>
    # both before and after the ToC block, leaving two back-to-back --- lines once the
    # ToC list is removed.
    md = re.sub(r"(\n---\n)(\s*\n---\n)+", "\n---\n", md)

    # Normalise whitespace: collapse runs of 3+ blank lines to 2
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = md.strip()

    # Build complete MDX file with YAML frontmatter
    safe_title = title.replace('"', '\\"')
    return f'---\ntitle: "{safe_title}"\n---\n\n{md}\n'


# ---------------------------------------------------------------------------
# CLI entry point (for testing)
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a Salesforce HTML file to Domo MDX (for testing)"
    )
    parser.add_argument("html_file", help="Path to input HTML file")
    parser.add_argument("--title", default="Untitled", help="Article title")
    parser.add_argument(
        "--language",
        default="en_US",
        choices=list(LANG_ARTICLE_PREFIX.keys()),
        help="Language code — controls internal link prefix (default: en_US)",
    )
    parser.add_argument(
        "--image-map",
        help="Path to JSON file mapping {salesforce_url: local_filename}",
    )
    parser.add_argument("--output", help="Output MDX file path (default: stdout)")
    args = parser.parse_args()

    with open(args.html_file, encoding="utf-8") as fh:
        html = fh.read()

    image_map: dict[str, str] = {}
    if args.image_map:
        with open(args.image_map, encoding="utf-8") as fh:
            image_map = json.load(fh)

    result = html_to_mdx(html, args.title, image_map, language=args.language)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(result)
        print(f"Written to {args.output}")
    else:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
