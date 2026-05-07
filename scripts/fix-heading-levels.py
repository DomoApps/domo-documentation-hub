#!/usr/bin/env python3
"""
fix-heading-levels.py

Normalizes MDX heading hierarchy so that the first content heading is always ##.
Salesforce exported headings with a non-standard mapping; this script corrects them.

Transformation rules per article:
  - min_level == 2        → no change (already correct)
  - has_h3 AND has_h1     → Salesforce swap: ### → ##, # → ###, ## stays, #### stays
  - has_h3 AND NOT has_h1 → shift -1: all levels -1 (### → ##, #### → ###, …), never below ##
  - min_level == 1        → normalize: compress gaps, remap levels to start at ##
  - min_level >= 4        → shift up: all levels shifted so minimum becomes ##

Safe guards:
  - Skips lines inside fenced code blocks (``` … ```)
  - Skips YAML frontmatter (--- … ---)
  - Never shifts a heading below ## (level 2)
  - Dry-run by default: prints diffs, writes nothing
"""

import re
import sys
import glob
import os
from pathlib import Path

DRY_RUN = True  # Set to False to write changes

# ── helpers ────────────────────────────────────────────────────────────────────

def parse_heading_level(line):
    """Return heading level (1-6) if line is a heading, else None."""
    m = re.match(r'^(#{1,6})\s', line)
    return len(m.group(1)) if m else None


def get_heading_levels(lines):
    """
    Walk lines tracking frontmatter / code-block state.
    Return list of (line_index, level) for every real heading.
    """
    in_frontmatter = False
    in_code_block = False
    frontmatter_done = False
    results = []

    for i, line in enumerate(lines):
        stripped = line.rstrip()

        # --- Frontmatter detection ---
        if i == 0 and stripped == '---':
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == '---':
                in_frontmatter = False
                frontmatter_done = True
            continue

        # --- Code block detection ---
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        level = parse_heading_level(stripped)
        if level is not None:
            results.append((i, level))

    return results


def classify(levels_present, first_level):
    """Return transformation type string."""
    has_h1 = 1 in levels_present
    has_h3 = 3 in levels_present

    # Key off the FIRST heading level, not min_level.
    # An article can have ## deeper (e.g. a FAQ section) while starting with ###.
    if first_level == 2:
        return 'no_change'

    # H6 preamble pattern: localized release-notes articles open with ######
    # category labels followed by # / ## content. Only flag when the FIRST
    # heading is H6; H6 buried deep in an otherwise-normal article is fine.
    if first_level == 6:
        return 'manual_review'

    # salesforce_swap only applies when the article STARTS with ### (H3).
    # If the first heading is # (H1), the article uses a standard hierarchy
    # where # is top-level and ### are sub-sections — use shift instead.
    if first_level == 3 and has_h1:
        return 'salesforce_swap'

    if first_level == 3 and not has_h1:
        # shift_minus1: all levels -1; max(2, …) guard keeps existing ## at ##
        return 'shift_minus1'

    if first_level == 1:
        return 'normalize_from_h1'

    if first_level >= 4:
        # Only safe when the article is entirely #### (or ####/##### etc.) with no ##.
        # If ## is present alongside ####, they'd both collapse to ##; flag instead.
        if 2 in levels_present:
            return 'manual_review'
        return f'shift_up_{first_level - 2}'

    return 'no_change'


def build_level_map(transform_type, levels_present):
    """
    Return a dict {old_level: new_level} for ALL levels in this article.
    Levels not in the dict are unchanged.
    """
    if transform_type == 'no_change':
        return {}

    if transform_type == 'salesforce_swap':
        # ### → ##, # → ###, everything else unchanged
        return {3: 2, 1: 3}

    if transform_type == 'shift_minus1':
        # All levels decrease by 1, but never below 2
        return {lv: max(2, lv - 1) for lv in levels_present}

    if transform_type == 'normalize_from_h1':
        # Compress gaps: map levels in order to 2, 3, 4, …
        sorted_levels = sorted(levels_present)
        return {lv: i + 2 for i, lv in enumerate(sorted_levels)}

    if transform_type.startswith('shift_up_'):
        delta = int(transform_type.split('_')[-1])
        return {lv: max(2, lv - delta) for lv in levels_present}

    return {}


def transform_heading_line(line, level_map):
    """Replace the leading #s in a heading line per level_map."""
    m = re.match(r'^(#{1,6})(\s.*)', line)
    if not m:
        return line
    old_level = len(m.group(1))
    new_level = level_map.get(old_level, old_level)
    if new_level == old_level:
        return line
    return '#' * new_level + m.group(2)


# ── per-file processing ─────────────────────────────────────────────────────────

def process_file(filepath, dry_run=True, verbose=True):
    with open(filepath, encoding='utf-8') as f:
        original = f.read()

    lines = original.splitlines(keepends=True)
    heading_positions = get_heading_levels(lines)

    if not heading_positions:
        return None  # No headings, skip

    levels_present = set(lv for _, lv in heading_positions)
    first_level = heading_positions[0][1]
    transform_type = classify(levels_present, first_level)

    if transform_type == 'no_change':
        return None

    if transform_type == 'manual_review':
        if verbose:
            rel = os.path.relpath(filepath)
            print(f"\n{'='*70}")
            print(f"FILE: {rel}  [MANUAL REVIEW — skipped]")
            print(f"  levels present: {sorted(levels_present)}, first: {first_level}")
        return {'file': str(filepath), 'type': 'manual_review', 'levels': sorted(levels_present), 'changes': 0}

    level_map = build_level_map(transform_type, levels_present)

    # Build new lines
    new_lines = list(lines)
    changes = []
    for line_idx, old_level in heading_positions:
        new_level = level_map.get(old_level, old_level)
        if new_level != old_level:
            old_line = lines[line_idx].rstrip('\n')
            new_line_content = transform_heading_line(lines[line_idx].rstrip('\n'), level_map)
            new_lines[line_idx] = new_line_content + ('\n' if lines[line_idx].endswith('\n') else '')
            changes.append((line_idx + 1, old_line[:80], new_line_content[:80]))

    if not changes:
        return None

    new_content = ''.join(new_lines)

    if verbose:
        rel = os.path.relpath(filepath)
        print(f"\n{'='*70}")
        print(f"FILE: {rel}")
        print(f"TYPE: {transform_type}  |  levels present: {sorted(levels_present)}")
        print(f"MAP:  {level_map}")
        print(f"CHANGES ({len(changes)}):")
        for lineno, old, new in changes[:20]:  # cap at 20 per file
            print(f"  L{lineno:<5} {old}")
            print(f"       → {new}")
        if len(changes) > 20:
            print(f"  … and {len(changes) - 20} more")

    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return {
        'file': str(filepath),
        'type': transform_type,
        'levels': sorted(levels_present),
        'changes': len(changes),
    }


# ── main ────────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Fix MDX heading hierarchy.')
    parser.add_argument('paths', nargs='*', help='Files or glob patterns to process')
    parser.add_argument('--write', action='store_true', help='Write changes (default: dry-run)')
    parser.add_argument('--quiet', action='store_true', help='Suppress per-file diffs')
    parser.add_argument('--summary', action='store_true', help='Print summary table only')
    args = parser.parse_args()

    dry_run = not args.write
    verbose = not args.quiet and not args.summary

    if dry_run:
        print("DRY RUN — no files will be modified. Pass --write to apply.\n")

    files = []
    if args.paths:
        for pattern in args.paths:
            files.extend(glob.glob(pattern, recursive=True))
    else:
        for d in ['s/article', 'ja/s/article', 'de/s/article', 'es/s/article', 'fr/s/article']:
            files.extend(glob.glob(f'{d}/*.mdx'))

    files.sort()

    results = []
    for fp in files:
        r = process_file(fp, dry_run=dry_run, verbose=verbose)
        if r:
            results.append(r)

    # Summary
    from collections import Counter
    type_counts = Counter(r['type'] for r in results)
    total_changes = sum(r['changes'] for r in results)

    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"  Files scanned:  {len(files)}")
    print(f"  Files to touch: {len(results)}")
    print(f"  Heading lines:  {total_changes}")
    print(f"  By type:")
    for t, c in sorted(type_counts.items()):
        print(f"    {t:<30} {c} files")

    if dry_run:
        print("\nRun with --write to apply all changes.")


if __name__ == '__main__':
    main()
