"""
Export Structure Command

Parses docs.json, extracts the full navigation structure, reads page titles
from MDX frontmatter, and outputs a CSV with columns:
tab, group, file_path, title, url

Usage:
    python scripts/docs_cli.py export-structure
    python scripts/docs_cli.py export-structure --base-url https://docs.domo.com
    python scripts/docs_cli.py export-structure --language jp
"""

import csv
import json
import re
from pathlib import Path
from typing import Dict, List


class DocStructureExtractor:
    """Extracts the navigation structure from docs.json and MDX frontmatter."""

    def __init__(self, project_dir: Path, language: str, base_url: str):
        self.project_dir = project_dir
        self.language = language
        self.base_url = base_url.rstrip("/")
        self.rows: List[Dict[str, str]] = []
        self.warnings: List[str] = []
        self.stats: Dict[str, int] = {
            "total_pages": 0,
            "titles_found": 0,
            "titles_missing": 0,
            "files_missing": 0,
            "openapi_refs_skipped": 0,
        }

    def run(self) -> None:
        """Load docs.json and extract the navigation structure."""
        docs_path = self.project_dir / "docs.json"
        if not docs_path.exists():
            raise FileNotFoundError(f"docs.json not found at {docs_path}")

        with open(docs_path, "r", encoding="utf-8") as f:
            docs = json.load(f)

        # Find the matching language block
        lang_block = None
        for lang in docs.get("navigation", {}).get("languages", []):
            if lang.get("language") == self.language:
                lang_block = lang
                break

        if lang_block is None:
            raise ValueError(
                f"Language '{self.language}' not found in docs.json. "
                f"Available: {[l['language'] for l in docs['navigation']['languages']]}"
            )

        for tab in lang_block.get("tabs", []):
            tab_name = tab.get("tab", "")

            if "pages" in tab:
                # Standard pages structure (Welcome, Knowledge Base, Release Notes)
                self._process_pages_recursive(tab_name, tab["pages"], [])

            elif "menu" in tab:
                # Menu structure (Developer Portal)
                for menu_item in tab["menu"]:
                    item_name = menu_item.get("item", "")

                    if "groups" in menu_item:
                        for group in menu_item["groups"]:
                            group_name = group.get("group", "")
                            group_stack = [item_name, group_name]
                            self._process_pages_recursive(
                                tab_name, group["pages"], group_stack
                            )

                    if "pages" in menu_item:
                        self._process_pages_recursive(
                            tab_name, menu_item["pages"], [item_name]
                        )

    def _process_pages_recursive(
        self, tab_name: str, pages: list, group_stack: List[str]
    ) -> None:
        """Recursively process a pages array, handling both string refs and group dicts."""
        for entry in pages:
            if isinstance(entry, str):
                # Skip OpenAPI endpoint references
                if entry.startswith("openapi/"):
                    self.stats["openapi_refs_skipped"] += 1
                    continue

                self.stats["total_pages"] += 1
                # Normalize: strip leading slash so path is relative
                file_path = entry.lstrip("/")
                title = self._extract_title(file_path)
                url = f"{self.base_url}/{file_path}"
                group_path = " > ".join(group_stack)

                self.rows.append(
                    {
                        "tab": tab_name,
                        "group": group_path,
                        "file_path": file_path,
                        "title": title,
                        "url": url,
                    }
                )

            elif isinstance(entry, dict) and "group" in entry:
                nested_stack = group_stack + [entry["group"]]
                root = [entry["root"]] if isinstance(entry.get("root"), str) else []
                self._process_pages_recursive(
                    tab_name, root + entry.get("pages", []), nested_stack
                )

    def _extract_title(self, file_path: str) -> str:
        """Extract the title from MDX frontmatter for a given file path."""
        mdx_path = self.project_dir / f"{file_path}.mdx"

        if not mdx_path.exists():
            self.stats["files_missing"] += 1
            self.warnings.append(f"File not found: {mdx_path}")
            return ""

        try:
            try:
                content = mdx_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                content = mdx_path.read_text(encoding="latin-1")
        except Exception as e:
            self.stats["files_missing"] += 1
            self.warnings.append(f"Error reading {mdx_path}: {e}")
            return ""

        title = self._parse_title_from_frontmatter(content)
        if title:
            self.stats["titles_found"] += 1
        else:
            self.stats["titles_missing"] += 1
            self.warnings.append(f"No title in frontmatter: {file_path}")
        return title

    def _parse_title_from_frontmatter(self, content: str) -> str:
        """Parse the title field from YAML frontmatter."""
        frontmatter_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not frontmatter_match:
            return ""

        yaml_content = frontmatter_match.group(1)

        # Try double-quoted title first (allows apostrophes inside)
        title_match = re.search(r'title:\s*"([^"\n]+)"', yaml_content)
        if title_match:
            return title_match.group(1).strip()

        # Try single-quoted title
        title_match = re.search(r"title:\s*'([^'\n]+)'", yaml_content)
        if title_match:
            return title_match.group(1).strip()

        # Unquoted title
        title_match = re.search(r"title:\s*([^\n]+)", yaml_content)
        if title_match:
            return title_match.group(1).strip()

        return ""

    def write_csv(self, output_path: Path) -> None:
        """Write the extracted rows to a CSV file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["tab", "group", "file_path", "title", "url"]
            )
            writer.writeheader()
            writer.writerows(self.rows)

        print(f"Wrote {len(self.rows)} rows to {output_path}")

    def print_report(self) -> None:
        """Print a summary report."""
        print()
        print("=" * 50)
        print("Documentation Structure Export Report")
        print("=" * 50)
        print(f"Language: {self.language}")
        print(f"Total page references: {self.stats['total_pages']}")
        print(f"Titles found: {self.stats['titles_found']}")
        print(f"Titles missing: {self.stats['titles_missing']}")
        print(f"Files not found: {self.stats['files_missing']}")
        print(f"OpenAPI refs skipped: {self.stats['openapi_refs_skipped']}")
        print(f"CSV rows written: {len(self.rows)}")
        print("=" * 50)

        if self.warnings:
            print(f"\nWarnings ({len(self.warnings)}):")
            for warning in self.warnings[:20]:
                print(f"  - {warning}")
            if len(self.warnings) > 20:
                print(f"  ... and {len(self.warnings) - 20} more")


def register(subparsers) -> None:
    """Register the export subcommand."""
    parser = subparsers.add_parser(
        "export",
        help=(
            "Export docs.json navigation structure to CSV. "
            "Options: --language, --base-url, --output, --project-dir"
        ),
        description=(
            "Parses docs.json, extracts the full navigation structure, "
            "reads page titles from MDX frontmatter, and outputs a CSV."
        ),
    )
    parser.add_argument(
        "--project-dir",
        type=str,
        default=".",
        help="Project root containing docs.json (default: .)",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="en",
        help="Language code to extract (default: en)",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default="https://docs.domo.com",
        help="Base URL for page URLs (default: https://docs.domo.com)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="scripts/reports/doc_structure.csv",
        help="Output CSV path (default: scripts/reports/doc_structure.csv)",
    )
    parser.set_defaults(func=run)


def run(args) -> int:
    """Execute the export-structure command."""
    project_dir = Path(args.project_dir).resolve()
    output_path = Path(args.output)

    # If output is relative, resolve it relative to project_dir
    if not output_path.is_absolute():
        output_path = project_dir / output_path

    extractor = DocStructureExtractor(
        project_dir=project_dir,
        language=args.language,
        base_url=args.base_url,
    )

    extractor.run()
    extractor.write_csv(output_path)
    extractor.print_report()

    return 0
