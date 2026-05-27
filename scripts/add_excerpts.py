#!/usr/bin/env python3
"""
Backfill `excerpt:` frontmatter fields into every MDX article in a language directory.

For each article missing the `excerpt:` field, this script reads the title and the
opening of the body, asks Claude Haiku to produce a one-sentence summary in the
target language, and writes the result into the file's YAML frontmatter directly
below the `title:` line.

Usage:
    python scripts/add_excerpts.py --language en [--dry-run] [--limit N] [--concurrency N]

Languages and target directories:
    en  ->  s/article/
    ja  ->  ja/s/article/
    fr  ->  fr/s/article/
    es  ->  es/s/article/
    de  ->  de/s/article/

Requires the ANTHROPIC_API_KEY environment variable.
Files that already have an `excerpt:` line are skipped, so reruns are safe.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from anthropic import AsyncAnthropic
except ImportError:
    sys.stderr.write("ERROR: anthropic SDK not installed. Run: pip install anthropic\n")
    sys.exit(1)


def load_dotenv(path: Path) -> None:
    """Minimal .env loader: populates os.environ from KEY=value lines."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_dotenv(Path(".env"))


LANGUAGE_CONFIG = {
    "en": {"dir": "s/article", "name": "English"},
    "ja": {"dir": "ja/s/article", "name": "Japanese"},
    "fr": {"dir": "fr/s/article", "name": "French"},
    "es": {"dir": "es/s/article", "name": "Spanish"},
    "de": {"dir": "de/s/article", "name": "German"},
}

MODEL = "claude-haiku-4-5-20251001"
BODY_SNIPPET_CHARS = 1200
MAX_RETRIES = 3
FAILURES_LOG = Path("scripts/add_excerpts.failures.json")


@dataclass
class Article:
    path: Path
    pre_lines: list[str]
    frontmatter_lines: list[str]
    post_lines: list[str]
    title: str
    title_line_index: int
    body: str


def parse_article(path: Path) -> Optional[Article]:
    """Split an MDX file into frontmatter and body. Returns None if unparseable or already has excerpt."""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip() != "---":
        return None

    end_index = None
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            end_index = i
            break
    if end_index is None:
        return None

    frontmatter_lines = lines[1:end_index]

    title_line_index = None
    for i, line in enumerate(frontmatter_lines):
        if re.match(r"^excerpt\s*:", line):
            return None
        if re.match(r"^title\s*:", line) and title_line_index is None:
            title_line_index = i
    if title_line_index is None:
        return None

    title_match = re.match(r'^title\s*:\s*"?(.*?)"?\s*$', frontmatter_lines[title_line_index])
    if not title_match:
        return None
    title = title_match.group(1).strip()
    if not title:
        return None

    body = "".join(lines[end_index + 1 :]).strip()

    return Article(
        path=path,
        pre_lines=lines[:1],
        frontmatter_lines=frontmatter_lines,
        post_lines=lines[end_index:],
        title=title,
        title_line_index=title_line_index,
        body=body,
    )


def clean_body_snippet(body: str, max_chars: int = BODY_SNIPPET_CHARS) -> str:
    """Strip MDX comments and grab the opening of the body for context."""
    body = re.sub(r"\{/\*.*?\*/\}", "", body, flags=re.DOTALL)
    body = body.strip()
    if len(body) <= max_chars:
        return body
    truncated = body[:max_chars]
    last_space = truncated.rfind(" ")
    if last_space > max_chars * 0.8:
        truncated = truncated[:last_space]
    return truncated + " [...]"


def yaml_escape(value: str) -> str:
    """Wrap a value in double quotes for YAML, escaping backslashes and quotes."""
    cleaned = value.strip().strip('"').strip("'")
    cleaned = re.sub(r"\s+", " ", cleaned)
    escaped = cleaned.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_prompt(title: str, body_snippet: str, language_name: str) -> str:
    return (
        f"You are summarizing a Domo Knowledge Base article.\n\n"
        f"Write ONE concise sentence (under 150 characters) that captures what the article "
        f"covers — the features, tasks, or concepts the reader learns to use. Match the "
        f"terminology used in the article. Do not start with phrases like \"This article\" "
        f"or \"Learn how to\".\n\n"
        f"The sentence MUST be written in {language_name}.\n\n"
        f"Output ONLY the sentence. Do not include quotes, a prefix, or any explanation. "
        f"End with a single period.\n\n"
        f"Title: {title}\n\n"
        f"Article opening:\n{body_snippet}"
    )


async def generate_excerpt(
    client: AsyncAnthropic,
    article: Article,
    language_name: str,
    semaphore: asyncio.Semaphore,
) -> tuple[Article, Optional[str], Optional[str]]:
    """Call Claude to generate an excerpt. Returns (article, excerpt, error)."""
    body_snippet = clean_body_snippet(article.body)
    prompt = build_prompt(article.title, body_snippet, language_name)

    last_error = None
    for attempt in range(MAX_RETRIES):
        async with semaphore:
            try:
                response = await client.messages.create(
                    model=MODEL,
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}],
                )
                text = response.content[0].text.strip()
                text = text.strip().strip('"').strip("'").strip()
                if not text:
                    last_error = "empty response"
                    continue
                return article, text, None
            except Exception as e:
                last_error = f"{type(e).__name__}: {e}"
                await asyncio.sleep(2 ** attempt)
    return article, None, last_error


def write_excerpt(article: Article, excerpt: str) -> None:
    """Insert `excerpt: "..."` directly under the title line and write the file back."""
    indent_match = re.match(r"^(\s*)", article.frontmatter_lines[article.title_line_index])
    indent = indent_match.group(1) if indent_match else ""
    excerpt_line = f"{indent}excerpt: {yaml_escape(excerpt)}\n"

    new_frontmatter = (
        article.frontmatter_lines[: article.title_line_index + 1]
        + [excerpt_line]
        + article.frontmatter_lines[article.title_line_index + 1 :]
    )

    new_text = "".join(article.pre_lines + new_frontmatter + article.post_lines)
    article.path.write_text(new_text, encoding="utf-8")


async def run(language: str, dry_run: bool, limit: Optional[int], concurrency: int) -> int:
    config = LANGUAGE_CONFIG[language]
    article_dir = Path(config["dir"])
    if not article_dir.is_dir():
        sys.stderr.write(f"ERROR: directory {article_dir} not found\n")
        return 1

    all_files = sorted(article_dir.glob("*.mdx"))
    candidates: list[Article] = []
    skipped_existing = 0
    skipped_unparseable = 0
    for path in all_files:
        article = parse_article(path)
        if article is None:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"^excerpt\s*:", text, re.MULTILINE):
                skipped_existing += 1
            else:
                skipped_unparseable += 1
            continue
        candidates.append(article)

    if limit:
        candidates = candidates[:limit]

    print(f"Language: {language} ({config['name']})")
    print(f"Directory: {article_dir}")
    print(f"Total .mdx files: {len(all_files)}")
    print(f"Already have excerpt: {skipped_existing}")
    print(f"Unparseable / no title: {skipped_unparseable}")
    print(f"Articles to process: {len(candidates)}")
    if dry_run:
        print("\n[DRY RUN] No API calls, no file writes.")
        for a in candidates[:10]:
            print(f"  would process: {a.path.name} — title: {a.title!r}")
        if len(candidates) > 10:
            print(f"  ... and {len(candidates) - 10} more")
        return 0

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.stderr.write("ERROR: ANTHROPIC_API_KEY environment variable not set\n")
        return 1

    client = AsyncAnthropic(api_key=api_key)
    semaphore = asyncio.Semaphore(concurrency)
    print(f"Concurrency: {concurrency}\nModel: {MODEL}\nStarting...\n")

    start = time.monotonic()
    tasks = [generate_excerpt(client, a, config["name"], semaphore) for a in candidates]

    succeeded = 0
    failed: list[dict] = []
    done = 0
    for coro in asyncio.as_completed(tasks):
        article, excerpt, error = await coro
        done += 1
        if excerpt:
            try:
                write_excerpt(article, excerpt)
                succeeded += 1
            except Exception as e:
                failed.append({"path": str(article.path), "error": f"write failed: {e}"})
        else:
            failed.append({"path": str(article.path), "error": error})
        if done % 25 == 0 or done == len(tasks):
            elapsed = time.monotonic() - start
            rate = done / elapsed if elapsed > 0 else 0
            print(f"  {done}/{len(tasks)}  ({succeeded} ok, {len(failed)} failed)  {rate:.1f}/s")

    elapsed = time.monotonic() - start
    print(f"\nDone in {elapsed:.1f}s. {succeeded} succeeded, {len(failed)} failed.")

    if failed:
        FAILURES_LOG.parent.mkdir(parents=True, exist_ok=True)
        FAILURES_LOG.write_text(json.dumps(failed, indent=2), encoding="utf-8")
        print(f"Failures written to {FAILURES_LOG}")
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--language", required=True, choices=list(LANGUAGE_CONFIG.keys()))
    parser.add_argument("--dry-run", action="store_true", help="List files that would be processed; no API calls or writes.")
    parser.add_argument("--limit", type=int, help="Process at most N articles (for testing).")
    parser.add_argument("--concurrency", type=int, default=20, help="Parallel API requests (default: 20).")
    args = parser.parse_args()

    return asyncio.run(run(args.language, args.dry_run, args.limit, args.concurrency))


if __name__ == "__main__":
    sys.exit(main())
