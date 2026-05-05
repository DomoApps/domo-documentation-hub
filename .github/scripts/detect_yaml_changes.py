#!/usr/bin/env python3
"""
Detect changed YAML files in source repository.

Compares source YAMLs against destination YAMLs by SHA-256 content hash
(mtimes are unreliable after a fresh actions/checkout). Writes
changed_files.txt with source paths of files needing sync, plus
GitHub Actions outputs `changed_files` and `summary`.
"""

import os
import sys
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Tuple


def find_yaml_files(source_dir: str) -> List[str]:
    """Find all YAML files in source directory"""
    yaml_files = []
    source_path = Path(source_dir)

    for ext in ["*.yaml", "*.yml"]:
        yaml_files.extend(source_path.glob(f"**/{ext}"))

    return [str(f) for f in yaml_files]


def file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def detect_changes(
    source_dir: str, dest_dir: str, force: bool = False
) -> Tuple[List[str], Dict[str, List[str]]]:
    """Detect which YAML files need syncing."""
    changed_files = []
    summary = {"new_files": [], "modified_files": [], "unchanged_files": []}

    yaml_files = find_yaml_files(source_dir)
    print(f"Found {len(yaml_files)} YAML files in source")

    # Build case-insensitive lookup for destination files
    dest_files_lower = {}
    if os.path.exists(dest_dir):
        dest_files_lower = {
            f.lower(): f
            for f in os.listdir(dest_dir)
            if f.lower().endswith((".yaml", ".yml"))
        }

    for yaml_file in yaml_files:
        yaml_filename = os.path.basename(yaml_file)
        dest_actual = dest_files_lower.get(yaml_filename.lower())
        if dest_actual:
            dest_file_path = os.path.join(dest_dir, dest_actual)
        else:
            dest_file_path = os.path.join(dest_dir, yaml_filename)

        if not os.path.exists(dest_file_path):
            print(f"NEW: {yaml_filename}")
            changed_files.append(yaml_file)
            summary["new_files"].append(yaml_filename)
            continue

        if force:
            print(f"FORCE: {yaml_filename}")
            changed_files.append(yaml_file)
            summary["modified_files"].append(yaml_filename)
            continue

        src_hash = file_sha256(yaml_file)
        dest_hash = file_sha256(dest_file_path)

        # Also treat a case-only filename change as a modification so sync
        # runs and normalizes the destination filename.
        case_changed = dest_actual is not None and dest_actual != yaml_filename

        if src_hash != dest_hash or case_changed:
            reason = "content differs" if src_hash != dest_hash else "case rename"
            print(f"MODIFIED: {yaml_filename} ({reason})")
            changed_files.append(yaml_file)
            summary["modified_files"].append(yaml_filename)
        else:
            print(f"UNCHANGED: {yaml_filename}")
            summary["unchanged_files"].append(yaml_filename)

    return changed_files, summary


def create_summary_markdown(summary: Dict[str, List[str]]) -> str:
    lines = []

    total_changes = len(summary["new_files"]) + len(summary["modified_files"])
    lines.append(f"**Total files to sync:** {total_changes}")
    lines.append("")

    if summary["new_files"]:
        lines.append(f"**New Files ({len(summary['new_files'])}):**")
        for f in summary["new_files"]:
            lines.append(f"- `{f}`")
        lines.append("")

    if summary["modified_files"]:
        lines.append(f"**Modified Files ({len(summary['modified_files'])}):**")
        for f in summary["modified_files"]:
            lines.append(f"- `{f}`")
        lines.append("")

    if summary["unchanged_files"]:
        lines.append(f"**Unchanged Files ({len(summary['unchanged_files'])}):**")
        lines.append(
            f"_{len(summary['unchanged_files'])} files are already up-to-date_"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Detect changed YAML files")
    parser.add_argument(
        "--source", required=True, help="Source directory with YAML files"
    )
    parser.add_argument(
        "--dest", required=True, help="Destination directory with YAML files"
    )
    parser.add_argument("--force", default="false", help="Force sync all files")

    args = parser.parse_args()
    force = args.force.lower() == "true"

    changed_files, summary = detect_changes(args.source, args.dest, force=force)

    with open("changed_files.txt", "w") as f:
        for file_path in changed_files:
            f.write(f"{file_path}\n")

    changed_files_str = "\n".join(changed_files)
    output_file = os.environ.get("GITHUB_OUTPUT", "/dev/stdout")
    with open(output_file, "a") as f:
        f.write(f"changed_files<<EOF\n{changed_files_str}\nEOF\n")

    summary_md = create_summary_markdown(summary)
    with open(output_file, "a") as f:
        f.write(f"summary<<EOF\n{summary_md}\nEOF\n")

    print(f"\n{'='*60}")
    print(f"Detection complete: {len(changed_files)} files to sync")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
