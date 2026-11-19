#!/usr/bin/env python3
"""Deterministic glossary-compliance check for a localized article.

Given an English source file, its translation, and the target language, verify
that the translation honors the deterministic glossary
(``localization/glossary/<lang>.csv``):

* **keep-in-English terms** that appear in the English source must appear
  verbatim (still in English) in the translation.
* **translated terms** that appear in the English source should have one of their
  approved target renderings present in the translation.

This is a heuristic aid, not a hard gate: it reports likely violations so the
`localize` skill (or a human) can fix them. Callout-label and section-header
rows are skipped here — the skill's language-specific checklist covers those.

Usage:
    python3 scripts/check-glossary.py <english.mdx> <translated.mdx> <lang>

    lang in {es, fr, de, ja}

Exit code is 0 when no likely violations are found, 1 otherwise (so the check
can be scripted), but the report is always printed.
"""

import csv
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOSSARY_DIR = os.path.join(REPO_ROOT, "localization", "glossary")
SKIP_CONTEXTS = {"callout-label", "section-header"}


def load_glossary(lang):
    path = os.path.join(GLOSSARY_DIR, f"{lang}.csv")
    if not os.path.exists(path):
        sys.exit(f"ERROR: no glossary at {path}")
    keep_en, translated = [], {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("context") in SKIP_CONTEXTS:
                continue
            term = row["english_term"]
            if row.get("keep_in_english") == "yes":
                keep_en.append(term)
            elif row.get("translation"):
                # group acceptable renderings across contexts
                translated.setdefault(term, set()).add(row["translation"])
    return keep_en, translated


def strip_code(text):
    """Remove fenced code blocks and inline code so term matching ignores them."""
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", " ", text)
    return text


def english_contains(text, term):
    """Whole-word / phrase presence of an English term (case-insensitive)."""
    pattern = r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])"
    return re.search(pattern, text, re.IGNORECASE) is not None


def kept_in_english(text, term):
    """True if the term (or its singular/plural variant) is present verbatim.

    Brand terms often appear pluralized in English (``DataSets``) but unchanged
    and unpluralized in the translation (``DataSet``); accept either form.
    """
    variants = {term}
    if term.endswith("s"):
        variants.add(term[:-1])
    else:
        variants.add(term + "s")
    return any(english_contains(text, v) for v in variants)


def main():
    if len(sys.argv) != 4:
        sys.exit("Usage: check-glossary.py <english.mdx> <translated.mdx> <lang>")
    en_path, tr_path, lang = sys.argv[1], sys.argv[2], sys.argv[3]
    if lang not in ("es", "fr", "de", "ja"):
        sys.exit(f"ERROR: lang must be one of es/fr/de/ja, got {lang!r}")
    for p in (en_path, tr_path):
        if not os.path.exists(p):
            sys.exit(f"ERROR: file not found: {p}")

    keep_en, translated = load_glossary(lang)
    en_text = strip_code(open(en_path, encoding="utf-8").read())
    tr_raw = open(tr_path, encoding="utf-8").read()
    tr_text = strip_code(tr_raw)

    keep_violations = []   # term should be kept in EN but is missing from translation
    term_violations = []   # expected translation missing

    for term in keep_en:
        if english_contains(en_text, term) and not kept_in_english(tr_text, term):
            keep_violations.append(term)

    for term, renderings in translated.items():
        if not english_contains(en_text, term):
            continue
        if not any(r in tr_text for r in renderings):
            term_violations.append((term, sorted(renderings)))

    print(f"Glossary check - {os.path.basename(tr_path)} ({lang})")
    print(f"  glossary: {len(keep_en)} keep-in-EN, {len(translated)} translated terms")

    if keep_violations:
        print(f"\n  [!] Keep-in-English terms present in the source but MISSING verbatim "
              f"in the translation ({len(keep_violations)}):")
        for t in keep_violations:
            print(f"      - {t}  (must stay in English)")

    if term_violations:
        print(f"\n  [!] Source terms whose approved translation was NOT found "
              f"({len(term_violations)}):")
        for term, renderings in term_violations:
            print(f"      - {term}  -> expected one of: {', '.join(renderings)}")

    total = len(keep_violations) + len(term_violations)
    if total == 0:
        print("\n  OK: no likely glossary violations found.")
        return 0
    print(f"\n  {total} item(s) to review. These are heuristic - confirm each against "
          "context before editing (some terms legitimately do not appear, and "
          "multi-context terms may use a different approved rendering).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
