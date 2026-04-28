#!/usr/bin/env python3
"""
Translates one or more MDX articles into Spanish, French, and German,
then saves each translation to the appropriate language directory.

Usage (pass paths as arguments):
    python3 scripts/localize_article.py s/article/360042924934.mdx
    python3 scripts/localize_article.py s/article/360042924934.mdx s/article/000005174.mdx

Usage (interactive — no arguments):
    python3 scripts/localize_article.py
"""

import anthropic
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

LANGUAGES = {
    "es": "Spanish",
    "fr": "French",
    "de": "German",
}

SYSTEM_PROMPT = """\
You are a technical documentation translator specializing in software product documentation.

When given an MDX article, translate ONLY the human-readable text into the target language.

Rules you MUST follow without exception:
- Preserve ALL MDX component tags exactly as-is: <Frame>, <Note>, <Warning>, <Tip>, <AccordionGroup>, <Accordion>, etc.
- Preserve ALL frontmatter keys exactly; only translate their string values (e.g., translate the title value but keep `title:` as the key)
- Preserve ALL image paths exactly (e.g., /images/kb/...)
- Preserve ALL internal links exactly (e.g., /s/article/...)
- Preserve ALL markdown formatting: **, *, `code`, |table|, ---, ###, etc.
- Preserve ALL JSX attribute names and syntax exactly (e.g., title="..." stays as title="...")
- Do NOT translate: UI element names shown in bold within product instructions (e.g., **Chart Properties**, **General > Value**, **Analyzer**) — these are proper names of UI elements and must remain in English
- Do NOT translate: technical terms used as proper names (e.g., DataSet, Beast Mode, Analyzer, Radial Gauge)
- Do NOT add any commentary, preamble, or explanation — return only the translated MDX content
- Return the complete file, not a summary or excerpt
"""

def translate_article(source_text: str, target_language: str, lang_code: str) -> str:
    client = anthropic.Anthropic()

    user_prompt = f"""\
Translate the following MDX article into {target_language}.
Return only the translated MDX file content — no explanation, no code fences.

{source_text}"""

    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=8192,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    ) as stream:
        translated = stream.get_final_message()

    # Extract text from response
    text_blocks = [b.text for b in translated.content if b.type == "text"]
    result = "\n".join(text_blocks).strip()

    # Strip accidental code fences if Claude wrapped the output
    if result.startswith("```"):
        lines = result.splitlines()
        # Drop the opening fence line and any closing fence
        inner = lines[1:]
        if inner and inner[-1].strip().startswith("```"):
            inner = inner[:-1]
        result = "\n".join(inner).strip()

    return result


def localize(article_path: str) -> None:
    source_path = REPO_ROOT / article_path
    if not source_path.exists():
        print(f"  Error: file not found: {source_path}")
        return

    source_text = source_path.read_text(encoding="utf-8")
    filename = source_path.name  # e.g. 360042924934.mdx

    for lang_code, lang_name in LANGUAGES.items():
        dest_dir = REPO_ROOT / lang_code / "s" / "article"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / filename

        print(f"  Translating to {lang_name} ({lang_code})...", end=" ", flush=True)
        translated = translate_article(source_text, lang_name, lang_code)
        dest_path.write_text(translated, encoding="utf-8")
        print(f"saved → {dest_path.relative_to(REPO_ROOT)}")


def collect_paths_interactively() -> list[str]:
    print("Enter article paths relative to the repo root, one per line.")
    print("Press Enter on a blank line when done.")
    print("Example: s/article/360042924934.mdx\n")
    paths = []
    while True:
        try:
            line = input("Article path: ").strip()
        except EOFError:
            break
        if not line:
            break
        paths.append(line)
    return paths


if __name__ == "__main__":
    article_paths = sys.argv[1:] if len(sys.argv) > 1 else collect_paths_interactively()

    if not article_paths:
        sys.exit("No article paths provided. Exiting.")

    for i, path in enumerate(article_paths, 1):
        print(f"\n[{i}/{len(article_paths)}] {path}")
        localize(path)

    print("\nAll done.")
